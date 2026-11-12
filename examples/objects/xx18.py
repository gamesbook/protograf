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

# ---- XX18 Game Grid: default (pointy)
Text("XX18 Game: Default Board", common=header)
xgp = XX18Game()
XX18State(board=xgp)

# ---- XX18 Game Grid: default & flat
PageBreak()
Text("XX18 Game: Flat Orientation", common=header)
xgf = XX18Game(orientation="flat")
XX18State(board=xgf)

# ---- XX18 Game Grid: offset & pointy
PageBreak()
Text("XX18 Game: Pointy & hex_offset", common=header)
xgpo = XX18Game(hex_offset="odd")
XX18State(board=xgpo)

# ---- XX18 Game Grid: offset & flat
PageBreak()
Text("XX18 Game: Flat & hex_offset", common=header)
xgfo = XX18Game(orientation="flat", hex_offset="odd")
XX18State(board=xgfo)

# ---- XX18 Game Grid: labels & debug
PageBreak()
xgld = XX18Game(
    rows=4, cols=3,
    label=True,
    debug=True,
)
XX18State(board=xgld)
Text("XX18 Game: label edges & debug", common=footer)

# ---- XX18 Game Grid: basic styles
PageBreak()
Text("XX18 Game: Styled Board", common=header)
xgs = XX18Game(
    rows=4, cols=3,
    name="grid",
    fill="khaki",
    stroke="red",
    stroke_width=2)
XX18State(board=xgs)

# ---- XX18 Game Grid: fill pattern
PageBreak()
Text("XX18 Game: Pattern and Fill", common=header)
xghp = XX18Game(
    rows=5, cols=4,
    fill='berylgreen',
    pattern = """
    . O O .
     O O O .
    O O O .
     . O O .
     . O O .
    """)
XX18State(board=xghp)

# ---- XX18 Game: Features: City
PageBreak()
xgfc = XX18Game(
    rows=4, cols=3,
    fill='berylgreen',
    label=True,
    label_size=18,
    features=[
        ('A1', 'city', None),
        ('A3', 'city', None, 'Arkwright', 'above'),
        ('A5', 'city', (180, .4), 'Aylish', 'right'),

        ('B2', 'cityx2', None, 'Baroque'),
        ('B4', 'cityx3', None, 'Blau'),
        ('B6', 'cityx4', None, 'Branth'),

        ('C1', 'city', None, 'Cantile', 'b',
            [image("images/Panama_Canal_Railway.svg")]),
        ('C3', 'city', None, 'Colwa', 'below',
            [circle(fill="aqua", label="6", radius=0.7)]),
        ('C5', 'city', None, 'Cuwate', 'above',
            [text("8", font_name="Times-Bold", font_size=24)]),

        ('D4', 'cityx3', None, 'Delroux', "b",
            [
              image("images/Jinchu_Railway.svg"),
              image("images/Panama_Canal_Railway.svg"),
              circle(fill="orange", label="6")
            ]),
    ]
)
XX18State(board=xgfc)
Text("XX18 Game: City and Styles", common=footer)

# ---- XX18 Game: Features: Town
PageBreak()
xgft = XX18Game(
    rows=4, cols=3,
    fill='berylgreen',
    label=True,
    label_size=18,
    features=[
        ('A1', 'town', None),
        ('B2', 'town', (90, .3), 'Durham', 'above'),
    ]
)
XX18State(board=xgft)
Text("XX18 Game: Town", common=footer)

# ---- XX18 Game: Features: Track
PageBreak()
xgfk = XX18Game(
    rows=4, cols=3,
    fill='berylgreen',
    label=True,
    label_size=18,
    features=[
        ('A1', 'track', 'e,w'),
        ('A3', 'track', 'ne,sw'),
        ('A5', 'track', 'se,nw'),
        ('B2', 'track', 'nw,sw'),
        ('B4', 'track', 'se,w'),
        ('B6', 'track', 'w,ne'),
        ('C1', 'track', 'nw,w'),
        ('C3', 'track', 'se,sw'),
        ('C5', 'track', 'ne,e'),
        ('D2', 'track', 'nw'),
        ('D4', 'track', 'w ne,sw'),
        ('D6', 'track', 'w,e w,ne w,sw'),
    ]
)
XX18State(board=xgfk)
Text("XX18 Game: Track", common=footer)

# ---- XX18 Game: Features: Track
PageBreak()
xgfkt = XX18Game(
    rows=4, cols=3,
    fill='berylgreen',
    label=True,
    label_size=18,
    features=[
        ('A1', 'track_town', 'e,w'),
        ('B2', 'track_town', 'nw,sw'),
        ('C1', 'track_town', 'nw,w'),
    ]
)
XX18State(board=xgfkt)
Text("XX18 Game: Track & Town", common=footer)


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
        'xx18_features_city',
        'xx18_features_town',
        'xx18_features_track',
        'xx18_features_track_town',
    ]
)
