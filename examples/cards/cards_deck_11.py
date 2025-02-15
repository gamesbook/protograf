"""
Deck design Example 11 for protograf

Written by: Derek Hohls
Created on: 15 February 2025
"""
from protograf import *

Create(filename='cards_deck_11.pdf', margin=0.25, paper=A8)

# design deck
Deck(
    cards=60,
    width=0.65,
    height=0.65,
    bleed_fill=silver,
    offset=0.15,
    grid_marks=True,
    grid_length=0.18,
    spacing_x=0.3,
    spacing_y=0.15,
    grouping_cols=2,
    grouping_rows=5,
    )
# design card
Card(
    '*',
    rectangle(
        x=0, y=0, width=0.65, height=0.65,
        stroke_width=1, rounding=0.1,
        label='{{sequence}}'),
)
# create output
Save(
     output='png',
     dpi=300,
     directory="../docs/source/images/decks",
     names=['cards_deck_11']
)
