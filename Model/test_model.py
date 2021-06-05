from burnout_prediction import * 
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import GradientBoostingRegressor

df,df_encoded = get_data()
xtrain, xtest, ytrain, ytest = train_test_split(df.loc[:, df.columns != "Burn Rate"],
                                                df.loc[:, df.columns == "Burn Rate"],
                                                test_size=0.3, random_state=88)

def test_get_data():
    '''
    pytest for testing get_data function and data_encoder function:
    test get_data() load a pandas dataframe object
    '''
    assert isinstance(df,pd.DataFrame)

def test_wfh_encoder():
    '''
    pytest for testing wfh_encoder function:
    test wfh_encoder return value in (0,1)
    '''
    x = wfh_encoder(df.iloc[0])
    assert x in (0,1)

def test_data_encoder():
    '''
    pytest for testing data_encoder function:
    test data_encoder return dataframe object
    '''
    assert isinstance(df_encoded,pd.DataFrame)

def test_lr_model():
    '''
    pytest for testing linear_regression model and evalu_model function:
    test performance metrics are float objects and within resonable numeric range
    '''
    lr = linear_regression(xtrain, xtest, ytrain, ytest)
    r2_train,r2_test,mse_train,mse_test = evalu_model(lr,xtrain, xtest, ytrain, ytest)
    
    assert isinstance(lr,LinearRegression)
    assert isinstance(r2_train,float)
    assert isinstance(r2_test,float)
    assert isinstance(mse_train,float)
    assert isinstance(mse_test,float)
    assert r2_train > 0.9
    assert mse_train > 0.001
    assert r2_test > 0.9
    assert mse_test > 0.001

def test_tree_model():
    '''
    pytest for testing tree model
    test tree model saved are GradientBoostingRegressor instances
    and precit result are float objects within resonable numeric range
    '''
    res = pd.DataFrame()
    loaded_model1 = pickle.load(open('tree_model.sav', 'rb'))
    res['prediction'] = loaded_model1.predict(xtest)
    loaded_model2 = pickle.load(open('tree_model_upper.sav', 'rb'))
    res['upper'] = loaded_model2.predict(xtest)
    loaded_model3 = pickle.load(open('tree_model_lower.sav', 'rb'))
    res['lower'] = loaded_model3.predict(xtest)
    x = res.iloc[0]
    assert isinstance(loaded_model1,GradientBoostingRegressor)
    assert isinstance(loaded_model2,GradientBoostingRegressor)
    assert isinstance(loaded_model3,GradientBoostingRegressor)
    assert isinstance(x,pd.Series)
    for i in x:
        assert i>=0 and i<=1