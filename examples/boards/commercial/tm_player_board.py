"""
"Terraforming Mars: Ares Expedition" player board example for protograf

Written by: Derek Hohls
Created on: 4 August 2025
Notes:

    * Icon Font `game-icons-net-20200315a` from
      https://github.com/toddfast/game-icons-net-font
"""
from protograf import *

Create(filename="tm_player_board.pdf", margin=0.1, paper="A5")

BLACK = "#18181A"
BLUE = "#78C9D1"
LT_GREEN = "#8BB846"
DK_GREEN = "#77A943"
LT_RED = "#FA903A"
DK_RED = "#F37C37"
LT_YELLOW = "#FFC32C"
DK_YELLOW = "#E1C82E"
LT_BLUE = "#91AAC8"
LT_BROWN = "#A26A23"
LT_GREY = "#AAA8AB"
LEAF = "forestgreen"

Rectangle(x=0, y=0.2, height=20.2, width=14.5, fill=BLACK, stroke=BLACK)

Rectangle(x=0.5, y=0.9, height=19, width=13.5, fill=BLACK, rounding=0.5,
          stroke_width=3, stroke=BLUE)
Stadium(x=1.1, y=0.5, height=0.7, width=12.3, fill=BLACK,
        stroke_width=2, stroke=BLUE)
Text(text="<b>I.</b> PLAY GREEN <b>II.</b> PLAY BLUE or RED <b>III.</b> ACTION <b>IV.</b> PRODUCE <b>V.</b> DRAW",
     style="font-family: Helvetica; font-size: 10pt; color: #78C9D1;",
     html=True, x=1, y=0.6, width=12.5, height=1)

# resource areas
rsrc = Common(x=7.5, width=6, rounding=0.1, stroke=None,
              hatch='w', hatch_stroke_width=2)
Rectangle(common=rsrc,
          y=1.4, height=6.8, fill=LT_YELLOW,
          hatch_stroke=DK_YELLOW, hatch_count=36,
          centre_shape=rectangle(
              height=0.9, width=0.9, fill="gold", stroke='dimgray', notch=0.1))
Rectangle(common=rsrc,
          y=8.8, height=3.1, fill=LT_RED,
          hatch_stroke=DK_RED, hatch_count=16,
          centre_shape=rectangle(height=0.9, width=0.9, fill="#E57847", stroke='dimgray'))
Rectangle(common=rsrc,
          y=12.4, height=3.1, fill=LT_GREEN,
          hatch_stroke=DK_GREEN, hatch_count=16,
          centre_shape=rectangle(height=0.9, width=0.9, fill="#8CC352", stroke='dimgray'))

# horizontal sections
seq_rsc = Common(
    height=0.9, width=0.9,
    notch=0.1, label="{{sequence}}",
    label_size=15, label_stroke="dimgray")

Sequence(
    rectangle(common=seq_rsc, y=2.0, x=1.1, fill_stroke=LT_YELLOW),
    setting=(5, 9, 1, 'number'),
    interval_x=0.9)
Sequence(
    rectangle(common=seq_rsc, y=3.5, x=1.1, fill_stroke=LT_YELLOW),
    setting=(0, 4, 1, 'number'),
    interval_x=0.9)

Sequence(
    rectangle(common=seq_rsc, y=5.6, x=1.1, fill_stroke=LT_BLUE),
    setting=(5, 9, 1, 'number'),
    interval_x=0.9)
Sequence(
    rectangle(common=seq_rsc, y=7.1, x=1.1, fill_stroke=LT_BLUE),
    setting=(0, 4, 1, 'number'),
    interval_x=0.9)

Sequence(
    rectangle(common=seq_rsc, y=9.2, x=1.1, fill_stroke=LT_RED),
    setting=(5, 9, 1, 'number'),
    interval_x=0.9)
Sequence(
    rectangle(common=seq_rsc, y=10.7, x=1.1, fill_stroke=LT_RED),
    setting=(0, 4, 1, 'number'),
    interval_x=0.9)

