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
    margin=2,
    page_grid=1)

header = Common(x=0, y=0, font_size=18, align="left")
footer = Common(x=0, y=19.5, font_size=18, align="left")

# ---- XX18Game Grid: default (pointy)
Text("XX18Game: Default Board", common=header)
xgp = XX18Game()
XX18State(board=xgp)

# ---- XX18Game Grid: default & flat
PageBreak()
Text("XX18Game: Flat Orientation", common=header)
xgf = XX18Game(orientation="flat")
XX18State(board=xgf)

# ---- XX18Game Grid: offset & pointy
PageBreak()
Text("XX18Game: Pointy & hex_offset", common=header)
xgpo = XX18Game(hex_offset="odd")
XX18State(board=xgpo)

# ---- XX18Game Grid: offset & flat
PageBreak()
Text("XX18Game: Flat & hex_offset", common=header)
xgfo = XX18Game(orientation="flat", hex_offset="odd")
XX18State(board=xgfo)

# ---- XX18Game Grid: labels & debug
PageBreak()
xgld = XX18Game(
    rows=4, cols=3,
    label=True,
    debug=True,
)
XX18State(board=xgld)
Text("XX18Game: label edges & debug", common=footer)

# ---- XX18Game Grid: basic styles
PageBreak()
Text("XX18Game: Styled Board", common=header)
xgs = XX18Game(
    rows=4, cols=3,
    name="grid",
    fill="khaki",
    stroke="red",
    stroke_width=2)
XX18State(board=xgs)

# ---- XX18Game Grid: fill pattern
PageBreak()
Text("XX18Game: Pattern and Fill", common=header)
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

# ---- XX18Game: Features: City
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

        ('D2', 'city', None, 'Darpa'),
        ('D2', 'revenue',  (330, .6), '20'),

        ('D4', 'cityx3', None, 'Delroux', "b",
            [
              image("images/Jinchu_Railway.svg"),
              image("images/Panama_Canal_Railway.svg"),
              circle(fill="orange", label="6")
            ]),
    ]
)
XX18State(board=xgfc)
Text("XX18Game: City and Styles", common=footer)

# ---- XX18Game: Features: Town & Mountain
PageBreak()
xgft = XX18Game(
    rows=4, cols=3,
    fill='berylgreen',
    label=True,
    label_size=18,
    features=[
        ('A1', 'town', None),
        ('B4', 'town', (90, .3), 'Burham', 'above'),
        ('C1', 'mountain', None, '$40'),
        ('C3 D2 D4', 'mountain', (90, .5)),
        ('C5', 'mountains', None, "mountains"),
    ]
)
XX18State(board=xgft)
Text("XX18Game: Town and Mountain/s", common=footer)

# ---- XX18Game: Features: Track
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
Text("XX18Game: Track", common=footer)

# ---- XX18Game: Features: Track
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
Text("XX18Game: Track & Town", common=footer)

# ---- XX18Game: Fills
PageBreak()
xgff = XX18Game(
    rows=4, cols=3,
    fill='berylgreen',
    label=True,
    label_size=18,
    features=[
        ('A1', 'fill', None, 'xyellow'),
        ('A3', 'fill', None, 'xred'),
        ('A5', 'fill', None, 'xbrown'),
        ('B2', 'fill', None, 'xgrey'),
        ('B4', 'fill', None, 'xgray'),
        ('C1', 'fill', None, 'xwater'),
        ('C3', 'fill', None, 'xplain'),
        ('C5', 'fill', None, 'pink'),
        ('D2', 'fill', None, 'xoffboard'),
        ('D4', 'highlight', None, 'yellow'),

    ]
)
XX18State(board=xgff)
Text("XX18Game: Fill and Highlight", common=footer)

# ---- XX18Game: Symbols
PageBreak()
xgfs = XX18Game(
    rows=5, cols=3,
    fill='berylgreen',
    label=True,
    label_size=18,
    features=[
        ('A1', 'oil', None, 'oil'),
        ('A3', 'coal', None, 'coal'),
        ('A5', 'factory', None, 'factory'),
        ('B2', 'river', None, 'river'),
        ('B4', 'swamp', None, 'swamp',),
        ('B6', 'desert', None, 'desert'),
        ('C1', 'forest', None, 'forest'),
        ('C3', 'fish', None, 'fish'),
        ('C5', 'tree', None, 'tree'),
        ('D2', 'port', None, 'port'),
        ('D4', 'tunnel', None, 'tunnel'),
        ('D6', 'hills', None, 'hills'),
        ('E1', 'flag', None, 'flag'),
        ('E3', 'pennant', None, 'pennant'),
        ('E5', 'noentry', None, 'noentry'),

    ]
)
XX18State(board=xgfs)
Text("XX18Game: Symbols", common=footer)

# ---- XX18Game: Offboard and Income - Pointy
PageBreak()
xgfi = XX18Game(
    rows=4, cols=3,
    fill='berylgreen',
    label=True,
    label_size=18,
    features=[
        # offboard color fills
        ('A5', 'fill', None, 'xoffboard'),
        ('C1', 'fill', None, 'xoffboard'),
        ('D4', 'fill', None, 'xoffboard'),
        # offboard tracks
        ('A5', 'spike', 'w se', "short",),
        ('D4', 'spike', 'nw ne', "long",),
        ('C1', 'spike', 'ne se', "medium",),
        # offboard phase revenue
        ('C1', 'phase_revenue', (180, .3), '10 20 30 40'),
        ('A5', 'phase_revenue', None, '20 50'),

    ]
)
XX18State(board=xgfi)
Text("XX18Game: Offboard Track & Income: Pointy", common=footer)

