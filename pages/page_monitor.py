#--------------------             
# Author : Serge Zaugg
# Description : incidence map where each canton has same size 
#--------------------

import streamlit as st
from streamlit import session_state as ss
from src.utils_hexaplot import make_hexagon_plot, get_mean_by_canton
from plotly.colors import sample_colorscale 
from src.utils_ui import make_simple_fig, make_subgroup_barplots
from src.utilsdataprep import get_mean_by_group
import plotly.express as px
from streamlit_vertical_slider import vertical_slider
import pandas as pd


with st.sidebar:
    st.markdown("""
    :primary[Top panel:] 
    <coming...>.

    :primary[Pseudo-Maps:] 
    <coming...>.

    :primary[Bar-plots:] 
    <coming...>.

    """)


#-------------------------------------------------
# setup page layout 
c00,c01,c02 = st.columns([1,7,4], border=False)
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
    st.caption("Avg wind. (weeks)")
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
# data prep
df_opc = ss.df_can

# select N  latest from above 
df_opc = df_opc.sort_values("date").groupby("georegion").tail(n_weeks_selected)
sel_data_min = df_opc["date"].min().date()
sel_data_max = df_opc["date"].max().date()

# make short info texts
infotext_period = f"{sel_data_min:%Y-%m-%d} to {sel_data_max:%Y-%m-%d}"
infotext_incide = infotext_period + "" + f" ({n_weeks_selected} weeks)"


# data prep II 
df_incide = get_mean_by_canton(df_opc, 'incValue')
df_counts = get_mean_by_canton(df_opc, 'value')
# selected data mini-plot
df_b = ss.df_all.loc[ss.df_all["date"].between(df_opc["date"].min(), df_opc["date"].max())] 

# select full past year 
n_weeks = 52
new_ts = ss.ref_date - pd.Timedelta(weeks=n_weeks)
df_reduced = ss.df_all[ss.df_all["date"] >= new_ts]




#-------------------------------------------------
# data prep subgroups

# keep only needed variables 
df_typ = ss.df_typ[['date','type','incValue','incValue_all', 'pop']]
df_sex = ss.df_sex[['date','sex','incValue','incValue_all', 'pop']]
df_age = ss.df_age[['date','agegroup','incValue','incValue_all', 'pop']]
# take n latest weeks only , by type 
df_typ_recent = df_typ.sort_values("date").groupby("type").tail(n_weeks_selected)
df_sex_recent = df_sex.sort_values("date").groupby("sex").tail(n_weeks_selected)
df_age_recent = df_age.sort_values("date").groupby("agegroup").tail(n_weeks_selected)
# get mean weekly-incidence
df_typ_recent_mean = get_mean_by_group(df_typ_recent, 'incValue', 'type')
df_sex_recent_mean = get_mean_by_group(df_sex_recent, 'incValue', 'sex')
df_age_recent_mean = get_mean_by_group(df_age_recent, 'incValue', 'agegroup')
# since pop constant per group we mis-use mean to get pop
df_typ_recent_pop = get_mean_by_group(df_typ_recent, 'pop', 'type')
df_sex_recent_pop = get_mean_by_group(df_sex_recent, 'pop', 'sex')
df_age_recent_pop = get_mean_by_group(df_age_recent, 'pop', 'agegroup')
# merge-in pop 
df_typ_recent_mean = df_typ_recent_mean.merge(df_typ_recent_pop, how = 'left', on = 'type')
df_sex_recent_mean = df_sex_recent_mean.merge(df_sex_recent_pop, how = 'left', on = 'sex')
df_age_recent_mean = df_age_recent_mean.merge(df_age_recent_pop, how = 'left', on = 'agegroup')
# convert pop from int to string (in millions)
df_typ_recent_mean["pop_str"] = (df_typ_recent_mean["pop"] / 1e6).map(lambda x: f"{x:.1f}M")
df_sex_recent_mean["pop_str"] = (df_sex_recent_mean["pop"] / 1e6).map(lambda x: f"{x:.1f}M")
df_age_recent_mean["pop_str"] = (df_age_recent_mean["pop"] / 1e6).map(lambda x: f"{x:.1f}M")

# make barplots 

glab_typ = {"gr_A": "A Type  ","gr_B": "B Type  ","gr_unknown": "Unk",}
glab_sex = {"gr_female": "Fema  ","gr_male": "Male  ","gr_unknown": "Unk ",}
glab_age = {"gr_00-04": "00-04  ",
            "gr_05-14": "05-14  ",
            "gr_15-29": "15-29  ",
            "gr_30-64": "30-64  ",
            "gr_65+":   "+65    ",
            "gr_Unknown": "Unk",}
# st.write(df_age_recent_mean['agegroup'].unique())
fig_bar_typ = make_subgroup_barplots(df_typ_recent_mean, 'type', 'incValue', ["#34BDEA"],  0.70, 170, "Incidence", glab_typ)
fig_bar_sex = make_subgroup_barplots(df_sex_recent_mean, 'sex', 'incValue', ["#D996E1"],  0.70, 170, "Incidence", glab_sex)
fig_bar_age = make_subgroup_barplots(df_age_recent_mean, 'agegroup', 'incValue', ["#E75C31"], 0.70, 360, "Incidence", glab_age)


# st.write(df_age_recent_mean)

#-------------------------------------------------
# render figures 

# full past year 
fig_lin_a = make_simple_fig(df_reduced, height = 200, colo=ss.colo_all_oblig)
fig_lin_b = fig_lin_a.add_vrect(x0=sel_data_min, x1=ss.ref_date, fillcolor="pink", opacity=0.30, line_width=2.5, 
    line_color="white", layer="below")
fig_lin_b.add_vline(x=ss.ref_date, line_color="green", line_dash="dot", line_width=2,
    annotation_text="Reference date", annotation_position="top", annotation_font_color="green")

# time-zoom 
figm = make_simple_fig(df_b, height = 200, colo=ss.colo_all_oblig)
figm.add_vline(x=ss.ref_date, line_color="green", line_dash="dot", line_width=2,
            annotation_text="Reference date", annotation_position="top", annotation_font_color="green")

# prepare main hexagon plots 
color_map_01 = sample_colorscale("rainbow", 10, low=0.45, high=0.85)
color_map_02 = "bluered"
fig_incide = make_hexagon_plot(df_one_per_canton = df_incide, resp_var = 'incValue', color_map = color_map_01, color_max_val = ss.col_max_inc)
fig_counts = make_hexagon_plot(df_one_per_canton = df_counts, resp_var = 'value',    color_map = color_map_02, color_max_val = ss.col_max_cou)


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




   



