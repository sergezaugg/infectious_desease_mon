#--------------------             
# Author : Serge Zaugg
# Description : incidence map where each canton has same size 
#--------------------

import streamlit as st
from streamlit import session_state as ss
import plotly.graph_objects as go
import math
import pandas as pd 
import plotly.colors




tiles = [
    ("GE", 0, 0,),
    ("NE", 1, 2, ),
    ("JU", 2, 4, ),
    ("BS", 3, 6, ),

    ("VD", 2, 0, ),
    ("BE", 3, 2, ),
    ("SO", 4, 4, ),
    ("BL", 5, 6, ),

    ("VS", 3, -2, ),
    ("FR", 4, 0, ),
    ("LU", 5, 2, ),
    ("AG", 6, 4, ),
    ("ZH", 7, 6, ),

    ("OW", 5, -2, ),
    ("NW", 6, 0, ),
    ("SZ", 7, 2, ),
    ("ZG", 8, 4, ),
    ("SH", 9, 6, ),

    ("UR", 8, 0, ),
    ("AR", 9, 2, ),
    ("TG", 10, 4, ),

    ("TI", 9, -2, ),
    ("AI", 10, 0, ),
    ("SG", 11, 2, ),

    ("GL", 12, 0, ),
    ("GR", 13, 2, ),
]

df_tiles = pd.DataFrame(tiles,columns=["georegion", "x", "y"])

# st.write(ss.df_can)



opt_dates = sorted(ss.df_can['date'].unique())

date_selected = st.select_slider(
    "Select date",
    options=opt_dates,
    value=opt_dates[-1],
    format_func=lambda d: d.strftime("%Y-%m-%d"),
)




#-------------------------------------------------
# data prep

# resp_var = 'incValue'
resp_var = 'value'
# resp_var = 'pop'





dfplot = ss.df_can[['date', 'georegion', resp_var]]




df_latest = dfplot[dfplot['date']==date_selected]
# df_latest = dfplot.loc[dfplot.groupby("georegion")["date"].idxmax()]

dfm = df_tiles.merge(df_latest, how = "left", on = ['georegion'])

max_val = ss.df_can[resp_var].max()
# max_val = dfm[resp_var].max()
max_val = 50

color_map = "RdYlGn_r"
color_map = "bluered"

dfm["color"] = dfm[resp_var].apply(lambda x: plotly.colors.sample_colorscale(color_map, x / max_val)[0])
dfm["color"] = dfm[resp_var].apply(lambda x: plotly.colors.sample_colorscale(color_map, min(x / max_val, 1))[0])




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
    width=1000,
    height=800,
    xaxis=dict(visible=False, range=[-1, 8.5], scaleanchor="y", showline=True, linecolor="white", linewidth=2),
    yaxis=dict(visible=False, range=[-2, 4]),
)

fig.add_shape(
    type="rect",
    xref="paper", yref="paper",
    x0=0, y0=0, x1=1, y1=1,
    line=dict(color="white", width=2),
    fillcolor="rgba(0,0,0,0)",
    layer="above",
)


st.plotly_chart(fig,  use_container_width=False, theme=None, )



st.dataframe(dfm)




