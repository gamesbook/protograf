"""
Deck design Example 19 for protograf

Written by: Derek Hohls
Created on: 31 July 2025
"""
from protograf import *

Create(filename='cards_deck_15.pdf', margin=0.25, paper="A8")

# design deck
Deck(
    cards=4,
    height=3.2,
    width=2.1,
    card_grid=0.25)
# design card
Card(
    '*',
    rectangle(
        x=0.2, y=0.2, width=1.7, height=2.8, stroke_width=1, rounding=0.2,
        fill=None,
        label='{{sequence}}\n{{id}}')
)
# create output
Save(
     output='png',
     dpi=300,
     directory="../docs/source/images/decks",
     names=['cards_deck_15']
)
