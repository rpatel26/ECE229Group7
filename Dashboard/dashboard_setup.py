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
<<<<<<< HEAD
from user_input import *
=======
>>>>>>> main

def load_data():
    '''loads the data from the data subdirectory'''
    train = pd.read_csv('../data/train.csv')
    #remove missing values form last three coloms
    train = train.dropna(subset=['Resource Allocation','Mental Fatigue Score',
                             'Burn Rate']).reset_index(drop=True)
    return train 
<<<<<<< HEAD

=======
>>>>>>> main

def main():
    '''main function to set up the streamlit application visuals'''
    st.title("Understanding Employee's Stress Level")
    st.write("""
    ## Welcome to the Dashboad :) 
    """)
    train = load_data()

<<<<<<< HEAD
    st.write("Here's the data used to train prediction model")

    st.write(train)

    df = pd.DataFrame(train, columns = ['Mental Fatigue Score','Burn Rate'])
    df = df.rename(columns = {'Mental Fatigue Score': 'fatigue'}, inplace = False)

    fatigue_score, gender_options, designation, company_options, wfh_options = setup_sidebar()

    setup_male_female_avg_plot(train)
    setup_distribution_plot(train, fatigue_score, gender_options, designation, company_options, wfh_options)
    
    st.write("## Using model to predict your burnout score")
    burnout_score = get_user_input()
    st.write("Your predicted burnout score is (scale 0-1):",burnout_score)

=======
def main():
    '''main function to set up the streamlit application visuals'''
    st.title("Understanding Employee's Stress Level")
    st.write("""
    ## Welcome to the Dashboad :) 
    """)
    train = load_data()

    st.write("Here's the data used to train prediction model")

    st.write(train)

    df = pd.DataFrame(train, columns = ['Mental Fatigue Score','Burn Rate'])
    df = df.rename(columns = {'Mental Fatigue Score': 'fatigue'}, inplace = False)

    fatigue_score, gender_options, designation, company_options, wfh_options = setup_sidebar()

    setup_male_female_avg_plot(train)
    setup_distribution_plot(train, fatigue_score, gender_options, designation, company_options, wfh_options)
>>>>>>> main

if __name__ == "__main__":
    main()