import numpy as np
import pandas as pd

from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import NearestCentroid
#from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.metrics import roc_auc_score, roc_curve, precision_score, recall_score, f1_score, accuracy_score
from fastcore.basics import *
from fastcore.parallel import *
from os import cpu_count
from dataBaseConnection import DBConnection
from datetime import datetime
import sys


if len(sys.argv) <= 1:
    exit(0)
else:
    print(f'{sys.argv[1]} {sys.argv[2] } \n{sys.argv[3] } {sys.argv[4] }')
df = pd.read_parquet(sys.argv[2])
df = df.drop(columns='Label')
db = DBConnection()
result = dict({"username":sys.argv[1], "date": datetime.today().strftime('%Y-%m-%d'), "filename": sys.argv[2]})

#df.shape

def binarizer(df):
    df.loc[df['ClassLabel'] != 'Benign', 'ClassLabel'] = 1
    df.loc[df['ClassLabel'] == 'Benign', 'ClassLabel'] = 0
    # print(df['Label'].value_counts())
    df['ClassLabel'] = df['ClassLabel'].astype(dtype=np.int32)
    return df

def xs_y(df_, targ): 
    if not isinstance(targ, list):
        xs = df_[df_.columns.difference([targ])].copy()
    else:
        xs = df_[df_.columns.difference(targ)].copy()
    y = df_[targ].copy()
    return xs, y

def evaluate_one_feature(feature, index='', metric=roc_auc_score):
    
    rootnode = DecisionTreeClassifier(max_depth=1, criterion='gini')
    if(sys.argv[3] == '2'):
        rootnode = NearestCentroid()
#rootnode = svm.LinearSVC()
    #rootnode = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5,2),random_state=1)
    rootnode.fit(X_train[feature].array.reshape(-1,1), y_train)    
    preds = rootnode.predict(X_test[feature].array.reshape(-1,1))
    preds_tr = rootnode.predict(X_train[feature].array.reshape(-1,1))    
    met = round(metric(y_test, preds), 4)
    if met > 0.5:
        return [feature, met, rootnode, preds, preds_tr]
    else:
        return [feature, met, None, [], []]


for chosen_class in ['DoS', 'Bruteforce', 'Portscan', 'Botnet', 'Webattack', 'Infiltration']:
    print("STARTING", chosen_class)
    df_atk = df.loc[df.ClassLabel == chosen_class].copy(deep=True)
    df_ben = df.loc[df.ClassLabel == 'Benign'].sample(n=2*len(df_atk)).copy(deep=True)    
    dfx = pd.concat(objs=[df_atk, df_ben], copy=False, sort=False)
    dfx = binarizer(dfx)
    print(chosen_class, dfx.shape)
    result[chosen_class] = dict({"no_of_samples": dfx.shape[0]})
    target = 'ClassLabel'
    conts = list(df.columns.difference([target]).values)    
    df_train = dfx.sample(frac=0.2, replace=False)
    df_test = dfx.drop(index=df_train.index)
    
    X_train, y_train = xs_y(df_train, targ=target)
    X_test, y_test = xs_y(df_test, targ=target)
    results = parallel(f=evaluate_one_feature, 
                  items=conts, n_workers=cpu_count(), threadpool=False, progress=True)
    result_df = pd.DataFrame(data=results, columns=['feature', 'roc_auc_score', 'fitted_models', 'predictions', 'preds_train']).sort_values(by='roc_auc_score', ascending=False)
    print(result_df[['feature', 'roc_auc_score']].head(5))
    useful_features = result_df.loc[result_df['roc_auc_score'] > 0.5]
    print(f"{len(useful_features)} / {len(conts)} features have direct separating power (linear)")
    ensemble_preds = np.mean(np.vstack(useful_features['predictions'].to_numpy()), axis=0)
    print(ensemble_preds.shape)
    ensemble_preds_train = np.mean(np.vstack(useful_features['preds_train'].to_numpy()), axis=0)
    print(ensemble_preds_train.shape)
    fpr, tpr, thresholds = roc_curve(y_train, ensemble_preds_train)
    # get the best threshold
    J = tpr - fpr
    ix = np.argmax(J)
    best_thresh = thresholds[ix]
    print("Best threshold", best_thresh)
    result[chosen_class]["Best_Threshold"] = best_thresh
    print("The Ensemble OneR model (simple average)")
     
    if sys.argv[4] == '1':
        result["Metric_Chosen"] = "Precision"
        result[chosen_class]["Metric_Value"] = round(precision_score(y_true=y_test, y_pred=np.where(ensemble_preds >= best_thresh, 1, 0)), 4)
    elif sys.argv[4] == '2':
        result["Metric_Chosen"] = "Recall"
        result[chosen_class]["Metric_Value"] = round(recall_score(y_true=y_test, y_pred=np.where(ensemble_preds >= best_thresh, 1, 0)), 4)
    elif sys.argv[4] == '2':
        result["Metric_Chosen"] = "F1-Score"
        result[chosen_class]["Metric_Value"] = round(f1_score(y_true=y_test, y_pred=np.where(ensemble_preds >= best_thresh, 1, 0)), 4)
    else:
        result["Metric_Chosen"] = "Receiver Operating Characteristic AUC"
        result[chosen_class]["Metric_Value"] = round(roc_auc_score(y_true=y_test, y_score=ensemble_preds),4)
    
    print("ROC-AUC", round(roc_auc_score(y_true=y_test, y_score=ensemble_preds),4))
    print("Precision", round(precision_score(y_true=y_test, y_pred=np.where(ensemble_preds >= best_thresh, 1, 0)), 4))
    print("Recall", round(recall_score(y_true=y_test, y_pred=np.where(ensemble_preds >= best_thresh, 1, 0)), 4))
    print("F1", round(f1_score(y_true=y_test, y_pred=np.where(ensemble_preds >= best_thresh, 1, 0)), 4))
    print("DONE", chosen_class)
    print()

db.insertResults(result)