#--------------------             
# Author : Serge Zaugg
# Description : incidence map where each canton has same size 
#--------------------

import streamlit as st
from streamlit import session_state as ss
from src.utils_hexaplot import make_hexagon_plot, get_mean_by_canton
from plotly.colors import sample_colorscale 
from src.utils_ui import make_line_plot_with_vref
import plotly.express as px
from streamlit_vertical_slider import vertical_slider
import pandas as pd



@st.cache_data
def make_simple_fig(df, height):
    fig = px.line(df, 
        x = 'date', y = 'incValue', 
        height = height,  markers=True, 
        color_discrete_sequence = ["#F25B10"]
        )
    _ = fig.update_xaxes(showline=True, linewidth=1, linecolor='white', mirror=True)
    _ = fig.update_yaxes(showline=True, linewidth=1, linecolor='white', mirror=True)
    _ = fig.update_layout(paper_bgcolor="#000000") # "#350030"
    _ = fig.update_xaxes(showgrid=False)
    _ = fig.update_yaxes(showgrid=False)
    _ = fig.update_layout(margin=dict(l=30, r=30, t=10, b=30))
    return(fig)



with st.sidebar:
    st.markdown("""
    :primary[Top panel:] 
    bla.

    :primary[Pseudo-Maps:] 
    bla.

    """)



# setup page layout 
c00,c01,c02 = st.columns([1,7,4], border=False)
c0,c1,c2,c3 = st.columns([5,1,5,1], border=False)

cont00 = c00.container(border=True, height = 260)
cont01 = c01.container(border=True, height = 260)
cont02 = c02.container(border=True, height = 260)

cont10 = c0.container(border=True, height = 500)
cont11 = c1.container(border=True, height = 500)
cont12 = c2.container(border=True, height = 500)
cont13 = c3.container(border=True, height = 500)

#-------------------------------------------------
# get user input 
with cont00:
    n_weeks_selected = vertical_slider("Nb weeks to average back", height=140,
        step = 1, min_value=1, max_value=24,
        default_value=5, key="fffgggttrrr",
        track_color = "#222222", slider_color = "#2198cf", thumb_color= "#2198cf", )

#-------------------------------------------------
# data prep
df_opc = ss.df_can
# select N  latest from above 
df_opc = df_opc.sort_values("date").groupby("georegion").tail(n_weeks_selected)
sel_data_min = df_opc["date"].min().date()
sel_data_max = df_opc["date"].max().date()
infotext_period = f"Selected period: {sel_data_min:%Y-%m-%d} to {sel_data_max:%Y-%m-%d}"
# data prep II 
df_incide = get_mean_by_canton(df_opc, 'incValue')
df_counts = get_mean_by_canton(df_opc, 'value')
# selected data mini-plot
df_b = ss.df_all.loc[ss.df_all["date"].between(df_opc["date"].min(), df_opc["date"].max())] 

#-------------------------------------------------
# show full past year 

# st.write((ss.ref_date))
n_weeks = 52
new_ts = ss.ref_date - pd.Timedelta(weeks=n_weeks)
# st.write(new_ts)
df_reduced = ss.df_all[ss.df_all["date"] >= new_ts]

with cont01:
    # fig_lin_a = make_line_plot_with_vref(df_reduced, height = 200, y_title = '')
    st.caption("aaaa", text_alignment  = "center")
    fig_lin_a = make_simple_fig(df_reduced, height = 200)
    fig_lin_b = fig_lin_a.add_vrect(x0=sel_data_min, x1=sel_data_max, fillcolor="pink", opacity=0.66, line_width=2.5, line_color="white", layer="below")
    st.plotly_chart(fig_lin_b, use_container_width=True, theme=None)




#-------------------------------------------------
# show time-zoom 
with cont02:
    st.caption(infotext_period, text_alignment  = "center")
    figm = make_simple_fig(df_b, height = 200)
    st.plotly_chart(figm, use_container_width=True, theme=None)








#######################################
# second row
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
# prepare main hexagon plots 
color_map_01 = sample_colorscale("rainbow", 10, low=0.45, high=0.85)
color_map_02 = "bluered"
fig_incide = make_hexagon_plot(df_one_per_canton = df_incide, resp_var = 'incValue', color_map = color_map_01, color_max_val = ss.col_max_inc)
fig_counts = make_hexagon_plot(df_one_per_canton = df_counts, resp_var = 'value',    color_map = color_map_02, color_max_val = ss.col_max_cou)

#-------------------------------------------------
# display main hexagon plots 
with cont10:
    st.plotly_chart(fig_incide, use_container_width=False, theme=None, )
    ca, cb = st.columns([2,2])
    ca.caption(infotext_period)
    infotext_incide = f"Incidence averaged over {n_weeks_selected} week"
    ca.caption(infotext_incide)
    cb.caption("Incidence values ('incValue') are normalized by canton's population")
with cont12:
    st.plotly_chart(fig_counts, use_container_width=False, theme=None, )
    ca, cb = st.columns([2,2])
    ca.caption(infotext_period)
    infotext_counts = f"case counts averaged over {n_weeks_selected} week"
    ca.caption(infotext_counts)
    cb.caption("Counts ('value') are not normalized by canton's population")







