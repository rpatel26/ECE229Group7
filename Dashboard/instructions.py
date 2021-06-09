import streamlit as st 

def setup_instruction_section_exploration():
    '''This function sets up visual explanations on how to use our provided dashboards in the exploration section.'''
    st.write("""
    # 1. Data Explorations
    This page helps you understand the distribution of your study data. If you decide not to upload your own data, you can explore the training data for our evaluation methods.""")


def setup_instruction_section_feature_analysis():
    '''This function sets up visual explanations on how to use our provided dashboard in the prediction section.'''
    st.write("""
    # 2. Feature Analysis""")


def setup_instruction_section_prediction():
    '''This function sets up visual explanations on how to use our provided dashboard in the prediction section.'''
    st.write("""
    # 3. Predict your Potential Employee Burnout
    We provide an interactive section for you to fill out. This section parses information
     from your company to predict the potential for burnout in your company. This can help
      you figure out which steps are necessary to modify to reduce the mental fatigue of your 
      employees and potentially make them more happy, healthy and productive.
    """)