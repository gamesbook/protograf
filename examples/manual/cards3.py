"""
`cards3` example for protograf

Written by: Derek Hohls
Created on: 29 February 2016
"""
from protograf import *

Create(filename="example3.pdf", margin_bottom=2.5)

# deck design - a "template" that all cards will use
Deck(cards=50,
     fill="#702EB0",
     height=5,
     width=3.8)

# create the output card file, using the card 'deck'
Save()
