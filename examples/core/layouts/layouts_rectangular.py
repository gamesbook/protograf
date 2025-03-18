# -*- coding: utf-8 -*-
"""
Virtual layout examples for protograf

Written by: Derek Hohls
Created on: 19 May 2024
"""
from protograf import *

Create(filename="layouts_basic_rectangular.pdf",
       paper="A8",
       margin=0.75,
       margin_right=0.2, margin_top=0.2,
       font_size=8,
       stroke_width=0.5)

header = Common(x=0, y=6, font_size=6, align="left")
a_circle = circle(
    x=0, y=0, diameter=1.0, label="{{sequence}}//{{col}}-{{row}}", label_size=6)

# ---- regular

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NW->south (2x3)")
rect = RectangularLocations(cols=2, rows=3, start="NW", direction="south")
Layout(rect, shapes=[circle(x=0, y=0, diameter=1)], debug='cr')
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NW->east")
rect = RectangularLocations(cols=3, rows=3, start="NW", direction="east")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NE->west")
rect = RectangularLocations(cols=3, rows=3, start="NE", direction="west")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NE->south")
rect = RectangularLocations(cols=3, rows=3, start="NE", direction="south")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: SE->north")
rect = RectangularLocations(cols=3, rows=3, start="SE", direction="north")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: SE->west")
rect = RectangularLocations(cols=3, rows=3, start="SE", direction="west")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: SW->north")
rect = RectangularLocations(cols=3, rows=3, start="SW", direction="north")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: SW->east")
rect = RectangularLocations(cols=3, rows=3, start="SW", direction="east")
Layout(rect, shapes=[a_circle,])
PageBreak()

# ---- snake

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NW->south: Snake")
rect = RectangularLocations(cols=3, rows=4, start="NW", direction="south", pattern="snake")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NW->east: Snake")
rect = RectangularLocations(cols=3, rows=4, start="NW", direction="east", pattern="snake")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NE->south: Snake")
rect = RectangularLocations(cols=3, rows=4, start="NE", direction="south", pattern="snake")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NE->west: Snake")
rect = RectangularLocations(cols=3, rows=4, start="NE", direction="west", pattern="snake")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: SE->north: Snake")
rect = RectangularLocations(cols=3, rows=4, start="SE", direction="north", pattern="snake")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: SE->west: Snake")
rect = RectangularLocations(cols=3, rows=4, start="SE", direction="west", pattern="snake")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: SW->north: Snake")
rect = RectangularLocations(cols=3, rows=4, start="SW", direction="north", pattern="snake")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: SW->east: Snake")
rect = RectangularLocations(cols=3, rows=4, start="SW", direction="east", pattern="snake")
Layout(rect, shapes=[a_circle,])
PageBreak()

# ---- outer

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NW->east: Outer")
rect = RectangularLocations(cols=3, rows=4, start="NW", direction="east", pattern="outer")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NW->south: Outer")
rect = RectangularLocations(cols=3, rows=4, start="NW", direction="south", pattern="outer")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NE->west: Outer")
rect = RectangularLocations(cols=3, rows=4, start="NE", direction="west", pattern="outer")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NE->south: Outer")
rect = RectangularLocations(cols=3, rows=4, start="NE", direction="south", pattern="outer")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: SE->north: Outer")
rect = RectangularLocations(cols=3, rows=4, start="SE", direction="north", pattern="outer")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: SE->west: Outer")
rect = RectangularLocations(cols=3, rows=4, start="SE", direction="west", pattern="outer")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: SW->east: Outer")
rect = RectangularLocations(cols=3, rows=4, start="SW", direction="east", pattern="outer")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: SW->north: Outer")
rect = RectangularLocations(cols=3, rows=4, start="SW", direction="north", pattern="outer")
Layout(rect, shapes=[a_circle,])
PageBreak()

Save(
    output='png',
    dpi=300,
    directory="../docs/source/images/layouts",
    names=[
        "rect_locs_reg_nw_S", "rect_locs_reg_nw_E",
        "rect_locs_reg_ne_W", "rect_locs_reg_ne_S",
        "rect_locs_reg_se_N", "rect_locs_reg_se_W",
        "rect_locs_reg_sw_N", "rect_locs_reg_sw_E",

        "rect_locs_snake_nw_S", "rect_locs_snake_nw_E",
        "rect_locs_snake_ne_S", "rect_locs_snake_ne_W",
        "rect_locs_snake_se_N", "rect_locs_snake_se_W",
        "rect_locs_snake_sw_N", "rect_locs_snake_sw_E",

        "rect_locs_outer_nw_E", "rect_locs_outer_nw_S",
        "rect_locs_outer_ne_W", "rect_locs_outer_ne_S",
        "rect_locs_outer_se_N", "rect_locs_outer_se_W",
        "rect_locs_outer_sw_E", "rect_locs_outer_sw_N",
    ]
)
