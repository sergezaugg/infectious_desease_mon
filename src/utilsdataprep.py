#--------------------             
# Author : Serge Zaugg
# Description : All data prep functions 
#--------------------

import pandas as pd 
import streamlit as st
from datetime import datetime
from streamlit import session_state as ss
import requests
import io

#---------------------------------
# (1) function for data download 
# must imperatively run on app stratup, Do not st.cache !!

@st.cache_data(ttl=24*60*60)
def download_all_data(data_file):
    full_query_string = 'https://api.idd.bag.admin.ch/api/v1/data/version'
    r = requests.get(full_query_string, allow_redirects=True)
    data_version = r.json()

    full_query_string = 'https://api.idd.bag.admin.ch/api/v1/export/latest/files'
    r = requests.get(full_query_string, allow_redirects=True)
    data_file_list = r.json()
    print("data_file_list")
    [print(a) for a in data_file_list]
    # limit data to one data file
    data_file_list =[a for a in data_file_list if a in data_file]

    data_di = {}
    for li_index in range(len(data_file_list)):
        print(li_index)
        data_set_name = data_file_list[li_index]
        full_query_string = 'https://api.idd.bag.admin.ch/api/v1/export/latest/' + data_set_name + '/csv'
        r = requests.get(full_query_string, allow_redirects=True)
        raw_text = r.text
        df = pd.read_csv(io.StringIO(raw_text, newline='\n'), sep=",")
        data_di[data_set_name] = df

    ts = datetime.now().strftime("%Y-%m-%d %H:%M")

    return(data_di, data_version, ts)   
          

#---------------------------------
# (2) function for data preparation 

def convert_iso_date_to_datetime(d):
    return(datetime.strptime(d + '-1', "%Y-W%W-%w"))

@st.cache_data
def preprocess_INFLUENZA(df):
    df = df.copy()
    # take only weekly data
    df = df[df["temporal_type"] == "iso_week"]
    # make string to a continuous time variable 
    df['date'] = df["temporal"].apply(convert_iso_date_to_datetime)
    # re-code agegroup 
    df['agegroup'] = df['agegroup'].replace(to_replace='0 - 4',   value='00-04') # ,   inplace=True)
    df['agegroup'] = df['agegroup'].replace(to_replace='5 - 14',  value='05-14') #,   inplace=True)
    df['agegroup'] = df['agegroup'].replace(to_replace='15 - 29', value='15-29') #,   inplace=True)
    df['agegroup'] = df['agegroup'].replace(to_replace='30 - 64', value='30-64') #,   inplace=True)
    df['agegroup'] = df['agegroup'].replace(to_replace='65+',     value='65+') #,     inplace=True)
    df['agegroup'] = df['agegroup'].replace(to_replace='unknown', value='Unknown') #, inplace=True)
    return(df)

@st.cache_data
def get_all_oblig(df):
    df = df[df["type"]  == 'all']
    df = df[df["valueCategory"]  == 'cases']
    df = df[df["georegion"] == 'CHFL']
    df = df[df["agegroup"]  == 'all']
    df = df[df["sex"]  == 'all']
    return(df)

@st.cache_data
def get_by_cantons_oblig(df):
    df = df[df["type"]  == 'all']
    df = df[df["valueCategory"]  == 'cases']
    df = df[df["georegion"] != 'CHFL']
    df = df[df["georegion"] != 'CH']
    df = df[df["georegion"] != 'FL']
    df = df[df["agegroup"]  == 'all']
    df = df[df["sex"]  == 'all']
    df = df.sort_values(by=["georegion", 'date'], ascending=True)
    return(df)

@st.cache_data
def get_by_agegroup_oblig(df):
    df = df[df["type"]  == 'all']
    df = df[df["valueCategory"]  == 'cases']
    df = df[df["georegion"] == 'CHFL']
    df = df[df["agegroup"]  != 'all']
    df = df[df["sex"]  == 'all']
    df = df.sort_values(by=["agegroup", 'date'], ascending=True)
    return(df)

@st.cache_data
def get_by_sex_oblig(df):
    df = df[df["type"]  == 'all']
    df = df[df["valueCategory"]  == 'cases']
    df = df[df["georegion"] == 'CHFL']
    df = df[df["agegroup"]  == 'all']
    df = df[df["sex"]  != 'all']
    df = df.sort_values(by=["sex", 'date'], ascending=True)
    return(df)

@st.cache_data
def get_by_type_oblig(df):
    df = df[df["type"] != 'all']
    df = df[df["valueCategory"]  == 'cases']
    df = df[df["georegion"] == 'CHFL']
    df = df[df["agegroup"]  == 'all']
    df = df[df["sex"]  == 'all']
    df = df.sort_values(by=["sex", 'date'], ascending=True)
    return(df)


