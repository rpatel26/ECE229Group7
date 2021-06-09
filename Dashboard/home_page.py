import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
from utils import load_data

def make_header():
    '''setup header section and allow user to select/input data file for analysis'''

    st.title("Understanding Your Employee's Stress Level")
    st.write('')
    st.subheader('A Web App by [Winter 2021 ECE 229 Group 7](https://github.com/rpatel26/ECE229Group7)')
    st.markdown("Our sample and training data is based on a 2019 [study](https://www.kaggle.com/blurredmachine/are-your-employees-burning-out) of employee burnout rates. The goal of the study is to understand dependencies of burnout rates and external contributing factors. Please use our subpages to get more information." )
    st.image("./Burnout.png", width=None)
    
def app():
    '''main function to set up the streamlit application visuals on the home page'''
    
    train = make_header()
    
    