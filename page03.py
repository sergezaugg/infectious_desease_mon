#--------------------             
# Author : Serge Zaugg
# Description : tbd
#--------------------

import pandas as pd 
import streamlit as st
from streamlit import session_state as ss
from utils import update_ss, show_selected_plots

if ss["data"]["data_di"] == "initial":
    st.info("Data not yet loaded!  --->   Please navigate to 'Load data' menu (left) and then click on 'Load data' button.")
else:    

    ca1, ca2 = st.columns([0.4, 0.4])
    # update time axes
    with ca1:
        with st.container(height=125, border=True):
            _ = st.slider("Time range to plot", min_value = ss["upar"]["full_date_range"][0], max_value = ss["upar"]["full_date_range"][1], 
                value = ss["upar"]["date_range"], format = "YYYY-MM-DD", label_visibility = "visible",
                key = "k_date_range", on_change=update_ss, args=["k_date_range", "date_range"]
                )     
        
    with ca2:
        with st.container(height=125, border=True):
            with st.form("form02", border=False, clear_on_submit=False, enter_to_submit=False): 
                ca1, ca2, ca3, ca4 = st.columns([0.3, 0.4, 0.3, 0.2])
                with ca1:
                    sel_dat_sou = st.segmented_control("Data source", options = ['oblig', 'sentinella'], selection_mode="multi", default = ['oblig', 'sentinella']) 
                with ca2:
                    sel_dat_grou = st.segmented_control("Data grouping", options = ['All', 'Sex', 'Age', 'Region'], selection_mode="multi", default = ['All'])
                with ca3:
                    ss["upar"]["plot_type"] = st.segmented_control("Plot type", options = ['Line', 'Area'], selection_mode="single", default = ss["upar"]["plot_type"])
                                                        # key = "k_plot_type", on_change=update_ss, args=["k_plot_type", "plot_type"])
                with ca4:
                    st.text(" ")
                    submitted02 = st.form_submit_button("Apply", type="primary", use_container_width = False) 
                if submitted02: 
                    ss["upar"]["selecte_data_sources"] = sel_dat_sou
                    ss["upar"]["selecte_data_groupings"] = sel_dat_grou

            cb1, cb2, cb3 = st.columns([0.4, 0.15, 0.5])
            cb1.text("Links to data source details:")
            cb2.page_link("https://www.idd.bag.admin.ch/survey-systems/oblig",      label=":blue[oblig]")  
            cb3.page_link("https://www.idd.bag.admin.ch/survey-systems/sentinella", label=":blue[sentinella]")   


    st.text("* Incidence is the rate of new events over a specified period. Here, the number of new cases/consultations per week and per 100000 inhabitants.")

    show_selected_plots()











