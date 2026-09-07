

import pandas as pd 
import streamlit as st
from streamlit import session_state as ss
from utils import update_ss, show_selected_plots, download_all_data, draw_figures, prepare_data



aaa = download_all_data()
