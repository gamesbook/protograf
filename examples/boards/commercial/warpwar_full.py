"""
A WarpWar map example for protograf

The original map was created by Rick Smith and posted to https://groups.io/g/warpwar/
forum on 3 June 2024.  This is not a complete copy - but serves to illustrate
how elements of such a map could be created.

Code by: Derek Hohls
Created on: 30 July 2024
"""

from protograf import *

Create(filename="warpwar.pdf", margin=0.5, paper="A2")

# set map colors
heading = "white"
map_fill = "black"
if map_fill == "white":
    heading = "black"

map_border = "lightgray"
grid_line = "#AA9A38"
system_label = "#1CAEE5"
warp = "#2ACD21"
# set star colors
m_red = "#FE1200"
k_orange = "#EC600C"
d_brown = "#6A4D05"
# set nebula colors
cloud_edge = "#890B81"
cloud_lite = "#C23E83"
cloud_med = "#711F61"
cloud_dark = "#4D173E"

Rectangle(x=0.0, y=0.0, width=41, height=58.3, stroke=map_border, fill=map_fill)

# title line
txt = Common(y=0.6, font_size=21, align="left", stroke=heading)
gridnum = Common(font_size=21, align="left", stroke=grid_line)
Text(common=txt, x=3,  text="2 Player Warp War Map:      Vedem Sector")
Text(common=txt, x=22, text="(c) 2024 by Richard W. Smith")

# numbered map grid
ww_grid = Hexagons(
    cols=20,
    rows=24,
    y=1.8,
    height=2.22,
    hex_offset="odd",
    coord_elevation="t",
    coord_type_y="upper-multiple",
    coord_offset=0.15,
    coord_font_size=12,
    coord_stroke=grid_line,
    coord_padding=0,
    coord_style="diagonal",
    fill=map_fill,
    stroke=grid_line,
    stroke_width=2,
)

# labels for map edges
Sequence(
    text(common=gridnum, x=0.3, y=5.2, text="{{sequence}}"),
    setting=('A', 'X'),
    interval_y=2.21)
Sequence(
    text(common=gridnum, x=1.9, y=1.5, text="{{sequence}}"),
    setting=(1, 20),
    interval_x=1.92)

# star properties
dstar = Common(fill=d_brown, stroke=d_brown, radius=0.18, dot=0.04, dot_stroke="black")
kstar = Common(fill=k_orange, stroke=k_orange, radius=0.15)
mstar = Common(fill=m_red, stroke=m_red, radius=0.1)
sname = Common(font_size=12, align="centre", stroke=system_label)
mask = rectangle(height=0.6, width=1.2, fill_stroke=map_fill, dx=0, dy=-0.75)
dwarf_outer = circle(fill=d_brown, stroke=d_brown, radius=0.2),
dwarf_inner = rectangle(height=0.1, width=0.1, fill=map_fill, stroke=map_fill),

# system details at a map Location
def draw_item(system):
    """Draw an object in hex"""
    detail = []
    if system[1] == 'm':
        detail = [circle(common=mstar, dx=system[2], dy=system[3])]
    elif system[1] == 'd':
        detail = [circle(common=dstar, dx=system[2], dy=system[3])]
    elif system[1] == 'k':
        detail = [circle(common=kstar, dx=system[2], dy=system[3])]
    elif system[1] == 'cloud':
        detail = [hexagon(
            fill_stroke=cloud_dark, height=2.15, dx=0, dy=0, transparency=50)]
    elif system[1] == '':
        detail = [text(common=sname, dx=system[2], dy=system[3], text=system[4])]
    elif system[1] == 'mask':
        detail = [mask]
    else:
        pass
    if detail:
        Location(ww_grid, system[0], detail)

