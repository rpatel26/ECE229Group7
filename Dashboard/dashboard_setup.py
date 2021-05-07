'''
This file intend to build a dashboard using streamlit to
provide end user visualization and analysis.
'''
import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import plotly.express as px

'''
Setting title
'''
st.title("Understanding Employee's Stress Level")
st.write("""
## Welcome to the Dashboad :) 
""")

'''
Table 1:
'''
st.write("Here's the data used to train prediction model")
train = pd.read_csv('../data/train.csv')
#remove missing values form last three coloms
train = train.dropna(subset=['Resource Allocation','Mental Fatigue Score',
                             'Burn Rate']).reset_index(drop=True)
st.write(train)



'''
Chart 1:
'''
#histogram
st.write("Example of line chart")
df = pd.DataFrame(train, columns = ['Mental Fatigue Score','Burn Rate'])
df = df.rename(columns = {'Mental Fatigue Score': 'fatigue'}, inplace = False)
values = st.sidebar.slider('Fatigure Score', 0., 10., (1., 9.))
f = px.histogram(df.query(f'fatigue.between{values}',engine='python'), x='fatigue', nbins=15, title='Fatigue Score Distribution')
f.update_xaxes(title='Mental Fatigue Score')
f.update_yaxes(title='Num of People')
st.plotly_chart(f)





st.write("Example of plotting a map")
map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [32.88, -117.20],
    columns=['lat', 'lon']
)
st.map(map_data)

st.write('Example of checkboxes')
if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c']
    )
    chart_data


# st.write("Here's example that using data to create a table:")
df2 = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})
# df
st.write('Example of using a selectbox for options')
option = st.selectbox(
    'Which number do you like best?',
    df2['first column']
)
'You selected: ', option

left_column, right_column = st.beta_columns(2)
pressed = left_column.button('Press')
if pressed:
    right_column.write('You press it!')

expander = st.beta_expander("FAQ")
expander.write("Here is the FAQ section")

st.write("Example of showing progress")
'Starting a long computation...'
latest_iteration = st.empty()
bar = st.progress(0)
for i in range(100):
    latest_iteration.text(f'Iteration{i + 1}')
    bar.progress(i + 1)
    time.sleep(0.1)
'...and now we are done!'
