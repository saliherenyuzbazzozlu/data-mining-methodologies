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


raw=load_kaggle('blastchar/telco-customer-churn','WA_Fn-UseC_-Telco-Customer-Churn.csv','88be4b93fbe0cc83421af1c503794c97c342eca914c1576db7c276e61d61358a')
df=raw.copy(); df['TotalCharges']=pd.to_numeric(df['TotalCharges'],errors='coerce')
assert df.customerID.is_unique and set(df.Churn)=={'Yes','No'}
assert (df[['tenure','MonthlyCharges','TotalCharges']].dropna()>=0).all().all()
quality_report(df)
y=df.Churn.eq('Yes').astype(int)
train_idx,other_idx=train_test_split(df.index,test_size=.4,stratify=y,random_state=SEED)
val_idx,test_idx=train_test_split(other_idx,test_size=.5,stratify=y.loc[other_idx],random_state=SEED)
assert not(set(train_idx)&set(val_idx) or set(train_idx)&set(test_idx) or set(val_idx)&set(test_idx))
splits=pd.Series('train',index=df.index);splits.loc[val_idx]='validation';splits.loc[test_idx]='test'
pd.DataFrame({'row_id':df.index,'partition':splits}).to_csv(ART/'split_manifest.csv',index=False)
display(pd.DataFrame({'partition':splits,'churn':y}).groupby('partition').agg(n=('churn','size'),prevalence=('churn','mean')))
train=df.loc[train_idx].copy()
train[['tenure','MonthlyCharges','TotalCharges']].hist(bins=30,figsize=(10,6));figure('training_distributions.png')
train.assign(churn=y.loc[train_idx]).groupby('Contract').churn.mean().sort_values().plot.bar(color='#287c8e',ylabel='Observed churn fraction',title='Training data: churn by contract');figure('training_contract_churn.png')
print('Training charge/tenure correlations:'); display(train[['tenure','MonthlyCharges','TotalCharges']].corr())


features=[c for c in df if c not in ['customerID','Churn','gender','SeniorCitizen']]
X=df[features]; numeric=['tenure','MonthlyCharges','TotalCharges']; categorical=[c for c in features if c not in numeric]
pre=ColumnTransformer([('num',Pipeline([('impute',SimpleImputer(strategy='median')),('scale',StandardScaler())]),numeric),('cat',Pipeline([('impute',SimpleImputer(strategy='most_frequent')),('encode',OneHotEncoder(handle_unknown='ignore',sparse_output=False))]),categorical)])
Xtr,Xv,Xte=X.loc[train_idx],X.loc[val_idx],X.loc[test_idx]
ytr,yv,yte=y.loc[train_idx],y.loc[val_idx],y.loc[test_idx]
save_json('schema.json',{'features':features,'numeric':numeric,'categorical':categorical,'excluded':['customerID','Churn','gender','SeniorCitizen'],'categories':{c:sorted(Xtr[c].dropna().unique().tolist()) for c in categorical},'numeric_ranges':{c:[float(Xtr[c].min()),float(Xtr[c].max())] for c in numeric}})


from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.dummy import DummyClassifier
cv=StratifiedKFold(n_splits=3,shuffle=True,random_state=SEED)
configs={'logistic':(LogisticRegression(max_iter=2000,random_state=SEED),{'model__C':[.1,1.,10.]}),'random_forest':(RandomForestClassifier(n_estimators=150,max_features='sqrt',random_state=SEED,n_jobs=1),{'model__min_samples_leaf':[3,10]})}
models={}; rows=[]
for name,(est,grid) in configs.items():
    search=GridSearchCV(Pipeline([('pre',clone(pre)),('model',est)]),grid,scoring='average_precision',cv=cv,n_jobs=1)
    search.fit(Xtr,ytr); models[name]=search.best_estimator_
    pd.DataFrame(search.cv_results_).to_csv(ART/(name+'_cv.csv'),index=False)
    rows.append({'model':name,'cv_AP':search.best_score_,'validation_AP':average_precision_score(yv,search.predict_proba(Xv)[:,1]),'parameters':str(search.best_params_)})
comparison=pd.DataFrame(rows).sort_values('validation_AP',ascending=False,kind='stable');display(comparison);comparison.to_csv(ART/'model_comparison.csv',index=False)
winner=comparison.iloc[0]['model']; model=models[winner]
baseline=DummyClassifier(strategy='prior').fit(Xtr,ytr)
print('Frozen winner:',winner)


