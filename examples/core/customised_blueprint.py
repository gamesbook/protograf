"""
Show customised BluePrint shape for protograf

Written by: Derek Hohls
Created on: 18 August 2024
"""

from protograf import *

Create(filename="customised_blueprint.pdf",
       paper=A8,
       margin_top=0.2,
       margin_left=0.75,
       margin_bottom=0.75,
       margin_right=0.2,
       font_size=8)

txt = Common(x=0, y=6, font_size=8, align="left")

Blueprint()
Text(common=txt, text="Blueprint:defaults")
PageBreak()

Blueprint(stroke_width=1, stroke=red)
Text(common=txt, text="Blueprint: stroke-red; width=1")
PageBreak()

Blueprint(style='invert')
Text(common=txt, text="Blueprint: style=blue")
PageBreak()

Blueprint(style='green')
Text(common=txt, text="Blueprint: style=green")
PageBreak()

Blueprint(style='grey')
Text(common=txt, text="Blueprint: style=grey")
PageBreak()

Blueprint(style='grey', stroke=purple)
Text(common=txt, text="Blueprint: grey; stroke=purple")
PageBreak()

Blueprint(subdivisions=4, stroke_width=.5)
Text(common=txt, text="Blueprint: 4 subdivisions (dotted)")
PageBreak()

Blueprint(subdivisions=5, subdivisions_dashed=[0.01, 0.01, 0], stroke_width=.5)
Text(common=txt, text="Blueprint: 5 dashed subdivisions")
PageBreak()

Blueprint(decimals=1)
Text(common=txt, text="Blueprint: decimals")
PageBreak()

Save(
     output='png',
     dpi=300,
     directory="../docs/source/images/custom/blueprint",
     names=[
        "defaults", "stroke_width_red",
        "style_blue", "style_green", "style_grey",
        "style_stroke", "subdivisions", "subdivisions_dashed",
        "decimals"
     ])
