"""
"New Classic" game boards example for protograf

Written by: Derek Hohls
Created on: 6 February 2026

Notes:
  * The boards in this collection are based on those presented in the
    booklet "A NEW BOOK OF CLASSIC BOARD GAMES (V1.0)"  by Brian E. Svoboda
    as discussed here https://boardgamegeek.com/thread/3357842 - but
    any faults, errors or omissions are mine and *not* the author's!
"""

from protograf import *

Create(filename="new_classic_boards.pdf", margin=0.5, paper="A4-l")

# ---- common usage
source = '"New Book of Classic Board Games", Brian E. Svoboda, 2026.'
title = Common(x=1, y=1, font_name="Times-Roman", align="left", font_size=13)
credit = Common(x=19.5, y=19.75, font_name="Times-Italic", align="left", font_size=10)

# ---- .Ataxx
Text("Attaxx", common=title)
Text(source, common=credit)
ATAXX_BLUE = "#21BDE6"
atx = Common(
    fill="#929292", stroke="#7C7C7C",
    blank_fill="#85DBF1",
    stroke_width=1,side=0.25,)
x00 = '0000000'
xcn = '0001000'
xdb = '0010100'
xot = '1000001'
xin = '0100010'
Polyomino(
    x=2, y=1.5, common=atx,
    pattern=[x00, x00, xcn, xdb, xcn, x00, x00])
Polyomino(
    x=4, y=1.5, common=atx,
    pattern=[x00, x00, xcn, '0011100', xcn, x00, x00])
Polyomino(
    x=6, y=1.5, common=atx,
    pattern=[xdb, x00, '1001001', x00, '1001001', x00, xdb])
Polyomino(
    x=2, y=3.5, common=atx,
    pattern=[x00, x00, xdb, x00, xdb, x00, x00])
Polyomino(
    x=4, y=3.5, common=atx,
    pattern=[x00, xin, xdb, x00, xdb, xin, x00])
Polyomino(
    x=6, y=3.5, common=atx,
    pattern=[xcn, xdb, xin, xot, xin, xdb, xcn])
Polyomino(
    x=2, y=5.5, common=atx,
    pattern=[x00, x00, xdb, xcn, xdb, x00, x00])
Polyomino(
    x=4, y=5.5, common=atx,
    pattern=[xcn, x00, x00, xot, x00, x00, xcn])
Polyomino(
    x=6, y=5.5, common=atx,
    pattern=[xdb, x00, '1010101', x00, '1010101', x00, xdb])
Polyomino(
    x=2, y=7.5, common=atx,
    pattern=[xcn, xcn, x00, '1100011', x00, xcn, xcn])
Polyomino(
    x=4, y=7.5, common=atx,
    pattern=[xcn, xcn, xcn, '1110111', xcn, xcn, xcn])
Polyomino(
    x=6, y=7.5, common=atx,
    pattern=[xdb, xdb, xot, '1001001', xot, xdb, xdb])
Polyomino(
    x=2, y=9.5, common=atx,
    pattern=[x00, xdb, xin, x00, xin, xdb, x00])
Polyomino(
    x=4, y=9.5, common=atx,
    pattern=[xcn, x00, xin, xot, xin, x00, xcn])
Polyomino(
    x=6, y=9.5, common=atx,
    pattern=['0011100', x00, '1101011', xot, '1101011', x00, '0011100'])
Polyomino(
    x=2, y=11.5, common=atx,
    pattern=[xdb, x00, xdb, xin, xdb, x00, xdb])
Polyomino(
    x=4, y=11.5, common=atx,
    pattern=[xdb, xin, xot, x00, xot,xin, xdb])
Polyomino(
    x=6, y=11.5, common=atx,
    pattern=[xcn, x00, '0110110', '1100011', '0110110', x00, xcn])
Polyomino(
    x=2, y=13.5, common=atx,
    pattern=[x00, xdb, '1101011', xcn, '1101011', xdb, x00])
Polyomino(
    x=4, y=13.5, common=atx,
    pattern=[x00, x00, x00, x00, x00, x00, x00])
