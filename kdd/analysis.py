# Run from this project directory. Generated from the executed notebook.

# Optional fresh-runtime installation (uncomment if needed):
# %pip install numpy==2.0.2 pandas==2.3.3 scikit-learn==1.6.1 matplotlib==3.9.4 joblib==1.5.3 requests==2.32.5 tabulate==0.9.0

from pathlib import Path
import io, json, hashlib, zipfile, platform, warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn, joblib, requests
from IPython.display import display
from sklearn.base import clone
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, FunctionTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold, GroupShuffleSplit, GroupKFold
from sklearn.metrics import *
SEED = 42
np.random.seed(SEED)
plt.rcParams.update({'figure.figsize': (9,5), 'axes.spines.top':False, 'axes.spines.right':False})
ART = Path('artifacts'); ART.mkdir(exist_ok=True)
def save_json(name, value):
    (ART/name).write_text(json.dumps(value, indent=2, default=lambda x: x.item() if hasattr(x,'item') else str(x)))
def figure(name):
    plt.tight_layout(); plt.savefig(ART/name, dpi=150, bbox_inches='tight'); plt.show(); plt.close()
def load_kaggle(slug, filename, expected):
    path = Path('data')/filename
    if not path.exists():
        path.parent.mkdir(exist_ok=True)
        response=requests.get('https://www.kaggle.com/api/v1/datasets/download/'+slug, timeout=120)
        response.raise_for_status()
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            matches=[n for n in z.namelist() if Path(n).name == filename]
            if len(matches)!=1: raise ValueError('Expected exactly one matching CSV in archive')
            path.write_bytes(z.read(matches[0]))
    actual=hashlib.sha256(path.read_bytes()).hexdigest()
    assert actual == expected, 'Dataset version changed; inspect before continuing'
    print('Verified SHA-256:',actual)
    return pd.read_csv(path)
def quality_report(df):
    out=pd.DataFrame({'dtype':df.dtypes.astype(str),'missing':df.isna().sum(),'unique':df.nunique()})
    out.to_csv(ART/'data_quality.csv'); display(out)
    print('Rows:',len(df),'Exact duplicates:',int(df.duplicated().sum()))
def bootstrap_ci(y, pred, metric, n=500):
    rng=np.random.default_rng(SEED); y=np.asarray(y); pred=np.asarray(pred); vals=[]
    for _ in range(n):
        ix=rng.integers(0,len(y),len(y))
        try: vals.append(metric(y[ix],pred[ix]))
        except ValueError: pass
    return np.quantile(vals,[.025,.975]).tolist()
save_json('environment.json',{'python':platform.python_version(),'numpy':np.__version__,'pandas':pd.__version__,'scikit_learn':sklearn.__version__,'seed':SEED})


raw=load_kaggle('arjunbhasin2013/ccdata','CC GENERAL.csv','29eea6389837c40fd760c927b5782563edeff55a37824598489716bdb3563be1')
assert raw.CUST_ID.is_unique
quality_report(raw)
anomaly_count=int((raw['CASH_ADVANCE_FREQUENCY']>1).sum())
print('Cash-advance frequency values above 1:',anomaly_count)
save_json('quality_decision.json',{'cash_advance_frequency_above_one':anomaly_count,'decision':'Exclude ambiguous CASH_ADVANCE_FREQUENCY; retain CASH_ADVANCE and CASH_ADVANCE_TRX'})
features=[c for c in raw if c not in ['CUST_ID','CASH_ADVANCE_FREQUENCY']];X=raw[features].copy()
assert (X.dropna()>=0).all().all()
tr,rest=train_test_split(X.index,test_size=.4,random_state=SEED);va,te=train_test_split(rest,test_size=.5,random_state=SEED)
assert not(set(tr)&set(va) or set(tr)&set(te) or set(va)&set(te))
Xtr,Xv,Xte=X.loc[tr],X.loc[va],X.loc[te]
part=pd.Series('train',index=X.index);part.loc[va]='validation';part.loc[te]='test';pd.DataFrame({'row_id':X.index,'partition':part}).to_csv(ART/'split_manifest.csv',index=False)
print('Discovery/validation/test:',len(tr),len(va),len(te))


frequency=[c for c in features if 'FREQUENCY' in c or c=='PRC_FULL_PAYMENT']
assert X[frequency].stack().between(0,1).all()
logcols=[c for c in features if c not in frequency+['TENURE']]
Xtr[logcols].hist(bins=35,figsize=(13,9));figure('training_distributions.png')
eda=pd.DataFrame({'missing':Xtr.isna().sum(),'median':Xtr.median(),'skew':Xtr.skew(),'max':Xtr.max()});display(eda);eda.to_csv(ART/'training_eda.csv')


def make_pre(log=True):
    amount=Pipeline([('impute',SimpleImputer(strategy='median')),('transform',FunctionTransformer(np.log1p,feature_names_out='one-to-one') if log else FunctionTransformer(feature_names_out='one-to-one')),('scale',StandardScaler())])
    other=Pipeline([('impute',SimpleImputer(strategy='median')),('scale',StandardScaler())])
    return ColumnTransformer([('amount',amount,logcols),('other',other,[c for c in features if c not in logcols])])
