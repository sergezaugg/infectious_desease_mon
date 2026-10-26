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
import pickle

#---------------------------------
# (1) function for data download 

@st.cache_data(ttl=24*60*60)
def download_all_data(data_file):

    try:
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
        data_source = "✅ Sucessfully downloaded"

    except:
        print("Warning: fall back to historical_data!")
        with open("historical_data/bag_flu_data_20261025.pkl", "rb") as f:
            di_reloded = pickle.load(f)
        data_di, data_version, ts = di_reloded
        data_source = "⚠️ Historical data fallback"

    return(data_di, data_version, ts, data_source)   
          

#---------------------------------
# (2) function for data preparation 
# Weekly data as string "2013-W13"
# corrected function
def convert_iso_date_to_datetime(d):
    return pd.to_datetime(f"{d[:4]}-W{d[-2:]}-1", format="%G-W%V-%u")

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

# filter rows 

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

# aggregate

@st.cache_data
def get_mean_by_group(x, resp_var, group_var):
    x = x[['date', group_var, resp_var]]
    x = x.groupby(group_var, as_index=False)[resp_var].mean()
    return(x)

@st.cache_data
def get_mean_by_canton(x, resp_var):
    """ take cumsum """
    x = x[['date', 'georegion', resp_var]]
    x = x.groupby("georegion", as_index=False)[resp_var].mean()
    x = x.rename(columns={"value": resp_var})
    return(x)

# spec

@ st.cache_data
def prepare_data_for_barplots(df_typ, df_sex, df_age, recency_limit_date, resp_var):
    """ AAA """
    # take latest valid weeks - per grp
    df_typ_recent = df_typ[df_typ['date'] >= recency_limit_date]
    df_sex_recent = df_sex[df_sex['date'] >= recency_limit_date]
    df_age_recent = df_age[df_age['date'] >= recency_limit_date]
    # get mean weekly-incidence
    df_typ_recent_mean = get_mean_by_group(df_typ_recent, resp_var, 'type')
    df_sex_recent_mean = get_mean_by_group(df_sex_recent, resp_var, 'sex')
    df_age_recent_mean = get_mean_by_group(df_age_recent, resp_var, 'agegroup')
    # since pop constant per group we mis-use mean to get pop
    df_typ_recent_pop = get_mean_by_group(df_typ_recent, 'pop', 'type')
    df_sex_recent_pop = get_mean_by_group(df_sex_recent, 'pop', 'sex')
    df_age_recent_pop = get_mean_by_group(df_age_recent, 'pop', 'agegroup')
    # merge-in pop 
    df_typ_recent_mean = df_typ_recent_mean.merge(df_typ_recent_pop, how = 'left', on = 'type')
    df_sex_recent_mean = df_sex_recent_mean.merge(df_sex_recent_pop, how = 'left', on = 'sex')
    df_age_recent_mean = df_age_recent_mean.merge(df_age_recent_pop, how = 'left', on = 'agegroup')
    # convert pop from int to string (in millions)
    df_typ_recent_mean["pop_str"] = (df_typ_recent_mean["pop"] / 1e6).map(lambda x: f"{x:.1f}M")
    df_sex_recent_mean["pop_str"] = (df_sex_recent_mean["pop"] / 1e6).map(lambda x: f"{x:.1f}M")
    df_age_recent_mean["pop_str"] = (df_age_recent_mean["pop"] / 1e6).map(lambda x: f"{x:.1f}M")
    # return 
    return df_typ_recent_mean, df_sex_recent_mean, df_age_recent_mean