Grid(
    x=9, y=1.5,
    rows=7, cols=7,
    side=2.5,
    fill=ATAXX_BLUE,
    stroke_width=2
)
Text(source, common=credit)
PageBreak()

# ---- .Cairo Corridor
Text("Cairo Corridor", common=title)
Text(source, common=credit)
START_X = 7
START_Y = 2.4
INTERVAL = 3.
litec = Common(stroke_width=1.5, stroke='black', fill='#F0E370')
darkc = Common(stroke_width=1.5, stroke='black', fill='#CEBB53')
# ---- light colors
offset = 0
for row in steps(0, 5, 1):
    for col in steps(0, 2, 1):
        Polyshape(
            x=START_X + INTERVAL*col*2 + offset,
            y=START_Y + INTERVAL*row,
            common=litec,
            snail=cairo_pentagon_snail(INTERVAL, "west"))
        Polyshape(
            x=START_X + INTERVAL*col*2 + offset,
            y=START_Y + INTERVAL*row,
            common=litec,
            snail=cairo_pentagon_snail(INTERVAL, "east"))
    offset = INTERVAL - offset
# ---- dark colors
offset = INTERVAL
for row in steps(0, 5, 1):
    for col in steps(0, 2, 1):
        Polyshape(
            x=START_X + INTERVAL*col*2 + offset,
            y=START_Y + INTERVAL*row,
            common=darkc,
            snail=cairo_pentagon_snail(INTERVAL, "north"))
        Polyshape(
            x=START_X + INTERVAL*col*2 + offset,
            y=START_Y + INTERVAL*row,
            common=darkc,
            snail=cairo_pentagon_snail(INTERVAL, "south"))
    offset = INTERVAL - offset
PageBreak()

# ---- .Checkers
Text("Checkers", common=title)
Text(source, common=credit)
place = Common(height=3, width=3, fill="#FFFA4F", stroke_width=2)
tch = RectangularLocations(x=10.5, y=5, cols=4, rows=3, interval=3)
Layout(tch, shapes=[rhombus(common=place)])
tch = RectangularLocations(x=12, y=6.5, cols=4, rows=3, interval=3)
Layout(tch, shapes=[rhombus(common=place)])
edge = Common(height=3, width=3, fill="#FFC433", stroke_width=2)
Repeat(rhombus(x=10.5, y=2, common=edge), interval=3, cols=4, rows=1)
Repeat(rhombus(x=9, y=12.5, common=edge), interval=3, cols=4, rows=1)
PageBreak()

# ---- .Chinese Checkers
Text("Chinese Checkers", common=title)
Text(source, common=credit)
CC_LINE = "#E4B700"
player_space = circle(
    radius=0.75, stroke="#B59200", fill="#E7B900", stroke_width=2)
board_space = circle(
    radius=0.75, stroke=CC_LINE, fill="#FFD42A", stroke_width=2)
dmds = DiamondLocations(
    y=10, x=0.5, cols=17, facing="west", side=2)
Layout(
    dmds,
    shapes=[board_space],
    gridlines='d n',
    gridlines_stroke=CC_LINE,
    gridlines_stroke_width=4,
    gridlines_fill="#FFFDB2")
Layout(dmds, cols="1-5,13-17", shapes=[player_space])
Layout(dmds, locations=[(9,9)], shapes=[dot(dot_width=5)])
PageBreak()

# ---- .Connect6 (pen-and-paper)

# ---- .Go
Text("Go", common=title)
Text(source, common=credit)
Rectangle(
    height=19, width=19,
    x=4.5, y=0.5,
    fill_stroke="#DCB35C")
Grid(
    x=6, y=2,
    cols=8, rows=8,
    stroke_width=1,
    side=2)
Dot(cx=14, cy=10, dot_width=10)
PageBreak()

# ---- .Hex
Text("Hex", common=title)
Text(source, common=credit)
HEX_LABELS = Common(align="left", font_size=20, stroke="#B58863")
Rhombus(
    height=17, width=29.2, cx=14.25, cy=9.25,
    stroke="black", fill="white", stroke_width=1,
    slices=["white", "black", "white", "black"])
