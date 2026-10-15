#--------------------             
# Author : Serge Zaugg
# Description : Main interactive visualization page 
#--------------------

# import pandas as pd 
import streamlit as st
from streamlit import session_state as ss
from utils import download_all_data, prepare_data, draw_figures, show_selected_plots
from utils import draw_figures, update_ss

# (2) sidebar
with st.sidebar:

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



if ss["data"]["data_di"] == "initial" or ss["upar"]["date_range"] == "initial" or len(ss["figures"]) == 0 :
    c02, c03, c04 = st.columns([0.3, 0.3, 0.5])
    c02.text("Download progress")
    progr_bar1 = c02.progress(0, text='')
    c02.text("Data preparation progress")
    progr_bar2 = c02.progress(0, text='')
    download_all_data(progr_bar1)
    prepare_data(progr_bar2)
    draw_figures(data = ss["data"], colseq = ss["colseq"])
    st.rerun()
else:  
    show_selected_plots()
