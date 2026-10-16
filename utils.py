#--------------------             
# Author : Serge Zaugg
# Description : All functions an UI elements used my the streamlit app
#--------------------

import numpy as np
import pandas as pd 
import plotly.express as px
import streamlit as st
from streamlit import session_state as ss

#---------------------------------
# (0) general function  

def update_ss(kname, ssname):
    """
    description : helper callback function to implement stateful apps
    kname : key name of widget
    ssname : key name of variable in session state (ss)
    """
    ss["upar"][ssname] = ss[kname]      








# -----------------------------------------
# (3) function to pre-render plotly figures

@st.cache_data
def make_line_plot(df, color_groups, color_sequence, y_title):
    fig = px.line(
        data_frame = df, 
        color = color_groups, 
        height = 260,
        x = 'date', 
        y = 'incValue', 
        markers=True, 
        template="plotly_dark", 
        color_discrete_sequence = color_sequence
        )
    _ = fig.update_xaxes(showline=True, linewidth=2, linecolor='white', mirror=True)
    _ = fig.update_yaxes(showline=True, linewidth=2, linecolor='white', mirror=True)
    _ = fig.update_layout(xaxis_title='Date', yaxis_title=y_title)
    _ = fig.update_layout(paper_bgcolor="#000000") # "#350030"
    _ = fig.update_layout(margin=dict(l=1, r=200, t=10, b=1))
    _ = fig.update_layout(xaxis_title_font_size=15)
    _ = fig.update_layout(yaxis_title_font_size=15)
    _ = fig.update_layout(xaxis_tickfont_size=15)
    _ = fig.update_layout(legend_font_size=20)
    _ = fig.update_layout(xaxis_title=None)
    return(fig)

@st.cache_data
def make_area_plot(df, color_groups, color_sequence, y_title, cutoff, height = 260):
    # set area plot to nan whe overall incidence was too low
    df = df.copy() # to avoid orig df in ss to be cut !
    # quick fix
    df.loc[df["incValue_all"] < cutoff, "incValue"] = np.nan

    fig = px.area(
        groupnorm = 'fraction',
        data_frame = df, 
        color = color_groups, 
        height = height,
        x = 'date', 
        y = 'incValue', 
        template="plotly_dark", 
        color_discrete_sequence = color_sequence,
        markers = False,
        line_shape = 'hvh', # 'hvh',#'spline', One of 'linear', 'spline', 'hv', 'vh', 'hvh', or 'vhv'
        )
    _ = fig.update_xaxes(showline=True, linewidth=2, linecolor='white', mirror=True)
    _ = fig.update_yaxes(showline=True, linewidth=2, linecolor='white', mirror=True)
    _ = fig.update_layout(xaxis_title='Date', yaxis_title=y_title)
    _ = fig.update_layout(paper_bgcolor="#000000") # "#350030"
    _ = fig.update_layout(margin=dict(l=1, r=200, t=10, b=1))
    _ = fig.update_layout(xaxis_title_font_size=15)
    _ = fig.update_layout(yaxis_title_font_size=15)
    _ = fig.update_layout(xaxis_tickfont_size=15)
    _ = fig.update_layout(legend_font_size=20)
    _ = fig.update_layout(xaxis_title=None)
    _ = fig.update_traces(line=dict(width=0.2))
    _ = fig.update_layout(yaxis_range=[0.0,1.0])
    _ = fig.for_each_trace(lambda trace: trace.update(fillcolor = trace.line.color))
    return(fig)

def draw_figures(data, colseq):
    # lineplots 
    ss["figures"]["fig_all_oblig"] = make_line_plot(data["df_all_obli"], 'georegion', colseq["fig_all_oblig"], y_title = 'Cases per 100000 inhab', )
    ss["figures"]["fig_can_oblig"] = make_line_plot(data["df_can_obli"], 'georegion', colseq["fig_can_oblig"], y_title = 'Cases per 100000 inhab', )
    ss["figures"]["fig_age_oblig"] = make_line_plot(data["df_age_obli"], 'agegroup',  colseq["fig_age_oblig"], y_title = 'Cases per 100000 inhab',)
    ss["figures"]["fig_sex_oblig"] = make_line_plot(data["df_sex_obli"], 'sex',       colseq["fig_sex_oblig"], y_title = 'Cases per 100000 inhab', )
    ss["figures"]["fig_typ_oblig"] = make_line_plot(data["df_typ_obli"], 'type',      colseq["fig_typ_oblig"], y_title = 'Cases per 100000 inhab', )
    # area plots
    ss["figures"]["figa_can_oblig"] = make_area_plot(data["df_can_obli"], 'georegion', colseq["fig_can_oblig"], y_title = 'Relative incidence', cutoff = ss["upar"]["cutoff_obli"])
    ss["figures"]["figa_age_oblig"] = make_area_plot(data["df_age_obli"], 'agegroup',  colseq["fig_age_oblig"], y_title = 'Relative incidence', cutoff = ss["upar"]["cutoff_obli"])
    ss["figures"]["figa_sex_oblig"] = make_area_plot(data["df_sex_obli"], 'sex',       colseq["fig_sex_oblig"], y_title = 'Relative incidence', cutoff = ss["upar"]["cutoff_obli"])
    ss["figures"]["figa_typ_oblig"] = make_area_plot(data["df_typ_obli"], 'type',      colseq["fig_typ_oblig"], y_title = 'Relative incidence', cutoff = ss["upar"]["cutoff_obli"])


#----------------------------------------------------
# (4) function to organize figures in main pannel

@st.fragment
def show_selected_plots(): 
    # rename locally for ease of reading coed
    sel_g = ss["upar"]["selecte_data_groupings"]
    set_t = ss["upar"]["plot_type"]
    with st.container(height = 'content', border=True):
        if  'All' in sel_g:
            st.plotly_chart(ss["figures"]["fig_all_oblig"],  use_container_width=True, theme=None, config={"displayModeBar": False}, key = "k001")

        if 'Age' in sel_g and "Line" in set_t:
            st.plotly_chart(ss["figures"]["fig_age_oblig"],  use_container_width=True, theme=None, config={"displayModeBar": False}, key = "k002")
        if 'Age' in sel_g and "Area" in set_t:
            st.plotly_chart(ss["figures"]["figa_age_oblig"], use_container_width=True, theme=None, config={"displayModeBar": False}, key = "k003")

        if 'Type' in sel_g and "Line" in set_t:
            st.plotly_chart(ss["figures"]["fig_typ_oblig"],  use_container_width=True, theme=None, config={"displayModeBar": False}, key = "k004")
        if 'Type' in sel_g and "Area" in set_t:
            st.plotly_chart(ss["figures"]["figa_typ_oblig"], use_container_width=True, theme=None, config={"displayModeBar": False}, key = "k005")

        if 'Sex' in sel_g and "Line" in set_t:
            st.plotly_chart(ss["figures"]["fig_sex_oblig"],  use_container_width=True, theme=None, config={"displayModeBar": False}, key = "k006")
        if 'Sex' in sel_g and "Area" in set_t: 
            st.plotly_chart(ss["figures"]["figa_sex_oblig"], use_container_width=True, theme=None, config={"displayModeBar": False}, key = "k007")

        if 'Region' in sel_g and "Line" in set_t:
            st.plotly_chart(ss["figures"]["fig_can_oblig"],  use_container_width=True, theme=None, config={"displayModeBar": False}, key = "k008")
        if 'Region' in sel_g and "Area" in set_t:
            st.plotly_chart(ss["figures"]["figa_can_oblig"], use_container_width=True, theme=None, config={"displayModeBar": False}, key = "k009") 

    









