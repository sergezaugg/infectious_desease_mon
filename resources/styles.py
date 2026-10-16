#--------------------             
# Author : Serge Zaugg
# Description : overall page styles (affects all pages) 
#--------------------

import streamlit as st

def apply_global_styles():
    """Apply global CSS styles to the Streamlit app."""

    # Reduce spacing around st.divider() 
    st.markdown("""
        <style>
            div[data-testid="stElementContainer"]:has([data-testid="stMarkdownContainer"] hr) {
                margin-top: -1.9rem !important;
                margin-bottom: -1.0rem !important;}
        </style>
        """, unsafe_allow_html=True)

    # space between main region and nav bar
    st.markdown("""
        <style>
            [data-testid="stMainBlockContainer"] {padding-top: 0rem; padding-left: 1.5rem;} /* here 
        </style>
        """, unsafe_allow_html=True)

    # reduce height of nav bar 
    st.markdown("""
    <style>
        [data-testid="stHeader"] {
            height: 4rem; 
            min-height: 4rem}
    </style>
    """, unsafe_allow_html=True)

    # change color of navigation bar background and tabs          
    st.markdown("""
        <style>
        /* Header background */
        .stAppHeader {background-color: #0E1117;}

        /* Default tab background */
        .stAppHeader a {background-color: #000000 !important;}

        /* Hover state */
        .stAppHeader a:hover {background-color: #3b4d63 !important;}

        /* click state */
        .stAppHeader a:active {background-color: #dddddd !important; }

        /* Active page */
        .stAppHeader a[aria-current="page"] {background-color: #176c93 !important;}

        /* Bouton borders  */
        .stAppHeader a {
            border: 1px solid rgba(255, 255, 255, 0.75);
            margin: 2px 4px;
            padding: 4px 10px;
        }

        </style>
    """, unsafe_allow_html=True)


   


    # All navigation tabs: same fixed width
    st.markdown("""
    <style>
        .stAppHeader a {
            width: 100px !important;
            min-width: 100px !important;
            max-width: 100px !important;
            box-sizing: border-box !important;
            justify-content: center !important;
            text-align: center !important;
            white-space: nowrap !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # text right to logo 
    st.markdown("""
    <style>
        .app-label {
            position: fixed;
            top:  17px;
            left: 60px;
            color: #9CA3AF;
            font-size: 15px;
            z-index: 999999;
            pointer-events: none;
        }
    </style>
    <div class="app-label">CH-FLU-Explorer v1.2.0-β</div>
    """, unsafe_allow_html=True)


    
    st.markdown("""
    <style>
    /* Outer frame around the entire app */
    body::after {
    content: "";
    position: fixed;
    inset: 4px;
    border: 1px solid rgba(255, 255, 255, 0.6);
    pointer-events: none;
    z-index: 999999;
    }

    /* Separator below navigation */
    [data-testid="stHeader"] {
    border-bottom: 1px solid rgba(255, 255, 255, 0.6);
    }

    /* Separator beside sidebar */
    [data-testid="stSidebar"] {
    border-right: 1px solid rgba(255, 255, 255, 0.6);
    }
    </style>
    """, unsafe_allow_html=True)