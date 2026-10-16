#--------------------             
# Author : Serge Zaugg
# Description : Main interactive visualization page 
#--------------------

# import pandas as pd 
import streamlit as st
from streamlit import session_state as ss
from utils import draw_figures, show_selected_plots
from utils import draw_figures, update_ss

# (2) sidebar
with st.sidebar:

    with st.container(border=True):

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




# else:  
show_selected_plots()