systems = [
    ["2B", "mask"],
    ["2B", "m", 0.1, -0.8],
    ["2B", "m", -0.6, 0.5],
    ["2B", "", 0.4, 0.1, "Redstar\n        3"],
    ["4B", "m", -0.6, 0.7],
    ["4B", "", 0.1, 0.1, "Lattur\n     2"],
    ["4E", "mask"],
    ["4E", "m", 0.3, -0.8],
    ["4E", "", 0., 0.1, "Rebb\n1"],
    ["1C", "k", 0.5, 0.],
    ["1C", "", 0.1, 0.1, "Bezsin\n         4"],
    ["3G", "d", 0.5, 0.],
    ["3G", "", 0.4, 0.1, "BD3G\n           1"],
    ["1H", "mask"],
    ["1H", "d", -0.6, -0.4],
    ["1H", "d", -0.6, 0.5],
    ["1H", "", 0.6, 0., "BD1H\n   3"],
    ["8L", "hex"],
    ["8L", "k", -0.5, 0.6],
    ["8L", "", 0.8, -0.1, "Highlakes\n    3"],
    ["7F", "mask"],
    ["7F", "", 0.7, -0.4, "  BD7F\nREE+4\n    2"],
    ["7F", "d", 0.1, 0.7],
    ["5E", "m", 0.0, 1.11],

    ["9Y", "m", -0.2, 0.5],
    ["9Y", "d", 0., 0.3],
    ["9Y", "", 0., -0.5, "Veex\      3"],

    ["11F", "m", 0., 0.],
    ["11F", "", 0., 0., "BD11F"],
    ["19J", "m", 0., 0.],
    ["19J", "", 0., 0., "Pullap\    2"],
    ["15I", "m", 0., 0.],
    ["15I", "", 0., 0., "Lexmar\    3"],

    ["15S", "m", -0.4, -0.4],
    ["15S", "d", 0., 0.8],
    ["15S", "", 0.4, -0.5, "Vedem\5"],
    ["15S", "", 0.4, 0.0, "REE+5"],

    ["10L", "m", 0., 0.],
    ["10L", "", 0., 0., "Forseason\   3"],
    ["10L", "", 0., 0., "REE+4"],
    ["13M", "m", 0., 0.],
    ["13M", "", 0., 0., "Tidal\    2"],
    ["17P", "m", 0., 0.],
    ["17P", "", 0., 0., "Peff\            2"],
    ["20Q", "m", 0., 0.],
    ["20Q", "", 0., 0., "BD2OQ\       1"],
    ["20Q", "m", 0., 0.],
    ["20Q", "", 0., 0., "BD2OQ\       1"],

    ["20CC", "m", 0.2, -0.2],
    ["20CC", "d", -0.8, 0.],
    ["20CC", "", 0.1, 0., "Valtol\5"],

    """
    ["", "m", 0., 0.],
    ["", "", 0., 0., ""],

    ["", "m", 0., 0.],
    ["", "", 0., 0., ""],

    ["", "m", 0., 0.],
    ["", "", 0., 0., ""],

    ["", "m", 0., 0.],
    ["", "", 0., 0., ""],

    ["", "m", 0., 0.],
    ["", "", 0., 0., ""],

    ["", "m", 0., 0.],
    ["", "", 0., 0., ""],

    ["", "m", 0., 0.],
    ["", "", 0., 0., ""],

    ["", "m", 0., 0.],
    ["", "", 0., 0., ""],

    ["", "m", 0., 0.],
    ["", "", 0., 0., ""],

    ["", "m", 0., 0.],
    ["", "", 0., 0., ""],

    ["", "m", 0., 0.],
    ["", "", 0., 0., ""],

    ["", "m", 0., 0.],
    ["", "", 0., 0., ""],

    ["", "m", 0., 0.],
    ["", "", 0., 0., ""],

    ["", "m", 0., 0.],
    ["", "", 0., 0., ""],

    ["", "m", 0., 0.],
    ["", "", 0., 0., ""],

    ["", "m", 0., 0.],
    ["", "", 0., 0., ""],

    ["", "m", 0., 0.],
    ["", "", 0., 0., ""],

    ["", "m", 0., 0.],
    ["", "", 0., 0., ""],

    """
]
for system in systems:
    draw_item(system)

