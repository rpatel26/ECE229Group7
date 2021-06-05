from home_page import * 
from dashboard_setup import *
import pandas as pd
from prediction import *
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split

df = load_data()
xtrain, xtest, ytrain, ytest = train_test_split(df.loc[:, df.columns != "Burn Rate"],
                                                df.loc[:, df.columns == "Burn Rate"],
                                                test_size=0.3, random_state=88)
cols = ['WFH Setup Available','Designation','Resource Allocation',
            'Mental Fatigue Score']
xtest = data_encoder(xtest)
xtest = xtest[cols]
def test_load_data():
    '''
    pytest for testing load_data function and data_encoder function:
    test load_data() load a pandas dataframe object
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
    assert isinstance(xtest,pd.DataFrame)

def test_predict():
    '''
    pytest for testing tree model prediction
    test tree model saved are GradientBoostingRegressor instances
    and precit result are float objects within resonable numeric range
    '''
    res = pd.DataFrame()
    loaded_model1 = pickle.load(open('../Model/tree_model.sav', 'rb'))
    res['Point Estimate'] = loaded_model1.predict(xtest)
    loaded_model3 = pickle.load(open('../Model/tree_model_lower.sav', 'rb'))
    res['Interval Lower Bound'] = loaded_model3.predict(xtest)
    loaded_model2 = pickle.load(open('../Model/tree_model_upper.sav', 'rb'))
    res['Interval Upper Bound'] = loaded_model2.predict(xtest)
    x = res.iloc[0]
    assert isinstance(loaded_model1,GradientBoostingRegressor)
    assert isinstance(loaded_model2,GradientBoostingRegressor)
    assert isinstance(loaded_model3,GradientBoostingRegressor)
    assert isinstance(x,pd.Series)
    for i in x:
        assert i>=0 and i<=1

def test_mitigation_strategies():
    '''
    pytest for get_mitigation_strategies
    '''
    x1,m1 = get_mitigation_strategies(0.3)
    x2,m2 = get_mitigation_strategies(0.5)
    x3,m3 = get_mitigation_strategies(0.8)
    strategies_low = "-   There is no immediate action necessary, congratulations."
    strategies_medium = "-   Incorporate balancing mechanisms in the company structure, like sports or meditation.\n  -   Offer time-management workshops to help the employee manage their time better."
    strategies_high = "-   Reduce the workload for the individual employee.\n -   Offer mental health services.\n -   Offer team building workshops to help employees raise their voice before burning out."
    assert x1 =='Low'
    assert x2 == 'Medium'
    assert x3 =='High'
    assert m1 == strategies_low
    assert m2 == strategies_low
    assert m3 == strategies_high