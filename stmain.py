#--------------------             
# Author : Serge Zaugg
# Description : Main streamlit entry point
# Run locally : streamlit run stmain.py
#--------------------

import streamlit as st
from streamlit import session_state as ss
import numpy as np

# (1) ---------------------
# set initial session state

# keep track of user-provided params
if 'upar' not in ss:
    ss["upar"] = {
        "par01" : "initial",
        "par02" : "initial",
        "par03" : "initial",
        "par04" : "initial",
        }


if 'data' not in ss:
    ss["data"] = {
        "data_di" : "initial",
        "data_ve" : "initial",
    }


if 'colseq' not in ss:
    ss["colseq"] = {
        "fig_all" : ['#ffbb00', '#0077ff', '#33ff00', '#00ffff', '#ff00ff', '#ffff66', '#ff0000'],
        "fig_can" : ['#ffbb00', '#0077ff', '#33ff00', '#00ffff', '#ff00ff', '#ffff66', '#ff0000'],
        "fig_age" : ['#ffbb00', '#0077ff', '#33ff00', '#00ffff', '#ff00ff', '#ffff66', '#ff0000'],
        "fig_sex" : ['#ffbb00', '#0077ff', '#33ff00', '#00ffff', '#ff00ff', '#ffff66', '#ff0000'],
    }






# -------------------
# (2) main navigation

st.set_page_config(layout="wide")
 
pages = [
    st.Page("page01.py",  title="Get new data"),
    st.Page("page02.py",  title="Check active data"),
    st.Page("page03.py",  title="Plot INFLUENZA"),
    # st.Page("st_page_03.py",  title="Settings"),
    ]

pg = st.navigation(pages)

pg.run()

with st.sidebar:
    st.text("v0.5.0 - under devel")
    # st.markdown(''':blue[QUICK GUIDE]''')
    # st.text("(1) Define distributional scenarios")
    # st.text("(2) Run simulations")
    # st.text("(3) Check the plotted results")
    st.title(""); st.title(""); st.title(""); 
    st.title(""); st.title("")
    st.markdown(''':gray[RELATED TOPICS]''')
    st.page_link("https://ml-performance-metrics.streamlit.app/", label=":gray[ml-performance-metrics]")
    # st.page_link("https://featureimportance.streamlit.app/", label=":gray[feature-importance:red]")
