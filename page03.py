#--------------------             
# Author : Serge Zaugg
# Description : tbd
#--------------------

import pandas as pd 
import plotly.express as px
import streamlit as st
from streamlit import session_state as ss
from utils import get_all, get_by_cantons, get_by_agegroup, get_by_sex, make_line_plot


@st.cache_data
def preprocess_INFLUENZA_oblig(df):
    # make a continuous time variable 
    df['date'] = df["temporal"].apply(pd.Timestamp.fromisoformat)
    return(df)

df = ss["data"]["data_di"]["INFLUENZA_oblig"]

df = preprocess_INFLUENZA_oblig(df)

df_all = get_all(df)
df_can = get_by_cantons(df)
df_age = get_by_agegroup(df)
df_sex = get_by_sex(df)

fig_all = make_line_plot(df_all, 'georegion', ss["colseq"]["fig_all"])
fig_can = make_line_plot(df_can, 'georegion', ss["colseq"]["fig_can"])
fig_age = make_line_plot(df_age, 'agegroup',  ss["colseq"]["fig_age"])
fig_sex = make_line_plot(df_sex, 'sex',       ss["colseq"]["fig_sex"])

st.plotly_chart(fig_all)
st.plotly_chart(fig_sex)
st.plotly_chart(fig_age)
st.plotly_chart(fig_can)



