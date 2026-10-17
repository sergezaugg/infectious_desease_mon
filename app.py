#--------------------             
# Author : Serge Zaugg
# Description : Main streamlit entry point
# Run locally : streamlit run stmain.py
#--------------------

import streamlit as st
from streamlit import session_state as ss
import plotly.express as px
from utilsdataprep import download_all_data, prepare_data
from resources.styles import apply_global_styles

st.set_page_config(layout="wide", initial_sidebar_state = "expanded", page_icon='pics/z_logo_turquoise.png')
apply_global_styles() # apply custom CSS styles 

#-------------------------------
# (1) data prep - do once on app start 
# this is then used in multiple session via cache 
if 'data_di' not in ss:
    # data items 
    ss.data_di, ss.data_ve = download_all_data()
    a,b,c,d,e = prepare_data(df_obli = ss.data_di["INFLUENZA_oblig"])
    ss.df_all = a
    ss.df_can = b
    ss.df_age = c
    ss.df_sex = d
    ss.df_typ = e
    # non-data items
    ss.setdefault("cutoff_obli", 1.0)
    ss.setdefault("opt_dates", sorted(ss.df_can["date"].unique()))
    ss.setdefault("opt_datseel", ss.opt_dates[-1])
    ss.setdefault("opt_n_weeks", 7)
    ss.setdefault("col_max_inc", 0.5)
    ss.setdefault("col_max_cou", 50.0)
    # color items 
    ss.colo_all_oblig = ["#F8DDF0"]
    ss.colo_can_oblig = px.colors.qualitative.Alphabet
    ss.colo_reg_oblig = px.colors.qualitative.Light24
    ss.colo_age_oblig = ["#00ffd5", "#bbff00", "#ffd900", "#ff7b00", "#ff0000", "#7c8584", "#ffffff"]
    ss.colo_sex_oblig = ["#fe21d2", "#0539F5", "#7c8584",]
    ss.colo_typ_oblig = ["#ff5e00", "#01FF51", "#7c8584",]

# Protects every ss key from being deleted (for multi-page consistency across clicks)
for key in list(st.session_state.keys()):
    st.session_state[key] = st.session_state[key]

#-------------------------------
# (2) sidebar
with st.sidebar:
    st.markdown("## :primary[**Swiss Weekly Influenza Monitoring**]") 
    st.write("Data version " + ss["data_ve"]["name"])
    st.divider()
    st.logo(image='pics/z_logo_blue.png', size="large", link="https://github.com/sergezaugg")

#-------------------------------
# (3) main navigation
pages = [
    st.Page("pages/page_history.py",  title="Flu History"),
    st.Page("pages/page_map.py",  title="Geo-Map", default = True),
    st.Page("pages/page_colors.py",  title="Colors"),
    st.Page("pages/page_info.py",  title="Info"),
    st.Page("pages/page_disclaimer.py",  title="Disclaimer"),
    st.Page("pages/page99.py",  title="Dev"),
    ]
pg = st.navigation(pages, position = "top")
pg.run()





