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
import requests
import io
from datetime import datetime, timedelta



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

    # rename locally for ease of reading coed
    sel_d = ss["upar"]["selecte_data_sources"]
    sel_g = ss["upar"]["selecte_data_groupings"]
    set_t = ss["upar"]["plot_type"]

    # ss["upar"]["plot_type"]

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





def download_all_data(progr_bar):
    full_query_string = 'https://api.idd.bag.admin.ch/api/v1/data/version'
    r = requests.get(full_query_string, allow_redirects=True)
    data_version = r.json()

    full_query_string = 'https://api.idd.bag.admin.ch/api/v1/export/latest/files'
    r = requests.get(full_query_string, allow_redirects=True)
    data_file_list = r.json()

    # limit to specific diseases , for now 
    data_file_list =[a for a in data_file_list if a == "INFLUENZA_oblig" or a == "INFLUENZA_sentinella"]

    n_files = len(data_file_list)

    data_di = {}
    for li_index in range(len(data_file_list)):
        print(li_index)
        data_set_name = data_file_list[li_index]
        full_query_string = 'https://api.idd.bag.admin.ch/api/v1/export/latest/' + data_set_name + '/csv'
        r = requests.get(full_query_string, allow_redirects=True)
        raw_text = r.text
        df = pd.read_csv(io.StringIO(raw_text, newline='\n')  , sep=",")
        data_di[data_set_name] = df
        # update status notifications 
        progr_bar.progress((li_index+1)/n_files, text="")
          
    ss["data"]["data_di"] = data_di
    ss["data"]["data_ve"] = data_version


   


def prepare_data(progr_bar):
    progr_bar.progress(0.0, text="")
    df_obli = ss["data"]["data_di"]["INFLUENZA_oblig"]
    df_sent = ss["data"]["data_di"]["INFLUENZA_sentinella"]

    df_obli = preprocess_INFLUENZA(df_obli)
    df_sent = preprocess_INFLUENZA(df_sent)

    progr_bar.progress(0.2, text="")

    df_all_obli = get_all_oblig(df_obli)
    df_can_obli = get_by_cantons_oblig(df_obli)
    df_age_obli = get_by_agegroup_oblig(df_obli)
    df_sex_obli = get_by_sex_oblig(df_obli)
    df_all_sent = get_all_sentinella(df_sent)
    df_can_sent = get_by_region_sentinella(df_sent)
    df_age_sent = get_by_agegroup_sentinella(df_sent)
    df_sex_sent = get_by_sex_sentinella(df_sent)

    progr_bar.progress(0.4, text="")

    # merge-in all info
    df_can_obli = pd.merge(df_can_obli, df_all_obli[['date', 'incValue']], how='inner', on='date', suffixes=('', '_all'))
    df_can_sent = pd.merge(df_can_sent, df_all_sent[['date', 'incValue']], how='inner', on='date', suffixes=('', '_all'))
    df_age_obli = pd.merge(df_age_obli, df_all_obli[['date', 'incValue']], how='inner', on='date', suffixes=('', '_all'))
    df_age_sent = pd.merge(df_age_sent, df_all_sent[['date', 'incValue']], how='inner', on='date', suffixes=('', '_all'))
    df_sex_obli = pd.merge(df_sex_obli, df_all_obli[['date', 'incValue']], how='inner', on='date', suffixes=('', '_all'))
    df_sex_sent = pd.merge(df_sex_sent, df_all_sent[['date', 'incValue']], how='inner', on='date', suffixes=('', '_all'))

    progr_bar.progress(0.6, text="")

    # lineplots 
    ss["figures"]["fig_all_oblig"] = make_line_plot(df_all_obli, 'georegion', ss["colseq"]["fig_all_oblig"], y_title = 'Cases per 100000 inhab *', )
    ss["figures"]["fig_all_sent"]  = make_line_plot(df_all_sent, 'georegion', ss["colseq"]["fig_all_oblig"], y_title = 'Consultations per 100000 inhab *', )

    # if ss["upar"]["plot_type"] == 'Line': 
    ss["figures"]["fig_can_oblig"] = make_line_plot(df_can_obli, 'georegion', ss["colseq"]["fig_can_oblig"], y_title = 'Cases per 100000 inhab *', )
    ss["figures"]["fig_age_oblig"] = make_line_plot(df_age_obli, 'agegroup',  ss["colseq"]["fig_age_oblig"], y_title = 'Cases per 100000 inhab *',)
    ss["figures"]["fig_sex_oblig"] = make_line_plot(df_sex_obli, 'sex',       ss["colseq"]["fig_sex_oblig"], y_title = 'Cases per 100000 inhab *', )
    ss["figures"]["fig_can_sent"]  = make_line_plot(df_can_sent, 'georegion', ss["colseq"]["fig_reg_oblig"], y_title = 'Consultations per 100000 inhab *', )
    ss["figures"]["fig_age_sent"]  = make_line_plot(df_age_sent, 'agegroup',  ss["colseq"]["fig_age_oblig"], y_title = 'Consultations per 100000 inhab *', )
    ss["figures"]["fig_sex_sent"]  = make_line_plot(df_sex_sent, 'sex',       ss["colseq"]["fig_sex_oblig"], y_title = 'Consultations per 100000 inhab *', )

    # area plots
    # if ss["upar"]["plot_type"] == 'Area': 
    ss["figures"]["figa_can_oblig"] = make_area_plot(df_can_obli, 'georegion', ss["colseq"]["fig_can_oblig"], y_title = 'Cases per 100000 inhab *')
    ss["figures"]["figa_age_oblig"] = make_area_plot(df_age_obli, 'agegroup',  ss["colseq"]["fig_age_oblig"], y_title = 'Cases per 100000 inhab *')
    ss["figures"]["figa_sex_oblig"] = make_area_plot(df_sex_obli, 'sex',       ss["colseq"]["fig_sex_oblig"], y_title = 'Cases per 100000 inhab *')
    ss["figures"]["figa_can_sent"]  = make_area_plot(df_can_sent, 'georegion', ss["colseq"]["fig_reg_oblig"], y_title = 'Consultations per 100000 inhab *')
    ss["figures"]["figa_age_sent"]  = make_area_plot(df_age_sent, 'agegroup',  ss["colseq"]["fig_age_oblig"], y_title = 'Consultations per 100000 inhab *')    
    ss["figures"]["figa_sex_sent"]  = make_area_plot(df_sex_sent, 'sex',       ss["colseq"]["fig_sex_oblig"], y_title = 'Consultations per 100000 inhab *')

    progr_bar.progress(0.8, text="")
 
    if ss["upar"]["date_range"] == 'initial':
        delta_time = timedelta(days=100)
        # concat dates from both dfs to get global min and max 
        df_dates = pd.concat([df_obli['date'], df_sent['date']])
        time_options = df_dates.sort_values()
        t_sta = time_options.min() - delta_time
        t_sta = datetime(year = t_sta.year, month = t_sta.month, day = t_sta.day)
        t_end = time_options.max() + delta_time
        t_end = datetime(year = t_end.year, month = t_end.month, day = t_end.day)
        ss["upar"]["date_range"] = (t_sta, t_end)
        ss["upar"]["full_date_range"] = (t_sta, t_end)

    progr_bar.progress(1.0, text="")













