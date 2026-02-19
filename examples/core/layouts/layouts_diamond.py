# -*- coding: utf-8 -*-
"""
Virtual layout examples for protograf

Written by: Derek Hohls
Created on: 14 February 2026
"""
from protograf import *

Create(filename="layouts_basic_diamond.pdf",
       paper="A8",
       margin_left=0.5,
       margin_right=0.3,
       margin_bottom=0.2,
       margin_top=0.5,
       font_size=8,
       stroke_width=0.5)

header = Common(x=0, y=0, font_size=8, align="left")
d_circle = circle(radius=0.33)
a_circle = circle(
    x=0, y=0, diameter=1.0,
    label="{{sequence}}//{{col}}-{{row}}",
    label_size=6)

# ---- all defaults

Blueprint(stroke_width=0.5)
Text(common=header, text="DiamondLocations: default/debug")
dia = DiamondLocations()
Layout(dia, shapes=[d_circle,], debug='cr')
PageBreak()

# ---- facing

Blueprint(stroke_width=0.5)
Text(common=header, text="Dia.Locations: east/3 cols; debug")
dia = DiamondLocations(facing='east', y=3, x=3, side=.66, cols=3)
Layout(dia, shapes=[d_circle,], debug='cr')
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Dia.Locations: west/5 rows; debug")
dia = DiamondLocations(facing='west', y=3, x=1, side=.66, rows=5)
Layout(dia, shapes=[d_circle,], debug='cr')
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Dia.Locations: north/3 cols; debug")
dia = DiamondLocations(facing='north', y=2, x=2, side=.66, cols=3)
Layout(dia, shapes=[d_circle,], debug='cr')
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Dia.Locations: south/5 rows; debug")
dia = DiamondLocations(facing='south', y=4, x=2, side=.66, rows=5)
Layout(dia, shapes=[d_circle,], debug='cr')
PageBreak()

# ---- layout with filled shape

red_circle = circle(radius=0.33, fill="tomato")
gold_circle = circle(radius=0.33, fill="gold")

Blueprint(stroke_width=0.5)
Text(common=header, text="Dia.Locations: north; locations")
dia = DiamondLocations(facing='north', y=2, x=2, side=.66, cols=7)
Layout(dia, shapes=[gold_circle,])
Layout(dia, locations=[(3,2), (5,2), (3,6), (5,6)], shapes=[red_circle], debug='cr')
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Dia.Locations: north; cols")
dia = DiamondLocations(facing='north', y=2, x=2, side=.66, cols=7)
Layout(dia, shapes=[gold_circle])
Layout(dia, cols=[1,2,6,7], shapes=[red_circle], debug='c')
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Dia.Locations: north; rows")
dia = DiamondLocations(facing='north', y=2, x=2, side=.66, cols=7)
Layout(dia, shapes=[gold_circle])
Layout(dia, rows=[1,2,6,7], shapes=[red_circle], debug='r')
PageBreak()


# ---- layout with grid line & fill

small_circle = circle(radius=0.2, fill="tomato")

Blueprint(stroke_width=0.5)
Text(common=header, text="Dia.Locations: gridlines; NE")
dia = DiamondLocations(facing='north', y=2, x=2, side=.66, cols=7)
Layout(
   dia,
   gridlines='ne',
   gridlines_stroke="gold",
   gridlines_stroke_width=2,
   shapes=[small_circle])
PageBreak()


Blueprint(stroke_width=0.5)
Text(common=header, text="Dia.Locations: gridlines; fill")
dia = DiamondLocations(facing='north', y=2, x=2, side=.66, cols=7)
Layout(
   dia,
   gridlines='*',
   gridlines_fill="aqua",
   gridlines_stroke="gold",
   gridlines_stroke_width=2,
   shapes=[small_circle])
PageBreak()


Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: gridlines")
rct = RectangularLocations(cols=3, rows=5, start="NE", direction="west")
Layout(
   rct,
   gridlines='*',
   gridlines_fill="aqua",
   gridlines_stroke="gold",
   gridlines_stroke_width=2,
   shapes=[small_circle])


Save(
    output='png',
    dpi=300,
    directory="../docs/source/images/layouts",
    names=[
       "layout_dia_default",
       "layout_dia_east_col3",
       "layout_dia_west_row5",
       "layout_dia_north_col3",
       "layout_dia_south_row5",
       "layout_dia_shape_locs",
       "layout_dia_shape_cols",
       "layout_dia_shape_rows",
       "layout_dia_gridlines_ne",
       "layout_dia_gridlines_fill",
       "layout_TEST"
    ]
)
