#--------------------             
# Author : Serge Zaugg
# Description : Streamlit page 
#--------------------

import streamlit as st
from streamlit import session_state as ss
from utils import draw_figures

co_main, _ = st.columns([0.4,0.6])   
with co_main:
    with st.form("colors_form"):
        
        cols_b = st.columns(6)   
        ss["colseq"]["fig_all_oblig"][0] = cols_b[0].color_picker("All",  ss["colseq"]["fig_all_oblig"][0])   
        
        st.text("  ")  
        st.text("Sex")  
        cols_b = st.columns(6)   
        ss["colseq"]["fig_sex_oblig"][0] = cols_b[0].color_picker("Female",  ss["colseq"]["fig_sex_oblig"][0])   
        ss["colseq"]["fig_sex_oblig"][1] = cols_b[1].color_picker("Male",    ss["colseq"]["fig_sex_oblig"][1])   
        ss["colseq"]["fig_sex_oblig"][2] = cols_b[2].color_picker("Unknown", ss["colseq"]["fig_sex_oblig"][2])   
        
        st.text("  ")  
        st.text("Type")  
        cols_b = st.columns(6)   
        ss["colseq"]["fig_typ_oblig"][0] = cols_b[0].color_picker("Female",  ss["colseq"]["fig_typ_oblig"][0])   
        ss["colseq"]["fig_typ_oblig"][1] = cols_b[1].color_picker("Male",    ss["colseq"]["fig_typ_oblig"][1])   
        ss["colseq"]["fig_typ_oblig"][2] = cols_b[2].color_picker("Unknown", ss["colseq"]["fig_typ_oblig"][2])   
        
        st.text("  ")  
        st.text("Age groups")  
        cols_b = st.columns(6)   
        ss["colseq"]["fig_age_oblig"][0] = cols_b[0].color_picker("00-04",   ss["colseq"]["fig_age_oblig"][0])   
        ss["colseq"]["fig_age_oblig"][1] = cols_b[1].color_picker("05-14",   ss["colseq"]["fig_age_oblig"][1])   
        ss["colseq"]["fig_age_oblig"][2] = cols_b[2].color_picker("15-29",   ss["colseq"]["fig_age_oblig"][2])   
        ss["colseq"]["fig_age_oblig"][3] = cols_b[3].color_picker("30-64",   ss["colseq"]["fig_age_oblig"][3])   
        ss["colseq"]["fig_age_oblig"][4] = cols_b[4].color_picker("65+",     ss["colseq"]["fig_age_oblig"][4])   
        ss["colseq"]["fig_age_oblig"][5] = cols_b[5].color_picker("Unknown", ss["colseq"]["fig_age_oblig"][5]) 
        
        st.text("")  
        st.text("")  
        submitted = st.form_submit_button("Confirm", type = "primary")
        if submitted:
            draw_figures(data = ss["data"], colseq =ss["colseq"])


 





