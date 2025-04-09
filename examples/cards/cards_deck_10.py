"""
Deck design Example 10 for protograf

Written by: Derek Hohls
Created on: 8 January 2025
"""
from protograf import *

Create(filename='cards_deck_10.pdf', margin=0.25, paper="A8")

# design deck
Deck(
    cards=6,
    radius=1,
    bleed_fill="lightsteelblue",
    offset=0.15,
    grid_marks=True,
    grid_length=0.18,
    spacing=0.15,
    frame='circle'
    )
# design card
Card(
    '*',
    rectangle(
        x=0.3, y=0.3, width=1.4, height=1.4, stroke_width=1, rounding=0.2,
        label_size=10, label='{{sequence}}\n{{id}}'),
)
# create output
Save(
     output='png',
     dpi=300,
     directory="../docs/source/images/decks",
     names=['cards_deck_10']
)
