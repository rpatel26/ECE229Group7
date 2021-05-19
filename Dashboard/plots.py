import plotly.express as px
import streamlit as st
import seaborn as sns
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import RendererAgg

def data_summary(df):
    '''set up the data summary section'''
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
    average_male = train.query('Gender == \'Male\'',engine='python').mean()
    average_female = train.query('Gender == \'Female\'',engine='python').mean()
    fig = px.bar([0,1], [average_male[2], average_female[2]])
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
    f = px.histogram(train_new.query(plot_query,engine='python'), x='Mental Fatigue Score', nbins=15)
    f.update_xaxes(title='Mental Fatigue Score')
    f.update_yaxes(title='Gender')
    st.write("Please use the sliders in the sidebar to adapt the following plot.")
    st.plotly_chart(f)
    
def features_plot(df):
    _lock = RendererAgg.lock
    st.write('')
    row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.beta_columns(
    (.1, 2, .2, 1, .1))
    row3_space1, row3_1, row3_space2, row3_2, row3_space3 = st.beta_columns(
    (.1, 1, .1, 1, .1))
  
    with row3_1, _lock:
        
        df_2 = df.groupby('Designation')['Mental Fatigue Score'].mean()
    
        st.subheader('Designation')
        fig = Figure(figsize=(5, 3), dpi=60)
        ax = fig.subplots()
        sns.barplot(df_2.index,
                    df_2.values, color='skyblue', ax=ax)
        ax.set_xlabel('Designation')
        ax.set_ylabel('Average Mental Fatigue Score')
        st.pyplot(fig)



    with row3_2, _lock:
        df_2 = df.groupby('Resource Allocation')['Mental Fatigue Score'].mean()
        st.subheader("Resource Allocation")
        fig = Figure(figsize=(5, 3), dpi=60)
        ax = fig.subplots()
        sns.barplot(df_2.index,
                    df_2.values, color='skyblue', ax=ax)
        ax.set_xlabel('Resource Allocation')
        ax.set_ylabel('Average Mental Fatigue Score')
        st.pyplot(fig)

