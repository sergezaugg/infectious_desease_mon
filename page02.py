#--------------------             
# Author : Serge Zaugg
# Description : tbd
#--------------------

import requests
import pandas as pd 
import io
import plotly.express as px
import streamlit as st
from streamlit import session_state as ss

# # dev
# st.write(ss["data"])

for k in ss["data"]["data_di"].keys() :
    st.divider()
    st.subheader(k)
    st.dataframe(ss["data"]["data_di"][k])




