#--------------------             
# Author : Serge Zaugg
# Description : Main interactive visualization page 
#--------------------

import streamlit as st
from streamlit import session_state as ss
from utils import draw_figures, update_ss

with st.sidebar:

    with st.container(border=True):

        # user input for the two thresholds
        with st.form("thld_form", border=True):
            col1, col2 = st.columns([4, 2])
            with col1:
                ss["upar"]["cutoff_obli"] = st.slider("Area plot cutoff", min_value = 0.0, max_value = 10.0, step = 0.1, 
                    value = ss["upar"]["cutoff_obli"], key="cutoff_obli_slider",) 
            with col2:
                st.text("")
                submitted = st.form_submit_button("Apply", type = "primary")
            if submitted:
                ss["upar"]["cutoff_obli"] = ss["cutoff_obli_slider"]
                draw_figures(data = ss["data"], colseq = ss["colseq"], cutoff = ss["upar"]["cutoff_obli"])

st.plotly_chart(ss["figures"]["fig_all_oblig"],  use_container_width=True, theme=None, config={"displayModeBar": False}, key = "k001")