if False:
    # borders - appear in multiple locations
    nebul = Common(fill=cloud_dark, stroke=grid_line, height=2.22, dx=0, dy=0, transparency=50)
    Locations(
        ww_grid,
        ["8P", "9Q", "10R" ], [hexagon(
            common=nebul,
            borders=[("n nw", 4, cloud_edge),
                     ("se ne", 4, cloud_edge)])
        ]
    )
    Locations(
        ww_grid, ["8O", "10Q", ], [hexagon(
            common=nebul,
            borders=[("nw sw s", 4, cloud_edge),
                     ("n ne se", 4, cloud_edge, True)])])
    Locations(
        ww_grid, ["8L", ], [hexagon(
            fill=None, stroke=grid_line, height=2.22, dx=0, dy=0, transparency=50,
            borders=[("nw sw", 4, cloud_edge),
                     ("n s", 4, cloud_edge, True)])])
    Locations(
        ww_grid, ["8M", ], [hexagon(
            common=nebul,
            borders=[("n se nw sw", 4, cloud_edge, True)])])
    Locations(
        ww_grid, ["8N", ], [hexagon(
            common=nebul,
            borders=[("n se nw sw", 4, cloud_edge),
                     ("ne s", 4, cloud_edge, True)])])
    Locations(
        ww_grid, ["8K", ], [hexagon(
            common=nebul,
            borders=[("ne nw s", 4, cloud_edge, True),
                     ("sw", 4, cloud_edge)])])
    Locations(
        ww_grid, ["7K", ], [hexagon(
            common=nebul,
            borders=[("s", 4, cloud_edge, True),
                     ("sw ne", 4, cloud_edge)])])
    Locations(
        ww_grid, ["6J", ], [hexagon(
            common=nebul,
            borders=[("nw", 4, cloud_edge, True),
                     ("s", 4, cloud_edge)])])

# warp lines
warp_line = Common(stroke=warp, stroke_width=3, rounded=True)
LinkLine(ww_grid, [("1C",  0.75,  0.2),  ("8L",  -0.6,   0.3)], common=warp_line)
LinkLine(ww_grid, [("1H",  0.0,  -0.7),  ("3G",   0.0,   0.4)], common=warp_line)
LinkLine(ww_grid, [("2B", -0.5,   0.7),  ("4E",   0.05, -0.9)], common=warp_line)
LinkLine(ww_grid, [("2B",  0.15, -0.85), ("4B", -0.75,  0.8)], common=warp_line)
LinkLine(ww_grid, [("4E",  0.25, -1.05), ("4B", -0.6,   0.9)], common=warp_line)

LinkLine(ww_grid, [("7F",  0.00,  0.00), ("11F",  0.00,  0.00)], common=warp_line)
LinkLine(ww_grid, [("11F",  0.00,  0.00), ("15I",  0.00,  0.00)], common=warp_line)
LinkLine(ww_grid, [("15I",  0.00,  0.00), ("19J",  0.00,  0.00)], common=warp_line)
LinkLine(ww_grid, [("15I",  0.00,  0.00), ("13M",  0.00,  0.00)], common=warp_line)
LinkLine(ww_grid, [("10L",  0.00,  0.00), ("13M",  0.00,  0.00)], common=warp_line)
LinkLine(ww_grid, [("13M",  0.00,  0.00), ("17P",  0.00,  0.00)], common=warp_line)
LinkLine(ww_grid, [("17P",  0.00,  0.00), ("20Q",  0.00,  0.00)], common=warp_line)

LinkLine(ww_grid, [("1O",  0.00,  0.00), ("3O",  0.00,  0.00)], common=warp_line)
LinkLine(ww_grid, [("3O",  0.00,  0.00), ("5N",  0.00,  0.00)], common=warp_line)
LinkLine(ww_grid, [("5N",  0.00,  0.00), ("9P",  0.00,  0.00)], common=warp_line)
LinkLine(ww_grid, [("9P",  0.00,  0.00), ("10P",  0.00,  0.00)], common=warp_line)

