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

st.set_page_config(layout="wide", initial_sidebar_state = "expanded", page_icon='pics/z_logo_turquoise.png')
apply_global_styles() # apply custom CSS styles 

#-------------------------------
# (1) data prep - do once on app start 
# this is then used in multiple session via cache 
if 'data_di' not in ss:
    
    # download and process data 
    ss.ref_date = pd.Timestamp.today().normalize()
    ss.data_di, ss.data_ve, ss.ts_downl = download_all_data(data_file = ["INFLUENZA_oblig", "INFLUENZA_sentinella"]) 
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
    ss.setdefault("cutoff_obli", 1.0)
    ss.setdefault("opt_dates", sorted(ss.df_can["date"].unique()))
    ss.setdefault("opt_datseel", ss.opt_dates[-1])
    ss.setdefault("opt_n_weeks", 7)
    ss.setdefault("col_max_inc", 2.0)
    ss.setdefault("col_max_cou", 50.0)
    # color items 
    ss.colo_all_oblig = ["#F8DDF0"]
    ss.colo_can_oblig = px.colors.qualitative.Alphabet
    ss.colo_reg_oblig = px.colors.qualitative.Light24
    ss.colo_age_oblig = ["#08fa20", "#bbff00", "#ffd900", "#ff7b00", "#ff0000", "#7c8584", "#ffffff"]
    ss.colo_sex_oblig = ["#f682df", "#51BEFD", "#7c8584",]
    ss.colo_typ_oblig = ["#fdd26d", "#7BFB95", "#7c8584",]

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
            <div>Data Version: <code>{}</code></div>
            <div>Downloaded: <code>{}</code></div>
            <div>Reference date: <code>{}</code></div>
        </div>
    """.format(ss["data_ve"]["name"], ss.ts_downl, ss.ref_date.date()),
    unsafe_allow_html=True)
    st.divider()

#-------------------------------
# (3) main navigation
pages = [
    st.Page("pages/page_monitor.py",  title="Latest status", default = True),
    st.Page("pages/page_map.py",  title="History - Cantons"),
    st.Page("pages/page_subgr.py",  title="History - Groups"),
    st.Page("pages/page_colors.py",  title="Colors"),
    st.Page("pages/page_info.py",  title="About"),
    st.Page("pages/page_disclaimer.py",  title="Disclaimer"),
    st.Page("pages/page99.py",  title="Dev"),
    ]
pg = st.navigation(pages, position = "top")
pg.run()

