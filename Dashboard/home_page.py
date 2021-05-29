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
from utils import * 
from instructions import * 
from multiapp import MultiApp


def load_data():
    '''loads the data from the data subdirectory'''
    train = pd.read_csv('../data/train.csv')
    #remove missing values form last three coloms
    train = train.dropna(subset=['Resource Allocation','Mental Fatigue Score',
                             'Burn Rate']).reset_index(drop=True)
    return train 

def make_header():
    '''setup header section and allow user to select/input data file for analysis'''
    st.title("Understanding Your Employee's Stress Level")
    st.write('')
    st.subheader('A Web App by [Winter 2021 ECE 229 Group 7](https://github.com/rpatel26/ECE229Group7)')
    st.markdown("Our sample data is based on a 2019 [study](https://www.kaggle.com/blurredmachine/are-your-employees-burning-out) of employee burnout rates. The goal of the study is to understand dependencies of burnout rates and external contributing factors." )

    
   

def app():
    '''main function to set up the streamlit application visuals'''
    
    train = make_header()
    
    