#--------------------             
# Author : Serge Zaugg
# Description : Some concise background info 
#--------------------

import streamlit as st

col_aa, col_bb, = st.columns([0.50, 0.20])

with col_aa: 

    with st.container(border=True):
        st.title("Swiss Influenza Monitoring Visualization") 

    with st.container(border=True, ):
        st.markdown(
        '''    
        **SUMMARY**

        A simple dashboard to visualize Influenza monitoring data provided by the Data API of the Swiss Federal Office of Public Health (FOPH).

        **EPI SUMMARY**

        Incidence is the rate of new cases or events over a specified period for the population at risk for the event. 
        


        ''')

    st.markdown(''':gray[CREDITS]''')
    st.page_link("https://www.bag.admin.ch/", label=":gray[Federal Office of Public Health]")

    st.markdown(''':gray[RELATED LINKS]''')
    st.page_link("https://www.idd.bag.admin.ch/portal-data", label=":gray[Data API provided by FOPH]")
    st.page_link("https://www.idd.bag.admin.ch/dataexplorer", label=":gray[Official frontend of FOPH]")
    
     

      
