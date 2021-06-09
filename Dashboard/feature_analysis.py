import streamlit as st
import scipy.stats as stats
import pandas as pd 
import plotly.express as px
import numpy as np
import seaborn as sn
from instructions import setup_instruction_section_feature_analysis
from utils import load_data
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

def get_corr(data):
    '''sets up the correlation matrix
    param: pd.DataFrame
    returns: pd.DataFrame'''
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
    return corrMatrix

def setup_correlation_plots(data):
    '''sets up bar plots for feature analysis with interactive widgets
    param: data pandas dataframe
    '''
    assert isinstance(data, pd.DataFrame)

    st.write('## Confusion Matrix')
    st.write('We provide a correlation confusion matrix for you to get insights into the importance of '
             'different features for your employee\'s burnout rate.')
    st.write("To observe Pearson correlations between categorical variables **Gender**, **Company Type**, and **WFH Setup Available**, we change its data type to a binary encoding "
             "to fit the correlation analysis. Here is the default setting:")
    st.write("**Gender**: Male = 0, Female = 1")
    st.write("**Company Type**: Service = 0, Product = 1")
    st.write("**WFH Setup Available**: No = 0, Yes = 1")
    st.write("In the confusion matrix, each feature is listed in the x and y axis. The value of the point "
             "where each pair of features intersects represents the correlation of the pair of features. "
             "The value is between -1 to 1 and can be seen when hovered over the respective cell. A positive number means features are positively correlated."
             "A negative number indicates that features are negatively correlated. The larger the absolute "
             "value, the higher their correlation. This is also indicated by the respective color.")
    
    corrMatrix = get_corr(data)

    hovertext = list()
    for yi, yy in enumerate(corrMatrix.columns):
        hovertext.append(list())
        for xi, xx in enumerate(corrMatrix.columns):
            hovertext[-1].append('x: {}<br />y: {}<br />Correlation Coefficient: {}'.format(xx, yy, np.array(corrMatrix)[yi][xi]))


    fig = make_subplots(rows=1, cols=1, subplot_titles=("Feature importance", "Statistical Significance"))
    f = go.Heatmap(
        z=corrMatrix,
        x=corrMatrix.columns,
        y=corrMatrix.columns,
        colorscale=px.colors.diverging.RdBu,
        hoverinfo='text',
        text=hovertext,
        zmin=-1,
        zmax=1
    )
    fig.add_trace(f, row=1, col=1)
    st.plotly_chart(fig)


def app():
    '''Build function for multi page streamlit aaplication - feature analysis section
    loads the data, sets up the instruction section and correlation plots'''
    train = load_data()
    setup_instruction_section_feature_analysis()
    setup_correlation_plots(train)
