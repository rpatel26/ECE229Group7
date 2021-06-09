import plotly.express as px
import streamlit as st
import seaborn as sns
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import RendererAgg
from instructions import * 
from sliders import * 
import pandas as pd
from utils import * 


def data_summary(df):
    '''set up the data summary section
    param: df pandas DataFrame'''

    assert isinstance(df, pd.DataFrame)

    st.write('')
    row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.beta_columns(
    (.1, 2, .2, 1, .1))
    with row0_1:
        st.markdown(f"**Total Records:** {df.shape[0]}")
        st.markdown(f"**Average Burn Rate:** " +\
                    f"{df['Burn Rate'].mean()}")
    
    with row0_2:
        st.markdown(f"**Highest Burn Rate:** {df['Burn Rate'].max()}")
        st.markdown(f"**Lowest Burn Rate :** {df['Burn Rate'].min()}")

    st.text("")

def setup_male_female_avg_plot(train):
    '''sets up the plot for average gender fatigue score -- static for now, can be adapted for dymanic change
    param: train input training dataframe'''

    assert isinstance(train, pd.DataFrame)

    average_male = train.query('Gender == \'Male\'',engine='python').mean()
    average_female = train.query('Gender == \'Female\'',engine='python').mean()
    fig = px.bar([0,1], [average_male[2], average_female[2]], color_discrete_sequence=px.colors.diverging.RdBu)
    fig.update_xaxes(title='Average Mental Fatigue Score')
    fig.update_yaxes(title='Gender')
    fig.update_layout(
    yaxis = dict(
        tickmode = 'array',
        tickvals = [0,1],
        ticktext = ['Male', 'Female'])) 
    st.plotly_chart(fig)


def setup_distribution_plot(train, fatigue_score, gender_options, designation, company_options, wfh_options):
    '''sets up a plot that is controlled with the sidepanels to control the distribution of the data in a histogram
    param: train training data dataframe
    param: fatigue_score slider value of fatigue score 
    param:  gender_options selected gender options from sidebar 
    param:  designation delected designation range from sidebar
    param:  company_options selected company options from sidebar 
    param:  wfh_options selected wfh options from sidebar '''


    assert isinstance(train, pd.DataFrame)
    assert isinstance(gender_options, str)
    assert isinstance(company_options, str)
    assert isinstance(wfh_options, str)
    assert isinstance(fatigue_score, tuple)
    assert isinstance(designation, tuple)

    assert len(fatigue_score) == 2
    assert len(designation) == 2

    train_new = train
    train_new['fatigue'] = train_new["Mental Fatigue Score"]
    train_new['company'] = train_new["Company Type"]
    train_new['wfh'] = train_new["WFH Setup Available"]

    plot_query = f'fatigue.between{fatigue_score} and Designation.between{designation}'
    if gender_options != "Both":
        plot_query = plot_query + f' and Gender == \'{gender_options}\''
    if company_options != "Both":
        plot_query = plot_query + f' and company == \'{company_options}\''
    if wfh_options != "Both":
        options = "Yes" if wfh_options == 'Work from Home' else "No"
        plot_query = plot_query + f' and wfh == \'{options}\''

    st.write("## Fatigue Score Distribution")
    f = px.histogram(train_new.query(plot_query,engine='python'), x='Mental Fatigue Score', nbins=15, color_discrete_sequence=px.colors.diverging.RdBu)
    f.update_xaxes(title='Mental Fatigue Score')
    f.update_yaxes(title='Number of Instances')
    st.write("Please use the sliders in the sidebar to adapt the following plot.")
    st.plotly_chart(f)

def app():
    '''Build function for multi page streamlit aaplication - exploration section
    loads the data, sets up UI explanations and deals with file uploads'''
    train = load_data()
    setup_instruction_section_exploration()

    uploaded_file = st.file_uploader("Choose a file to upload or explore our training data (default). Fallback to sample data.")
    if uploaded_file is not None:
        train = pd.read_csv(uploaded_file)
        if not check_data_format(train):
            wrong_data_format_message()
            train = load_data()
        else:
            train = train.dropna(subset=['Resource Allocation','Mental Fatigue Score']).reset_index(drop=True)
            st.markdown("Input Survery Data")
    
    need_help = st.beta_expander('Need help? 👉')
    with need_help:
        st.markdown("Having trouble uploading your data file? Refresh the page to restart uploading a file according to the fields template here https://github.com/rpatel26/ECE229Group7/blob/main/data_template.csv.")
    
    df = pd.DataFrame(train, columns = ['Mental Fatigue Score','Burn Rate'])
    df = df.rename(columns = {'Mental Fatigue Score': 'fatigue'}, inplace = False)


    fatigue_score, gender_options, designation, company_options, wfh_options = setup_interaction_items()
    setup_distribution_plot(train, fatigue_score, gender_options, designation, company_options, wfh_options)
