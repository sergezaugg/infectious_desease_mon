


import pandas as pd 
import streamlit as st
from streamlit import session_state as ss
from utils import update_ss, show_selected_plots, download_all_data, draw_figures, prepare_data

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

c02, c03, c04 = st.columns([0.3, 0.3, 0.5])
c02.text("Download progress")
progr_bar1 = c02.progress(0, text='')


aaa = download_all_data(progr_bar1)




aaa = ss["data"]["data_di"]['INFLUENZA_oblig'].head()


aaa.temporal
ss["data"]["data_di"]['INFLUENZA_oblig'].columns



df_obli = ss["data"]["data_di"]["INFLUENZA_oblig"]



df_obli["temporal"].unique()

# fix 
df_obli.shape
df_obli = df_obli[df_obli["temporal_type"] == "iso_week"]
df_obli.shape

df_obli.head()

df_obli = preprocess_INFLUENZA(df_obli)


# temporal_type == 'iso_week'


df_obli['date'] = df_obli["temporal"].apply(convert_iso_date_to_datetime)








