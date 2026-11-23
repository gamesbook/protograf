# -*- coding: utf-8 -*-
"""
Example code for protograf XX18 command

Written by: Derek Hohls
Created on: 22 November 2026
"""
from protograf import *

Create(
    filename="xx18_market.pdf",
    paper="A5-l",
    margin=1,
    page_grid=1)

header = Common(x=0, y=0, font_size=18, align="left")
footer = Common(x=0, y=19.5, font_size=18, align="left")

# ---- XX18Market
Text("XX18Market: Default", common=header)
xgp = XX18Market()
XX18State(market=xgp)

the_values=[
    " 0  0 90 100 110 120 135 150 170",
    " 0 75 80  90 100 110 120 135 150",
    "65 70 75  80  90 100 110 120 135",
    "60 65 70  75  80  90 100 110 120",
    "55 60 65  70  75  80  90 100 110",
    "50 55 60  65  70  75  80",
    "40 50 55  60  65  70",
    "30 40 50  55  60",
]

# ---- XX18Market: unstyled
PageBreak()
Text("XX18Market: Unstyled", common=header)
xgu = XX18Market(
    values=the_values
)
XX18State(market=xgu)

# ---- XX18Market: sized
PageBreak()
Text("XX18Market: Sized", common=header)
xgs = XX18Market(
    x=0, y=0,
    height=1.5, width=2,
    font_name='Times-Roman',
    stroke_width=1,
    values=the_values
)
XX18State(market=xgs)

# Polyshape(points=[
#     xgs.A1.nw, xgs.B1.ne, xgs.B1.se, xgs.B1.sw, xgs.A2.se, xgs.A2.sw,
#     ], fill="pink", stroke=None)

# ---- XX18Market: colors & borders
PageBreak()
Text("XX18Market: Colors and Borders", common=header)
xgs = XX18Market(
    x=0, y=0,
    height=1.5, width=2,
    font_name='Times-Roman',
    stroke_width=1,
    market_colors=[(1, "sienna"), (2, "lime"), (3, "gold")],
    value_direction='w',
    values=[
    " 0  0 90 100 110 120 135 150 170",
    " 0 75 80  90,,b 100 110 120 135 150",
    "65 70 75  80,,b  90 100 110 120 135",
    "60 65 70  75,,b  80  90 100 110 120",
    "55,3 60 65  70,,b  75  80  90 100 110",
    "50,3 55,3 60  65  70  75  80",
    "40,2 50,3 55,3  60  65  70",
    "30,1 40,2 50,3  55,3  60",
    ]
)
XX18State(market=xgs)



# ---- XX18Market: zzz
PageBreak()
xgzz = XX18Market(

)
XX18State(market=xgzz)
Text("XX18Market: zzz", common=footer)


# ---- *Save* images
Save(
    output='png',
    dpi=300,
    directory="../docs/source/images/objects",
    names=[
        'xx18_market_default',
        'xx18_market_unstyled',
        'xx18_market_sized',
        'xx18_market_colored',
        'xx18_market_zz',
    ]
)
