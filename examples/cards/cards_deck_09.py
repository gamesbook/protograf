"""
Deck design Example 09 for protograf

Written by: Derek Hohls
Created on: 8 January 2025
"""
from protograf import *

Create(filename='cards_deck_09.pdf', margin=0.25, paper="A8")

# design deck
Deck(
    cards=4,
    height=3.2,
    width=2.1,
    stroke=None,
    bleed_fill="lightsteelblue",
    offset=0.15,
    grid_marks=True,
    grid_marks_length=0.2,
    rows=1
    )
# design card
Card(
    '*',
    rectangle(
        x=0.2, y=0.2, width=1.7, height=2.8, stroke_width=1, rounding=0.2,
        label='{{sequence}}\n{{id}}'),
)
# create output
Save(
     output='png',
     dpi=300,
     directory="../docs/source/images/decks",
     names=['cards_deck_09', None]
)
