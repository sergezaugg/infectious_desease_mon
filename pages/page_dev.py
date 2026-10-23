#--------------------             
# Author : Serge Zaugg
# Description : app maintenance and refresh 
#--------------------

import streamlit as st
from streamlit import session_state as ss
from src.utilsdataprep import download_all_data

c1, c2 = st.columns([15, 50])
with c1:
    # password protected maintenance dev-mode
    dev_mode = st.text_input("🛠️ Maintenance access: enter code 🥄", value="", type="password") == st.secrets['maintenancecode']
    if dev_mode:
        with st.container(border=True, height = 100):    
            if st.button("🔄 Refresh data"):
                del ss["data_di"]
                download_all_data.clear()
                st.rerun()

with st.expander("Session state"):
    st.write(sorted(st.session_state.keys()))


