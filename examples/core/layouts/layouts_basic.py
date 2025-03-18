# -*- coding: utf-8 -*-
"""
Virtual layout examples for protograf

Written by: Derek Hohls
Created on: 19 May 2024
"""
from protograf import *

Create(filename="layouts_basic.pdf",
       paper="A8",
       margin=0.75,
       margin_right=0.2, margin_top=0.2,
       font_size=10,
       stroke_width=0.5)

header = Common(x=0, y=6, font_size=7, align="left")
a_circle = circle(
    x=0, y=0, diameter=1.0, label="{{sequence}}//{{col}}-{{row}}", label_size=6)

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: debug > no label")
rect = RectangularLocations(cols=3, rows=4, x=0.5, y=0.5)
Layout(rect, debug='none')
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rec.Locations: debug > sequence")
rect = RectangularLocations(cols=3, rows=4, x=0.5, y=0.5)
Layout(rect, debug='sequence')
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rec.Locations: debug > x;y")
rect = RectangularLocations(cols=3, rows=4, x=0.5, y=0.5)
Layout(rect, debug='xy')
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rec.Locations: debug > col;row")
rect = RectangularLocations(cols=3, rows=4, x=0.5, y=0.5)
Layout(rect, debug='colrow')
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: default")
rect = RectangularLocations(cols=3, rows=4)
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NW->east")
rect = RectangularLocations(cols=3, rows=4, start="NW", direction="east")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NW/east: even col shift")
rect = RectangularLocations(cols=3, rows=4, start="NW", direction="east", col_even=0.5)
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NW/east: odd row shift")
rect = RectangularLocations(cols=3, rows=4, start="NW", direction="east", row_odd=-0.5)
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NW/east: snake")
rect = RectangularLocations(cols=3, rows=4, start="NW", direction="east", pattern="snake")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NW/east: Outer")
rect = RectangularLocations(cols=3, rows=4, start="NW", direction="east", pattern="outer")
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NW/east: Outer+Masked")
rect = RectangularLocations(cols=3, rows=4, start="NW", direction="east", pattern="outer")
Layout(rect, shapes=[a_circle], masked=[2,7])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NW/east: Outer+Visible")
rect = RectangularLocations(cols=3, rows=4, start="NW", direction="east", pattern="outer")
Layout(rect, shapes=[a_circle], visible=[1,3,6,8])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NW->east: interval")
rect = RectangularLocations(cols=3, rows=4, start="NW", direction="east",
                            interval=1.25)
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NW->east: interval x&y")
rect = RectangularLocations(cols=3, rows=4, start="NW", direction="east",
                            x=1.5, y=1.5, interval_x=0.75, interval_y=1.25)
Layout(rect, shapes=[a_circle,])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: shapes & locations")
rect = RectangularLocations(
    cols=3, rows=4)
Layout(
  rect,
  shapes=[a_circle, rectangle(label="{{sequence}}//{{col}}-{{row}}", label_size=6)],
  locations=[(1,2), (2,3), (3,1), (1,1), (3,4)])

# Save()
Save(
     output='png',
     dpi=300,
     directory="../docs/source/images/layouts",
     names=[
        "rect_basic_debug", "rect_basic_debug_sequence", "rect_basic_debug_xy",
        "rect_basic_debug_colrow",
        "rect_basic_default",
        "rect_basic_east", "rect_basic_east_even",  "rect_basic_east_odd",
        "rect_basic_snake",
        "rect_basic_outer", "rect_basic_outer_mask", "rect_basic_outer_visible",
        "rect_basic_interval", "rect_basic_interval_row_col",
        "rect_basic_locations",
     ]
)
