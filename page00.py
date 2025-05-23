#--------------------             
# Author : Serge Zaugg
# Description : Some concise background info 
#--------------------

import streamlit as st

col_aa, col_bb, = st.columns([0.50, 0.20])

with col_aa: 

    with st.container(border=True):
        st.title("Swiss Influenza Monitoring Visualization (under development)") 

    with st.container(border=True, ):
        st.markdown(
        '''    
        **SUMMARY**

        A simple dashboard to visualize Influenza monitoring data provided by the Data API of the Swiss Federal Office of Public Health (FOPH).

        <Under construction>
        
        ''')

    st.markdown(''':gray[CREDITS]: Please see links in sidebar left.''')
   
    
     

      
