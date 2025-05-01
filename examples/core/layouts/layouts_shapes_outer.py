# -*- coding: utf-8 -*-
"""
Examples of multiple shapes on outer edge of RectangularLocations for protograf

Written by: Derek Hohls
Created on: 15 September 2024
"""
from protograf import *

Create(filename="layouts_shapes_outer.pdf",
       paper="A8",
       margin_left=0.5,
       margin_right=0.3,
       margin_bottom=0.2,
       margin_top=0.5,
       font_size=8,
       stroke_width=0.5)

header = Common(x=0, y=0, font_size=6, align="left")
is_common = Common(label="{{sequence}}")
rct_common = Common(label_size=5, points=[('s', 0.1)], height=0.5, width=0.5)

# ---- multi-shapes - layout_rect_outer_multi

sqr = square(common=is_common, side=0.9, label_size=6)
sqr5 = square(common=is_common, side=1.0, label_size=8, fill="yellow")

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: SW->north/outer + sequence")
rect = RectangularLocations(
    x=0.5, y=0.5, cols=4, rows=6, interval=1,
    start="SW", direction="north", pattern="outer")
Layout(rect, shapes=[sqr]*4 + [sqr5] )
PageBreak()

# ---- single shape + multi-color + stop - layout_rect_outer_multi_stop

rct_small = Common(label_size=5, side=0.48)
rct1 = square(common=rct_small, fill_stroke="palegreen")
rct5 = square(common=rct_small, fill_stroke="lightgreen")
rct10 = square(common=rct_small, fill_stroke="mediumseagreen")

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: NW->east/outer + stop")
rect = RectangularLocations(
    x=0.25, y=0.25, cols=8, rows=11, interval=0.5, stop=26,
    start="NW", direction="east", pattern="outer")
Layout(rect, shapes=[rct1]*4 + [rct5] + [rct1]*4 + [rct10])
PageBreak()

# ---- rotations + corners - layout_rect_outer_rotation

circ = circle(
    label="{{sequence - 1}}", label_size=5, radius=0.26, fill="rosybrown")
rct2 = rectangle(
    common=rct_common, label="{{sequence - 1}}", fill="tan")
rct3 = rectangle(
    common=rct_common, label="{{sequence - 1}}",
    fill="maroon", stroke="rosybrown")

Blueprint(stroke_width=0.5)
Text(common=header, text="Rect.Locations: SW/outer + rotate + corner")
rrect = RectangularLocations(
    x=0.5, y=0.75, cols=7, rows=10, interval=0.5,
    start="SW", direction="north", pattern="outer")
Layout(
    rrect,
    shapes=[rct3] + [rct2]*4,
    rotations=[
        ("1", 135), ("2-9", 90),
        ("10", 45),
        ("16", -45), ("17-24", 270),
        ("25", 225), ("26-30", 180),],
    corners=[('*',circ)])

#Save()
Save(
     output='png',
     dpi=300,
     directory="../docs/source/images/layouts",
     names=[
        "layout_rect_outer_multi",
        "layout_rect_outer_multi_stop",
        "layout_rect_outer_rotation",
     ]
)