LinkLine(ww_grid, [("8L",  0.00,  0.00), ("15S",  0.00,  0.00)], common=warp_line)
LinkLine(ww_grid, [("15S",  0.00,  0.00), ("18U",  0.00,  0.00)], common=warp_line)
LinkLine(ww_grid, [("15S",  0.00,  0.00), ("8S",  0.00,  0.00)], common=warp_line)
LinkLine(ww_grid, [("15S",  0.00,  0.00), ("20CC",  0.00,  0.00)], common=warp_line)
LinkLine(ww_grid, [("19W",  0.00,  0.00), ("20W",  0.00,  0.00)], common=warp_line)
LinkLine(ww_grid, [("8S",  0.00,  0.00), ("20CC",  0.00,  0.00)], common=warp_line)

LinkLine(ww_grid, [("5S",  0.00,  0.00), ("8Q",  0.00,  0.00)], common=warp_line)
LinkLine(ww_grid, [("5S",  0.00,  0.00), ("9Y",  0.00,  0.00)], common=warp_line)
LinkLine(ww_grid, [("2U",  0.00,  0.00), ("5V",  0.00,  0.00)], common=warp_line)
LinkLine(ww_grid, [("5V",  0.00,  0.00), ("9Y",  0.00,  0.00)], common=warp_line)
LinkLine(ww_grid, [("9Y",  0.00,  0.00), ("14Y",  0.00,  0.00)], common=warp_line)

LinkLine(ww_grid, [("2W",  0.00,  0.00), ("5Z",  0.00,  0.00)], common=warp_line)
LinkLine(ww_grid, [("5Z",  0.00,  0.00), ("9Y",  0.00,  0.00)], common=warp_line)
LinkLine(ww_grid, [("16BB",  0.00,  0.00), ("20CC",  0.00,  0.00)], common=warp_line)

# LinkLine(ww_grid, [("1A",  0.00,  0.00), ("1A",  0.00,  0.00)], common=warp_line)

# KEY BOX
Rectangle(x=21, y=50.5, width=17, height=6.5, fill=map_fill, stroke=heading)
Text(text="KEY:", font_size=24, x=23, y=52, stroke=heading)
Text(text="(All stars are main sequence)", font_size=12, x=28, y=52, stroke=heading)
Circle(common=dstar, cx=23, cy=53); Text(text="Brown dwarf", font_size=15, x=25, y=53.2, stroke=heading)
Circle(common=mstar, cx=23, cy=53.5); Text(text="M Class Star", font_size=15, x=25, y=53.7, stroke=heading)
Circle(common=kstar, cx=23, cy=54); Text(text="K Class Star", font_size=15, x=25, y=54.2, stroke=heading)

Text(text="Vedeem", font_size=15, x=23, y=55, stroke=system_label)
Text(text="Lettering gives the system name", font_size=15, x=25, y=55, stroke=heading, align="left")
Text(text="REE+5", font_size=15, x=23, y=55.7, stroke=system_label)
Text(text="Number shows the economic value of the system", font_size=15, x=25, y=55.5, stroke=heading, align="left")
Text(text="REE+# the system is rich in Rare Earth Minerals", font_size=15, x=25, y=56, stroke=heading, align="left")
Line(x=22, y=56.5, x1=24, y1=56, common=warp_line)
Text(text="Green lines show Warp Lines between the stars", font_size=15, x=25, y=56.5, stroke=heading, align="left")

Line(x=33, y=53, x1=34.5, y1=53, stroke=cloud_edge, stroke_width=3)
Line(x=33, y=54, x1=34.5, y1=54, stroke=cloud_edge, stroke_width=3, dotted=True)
Text(text="Dust Cloud:", font_size=15, x=33, y=52, stroke=heading, align="left")
Text(text="Max 10 PD", font_size=15, x=35, y=53, stroke=heading, align="left")
Text(text="Max 20 PD", font_size=15, x=35, y=54, stroke=heading, align="left")

Save()
