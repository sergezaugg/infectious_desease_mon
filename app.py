#--------------------             
# Author : Serge Zaugg
# Description : Main streamlit entry point
# Run locally : streamlit run stmain.py
#--------------------

import streamlit as st
from streamlit import session_state as ss
import numpy as np
import plotly.express as px
from utils import draw_figures, update_ss
st.set_page_config(layout="wide", initial_sidebar_state = "expanded")

# (1) set initial session state
if 'upar' not in ss:
    ss["upar"] = {
        "full_date_range" : "initial",
        "date_range" : "initial",
        "par03" : "initial",
        "par04" : "initial",
        "selecte_data_groupings" : ['All', 'Age', 'Type', 'Sex', 'Region',],
        "plot_type" : 'Area',
        "cutoff_obli" :  1.0,
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
        "fig_reg_oblig" : px.colors.qualitative.Light24, 
        "fig_age_oblig" : ["#00ffd5", "#bbff00", "#ffd900", "#ff7b00", "#ff0000", "#7c8584", "#ffffff"],
        "fig_sex_oblig" : ["#fd6804", "#0727F7", "#7c8584",],
        "fig_typ_oblig" : ["#7802e6", "#02BB2A", "#7c8584",],
        }

if 'figures' not in ss:
    ss["figures"] = dict()


# (2) sidebar
with st.sidebar:

    st.markdown(":blue[**Swiss Weekly Influenza Monitoring**]") 

    # Data version
    st.info("Data from " + ss["data"]["data_ve"]["name"] + " downloaded via FOPH API")

    # logos an links        
    c1,c2=st.columns([70,200])
    c1.image(image='pics/z_logo_blue.png', width=65)
    c2.markdown(''':primary[v1.1.2]  
    :primary[Created by]
    :primary[[Serge Zaugg](https://www.linkedin.com/in/dkifh34rtn345eb5fhrthdbgf45/)]    
    :primary[[Pollito-ML](https://github.com/sergezaugg)]
    ''')
    st.logo(image='pics/z_logo_blue.png', size="large", link="https://github.com/sergezaugg")


# (3) main navigation
pages = [
    st.Page("pages/page00.py",  title="Visualize"),
    st.Page("pages/page01.py",  title="Color settings"),
    st.Page("pages/page02.py",  title="Credits"),
    ]
pg = st.navigation(pages, position = "top")
pg.run()





