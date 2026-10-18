#--------------------             
# Author : Serge Zaugg
# Description : Main interactive visualization page 
#--------------------

import streamlit as st
from streamlit import session_state as ss
from src.utils_ui import draw_figures

with st.sidebar:
    # user input for the two thresholds
    ss.cutoff_obli = st.slider("Area plot cutoff", 
        min_value = 0.0, 
        max_value = 10.0, 
        step = 0.1, 
        value = ss.cutoff_obli, 
        key="cutoff_slider",) 
    
    ss.fig_all_oblig = draw_figures(ss.df_all, ss.df_age, ss.df_sex, ss.df_typ, cutoff = ss.cutoff_obli, 
        colo = [ss.colo_all_oblig, ss.colo_age_oblig , ss.colo_sex_oblig, ss.colo_typ_oblig])

st.plotly_chart(ss.fig_all_oblig,  use_container_width=True, theme=None, config={"displayModeBar": False}, key = "k001")

