"""
Show customised Hexagons grid locations and linklines for protograf

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
a_circle = Common(radius=0.4)

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

# ---- linklines - single line -  hexgrid_linkline_single
Blueprint(stroke_width=0.5)
Text(common=header, text="LinkLine: single")
hexgrid = Hexagons(
    side=0.5,
    x=0, y=0,
    rows=6, cols=4,
    dot=0.02,
    coord_elevation='top'
)
LinkLine(
    grid=hexgrid,
    locations="0101,0403"
)
PageBreak()

# ---- linklines - double-line -  hexgrid_linkline_double
Blueprint(stroke_width=0.5)
Text(common=header, text="LinkLine: double")
hexgrid = Hexagons(
    side=0.5,
    x=0, y=0,
    rows=6, cols=4,
    dot=0.02,
    coord_elevation='top'
)
LinkLine(
    hexgrid,
    "0101,0403,0104"
)
PageBreak()

# ---- linklines - double-line style -  hexgrid_linkline_multi_style
Blueprint(stroke_width=0.5)
Text(common=header, text="LinkLine: multi style")
hexgrid = Hexagons(
    side=0.5,
    x=0, y=0,
    rows=6, cols=4,
    dot=0.02,
    coord_elevation='top'
)
LinkLine(
    hexgrid,
    ["0101","0403","0104","0406"],
    common=Common(stroke="tomato", stroke_width=2)
)
LinkLine(
    hexgrid,
    ["0104","0406"],
    common=Common(stroke="cyan", stroke_width=2)
)
PageBreak()

# ---- linklines - double-line & offset -  hexgrid_linkline_offset
Blueprint(stroke_width=0.5)
Text(common=header, text="LinkLine: style & offset")
hexgrid = Hexagons(
    side=0.5,
    x=0, y=0,
    rows=6, cols=4,
    dot=0.02,
    coord_elevation='top'
)
LinkLine(
    hexgrid,
    [("0101", 0.25, 0.25), ("0403", -0.25, -0.25),
     ("0104", 0.0, 0.25), ("0104", 0.25, -0.25)],
    common=Common(stroke="tomato", stroke_width=1, dotted=True)
)

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
    ]
)
