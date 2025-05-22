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
from utils import get_all_oblig, get_by_cantons_oblig, get_by_agegroup_oblig, get_by_sex_oblig, make_line_plot
from utils import get_all_sentinella, get_by_region_sentinella, get_by_agegroup_sentinella, get_by_sex_sentinella
from utils import update_ss, preprocess_INFLUENZA, make_line_plot, make_area_plot
from datetime import datetime, timedelta



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


def prepare_data(progr_bar):
    progr_bar.progress(0.0, text="")
    progr_info.write('Preparing data and plots ...')
    df_obli = ss["data"]["data_di"]["INFLUENZA_oblig"]
    df_sent = ss["data"]["data_di"]["INFLUENZA_sentinella"]

    df_obli = preprocess_INFLUENZA(df_obli)
    df_sent = preprocess_INFLUENZA(df_sent)

    progr_bar.progress(0.2, text="")

    df_all_obli = get_all_oblig(df_obli)
    df_can_obli = get_by_cantons_oblig(df_obli)
    df_age_obli = get_by_agegroup_oblig(df_obli)
    df_sex_obli = get_by_sex_oblig(df_obli)
    df_all_sent = get_all_sentinella(df_sent)
    df_can_sent = get_by_region_sentinella(df_sent)
    df_age_sent = get_by_agegroup_sentinella(df_sent)
    df_sex_sent = get_by_sex_sentinella(df_sent)

    progr_bar.progress(0.4, text="")

    # merge-in all info
    df_can_obli = pd.merge(df_can_obli, df_all_obli[['date', 'incValue']], how='inner', on='date', suffixes=('', '_all'))
    df_can_sent = pd.merge(df_can_sent, df_all_sent[['date', 'incValue']], how='inner', on='date', suffixes=('', '_all'))
    df_age_obli = pd.merge(df_age_obli, df_all_obli[['date', 'incValue']], how='inner', on='date', suffixes=('', '_all'))
    df_age_sent = pd.merge(df_age_sent, df_all_sent[['date', 'incValue']], how='inner', on='date', suffixes=('', '_all'))
    df_sex_obli = pd.merge(df_sex_obli, df_all_obli[['date', 'incValue']], how='inner', on='date', suffixes=('', '_all'))
    df_sex_sent = pd.merge(df_sex_sent, df_all_sent[['date', 'incValue']], how='inner', on='date', suffixes=('', '_all'))

    progr_bar.progress(0.6, text="")

    # lineplots 
    ss["figures"]["fig_all_oblig"] = make_line_plot(df_all_obli, 'georegion', ss["colseq"]["fig_all_oblig"], y_title = 'Cases per 100000 inhab *', )
    ss["figures"]["fig_all_sent"]  = make_line_plot(df_all_sent, 'georegion', ss["colseq"]["fig_all_oblig"], y_title = 'Consultations per 100000 inhab *', )

    # if ss["upar"]["plot_type"] == 'Line': 
    ss["figures"]["fig_can_oblig"] = make_line_plot(df_can_obli, 'georegion', ss["colseq"]["fig_can_oblig"], y_title = 'Cases per 100000 inhab *', )
    ss["figures"]["fig_age_oblig"] = make_line_plot(df_age_obli, 'agegroup',  ss["colseq"]["fig_age_oblig"], y_title = 'Cases per 100000 inhab *',)
    ss["figures"]["fig_sex_oblig"] = make_line_plot(df_sex_obli, 'sex',       ss["colseq"]["fig_sex_oblig"], y_title = 'Cases per 100000 inhab *', )
    ss["figures"]["fig_can_sent"]  = make_line_plot(df_can_sent, 'georegion', ss["colseq"]["fig_reg_oblig"], y_title = 'Consultations per 100000 inhab *', )
    ss["figures"]["fig_age_sent"]  = make_line_plot(df_age_sent, 'agegroup',  ss["colseq"]["fig_age_oblig"], y_title = 'Consultations per 100000 inhab *', )
    ss["figures"]["fig_sex_sent"]  = make_line_plot(df_sex_sent, 'sex',       ss["colseq"]["fig_sex_oblig"], y_title = 'Consultations per 100000 inhab *', )

    # area plots
    # if ss["upar"]["plot_type"] == 'Area': 
    ss["figures"]["figa_can_oblig"] = make_area_plot(df_can_obli, 'georegion', ss["colseq"]["fig_can_oblig"], y_title = 'Cases per 100000 inhab *')
    ss["figures"]["figa_age_oblig"] = make_area_plot(df_age_obli, 'agegroup',  ss["colseq"]["fig_age_oblig"], y_title = 'Cases per 100000 inhab *')
    ss["figures"]["figa_sex_oblig"] = make_area_plot(df_sex_obli, 'sex',       ss["colseq"]["fig_sex_oblig"], y_title = 'Cases per 100000 inhab *')
    ss["figures"]["figa_can_sent"]  = make_area_plot(df_can_sent, 'georegion', ss["colseq"]["fig_reg_oblig"], y_title = 'Consultations per 100000 inhab *')
    ss["figures"]["figa_age_sent"]  = make_area_plot(df_age_sent, 'agegroup',  ss["colseq"]["fig_age_oblig"], y_title = 'Consultations per 100000 inhab *')    
    ss["figures"]["figa_sex_sent"]  = make_area_plot(df_sex_sent, 'sex',       ss["colseq"]["fig_sex_oblig"], y_title = 'Consultations per 100000 inhab *')

    progr_bar.progress(0.8, text="")
 
    if ss["upar"]["date_range"] == 'initial':
        delta_time = timedelta(days=100)
        # concat dates from both dfs to get global min and max 
        df_dates = pd.concat([df_obli['date'], df_sent['date']])
        time_options = df_dates.sort_values()
        t_sta = time_options.min() - delta_time
        t_sta = datetime(year = t_sta.year, month = t_sta.month, day = t_sta.day)
        t_end = time_options.max() + delta_time
        t_end = datetime(year = t_end.year, month = t_end.month, day = t_end.day)
        ss["upar"]["date_range"] = (t_sta, t_end)
        ss["upar"]["full_date_range"] = (t_sta, t_end)

    progr_bar.progress(1.0, text="")



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
            prepare_data(progr_bar)





