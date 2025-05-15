#--------------------             
# Author : Serge Zaugg
# Description : Streamlit page 
#--------------------

import streamlit as st
from streamlit import session_state as ss
# from utils import update_ss

st.text("  ")  
st.text("Sex")  
cols_b = st.columns(18)   
ss["colseq"]["fig_sex"][0] = cols_b[0].color_picker("Female",  ss["colseq"]["fig_sex"][0])   
ss["colseq"]["fig_sex"][1] = cols_b[1].color_picker("Male",    ss["colseq"]["fig_sex"][1])   
ss["colseq"]["fig_sex"][2] = cols_b[2].color_picker("Unknown", ss["colseq"]["fig_sex"][2])   

st.text("  ")  
st.text("Age groups")  
cols_b = st.columns(18)   
ss["colseq"]["fig_age"][0] = cols_b[0].color_picker("00-04",   ss["colseq"]["fig_age"][0])   
ss["colseq"]["fig_age"][1] = cols_b[1].color_picker("05-14",   ss["colseq"]["fig_age"][1])   
ss["colseq"]["fig_age"][2] = cols_b[2].color_picker("15-29",   ss["colseq"]["fig_age"][2])   
ss["colseq"]["fig_age"][3] = cols_b[3].color_picker("30-64",   ss["colseq"]["fig_age"][3])   
ss["colseq"]["fig_age"][4] = cols_b[4].color_picker("65+",     ss["colseq"]["fig_age"][4])   
ss["colseq"]["fig_age"][5] = cols_b[5].color_picker("Unknown", ss["colseq"]["fig_age"][5])   




