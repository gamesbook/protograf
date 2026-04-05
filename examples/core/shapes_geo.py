"""
Show use of Shapes' "geo" property for protograf

Written by: Derek Hohls
Created on: 2 Apr 2026
"""
from protograf import *

Create(
    filename="shapes_geo.pdf",
    paper="A8",
    margin=0.5,
    font_size=8,
    stroke_width=0.5,
)

txt = Common(x=0, y=0, font_size=8, align="left")

# ---- hexagon - vertices and perbii points
Text(common=txt, text='Hexagon: "geo" points')
Blueprint(stroke_width=0.5)
Image("compass.png", x=0, y=0.1, height=2, width=2)
hx = Hexagon(x=-0.15, y=0.1, height=2, fill=None, stroke_width=1)
Dot(cxy=hx.geo.ne, fill_stroke="red")
Dot(cxy=hx.geo.e, fill_stroke="blue")
Dot(cxy=hx.geo.se, fill_stroke="green")
Dot(cxy=hx.geo.sw, fill_stroke="yellow")
Dot(cxy=hx.geo.w, fill_stroke="pink")
Dot(cxy=hx.geo.nw, fill_stroke="purple")

Image("compass.png", x=2, y=1.1, height=2, width=2)
hx = Hexagon(x=1.85, y=1.1, height=2, fill=None, stroke_width=1)
Dot(cxy=hx.geo.ene, fill_stroke="red")
Dot(cxy=hx.geo.ese, fill_stroke="blue")
Dot(cxy=hx.geo.s, fill_stroke="green")
Dot(cxy=hx.geo.wsw, fill_stroke="yellow")
Dot(cxy=hx.geo.wnw, fill_stroke="pink")
Dot(cxy=hx.geo.n, fill_stroke="purple")

Image("compass.png", x=0, y=3, height=2, width=2)
hx = Hexagon(x=0, y=2.85, height=2, fill=None, stroke_width=1, orientation="pointy")
Dot(cxy=hx.geo.ne, fill_stroke="red")
Dot(cxy=hx.geo.se, fill_stroke="blue")
Dot(cxy=hx.geo.s, fill_stroke="green")
Dot(cxy=hx.geo.sw, fill_stroke="yellow")
Dot(cxy=hx.geo.nw, fill_stroke="pink")
Dot(cxy=hx.geo.n, fill_stroke="purple")

Image("compass.png", x=2.1, y=3.8, height=2, width=2)
hx = Hexagon(x=2.1, y=3.65, height=2, fill=None, stroke_width=1, orientation="pointy")
Dot(cxy=hx.geo.nne, fill_stroke="red")
Dot(cxy=hx.geo.e, fill_stroke="blue")
Dot(cxy=hx.geo.sse, fill_stroke="green")
Dot(cxy=hx.geo.ssw, fill_stroke="yellow")
Dot(cxy=hx.geo.w, fill_stroke="pink")
Dot(cxy=hx.geo.nnw, fill_stroke="purple")

Save(
    output='png',
    dpi=300,
    directory="../docs/source/images/custom/geo",
    names=[
        "hex_vertices_perbii",
    ]
)
