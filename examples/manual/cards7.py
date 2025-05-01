"""
`cards7` example for protograf

Written by: Derek Hohls
Created on: 29 February 2016
"""
from protograf import *

Create(
   filename="example7.pdf",
   margin_bottom=1.5,
   margin_left=2.5,
   paper=landscape(A4))

# deck design - a "template" that all cards will use
Deck(cards=9,
     fill=darkgreen,
     height=6,
     grid_marks=True,
     frame='hexagon')

times = Common(font_name="Times-Roman", font_size=48, stroke="white", x=3.5, y=2.5)

# create a list of text elements for the cards
mytext1 = text(text=["N","S","!","A","G","O","H","E","X"], common=times)

# specify a range of cards to contain these letters
Card("1-9", mytext1)

# create the output file
Save()
