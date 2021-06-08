import pandas as pd
import streamlit as st
def load_data():
    '''loads the data from the data subdirectory'''
    train = pd.read_csv('../data/train.csv')
    #remove missing values form last three coloms
    train = train.dropna(subset=['Resource Allocation','Mental Fatigue Score',
                             'Burn Rate']).reset_index(drop=True)
    return train 

def check_data_format(train):
    assert isinstance(train, pd.DataFrame)
    required_cols = ['Employee ID',	'Date of Joining','Gender','Company Type','WFH Setup Available',
    'Designation','Resource Allocation','Mental Fatigue Score']
    for col in required_cols:
        if col in list(train.columns):
            continue
        else:
            return False
    return True

def wrong_data_format_message():
    st.error("Wrong data format. Please make sure your data contains columns Employee ID, Date of Joining, Gender, Company Type, WFH Setup Available, Designation, Resource Allocation and Mental Fatigue Score. Fall back to sample data.")
