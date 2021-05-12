import plotly.express as px
import streamlit as st

def setup_male_female_avg_plot(train):

    '''sets up the plot for average gender fatigue score -- static for now, can be adapted for dymanic change'''
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
    '''sets up a plot that is controlled with the sidepanels to control the distribution of the data in a histogram'''
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

    f = px.histogram(train_new.query(plot_query,engine='python'), x='Mental Fatigue Score', nbins=15, title='Fatigue Score Distribution')
    f.update_xaxes(title='Mental Fatigue Score')
    f.update_yaxes(title='Gender')
    st.write("Please use the sliders in the sidebar to adapt the following plot.")
    st.plotly_chart(f)
    