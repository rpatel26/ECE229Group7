import streamlit as st 

def setup_instruction_section_exploration():
    '''This function sets up visual explanations on how to use our provided dashboards in the exploration section.'''
    st.write("""
    # 1. Data Explorations
    We provide a gamut of data exploration plots, which you can adapt to your desire.""")


def setup_instruction_section_feature_analysis():
    '''This function sets up visual explanations on how to use our provided dashboard in the prediction section.'''
    st.write("""
    # 2. Feature Analysis""")
    #We provide an interactive section for you to compare the importance of different different features.
    #We use a correlation coefficient for continuous variables and a one-way ANOVA for categorical variables.


def setup_instruction_section_prediction():
    '''This function sets up visual explanations on how to use our provided dashboard in the prediction section.'''
    st.write("""
    # 3. Predict your Potential Employee Burnout
    We provide an interactive section for you to fill out. This section parses information
     from your company to predict a the potential for burnout in your company. This can help
      you figure out which steps are necessary to modify to reduce the mental fatigue of your 
      employees and potentially make them more happy, healthy and productive.
    """)