def ranked_metrics(y,p):
    yy=np.asarray(y); n=max(1,int(.2*len(yy))); ix=np.argsort(-np.asarray(p),kind='stable')[:n]
    precision=yy[ix].mean(); return {'precision_at_20pct':float(precision),'recall_at_20pct':float(yy[ix].sum()/yy.sum()),'lift_at_20pct':float(precision/yy.mean()),'contacts':n}
def clf_metrics(y,p):
    return {'AP':average_precision_score(y,p),'ROC_AUC':roc_auc_score(y,p),'Brier':brier_score_loss(y,p),'accuracy_0.5':accuracy_score(y,np.asarray(p)>=.5),**ranked_metrics(y,p)}
pv=model.predict_proba(Xv)[:,1]; pt=model.predict_proba(Xte)[:,1]; pb=baseline.predict_proba(Xte)[:,1]
metrics={'winner':winner,'validation':clf_metrics(yv,pv),'test':clf_metrics(yte,pt),'test_baseline':clf_metrics(yte,pb),'test_AP_CI95':bootstrap_ci(yte,pt,average_precision_score),'test_lift_CI95':bootstrap_ci(yte,pt,lambda a,b:ranked_metrics(a,b)['lift_at_20pct'])}
metrics['proxy_gate_passed']=bool(metrics['test']['lift_at_20pct']>=2 and metrics['test']['AP']>yte.mean())
save_json('metrics.json',metrics);display(pd.DataFrame({k:v for k,v in metrics.items() if isinstance(v,dict)}).T)
pd.DataFrame({'row_id':test_idx,'observed':yte.to_numpy(),'probability':pt}).to_csv(ART/'test_predictions.csv',index=False)
fig,axs=plt.subplots(1,2,figsize=(11,4));RocCurveDisplay.from_predictions(yte,pt,ax=axs[0]);PrecisionRecallDisplay.from_predictions(yte,pt,ax=axs[1]);figure('test_discrimination.png')
ConfusionMatrixDisplay.from_predictions(yte,pt>=.5,display_labels=['Stay','Churn']);figure('test_confusion.png')
from sklearn.calibration import CalibrationDisplay
CalibrationDisplay.from_predictions(yte,pt,n_bins=8,strategy='quantile');figure('test_calibration.png')
group_rows=[]
for col in ['gender','SeniorCitizen']:
    for value,idx in df.loc[test_idx].groupby(col).groups.items():
        mask=pd.Index(test_idx).isin(idx); yy=yte.to_numpy()[mask]; pp=pt[mask]; pred=pp>=.5
        group_rows.append({'attribute':col,'group':str(value),'n':len(yy),'prevalence':yy.mean(),'AP':average_precision_score(yy,pp),'TPR_0.5':recall_score(yy,pred,zero_division=0),'FPR_0.5':float(pred[yy==0].mean())})
groups=pd.DataFrame(group_rows);display(groups);groups.to_csv(ART/'subgroup_metrics.csv',index=False)
from sklearn.inspection import permutation_importance
imp=permutation_importance(model,Xv,yv,scoring='average_precision',n_repeats=5,random_state=SEED,n_jobs=1)
importance=pd.DataFrame({'feature':features,'AP_drop':imp.importances_mean,'sd':imp.importances_std}).sort_values('AP_drop',ascending=False)
importance.to_csv(ART/'validation_importance.csv',index=False);display(importance.head(10))


joblib.dump(model,ART/'model.joblib'); restored=joblib.load(ART/'model.joblib')
np.testing.assert_allclose(restored.predict_proba(Xte.iloc[:20]),model.predict_proba(Xte.iloc[:20]))
sample=Xte.iloc[:5].copy(); sample.to_csv(ART/'sample_input.csv',index=False)
pd.DataFrame({'churn_probability':restored.predict_proba(sample)[:,1]}).to_csv(ART/'sample_output.csv',index=False)
unseen=sample.copy(); unseen.loc[unseen.index[0],'Contract']='Previously unseen plan'
assert np.isfinite(restored.predict_proba(unseen)).all()
missing=sample.copy(); missing.loc[missing.index[0],'TotalCharges']=np.nan
assert np.isfinite(restored.predict_proba(missing)).all()
save_json('policy.json',{'type':'batch_top_fraction','fraction':.2,'tie_break':'stable_input_order','classification_diagnostic_threshold':.5})
save_json('verification.json',{'disjoint_splits':True,'pipeline_roundtrip':True,'unseen_category':True,'missing_charge':True,'finite_probabilities':bool(np.isfinite(pt).all()),'human_review_completed':False})
print('Saved deployable pipeline and batch example. Proxy gate:',metrics['proxy_gate_passed'])
