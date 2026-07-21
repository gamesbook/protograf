"""
`cards6` example for protograf

Written by: Derek Hohls
"""
from protograf import *

Create(filename="example6.pdf", offset=0.5)

# deck design - a "template" that all cards will use
Deck(
    cards=6,
    fill="teal",
    radius=3,
    grid_marks=True,
    frame='circle')

times = Common(font_name="Times-Roman", font_size=48, stroke="white", x=3, y=3.5)

# create a list of text elements for the cards, containing single letters
mytext1 = letters("D", "L")

# create cards to contain these letters
Card("1", text(text=mytext1[0], common=times))
Card("2", text(text=mytext1[1], common=times))
Card("3", text(text=mytext1[2], common=times))
Card("4", text(text=mytext1[3], common=times))
Card("5", text(text=mytext1[4], common=times))
Card("6", text(text=mytext1[5], common=times))

# create the output file
Save()
