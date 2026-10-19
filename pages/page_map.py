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

    


c00,c01 = st.columns([4.0,1.5], border=False)

cont01 = c00.container(border=True, height = 260)
cont02 = c01.container(border=True, height = 260)


#-------------------------------------------------
# get user input 
with cont01:
    c0,c1 = st.columns([0.8,7.0], border=False)
    with c0:
        st.caption("Nb previous weeks to sum")
        st.caption("Target date")
        st.caption(" ")
        st.caption("Overview")
    with c1:
        n_weeks_selected = st.pills("Number" , label_visibility="collapsed",
            options = range(1, 16), 
            default = ss.opt_n_weeks, 
            width = "stretch", 
            key = "hexa_weeks_pills",)
        date_selected = st.select_slider("Select date", label_visibility="collapsed",
            options = ss.opt_dates, 
            value = ss.opt_datseel, 
            format_func=lambda d: d.strftime("%Y-%m-%d") ,
            key="hexa_date_slider",)


infotext_incide = f"Incidence averaged over {n_weeks_selected} week"
infotext_counts = f"case counts averaged over {n_weeks_selected} week"


#-------------------------------------------------
# data prep
# keep only up to selected weeks 
df_temp = ss.df_can
df_opc = df_temp[df_temp['date']<=date_selected]
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
with cont02:
    st.caption(infotext_period, text_alignment  = "center")
    figm = px.line(df_b, 
        x = 'date', y = 'incValue', 
        height = 200,  markers=True, 
        color_discrete_sequence = ["#F25B10"]
        )
    _ = figm.update_xaxes(showline=True, linewidth=1, linecolor='white', mirror=True)
    _ = figm.update_yaxes(showline=True, linewidth=1, linecolor='white', mirror=True)
    _ = figm.update_layout(paper_bgcolor="#000000") # "#350030"
    _ = figm.update_layout(margin=dict(l=5, r=15, t=10, b=3))
    st.plotly_chart(figm, use_container_width=True)


#-------------------------------------------------
# line-plot feedback to user 
# with c0:
with c1:
    fig_lin_a = make_line_plot_with_vref(ss.df_all, height = 100, y_title = '')
    fig_lin_b = fig_lin_a.add_vrect(x0=sel_data_min, x1=sel_data_max, fillcolor="pink", opacity=0.66, line_width=2.5, line_color="white", layer="below")
    st.plotly_chart(fig_lin_b, use_container_width=True, theme=None)

#######################################
# second row

from streamlit_vertical_slider import vertical_slider


c0,c1,c2,c3 = st.columns([5,1,5,1], border=True)
with c1:
    ss.col_max_inc = st.number_input("Color threshold incValue", min_value = 1.0, max_value =20.0, 
                            value = ss.col_max_inc, step = 0.1, key="k_col_max_inx",)
with c3:
    # ss.col_max_cou = st.slider("Color threshold counts",   min_value = 10.0, max_value =500.0 ,
    #                            value = ss.col_max_cou, step = 5.0, key="k_col_max_cou",)
   
    ss.col_max_cou = vertical_slider("Color threshold incValue", 
        key="k_col_max_cou",
        height=300,
        step = 10.0,
        min_value=10.0,
        max_value=500.0,
        default_value=ss.col_max_cou,
    )



#-------------------------------------------------
# prepare main hexagon plots 
color_map_01 = sample_colorscale("rainbow", 10, low=0.45, high=0.85)
color_map_02 = "bluered"
fig_incide = make_hexagon_plot(df_one_per_canton = df_incide, resp_var = 'incValue', color_map = color_map_01, color_max_val = ss.col_max_inc)
fig_counts = make_hexagon_plot(df_one_per_canton = df_counts, resp_var = 'value',    color_map = color_map_02, color_max_val = ss.col_max_cou)

#-------------------------------------------------
# display main hexagon plots 
with c0:
    st.plotly_chart(fig_incide, use_container_width=False, theme=None, )
    ca, cb = st.columns([2,2])
    ca.caption(infotext_period)
    ca.caption(infotext_incide)
    cb.caption("Incidence values ('incValue') are normalized by canton's population")
with c2:
    st.plotly_chart(fig_counts, use_container_width=False, theme=None, )
    ca, cb = st.columns([2,2])
    ca.caption(infotext_period)
    ca.caption(infotext_counts)
    cb.caption("Counts ('value') are not normalized by canton's population")







