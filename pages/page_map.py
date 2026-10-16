


import streamlit as st
from streamlit import session_state as ss
import plotly.graph_objects as go
import math


tiles = [
    ("GE", 0, 0, "red", 120),
    ("NE", 1, 2, "orange", 80),
    ("JU", 2, 4, "lightblue", 40),
    ("BS", 3, 6, "lightblue", 40),

    ("VD", 2, 0, "lightblue", 40),
    ("BE", 3, 2, "lightblue", 40),
    ("SO", 4, 4, "lightblue", 40),
    ("BL", 5, 6, "lightblue", 40),

    ("VS", 3, -2, "lightblue", 40),
    ("FR", 4, 0, "lightblue", 40),
    ("LU", 5, 2, "lightblue", 40),
    ("AG", 6, 4, "lightblue", 40),
    ("ZH", 7, 6, "lightblue", 40),

    ("OW", 5, -2, "lightblue", 40),
    ("NW", 6, 0, "lightblue", 40),
    ("SZ", 7, 2, "lightblue", 40),
    ("ZG", 8, 4, "lightblue", 40),
    ("SH", 9, 6, "lightblue", 40),

    ("UR", 8, 0, "lightblue", 40),
    ("AR", 9, 2, "lightblue", 40),
    ("TG", 10, 4, "lightblue", 40),

    ("TI", 9, -2, "lightblue", 40),
    ("AI", 10, 0, "lightblue", 40),
    ("SG", 11, 2, "lightblue", 40),

    ("GL", 12, 0, "lightblue", 40),
    ("GR", 13, 2, "lightblue", 40),
    
]




R = 0.60

fig = go.Figure()


for label, cx, cy, color, value in tiles:
    angles = [math.radians(60 * i + 30) for i in range(6)]

    cx = cx* 0.56
    cy = cy* 0.48

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
    title="hexagon",
    width=1000,
    height=800,
    xaxis=dict(visible=False, range=[-1, 7], scaleanchor="y"),
    yaxis=dict(visible=False, range=[-2, 5]),
)

# fig.show()

st.plotly_chart(fig,  use_container_width=False, theme=None, )