Hexagons(
    cols=21, rows=11,
    hex_layout="diamond",
    height=1.5,
    fill="#F0D9B5",
    margin_bottom=1.25,
    margin_left=-0.1,
)
Dot(cx=14.25, cy=9.25, dot_width=6)
Sequence(
    text(text="{{sequence}}",
         x=0.8, y=9.8,
         common=HEX_LABELS),
    setting=(1, 11),
    interval_y=0.763, interval_x=1.3)
Sequence(
    text(text="{{sequence}}",
         x=0.8, y=9.1,
         common=HEX_LABELS),
    setting=('a', 'k', 1, 'letter'),
    interval_y=-0.763, interval_x=1.3)
PageBreak()

# ---- .Joust
Text("Joust", common=title)
Text(source, common=credit)
sqr_locations = RectangularLocations(
    cols=8, rows=8,
    x=6.75, y=2,
    interval=2.25,
    start="NW", direction="east",
    pattern="snake")
Layout(
   sqr_locations,
   shapes=[
       square(side=2.25, stroke=None, fill="#FFFDB2"),
       square(side=2.25, stroke=None, fill="gray")])
Rectangle(
    x=5.57, y=0.85,
    width=18, height=18,
    stroke="#B59200",
    stroke_width=3,
    fill=None)
PageBreak()

# ---- .King's Valley
Text("King's Valley", common=title)
Text(source, common=credit)
brd = Common(cx=14.4, cy=10.4, radius=8, stroke_width=8)
Circle(
    common=brd,
    fill="#FFDC85",
    stroke="#CAB36E",
    radii=steps(22, 355, 45),
    radii_stroke="black",
    radii_stroke_width=4,
    rotation=15)
Circle(common=brd, stroke="#CAB36E", fill=None)
PageBreak()

# ---- .Mills
Text("Mills", common=title)
Text(source, common=credit)
SIZE = 5
dotty = dot(dot_width=20)
# frame
rect = Rectangle(
    cx=14.3, cy=10,
    width=SIZE*3 + 2.5, height=SIZE*3 + 2.5,
    stroke_width=3, fill_stroke="#D9D9D9",
    rounding=1)
# board
rect = Common(
    cx=14.3, cy=10,
    stroke_width=4,
    vertex_shapes=[dotty]*4,
    perbii_shapes=[('*', dotty)]*4)
r1 = Rectangle(
    common=rect,
    width=SIZE*3, height=SIZE*3, fill="#8DD9FF")
r2 = Rectangle(
    common=rect,
    width=SIZE*2, height=SIZE*2, fill="#8DB3FF")
r3 = Rectangle(
    common=rect,
    width=SIZE, height=SIZE, fill="#D08DFF")
lns = Common(stroke_width=4)
# connections (orthogonal)
Line(common=lns, connections=[(r3, 'p', 'n'), (r1, 'p', 'n')])
Line(common=lns, connections=[(r3, 'p', 's'), (r1, 'p', 's')])
Line(common=lns, connections=[(r3, 'p', 'e'), (r1, 'p', 'e')])
Line(common=lns, connections=[(r3, 'p', 'w'), (r1, 'p', 'w')])
PageBreak()

# ---- .Odd
Text("Odd", common=title)
Text(source, common=credit)
Hexagon(cx=14.8, cy=10.5, height=17, fill_stroke="#FDDCDC")
HexHex(
    cx=14.8, cy=10.5,
    height=1.8,
    rings=4,
    orientation="pointy",
    shape=hexagon(
        height=1.65, orientation="pointy",
        fill="#ED3436",
        stroke="#8A1F20",
        stroke_width=1))
PageBreak()

# ---- .Sea Battle Tafl
Text("Sea Battle Tafl", common=title)
Text(source, common=credit)
Grid(
    x=5.5, y=1,
    cols=9, rows=9,
    stroke_width=2,
    side=2,
    fill="#63B0EB", stroke="#003F73")