save_json('schema.json',{'features':features,'numeric':features,'categorical':[],'frequency':frequency,'log_columns':logcols,'numeric_ranges':{c:[float(Xtr[c].min()),float(Xtr[c].max())] for c in features}})


from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA
models={};rows=[]
for rep in ['raw','log']:
    pre=make_pre(rep=='log');zt=pre.fit_transform(Xtr);zv=pre.transform(Xv)
    for algorithm in (['kmeans','gmm'] if rep=='log' else ['kmeans']):
        for k in range(2,7):
            est=KMeans(n_clusters=k,n_init=20,random_state=SEED) if algorithm=='kmeans' else GaussianMixture(n_components=k,covariance_type='diag',n_init=3,reg_covar=1e-5,random_state=SEED)
            est.fit(zt);labels=est.predict(zv);key=f'{rep}_{algorithm}_{k}'
            share=np.bincount(labels,minlength=k)/len(labels)
            row={'candidate':key,'representation':rep,'algorithm':algorithm,'k':k,'silhouette':silhouette_score(zv,labels,sample_size=min(1500,len(zv)),random_state=SEED),'davies_bouldin':davies_bouldin_score(zv,labels),'minimum_share':share.min()}
            rows.append(row);models[key]=Pipeline([('pre',pre),('model',est)])
comparison=pd.DataFrame(rows);eligible=comparison[comparison.minimum_share>=.05];selection=eligible if len(eligible) else comparison
winner=selection.sort_values('silhouette',ascending=False).iloc[0]['candidate'];model=models[winner];choice=comparison.set_index('candidate').loc[winner]
comparison.to_csv(ART/'model_comparison.csv',index=False);display(comparison.sort_values('silhouette',ascending=False));print('Frozen winner:',winner)
base_labels=model.predict(Xv);aris=[]
for seed in range(5):
    idx=np.random.default_rng(seed).choice(len(Xtr),size=int(.8*len(Xtr)),replace=False)
    alternative=clone(model);alternative.set_params(model__random_state=seed);alternative.fit(Xtr.iloc[idx])
    aris.append(adjusted_rand_score(base_labels,alternative.predict(Xv)))
print('Validation resampling ARIs:',aris)


ztr=model.named_steps['pre'].transform(Xtr);zte=model.named_steps['pre'].transform(Xte);labels=model.predict(Xte);k=int(choice['k'])
shares=np.bincount(labels,minlength=k)/len(labels)
metrics={'winner':winner,'test_silhouette':silhouette_score(zte,labels,sample_size=min(1500,len(zte)),random_state=SEED),'test_davies_bouldin':davies_bouldin_score(zte,labels),'test_cluster_shares':shares.tolist(),'validation_resampling_ARI':aris,'median_ARI':float(np.median(aris))}
metrics['proxy_gate_passed']=bool(metrics['test_silhouette']>=.2 and shares.min()>=.05 and np.median(aris)>=.7)
profile=Xte.assign(cluster=labels).groupby('cluster').median();profile.insert(0,'n',np.bincount(labels,minlength=k));display(profile);profile.to_csv(ART/'test_cluster_profiles.csv')
pd.DataFrame({'row_id':te,'cluster':labels}).to_csv(ART/'test_assignments.csv',index=False)
pca=PCA(n_components=2,random_state=SEED).fit(ztr);plot=pca.transform(zte);metrics['PCA_2d_variance']=float(pca.explained_variance_ratio_.sum());save_json('metrics.json',metrics)
plt.scatter(plot[:,0],plot[:,1],c=labels,cmap='tab10',s=12,alpha=.45);plt.xlabel('PC1');plt.ylabel('PC2');plt.title(f'Held-out segments; 2D variance = {metrics["PCA_2d_variance"]:.1%}');figure('test_pca.png')
scaled=pd.DataFrame(zte).assign(cluster=labels).groupby('cluster').mean()
plt.figure(figsize=(13,4));plt.imshow(scaled,aspect='auto',cmap='RdBu_r',vmin=-2,vmax=2);plt.xticks(range(zte.shape[1]),model.named_steps['pre'].get_feature_names_out(),rotation=90);plt.yticks(range(k),range(k));plt.colorbar(label='Mean transformed standardized value');figure('test_segment_heatmap.png')
print(json.dumps(metrics,indent=2))


joblib.dump(model,ART/'model.joblib');restored=joblib.load(ART/'model.joblib');np.testing.assert_array_equal(restored.predict(Xte),labels)
Xte.iloc[:5].to_csv(ART/'sample_input.csv',index=False);pd.DataFrame({'cluster':restored.predict(Xte.iloc[:5])}).to_csv(ART/'sample_output.csv',index=False)
sample=Xte.iloc[:5].copy();sample.iloc[0,0]=np.nan;assert len(restored.predict(sample))==5
save_json('verification.json',{'disjoint_splits':True,'pipeline_roundtrip':True,'missing_input_handled':True,'all_clusters_observed':bool((shares>0).all()),'human_review_completed':False})
print('Assignment pipeline saved. Proxy gate:',metrics['proxy_gate_passed'])
