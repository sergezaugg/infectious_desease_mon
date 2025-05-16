#--------------------             
# Author : Serge Zaugg
# Description : tbd
#--------------------

import pandas as pd 
import plotly.express as px
import streamlit as st
from datetime import date
from datetime import datetime

def convert_iso_date_to_datetime(d):
    return(datetime.strptime(d + '-1', "%Y-W%W-%w"))

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




# plot haha
@st.cache_data
def make_line_plot(df, color_groups, color_sequence):
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
    _ = fig.update_layout(xaxis_title='Date', yaxis_title='Cases per 100000 inhabitants')
    _ = fig.update_layout(paper_bgcolor="#000000") # "#350030"
    _ = fig.update_layout(margin=dict(l=1, r=200, t=10, b=1))
    # _ = fig.update_layout(xaxis_title_font_size=25)
    # _ = fig.update_layout(yaxis_title_font_size=25)
    # _ = fig.update_layout(xaxis_tickfont_size=25)
    # _ = fig.update_layout(legend_font_size=20)
    _ = fig.update_layout(xaxis_title=None)

    return(fig)




    # _ = fig00.update_xaxes(showline = True, linecolor = 'white', linewidth = 2, row = 1, col = 1, mirror = True)
    # _ = fig00.update_yaxes(showline = True, linecolor = 'white', linewidth = 2, row = 1, col = 1, mirror = True)
    # _ = fig00.update_traces(marker=dict(size=4))
    # _ = fig00.update_layout(xaxis=dict(showgrid=False, zeroline=False), yaxis=dict(showgrid=False, zeroline=False))
    # _ = fig00.update_layout(xaxis_range=[-0.00001, +1.00001])
    # _ = fig00.update_layout(paper_bgcolor="#000000") # "#350030"
    # _ = fig00.update_yaxes(showticklabels=False)
    # # text font sizes 
    # # _ = fig00.update_layout(title_font_size=25)
    # _ = fig00.update_layout(xaxis_title_font_size=25)
    # _ = fig00.update_layout(yaxis_title_font_size=25)
    # _ = fig00.update_layout(xaxis_tickfont_size=25)
    # _ = fig00.update_layout(legend_font_size=20)
    # # _ = fig00.update_layout(title_y=0.96)
    # _ = fig00.update_layout(showlegend=False)
    # _ = fig00.update_layout(yaxis_title=None)
    # _ = fig00.update_layout(margin=dict(t=10, b=10, l=15, r=15))
    # # _ = fig00.update_layout(xaxis={'side': 'top'}) # , yaxis={'side': 'right'}  )
    # # 




