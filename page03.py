#--------------------             
# Author : Serge Zaugg
# Description : tbd
#--------------------

import pandas as pd 
import plotly.express as px
import streamlit as st
from datetime import datetime
from streamlit import session_state as ss
from utils import get_all, get_by_cantons, get_by_agegroup, get_by_sex, make_line_plot, preprocess_INFLUENZA_oblig


if ss["data"]["data_di"] == "initial":
    st.info("Data not yet loaded!  --->   Please navigate to 'Load data' menu (left) and then click on 'Load data' button.")
else:    
    df = ss["data"]["data_di"]["INFLUENZA_oblig"]

    df = preprocess_INFLUENZA_oblig(df)

    df_all = get_all(df)
    df_can = get_by_cantons(df)
    df_age = get_by_agegroup(df)
    df_sex = get_by_sex(df)

    ss["figures"]["fig_all"] = make_line_plot(df_all, 'georegion', ss["colseq"]["fig_all"])
    ss["figures"]["fig_can"] = make_line_plot(df_can, 'georegion', ss["colseq"]["fig_can"])
    ss["figures"]["fig_age"] = make_line_plot(df_age, 'agegroup',  ss["colseq"]["fig_age"])
    ss["figures"]["fig_sex"] = make_line_plot(df_sex, 'sex',       ss["colseq"]["fig_sex"])

    # update time axes 
    with st.form("form01", border=True, clear_on_submit=False, enter_to_submit=False): 
        c1, c2, c3 = st.columns([0.4, 0.1, 0.4])
        time_options = options=df['date'].sort_values()
        t_sta = time_options.min()
        t_sta = datetime(year = t_sta.year, month = t_sta.month, day = t_sta.day)
        t_end = time_options.max()
        t_end = datetime(year = t_end.year, month = t_end.month, day = t_end.day)
        with c1:
             sel_sta, sel_end = st.slider("Time range to plot", value=( t_sta, t_end), format="YYYY-MM-DD", label_visibility = "visible")
        with c2:
            st.text(" ")
            submitted02 = st.form_submit_button("Apply", type="primary", use_container_width = False) 
        if submitted02:
            _ = ss["figures"]["fig_all"].update_xaxes(type="date", range=[sel_sta, sel_end])
            _ = ss["figures"]["fig_can"].update_xaxes(type="date", range=[sel_sta, sel_end])
            _ = ss["figures"]["fig_age"].update_xaxes(type="date", range=[sel_sta, sel_end])
            _ = ss["figures"]["fig_sex"].update_xaxes(type="date", range=[sel_sta, sel_end])


    with st.container(height=None, border=True):

        # with st.expander("All", expanded=True):
        st.plotly_chart(ss["figures"]["fig_all"], key = "fig_all")

        # with st.expander("Grouped : Sex", expanded=True):
        st.plotly_chart(ss["figures"]["fig_sex"], key = "fig_sex")

        # with st.expander("Grouped : Age", expanded=True):
        st.plotly_chart(ss["figures"]["fig_age"], key = "fig_age")

        # with st.expander("Grouped : Canton", expanded=True):
        st.plotly_chart(ss["figures"]["fig_can"], key = "fig_can")
















