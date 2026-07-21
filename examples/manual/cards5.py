"""
`cards5` example for protograf

Written by: Derek Hohls
"""
from protograf import *

Create(filename="example5.pdf", margin_bottom=2.5)

# deck design - a "template" that all cards will use
Deck(
    cards=50,
    fill="indigo",
    height=5,
    width=3.8,
    grid_marks=True,
    rounded=True)

times = Common(font_name="Times-Roman", font_size=48, stroke="white", x=1.9, y=3)

mytext1 = text("1", common=times)
mytext2 = text("A", common=times)

# create ranges of cards to contain text
Card("1-25", mytext1)
Card("26-50", mytext2)

# create the output file
Save()
