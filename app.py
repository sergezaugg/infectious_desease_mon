#--------------------             
# Author : Serge Zaugg
# Description : Main streamlit entry point
# Run locally : streamlit run stmain.py
#--------------------

import streamlit as st
from streamlit import session_state as ss
import plotly.express as px
from utils import draw_figures
from utilsdataprep import download_all_data, prepare_data
from resources.styles import apply_global_styles

st.set_page_config(layout="wide", initial_sidebar_state = "expanded")
apply_global_styles() # apply custom CSS styles 



# (1) set initial session state
if 'upar' not in ss:
    ss["upar"] = {
        "par03" : "initial",
        "par04" : "initial",
        "selecte_data_groupings" : ['All', 'Age', 'Type', 'Sex', 'Region',],
        "plot_type" : 'Area',
        "cutoff_obli" :  1.0,
        }

# Initialize widget state once
if "cutoff_obli_slider" not in ss:
    ss["cutoff_obli_slider"] = ss["upar"]["cutoff_obli"]    


if 'colseq' not in ss:
    ss["colseq"] = {
        "fig_all_oblig" : ["#FC08B3"],
        "fig_can_oblig" : px.colors.qualitative.Alphabet,
        "fig_reg_oblig" : px.colors.qualitative.Light24, 
        "fig_age_oblig" : ["#00ffd5", "#bbff00", "#ffd900", "#ff7b00", "#ff0000", "#7c8584", "#ffffff"],
        "fig_sex_oblig" : ["#fd6804", "#0727F7", "#7c8584",],
        "fig_typ_oblig" : ["#7802e6", "#02BB2A", "#7c8584",],
        }

if 'figures' not in ss:
    ss["figures"] = dict()



# do once on session start 
if 'data' not in ss:
    ss["data"] = {
        "data_di" : "initial",
        "data_ve" : {'name' : "Data not yet loaded!"},
        }
    ss.data.data_di, ss.data.data_ve = download_all_data()
    prepare_data()
    draw_figures(data = ss["data"], colseq = ss["colseq"], cutoff = ss["upar"]["cutoff_obli"])




# (2) sidebar
with st.sidebar:
    st.markdown(":blue[**Swiss Weekly Influenza Monitoring**]") 
    st.write("Data version " + ss["data"]["data_ve"]["name"])
    st.logo(image='pics/z_logo_blue.png', size="large", link="https://github.com/sergezaugg")

# (3) main navigation
pages = [
    st.Page("pages/page00.py",  title="Visualize"),
    st.Page("pages/page01.py",  title="Color settings"),
    st.Page("pages/page_info.py",  title="Info"),
    st.Page("pages/page02.py",  title="About"),
    st.Page("pages/page_disclaimer.py",  title="Disclaimer"),
    st.Page("pages/page99.py",  title="Dev"),
    ]
pg = st.navigation(pages, position = "top")
pg.run()





