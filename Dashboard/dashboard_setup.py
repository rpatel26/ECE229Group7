'''
This file intend to build a dashboard using streamlit to
provide end user visualization and analysis.
'''
import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import plotly.express as px
from sidebar import * 

def load_data():
    train = pd.read_csv('../data/train.csv')
    #remove missing values form last three coloms
    train = train.dropna(subset=['Resource Allocation','Mental Fatigue Score',
                             'Burn Rate']).reset_index(drop=True)
    return train 


def main():
    st.title("Understanding Employee's Stress Level")
    st.write("""
    ## Welcome to the Dashboad :) 
    """)
    train = load_data()

    st.write("Here's the data used to train prediction model")

    st.write(train)

    df = pd.DataFrame(train, columns = ['Mental Fatigue Score','Burn Rate'])
    df = df.rename(columns = {'Mental Fatigue Score': 'fatigue'}, inplace = False)

    fatigue_score, gender_options, designation, company_options = setup_sidebar()


    average_male = train.query('Gender == \'Male\'',engine='python').mean()
    average_female = train.query('Gender == \'Female\'',engine='python').mean()

    fig = px.bar([0,1], [average_male[2], average_female[2]])
    fig.update_xaxes(title='Average Mental Fatigue Score')
    fig.update_yaxes(title='Gender')
    st.plotly_chart(fig)

    setup_distribution_plot(train, fatigue_score, gender_options, designation, company_options)

def setup_distribution_plot(train, fatigue_score, gender_options, designation, company_options):
    '''sets up a plot that is controlled with the sidepanels to control the distribution of the data in a histogram'''
    train_new = train
    train_new['fatigue'] = train_new["Mental Fatigue Score"]
    train_new['company'] = train_new["Company Type"]

    plot_query = f'fatigue.between{fatigue_score} and Designation.between{designation}'
    if gender_options != "Both":
        plot_query = plot_query + f' and Gender == \'{gender_options}\''
    if company_options != "Both":
        plot_query = plot_query + f' and company == \'{company_options}\''

    f = px.histogram(train_new.query(plot_query,engine='python'), x='Mental Fatigue Score', nbins=15, title='Fatigue Score Distribution')
    f.update_xaxes(title='Mental Fatigue Score')
    f.update_yaxes(title='Gender')
    st.plotly_chart(f)

if __name__ == "__main__":
    main()