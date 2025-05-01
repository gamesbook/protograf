"""
`cards5` example for protograf

Written by: Derek Hohls
Created on: 29 February 2016
"""
from protograf import *

Create(filename="example5.pdf", margin_bottom=2.5)

# deck design - a "template" that all cards will use
Deck(cards=50,
     fill=indigo,
     height=5,
     width=3.8,
     grid_marks=True,
     rounded=True)

times = Common(font_name="Times-Roman", font_size=48, stroke="white", x=1.9, y=2)

# create a list of text elements for the cards, containing single letters
mytext1 = text(text=letters("A", "Y"), common=times)
mytext2 = text(text=split("A B C D E F G H J K L M N O P Q R S T U V W X Y Z"),
               common=times)

# specify a range of cards to contain these letters
Card("1-25", mytext1)
Card("26-50", mytext2)

# create the output file
Save()
