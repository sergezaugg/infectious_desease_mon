#--------------------             
# Author : Serge Zaugg
# Description : tbd
#--------------------

import pandas as pd 
import streamlit as st
from streamlit import session_state as ss
from utils import update_ss, show_selected_plots, download_all_data, draw_figures, prepare_data

if ss["data"]["data_di"] == "initial" or ss["upar"]["date_range"] == "initial":

    st.cache_data.clear() # quick fix
   
    c02, c03, c04 = st.columns([0.3, 0.3, 0.5])
    c02.text("Download progress")
    progr_bar1 = c02.progress(0, text='')
    c02.text("Data preparation progress")
    progr_bar2 = c02.progress(0, text='')
    download_all_data(progr_bar1)
    prepare_data(progr_bar2)
    st.rerun()

else:  

    draw_figures(data = ss["data"], colseq =ss["colseq"])

    ca1, ca2 = st.columns([0.4, 0.4])
    # update time axes
    with ca1:
        with st.container(height=125, border=True):
            _ = st.slider("Time range to plot", min_value = ss["upar"]["full_date_range"][0], max_value = ss["upar"]["full_date_range"][1], value = ss["upar"]["date_range"], 
                format = "YYYY-MM-DD", label_visibility = "visible",key = "k_date_range", on_change=update_ss, args=["k_date_range", "date_range"])      
    with ca2:
        with st.container(height=125, border=True):
            ca1, ca2, ca3, ca4 = st.columns([0.3, 0.4, 0.3, 0.2])
            _ = ca1.segmented_control("Data source", options = ['oblig', 'sentinella'], selection_mode="multi",  default = ss["upar"]["selecte_data_sources"],
                                                key = "k_data_sou", on_change=update_ss, args=["k_data_sou", "selecte_data_sources"]) 
            _ = ca2.segmented_control("Data grouping", options = ['All', 'Sex', 'Age', 'Region'], selection_mode="multi", default = ss["upar"]["selecte_data_groupings"],
                                                key = "k_data_gr", on_change=update_ss, args=["k_data_gr", "selecte_data_groupings"])  
            _ = ca3.segmented_control("Plot type", options = ['Line', 'Area'], selection_mode="single", default = ss["upar"]["plot_type"], 
                                                key = "k_plot_type", on_change=update_ss, args=["k_plot_type", "plot_type"])
            ca4.text(" ")
            cb1, cb2, cb3 = st.columns([0.4, 0.15, 0.5])
            cb1.text("Links to data source details:")
            cb2.page_link("https://www.idd.bag.admin.ch/survey-systems/oblig",      label=":blue[oblig]")  
            cb3.page_link("https://www.idd.bag.admin.ch/survey-systems/sentinella", label=":blue[sentinella]")   

    st.text("""* Incidence is the rate of new events over a specified period. Here, the number of new cases/consultations per week and per 100000 inhabitants.\
    For groups, incidence is normalized within group, e.g. per 100000 inh. in age-group '+65'""")
    st.text("""° Area plots only shown when overall incidence was above 1.0. \
    Relative incidence = inc. group / sum(inc. all groups) <experimental!>""")
    show_selected_plots()