rct = RectangularLocations(x=6.5, y=2, cols=9, rows=9, interval=2)
place = Common(fill=None, stroke="white", stroke_width=3, dotted=True)
Layout(
    rct,
    shapes=[square(common=place)],
    locations=[
        (5,1), (2,2), (5,2), (8,2), (3,3), (7,3),
        (1,5), (2,5), (8,5), (9,5),
        (5,9), (2,8), (5,8), (8,8), (3,7), (7,7),
    ])
Layout(
   rct,
   shapes=[circle(common=place)],
   locations=[
       (4,4), (5,4), (6,4),
       (4,5), (5,5), (6,5),
       (4,6), (5,6), (6,6),
   ])
PageBreak()

# ---- .Sprouts (pen-and-paper)

# ---- .Squava
Text("Squava", common=title)
Text(source, common=credit)
Grid(
    x=10, y=4,
    cols=5, rows=5,
    stroke_width=1,
    side=2,
    omit_outer=True)
PageBreak()

# ---- .Strands
Text("Strands", common=title)
Text(source, common=credit)
hxc = Common(
    orientation="pointy",
    height=2,
    stroke="black",
    stroke_width=2,
    label_size=42,
    label_font="Helvetica-Bold")
hx1 = hexagon(
    common=hxc,
    label="1",
    fill="#EEC3C3",
    label_stroke="#C63A39")
hx2 = hexagon(
    common=hxc,
    label="2",
    fill="#F9DCB9",
    label_stroke="#EB8814")
hx3 = hexagon(
    common=hxc,
    label="3",
    fill="#C5EED7",
    label_stroke="#39C676")
hx4 = hexagon(
    common=hxc,
    label="4",
    fill="#B9D7F8",
    label_stroke="#3978C6")
hx6 = hexagon(
    common=hxc,
    label="6",
    fill="#CEC4EF",
    label_stroke="#5839C6")
HexHex(
    cx=14.3, cy=10,
    height=2,
    rings=4,
    orientation="pointy",
    shapes=[
        (0, [hx1]),
        (1, [hx2]*6),
        (2, [hx2]*12),
        (3, [hx3, hx2, hx3, hx3, hx3, hx2, hx3, hx3, hx3]*2),
        (4, [hx6, hx4, hx4, hx4]*6),
   ])
PageBreak()

# ---- .Turkish Checkers (checker/chess board)

# ---- .Ultimate Tic-Tac-Toe
Text("Ultimate Tic-Tac-Toe", common=title)
Text(source, common=credit)
Grid(
    x=4, y=1,
    cols=3, rows=3,
    stroke_width=3,
    side=6,
    omit_outer=True)
for x in range(0, 18, 6):
    for y in range(0, 18, 6):
        Grid(
            x=x + 4.45, y=y + 1.45,
            cols=3, rows=3,
            stroke_width=1.5,
            side=1.7,
            dotted=True,
            omit_outer=True)
PageBreak()

# ---- .Volo
Text("Volo", common=title)
Text(source, common=credit)
HexHex(
    cx=14.3, cy=10,
    height=2,
    rings=5,
    orientation="pointy",
    shape=None,
    gridlines=True,
    gridlines_fill="#99EBFF",
    gridlines_stroke_width=2)
Hexagon(
    cx=14.3, cy=10,
    height=17.2, stroke_width=4, fill=None,
    centre_shape=hexagon(
        height=3.5, stroke_width=4, fill="white"),
    radii_shapes=[
        ('*',
         rhombus(
             width=3.5, height=1.95, stroke_ends="squared",
             stroke_width=4, fill="white"),
         0.9)
    ],
    radii_shapes_rotated=True)
place = Common(fill=None, stroke="grey", stroke_width=2, dotted=True)
Hexagon(
    cx=14.3, cy=10,
    height=17.2, stroke_width=6,
    caltrops=0.185, stroke_ends="squared",
    stroke="white", fill=None,
    radii_shapes=[
        ('ne', square(common=place), 0.8),
        ('se', square(common=place), 0.8),
        ('w', square(common=place), 0.8),
        ('e', circle(common=place), 0.8),
        ('sw', circle(common=place), 0.8),
        ('nw', circle(common=place), 0.8),
    ])

Save()