Sequence(
    rectangle(common=seq_rsc, y=12.9, x=1.1, fill_stroke=LT_GREEN),
    setting=(5, 9, 1, 'number'),
    interval_x=0.9)
Sequence(
    rectangle(common=seq_rsc, y=14.4, x=1.1, fill_stroke=LT_GREEN),
    setting=(0, 4, 1, 'number'),
    interval_x=0.9)

Sequence(
    rectangle(common=seq_rsc, y=16.5, x=1.1, fill_stroke=LT_BROWN),
    setting=(5, 9, 1, 'number'),
    interval_x=0.9)
Sequence(
    rectangle(common=seq_rsc, y=18.0, x=1.1, fill_stroke=LT_BROWN),
    setting=(0, 4, 1, 'number'),
    interval_x=0.9)

Sequence(
    rectangle(common=seq_rsc, y=16.5, x=7.5, fill_stroke=LT_GREY),
    setting=(5, 9, 1, 'number'),
    interval_x=0.9)
Sequence(
    rectangle(common=seq_rsc, y=18.0, x=7.5, fill_stroke=LT_GREY),
    setting=(0, 4, 1, 'number'),
    interval_x=0.9)

# vertical sections
seq_vert = Common(
    height=0.9, width=0.9,
    notch=0.1, label="{{sequence}}",
    label_size=15, label_stroke="dimgray")

Sequence(
    rectangle(common=seq_vert, y=1.8, x=6.1, fill_stroke=LT_YELLOW),
    setting=(30, 10, -10, 'number'),
    interval_y=0.9)
Sequence(
    rectangle(common=seq_vert, y=5.4, x=6.1, fill_stroke=LT_BLUE),
    setting=(30, 10, -10, 'number'),
    interval_y=0.9)
Sequence(
    rectangle(common=seq_vert, y=9.0, x=6.1, fill_stroke=LT_RED),
    setting=(30, 10, -10, 'number'),
    interval_y=0.9)
Sequence(
    rectangle(common=seq_vert, y=12.7, x=6.1, fill_stroke=LT_GREEN),
    setting=(30, 10, -10, 'number'),
    interval_y=0.9)
Sequence(
    rectangle(common=seq_vert, y=16.8, x=6.1, fill_stroke=LT_BROWN),
    setting=(20, 10, -10, 'number'),
    interval_y=0.9)
Sequence(
    rectangle(common=seq_vert, y=16.8, x=12.5, fill_stroke=LT_GREY),
    setting=(20, 10, -10, 'number'),
    interval_y=0.9)

Rectangle(x=1.5, y=19, height=1, width=11.5, fill_stroke=BLACK)

# cash
Font("Helvetica-Bold")
money = Common(
    y=19.5, side=0.6, fill="gold", stroke='black', notch=0.08)
Square(common=money, x=1.7, label="20")
Square(common=money, x=4.2, label="14")
Square(common=money, x=11, label="15")

# resource icons
Font("game-icons-net-20200315a")
Text(text="\uE8A4", y=5, x=10.5, stroke="goldenrod")  # coin
Text(text="\uE6C5", y=10.5, x=10.5, stroke="yellow")  # fire
Text(text="\uEC14", y=14.1, x=10.5, stroke=LEAF)  # leaf

# TODO - icons and text at the bottom
forest = Common(
    cy=19.8, label="\uEC14", orientation="pointy",
    height=0.5, fill_stroke=LT_GREEN)
Hexagon(common=forest, cx=3.2)
Hexagon(common=forest, cx=8)
Square(y=19.5, x=6.5, side=0.6, fill_stroke=LT_GREEN)
water = Common(
    cy=19.8, label="\uE494", orientation="pointy",
    height=0.5, fill_stroke=LT_BLUE)
Hexagon(common=water, cx=12.6)


arrow = Common(
    y=19.8, length=0.4, arrow_style='notch',
    arrow_height=0.3,
    arrow_width=0.3,
    stroke="red", stroke_width=2.5)
Line(common=arrow, x=2.4)
Line(common=arrow, x=7.2)
Line(common=arrow, x=4.9)
Line(common=arrow, x=9.9)
Line(common=arrow, x=11.8)

Save()
