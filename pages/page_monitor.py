#--------------------             
# Author : Serge Zaugg
# Description : incidence map where each canton has same size 
#--------------------

import streamlit as st
from streamlit import session_state as ss
from src.utils_hexaplot import make_hexagon_plot, get_mean_by_canton
from plotly.colors import sample_colorscale 
from src.utils_ui import make_simple_fig
import plotly.express as px
from streamlit_vertical_slider import vertical_slider
import pandas as pd


with st.sidebar:
    st.markdown("""
    :primary[Top panel:] 
    bla.

    :primary[Pseudo-Maps:] 
    bla.

    """)


#-------------------------------------------------
# setup page layout 
c00,c01,c02 = st.columns([0.8,7,4], border=False)
c1, c0,c2   = st.columns([0.8,5,6], border=False)

cont00 = c00.container(border=True, height = 260)
cont01 = c01.container(border=True, height = 260)
cont02 = c02.container(border=True, height = 260)

cont10 = c0.container(border=True, height = 450)
cont11 = c1.container(border=True, height = 450)
cont12 = c2.container(border=True, height = 450)


#-------------------------------------------------
# get user input 
with cont00:
    n_weeks_selected = vertical_slider("Averaging window (weeks)", height=120,
        step = 1, min_value=1, max_value=20,
        default_value=5, key="fffgggttrrr",
        track_color = "#222222", slider_color = "#2198cf", thumb_color= "#2198cf", )

with cont11:
    ss.col_max_inc = vertical_slider("Color threshold", height=300,
        step = 0.1, min_value=1.0, max_value=20.0,
        default_value=ss.col_max_inc,key="k_col_max_inx",
        track_color = "#222222", slider_color = "#2198cf", thumb_color= "#2198cf", )
    


#-------------------------------------------------
# data prep
df_opc = ss.df_can

# select N  latest from above 
df_opc = df_opc.sort_values("date").groupby("georegion").tail(n_weeks_selected)
sel_data_min = df_opc["date"].min().date()
sel_data_max = df_opc["date"].max().date()

# make short info texts
infotext_period = f" Period: {sel_data_min:%Y-%m-%d} to {sel_data_max:%Y-%m-%d}"
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





# subgroups 

@st.cache_data
def get_mean_by_group(x, resp_var, group_var):
    x = x[['date', group_var, resp_var]]
    x = x.groupby(group_var, as_index=False)[resp_var].mean()
    return(x)

@st.cache_data
def make_subgroup_barplots(df, group_var, resp_var, color_sequence, bar_width, height):
    df[group_var] = "gr_" + df[group_var].astype(str)
    fig = px.bar(df, y=group_var, x=resp_var, orientation = 'h',
        text="pop_str",
        category_orders={group_var: df[group_var].astype(str).unique().tolist()},
        color_discrete_sequence = color_sequence,
        color=group_var,
        height = height,
        )
    _ = fig.update_xaxes(showline=True, linewidth=1, linecolor='white', mirror=True)
    _ = fig.update_yaxes(showline=True, linewidth=1, linecolor='white', mirror=True)
    _ = fig.update_layout(paper_bgcolor="#000000") # "#350030"
    _ = fig.update_xaxes(showgrid=False)
    _ = fig.update_yaxes(showgrid=False)
    _ = fig.update_layout(margin=dict(l=30, r=20, t=10, b=30))
    _ = fig.update_yaxes(tickangle=270, title_text="")
    _ = fig.update_layout(showlegend=False)
    _ = fig.update_traces(width=bar_width)
    return fig

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
fig_bar_typ = make_subgroup_barplots(df_typ_recent_mean, 'type', 'incValue', ss.colo_typ_oblig,  0.80, 200)
fig_bar_sex = make_subgroup_barplots(df_sex_recent_mean, 'sex', 'incValue', ss.colo_sex_oblig,  0.80, 200)
fig_bar_age = make_subgroup_barplots(df_age_recent_mean, 'agegroup', 'incValue', ss.colo_age_oblig, 0.80, 400)




#-------------------------------------------------
# render figures 

# full past year 
fig_lin_a = make_simple_fig(df_reduced, height = 200)
fig_lin_b = fig_lin_a.add_vrect(x0=sel_data_min, x1=sel_data_max, fillcolor="pink", opacity=0.30, line_width=2.5, line_color="white", layer="below")
fig_lin_b.add_vline(x=ss.ref_date, line_color="green", line_dash="dot", line_width=2,
    annotation_text="Reference date", annotation_position="top", annotation_font_color="green")

# time-zoom 
figm = make_simple_fig(df_b, height = 200)
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
    st.caption("Weekly Incidence Values all CH" + " -- " + "Period = Last year", text_alignment  = "center")
    st.plotly_chart(fig_lin_b, use_container_width=True, theme=None)

# display time-zoom 
with cont02:
    st.caption("Weekly Incidence Values all CH" + " -- " +infotext_incide, text_alignment  = "center")
    st.plotly_chart(figm, use_container_width=True, theme=None)



# display main hexagon plots 
with cont10:
    st.caption("Average Weekly Incidence by canton" + " -- " + infotext_incide, text_alignment  = "center")
    st.plotly_chart(fig_incide, use_container_width=False, theme=None, )
    
with cont12:
    st.caption("Average Weekly Incidence by subgroups" + " -- " + infotext_incide, text_alignment  = "center")
    x1,x2,x3 = st.columns(3)
    x1.plotly_chart(fig_bar_typ, use_container_width=False, theme=None, )
    x2.plotly_chart(fig_bar_sex, use_container_width=False, theme=None, )
    x3.plotly_chart(fig_bar_age, use_container_width=False, theme=None, )




   



