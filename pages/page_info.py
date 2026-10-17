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


import streamlit as st

col_aa, col_bb, = st.columns([0.50, 0.05])
with col_aa: 
    with st.container(border=True, ):
        st.markdown('''
        ### CREDITS
        Data kindly provided weekly on this [API](https://www.idd.bag.admin.ch/portal-data) by the Swiss Federal Office of Public Health ([FOPH](https://www.bag.admin.ch/)).
        ''')
        st.markdown('''### LINKS ''')
        st.page_link("https://www.idd.bag.admin.ch/dataexplorer", label="Official visual frontend of FOPH")
        st.page_link("https://www.idd.bag.admin.ch/survey-systems/oblig", label="Mandatory reporting (oblig)")



        st.markdown(''' 
            :primary[Created by]
            :primary[[Serge Zaugg](https://www.linkedin.com/in/dkifh34rtn345eb5fhrthdbgf45/)]    
            :primary[[Pollito-ML](https://github.com/sergezaugg)]
            ''')


