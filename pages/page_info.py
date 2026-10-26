#--------------------             
# Author : Serge Zaugg
# Description : Some infos for user
#--------------------

import streamlit as st
from streamlit import session_state as ss

col_aa, col_bb, = st.columns([0.50, 0.40])
with col_aa: 
    with st.container(border=True):
        st.markdown('''
        ### About this web-app
        This web-app provides interactive visualizations and analytics of the latest influenza surveillance data published weekly 
        by the Swiss Federal Office of Public Health (FOPH).
        Its primary goal is to provide an overview of the current influenza situation in Switzerland.
        Historical analysis tools are provided to explore past waves and put recent observations into context.
        ''') 

    with st.container(border=True):
        st.markdown('''    
        ### Credits 
        Data kindly compiled and curated by the [Swiss Federal Office of Public Health (FOPH)](https://www.bag.admin.ch/).   
        The data is provided weekly (updated Wednesdays) on this [API](https://www.idd.bag.admin.ch/portal-data).   
        A visual data explorer of FOPH can be found [here](https://www.idd.bag.admin.ch/dataexplorer).   
        ''') 

    with st.container(border=True):
        st.markdown('''   
        ### Author
        Created by: :primary[[Serge Zaugg](https://www.linkedin.com/in/dkifh34rtn345eb5fhrthdbgf45/)]     
        GitHub: :primary[[Pollito-ML](https://github.com/sergezaugg)]
        ''')


