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
    then use model to predict score
    '''
    st.write('1. Do you have work from home setup available:')
    whf_yes = st.checkbox('Yes')
    whf_no = st.checkbox('No')
    wfh = whf_yes + whf_no 

    if wfh >1 or wfh <0 :
        st.write('Wrong input: Select exactly one choice.')
    
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

        filename = '../Model/linear_model.sav'
        loaded_model = pickle.load(open(filename, 'rb'))
        xtest = pd.DataFrame(inputs)
        result = float(loaded_model.predict(xtest)[0])
        return result

        #st.write(pd.DataFrame(get_data()))
        #return pd.DataFrame(get_data())
