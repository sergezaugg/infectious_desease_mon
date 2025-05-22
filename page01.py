#--------------------             
# Author : Serge Zaugg
# Description : Page to reload data from FOPF API 
# not very useful as FOPH data update once per week only and you can reload with new browser window
#--------------------

import streamlit as st
from streamlit import session_state as ss
from utils import download_all_data, prepare_data

c01, c02, c03, c04 = st.columns([0.15, 0.3, 0.3, 0.5])
c02.text("Download progress")
progr_bar1 = c02.progress(0, text='')
c02.text(" ")

c02.text("Data preparation progress")
progr_bar2 = c02.progress(0, text='')
    
with c01:
    st.text("Fetch newest data")
    with st.form("form01", border=False, clear_on_submit=True, enter_to_submit=False): 
        submitted01 = st.form_submit_button("Load data", type="primary", use_container_width = False) 
        if submitted01:
            download_all_data(progr_bar1)
            prepare_data(progr_bar2)





