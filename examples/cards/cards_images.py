"""
`cards_images` example for protograf

Written by: Derek Hohls
Created on: 29 April 2024
"""
from protograf import *

Create(filename='cards_images.pdf', margin_bottom=1.5)

# load image data
Data(images="pictures", images_filter=".png,.jpg")

# create the deck with default size cards
# * card count will be based on number of images loaded via Data()
Deck(grid_marks=True)

# add an image to each card
img = image("*", x=0, y=0, width=6.3, height=8.8)
rct = rectangle(fill_stroke=None)
layout = group(rct, img)
Card('*', layout)

# FIXME - should be:
# img = image("*", x=0, y=0, width=6.3, height=8.8)
# Card('*', img)

Save()
