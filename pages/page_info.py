#--------------------             
# Author : Serge Zaugg
# Description : Some infos for user
#--------------------

import streamlit as st
from streamlit import session_state as ss

st.text("""Incidence given as number of new cases per week normalized per 100000 inhabitants.""")
st.text("""For groups, incidence is normalized within group.""")
st.text("""Relative incidence = inc. group / sum(inc. all groups).""")
st.text("""Area plots shown when overall incidence above cutoff (can be adjusted).""")




