# -*- coding: utf-8 -*-
"""
Example code for protograf XX18 command

Written by: Derek Hohls
Created on: 11 November 2026
"""
from protograf import *

Create(
    filename="xx18.pdf",
    paper="A5",
    margin=1,
    page_grid=1)

header = Common(x=0, y=0, font_size=18, align="left")
footer = Common(x=0, y=18, font_size=18, align="left")

# ---- default XX18 Game Grid: pointy
Text("XX18 Game: Default Board", common=header)
xgp = XX18Game()
XX18State(board=xgp)

# ---- default XX18 Game Grid: flat
PageBreak()
Text("XX18 Game: Flat Orientation", common=header)
xgf = XX18Game(orientation="flat")
XX18State(board=xgf)

# ---- offset XX18 Game Grid: pointy
PageBreak()
Text("XX18 Game: Pointy & hex_offset", common=header)
xgpo = XX18Game(hex_offset="odd")
XX18State(board=xgpo)

# ---- offset XX18 Game Grid: flat
PageBreak()
Text("XX18 Game: Flat & hex_offset", common=header)
xgfo = XX18Game(orientation="flat", hex_offset="odd")
XX18State(board=xgfo)

# ---- XX18 Game Grids: Labels & debug
PageBreak()
Text("XX18 Game: labels & debug", common=header)
xgld = XX18Game(
    rows=4, cols=3,
    labels=True,
    debug=True,
)
XX18State(board=xgld)

# ---- XX18 Game Grid - styled
PageBreak()
xgs = XX18Game(
    rows=4, cols=3,
    name="grid",
    fill="khaki",
    stroke="red",
    stroke_width=2,
    label=True,
    label_stroke="blue")
XX18State(board=xgs)
Text("XX18 Game: Styled Board", common=footer)

# ---- Hexagons - pattern
PageBreak()
Text("Hexagons: pattern", common=header)
xgha = XX18Game(
    rows=5,
    cols=4,
    fill='lawngreen',
    pattern = """
    . O O .
     O O O .
    O O O .
     . O O .
     . O O .
    """)
XX18State(board=xgha)


# ---- *Save* images
Save(
    output='png',
    dpi=300,
    directory="../docs/source/images/objects",
    names=[
        'xx18_grid_pointy', 'xx18_grid_flat',
        'xx18_grid_pointy_offset', 'xx18_grid_flat_offset',
        'xx18_grid_labels_debug',
        'xx18_styled',
        'xx18_hexagons_pattern',
    ]
)
