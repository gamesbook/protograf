# -*- coding: utf-8 -*-
"""
An overview of protograf capabilities

Written by: Derek Hohls
Created on: 29 November 2025
Notes:
    Chess font from: http://www.enpassant.dk/chess/fontimg/alpha.htm
"""
from protograf import *

Create(
   filename="overview.pdf", margin=1, page_grid=2)

txt = Default(x=5, font_size=19, align="left")

# ---- title
Image("protograf_slogan.png", x=3.5, y=8, height=3.6, width=12)
Text('A Brief Tour...', font_size=48, x=9.5, y=15)
PageBreak()

# ---- base
Rectangle()
Text('Rectangle()', default=txt)
PageBreak()

# ---- styled
Rectangle(width=3, height=4)
Text('Rectangle(\n width=3, height=4)', default=txt, y=1)
Rectangle(y=6, width=3, height=4, fill="yellow", stroke="red", stroke_width=4)
Text('Rectangle(\n y=6, \n width=3, height=4,\n fill="yellow", stroke="red",\n stroke_width=4)', default=txt, y=6)
Rectangle(y=11, width=3, height=4, label="Hi!")
Text('Rectangle(\n y=11, \n width=3, height=4,\n label="Hi!")', default=txt, y=11)
Rectangle(y=16, width=3, height=4, hatches_count=5)
Text('Rectangle(\n y=16, \n width=3, height=4,\n hatches_count=5)', default=txt, y=16)
Rectangle(y=21, width=3, height=4, notch_style='bite', notch=0.5,
          # radii_shapes=[('*', dot())]
          radii_shapes=[('*', dot())],
          )
Text('Rectangle(\n y=21, \n width=3, height=4,\n notch=0.5, notch_style="bite",\n radii_shapes=[("*", dot())]', default=txt, y=21)
PageBreak()

# ---- filled shapes
shp = Default(title_stroke="black", title_size=18)
Arrow(x=3, y=27,  height=2, width=1,
      title="Arrow", default=shp, fill_stroke="plum")
Cross(cx=9, cy=26, height=3, width=3, thickness=1,
      title="Cross", default=shp, fill_stroke="plum")
Sector(cx=16, cy=27, radius=3, angle_start=68, angle_width=44,
      title="Sector", default=shp, fill_stroke="plum")
Pod(cx=3, cy=21, length=5, dx=2,
    title="Pod", default=shp, fill_stroke="tomato")
Ellipse(cx=9, cy=21, width=5, height=3,
        title="Ellipse", default=shp, fill_stroke="tomato")
Stadium(cx=16, cy=21, width=3, height=2,
        title="Stadium", default=shp, fill_stroke="tomato")
Hexagon(cx=3, cy=15, side=2, orientation="flat",
        title="Hexagon", default=shp, fill_stroke="gold")
Triangle(
    cx=9, cy=15, side=4,
    title="Triangle", default=shp, fill_stroke="gold")
Trapezoid(cx=16, cy=15, width=4, top=2, height=3,
          title="Trapezoid", default=shp, fill_stroke="gold")
Hexagon(cx=3, cy=9, side=2, orientation="pointy",
        title="Hexagon", default=shp, fill_stroke="chartreuse")
Polygon(cx=9, cy=9, radius=2, sides=8,
        title="Polygon", default=shp, fill_stroke="chartreuse")
Circle(cx=16, cy=9, radius=2,
       title="Circle", default=shp, fill_stroke="chartreuse")
Star(cx=3, cy=3, vertices=5, radius=2,
     title="Star", default=shp, fill_stroke="cyan")
Rhombus(cx=16, cy=3, width=3, height=5,
        title="Rhombus", default=shp, fill_stroke="cyan")
Square(cx=9, cy=3, side=3,
       title="Square", default=shp, fill_stroke="cyan")
Dot(cx=9, cy=0, dot_width=12, title="Dot", default=shp, fill_stroke="red")
PageBreak()

# ---- Go board
Grid(
    cols=18, rows=18,
    stroke_width=1
)
DotGrid(
    offset_x=4, offset_y=4,
    side=6,
    cols=3, rows=3,
    dot_width=8
)
Text("""Grid(
    cols=18, rows=18,
    stroke_width=1
)""", default=txt, x=2, y=20)
Text("""DotGrid(
    cols=3, rows=3,
    offset_x=4, offset_y=4,
    side=6,
    dot_width=8
)""", default=txt, x=10, y=20)
PageBreak()


Save()
