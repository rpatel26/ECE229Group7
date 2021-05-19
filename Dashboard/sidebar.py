import streamlit as st

def setup_sidebar():
    '''sets up the sidebar elements for streamlit
    returns: selected fatigue score and designation range, 
    if males or females were selected, selected industry type and selected work setup'''

    st.sidebar.write("Please select applicable settings.")
    fatigue_score = st.sidebar.slider('Fatigure Score', 0., 10., (0., 10.))
    gender_options = st.sidebar.selectbox(
        'Select Gender to be displayed',
        ('Male', 'Female', 'Both'))

    designation = st.sidebar.slider('Designation', 0., 5., (0., 5.))

    company_options = st.sidebar.selectbox(
        'Select Industry to be displayed',
        ('Service', 'Product', 'Both'))
    wfh_options = st.sidebar.selectbox(
        'Select the work setup to be displayed',
        ('Work from Home', 'Work from Office', 'Both'))

    return fatigue_score, gender_options, designation, company_options, wfh_options