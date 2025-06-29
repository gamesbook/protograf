"""
Deck design Example 12 for protograf

Written by: Derek Hohls
Created on: 20 February 2025
"""
from protograf import *

Create(filename='cards_deck_12.pdf', margin=0.25, paper="A8")

# design deck
Deck(
    cards=6,
    #radius=1,
    height=2, width=2,
    bleed_fill="lightsteelblue",
    offset=0.15,
    grid_marks=True,
    grid_marks_length=0.2,
    spacing=0.15,
    )
# design card
Card(
    '*',
    rectangle(
        x=0.3, y=0.3, width=1.4, height=1.4,
        stroke_width=1, rounding=0.2,
        fill="white",
        label_size=11,
        label='{{sequence}}\n{{id}}'),
)
# create output
Save(
     output='png',
     dpi=300,
     directory="../docs/source/images/decks",
     names=['cards_deck_12',]
)
