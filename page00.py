#--------------------             
# Author : Serge Zaugg
# Description : Some concise background info 
#--------------------

import streamlit as st

col_aa, col_bb, = st.columns([0.50, 0.20])
with col_aa: 
    with st.container(border=True, ):

        st.markdown('''
        ## CREDITS
        * ### Data kindly provided weekly on this [API](https://www.idd.bag.admin.ch/portal-data) by the Swiss Federal Office of Public Health ([FOPH](https://www.bag.admin.ch/)).
        ''')

        st.markdown('''### LINKS ''')
        st.page_link("https://www.bag.admin.ch/", label="Data provided by FOPH")
        st.page_link("https://www.idd.bag.admin.ch/portal-data", label="Data API")
        st.page_link("https://www.idd.bag.admin.ch/dataexplorer", label="Official frontend of FOPH")
        st.page_link("https://www.idd.bag.admin.ch/survey-systems/oblig", label="Mandatory reporting (oblig)")
        st.page_link("https://www.idd.bag.admin.ch/survey-systems/sentinella", label="Voluntary surveillance (sentinella)")

   
    
     

      
