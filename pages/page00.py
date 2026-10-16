#--------------------             
# Author : Serge Zaugg
# Description : Main interactive visualization page 
#--------------------

import streamlit as st
from streamlit import session_state as ss
from utils import draw_figures, update_ss

with st.sidebar:
    # user input for the two thresholds
    with st.form("thld_form", border=True):
        ss["upar"]["cutoff_obli"] = st.slider("Area plot cutoff", min_value = 0.0, max_value = 10.0, step = 0.1, 
            value = ss["upar"]["cutoff_obli"], key="cutoff_obli_slider",) 
        st.text("")
        submitted = st.form_submit_button("Apply", type = "primary")
        if submitted:
            ss["upar"]["cutoff_obli"] = ss["cutoff_obli_slider"]
            ss.fig_all_oblig = draw_figures(ss.df_all_obli, ss.df_age_obli, ss.df_sex_obli, ss.df_typ_obli, 
                             colseq = ss["colseq"], cutoff = ss["upar"]["cutoff_obli"])

st.plotly_chart(ss.fig_all_oblig,  use_container_width=True, theme=None, config={"displayModeBar": False}, key = "k001")

