#--------------------             
# Author : Serge Zaugg
# Description : Main interactive visualization page 
#--------------------

import pandas as pd 
import streamlit as st
from streamlit import session_state as ss
from utils import update_ss, show_selected_plots, download_all_data, draw_figures, prepare_data

if ss["data"]["data_di"] == "initial" or ss["upar"]["date_range"] == "initial" or len(ss["figures"]) == 0 :
    c02, c03, c04 = st.columns([0.3, 0.3, 0.5])
    c02.text("Download progress")
    progr_bar1 = c02.progress(0, text='')
    c02.text("Data preparation progress")
    progr_bar2 = c02.progress(0, text='')
    download_all_data(progr_bar1)
    prepare_data(progr_bar2)
    draw_figures(data = ss["data"], colseq =ss["colseq"])
    st.rerun()

else:  
    ca1, ca2 = st.columns([0.4, 0.4])
    # update time axes
    with ca1:
        with st.container(height=120, border=True):
            _ = st.slider("Time range to plot", min_value = ss["upar"]["full_date_range"][0], max_value = ss["upar"]["full_date_range"][1], value = ss["upar"]["date_range"], 
                format = "YYYY-MM-DD", label_visibility = "visible",key = "k_date_range", on_change=update_ss, args=["k_date_range", "date_range"])      
    with ca2:
        with st.container(height=120, border=True):
            ca1, ca2, ca3, _ = st.columns([0.3, 0.60, 0.15, 0.15])
            _ = ca1.segmented_control("Data source", options = ['oblig', 'sentinella'], selection_mode="multi",  default = ss["upar"]["selecte_data_sources"],
                                                key = "k_data_sou", on_change=update_ss, args=["k_data_sou", "selecte_data_sources"]) 
            _ = ca2.segmented_control("Data grouping", options = ['All', 'Age', 'Type', 'Sex', 'Region',], selection_mode="multi", default = ss["upar"]["selecte_data_groupings"],
                                                key = "k_data_gr", on_change=update_ss, args=["k_data_gr", "selecte_data_groupings"])
              
            # _ = ca3.segmented_control("Plot type", options = ['Line', 'Area'], selection_mode="single", default = ss["upar"]["plot_type"], 
            #                                     key = "k_plot_type", on_change = update_ss, args=["k_plot_type", "plot_type"])
            _ = ca3.select_slider("Plot type", options = ['Line', 'Area'], value=ss["upar"]["plot_type"], 
                                                key="k_plot_type", on_change = update_ss, args=["k_plot_type", "plot_type"])

            cb1, cb2, cb3 = st.columns([0.3, 0.60, 0.25])
                  
    with st.expander( "Info on incidence metrics"):
        st.text("""* Incidence is the rate of new events per period. Here, the number of new cases/consultations per week and normalized per 100000 inhabitants.\
        For groups, incidence is normalized within group.""")
        st.text("""° Relative incidence = inc. group / sum(inc. all groups).\
        Area plots only shown when overall incidence above cutoff value.\
        Can be adjusted in left panel.\
        """)

    # update x axis zoom for all available plots 
    for k in ss["figures"].keys():
        ss["figures"][k].update_xaxes(type="date", range=ss["upar"]["date_range"])

    show_selected_plots()











