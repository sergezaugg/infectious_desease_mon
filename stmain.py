#--------------------             
# Author : Serge Zaugg
# Description : Main streamlit entry point
# Run locally : streamlit run stmain.py
#--------------------

import streamlit as st
from streamlit import session_state as ss
import numpy as np
import plotly.express as px
st.set_page_config(layout="wide")

# (1) set initial session state
if 'upar' not in ss:
    ss["upar"] = {
        "full_date_range" : "initial",
        "date_range" : "initial",
        "par03" : "initial",
        "par04" : "initial",
        "selecte_data_sources" : ['oblig'],
        "selecte_data_groupings" : ['All', 'Age', 'Type'],
        "plot_type" : 'Area'
        }

if 'data' not in ss:
    ss["data"] = {
        "data_di" : "initial",
        "data_ve" : {'name' : "Data not yet loaded!"},
        }

if 'colseq' not in ss:
    ss["colseq"] = {
        "fig_all_oblig" : ["#FC08B3"],
        "fig_can_oblig" : px.colors.qualitative.Alphabet,
        "fig_reg_oblig" : px.colors.qualitative.Light24, #Plotly,
        "fig_age_oblig" : ["#00ffd5", "#bbff00", "#ffd900", "#ff7b00", "#ff0000", "#7c8584", "#ffffff"],
        "fig_sex_oblig" : ["#fd6804", "#0727F7", "#7c8584",],
        "fig_typ_oblig" : ["#7802e6", "#02BB2A", "#7c8584",],
        }

if 'figures' not in ss:
    ss["figures"] = dict()


with st.sidebar:
    st.info("App v0.5.1 - under devel")
    st.info("Data version: " + ss["data"]["data_ve"]["name"])
    st.title(""); st.title(""); st.title(""); 
    st.markdown(''':gray[CREDITS / LINKS]''')
    st.page_link("https://www.bag.admin.ch/", label=":gray[Federal Office of Public Health]")
    st.page_link("https://www.idd.bag.admin.ch/portal-data", label=":gray[Data API provided by FOPH]")
    st.page_link("https://www.idd.bag.admin.ch/dataexplorer", label=":gray[Official frontend of FOPH]")
    st.markdown(''':gray[MORE COOL STUFF]''')
    st.page_link("https://ml-performance-metrics.streamlit.app/", label=":gray[ml-performance-metrics]")


# (2) main navigation

pages = [
    st.Page("page03.py",  title="Visualize"),
    st.Page("page04.py",  title="Color Settings"),
    st.Page("page00.py",  title="Background Info"),
    st.Page("page02.py",  title="Tabular Data"),
    ]
pg = st.navigation(pages)
pg.run()





