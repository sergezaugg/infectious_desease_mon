#--------------------             
# Author : Serge Zaugg
# Description : tbd
#--------------------

import streamlit as st
from streamlit import session_state as ss

for k in ss["data"]["data_di"].keys() :
    st.divider()
    st.subheader(k)
    st.dataframe(ss["data"]["data_di"][k])




