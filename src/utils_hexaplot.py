#--------------------             
# Author : Serge Zaugg
# Description : code related to the hexagonal/honeycomb plot
#--------------------

import streamlit as st
from streamlit import session_state as ss
import plotly.graph_objects as go
import math
import pandas as pd 
import plotly.colors

@st.cache_data
def get_mean_by_canton(x, resp_var):
    """ take cumsum """
    x = x[['date', 'georegion', resp_var]]
    x = x.groupby("georegion", as_index=False)[resp_var].mean()
    x = x.rename(columns={"value": resp_var})
    return(x)

@st.cache_data
def make_hexagon_plot(df_one_per_canton, resp_var, color_map, color_max_val):
    """ Map color-coded values to the honeycomb Switzerland (Hexagons) """
    tiles = [
        ("GE", 0, 0,),
        ("FR", 3, 2, ),
        ("JU", 2, 4, ),
        ("BS", 3, 6, ),

        ("VD", 2, 0, ),
        ("BE", 4, 0, ),
        ("SO", 4, 4, ),
        ("BL", 5, 6, ),

        ("VS", 3, -2, ),
        ("NE", 1, 2, ),
        ("LU", 5, 2, ),
        ("AG", 6, 4, ),
        ("ZH", 7, 6, ),

        ("OW", 8, 0, ),
        ("NW", 9, 2, ),
        ("SZ", 7, 2, ),
        ("ZG", 8, 4, ),
        ("SH", 8, 8, ),

        ("UR", 10, 0, ),
        ("AR", 11, 6, ),
        ("TG", 9, 6, ),

        ("TI", 11, -2, ),
        ("AI", 12, 4, ),
        ("SG", 10, 4, ),

        ("GL", 11, 2, ),
        ("GR", 12, 0, ),
    ]

    df_tiles = pd.DataFrame(tiles,columns=["georegion", "x", "y"])

    dfm = df_tiles.merge(df_one_per_canton, how = "left", on = ['georegion'])

    # prepare custom color map
    dfm["color"] = dfm[resp_var].apply(lambda x: plotly.colors.sample_colorscale(color_map, min(x / color_max_val, 1.0))[0])

    dfm[resp_var] = dfm[resp_var].round(2)

    
    R = 0.59

    fig = go.Figure()

    for i,r in dfm.iterrows():
        label = r.georegion
        cx    = r.x
        cy    = r.y
        color = r.color
        value = r[resp_var]

        angles = [math.radians(60 * i + 30) for i in range(6)]

        cx = cx * 0.56
        cy = cy * 0.48

        x = [cx + R * math.cos(a) for a in angles] 
        y = [cy + R * math.sin(a) for a in angles] 

        fig.add_trace(go.Scatter(
            x=x + [x[0]],
            y=y + [y[0]],
            mode="lines",
            fill="toself",
            fillcolor=color,
            line=dict(color="black", width=2),
            showlegend=False,
            hoverinfo="text",
            text=f"{label}: {value}",
        ))

        fig.add_annotation(
            x=cx, y=cy,
            text=f"{label}<br>{value}",
            showarrow=False,
            font=dict(color="black", size=14),
        )

    fig.update_layout(
        title=None,
        # width=650,
        height=360,
        xaxis=dict(visible=False, range=[-1.6, 8.3], scaleanchor="y", showline=True, linecolor="white", linewidth=2),
        yaxis=dict(visible=False, range=[-0.9, 3.1]),
        margin=dict(l=1, r=10, t=1, b=1)
    )

    # # add frame around figure 
    # fig.add_shape(
    #     type="rect",
    #     xref="paper", yref="paper",
    #     x0=0, y0=0, x1=1, y1=1,
    #     line=dict(color="white", width=1),
    #     fillcolor="rgba(0,0,0,0)",
    #     layer="above",
    # )

    # trick to add a colorbar 
    fig.add_trace(go.Scatter(
    x=[None], y=[None],
    mode="markers",
    marker=dict(
        color=[0],
        colorscale=color_map,
        cmin=0,
        cmax=color_max_val,
        showscale=True,
        colorbar=dict(
            title=resp_var,
            tickvals=[0, color_max_val],
            ticktext=["0", str(color_max_val)],
        ),
    ),
    showlegend=False,
    hoverinfo="skip",
    ))

    return fig




