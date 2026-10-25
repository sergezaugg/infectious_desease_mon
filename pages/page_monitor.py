#--------------------             
# Author : Serge Zaugg
# Description : incidence map where each canton has same size 
#--------------------

import streamlit as st
from streamlit import session_state as ss
from src.utils_hexaplot import make_hexagon_plot, get_mean_by_canton
from plotly.colors import sample_colorscale 
from src.utils_ui import make_simple_fig, make_subgroup_barplots
from src.utilsdataprep import get_mean_by_group, prepare_data_for_barplots
import plotly.express as px
from streamlit_vertical_slider import vertical_slider
import pandas as pd
import plotly.graph_objects as go

with st.sidebar:
    st.markdown("""
    :primary[The top-left panel] shows incidence across Switzerland for the most recent weeks. 
    Use the slider to average incidence over a few recent weeks.

    :primary[The top-right panel] shows incidence across Switzerland for the past year as a reference.

    :primary[The hexagonal pseudo-map] displays per-canton incidence for the selected recent weeks.
    Use the slider to adjust colors to current incidence levels.

    :primary[The bar charts] show incidence by age, sex, and influenza type (A or B) for the selected recent weeks.
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
cont11 = c1.container(border=True, height = 450)
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

with cont11:
    st.caption("Upper Color Threshold")
    ss.col_max_inc = vertical_slider(
        height=300,
        step = 0.1, min_value=1.0, max_value=20.0,
        default_value=ss.mon_col_thld_1,
        key="mon_col_thld_1",
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

# legacy
# sel_data_min = df_opc["date"].min().date()
# sel_data_max = df_opc["date"].max().date()
# infotext_period = f"{sel_data_min:%Y-%m-%d} to {sel_data_max:%Y-%m-%d}"

# make short info texts
infotext_period = f"{recency_limit_date:%Y-%m-%d} to {ss.ref_date:%Y-%m-%d}" # use absolute time from ref
# st.write(infotext_period)
infotext_incide = infotext_period # + "" + f" ({n_weeks_realized} weeks)"
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
df_typ, df_sex, df_age =  prepare_data_for_barplots(ss.df_typ, ss.df_sex, ss.df_age, recency_limit_date)


#-------------------------------------------------
# render figures 

# full past year 
fig_lin_a = make_simple_fig(df_reduced, height = 200, colo=ss.colo_all_oblig)
fig_lin_b = fig_lin_a.add_vrect(x0=recency_limit_date, x1=ss.ref_date, fillcolor="pink", opacity=0.30, line_width=2.5, 
    line_color="white", layer="below")
fig_lin_b.add_vline(x=ss.ref_date, line_color="green", line_dash="dot", line_width=2,
    annotation_text="Reference date", annotation_position="top", annotation_font_color="green")

# prepare time-zoom plot
figm = make_simple_fig(df_time_zoom, height = 200, colo=ss.colo_all_oblig)
figm.add_vline(x=ss.ref_date, line_color="green", line_dash="dot", line_width=2,
            annotation_text="Reference date", annotation_position="top", annotation_font_color="green")

# prepare main hexagon plots 
color_map_01 = sample_colorscale("rainbow", 10, low=0.45, high=0.85)
color_map_02 = "bluered"
if n_weeks_realized > 0:
    fig_incide = make_hexagon_plot(df_one_per_canton = df_incide, resp_var = 'incValue', resp_label = "Average Incidence",
        color_map = color_map_01, color_max_val = ss.col_max_inc)
    # fig_counts = make_hexagon_plot(df_one_per_canton = df_counts, resp_var = 'value', resp_label = "Average Case Count",   
    #     color_map = color_map_02, color_max_val = ss.col_max_cou)
else:
    fig_incide = go.Figure() 
    # fig_counts = go.Figure()

# prepare per-group barplots 
fig_bar_typ = make_subgroup_barplots(df_typ, 'type', 'incValue', ["#34BDEA"],  0.70, 170, "Average Incidence")
fig_bar_sex = make_subgroup_barplots(df_sex, 'sex', 'incValue', ["#D996E1"],  0.70, 170, "Average Incidence")
fig_bar_age = make_subgroup_barplots(df_age, 'agegroup', 'incValue', ["#E75C31"], 0.70, 360, "Average Incidence")


#-------------------------------------------------
# display on screen 

# display full past year 
with cont01:
    st.caption("Weekly Inc. all CH" + " -- " + "one year back", text_alignment  = "left")
    st.plotly_chart(fig_lin_b, use_container_width=True, theme=None)

# display time-zoom 
with cont02:
    st.caption("Weekly Inc. all CH" + " -- " +infotext_incide, text_alignment  = "left")
    st.plotly_chart(figm, use_container_width=True, theme=None)

# display main hexagon plots 
with cont10:
    st.caption("Average Weekly Incidence by canton" + " -- " + infotext_incide, text_alignment  = "left")
    st.plotly_chart(fig_incide, use_container_width=False, theme=None, )
    
with cont12:
    st.caption("Average Weekly Incidence by subgroups" + " -- " + infotext_incide, text_alignment  = "left")
    x1,x2 = st.columns(2)
    x1.plotly_chart(fig_bar_typ, use_container_width=False, theme=None, )
    x1.plotly_chart(fig_bar_sex, use_container_width=False, theme=None, )
    x2.plotly_chart(fig_bar_age, use_container_width=False, theme=None, )




   