# ---- XX18Game: Offboard and Income - Flat
PageBreak()
xgfif = XX18Game(
    rows=4, cols=3,
    fill='berylgreen',
    label=True,
    label_size=18,
    orientation='flat',
    features=[
        # offboard color fills
        ('A5', 'fill', None, 'xoffboard'),
        ('C1', 'fill', None, 'xoffboard'),
        ('C5', 'fill', None, 'xoffboard'),
        ('B8', 'fill', None, 'xoffboard'),
        # offboard tracks
        ('A5', 'spike', '"n se', "short",),
        ('B8', 'spike', 'nw ne', "long",),
        ('C1', 'spike', 'ne se', "medium",),
        ('C5', 'spike', 'sw', "long",),
        # offboard phase revenue
        ('C1', 'phase_revenue', (180, .1), '10 20 30 40'),
        ('A5', 'phase_revenue', None, '20 50'),
    ]
)
XX18State(board=xgfif)
xgfif.phase_revenue("C5", "30 40 50", 0, 0.3, ["xbrown","xgrey","pink"], "vertical")
Text("XX18Game: Offboard Track & Income: Flat", common=footer)

# ---- XX18Game: Private Railroads
PageBreak()
xgprv = XX18Game(
    rows=4, cols=3,
    fill='berylgreen',
    label=True,
    label_size=18,
    features=[
        ('A1', 'private', None, ""),
        ('A3', 'private', None, "L&L", "A3",  None, "left"),
        ('B2', 'private', ( 15, .7), "R&R", "B2", (140, .4), "above"),
        ('B4', 'private', ( 15, .6), "D&D", "B6", (140, .5), "below"),
        ('C1', 'private', (210, .4), "DD", "C3", ( 15, .7), "left"),
        ('C5', 'private', (140, .5), "RR", "C5", ( 15, .6),"right"),
        ('D2', 'private', (180, .7), "RD", "D2", (0, .4), "above"),
        ('D4', 'private', (270, .7), "D&R", "D4", (90, .4), "above"),
        ('D6', 'private', (270, .7), "R&D", "D6", (90, .4), "below"),
    ]
)
XX18State(board=xgprv)
Text("XX18Game: Private Railroads", common=footer)

# ---- XX18Game: Track-to-Point
PageBreak()
B3 = (270, .4)
xgttp = XX18Game(
    rows=4, cols=3,
    fill='berylgreen',
    label=True,
    label_size=18,
    features=[
        ('A1', 'track_point', (210, .3), 'ne', -0.1),
        ('A1', 'track_point', (210, .3), 'sw', 0.2),
        ('A1', 'city', (210, .3), 'Archide', "above"),

        ('A3', 'track_point', (210, .3), 'ne', -0.1),
        ('A3', 'track_point', (210, .3), 'sw', 0.2),

        ('B2', 'track_point', (180, .3), 'w', 0),

        ('C3', 'track_point', B3, 'w', 0.25),
        ('C3', 'track_point', B3, 'se', -0.1),

        ('C5', 'track_point', B3, 'w', 0.25),
        ('C5', 'track_point', B3, 'se', -0.1),
        ('C5', 'city', B3, 'Cron', "above"),
    ]
)
XX18State(board=xgttp)
Text("XX18Game: Track-to-Point", common=footer)


# ---- XX18Game: Miscellaneous
PageBreak()
poly5 = polygon(sides=5, side=0.5, fill_stroke="purple")
xgmis = XX18Game(
    rows=4, cols=3,
    fill='berylgreen',
    label=True,
    label_size=18,
    features=[
        ('A1', 'tile-letter', (330, 0.6), "Y"),
        ('A5', 'track', 'e,w'),
        ('A5', 'town_border', None),
        ('B4', 'block', "w nw ne"),
        ('C1', 'river_line', 'nw se e se'),
        ('D2 D4', poly5, (90, 0.7)),
    ]
)
XX18State(board=xgmis)
Text("XX18Game: Miscellaneous", common=footer)

# ---- XX18Game: JSON settings
PageBreak()
xgzz = XX18Game(
    rows=4, cols=3,
    fill='berylgreen',
    label=True,
    label_size=18,
    settings="xx18.json",
    features=[
        ('A1', 'mountain', None, '$20'),
        ('A3', 'track', 'e,w'),
        ('A3', 'town_border', None, 'St. Agnes', "below"),
    ]
)
XX18State(board=xgzz)
Text("XX18Game: JSON settings", common=footer)

# ---- XX18Game: zzz
PageBreak()
xgzz = XX18Game(
    rows=4, cols=3,
    fill='berylgreen',
    label=True,
    label_size=18,
    features=[
        ('A5', 'fill', None, 'black'),
    ]
)
XX18State(board=xgzz)
Text("XX18Game: zzz", common=footer)


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
        'xx18_fills',
        'xx18_symbols',
        'xx18_offboard',
        'xx18_offboard_flat',
        'xx18_private',
        'xx18_tracktopoint',
        'xx18_miscellaneous',
        'xx18_json',
        'xx18_zz',
    ]
)
