#--------------------             
# Author : Serge Zaugg
# Description : tbd
#--------------------

import streamlit as st
from streamlit import session_state as ss

if ss["data"]["data_di"] == "initial":
    st.info("Data not yet loaded!")
else:
    for k in ss["data"]["data_di"].keys() :
        st.divider()
        st.subheader(k)
        st.dataframe(ss["data"]["data_di"][k])




