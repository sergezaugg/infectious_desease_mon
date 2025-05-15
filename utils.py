#--------------------             
# Author : Serge Zaugg
# Description : tbd
#--------------------

import pandas as pd 
import plotly.express as px
import streamlit as st

@st.cache_data
def get_all(df):
    df = df[df["type"]  == 'all']
    df = df[df["valueCategory"]  == 'cases']
    df = df[df["georegion"] == 'CHFL']
    df = df[df["agegroup"]  == 'all']
    df = df[df["sex"]  == 'all']
    return(df)

@st.cache_data
def get_by_cantons(df):
    df = df[df["type"]  == 'all']
    df = df[df["valueCategory"]  == 'cases']
    df = df[df["georegion"] != 'CHFL']
    df = df[df["agegroup"]  == 'all']
    df = df[df["sex"]  == 'all']
    return(df)

@st.cache_data
def get_by_agegroup(df):
    df = df[df["type"]  == 'all']
    df = df[df["valueCategory"]  == 'cases']
    df = df[df["georegion"] == 'CHFL']
    df = df[df["agegroup"]  != 'all']
    df = df[df["sex"]  == 'all']
    return(df)

@st.cache_data
def get_by_sex(df):
    df = df[df["type"]  == 'all']
    df = df[df["valueCategory"]  == 'cases']
    df = df[df["georegion"] == 'CHFL']
    df = df[df["agegroup"]  == 'all']
    df = df[df["sex"]  != 'all']
    return(df)

@st.cache_data
def make_line_plot(df, color_groups, color_sequence):
    fig = px.line(
        data_frame = df, 
        color = color_groups, 
        x = 'date', y = 'incValue', markers=True, template="plotly_dark", color_discrete_sequence = color_sequence)
    return(fig)










