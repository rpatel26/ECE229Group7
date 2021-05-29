from pandas.core.frame import DataFrame
import streamlit as st
import pandas as pd
import pickle
from instructions import * 
import base64

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
    res['Point Estimate'] = loaded_model1.predict(xtest)
    loaded_model3 = pickle.load(open('../Model/tree_model_lower.sav', 'rb'))
    res['Interval Lower Bound'] = loaded_model3.predict(xtest)
    loaded_model2 = pickle.load(open('../Model/tree_model_upper.sav', 'rb'))
    res['Interval Upper Bound'] = loaded_model2.predict(xtest)

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
        st.markdown("Predicted Burnout Rate per Employee:")
        st.write(res[["Employee ID", "Point Estimate", 'Interval Lower Bound', 'Interval Upper Bound']])
        tmp_download_link = download_link(res, 'Employee_Burnout_Predictions.csv', 'Download Burnout Predictions as CSV')
        st.markdown(tmp_download_link, unsafe_allow_html=True)
    need_help = st.beta_expander('Need help? 👉')
    with need_help:
        st.markdown("Having trouble uploading your data file? Read the data fields template here https://github.com/rpatel26/ECE229Group7.")
    st.markdown("**or just use the input section below to predict one record**")

    burnout_score = get_user_input()
    st.write("Your predicted burnout score (scale 0-1) and 95% confidence interval:",burnout_score)


def download_link(object_to_download, download_filename, download_link_text):
    """
    Generates a link to download the given object_to_download.

    object_to_download (str, pd.DataFrame):  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv, some_txt_output.txt
    download_link_text (str): Text to display for download link.

    Examples:
    download_link(YOUR_DF, 'YOUR_DF.csv', 'Click here to download data!')
    download_link(YOUR_STRING, 'YOUR_STRING.txt', 'Click here to download your text!')

    """
    if isinstance(object_to_download,pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode()).decode()

    return f'<a href="data:file/txt;base64,{b64}" style="border-radius: 0.25rem;text-decoration:none; padding: 0.25rem 0.75rem;color:#1b4174; border: 1px solid #1b4174; border-radius: 5px;" download="{download_filename}">{download_link_text}</a>'