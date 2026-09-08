#--------------------             
# Author : Serge Zaugg
# Description : Streamlit color selection page 
#--------------------

import streamlit as st
from streamlit import session_state as ss
from utils import draw_figures

with st.form("colors_form", border=False):
    co_main1, co_main2, _ = st.columns([0.4,0.4, 0.2])  
    with co_main1:
        with st.container(border=True, height = 450):
            cols_b = st.columns(6)   
            ss["colseq"]["fig_all_oblig"][0] = cols_b[0].color_picker("All",  ss["colseq"]["fig_all_oblig"][0])   
            
            st.text("  ")  
            cols_b = st.columns(6)   
            ss["colseq"]["fig_sex_oblig"][0] = cols_b[0].color_picker("Female",  ss["colseq"]["fig_sex_oblig"][0])   
            ss["colseq"]["fig_sex_oblig"][1] = cols_b[1].color_picker("Male",    ss["colseq"]["fig_sex_oblig"][1])   
            ss["colseq"]["fig_sex_oblig"][2] = cols_b[2].color_picker("Unknown", ss["colseq"]["fig_sex_oblig"][2], key = "u1")   
            
            st.text("  ")  
            cols_b = st.columns(6)   
            ss["colseq"]["fig_typ_oblig"][0] = cols_b[0].color_picker("Type A",  ss["colseq"]["fig_typ_oblig"][0])   
            ss["colseq"]["fig_typ_oblig"][1] = cols_b[1].color_picker("Type B",  ss["colseq"]["fig_typ_oblig"][1])   
            ss["colseq"]["fig_typ_oblig"][2] = cols_b[2].color_picker("Unknown", ss["colseq"]["fig_typ_oblig"][2], key = "u2")   
            
            st.text("  ")  
            cols_b = st.columns(6)   
            ss["colseq"]["fig_age_oblig"][0] = cols_b[0].color_picker("00-04",   ss["colseq"]["fig_age_oblig"][0])   
            ss["colseq"]["fig_age_oblig"][1] = cols_b[1].color_picker("05-14",   ss["colseq"]["fig_age_oblig"][1])   
            ss["colseq"]["fig_age_oblig"][2] = cols_b[2].color_picker("15-29",   ss["colseq"]["fig_age_oblig"][2])   
            ss["colseq"]["fig_age_oblig"][3] = cols_b[3].color_picker("30-64",   ss["colseq"]["fig_age_oblig"][3])   
            ss["colseq"]["fig_age_oblig"][4] = cols_b[4].color_picker("65+",     ss["colseq"]["fig_age_oblig"][4])   
            ss["colseq"]["fig_age_oblig"][5] = cols_b[5].color_picker("Unknown", ss["colseq"]["fig_age_oblig"][5], key = "u3") 

    submitted = st.form_submit_button("Save changes", type = "primary")
    if submitted:
        draw_figures(data = ss["data"], colseq =ss["colseq"])
