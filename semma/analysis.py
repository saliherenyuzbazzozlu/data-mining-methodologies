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


raw=load_kaggle('uciml/red-wine-quality-cortez-et-al-2009','winequality-red.csv','d6a0d9bd24806944818795f22500c46cb6424cbff517aacda36595d3ed9b2daa')
quality_report(raw)
df=raw.drop_duplicates().copy(); features=[c for c in df if c!='quality']; X=df[features]; y=df.quality
assert np.isfinite(df.to_numpy()).all() and y.between(0,10).all()
assert (X>=0).all().all()
groups=pd.util.hash_pandas_object(X,index=False)
tr,rest=next(GroupShuffleSplit(n_splits=1,test_size=.4,random_state=SEED).split(X,y,groups))
va0,te0=next(GroupShuffleSplit(n_splits=1,test_size=.5,random_state=SEED).split(X.iloc[rest],y.iloc[rest],groups.iloc[rest]))
va,te=rest[va0],rest[te0]
assert not(set(groups.iloc[tr])&set(groups.iloc[va]) or set(groups.iloc[tr])&set(groups.iloc[te]) or set(groups.iloc[va])&set(groups.iloc[te]))
Xtr,Xv,Xte=X.iloc[tr],X.iloc[va],X.iloc[te];ytr,yv,yte=y.iloc[tr],y.iloc[va],y.iloc[te]
part=np.full(len(df),'train',dtype=object);part[va]='validation';part[te]='test'
pd.DataFrame({'source_row':df.index,'feature_group':groups.to_numpy(),'partition':part}).to_csv(ART/'split_manifest.csv',index=False)
save_json('sample_audit.json',{'raw_n':len(raw),'unique_n':len(df),'exact_duplicates_removed':len(raw)-len(df),'n_train':len(tr),'n_validation':len(va),'n_test':len(te),'feature_groups':groups.nunique()})
display(pd.crosstab(pd.Series(part),pd.Series(y.to_numpy())))


ytr.value_counts().sort_index().plot.bar(color='#8b4663',title='Training sensory score distribution',ylabel='Wines');figure('training_quality_distribution.png')
Xtr.hist(bins=25,figsize=(13,9));figure('training_chemistry.png')
corr=Xtr.assign(quality=ytr).corr();plt.figure(figsize=(10,8));plt.imshow(corr,cmap='RdBu_r',vmin=-1,vmax=1);plt.xticks(range(len(corr)),corr.columns,rotation=90);plt.yticks(range(len(corr)),corr.columns);plt.colorbar(label='Pearson correlation');figure('training_correlations.png')
eda=pd.DataFrame({'skew':Xtr.skew(),'min':Xtr.min(),'median':Xtr.median(),'max':Xtr.max(),'quality_correlation':corr.quality.drop('quality')});display(eda);eda.to_csv(ART/'training_eda.csv')


from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.dummy import DummyRegressor
pre=Pipeline([('impute',SimpleImputer(strategy='median')),('scale',StandardScaler())])
save_json('schema.json',{'features':features,'numeric':features,'categorical':[],'numeric_ranges':{c:[float(Xtr[c].min()),float(Xtr[c].max())] for c in features}})


configs={'ridge':(Ridge(),{'model__alpha':[.1,1.,10.,100.],'select__k':[8,'all']}),'random_forest':(RandomForestRegressor(n_estimators=150,random_state=SEED,n_jobs=1),{'model__min_samples_leaf':[1,3,8],'select__k':['all']})}
models={};rows=[]
for name,(est,grid) in configs.items():
    pipe=Pipeline([('pre',clone(pre)),('select',SelectKBest(f_regression,k='all')),('model',est)])
    search=GridSearchCV(pipe,grid,scoring='neg_root_mean_squared_error',cv=GroupKFold(3),n_jobs=1)
    search.fit(Xtr,ytr,groups=groups.iloc[tr]);models[name]=search.best_estimator_
    pd.DataFrame(search.cv_results_).to_csv(ART/(name+'_cv.csv'),index=False)
    rows.append({'model':name,'cv_RMSE':-search.best_score_,'validation_RMSE':root_mean_squared_error(yv,search.predict(Xv)),'parameters':str(search.best_params_)})
comparison=pd.DataFrame(rows).sort_values('validation_RMSE');display(comparison);comparison.to_csv(ART/'model_comparison.csv',index=False)
winner=comparison.iloc[0]['model'];model=models[winner];baseline=DummyRegressor(strategy='mean').fit(Xtr,ytr)
print('Frozen winner:',winner)


def reg_metrics(y,p):
    return {'RMSE':root_mean_squared_error(y,p),'MAE':mean_absolute_error(y,p),'R2':r2_score(y,p),'within_one_point':float(np.mean(np.abs(np.asarray(y)-p)<=1))}
pv=model.predict(Xv);pt=model.predict(Xte);pb=baseline.predict(Xte)
metrics={'winner':winner,'validation':reg_metrics(yv,pv),'test':reg_metrics(yte,pt),'test_baseline':reg_metrics(yte,pb),'test_RMSE_CI95':bootstrap_ci(yte,pt,root_mean_squared_error)}
metrics['RMSE_relative_improvement']=1-metrics['test']['RMSE']/metrics['test_baseline']['RMSE'];metrics['proxy_gate_passed']=bool(metrics['RMSE_relative_improvement']>=.1)
save_json('metrics.json',metrics);display(pd.DataFrame({k:v for k,v in metrics.items() if isinstance(v,dict)}).T)
pred=pd.DataFrame({'source_row':df.index[te],'observed':yte.to_numpy(),'predicted':pt,'residual':yte.to_numpy()-pt});pred.to_csv(ART/'test_predictions.csv',index=False)
by=pred.groupby('observed').agg(n=('residual','size'),mean_residual=('residual','mean'),MAE=('residual',lambda x:abs(x).mean()));display(by);by.to_csv(ART/'quality_error.csv')
fig,axs=plt.subplots(1,2,figsize=(11,4));axs[0].scatter(yte,pt,alpha=.4);axs[0].plot([3,8],[3,8],'k--');axs[0].set(xlabel='Observed quality',ylabel='Predicted quality');axs[1].scatter(pt,yte.to_numpy()-pt,alpha=.4);axs[1].axhline(0,color='k');axs[1].set(xlabel='Prediction',ylabel='Observed minus predicted');figure('test_residuals.png')
from sklearn.inspection import permutation_importance
imp=permutation_importance(model,Xv,yv,scoring='neg_root_mean_squared_error',n_repeats=5,random_state=SEED,n_jobs=1)
importance=pd.DataFrame({'feature':features,'RMSE_increase':imp.importances_mean,'sd':imp.importances_std}).sort_values('RMSE_increase',ascending=False);display(importance);importance.to_csv(ART/'validation_importance.csv',index=False)


joblib.dump(model,ART/'model.joblib');restored=joblib.load(ART/'model.joblib');np.testing.assert_allclose(restored.predict(Xte),pt)
Xte.iloc[:5].to_csv(ART/'sample_input.csv',index=False);pd.DataFrame({'predicted_quality':restored.predict(Xte.iloc[:5])}).to_csv(ART/'sample_output.csv',index=False)
sample=Xte.iloc[:5].copy();sample.iloc[0,0]=np.nan;assert np.isfinite(restored.predict(sample)).all()
save_json('verification.json',{'disjoint_feature_groups':True,'pipeline_roundtrip':True,'missing_measurement':True,'finite_predictions':bool(np.isfinite(pt).all()),'human_review_completed':False})
print('Saved pipeline. Proxy gate:',metrics['proxy_gate_passed'])
