#--------------------             
# Author : Serge Zaugg
# Description : incidence map where each canton has same size 
#--------------------

import streamlit as st
from streamlit import session_state as ss
from streamlit_vertical_slider import vertical_slider

from src.utils_hexaplot import make_hexagon_plot
from src.utils_ui import make_simple_fig, make_subgroup_barplots
from src.utilsdataprep import get_mean_by_canton, prepare_data_for_barplots

import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go

with st.sidebar:
    st.markdown("""
    :primary[Top panels:] Weekly incidence across Switzerland. 
    Use slider to select nb of recent weeks for averaging (shown on bottom panels). 
    
    :primary[Bottom panels:] Average weekly incidence or Case Count by canton, age, sex, and influenza type for the selected recent weeks.
    Use slider to adjust colors.
    """)


#-------------------------------------------------
# setup page layout 
# c00,c01,c02 = st.columns([1,7,4], border=False)
c00,c02,c01 = st.columns([1,4,7], border=False)
c1, c0,c2   = st.columns([1,5,6], border=False)

cont00 = c00.container(border=True, height = 260)
cont01 = c01.container(border=True, height = 260)
cont02 = c02.container(border=True, height = 260)

cont10 = c0.container(border=True, height = 450)
with c1:
    cont11a = st.container(border=True, height = 130)
    cont11b = st.container(border=True, height = 300)
cont12 = c2.container(border=True, height = 450)




#-------------------------------------------------
# get user input 
with cont00:
    st.caption("Weeks to look back")
    n_weeks_selected = vertical_slider(
        height=100,
        step = 1, min_value=1, max_value=20,
        default_value=ss.mon_slider_window, 
        key="mon_slider_window",
        track_color = "#222222", slider_color = "#2198cf", thumb_color= "#2198cf", )

with cont11a:
    ss.mon_outcome= st.radio(
        "Outcome",
        options = ["Incid","Count"],
        key="mon_radio_1", 
        # label_visibility="hidden",
        horizontal=True)

with cont11b:
    st.caption("Upper Color Threshold")
    if ss.mon_outcome == "Incid":
        ss.col_max_inc = vertical_slider(
            height=140,
            step = 0.1, min_value=1.0, max_value=20.0,
            default_value=ss.mon_col_thld_1,
            key="mon_col_thld_1",
            track_color = "#222222", slider_color = "#2198cf", thumb_color= "#2198cf", )
    if ss.mon_outcome == "Count":
        ss.col_max_cou = vertical_slider(
            height=140,
            step = 10.0, min_value=10.0, max_value=500.0,
            default_value=ss.k_col_max_cou,
            key="k_col_max_cou",
            track_color = "#222222", slider_color = "#2198cf", thumb_color= "#2198cf", )


#-------------------------------------------------
# data prep I
# compute recency limit from ref date and user selection
recency_limit_date = ss.ref_date - pd.Timedelta(weeks=n_weeks_selected)
# get per canton data
df_opc = ss.df_can
# select latest 
df_opc = df_opc[df_opc['date'] >= recency_limit_date]

# get nb actual weeks >= recency_limit_date
n_weeks_realized = len(df_opc['date'].unique())

# make short info texts
infotext_incide = f"{recency_limit_date:%Y-%m-%d} to {ss.ref_date:%Y-%m-%d}" # use absolute time from ref
# prep per-canton data for hexa plots 
df_incide = get_mean_by_canton(df_opc, 'incValue')
df_counts = get_mean_by_canton(df_opc, 'value')
# data for time-zoom plot
df_time_zoom = ss.df_all.loc[ss.df_all["date"].between(df_opc["date"].min(), df_opc["date"].max())] 
#-------------------------------------------------
# data prep II - selected data for 1-Y plot 
n_weeks = 52
new_ts = ss.ref_date - pd.Timedelta(weeks=n_weeks)
df_reduced = ss.df_all[ss.df_all["date"] >= new_ts]
#-------------------------------------------------
# data prep III - subgroups
df_typ_inc, df_sex_inc, df_age_inc =  prepare_data_for_barplots(ss.df_typ, ss.df_sex, ss.df_age, recency_limit_date, 'incValue')
df_typ_cou, df_sex_cou, df_age_cou =  prepare_data_for_barplots(ss.df_typ, ss.df_sex, ss.df_age, recency_limit_date, 'value')


