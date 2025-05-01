"""
`cards4` example for protograf

Written by: Derek Hohls
Created on: 29 February 2016
"""
from protograf import *

# create the output card file
Create(filename='example4.pdf', margin_bottom=2.5)

# create a deck design
Deck(cards=25,
     fill="skyblue",
     stroke="white",
     height=5,
     width=3.8)

# create some text, with the default font, and centre it at a location
mytext = text(text="25!", point=(1.9, 2.5))

# customize a specific card (number 25) in the deck with 'mytext'
Card("25", mytext)

# specify and store a specifx font; using face, size and color
times = Common(font_name="Times-Roman", font_size=8, stroke="red")

# create more text, and display it using font stored in 'times'
mytext2 = text(x=1.9, y=1, text="I'm on cards 1-10", common=times)

# specify a range of cards to contain 'mytext2'
Card("1-10", mytext2)

# create the output file
Save()
