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

co_main1, co_main2, _ = st.columns([0.4, 0.2, 0.2])  
with co_main1:
    with st.container(border=True, height = 550):
        cols_b = st.columns(6)   
        ss.colo_all_line[0] = cols_b[0].color_picker("Line-All",  ss.colo_all_line[0], key = "u1b")   
        ss.colo_sex_bar[0]   = cols_b[1].color_picker("Bar-Sex",  ss.colo_sex_bar[0], key = "u2b")  
        ss.colo_typ_bar[0]   = cols_b[2].color_picker("Bar-Type", ss.colo_typ_bar[0], key = "u3b")    
        ss.colo_age_bar[0]   = cols_b[3].color_picker("Bar-Age", ss.colo_age_bar[0], key = "u4b")    
        st.text("  ")  
        cols_b = st.columns(6)   
        ss.colo_sex_area[0] = cols_b[0].color_picker("Area-Female",  ss.colo_sex_area[0], key = "u2")   
        ss.colo_sex_area[1] = cols_b[1].color_picker("Area-Male",    ss.colo_sex_area[1], key = "u3")   
        ss.colo_sex_area[2] = cols_b[2].color_picker("Area-Unkn", ss.colo_sex_area[2], key = "u4")   
        st.text("  ")  
        cols_b = st.columns(6)   
        ss.colo_typ_area[0] = cols_b[0].color_picker("Area-Type-A",  ss.colo_typ_area[0], key = "u5")   
        ss.colo_typ_area[1] = cols_b[1].color_picker("Area-Type-B",  ss.colo_typ_area[1], key = "u6")   
        ss.colo_typ_area[2] = cols_b[2].color_picker("Area-Unkn", ss.colo_typ_area[2], key = "u7")   
        st.text("  ")  
        cols_b = st.columns(6)   
        ss.colo_age_area[0] = cols_b[0].color_picker("Area-00-04",   ss.colo_age_area[0], key = "u8")   
        ss.colo_age_area[1] = cols_b[1].color_picker("Area-05-14",   ss.colo_age_area[1], key = "u9")   
        ss.colo_age_area[2] = cols_b[2].color_picker("Area-15-29",   ss.colo_age_area[2], key = "u10")   
        ss.colo_age_area[3] = cols_b[3].color_picker("Area-30-64",   ss.colo_age_area[3], key = "u11")   
        ss.colo_age_area[4] = cols_b[4].color_picker("Area-65+",     ss.colo_age_area[4], key = "u12")   
        ss.colo_age_area[5] = cols_b[5].color_picker("Area-Unkn", ss.colo_age_area[5], key = "u13") 

   



