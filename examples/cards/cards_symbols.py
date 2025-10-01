"""
`cards_symbols` example for protograf

Written by: Derek Hohls
Created on: 30 September 2025
"""
from protograf import *

Create(
   filename='cards_symbols.pdf',
   margin=1.25,
   paper="A6")

# deck data
lotr = [
    ['ID', 'Name', 'Age', 'Race', 'Ability', 'Copies'],
    [1, "Gimli", 140, "Dwarf",
     "Gain 1 |!\u2666 12 red!| per turn", 1],
    [6, "Merry", 37, "Hobbit",
     "Gain 1 |!\uEB73 12 green!| per round", 1],
    [7, "Samwise", 39, "Hobbit",
     "Gain 1 |;openmoji--fish 14;| per turn", 1],
    [9, "Gollum", None, "Hobbit",
     "Use 2 |:openmoji--fish 12:| to get 1 |!\u2666 12 blue!|", 1],
]
Data(data_list=lotr)

# design the deck
Deck(
    cards=1,
    height=6, width=4,
    grid_marks=True,
    rounding=0.3,
    fill=None,
    stroke="gray",
    copy='Copies')

# character Name
name_box = rectangle(
    x=0.5, y=0.5,
    width=3, height=1,
    rounding=0.2)
Card("*", name_box)
Card("all",
     text(
         text=T("{{ Name }}"),
         x=2, y=1.2,
         font_size=14))

# character Ability
IconFont("game-icons-net-20200315a")
able = text(
    x=0.25, y=2,
    width=3.5, height=2,
    font_size=10,
    box_fill="lightgrey",
    html=True,
    text=T("{{ Ability }}")
)
Card("all", able)


Save()
