import streamlit as st
import pandas as pd
import pickle
@st.cache(allow_output_mutation=True)

def get_data():
    '''
    used for store multiple user input
    '''
    return []

def get_user_input():
    '''
    setup the user inputs section and store inputs as dataframe
    then use model to predict burnout rate
    '''
    st.write('1. Do you have work from home setup available:')
    wfh_yes = st.radio('WFH setup available',['Yes','No'])
    if wfh_yes == 'Yes':
        wfh = 1
    else:
        wfh = 0

    #user_id = st.text_input("User ID")
    st.write('2. Designation of the employee of work in the organization (bigger is higher designation)')
    designation = st.slider(" Designation", 0, 5)
    st.write('3. Amount of resource allocated to the employee to work, ie. number of working hours. (higher means more resource)')
    resource = st.slider("Resource Allocation", 0, 10)
    st.write('4. The level of fatigue mentally the employee is facing. 0.0 means no fatigue and 10.0 means completely fatigue.')
    fatigue = st.slider("Fatigue Score", 0, 10)
    inputs = []
    if st.button("Submit"):
        inputs.append({'WFH Setup Available':wfh,"Designation": designation,
                            "Resource Allocation": resource,'Mental Fatigue Score':fatigue})


        xtest = pd.DataFrame(inputs)
        #load trained tree model 
        res = pd.DataFrame()
        loaded_model1 = pickle.load(open('../Model/tree_model.sav', 'rb'))
        res['point estimate'] = loaded_model1.predict(xtest)
        loaded_model3 = pickle.load(open('../Model/tree_model_lower.sav', 'rb'))
        res['interval lower bound'] = loaded_model3.predict(xtest)
        loaded_model2 = pickle.load(open('../Model/tree_model_upper.sav', 'rb'))
        res['interval upper bound'] = loaded_model2.predict(xtest)

        res.reset_index(drop=True, inplace=True)
        return res

        #st.write(pd.DataFrame(get_data()))
        #return pd.DataFrame(get_data())
