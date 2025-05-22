#--------------------             
# Author : Serge Zaugg
# Description : tbd
#--------------------

import numpy as np
import pandas as pd 
import plotly.express as px
import streamlit as st
from datetime import date
from datetime import datetime
from streamlit import session_state as ss

def convert_iso_date_to_datetime(d):
    return(datetime.strptime(d + '-1', "%Y-W%W-%w"))


def update_ss(kname, ssname):
    """
    description : helper callback fun to implement statefull apps
    kname : key name of widget
    ssname : key name of variable in session state (ss)
    """
    ss["upar"][ssname] = ss[kname]      


@st.cache_data
def preprocess_INFLUENZA(df):
    # make a continuous time variable 
    # df['date'] = df["temporal"].apply(pd.Timestamp.fromisoformat) # Buggie
    df['date'] = df["temporal"].apply(convert_iso_date_to_datetime)
    # re-code  
    df['agegroup'].replace(to_replace='0 - 4',   value='00-04',   inplace=True)
    df['agegroup'].replace(to_replace='5 - 14',  value='05-14',   inplace=True)
    df['agegroup'].replace(to_replace='15 - 29', value='15-29',   inplace=True)
    df['agegroup'].replace(to_replace='30 - 64', value='30-64',   inplace=True)
    df['agegroup'].replace(to_replace='65+',     value='65+',     inplace=True)
    df['agegroup'].replace(to_replace='unknown', value='Unknown', inplace=True)
    df['agegroup'].replace(to_replace='all',     value='All',     inplace=True)
    # 
    return(df)


# oblig 
@st.cache_data
def get_all_oblig(df):
    df = df[df["type"]  == 'all']
    df = df[df["valueCategory"]  == 'cases']
    df = df[df["georegion"] == 'CHFL']
    df = df[df["agegroup"]  == 'All']
    df = df[df["sex"]  == 'all']
    return(df)

@st.cache_data
def get_by_cantons_oblig(df):
    df = df[df["type"]  == 'all']
    df = df[df["valueCategory"]  == 'cases']
    df = df[df["georegion"] != 'CHFL']
    df = df[df["agegroup"]  == 'All']
    df = df[df["sex"]  == 'all']
    return(df)

@st.cache_data
def get_by_agegroup_oblig(df):
    df = df[df["type"]  == 'all']
    df = df[df["valueCategory"]  == 'cases']
    df = df[df["georegion"] == 'CHFL']
    df = df[df["agegroup"]  != 'All']
    df = df[df["sex"]  == 'all']
    df = df.sort_values(by=["agegroup", 'date'], ascending=True)
    return(df)

@st.cache_data
def get_by_sex_oblig(df):
    df = df[df["type"]  == 'all']
    df = df[df["valueCategory"]  == 'cases']
    df = df[df["georegion"] == 'CHFL']
    df = df[df["agegroup"]  == 'All']
    df = df[df["sex"]  != 'all']
    df = df.sort_values(by=["sex", 'date'], ascending=True)
    return(df)



# sentinella
@st.cache_data
def get_all_sentinella(df):
    df = df[df["valueCategory"]  == 'consultations']
    df = df[df["georegion"] == 'CH']
    df = df[df["agegroup"]  == 'All']
    df = df[df["sex"]  == 'all']
    return(df)

@st.cache_data
def get_by_region_sentinella(df):
    df = df[df["valueCategory"]  == 'consultations']
    df = df[df["georegion"] != 'CH']
    df = df[df["agegroup"]  == 'All']
    df = df[df["sex"]  == 'all']
    return(df)

@st.cache_data
def get_by_agegroup_sentinella(df):
    df = df[df["valueCategory"]  == 'consultations']
    df = df[df["georegion"] == 'CH']
    df = df[df["agegroup"]  != 'All']
    df = df[df["sex"]  == 'all']
    return(df)

