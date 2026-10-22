#--------------------             
# Author : Serge Zaugg
# Description : Main interactive visualization page 
#--------------------

import streamlit as st
from streamlit import session_state as ss
from src.utils_ui import draw_figures
from streamlit_vertical_slider import vertical_slider

with st.sidebar:
    st.markdown("""
    :primary[Incidence:] Weekly number of new cases per 100'000 inhabitants. For subgroup analyses, incidence is normalized 
    to the population of the respective subgroup.  

    :primary[Relative incidence:] Incidence in a subgroup group divided by the sum of incidences across all subgroup.  
    
    :primary[Area plots] shown when overall incidence above adjustable cutoff (slider).
    with very low incidence values the relative incidence cannot be reliably estimated.
    """)



c0,c1 = st.columns([1,10], border=True)
with c0:
    st.text("Cutoff on incidence to draw area plots")
    ss.cutoff_obli = vertical_slider("", height=500,
        step = -0.1, 
        min_value=-0.1, max_value=10.0,
        default_value=ss.cutoff_obli, key="cutoff_slider",
        track_color = "#222222", slider_color = "#2198cf", thumb_color= "#2198cf", )
    # st.write(ss.cutoff_obli)
    ss.fig_all_oblig = draw_figures(ss.df_all, ss.df_age, ss.df_sex, ss.df_typ, cutoff = ss.cutoff_obli, 
        colo = [ss.colo_all_oblig, ss.colo_age_oblig , ss.colo_sex_oblig, ss.colo_typ_oblig])
    # plot the cutoff as a line 
    ss.fig_all_oblig.add_hline(y=ss.cutoff_obli, line_dash="dot", line_color="grey", line_width=1, row = 1)
  
with c1:
    st.plotly_chart(ss.fig_all_oblig,  use_container_width=True, theme=None, config={"displayModeBar": False}, key = "k001")

