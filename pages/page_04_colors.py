#--------------------             
# Author : Serge Zaugg
# Description : Streamlit color selection page 
#--------------------

import streamlit as st
from streamlit import session_state as ss

with st.sidebar:
    st.markdown("""
    Colors can be adjusted here (will trigger re-rendering of plots).
    """)

co_main1, co_main2, _ = st.columns([0.4, 0.4, 0.2])  
with co_main1:
    with st.container(border=True, height = 450):
        cols_b = st.columns(6)   
        ss.colo_all_oblig[0] = cols_b[0].color_picker("All",  ss.colo_all_oblig[0])   
        st.text("  ")  
        cols_b = st.columns(6)   
        ss.colo_sex_oblig[0] = cols_b[0].color_picker("Female",  ss.colo_sex_oblig[0], key = "u2")   
        ss.colo_sex_oblig[1] = cols_b[1].color_picker("Male",    ss.colo_sex_oblig[1], key = "u3")   
        ss.colo_sex_oblig[2] = cols_b[2].color_picker("Unknown", ss.colo_sex_oblig[2], key = "u4")   
        st.text("  ")  
        cols_b = st.columns(6)   
        ss.colo_typ_oblig[0] = cols_b[0].color_picker("Type A",  ss.colo_typ_oblig[0], key = "u5")   
        ss.colo_typ_oblig[1] = cols_b[1].color_picker("Type B",  ss.colo_typ_oblig[1], key = "u6")   
        ss.colo_typ_oblig[2] = cols_b[2].color_picker("Unknown", ss.colo_typ_oblig[2], key = "u7")   
        st.text("  ")  
        cols_b = st.columns(6)   
        ss.colo_age_oblig[0] = cols_b[0].color_picker("00-04",   ss.colo_age_oblig[0], key = "u8")   
        ss.colo_age_oblig[1] = cols_b[1].color_picker("05-14",   ss.colo_age_oblig[1], key = "u9")   
        ss.colo_age_oblig[2] = cols_b[2].color_picker("15-29",   ss.colo_age_oblig[2], key = "u10")   
        ss.colo_age_oblig[3] = cols_b[3].color_picker("30-64",   ss.colo_age_oblig[3], key = "u11")   
        ss.colo_age_oblig[4] = cols_b[4].color_picker("65+",     ss.colo_age_oblig[4], key = "u12")   
        ss.colo_age_oblig[5] = cols_b[5].color_picker("Unknown", ss.colo_age_oblig[5], key = "u13") 

   



