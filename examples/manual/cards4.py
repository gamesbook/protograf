"""
`cards4` example for pyprototypr

Written by: Derek Hohls
Created on: 29 February 2016
"""
from pyprototypr.draw import *

# create the output card file
Create(filename='example4.pdf', offset=0.5)

# create a deck design
Deck(cards=25,
     fill=skyblue,
     stroke=white,
     height=5,
     width=3.8)

# create some text, with the default font, and centre it at a location
mytext = text(text="25!", point=(1.9, 1.0))

# customize a specific card (number 25) in the deck with 'mytext'
Card("25", mytext)

# specify a particular font; face and size and color
times = Common(font_face="Times New Roman", font_size=8, stroke=red)

# create more text, and display it using 'times' font
mytext2 = text(x=1.9, y=1, text="I'm on cards 1-10", common=times)

# specify a range of cards to contain 'mytext2'
Card("1-10", mytext2)

# save to file
Save()
