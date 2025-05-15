#--------------------             
# Author : Serge Zaugg
# Description : Streamlit page 
#--------------------

import streamlit as st
from streamlit import session_state as ss
# from utils import update_ss

# st.text("Scatter color")
# cols_a = st.columns(18)
# ss["upar"]["col_a"] = cols_a[0].color_picker("Class A", ss["upar"]["col_a"])   
# ss["upar"]["col_b"] = cols_a[1].color_picker("Class B", ss["upar"]["col_b"])  

st.text("  ")  
st.text("Sex")  
cols_b = st.columns(18)   
ss["colseq"]["fig_sex"][0] = cols_b[0].color_picker("Female",  ss["colseq"]["fig_sex"][0])   
ss["colseq"]["fig_sex"][1] = cols_b[1].color_picker("Male",    ss["colseq"]["fig_sex"][1])   
ss["colseq"]["fig_sex"][2] = cols_b[2].color_picker("Unknown", ss["colseq"]["fig_sex"][2])   



st.text("  ")  
st.text("Age groups")  
cols_b = st.columns(18)   
ss["colseq"]["fig_age"][0] = cols_b[0].color_picker("aa", ss["colseq"]["fig_age"][0])   
ss["colseq"]["fig_age"][1] = cols_b[1].color_picker("bb", ss["colseq"]["fig_age"][1])   
ss["colseq"]["fig_age"][2] = cols_b[2].color_picker("cc", ss["colseq"]["fig_age"][2])   
ss["colseq"]["fig_age"][3] = cols_b[3].color_picker("dd", ss["colseq"]["fig_age"][3])   
ss["colseq"]["fig_age"][4] = cols_b[4].color_picker("ee", ss["colseq"]["fig_age"][4])   
ss["colseq"]["fig_age"][5] = cols_b[5].color_picker("ff", ss["colseq"]["fig_age"][5])   