import streamlit as st
import scipy.stats as stats
import pandas as pd 
import plotly.express as px
import numpy as np
import seaborn as sn
from instructions import setup_instruction_section_feature_analysis
from home_page import load_data
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

    
def get_correlations(train_data, dependent_variable="Mental Fatigue Score", method='pearson'):
    '''calculates the feature importance for the dependent variables
    param: train_data pandas dataframe
    param: dependent_variable string indicating the column name of the dependent variable
    method: string indicating the correlation calculation method. Needs to be one of {pearson, spearman, kendall}'''

    train_data.drop("Employee ID", inplace=True, axis=1)
    result = dict()
    result['continuous'] = dict()
    result['categorical'] = dict()
    for x in train_data.columns:
        if train_data[x].dtype != str and train_data[x].dtype != object:
            result['continuous'][x] = train_data[x].corr(train_data[dependent_variable], method=method)
        else:
            df_sub = train_data[[x, dependent_variable]].dropna()
            data = [x for _, x in df_sub.groupby(by=x)[dependent_variable]]
            result['categorical'][x] = tuple(stats.f_oneway(*data))

    return result

def setup_correlation_plots(data):
    '''sets up bar plots for feature analysis with interactive widgets
    param: data pandas dataframe'''
    '''
    st.write("## Continuous Features")

    corr_options = st.selectbox(
        'Select Correlation Method',
        ('pearson', 'kendall', 'spearman'))

    dependent_var = st.selectbox(
        'Select Dependent Variable',
        ('Mental Fatigue Score', 'Burn Rate'))
    
    train_data = data
    train_data.drop("fatigue", inplace=True, axis=1)
    train_data.drop("wfh", inplace=True, axis=1)
    train_data.drop("Date of Joining", inplace=True, axis=1)
    train_data.drop("company", inplace=True, axis=1)

    correlation_dict = get_correlations(train_data, dependent_variable=dependent_var, method=corr_options)
    continuous = correlation_dict["continuous"]
    agreed_designation = st.checkbox("Designation", value=True, key=None, help=None)
    agreed_resource = st.checkbox("Resource Allocation", value=True, key=None, help=None)
    agreed_burn = st.checkbox("Burn Rate", value=True if dependent_var != "Mental Fatigue Score" else False, key=None, help=None)
    agreed_fatigue = st.checkbox("Mental Fatigue", value=True if dependent_var == "Mental Fatigue Score" else False, key=None, help=None)

    updates = np.array([agreed_designation, agreed_resource, agreed_burn, agreed_fatigue])
    keys = np.array(list(continuous.keys()))[updates]
    values = np.array(list(continuous.values()))[updates]


    f = px.bar(x=keys, y=values, title='Continuous Feature Importance')
    f.update_yaxes(title=dependent_var)
    f.update_xaxes(title='Features')
    st.plotly_chart(f)


    ####Categorical Setup ###########################

    st.write("## Categorical Features")


    categorical = correlation_dict["categorical"]
    agreed_gender = st.checkbox("Gender", value=True, key=None, help=None)
    agreed_company = st.checkbox("Company Type", value=True, key=None, help=None)
    agreed_wfh = st.checkbox("WHF Setup", value=True, key=None, help=None)

    updates = np.array([agreed_gender, agreed_company, agreed_wfh])

    keys_1 = np.array(list((categorical.keys())))[updates]
    values_f_stat = np.array(list(map(lambda x: x[0], list(categorical.values()))))[updates]
    values_p_value = np.array(list(map(lambda x: x[1], list(categorical.values()))))[updates]

    fig = make_subplots(rows=1, cols=2, subplot_titles=("Feature importance", "Statistical Significance"))

    f_2 = go.Bar(x=keys_1, y=values_f_stat)
    fig.add_trace(f_2, row=1, col=1)

    f_3 = go.Bar(x=keys_1, y=values_p_value)
    fig.add_trace(f_3,row=1, col=2)
    fig.update_layout(height=400, width=1200, title_text="")
    fig.update_yaxes(title_text="Feature Importance", row=1, col=1)
    fig.update_yaxes(title_text="p-value", row=1, col=2)
    st.plotly_chart(fig)

    if st.checkbox('Show Analysis'):
        st.write("")
        for i,key_name in enumerate(keys_1):
            st.write('### %s' % key_name)
            if values_p_value[i] > 0.05:
                st.write("Based on the ANOVA result, there is no significant difference respect to %s" % key_name)
            else:
                feature_dict = data.groupby(key_name).agg('mean')["Mental Fatigue Score"].to_dict()
                higher_v = 0
                higher_k = 0
                for k_dict, v_dict in feature_dict.items():
                    st.write("The mean for %s is %f" % (k_dict,v_dict))
                    if feature_dict[k_dict] > higher_v:
                        higher_k = k_dict
                        higher_v = feature_dict[k_dict]
                st.write("So, based on these samples, we can say that %s == %s may "
                         "lead to higher mental fatigue" % (key_name,higher_k))
            st.write("")
    '''
    st.write('## Confusion Matrix')
    st.write('For feature analysis, we mainly provide confusion matrix for you to realize the correlation'
             'between each of feature.')
    st.write("For **Gender**, **Company Type**, and **WFH Setup Available**, we change its data type to value"
             "which fits correlation analysis. Here is the default setting:")
    st.write("**Gender**: male = 0, female = 1")
    st.write("**Company Type**: Service = 0, Product = 1")
    st.write("**WTF Setup Available**: No = 0, Yest = 1")
    st.write("In the confusion matrix, each feature is listed in x and y axis. The value of the point "
             "where each pair of features intersects represents the correlation of the pair of features"
             "The value is between -1 to 1. Positive number means they are positively correlated."
             "Negative numbers indicate that they are negatively correlated. The larger the absolute "
             "value, the higher their correlation.")
    data_corr = data[['Gender', 'Company Type', 'WFH Setup Available', 'Designation',
                      'Resource Allocation', 'Mental Fatigue Score','Burn Rate']].dropna()
    data_corr.loc[data_corr['Gender'] == 'Male', 'Gender'] = 0
    data_corr.loc[data_corr['Gender'] == 'Female', 'Gender'] = 1
    data_corr.loc[data_corr['Company Type'] == 'Service', 'Company Type'] = 0
    data_corr.loc[data_corr['Company Type'] == 'Product', 'Company Type'] = 1
    data_corr.loc[data_corr['WFH Setup Available'] == 'No', 'WFH Setup Available'] = 0
    data_corr.loc[data_corr['WFH Setup Available'] == 'Yes', 'WFH Setup Available'] = 1

    data_corr[['Gender']] = data_corr[['Gender']].astype(int)
    data_corr[['Company Type']] = data_corr[['Company Type']].astype(int)
    data_corr[['WFH Setup Available']] = data_corr[['WFH Setup Available']].astype(int)
    corrMatrix = data_corr.corr()
    fig, ax = plt.subplots()
    ax = sn.heatmap(corrMatrix, annot=True)
    st.pyplot(fig)





def app():
    train = load_data()
    setup_instruction_section_feature_analysis()
    setup_correlation_plots(train)
    print(get_correlations(train))