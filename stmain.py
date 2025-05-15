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
        "data_ve" : {'name' : "Data not yet loaded!"},
        }

if 'colseq' not in ss:
    ss["colseq"] = {
        "fig_all" : ["#fcf808"],
        "fig_can" : ['#ffbb00', '#0077ff', '#33ff00', '#00ffff', '#ff00ff', '#ffff66', '#ff0000'],
        "fig_age" : ["#ffff00", "#00ff00", "#00ffff", "#0000ff", "#ff00ff", "#ff0000", "#ffffff"],
        "fig_sex" : ["#fc9107", "#0727F7", "#7c8584",],
        }

if 'figures' not in ss:
    ss["figures"] = {
         "fig_all" : None,
         "fig_can" : None,
         "fig_age" : None,
         "fig_sex" : None,
    }



# -------------------
# (2) main navigation

st.set_page_config(layout="wide")
 
pages = [
    st.Page("page01.py",  title="Load data"),
    st.Page("page02.py",  title="Check active data"),
    st.Page("page03.py",  title="Plot INFLUENZA"),
    st.Page("page04.py",  title="Color Settings"),
    ]

pg = st.navigation(pages)

pg.run()

with st.sidebar:
    st.info("App v0.0.0 - under initial devel")
    # st.markdown(''':blue[QUICK GUIDE]''')
    # st.text("(1) Define distributional scenarios")
    # st.text("(2) Run simulations")
    # st.text("(3) Check the plotted results")


    st.info("Data version: " + ss["data"]["data_ve"]["name"])

    st.title(""); st.title(""); st.title(""); 
    st.title(""); st.title("")
    st.markdown(''':gray[RELATED TOPICS]''')

    st.page_link("https://www.bag.admin.ch/", label=":gray[Federal Office of Public Health ]")
    st.page_link("https://www.idd.bag.admin.ch/portal-data", label=":gray[Data API provided by FOPH]")

    # st.page_link("https://ml-performance-metrics.streamlit.app/", label=":gray[ml-performance-metrics]")
    # st.page_link("https://featureimportance.streamlit.app/", label=":gray[feature-importance:red]")




