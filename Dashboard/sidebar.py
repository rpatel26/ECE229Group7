import streamlit as st

def setup_sidebar():
    '''sets up the sidebar elements for streamlit
    returns: selected fatigue score and designation range, 
    if males or females were selected, selected industry type and selected work setup'''

    st.write("Please select applicable settings to see the data distribution for different data subsets.")
    st.write('1. Select Fatigue Score range to be displayed')
    fatigue_score = st.slider('The level of fatigue mentally the employee is facing. 0.0 means no fatigue and 10.0 means completely fatigue.', 0., 10., (0., 10.))
    st.write('2. Select Gender to be displayed')
    gender_options = st.selectbox('',
        ('Male', 'Female', 'Both'))
    st.write('3. Select Designation range to be displayed')
    designation = st.slider('Seniority level of the employee in the organization. Larger value means higher seniority level.', 0., 5., (0., 5.))
    st.write('4. Select industry to be displayed')
    company_options = st.selectbox('',
        ('Service', 'Product', 'Both'))
    st.write('5. Select the work setup to be displayed')
    wfh_options = st.selectbox('',
        ('Work from Home', 'Work from Office', 'Both'))

    return fatigue_score, gender_options, designation, company_options, wfh_options