#-------------------------------------------------
# render figures 

# full past year 
fig_lin_a = make_simple_fig(df_reduced, height = 190, colo=ss.colo_all_oblig)
fig_lin_b = fig_lin_a.add_vrect(x0=recency_limit_date, x1=ss.ref_date, fillcolor="pink", opacity=0.30, line_width=2.5, 
    line_color="white", layer="below")
fig_lin_b.add_vline(x=ss.ref_date, line_color="green", line_dash="dot", line_width=2,
    annotation_text="Reference date", annotation_position="top", annotation_font_color="green")

# prepare time-zoom plot
figm = make_simple_fig(df_time_zoom, height = 190, colo=ss.colo_all_oblig)
figm.add_vline(x=ss.ref_date, line_color="green", line_dash="dot", line_width=2,
            annotation_text="Reference date", annotation_position="top", annotation_font_color="green")

# prepare main hexagon plots 
if n_weeks_realized > 0:
    if ss.mon_outcome == "Incid":
        fig_map = make_hexagon_plot(df_one_per_canton = df_incide, resp_var = 'incValue', resp_label = "Average Incidence",
            color_map = ss.color_map_01, color_max_val = ss.col_max_inc)
        fig_bar_typ = make_subgroup_barplots(df_typ_inc, 'type', 'incValue', ["#34BDEA"],  0.70, 170, "Average Incidence")
        fig_bar_sex = make_subgroup_barplots(df_sex_inc, 'sex', 'incValue', ["#D996E1"],  0.70, 170, "Average Incidence")
        fig_bar_age = make_subgroup_barplots(df_age_inc, 'agegroup', 'incValue', ["#E75C31"], 0.70, 360, "Average Incidence")

    if ss.mon_outcome == "Count":
        fig_map = make_hexagon_plot(df_one_per_canton = df_counts, resp_var = 'value', resp_label = "Average Case Count",   
            color_map = ss.color_map_02, color_max_val = ss.col_max_cou)
        fig_bar_typ = make_subgroup_barplots(df_typ_cou, 'type', 'value', ["#34BDEA"],  0.70, 170, "Average Case Count")
        fig_bar_sex = make_subgroup_barplots(df_sex_cou, 'sex', 'value', ["#D996E1"],  0.70, 170, "Average Case Count")
        fig_bar_age = make_subgroup_barplots(df_age_cou, 'agegroup', 'value', ["#E75C31"], 0.70, 360, "Average Case Count")
else:
    # fig_map = go.Figure() 
    # fig_bar_typ = go.Figure() 
    # fig_bar_sex = go.Figure() 
    # fig_bar_age = go.Figure() 
    fig_map = None
    fig_bar_typ = dict()
    fig_bar_sex = dict()
    fig_bar_age = dict()


#-------------------------------------------------
# display on screen 

# display full past year 
with cont01:
    st.caption("Weekly Inc. all CH" + " -- " + "one year back", text_alignment  = "left")
    st.plotly_chart(fig_lin_b, use_container_width=True, theme=None)

if fig_map is  None:
    with cont02:
            st.caption("Time window too recent, please select more backwards weeks with slider.", text_alignment  = "left")
else:    
    # display time-zoom 
    with cont02:
        st.caption("Weekly Inc. all CH" + " -- " +infotext_incide, text_alignment  = "left")
        st.plotly_chart(figm, use_container_width=True, theme=None)
    # display main hexagon plots 
    with cont10:
        st.caption("Weekly Average by canton" + " -- " + infotext_incide, text_alignment  = "left")
        st.plotly_chart(fig_map, use_container_width=False, theme=None, )
    # display bar-plots    
    with cont12:
        st.caption("Weekly Average by subgroups" + " -- " + infotext_incide, text_alignment  = "left")
        x1,x2 = st.columns(2)
        x1.plotly_chart(fig_bar_typ, use_container_width=False, theme=None, key = "adfbweqodfb")
        x1.plotly_chart(fig_bar_sex, use_container_width=False, theme=None, key = "adffgbvbdfb")
        x2.plotly_chart(fig_bar_age, use_container_width=False, theme=None, key = "addfbnfbdfb")





   



