#--------------------             
# Author : Serge Zaugg
# Description : tbd
#--------------------

import pandas as pd 
import plotly.express as px
import streamlit as st



@st.cache_data
def preprocess_INFLUENZA_oblig(df):
    # make a continuous time variable 
    df['date'] = df["temporal"].apply(pd.Timestamp.fromisoformat)
    # ewcode  
    df['agegroup'].replace(to_replace='0 - 4',   value='00-04',   inplace=True)
    df['agegroup'].replace(to_replace='5 - 14',  value='05-14',   inplace=True)
    df['agegroup'].replace(to_replace='15 - 29', value='15-29',   inplace=True)
    df['agegroup'].replace(to_replace='30 - 64', value='30-64',   inplace=True)
    df['agegroup'].replace(to_replace='65+',     value='65+',     inplace=True)
    df['agegroup'].replace(to_replace='unknown', value='Unknown', inplace=True)
    df['agegroup'].replace(to_replace='all',     value='All',     inplace=True)
    # 
    return(df)


@st.cache_data
def get_all(df):
    df = df[df["type"]  == 'all']
    df = df[df["valueCategory"]  == 'cases']
    df = df[df["georegion"] == 'CHFL']
    df = df[df["agegroup"]  == 'All']
    df = df[df["sex"]  == 'all']
    return(df)

@st.cache_data
def get_by_cantons(df):
    df = df[df["type"]  == 'all']
    df = df[df["valueCategory"]  == 'cases']
    df = df[df["georegion"] != 'CHFL']
    df = df[df["agegroup"]  == 'All']
    df = df[df["sex"]  == 'all']
    return(df)

@st.cache_data
def get_by_agegroup(df):
    df = df[df["type"]  == 'all']
    df = df[df["valueCategory"]  == 'cases']
    df = df[df["georegion"] == 'CHFL']
    df = df[df["agegroup"]  != 'All']
    df = df[df["sex"]  == 'all']
    df = df.sort_values(by=["agegroup", 'date'], ascending=True)
    return(df)

@st.cache_data
def get_by_sex(df):
    df = df[df["type"]  == 'all']
    df = df[df["valueCategory"]  == 'cases']
    df = df[df["georegion"] == 'CHFL']
    df = df[df["agegroup"]  == 'All']
    df = df[df["sex"]  != 'all']
    df = df.sort_values(by=["sex", 'date'], ascending=True)
    return(df)

@st.cache_data
def make_line_plot(df, color_groups, color_sequence):
    fig = px.line(
        data_frame = df, 
        color = color_groups, 
        x = 'date', y = 'incValue', markers=True, template="plotly_dark", color_discrete_sequence = color_sequence)
    
    fig.update_xaxes(showline=True, linewidth=2, linecolor='white', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='white', mirror=True)
    fig.update_layout(xaxis_title='Date', yaxis_title='Cases per 100000 inhabitants')

    return(fig)










