"""
Show customised Hexagons grid locations and gridlines for protograf

Written by: Derek Hohls
Created on: 7 December 2024
"""

from protograf import *

Create(
    filename="customised_hexagonal_grid_locations.pdf",
    paper="A8",
    margin_left=0.5,
    margin_right=0.3,
    margin_bottom=0.2,
    margin_top=0.5,
    font_size=8,
    stroke_width=0.5
)

header = Common(x=0, y=0, font_size=8, align="left")
a_circle = Common(radius=0.3)
'''
# ---- location - single shape -  hexgrid_location_single
Blueprint(stroke_width=0.5)
Text(common=header, text="Location: single shape")
hexgrid = Hexagons(
    side=0.5,
    x=0, y=0,
    rows=6, cols=4,
)
Location(
    hexgrid,
    "0101",
    [circle(common=a_circle)]
)
PageBreak()

# ---- location - multiple shapes -  hexgrid_location_multiple
Blueprint(stroke_width=0.5)
Text(common=header, text="Location: multiple shapes")
hexgrid = Hexagons(
    side=0.5,
    x=0, y=0,
    rows=6, cols=4,
)
Location(
    hexgrid,
    "0101",
    [circle(common=a_circle), dot()]
)
PageBreak()

# ---- locations - multiple shapes -  hexgrid_locations_multi
Blueprint(stroke_width=0.5)
Text(common=header, text="Locations: multiple shapes")
hexgrid = Hexagons(
    side=0.5,
    x=0, y=0,
    rows=6, cols=4,
)
Locations(
    hexgrid,
    "0204, 0101",
    [circle(common=a_circle), dot()]
)
PageBreak()

# ---- locations - sequence numbers -  hexgrid_locations_seq
Blueprint(stroke_width=0.5)
Text(common=header, text="Locations: sequence numbers")
hexgrid = Hexagons(
    side=0.5,
    x=0, y=0,
    rows=6, cols=4,
)
Locations(
    hexgrid,
    "all",
    [circle(common=a_circle, label="s{{sequence}}")]
)
PageBreak()

# ---- locations - col & row numbers -  hexgrid_locations_colrow
Blueprint(stroke_width=0.5)
Text(common=header, text="Locations: col&row")
hexgrid = Hexagons(
    side=0.5,
    x=0, y=0,
    rows=6, cols=4,
)
Locations(
    hexgrid,
    "all",
    [circle(common=a_circle, label="c{{col}}r{{row}}")]
)
PageBreak()

# ---- locations - labels -  hexgrid_locations_labels
Blueprint(stroke_width=0.5)
Text(common=header, text="Locations: labels")
hexgrid = Hexagons(
    side=0.5,
    x=0, y=0,
    rows=6, cols=4,
)
Locations(
    hexgrid,
    "all",
    [circle(common=a_circle, label="l{{label}}")]
)
PageBreak()

# ---- gridlines - single line
Blueprint(stroke_width=0.5)
Text(common=header, text="GridLine: locations: single")
hexgrid = Hexagons(
    side=0.5,
    x=0, y=0,
    rows=6, cols=4,
    dot=0.02,
    coord_elevation='top'
)
GridLine(
    grid=hexgrid,
    locations="0101,0403"
)
PageBreak()

# ---- gridlines - double-line
Blueprint(stroke_width=0.5)
Text(common=header, text="GridLine: locations: double")
hexgrid = Hexagons(
    side=0.5,
    x=0, y=0,
    rows=6, cols=4,
    dot=0.02,
    coord_elevation='top'
)
GridLine(
    hexgrid,
    locations="0101,0403,0104"
)
PageBreak()

# ---- gridlines - double-line style
Blueprint(stroke_width=0.5)
Text(common=header, text="GridLine: locations: multi style")
hexgrid = Hexagons(
    side=0.5,
    x=0, y=0,
    rows=6, cols=4,
    dot=0.02,
    coord_elevation='top'
)
GridLine(
    hexgrid,
    locations=["0101","0403","0104","0406"],
    common=Common(stroke="tomato", stroke_width=2)
)
GridLine(
    hexgrid,
    locations=["0104","0406"],
    common=Common(stroke="cyan", stroke_width=2)
)
PageBreak()

# ---- gridlines - double-line & offset
Blueprint(stroke_width=0.5)
Text(common=header, text="GridLine: locations: style & offset")
hexgrid = Hexagons(
    side=0.5,
    x=0, y=0,
    rows=6, cols=4,
    dot=0.02,
    coord_elevation='top'
)
GridLine(
    hexgrid,
    locations=[
        ("0101", 0.25, 0.25), ("0403", -0.25, -0.25),
        ("0104", 0.0, 0.25), ("0104", 0.25, -0.25)],
    common=Common(stroke="tomato", stroke_width=1, dotted=True)
)
PageBreak()
'''
# ---- gridlines - edges
Blueprint(stroke_width=0.5)
Text(common=header, text="GridLine: edges: multi style")
hexgrid = Hexagons(
    side=0.5,
    x=0, y=0.1,
    rows=6, cols=5,
    dot=0.02,
    # coord_elevation='top'
)
Locations(
    hexgrid,
    "all",
    [circle(common=a_circle, label="c{{col}}r{{row}}", fill=None, stroke="red", label_size=6)]
)

for hg in hexgrid:
    print(hg.col, hg.row, hg.id)

GridLine(
    hexgrid,
    start="0203",
    vertex="nw",
    edges="e,ne,e,ne",
    common=Common(
        stroke="cyan",
        stroke_width=3)
)

Hexagons(side=0.5, x=0, y=0.1, rows=6, cols=5, fill=None)

GridLine(
    hexgrid,
    start="0204",
    vertex="ne",
    edges=["se", "e", "ne", "e"],
    common=Common(
        stroke="tomato",
        stroke_width=2,
        dotted=True)
)
PageBreak()

Save(
    output='png',
    dpi=300,
    directory="../docs/source/images/custom/hexagonal_grid",
    names=[
        "hexgrid_location_single",
        "hexgrid_location_multiple",
        "hexgrid_locations_multi",
        "hexgrid_locations_seq",
        "hexgrid_locations_colrow",
        "hexgrid_locations_labels",
        "hexgrid_linkline_single",
        "hexgrid_linkline_double",
        "hexgrid_linkline_multi_style",
        "hexgrid_linkline_offset",
        "hexgrid_edges_multi_style",
    ]
)
