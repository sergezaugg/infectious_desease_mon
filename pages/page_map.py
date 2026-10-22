#--------------------             
# Author : Serge Zaugg
# Description : incidence map where each canton has same size 
#--------------------

import streamlit as st
from streamlit import session_state as ss
from src.utils_hexaplot import make_hexagon_plot, get_mean_by_canton
from plotly.colors import sample_colorscale 
from src.utils_ui import make_line_plot_with_vref, make_simple_fig
import plotly.express as px
from streamlit_vertical_slider import vertical_slider

with st.sidebar:
    st.markdown("""
    :primary[Top panel:] 
    The top panel on the right shows the incidence across Switzerland over recent weeks, 
    with the latest available week selected by default. 
    Use the slider to explore historical data averaged over multiple weeks (pills).

    :primary[Pseudo-Maps:] 
    The hexagonal pseudo map displays incidence and case counts by canton.
    Maps show values from the specific time period selected above.

    """)


#-------------------------------------------------
# setup page layout 
c00,c01 = st.columns([4.0,1.5], border=False)
c0,c1,c2,c3 = st.columns([5,1,5,1], border=False)

cont00 = c00.container(border=True, height = 260)
cont01 = c01.container(border=True, height = 260)

with cont00:
    cx0,cx1 = st.columns([0.8,7.0], border=False)

cont10 = c0.container(border=True, height = 450)
cont11 = c1.container(border=True, height = 450)
cont12 = c2.container(border=True, height = 450)
cont13 = c3.container(border=True, height = 450)


#-------------------------------------------------
# get user input 
with cx0:
    st.caption("Averaging window (weeks)")
    st.caption("Target date")
    st.caption(" ")
    st.caption("Overview")

with cx1:
    n_weeks_selected = st.pills("Number" , label_visibility="collapsed",
        options = range(1, 20), 
        default = ss.opt_n_weeks, 
        width = "stretch", 
        key = "hexa_weeks_pills",)
    date_selected = st.select_slider("Select date", label_visibility="collapsed",
        options = ss.opt_dates, 
        value = ss.opt_datseel, 
        format_func=lambda d: d.strftime("%Y-%m-%d") ,
        key="hexa_date_slider",)

with cont11:
    ss.col_max_inc = vertical_slider("Color threshold", height=300,
        step = 0.1, min_value=1.0, max_value=20.0,
        default_value=ss.col_max_inc,key="k_col_max_inx",
        track_color = "#222222", slider_color = "#2198cf", thumb_color= "#2198cf", )
    
with cont13:
    ss.col_max_cou = vertical_slider("Color threshold", height=300,
        step = 10.0, min_value=10.0, max_value=500.0,
        default_value=ss.col_max_cou,key="k_col_max_cou",
        track_color = "#222222", slider_color = "#2198cf", thumb_color= "#2198cf", )


#-------------------------------------------------
# data prep
# keep only up to selected weeks 
df_temp = ss.df_can
df_opc = df_temp[df_temp['date']<=date_selected]
# select N  latest from above 
df_opc = df_opc.sort_values("date").groupby("georegion").tail(n_weeks_selected)
sel_data_min = df_opc["date"].min().date()
sel_data_max = df_opc["date"].max().date()
# data prep II 
df_incide = get_mean_by_canton(df_opc, 'incValue')
df_counts = get_mean_by_canton(df_opc, 'value')
# selected data mini-plot
df_b = ss.df_all.loc[ss.df_all["date"].between(df_opc["date"].min(), df_opc["date"].max())]

# make short info texts
infotext_period = f" Period: {sel_data_min:%Y-%m-%d} to {sel_data_max:%Y-%m-%d}"
infotext_incide = infotext_period + "" + f" ({n_weeks_selected} W)"


#-------------------------------------------------
# render figures 

# render time-zoom fig
figm = make_simple_fig(df=df_b, height = 200)

# render line-plot feedback to user 
fig_lin_a = make_line_plot_with_vref(ss.df_all, height = 100, y_title = '')
fig_lin_b = fig_lin_a.add_vrect(x0=sel_data_min, x1=sel_data_max, fillcolor="pink", opacity=0.66, 
    line_width=2.5, line_color="white", layer="below")

# prepare main hexagon plots 
color_map_01 = sample_colorscale("rainbow", 10, low=0.45, high=0.85)
color_map_02 = "bluered"
fig_incide = make_hexagon_plot(df_one_per_canton = df_incide, resp_var = 'incValue', 
    color_map = color_map_01, color_max_val = ss.col_max_inc)
fig_counts = make_hexagon_plot(df_one_per_canton = df_counts, resp_var = 'value',   
    color_map = color_map_02, color_max_val = ss.col_max_cou)



#-------------------------------------------------
# display on screen

# time-zoom fig
with cont01:
    st.caption("Weekly Inc. all CH" + " -- " +infotext_incide, text_alignment  = "center")
    st.plotly_chart(figm, use_container_width=True)

# line-plot feedback to user 
with cx1:
    st.plotly_chart(fig_lin_b, use_container_width=True, theme=None)

# main hexagon plots 
with cont10:
    st.caption("Average Weekly Incidence by canton" + " -- " + infotext_incide, text_alignment  = "center")
    st.plotly_chart(fig_incide, use_container_width=False, theme=None, )
    st.caption("Incidence values are normalized by canton's population")

with cont12:
    st.caption("Average Weekly Count by canton" + " -- " + infotext_incide, text_alignment  = "center")
    st.plotly_chart(fig_counts, use_container_width=False, theme=None, )
    st.caption("Counts are NOT normalized by canton's population")







