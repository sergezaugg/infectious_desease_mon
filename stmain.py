#--------------------             
# Author : Serge Zaugg
# Description : Main streamlit entry point
# Run locally : streamlit run stmain.py
#--------------------

import streamlit as st
from streamlit import session_state as ss
import numpy as np
import plotly.express as px
from utils import draw_figures
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
        "plot_type" : 'Area',
        "cutoff_obli" :  1.0,
        "cutoff_sent" : 20.0,
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
    st.info("Data version: " + ss["data"]["data_ve"]["name"])
    # new     
    with st.form("thld_form", border=False):
        with st.container(border=True):
            st.text("  ")  
            ss["upar"]["cutoff_obli"] = st.slider("Area plot cutoff (oblig)", min_value = 0.0, max_value = 10.0, step = 0.1, value = ss["upar"]["cutoff_obli"]) 
            ss["upar"]["cutoff_sent"] = st.slider("Area plot cutoff (sentinella)", min_value = 0.0, max_value = 200.0, step = 0.5, value = ss["upar"]["cutoff_sent"])          
            submitted = st.form_submit_button("Apply thresholds", type = "primary")
        if submitted:
            draw_figures(data = ss["data"], colseq =ss["colseq"])
            st.rerun()
    # st.title("")
    st.markdown(''':gray[CREDITS and LINKS]''')
    st.page_link("https://www.bag.admin.ch/", label=":gray[Data provided by FOPH]")
    st.page_link("https://www.idd.bag.admin.ch/portal-data", label=":gray[Data API]")
    st.page_link("https://www.idd.bag.admin.ch/dataexplorer", label=":gray[Official frontend of FOPH]")
    st.page_link("https://www.idd.bag.admin.ch/survey-systems/oblig", label=":gray[Mandatory reporting (oblig)]")
    st.page_link("https://www.idd.bag.admin.ch/survey-systems/sentinella", label=":gray[Voluntary surveillance (sentinella)]")
    # logos an links
    # st.header("")
    c1,c2=st.columns([80,200])
    c1.image(image='pics/z_logo_blue.png', width=65)
    c2.markdown(''':gray[Frontend app v1.0.2]  
    :gray[Created by]
    :gray[[Serge Zaugg](https://www.linkedin.com/in/dkifh34rtn345eb5fhrthdbgf45/)]    
    :gray[[Pollito-ML](https://github.com/sergezaugg)]
    ''')
    st.logo(image='pics/z_logo_blue.png', size="large", link="https://github.com/sergezaugg")


# (2) main navigation
pages = [
    st.Page("page03.py",  title="Visualize"),
    st.Page("page04.py",  title="Color settings"),
    # st.Page("page00.py",  title="Background Info"),
    # st.Page("page02.py",  title="Tabular Data"),
    ]
pg = st.navigation(pages)
pg.run()





