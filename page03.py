#--------------------             
# Author : Serge Zaugg
# Description : tbd
#--------------------

import pandas as pd 
import plotly.express as px
import streamlit as st
from datetime import datetime
from streamlit import session_state as ss
from utils import get_all_oblig, get_by_cantons_oblig, get_by_agegroup_oblig, get_by_sex_oblig, make_line_plot
from utils import get_all_sentinella, get_by_region_sentinella, get_by_agegroup_sentinella, get_by_sex_sentinella
from utils import update_ss, preprocess_INFLUENZA, make_line_plot, update_zoom_line_plot

if ss["data"]["data_di"] == "initial":
    st.info("Data not yet loaded!  --->   Please navigate to 'Load data' menu (left) and then click on 'Load data' button.")
else:    
    df_obli = ss["data"]["data_di"]["INFLUENZA_oblig"]
    df_sent = ss["data"]["data_di"]["INFLUENZA_sentinella"]

    df_obli = preprocess_INFLUENZA(df_obli)
    df_sent = preprocess_INFLUENZA(df_sent)

    df_all = get_all_oblig(df_obli)
    df_can = get_by_cantons_oblig(df_obli)
    df_age = get_by_agegroup_oblig(df_obli)
    df_sex = get_by_sex_oblig(df_obli)
    df_all_sent = get_all_sentinella(df_sent)
    df_can_sent = get_by_region_sentinella(df_sent)
    df_age_sent = get_by_agegroup_sentinella(df_sent)
    df_sex_sent = get_by_sex_sentinella(df_sent)

    if ss["upar"]["date_range"] == 'initial':
            # concat dates from both dfs to get global min and max 
            df_dates = pd.concat([df_obli['date'], df_sent['date']])
            # st.write(df_dates.shape, df_obli['date'].shape, df_sent['date'].shape,)
            time_options = options=df_dates.sort_values()
            t_sta = time_options.min()
            t_sta = datetime(year = t_sta.year, month = t_sta.month, day = t_sta.day)
            t_end = time_options.max()
            t_end = datetime(year = t_end.year, month = t_end.month, day = t_end.day)
            ss["upar"]["date_range"] = (t_sta, t_end)
            ss["upar"]["full_date_range"] = (t_sta, t_end)
      

    ss["figures"]["fig_all_oblig"] = make_line_plot(df_all, 'georegion', ss["colseq"]["fig_all_oblig"], y_title = 'Cases per 100000 inhab *', )
    ss["figures"]["fig_can_oblig"] = make_line_plot(df_can, 'georegion', ss["colseq"]["fig_can_oblig"], y_title = 'Cases per 100000 inhab *', )
    ss["figures"]["fig_age_oblig"] = make_line_plot(df_age, 'agegroup',  ss["colseq"]["fig_age_oblig"], y_title = 'Cases per 100000 inhab *',)
    ss["figures"]["fig_sex_oblig"] = make_line_plot(df_sex, 'sex',       ss["colseq"]["fig_sex_oblig"], y_title = 'Cases per 100000 inhab *', )
    ss["figures"]["fig_all_sent"]  = make_line_plot(df_all_sent, 'georegion', ss["colseq"]["fig_all_oblig"], y_title = 'Consultations per 100000 inhab *', )
    ss["figures"]["fig_can_sent"]  = make_line_plot(df_can_sent, 'georegion', ss["colseq"]["fig_reg_oblig"], y_title = 'Consultations per 100000 inhab *', )
    ss["figures"]["fig_age_sent"]  = make_line_plot(df_age_sent, 'agegroup',  ss["colseq"]["fig_age_oblig"], y_title = 'Consultations per 100000 inhab *', )
    ss["figures"]["fig_sex_sent"]  = make_line_plot(df_sex_sent, 'sex',       ss["colseq"]["fig_sex_oblig"], y_title = 'Consultations per 100000 inhab *', )

    ss["figures"]["fig_all_oblig"] = update_zoom_line_plot(fig = ss["figures"]["fig_all_oblig"], date_range = ss["upar"]["date_range"])
    ss["figures"]["fig_can_oblig"] = update_zoom_line_plot(fig = ss["figures"]["fig_can_oblig"], date_range = ss["upar"]["date_range"])                
    ss["figures"]["fig_age_oblig"] = update_zoom_line_plot(fig = ss["figures"]["fig_age_oblig"], date_range = ss["upar"]["date_range"])                
    ss["figures"]["fig_sex_oblig"] = update_zoom_line_plot(fig = ss["figures"]["fig_sex_oblig"], date_range = ss["upar"]["date_range"])                
    ss["figures"]["fig_all_sent"]  = update_zoom_line_plot(fig = ss["figures"]["fig_all_sent"], date_range = ss["upar"]["date_range"])                
    ss["figures"]["fig_can_sent"]  = update_zoom_line_plot(fig = ss["figures"]["fig_can_sent"], date_range = ss["upar"]["date_range"])                
    ss["figures"]["fig_age_sent"]  = update_zoom_line_plot(fig = ss["figures"]["fig_age_sent"], date_range = ss["upar"]["date_range"])                
    ss["figures"]["fig_sex_sent"]  = update_zoom_line_plot(fig = ss["figures"]["fig_sex_sent"], date_range = ss["upar"]["date_range"])                



    ca1, ca2 = st.columns([0.4, 0.4])
    with ca1:
        # update time axes
        with st.container(height=125, border=True):
            with st.form("form01", border=False, clear_on_submit=False, enter_to_submit=False): 
                c1, c2 = st.columns([0.4, 0.1])
                with c1:
                    sel_sta, sel_end = st.slider("Time range to plot", min_value = ss["upar"]["full_date_range"][0], max_value = ss["upar"]["full_date_range"][1]  , 
                                                 value = ss["upar"]["date_range"], format = "YYYY-MM-DD", label_visibility = "visible")    
                with c2:
                    st.text(" ")
                    submitted01 = st.form_submit_button("Apply", type="primary", use_container_width = False) 
                if submitted01:
                    ss["upar"]["date_range"] = (sel_sta, sel_end)
                    st.rerun()
                 
    with ca2:
        with st.container(height=125, border=True):
            with st.form("form02", border=False, clear_on_submit=False, enter_to_submit=False): 
                ca1, ca2, ca3 = st.columns([0.3, 0.4, 0.4])
                with ca1:
                    sel_dat_sou = st.segmented_control("Data source", options = ['oblig', 'sentinella'], selection_mode="multi", default = ['oblig', 'sentinella']) 
                with ca2:
                    sel_dat_grou = st.segmented_control("Data grouping", options = ['All', 'Sex', 'Age', 'Region'], selection_mode="multi", default = ['All'])
                with ca3:
                    st.text(" ")
                    # st.text(" ")
                    submitted02 = st.form_submit_button("Apply", type="primary", use_container_width = False) 
                if submitted02: 
                    ss["upar"]["selecte_data_sources"] = sel_dat_sou
                    ss["upar"]["selecte_data_groupings"] = sel_dat_grou

            cb1, cb2, cb3 = st.columns([0.4, 0.15, 0.5])
            cb1.text("Links to data source details:")
            cb2.page_link("https://www.idd.bag.admin.ch/survey-systems/oblig",      label=":blue[oblig]")  
            cb3.page_link("https://www.idd.bag.admin.ch/survey-systems/sentinella", label=":blue[sentinella]")   
 
                


    st.text("* Incidence is the rate of new events over a specified period. Here, the number of new cases/consultations per week and per 100000 inhabitants.")

    if 'oblig' in ss["upar"]["selecte_data_sources"]:
        with st.container(height=None, border=True):
            if 'All' in ss["upar"]["selecte_data_groupings"]:
                st.plotly_chart(ss["figures"]["fig_all_oblig"], key = "fig_all_oblig",  use_container_width=True, theme=None)
            if 'Sex' in ss["upar"]["selecte_data_groupings"]:
                st.plotly_chart(ss["figures"]["fig_sex_oblig"], key = "fig_sex_oblig",  use_container_width=True, theme=None)
            if 'Age' in ss["upar"]["selecte_data_groupings"]:
                st.plotly_chart(ss["figures"]["fig_age_oblig"], key = "fig_age_oblig",  use_container_width=True, theme=None)
            if 'Region' in ss["upar"]["selecte_data_groupings"]:
                st.plotly_chart(ss["figures"]["fig_can_oblig"], key = "fig_can_oblig",  use_container_width=True, theme=None)
    if 'sentinella' in ss["upar"]["selecte_data_sources"]:
        with st.container(height=None, border=True):
            if 'All' in ss["upar"]["selecte_data_groupings"]:
                st.plotly_chart(ss["figures"]["fig_all_sent"], key = "fig_all_sent",  use_container_width=True, theme=None)
            if 'Sex' in ss["upar"]["selecte_data_groupings"]:
                st.plotly_chart(ss["figures"]["fig_sex_sent"], key = "fig_sex_sent",  use_container_width=True, theme=None)
            if 'Age' in ss["upar"]["selecte_data_groupings"]:
                st.plotly_chart(ss["figures"]["fig_age_sent"], key = "fig_age_sent",  use_container_width=True, theme=None)
            if 'Region' in ss["upar"]["selecte_data_groupings"]:
                st.plotly_chart(ss["figures"]["fig_can_sent"], key = "fig_can_sent",  use_container_width=True, theme=None)


















