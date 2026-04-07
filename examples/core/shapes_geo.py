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

# ---- shapes - compass points
Text(common=txt, text='Named "geo" points')
Blueprint(stroke_width=0.5)
sh = Rectangle(
    cx=1, cy=1, height=1, width=1.5,
    label="rectangle", label_size=6)
Dot(cxy=sh.geo.ne, fill_stroke="red")
Dot(cxy=sh.geo.se, fill_stroke="blue")
Dot(cxy=sh.geo.sw, fill_stroke="green")
Dot(cxy=sh.geo.nw, fill_stroke="yellow")
sh = Trapezoid(
    cx=3, cy=1, height=1, width=1.5,
    label="trapezoid", label_size=6)
Dot(cxy=sh.geo.ne, fill_stroke="red")
Dot(cxy=sh.geo.se, fill_stroke="blue")
Dot(cxy=sh.geo.sw, fill_stroke="green")
Dot(cxy=sh.geo.nw, fill_stroke="yellow")
sh = Rhombus(
    cx=1, cy=2.5, height=1, width=1.5,
    label="rhombus", label_size=6)
Dot(cxy=sh.geo.n, fill_stroke="red")
Dot(cxy=sh.geo.s, fill_stroke="blue")
Dot(cxy=sh.geo.e, fill_stroke="green")
Dot(cxy=sh.geo.w, fill_stroke="yellow")
sh = Cross(
    cx=3, cy=2.5, height=1, width=1.5,
    label="cross", label_size=6)
Dot(cxy=sh.geo.n, fill_stroke="red")
Dot(cxy=sh.geo.s, fill_stroke="blue")
Dot(cxy=sh.geo.e, fill_stroke="green")
Dot(cxy=sh.geo.w, fill_stroke="yellow")
sh = Stadium(
    cx=1, cy=4, height=1, width=1,
    label="stadium", label_size=6)
Dot(cxy=sh.geo.n, fill_stroke="red")
Dot(cxy=sh.geo.s, fill_stroke="blue")
Dot(cxy=sh.geo.e, fill_stroke="green")
Dot(cxy=sh.geo.w, fill_stroke="yellow")
sh = Star(
    cx=3, cy=4, radius=0.8, rays=5,
    label="star", label_size=6)
Dot(cxy=sh.geo.v[0], fill_stroke="red")
Dot(cxy=sh.geo.v[1], fill_stroke="blue")
Dot(cxy=sh.geo.v[2], fill_stroke="green")
Dot(cxy=sh.geo.v[3], fill_stroke="yellow")
Dot(cxy=sh.geo.v[4], fill_stroke="pink")
PageBreak()

# ---- polyshape/sector - geo points
Text(common=txt, text='Reuse of "geo" points')
Blueprint(stroke_width=0.5)
hx = Hexagon(
  x=0, y=0.85, height=2,
  fill="yellow",
  orientation="pointy")
Polyshape(
  points=[hx.geo.c, hx.geo.ne, hx.geo.se],
  fill="tomato")
cc = Circle(
  x=2, y=3, radius=0.9,
  fill="yellow")
Sector(
  cxy=cc.geo.c,
  radius=cc.geo.radius,
  angle_width=60,
  angle_start=-30,
  fill="tomato")
PageBreak()

# ---- polygon - numbered and named points
Text(common=txt, text='Polygon: "geo" points')
Blueprint(stroke_width=0.5)
# triangle
p1 = Polygon(x=1, y=1, sides=3, side=1.5)
Dot(cxy=p1.geo.n, fill_stroke="red")
Dot(cxy=p1.geo.se, fill_stroke="blue")
Dot(cxy=p1.geo.sw, fill_stroke="green")
p2 = Polygon(x=3, y=1, sides=3, side=1.5)
Dot(cxy=p2.geo.v[2], fill_stroke="red")
Dot(cxy=p2.geo.v[0], fill_stroke="blue")
Dot(cxy=p2.geo.v[1], fill_stroke="green")
# square
p1 = Polygon(x=1, y=3, sides=4, side=1.5)
Dot(cxy=p1.geo.ne, fill_stroke="red")
Dot(cxy=p1.geo.se, fill_stroke="blue")
Dot(cxy=p1.geo.sw, fill_stroke="green")
Dot(cxy=p1.geo.nw, fill_stroke="yellow")
p2 = Polygon(x=3, y=3, sides=4, side=1.5)
Dot(cxy=p2.geo.v[0], fill_stroke="red")
Dot(cxy=p2.geo.v[1], fill_stroke="blue")
Dot(cxy=p2.geo.v[2], fill_stroke="green")
Dot(cxy=p2.geo.v[3], fill_stroke="yellow")
# hexagon
p1 = Polygon(x=1, y=5, sides=6, side=0.8)
Dot(cxy=p1.geo.ne, fill_stroke="red")
Dot(cxy=p1.geo.e, fill_stroke="blue")
Dot(cxy=p1.geo.se, fill_stroke="green")
Dot(cxy=p1.geo.sw, fill_stroke="yellow")
Dot(cxy=p1.geo.w, fill_stroke="pink")
Dot(cxy=p1.geo.nw, fill_stroke="purple")
p2 = Polygon(x=3, y=5, sides=6, side=0.8)
Dot(cxy=p2.geo.v[0], fill_stroke="red")
Dot(cxy=p2.geo.v[1], fill_stroke="blue")
Dot(cxy=p2.geo.v[2], fill_stroke="green")
Dot(cxy=p2.geo.v[3], fill_stroke="yellow")
Dot(cxy=p2.geo.v[4], fill_stroke="pink")
Dot(cxy=p2.geo.v[5], fill_stroke="purple")
PageBreak()

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
        "shape_points_geo",
        "polygon_named",
        "geo_points_poly",
        "hex_vertices_perbii",
    ]
)
