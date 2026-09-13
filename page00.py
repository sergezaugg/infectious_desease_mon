#--------------------             
# Author : Serge Zaugg
# Description : Main interactive visualization page 
#--------------------

import pandas as pd 
import streamlit as st
from streamlit import session_state as ss
from utils import show_selected_plots, download_all_data, draw_figures, prepare_data

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

    # # update x axis zoom for all available plots 
    # for k in ss["figures"].keys():
    #     ss["figures"][k].update_xaxes(type = "date", range = ss["upar"]["date_range"])

    show_selected_plots()











