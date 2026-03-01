"""
Deck design Example 13 for protograf

Written by: Derek Hohls
Created on: 8 January 2025
"""
from protograf import *

Create(filename='cards_deck_13.pdf', margin=0.25, paper="A8")

# design deck
Deck(
    cards=4,
    height=2.1,
    width=3.2,
    bleed_fill="lightsteelblue",
    #offset=0.15,
    grid_marks=True,
    grid_marks_length=0.2,
    gutter=0.4
    )
# design card
Card(
    '*',
    rectangle(
        x=0.2, y=0.2, width=2.8, height=1.7,
        stroke_width=1, rounding=0.2,
        label='{{sequence}}\n{{id}}'),
)
# design card back
CardBack(
    '*',
    rectangle(
        x=0.3, y=0.3, width=2.5, height=1.5,
        stroke_width=1, rounding=0.1,
        fill="yellowgreen",
        label='{{sequence}}*\n{{id}}'),
)
# create output
Save(
     output='png',
     dpi=300,
     directory="../docs/source/images/decks",
     names=['cards_deck_13', None, None, None]
)
