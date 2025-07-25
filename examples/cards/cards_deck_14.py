"""
Deck design Example 14 for protograf

Written by: Derek Hohls
Created on: 20 July 2025
"""
from protograf import *

Create(filename='cards_deck_14.pdf', margin=0.25, paper="A8")

# design deck
page_header = text(
    text="protograf-cards_deck#14 // page:{{page}}",
    x=2.5, y=0.5, font_size=6, )
silver = rectangle(
     x=0.5, y=0.75, width=4, height=4,
     fill_stroke="silver")
gold = rectangle(
     x=0.5, y=3.75, width=4, height=3,
     fill_stroke="gold")
Deck(
    cards=32,
    width=0.65,
    height=0.65,
    offset=1,
    grid_marks=True,
    grid_marks_length=0.4,
    spacing_x=0.3,
    spacing_y=0.25,
    grouping_cols=2,
    grouping_rows=4,
    stroke=None,
    zones=[
        ('*', page_header),
        ('1', silver),
        ('1', gold)]
    )
# design card
Card(
    '1-16',
    rectangle(
        x=0.05, y=0.05, width=0.55, height=0.55,
        stroke_width=0.75, rounding=0.1, fill="silver",
        label='{{sequence}}'),
)
Card(
    '17-32',
    rectangle(
        x=0.05, y=0.05, width=0.55, height=0.55,
        stroke_width=0.75, rounding=0.1, fill="gold",
        label='{{sequence}}'),
)
# create output
Save(
     output='png',
     dpi=300,
     directory="../docs/source/images/decks",
     names=['cards_deck_14']
)
