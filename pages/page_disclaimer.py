#--------------------             
# Author : Serge Zaugg
# Description : Page with concise background info and credits
#--------------------

import streamlit as st

col_aa, col_bb, = st.columns([0.50, 0.50])
with col_aa: 
    with st.container(border=True, ):
        st.markdown('''
        ### DISCLAIMER
        This dashboard provides visualizations of Influenza (Flu) surveillance data from the API of the
        Swiss Federal Office of Public Health (FOPH). 
        This web-app is an independent project and is not an official FOPH product, nor is it endorsed by the FOPH. 
        This web-app is intended only for exploration purposes. 
        It is not intended to provide medical advice, diagnosis, or to replace official public-health
        information or guidance.
        ''')
       
