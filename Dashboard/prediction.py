from pandas.core.frame import DataFrame
import streamlit as st
import pandas as pd
import pickle
from instructions import * 

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
        res_init = pd.DataFrame()
        res = predict(xtest,res_init)

        return res

def wfh_encoder(data):
    if data["WFH Setup Available"] == "Yes":
        return 1
    return 0

def data_encoder(df):
    df["WFH Setup Available"] = df.apply(wfh_encoder, axis=1)
    df = pd.get_dummies(data=df,columns=['Gender', 'Company Type'], drop_first=True)
    return df
    
def predict(xtest,res):
    '''
    predict burnout rate using user input data
    '''
    #load trained tree model 
    
    loaded_model1 = pickle.load(open('../Model/tree_model.sav', 'rb'))
    res['point estimate'] = loaded_model1.predict(xtest)
    loaded_model3 = pickle.load(open('../Model/tree_model_lower.sav', 'rb'))
    res['interval lower bound'] = loaded_model3.predict(xtest)
    loaded_model2 = pickle.load(open('../Model/tree_model_upper.sav', 'rb'))
    res['interval upper bound'] = loaded_model2.predict(xtest)

    res.reset_index(drop=True, inplace=True)
    return res

def app():

    setup_instruction_section_prediction()

    st.markdown("In this page you can predict your employees' burnout rate using variables like Designation, WFH Setup Available etc. Give it a go!")
    st.markdown("**To begin, please upload your company's survey data .** 👇")

    uploaded_file = st.file_uploader("Choose a file to upload")
    if uploaded_file is not None:
        dataframe = pd.read_csv(uploaded_file)
        st.markdown("Input Survery Data")
        st.write(dataframe)

        cols = ['WFH Setup Available','Designation','Resource Allocation',
        'Mental Fatigue Score']
        xtest = data_encoder(dataframe)
        xtest = xtest[cols]
        res = predict(xtest,dataframe)
        st.markdown("With Predicted Burnout Rate")
        st.write(res)
    # user_input = st.text_input(
    #     "Input your own employee data file(csv) path here (e.g. https://github.com/rpatel26/ECE229Group7)")
    need_help = st.beta_expander('Need help? 👉')
    with need_help:
        st.markdown("Having trouble uploading your data file? Read the data fields template here https://github.com/rpatel26/ECE229Group7.")
    st.markdown("**or just use the input section below to predict one record**")

    burnout_score = get_user_input()
    st.write("Your predicted burnout score (scale 0-1) and 95% confidence interval:",burnout_score)
