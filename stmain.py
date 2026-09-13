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
        "selecte_data_groupings" : ['All', 'Age', 'Type'],
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

    st.markdown(":blue[**Swiss influenza monitoring with weekly data from Federal Office of Public Health**]") 

    with st.container(border=True):

        if ss["upar"]["date_range"] != "initial":
            _ = st.slider("Time range to plot", min_value = ss["upar"]["full_date_range"][0], max_value = ss["upar"]["full_date_range"][1], value = ss["upar"]["date_range"], 
                format = "YYYY-MM-DD", label_visibility = "visible",key = "k_date_range", 
                on_change=update_ss, args=["k_date_range", "date_range"]) 
                
        # update x axis zoom for all available plots 
        for k in ss["figures"].keys():
            ss["figures"][k].update_xaxes(type = "date", range = ss["upar"]["date_range"])         

        _ = st.segmented_control("Data grouping", options = ['All', 'Age', 'Type', 'Sex', 'Region',], 
            selection_mode="multi", default = ss["upar"]["selecte_data_groupings"],
            key = "k_data_gr", on_change=update_ss, args=["k_data_gr", "selecte_data_groupings"])
        
        _ = st.segmented_control("Plot type", options = ['Line', 'Area'], 
            selection_mode = "single", default = ss["upar"]["plot_type"],
            key="k_plot_type", on_change = update_ss, args=["k_plot_type", "plot_type"])


   # user input for the two thresholds
    with st.form("thld_form", border=True):
        col1, col2 = st.columns([4, 2])
        with col1:
            ss["upar"]["cutoff_obli"] = st.slider("Area plot cutoff", min_value = 0.0, max_value = 10.0, step = 0.1, value = ss["upar"]["cutoff_obli"]) 
        with col2:
            st.text("")
            submitted = st.form_submit_button("Apply", type = "primary")
        if submitted:
            draw_figures(data = ss["data"], colseq = ss["colseq"])
            st.rerun()

    with st.expander( "Info on incidence metrics"):
        st.text("""Incidence given as number of new cases per week normalized per 100000 inhabitants.""")
        st.text("""For groups, incidence is normalized within group.""")
        st.text("""Relative incidence = inc. group / sum(inc. all groups).""")
        st.text("""Area plots shown when overall incidence above cutoff (can be adjusted).""")

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
    st.Page("page00.py",  title="Visualize"),
    st.Page("page01.py",  title="Color settings"),
    st.Page("page02.py",  title="Credits"),
    ]
pg = st.navigation(pages)
pg.run()





