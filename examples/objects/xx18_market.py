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
    "55 60 65  70  75  80  90",
    "50 55 60  65  70  75  80",
    "40 50 55  60  65  70",
    "30 40 50  55  60",
]

# ---- XX18Market: unstyled
PageBreak()
Text("XX18Market: Unstyled", common=header)
xgu = XX18Market(
    values=the_values,
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
    values=the_values,
)
XX18State(market=xgs)


# ---- XX18Market: colors & borders
PageBreak()
Text("XX18Market: Colors and Borders", common=header)
xgs = XX18Market(
    x=0, y=0,
    height=1.5, width=2,
    font_name='Times-Roman',
    stroke_width=1,
    fill="bisque",
    market_colors=[(1, "sienna"), (2, "lime"), (3, "gold")],
    value_direction='sw',
    values=[
    " 0  0 90 100 110 120 135 150 170",
    " 0 75 80  90,,,o 100 110 120 135 150",
    "65 70 75  80,,,o  90 100 110 120 135",
    "60 65 70  75,,,o  80  90 100 110 120",
    "55,3 60 65  70,,,o  75  80  90",
    "50,3 55,3 60  65  70  75  80",
    "40,2 50,3 55,3  60  65  70",
    "30,1 40,2 50,3  55,3  60   0   0  ~",
    ],
)
XX18State(market=xgs)

# ---- XX18Market: arrows default
PageBreak()
Text("XX18Market: Default Arrows", common=header)
xga = XX18Market(
    x=0, y=0,
    height=1.5, width=2,
    font_name='Times-Roman',
    stroke_width=1,
    value_direction='se',
    values=[
    " 0  0 90 100 110 120 135 150 170",
    " 0 75 80  90 100 110 120 135 150,,u",
    "65,,d 70 75  80  90 100 110 120 135,,u",
    "60,,d 65 70  75  80  90 100 110 120,,u",
    "55,,d 60 65  70  75  80  90,,u",
    "50,,d 55 60  65  70  75  80,,u",
    "40,,d 50 55  60  65  70,,u",
    "30 40 50  55  60,,u",
    ],
)
XX18State(market=xga)

# ---- XX18Market: arrows
PageBreak()
Text("XX18Market: Custom Arrows", common=header)

arrows = Common(
    fill="black",
    height=0.6, width=0.1,
    head_height=0.3, head_width=0.3,)
arr_up = arrow(
    common=arrows,
    offset_x=0.7, offset_y=0.6)
arr_down = arrow(
    common=arrows,
    rotation=180,
    offset_x=-0.7, offset_y=-0.6)

xgr = XX18Market(
    x=0, y=0,
    height=1.5, width=2,
    font_name='Times-Roman',
    stroke_width=1,
    value_direction='s',
    arrow_up=arr_up,
    arrow_down=arr_down,
    values=[
    " 0  0 90 100 110 120 135 150 170",
    " 0 75 80  90 100 110 120 135 150,,u",
    "65,,d 70 75  80  90 100 110 120 135,,u",
    "60,,d 65 70  75  80  90 100 110 120,,u",
    "55,,d 60 65  70  75  80  90,,u",
    "50,,d 55 60  65  70  75  80,,u",
    "40,,d 50 55  60  65  70,,u",
    "30 40 50  55  60,,u",
    ],
)
XX18State(market=xgr)

# ---- XX18Market: Full
PageBreak()
Text("XX18Market", common=header)

arrows = Common(
    fill="black",
    height=0.6, width=0.1,
    head_height=0.3, head_width=0.3,)
arr_up = arrow(
    common=arrows,
    offset_x=0.7, offset_y=0.6)
arr_down = arrow(
    common=arrows,
    rotation=180,
    offset_x=-0.7, offset_y=-0.6)

xgf = XX18Market(
    x=0, y=0,
    height=1.5, width=2,
    font_name='Times-Bold',
    stroke_width=1,
    value_direction='s',
    fill="ivory",
    market_colors=[(1, "sienna"), (2, "lime"), (3, "gold")],
    arrow_up=arr_up,
    arrow_down=arr_down,
    values=[
    " 0  0 90 100,,,o 110 120 135 150 170",
    " 0 75 80  90,,,o 100 110 120 135 150,,u",
    "65,,d 70 75 80,,,o 90 100 110 120 135,,u",
    "60,,d 65 70 75,,,o 80 90 100 110 120,,u",
    "55,3,d 60 65 70,,,o 75 80 90,,u",
    "50,3,d 55,3 60 65 70 75 80,,u",
    "40,2,d 50,3 55 60 65 70,,u",
    "30,1 40,2 50,3 55 60,,u",
    ],
)
XX18State(market=xgf)

Text("Initial", xy=xgf.D3.c, stroke="firebrick")
Image("images/king.png", x=xgf.I1.c.x, y=xgf.I1.c.y - 0.9)
Polyshape(points=[
    xgs.A1.nw,
    xgs.B1.ne, xgs.B1.se, xgs.B1.sw,
    xgs.A2.se, xgs.A2.sw,
    ],
    fill="silver",
    stroke=None)


# ---- XX18Market: zzz
PageBreak()
xgzz = XX18Market()
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
        'xx18_market_arrows_default',
        'xx18_market_arrows_custom',
        'xx18_market_full',
        'xx18_market_zz',
    ]
)
