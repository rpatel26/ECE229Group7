import warnings
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from scipy.sparse import hstack
from scipy.optimize import minimize
from matplotlib import pyplot as plt
from tqdm import tqdm_notebook, tqdm
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.metrics import roc_auc_score, accuracy_score, log_loss, r2_score
from sklearn.metrics import mean_squared_error, mean_squared_log_error
from sklearn.feature_selection import RFE
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_validate
from sklearn.linear_model import LinearRegression
from sklearn import model_selection
from sklearn import metrics
from sklearn.preprocessing import LabelEncoder
import pickle
from sklearn.ensemble import GradientBoostingRegressor


#from catboost import CatBoostRegressor
#import category_encoders as ce
#import xgboost as xgb
#import lightgbm as lgb
#from lightgbm import LGBMRegressor
warnings.filterwarnings('ignore')


def get_data():
    '''
    Download dataset and saved under folder "data" in working directory
    '''
    train = pd.read_csv('../data/train.csv')
    test = pd.read_csv('../data/test.csv')
    sample = pd.read_csv('../data/sample_submission.csv')
    #remove missing values form last three coloms
    train = train.dropna(subset=['Resource Allocation','Mental Fatigue Score','Burn Rate']).reset_index(drop=True)

    train_encoded = data_encoder(train)
    test_encoded = data_encoder(test)
    train_encoded = train_encoded.drop_duplicates(keep='first')  # dropping duplicates
    df_train=train_encoded.copy()
    df_test=test_encoded.copy()
    df_train=df_train[df_train['Burn Rate'].isnull()==False]  # removing null values
    df_train=df_train[df_train['Mental Fatigue Score'].isnull()==False]
    df_train=df_train[df_train['Resource Allocation'].isnull()==False]
    cols = ['WFH Setup Available','Designation','Resource Allocation',
        'Mental Fatigue Score','Burn Rate']
    df =df_train[cols]
    return df,train_encoded


def wfh_encoder(data):
    '''
    Function to encode variable "WFH Setup Available" as binary variable
    '''
    if data["WFH Setup Available"] == "Yes":
        return 1
    return 0
def data_encoder(df):
    '''
    Funtion to transform all categorical features into dummy variables
    '''
    df["WFH Setup Available"] = df.apply(wfh_encoder, axis=1)
    df = pd.get_dummies(data=df,columns=['Gender', 'Company Type'], drop_first=True)
    return df

def evalu_model(model, xtrain, xtest, ytrain, ytest):
    '''
    Function to evaluate model performance through cross validation.
    Metrics to evaluate performance: R-sqaured and mean squared error
    '''
    r2_train = cross_val_score(model,xtrain,ytrain,cv=5,scoring="r2").mean()
    r2_test = cross_val_score(model,xtest,ytest,cv=5,scoring="r2").mean()
    mse_train = abs(cross_val_score(model,xtrain,ytrain,cv=5,scoring = "neg_mean_squared_error").mean())
    mse_test = abs(cross_val_score(model,xtest,ytest,cv=5,scoring = "neg_mean_squared_error").mean())
    print("r2 score for train: "+str(round(100*r2_train,2))+"%")
    print("r2 score for test: "+str(round(100*r2_test,2))+"%")
    print("MSE score for train: "+str(round(100*mse_train,2))+"%")
    print("MSE score for test: "+str(round(100*mse_test,2))+"%")
    return r2_train,r2_test,mse_train,mse_test

def linear_regression(xtrain, xtest, ytrain, ytest):
    '''
    Predict burn rate using linear regression model
    '''
    lr = LinearRegression().fit(xtrain, ytrain)
    print('====================================')
    print('linear regression model performance:')
    print('====================================')
    evalu_model(lr, xtrain, xtest, ytrain, ytest)

    fi = [*zip(xtrain.columns, lr.coef_[0])]
    print('====================================')
    print('linear regression model coefficient:')
    print('====================================')
    for i in fi:
        print(i)
    # #save model
    # filename = 'linear_model.sav'
    # pickle.dump(lr, open(filename, 'wb'))
    # loaded_model = pickle.load(open(filename, 'rb'))
    # result = loaded_model.predict(xtest)
    return lr

def tree_model(xtrain, xtest, ytrain, ytest):
    '''
    Predict burout rate using gradient boosting model output both point estimation and predict interval
    '''
    alpha = 0.95

    clf = GradientBoostingRegressor(loss='quantile', alpha=alpha,
                                    n_estimators=250, max_depth=3,
                                    learning_rate=.1, min_samples_leaf=9,
                                    min_samples_split=9)

    clf.fit(xtrain, ytrain)
    predictions = pd.DataFrame(ytest.copy())

    # Make the prediction on the meshed x-axis
    predictions['upper'] = clf.predict(xtest)
    #save model
    filename = 'tree_model_upper.sav'
    pickle.dump(clf, open(filename, 'wb'))
    #eval_model(clf, xtrain, xtest, ytrain, ytest)
    clf.set_params(alpha=1.0 - alpha)
    clf.fit(xtrain, ytrain)
    # Make the prediction on the meshed x-axis
    predictions['lower'] = clf.predict(xtest)
    filename = 'tree_model_lower.sav'
    pickle.dump(clf, open(filename, 'wb'))
    #eval_model(clf, xtrain, xtest, ytrain, ytest)
    clf.set_params(loss='ls')
    clf.fit(xtrain, ytrain)

    # Make the prediction on the meshed x-axis
    predictions['mid']  = clf.predict(xtest)
    print('====================================')
    print('tree model performance:')
    print('====================================')
    evalu_model(clf, xtrain, xtest, ytrain, ytest)
    filename = 'tree_model.sav'
    pickle.dump(clf, open(filename, 'wb'))
    return clf

if __name__=='__main__':
    df,_ = get_data()
    xtrain, xtest, ytrain, ytest = train_test_split(df.loc[:, df.columns != "Burn Rate"],
                                                df.loc[:, df.columns == "Burn Rate"],
                                                test_size=0.3, random_state=88)
    linear_regression(xtrain, xtest, ytrain, ytest)
    tree_model(xtrain, xtest, ytrain, ytest)
    res = pd.DataFrame()
    loaded_model1 = pickle.load(open('tree_model.sav', 'rb'))
    res['prediction'] = loaded_model1.predict(xtest)

    loaded_model2 = pickle.load(open('tree_model_upper.sav', 'rb'))
    res['upper'] = loaded_model2.predict(xtest)
    loaded_model3 = pickle.load(open('tree_model_lower.sav', 'rb'))
    res['lower'] = loaded_model3.predict(xtest)
    print(res.iloc[0])

    #feature importance
    print('====================================')
    print('tree model feature importances:')
    print('====================================')
    fi = pd.DataFrame({"feature":list(xtrain.columns),"score":loaded_model1.feature_importances_}).sort_values(by='score',ascending=False)
    print(fi)