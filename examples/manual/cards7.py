"""
`cards7` example for protograf

Written by: Derek Hohls
"""
from protograf import *

Create(
    filename="example7.pdf",
    margin_bottom=1.5,
    margin_left=2.5,
    paper="A4-l")

# deck design - a "template" that all cards will use
Deck(
    cards=9,
    fill="darkgreen",
    height=6,
    grid_marks=True,
    frame="hexagon")

times = Common(font_name="Times-Roman", font_size=48, stroke="white", x=3.5, y=3.5)

# create a list of text elements for the cards
mytext = ["N", "S", "!", "A", "G", "O", "H", "E", "X"]

# create a range of cards to contain these letters
# using "built-in" Python grammar
for key, letter in enumerate(mytext):
    Card(key + 1, text(letter, common=times))

# create the output file
Save()
