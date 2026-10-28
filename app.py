#--------------------             
# Author : Serge Zaugg
# Description : Main streamlit entry point
# Run locally : streamlit run stmain.py
#--------------------

import streamlit as st
from streamlit import session_state as ss
import plotly.express as px
from src.utilsdataprep import download_all_data, preprocess_INFLUENZA
from src.utilsdataprep import get_all_oblig,get_by_cantons_oblig, get_by_agegroup_oblig, get_by_sex_oblig,get_by_type_oblig
from resources.styles import apply_global_styles
import pandas as pd
from plotly.colors import sample_colorscale 

st.set_page_config(layout="wide", initial_sidebar_state = "expanded", page_title = "Swiss Influenza Monitor", page_icon='pics/z_logo_turquoise.png')
apply_global_styles() # apply custom CSS styles 

#-------------------------------
# (1) data prep - do once on app start 
# this is then used in multiple session via cache 
if 'data_di' not in ss:
    
    # download and pre-process data 
    ss.data_di, ss.data_ve, ss.ts_downl, ss.dl_status = download_all_data(data_file = ["INFLUENZA_oblig", "INFLUENZA_sentinella"]) 
    ss.ref_date = pd.Timestamp.today().normalize()
    # take weekly data, make continuous time variable, re-code agegroup 
    df_obli = preprocess_INFLUENZA(ss.data_di["INFLUENZA_oblig"])
    # take data for all i.e. not grouped 
    ss.df_all = get_all_oblig(df_obli)
    # take incidence for specific sub-groups 
    df_can_obli = get_by_cantons_oblig(df_obli)
    df_age_obli = get_by_agegroup_oblig(df_obli)
    df_sex_obli = get_by_sex_oblig(df_obli)
    df_typ_obli = get_by_type_oblig(df_obli)
    # add incidence of ungrpouped 'all' for each date to the sub-groups df , needed to compute proportions 
    ss.df_can = pd.merge(df_can_obli, ss.df_all[['date', 'incValue']], how='inner', on='date', suffixes=('', '_all'))
    ss.df_age = pd.merge(df_age_obli, ss.df_all[['date', 'incValue']], how='inner', on='date', suffixes=('', '_all'))
    ss.df_sex = pd.merge(df_sex_obli, ss.df_all[['date', 'incValue']], how='inner', on='date', suffixes=('', '_all'))
    ss.df_typ = pd.merge(df_typ_obli, ss.df_all[['date', 'incValue']], how='inner', on='date', suffixes=('', '_all'))
    
    # non-data items
    ss.setdefault("opt_dates", sorted(ss.df_can["date"].unique()))
    ss.setdefault("col_max_inc", 2.0)
    ss.setdefault("col_max_cou", 50.0)
    # subgroup page 
    ss.setdefault("cutoff_obli", 1.0)
    # monitor page 
    ss.setdefault("mon_slider_window", 10)
    ss.setdefault("mon_col_thld_1", ss.col_max_inc)
    
    # history (map) page 
    ss.setdefault("k_col_max_inx", ss.col_max_inc)
    ss.setdefault("k_col_max_cou", ss.col_max_cou)
    ss.setdefault("hexa_weeks_pills", 10)
    ss.setdefault("hexa_date_slider", ss.opt_dates[-1])
    
    # color items 
    ss.colo_all_oblig = ["#F25B10"]
    ss.colo_can_oblig = px.colors.qualitative.Alphabet
    ss.colo_reg_oblig = px.colors.qualitative.Light24
    ss.colo_age_oblig = ["#08fa20", "#bbff00", "#edd131", "#d77921", "#d12121", "#7c8584", "#ffffff"]
    ss.colo_sex_oblig = ["#f682df", "#37A2DF", "#7c8584",]
    ss.colo_typ_oblig = ["#df951d", "#17DB3E", "#7c8584",]
    
    # color maps
    ss.color_map_01 = sample_colorscale("rainbow", 10, low=0.45, high=0.85)
    ss.color_map_02 = "bluered"


st.write(ss.data_di["INFLUENZA_oblig"])

# Protects every ss key from being deleted (for multi-page consistency across clicks)
for key in list(st.session_state.keys()):
    st.session_state[key] = st.session_state[key]

#-------------------------------
# (2) sidebar
with st.sidebar:
    st.logo(image='pics/z_logo_blue.png', size="large", link="https://github.com/sergezaugg")
    st.markdown("## :primary[**Swiss Influenza Monitor**]") 
    st.markdown("""
        <div style="line-height: 1.3; margin-bottom: 0.9em;;">
            <div>Data Version: <code style="color:cyan">{}</code></div>
            <div>Downloaded: <code style="color:cyan">{}</code></div>
            <div>Reference date: <code style="color:cyan">{}</code></div>
        </div>
    """.format(ss["data_ve"]["name"], ss.ts_downl, ss.ref_date.date()),
    unsafe_allow_html=True)
    st.caption(ss.dl_status)
    st.divider()

#-------------------------------
# (3) main navigation
pages = [
    st.Page("pages/page_monitor.py",  title="Latest status", default = True),
    st.Page("pages/page_map.py",  title="History CNT"),
    st.Page("pages/page_subgr.py",  title="History GRP"),
    st.Page("pages/page_colors.py",  title="Colors"),
    st.Page("pages/page_info.py",  title="About"),
    st.Page("pages/page_disclaimer.py",  title="Disclaimer"),
    st.Page("pages/page_dev.py",  title="Dev"),
    ]
pg = st.navigation(pages, position = "top")
pg.run()

