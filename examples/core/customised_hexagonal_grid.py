"""
Show customised Hexagons grid for protograf

Written by: Derek Hohls
Created on: 22 November 2024
"""

from protograf import *

Create(filename="customised_hexagonal_grid.pdf",
       paper=A8,
       margin=0.75,
       margin_right=0.2, margin_top=0.2,
       font_size=8,
       stroke_width=0.5)

Footer(draw=False)

header = Common(x=0, y=6, font_size=8, align="left")

# ---- rectangular - flat
Blueprint(stroke_width=0.5)
Text(common=header, text="Hexagons: flat")
Hexagons(
    side=0.5,
    x=0, y=0,
    rows=3, cols=3,
)
PageBreak()

# ---- rectangular - pointy
Blueprint(stroke_width=0.5)
Text(common=header, text="Hexagons: pointy")
Hexagons(
    side=0.5,
    x=0, y=0,
    rows=3, cols=3,
    orientation='pointy',
)
PageBreak()

# ---- rectangular - flat - coords
Blueprint(stroke_width=0.5)
Text(common=header, text="Hexagons: flat; coordinates")
Hexagons(
    side=0.6,
    x=0, y=0,
    rows=2, cols=2,
    coord_elevation="middle", coord_prefix='z', coord_suffix='!',
)
Hexagons(
    side=0.6,
    x=2, y=3,
    rows=2, cols=2,
    fill=darkseagreen,
    hex_offset="odd",
    coord_elevation="top", coord_type_x="upper", coord_separator='::',
)
PageBreak()

# ---- rectangular - pointy - coords
Blueprint(stroke_width=0.5)
Text(common=header, text="Hexagons: pointy; coordinates")
Hexagons(
    side=0.6,
    x=0, y=0,
    rows=2, cols=2,
    orientation='pointy',
    coord_elevation="middle", coord_prefix='z', coord_suffix='!',
)
Hexagons(
    side=0.6,
    x=1, y=3,
    rows=2, cols=2,
    orientation='pointy',
    fill=darkseagreen,
    hex_offset="odd",
    coord_elevation="top", coord_type_x="upper", coord_separator='::',
)
PageBreak()

# ---- rectangular - flat - caltrops
Blueprint(stroke_width=0.5)
Text(common=header, text="Hexagons: flat; caltrops&dots")
Hexagons(
    side=0.6,
    x=0, y=0,
    rows=3, cols=3,
    dot=0.04,
    caltrops="medium",
)
PageBreak()

# ---- rectangular - pointy - caltrops
Blueprint(stroke_width=0.5)
Text(common=header, text="Hexagons: pointy; caltrops&dots")
Hexagons(
    side=0.6,
    x=0, y=0,
    rows=3, cols=3,
    orientation='pointy',
    dot=0.04,
    caltrops="large",
)
PageBreak()

# ---- rectangular - offset
Blueprint(stroke_width=0.5)
Text(common=header, text="Hexagons: offset")
Hexagons(
    side=0.5,
    x=0, y=0,
    rows=3, cols=3,
    hex_offset="odd",
    coord_elevation="middle", coord_font_size=5,
    coord_separator=' r', coord_prefix='c',
)
Hexagons(
    side=0.5,
    x=1, y=3,
    rows=3, cols=3,
    hex_offset="odd",
    orientation='pointy',
    fill=darkseagreen,
    coord_elevation="middle", coord_font_size=5,
    coord_separator=' r', coord_prefix='c',
)
PageBreak()

# ---- rectangular - hidden
Blueprint(stroke_width=0.5)
Text(common=header, text="Hexagons: hidden")
Hexagons(
    side=0.5,
    x=1, y=3,
    rows=3, cols=3,
    orientation='pointy',
    fill=darkseagreen,
    hidden=[(1, 2), (1, 3), (3, 2), (3, 3)]
)
Hexagons(
    side=0.5,
    x=0, y=0,
    rows=3, cols=3,
    hidden="2,1 2,3"
)
PageBreak()

# ---- rectangular - radii
Blueprint(stroke_width=0.5)
Text(common=header, text="Hexagons: radii")
Hexagons(
    side=0.5,
    x=0.5, y=0,
    rows=3, cols=3,
    hex_offset="odd",
    radii="w ne se",
)
Hexagons(
    side=0.5,
    x=1.25, y=3,
    rows=3, cols=3,
    stroke=red,
    radii_stroke=red,
    hex_offset="even",
    radii="e nw sw",
)
PageBreak()

# ---- circular
Blueprint(stroke_width=0.5)
Text(common=header, text="Hexagons: circular")
Hexagons(
    x=0, y=0,
    sides=3,
    height=.75,
    hex_layout="circle",
)
PageBreak()

# ---- circular - nested
Blueprint(stroke_width=0.5)
Text(common=header, text="Hexagons: circular; nested")
Hexagons(
    x=0, y=0,
    sides=3,
    stroke=None, fill=None,
    height=.75,
    hex_layout="circle",
    centre_shape=hexagon(stroke=black, fill=silver, height=0.6, stroke_width=2),
)
PageBreak()

# ---- diamond
Blueprint(stroke_width=0.5)
Text(common=header, text="Hexagons: diamond")
Hexagons(
    x=0, y=0,
    rows=3,
    height=0.75,
    hex_layout="diamond",
)
PageBreak()


Save(
    output='png',
    dpi=300,
    directory="../docs/source/images/custom/hexagonal_grid",
    names=[
        "rect_basic_flat", "rect_basic_pointy",
        "rect_coords_flat", "rect_coords_pointy",
        "rect_caltrops_flat", "rect_caltrops_pointy",
        "rect_offset", "rect_hidden", "rect_radii",
        "circular", "circular_nested",
        "diamond",
      ])
