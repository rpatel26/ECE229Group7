import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
from sliders import *  
import prediction
from utils import * 
import feature_analysis
import home_page
from multiapp import MultiApp
import plots


def main():
    '''
    This file intends to build a dashboard using streamlit to
    provide end user visualization and analysis.
    '''
    st.set_page_config(layout="wide")
    app = MultiApp()
    app.add_app("Home Page", home_page.app)
    app.add_app("Data Exploration", plots.app)
    app.add_app("Feature Analysis", feature_analysis.app)
    app.add_app("Prediction", prediction.app)
    app.run()

if __name__ == "__main__":
    main()