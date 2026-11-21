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

# ---- XX18Game Grid: Styled
PageBreak()
Text("XX18Game: Styled & Shifted Board", common=header)
xgs = XX18Game(
    rows=4, cols=3,
    x=1.25, y=2,
    label=True,
    label_size=24,
    label_locations="BL",
    fill="khaki",
    stroke="red",
    stroke_width=3)
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
        ('A1', 'city'),
        ('A3', 'city', None, 'Arkwright'),
        ('A5', 'city', (180, .4), 'Aylish', 'right'),

        ('B2', 'cityx2', None, 'Baroque'),
        ('B4', 'cityx3', None, 'Blau'),
        ('B6', 'cityx4', None, 'Branth'),

        ('C1', 'city', None, 'Cantile', 'b',
            [image('images/Panama_Canal_Railway.svg')]),
        ('C3', 'city', None, 'Colwa', 'below',
            [circle(fill="aqua", label="6", radius=0.7)]),
        ('C5', 'city', None, 'Cuwate', 'above',
            [text("8", font_name='Times-Bold', font_size=24)]),

        ('D2', 'cityx2v', None, 'Darpa'),

        ('D4', 'cityx3', None, 'Delroux', 'b',
            [
              image('images/Jinchu_Railway.svg'),
              image('images/Panama_Canal_Railway.svg'),
              circle(fill="orange", label='6')
            ]
        ),

        ('D6', 'city', None, 'Domrus', 'above'),
        ('D6', 'revenue',  (120, .6), '20'),
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
        ('A1', 'town'),
        ('A3', 'town', (90, .3), 'Arkham', 'above'),
        ('A5', circle(fill=None, radius=0.8)),
        ('A5', 'town',),
        ('B2', 'mountain'),
        ('B4 C1 C3', 'mountain', (270, .5), '$40'),
        ('B6', 'mountains', None, "mountains"),
        ('D2', triangle(side=1.5, fill=None, stroke_width=2, label="$20")),
        ('D4', triangle(side=1.5, fill="tan", stroke_width=1, title="$20")),
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

# ---- XX18Game: Features: Track & Town
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
        ('A1', 'hex_fill', None, 'xyellow'),
        ('A3', 'hex_fill', None, 'xred'),
        ('A5', 'hex_fill', None, 'xbrown'),
        ('B2', 'hex_fill', None, 'xgrey'),
        ('B4', 'hex_fill', None, 'xgray'),
        ('B6', 'hex_fill', None, 'xwater'),
        ('C1', 'hex_fill', None, 'xplain'),
        ('C3', 'hex_fill', None, 'pink'),
        ('C5', 'hex_fill', None, 'xoffboard'),
        ('D2 D6', 'hex_fill', None, 'XX18_TILE_YELLOW'),
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
        ('A5', 'mine', None, 'mine'),
        ('B2', 'river', None, 'river'),
        ('B4', 'swamp', None, 'swamp',),
        ('B6', 'desert', None, 'desert'),
        ('C1', 'forest', None, 'forest'),
        ('C3', 'fish', None, 'fish'),
        ('C5', 'tree', None, 'tree'),
        ('D2', 'port', None, 'port'),
        ('D4', 'tunnel', None, 'tunnel'),
        ('D6', 'factory', None, 'factory'),
        ('E1', 'flag', None, 'flag'),
        ('E3', 'pennant', None, 'pennant'),
        ('E5', 'hills', None, 'hills'),
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
        ('A5', 'hex_fill', None, 'xoffboard'),
        ('C1', 'hex_fill', None, 'xoffboard'),
        ('D4', 'hex_fill', None, 'xoffboard'),
        # offboard tracks
        ('A5', 'spike', 'w se', "short",),
        ('D4', 'spike', 'nw ne', "long",),
        ('C1', 'spike', 'ne se', "medium",),
        # offboard phase revenue
        ('A5', 'phase_revenue', None, '20 40', ['xbrown', 'pink']),
        ('C1', 'phase_revenue', (180, .3), '10 20 30 40'),
        ('D4', 'phase_revenue', (90, .2), '20 30'),

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
        ('A5', 'hex_fill', None, 'xoffboard'),
        ('C1', 'hex_fill', None, 'xoffboard'),
        ('B8', 'hex_fill', None, 'xoffboard'),
        # offboard tracks
        ('A5', 'spike', '"n se', "medium",),
        ('B8', 'spike', 'nw ne', "long",),
        ('C1', 'spike', 'sw s', "short",),
        # offboard phase revenue
        ('C1', 'phase_revenue', (180, 0.1), '10 20 30 40'),
        ('B8', 'phase_revenue', (90, 0.2), '30 50'),
        ('A5', 'phase_revenue', None, '30 50 60', ['xgrey', 'pink', 'purple']),
    ]
)
XX18State(board=xgfif)
Text("XX18Game: Offboard Track & Income: Flat", common=footer)

