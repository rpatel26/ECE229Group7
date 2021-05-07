import streamlit as st
import pandas as pd
import numpy as np
import time

st.title("Understanding your Employee's Stress Level")

st.write("""
# Our first app
Hello *world!*
""")

st.write("Here's example that using data to create a table:")
df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})
df

st.write("Example of line chart")
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c']
)
st.line_chart(chart_data)

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

st.write('Example of using a selectbox for options')
option = st.selectbox(
    'Which number do you like best?',
    df['first column']
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
