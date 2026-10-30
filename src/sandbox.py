
import pandas as pd 
# import streamlit as st
from datetime import datetime
from streamlit import session_state as ss
import requests
import io
import pickle
from config import FOPH_DATA_VERSION_URL, FOPH_LATEST_DATA_URL
from src.utils_dataprep import download_all_data, preprocess_INFLUENZA
import pickle

full_query_string = FOPH_DATA_VERSION_URL
r = requests.get(full_query_string, allow_redirects=True)
r.status_code
data_version = r.json()
data_version.get("statusCode", 200) != 200
# di_downloded = download_all_data(data_file = ["INFLUENZA_oblig", "INFLUENZA_sentinella"]) 
