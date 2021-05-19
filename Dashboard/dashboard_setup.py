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
from sidebar import * 
from plots import * 
from user_input import *
from utils import * 
from instructions import * 
from variable_correlations import *

def load_data():
    '''loads the data from the data subdirectory'''
    train = pd.read_csv('../data/train.csv')
    #remove missing values form last three coloms
    train = train.dropna(subset=['Resource Allocation','Mental Fatigue Score',
                             'Burn Rate']).reset_index(drop=True)
    return train 

def make_header():
    '''setup header section and allow user to select/input data file for analysis'''
    row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.beta_columns(
    (.1, 2, .2, 1, .1))

    row0_1.title("Understanding Your Employee's Stress Level")

    with row0_2:
        st.write('')

    row0_2.subheader('A Web App by [Winter 2021 ECE 229 Group 7](https://github.com/rpatel26/ECE229Group7)')
    
    row1_spacer1, row1_1, row1_spacer2 = st.beta_columns((.1, 3.2, .1))

    with row1_1:
        st.markdown("Welcome to Employee Stress Analysis App. Our project team aims to predict, analyze and visualize how stressed employees in a company are, by looking at various metrics such as how long employees have been in the company, their work type, working hours, setups, benefits, etc. Give it a go!")
        st.markdown("**To begin, please upload your company's survey data (or just use our sample data!).** 👇")
        st.markdown("Our sample data is based on a 2019 [study](https://www.kaggle.com/blurredmachine/are-your-employees-burning-out) of employee burnout rates. The goal of the study is to understand dependencies of burnout rates and external contributing factors." )

    row2_spacer1, row2_1, row2_spacer2 = st.beta_columns((.1, 3.2, .1))
    with row2_1:
        default_username = st.selectbox("Select one of our sample data", ("Employee-Data-Sample-1","Employee-Data-Sample-2"))
        st.markdown("**or**")
        user_input = st.text_input(
            "Input your own employee data file(csv) path here (e.g. https://github.com/rpatel26/ECE229Group7)")
        need_help = st.beta_expander('Need help? 👉')
        with need_help:
            st.markdown("Having trouble loading your data file? Read the data fields template here https://github.com/rpatel26/ECE229Group7.")

        if not user_input:
            df = load_data()
        else:
            try:
                with open(user_input) as input:
                    st.text(input.read())
            except FileNotFoundError:
                st.error('File not found.')
        
        st.write(df)
        return df

def main():
    '''main function to set up the streamlit application visuals'''
    st.set_page_config(layout="wide")
    train = make_header()

    data_summary(train)  
    
    setup_instruction_section_exploration()

    df = pd.DataFrame(train, columns = ['Mental Fatigue Score','Burn Rate'])
    df = df.rename(columns = {'Mental Fatigue Score': 'fatigue'}, inplace = False)


    fatigue_score, gender_options, designation, company_options, wfh_options = setup_sidebar()
    setup_distribution_plot(train, fatigue_score, gender_options, designation, company_options, wfh_options)

    st.write("## Average Mental Fatigue Score by Gender")
    setup_male_female_avg_plot(train)

    setup_instruction_section_feature_analysis()
    setup_correlation_plots(train)
    features_plot(train)


    setup_instruction_section_prediction()
    burnout_score = get_user_input()
    st.write("Your predicted burnout score is (scale 0-1):",burnout_score)


    


if __name__ == "__main__":
    main()