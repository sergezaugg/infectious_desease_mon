#--------------------             
# Author : Serge Zaugg
# Description : incidence map where each canton has same size 
#--------------------

import streamlit as st
from streamlit import session_state as ss
import pandas as pd 
from utils_hexaplot import make_hexagon_plot
from plotly.colors import sample_colorscale # "bluered"
from utils_ui import make_line_plot_with_vref

@st.cache_data
def get_cumsum(x, resp_var):
    """ take cumsum """
    x = x[['date', 'georegion', resp_var]]
    x = x.groupby("georegion", as_index=False)[resp_var].sum()
    x = x.rename(columns={"value": resp_var})
    return(x)



# make_line_plot
fig_lin_a = make_line_plot_with_vref(ss.df_all, height = 100, y_title = 'Cases per 100000 inhab')

with st.sidebar:
     st.markdown("""
        Incidence values ('incValue') are normalized by canton's population while counts ('value') are not.
        """)


#-------------------------------------------------
# user actions
c0,c1,c2 = st.columns([0.8,7,1])
with c0:
    st.caption("Nb weeks to sum over backwards")
    st.caption("Select date to inspect")
with c1:

    n_weeks_selected = st.pills("Number", range(1, 16), default=3, width = "stretch", label_visibility="collapsed",)
    opt_dates = sorted(ss.df_can['date'].unique())
    date_selected = st.select_slider("Select date", options=opt_dates,value=opt_dates[-1],
        format_func=lambda d: d.strftime("%Y-%m-%d"),  label_visibility="collapsed",)
    


#-------------------------------------------------
# data prep

# keep only up to selected weeks 
df_temp = ss.df_can
df_opc = df_temp[df_temp['date']<=date_selected]
# select N  latest from above 
df_opc = df_opc.sort_values("date").groupby("georegion").tail(n_weeks_selected)
sel_data_min = df_opc["date"].min().date()
sel_data_max = df_opc["date"].max().date()

with c1:
    fig_lin_b = fig_lin_a.add_vrect(x0=sel_data_min, x1=sel_data_max, fillcolor="pink", opacity=0.50, line_width=2, layer="below")
    st.plotly_chart(fig_lin_b, use_container_width=True, theme=None)

with c0:
    st.caption(f"Selection: {sel_data_min:%Y-%m-%d} to {sel_data_max:%Y-%m-%d}")

df_incide = get_cumsum(df_opc, 'incValue')
df_counts = get_cumsum(df_opc, 'value')

color_map_01 = sample_colorscale("rainbow", 10, low=0.45, high=0.85)
color_map_02 = "bluered"

fig_incide = make_hexagon_plot(df_one_per_canton = df_incide, resp_var = 'incValue', color_map = color_map_01, color_max_val = 0.50)
fig_counts = make_hexagon_plot(df_one_per_canton = df_counts, resp_var = 'value',    color_map = color_map_02, color_max_val = 50.0)


c0,c1 = st.columns([4,4])

with c0:
    st.plotly_chart(fig_incide, use_container_width=False, theme=None, )
with c1:
    st.plotly_chart(fig_counts, use_container_width=False, theme=None, )








