#--------------------             
# Author : Serge Zaugg
# Description : Plots and UI elements used my the streamlit app
#--------------------

import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit as st
from streamlit import session_state as ss

#---------------------------------
# (0) general function  

def update_ss(kname, ssname):
    """
    description : helper callback function to implement stateful apps
    kname : key name of widget
    ssname : key name of variable in session state (ss)
    """
    ss["upar"][ssname] = ss[kname]      


# -----------------------------------------
# (3) function to pre-render plotly figures


@st.cache_data
def make_line_plot_with_vref(df, y_title, height):
    fig = px.line(
        data_frame = df, 
        height = height,
        x = 'date', 
        y = 'incValue', 
        markers=False, 
        template="plotly_dark", 
        color_discrete_sequence = ["#F25B10"]
        )
    _ = fig.update_xaxes(showline=True, linewidth=1, linecolor='white', mirror=True)
    _ = fig.update_yaxes(showline=True, linewidth=1, linecolor='white', mirror=True)
    _ = fig.update_layout(xaxis_title='Date', yaxis_title=y_title)
    _ = fig.update_layout(paper_bgcolor="#000000") # "#350030"
    _ = fig.update_layout(margin=dict(l=7, r=7, t=1, b=1))
    _ = fig.update_layout(xaxis_title_font_size=15)
    _ = fig.update_layout(yaxis_title_font_size=15)
    _ = fig.update_layout(xaxis_tickfont_size=15)
    _ = fig.update_layout(legend_font_size=20)
    _ = fig.update_layout(xaxis_title=None)
    _ = fig.update_layout(yaxis_title=None)
    _ = fig.update_yaxes(showticklabels=False)
    _ =fig.update_xaxes(showgrid=False)
    _ =fig.update_yaxes(showgrid=False)
    return(fig)



@st.cache_data
def make_line_plot(df, color_groups, color_sequence, y_title, height):
    fig = px.line(
        data_frame = df, 
        color = color_groups, 
        height = height,
        x = 'date', 
        y = 'incValue', 
        markers=False, 
        template="plotly_dark", 
        color_discrete_sequence = color_sequence,
        )
    _ = fig.update_xaxes(showline=True, linewidth=2, linecolor='white', mirror=True)
    _ = fig.update_yaxes(showline=True, linewidth=2, linecolor='white', mirror=True)
    _ = fig.update_layout(xaxis_title='Date', yaxis_title=y_title)
    _ = fig.update_layout(paper_bgcolor="#000000") # "#350030"
    _ = fig.update_layout(margin=dict(l=1, r=200, t=10, b=1))
    _ = fig.update_layout(xaxis_title_font_size=15)
    _ = fig.update_layout(yaxis_title_font_size=15)
    _ = fig.update_layout(xaxis_tickfont_size=15)
    _ = fig.update_layout(legend_font_size=20)
    _ = fig.update_layout(xaxis_title=None)
    return(fig)

@st.cache_data
def make_area_plot(df, color_groups, color_sequence, y_title, cutoff, height = 260):
    # set area plot to nan whe overall incidence was too low
    df = df.copy() # to avoid orig df in ss to be cut !
    # quick fix
    df.loc[df["incValue_all"] < cutoff, "incValue"] = np.nan

    fig = px.area(
        groupnorm = 'fraction',
        data_frame = df, 
        color = color_groups, 
        height = height,
        x = 'date', 
        y = 'incValue', 
        template="plotly_dark", 
        color_discrete_sequence = color_sequence,
        markers = False,
        line_shape = 'hvh', # 'hvh',#'spline', One of 'linear', 'spline', 'hv', 'vh', 'hvh', or 'vhv'
        )
    _ = fig.update_xaxes(showline=True, linewidth=2, linecolor='white', mirror=True)
    _ = fig.update_yaxes(showline=True, linewidth=2, linecolor='white', mirror=True)
    _ = fig.update_layout(xaxis_title='Date', yaxis_title=y_title)
    _ = fig.update_layout(paper_bgcolor="#000000") # "#350030"
    _ = fig.update_layout(margin=dict(l=1, r=200, t=10, b=1))
    _ = fig.update_layout(xaxis_title_font_size=15)
    _ = fig.update_layout(yaxis_title_font_size=15)
    _ = fig.update_layout(xaxis_tickfont_size=15)
    _ = fig.update_layout(legend_font_size=20)
    _ = fig.update_layout(xaxis_title=None)
    _ = fig.update_traces(line=dict(width=0.2))
    _ = fig.update_layout(yaxis_range=[0.0,1.0])
    _ = fig.for_each_trace(lambda trace: trace.update(fillcolor = trace.line.color))
    return(fig)

@st.cache_data
def draw_figures(df_all,df_age, df_sex, df_typ, cutoff, colo):
    # lineplots 
    # fig_lin = make_line_plot(df_all, 'georegion', ss.colo_all_oblig, height = 800,
    fig_lin = make_line_plot(df_all, 'georegion', colo[0], height = 800,
                             y_title = 'Cases per 100000 inhab')
    # area plots
    fig_age = make_area_plot(df_age, 'agegroup',  colo[1], height = 400,
                             y_title = 'Relative incidence', cutoff = cutoff)
    
    fig_sex = make_area_plot(df_sex, 'sex',       colo[2], height = 400,
                             y_title = 'Relative incidence', cutoff = cutoff)
    
    fig_typ = make_area_plot(df_typ, 'type',      colo[3], height = 400,
                             y_title = 'Relative incidence', cutoff = cutoff)

    fig = make_subplots(rows=4, cols=1, shared_xaxes=True, row_heights=[0.3, 0.2, 0.2, 0.2],  vertical_spacing=0.05)

    for trace in fig_lin.data:
        # trace.legend = "legend1"
        fig.add_trace(trace, row=1, col=1)

    for trace in fig_age.data:
        trace.legend = "legend2"
        fig.add_trace(trace, row=2, col=1)

    for trace in fig_sex.data:
        trace.legend = "legend3"
        fig.add_trace(trace, row=3, col=1)

    for trace in fig_typ.data:
        trace.legend = "legend4"
        fig.add_trace(trace, row=4, col=1)

    fig.update_layout(
    # legend1=dict(orientation="v",x=1.02, y=0.70, xanchor="left", yanchor="bottom",),
    legend2=dict(orientation="v",x=1.02, y=0.45, xanchor="left", yanchor="bottom",),
    legend3=dict(orientation="v",x=1.02, y=0.25, xanchor="left", yanchor="bottom",),
    legend4=dict(orientation="v",x=1.02, y=0.0,  xanchor="left", yanchor="bottom",),
    )    



    fig.update_layout(margin=dict(l=30, r=35, t=1, b=30))
    fig.update_layout(height=700)
    fig.update_xaxes(matches="x")
    fig.update_layout(hovermode="x unified")
    fig.update_xaxes(showline = True, linewidth=0.8, mirror=True)
    fig.update_yaxes(showline = True, linewidth=0.8, mirror=True)
    fig.update_yaxes(range=[0.0, 1.00], row=2, col=1)
    fig.update_yaxes(range=[0.0, 1.00], row=3, col=1)
    fig.update_yaxes(range=[0.0, 1.00], row=4, col=1)
    # fig.update_layout(legend=dict(orientation="h", x=0, xanchor="left", y=1.2, yanchor="top",))    
    return(fig) 