@st.cache_data
def get_by_sex_sentinella(df):
    df = df[df["valueCategory"]  == 'consultations']
    df = df[df["georegion"] == 'CH']
    df = df[df["agegroup"]  == 'All']
    df = df[df["sex"]  != 'all']
    return(df)

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
def make_area_plot(df, color_groups, color_sequence, y_title):
    # set area plot to nan whe overall incidence was too low
    df['incValue'][df['incValue_all']<1.0] = np.nan
    fig = px.area(
        groupnorm = 'fraction',
        data_frame = df, 
        color = color_groups, 
        height = 260,
        x = 'date', 
        y = 'incValue', 
        template="plotly_dark", 
        color_discrete_sequence = color_sequence,
        markers = False,
        line_shape = 'hvh',#'spline', One of 'linear', 'spline', 'hv', 'vh', 'hvh', or 'vhv'
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


@st.fragment
def show_selected_plots(): 

    # update x axis zoom for all available plots 
    for k in ss["figures"].keys():
        ss["figures"][k].update_xaxes(type="date", range=ss["upar"]["date_range"])
        # update_zoom_line_plot(fig = ss["figures"][k], date_range = ss["upar"]["date_range"])

    # rename locally for ease of reading coed
    sel_d = ss["upar"]["selecte_data_sources"]
    sel_g = ss["upar"]["selecte_data_groupings"]
    set_t = ss["upar"]["plot_type"]

    with st.container(height=None, border=True):

        if 'oblig' in sel_d and 'All' in sel_g:
            st.plotly_chart(ss["figures"]["fig_all_oblig"], use_container_width=True, theme=None)

        if 'oblig' in sel_d and 'Sex' in sel_g and "Line" in set_t:
            st.plotly_chart(ss["figures"]["fig_sex_oblig"], use_container_width=True, theme=None)
        if 'oblig' in sel_d and 'Sex' in sel_g and "Area" in set_t:
            st.plotly_chart(ss["figures"]["figa_sex_oblig"], use_container_width=True, theme=None)

        if 'oblig' in sel_d and 'Age' in sel_g and "Line" in set_t:
            st.plotly_chart(ss["figures"]["fig_age_oblig"], use_container_width=True, theme=None)
        if 'oblig' in sel_d and 'Age' in sel_g and "Area" in set_t:
            st.plotly_chart(ss["figures"]["figa_age_oblig"], use_container_width=True, theme=None)

        if 'oblig' in sel_d and 'Region' in sel_g and "Line" in set_t:
            st.plotly_chart(ss["figures"]["fig_can_oblig"], use_container_width=True, theme=None)
        if 'oblig' in sel_d and 'Region' in sel_g and "Area" in set_t:
            st.plotly_chart(ss["figures"]["figa_can_oblig"], use_container_width=True, theme=None)
    
    with st.container(height=None, border=True):

        if 'sentinella' in sel_d and  'All' in sel_g:
            st.plotly_chart(ss["figures"]["fig_all_sent"], use_container_width=True, theme=None)

        if 'sentinella' in sel_d and  'Sex' in sel_g and "Line" in set_t:
            st.plotly_chart(ss["figures"]["fig_sex_sent"], use_container_width=True, theme=None)
        if 'sentinella' in sel_d and  'Sex' in sel_g and "Area" in set_t:
            st.plotly_chart(ss["figures"]["figa_sex_sent"], use_container_width=True, theme=None)

        if 'sentinella' in sel_d and  'Age' in sel_g and "Line" in set_t:
            st.plotly_chart(ss["figures"]["fig_age_sent"], use_container_width=True, theme=None)
        if 'sentinella' in sel_d and  'Age' in sel_g and "Area" in set_t:
            st.plotly_chart(ss["figures"]["figa_age_sent"], use_container_width=True, theme=None)

        if 'sentinella' in sel_d and  'Region' in sel_g and "Line" in set_t:
            st.plotly_chart(ss["figures"]["fig_can_sent"], use_container_width=True, theme=None)
        if 'sentinella' in sel_d and  'Region' in sel_g and "Area" in set_t:
            st.plotly_chart(ss["figures"]["figa_can_sent"], use_container_width=True, theme=None)
















