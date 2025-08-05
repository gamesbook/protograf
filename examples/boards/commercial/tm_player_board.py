"""
"Terraforming Mars: Ares Expedition" player board example for protograf

Written by: Derek Hohls
Created on: 4 August 2025
Notes:

    * Icon Font `game-icons-net-20200315a` from
      https://github.com/toddfast/game-icons-net-font
"""
from protograf import *

Create(filename="tm_player_board.pdf", margin=0.1, paper="A5", fill="black")

BLACK = "#18181A"
BLUE = "#78C9D1"
LT_GREEN = "#8BB846"
DK_GREEN = "#77A943"
LT_RED = "#FA903A"
DK_RED = "#F37C37"
LT_YELLOW = "#FFC32C"
DK_YELLOW = "#E1C82E"

Rectangle(x=0, y=0.2, height=20.2, width=14.5, fill=BLACK, stroke=BLACK)

Rectangle(x=0.5, y=0.9, height=19, width=13.5, fill=BLACK, rounding=0.5,
          stroke_width=3, stroke=BLUE)
Stadium(x=1.1, y=0.5, height=0.7, width=12.3, fill=BLACK,
        stroke_width=2, stroke=BLUE)

# resource areas
rsrc = Common(x=7.5, width=6, rounding=0.1, stroke=None,
              hatch='w', hatch_width=2)
Rectangle(common=rsrc,
          y=1.4, height=6.8, fill=LT_YELLOW,
          hatch_stroke=DK_YELLOW, hatch_count=36)
Rectangle(common=rsrc,
          y=12.4, height=3.1, fill=LT_GREEN,
          hatch_stroke=DK_GREEN, hatch_count=16)
Rectangle(common=rsrc,
          y=8.8, height=3.1, fill=LT_RED,
          hatch_stroke=DK_RED, hatch_count=16)

# Extract("1", cols_rows="2,2", names=["q1", "q2", "q3", "q4"])

Save()
