"""
`cards6` example for protograf

Written by: Derek Hohls
Created on: 29 February 2016
"""
from protograf import *

Create(filename="example6.pdf", offset=0.5)

# deck design - a "template" that all cards will use
Deck(cards=9,
     fill=teal,
     radius=3,
     grid_marks=True,
     shape='circle')

times = Common(font_name="Times-Roman", font_size=48, stroke=white, x=3, y=2.5)

# create a list of text elements for the cards, containing single letters
mytext1 = text(text=letters("D", "L"), common=times)

# specify a range of cards to contain these letters
Card("1-9", mytext1)

# create the output file
Save()
