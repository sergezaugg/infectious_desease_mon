#--------------------             
# Author : Serge Zaugg
# Description : tbd
#--------------------

import requests
import pandas as pd 
import io
import plotly.express as px
import streamlit as st
from streamlit import session_state as ss



def download_all_data(progr_bar):
    full_query_string = 'https://api.idd.bag.admin.ch/api/v1/data/version'
    r = requests.get(full_query_string, allow_redirects=True)
    data_version = r.json()

    full_query_string = 'https://api.idd.bag.admin.ch/api/v1/export/latest/files'
    r = requests.get(full_query_string, allow_redirects=True)
    data_file_list = r.json()

    # limit to specific diseases , for now 
    data_file_list =[a for a in data_file_list if a == "INFLUENZA_oblig" or a == "INFLUENZA_sentinella"]

    n_files = len(data_file_list)

    data_di = {}
    for li_index in range(len(data_file_list)):
        print(li_index)
        data_set_name = data_file_list[li_index]
        full_query_string = 'https://api.idd.bag.admin.ch/api/v1/export/latest/' + data_set_name + '/csv'
        r = requests.get(full_query_string, allow_redirects=True)
        raw_text = r.text
        df = pd.read_csv(io.StringIO(raw_text, newline='\n')  , sep=",")
        data_di[data_set_name] = df
        # update status notifications 
        progr_bar.progress((li_index+1)/n_files, text="")
        progr_info.write('loading ' + data_set_name + ' ...')
          
    ss["data"]["data_di"] = data_di
    ss["data"]["data_ve"] = data_version
    progr_info.write('Done!')

    st.page_link("page03.py", label="Go to visualization tab")

    # # [data_di[a].shape for a in data_di.keys()]
    # return(data_version, data_di)




c01, c02, c03 = st.columns([0.15, 0.3, 1.0])
with c02:
    st.text("Download progress")
    progr_bar = st.progress(0, text='')
    progr_info = st.info("")

with c01:
    st.text("Get newest data via FOPH's API")
    with st.form("form01", border=False, clear_on_submit=True, enter_to_submit=False): 
        submitted01 = st.form_submit_button("Load data", type="primary", use_container_width = False) 
        if submitted01:
            download_all_data(progr_bar)