# ---- XX18Game: Private Railroads
PageBreak()
xgprv = XX18Game(
    rows=4, cols=3,
    fill='berylgreen',
    label=True,
    label_size=18,
    features=[
        ('A1', 'private', ( 15, .7), 'L&R', 'A1', (140, .4), 'left'),
        ('A3', 'private', None, 'L&C', 'A3',  None, 'left'),
        ('A5', 'private', ( 15, .3), 'R&L', 'A5', (140, .7), 'right'),
        ('B2', 'private', ( 15, .7), 'B&C', 'B2', (120, .4), 'below'),
        ('B4', 'private', (195, .6), 'A&C', 'B6', (140, .5), 'above'),
        ('C1', 'private', (210, .4), 'LL', 'D2', ( 15, .7), 'left'),
        ('C3', 'private', (180, .7), 'H&A ', 'C3', (0, .4), 'above'),
        ('C5', 'private', (  0, .5), 'H&B', 'C5', ( 180, .6), 'below'),
        ('D4', 'private', (270, .7), 'V&A', 'D4', (90, .4), 'above'),
        ('D6', 'private', (270, .7), 'V&B', 'D6', (90, .4), 'below'),
    ]
)
XX18State(board=xgprv)
Text("XX18Game: Private Railroads", common=footer)

# ---- XX18Game: Track-to-Edge
PageBreak()
C3 = (270, .4)
xgttp = XX18Game(
    rows=4, cols=3,
    fill='berylgreen',
    label=True,
    label_size=18,
    features=[
        ('A1', 'track_edge', (210, .3), 'ne', -0.1),
        ('A1', 'track_edge', (210, .3), 'sw', 0.2),
        ('A1', 'city', (210, .3), 'Archide', 'above'),

        ('A3', 'track_edge', (210, .3), 'ne', -0.1),
        ('A3', 'track_edge', (210, .3), 'sw', 0.2),

        ('B2', 'track_edge', (180, .3), 'w', 0),

        ('C3', 'track_edge', C3, 'w', 0.25),
        ('C3', 'track_edge', C3, 'se', -0.1),

        ('C5', 'track_edge', C3, 'w', 0.25),
        ('C5', 'track_edge', C3, 'se', -0.1),
        ('C5', 'city', C3, 'Cron', 'above'),
    ]
)
XX18State(board=xgttp)
Text("XX18Game: Track-to-Point", common=footer)


# ---- XX18Game: Miscellaneous
PageBreak()
xgmis = XX18Game(
    rows=4, cols=3,
    fill='berylgreen',
    label=True,
    label_size=18,
    features=[
        ('A1', 'tile-letter', (330, 0.6), "Y"),
        ('A3', 'town_border', None),
        ('B2', 'river_line', 'sw B2,ne A3,e A5,ne', 'aqua'),
        ('B4', 'block', "w nw ne"),
        ('B6', image('images/Jinchu_Railway.svg', height=1.5, width=1.5)),
        ('C1', 'river_line', 'nw C1,se C3,se D6,e'),
        ('C5', 'block', "nw", "xred"),
        ('D2 D4', polygon(sides=5, side=0.5, fill_stroke="olive"), (210, 0.7)),
        ('D6 C5', circle(radius=0.3, fill_stroke="orange"), 'w se'),
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
        ('A3', 'town_border', None, 'St. Agnes', 'below'),
        ('B2', 'city', None, 'Brodie'),
        ('B2', 'revenue',  (240, .6), '30'),
        ('C1', 'river_line', 'nw C1,n C1,ne C3,n C3,ne C5,n C5,ne'),
        ('C1 C3 C5', circle(radius=0.5, fill="aqua", label="$20"), 'ne nw'),
        ('D4', 'hex_fill', None, 'xoffboard'),
        ('D4', 'spike', 'ne nw', "short",),
    ]
)
XX18State(board=xgzz)
Text("XX18Game: JSON settings", common=footer)

# ---- XX18Game: Functions
PageBreak()
xgffn = XX18Game(
    rows=4, cols=3,
    fill='berylgreen',
    label=True,
    label_size=18,
    orientation='flat',
)
XX18State(board=xgffn)

xgffn.hex_fill('C5', 'xoffboard')
xgffn.phase_revenue(
    "C5", "30 40 50", 0, 0.3, "vertical",
    ["xbrown","xgrey","pink"])
xgffn.block(
    'B4', 'ne n nw',
    dotted=True)
xgffn.track(
    'A5 B6', 'nw,se',
    color="red")
xgffn.track_edge(
    'A3', 'nw', 30, .3, 0,
    color="purple"),
xgffn.private(
    'B2', 15, 0.7,  'B2', 140, 0.4, 'C&C', 'right',
    color="orange")
xgffn.private(
    'B2', 15, 0.7, 'C3', 280, 0.6,
    color="orange")

Text("XX18Game: Functions", common=footer)

# ---- XX18Game: zzz
PageBreak()
xgzz = XX18Game(
    rows=4, cols=3,
    fill='berylgreen',
    label=True,
    label_size=18,
    features=[
        ('A5', 'hex_fill', None, 'black'),
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
        'xx18_tracktoedge',
        'xx18_miscellaneous',
        'xx18_json',
        'xx18_functions',
        'xx18_zz',
    ]
)
