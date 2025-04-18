"""
Show customised BluePrint shape for protograf

Written by: Derek Hohls
Created on: 18 August 2024
"""

from protograf import *

Create(
    filename="customised_blueprint.pdf",
    paper="A8",
    margin_left=0.5,
    margin_right=0.3,
    margin_bottom=0.2,
    margin_top=0.5,
    font_size=8,
)

txt = Common(x=0, y=0, font_size=8, align="left")

Blueprint()
Text(common=txt, text="Blueprint:defaults")
PageBreak()

Blueprint(stroke_width=1, stroke="red")
Text(common=txt, text="Blueprint: stroke - red&width=1")
PageBreak()

Blueprint(style="invert")
Text(common=txt, text="Blueprint: style=blue")
PageBreak()

Blueprint(style="green")
Text(common=txt, text="Blueprint: style=green")
PageBreak()

Blueprint(style="gray")
Text(common=txt, text="Blueprint: style=gray")
PageBreak()

Blueprint(style="gray", stroke="purple")
Text(common=txt, text="Blueprint: gray; stroke=purple")
PageBreak()

Blueprint(subdivisions=4, stroke_width=1)
Text(common=txt, text="Blueprint: 4 subdivisions (dotted)")
PageBreak()

Blueprint(subdivisions=5, subdivisions_dashed=[0.08, 0.08], stroke_width=0.5)
Text(common=txt, text="Blueprint: 5 dashed subdivisions")
PageBreak()

Blueprint(decimals=1)
Text(common=txt, text="Blueprint: decimals")
PageBreak()

Blueprint(edges="n,s,e,w")
Text(common=txt, text="Blueprint: label all edges")
PageBreak()

Blueprint(edges="", edges_y=2, edges_x=2)
Text(common=txt, text="Blueprint: label x & y")

Save(
    output="png",
    dpi=300,
    directory="../docs/source/images/custom/blueprint",
    names=[
        "defaults",
        "stroke_width_red",
        "style_blue",
        "style_green",
        "style_gray",
        "style_stroke",
        "subdivisions",
        "subdivisions_dashed",
        "decimals",
        "edges",
        "edges_x_y",
    ],
)
