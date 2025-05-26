"""
`cards_images` example for protograf

Written by: Derek Hohls
Created on: 29 April 2024
"""
from protograf import *

Create(filename='cards_images.pdf', margin_bottom=1.5, stroke="white", stroke_width=0.01)

# load image data
Data(images="pictures", images_filter=".png,.jpg")

# create the deck with default size cards
# * card count will be based on number of images loaded via Data()
Deck(grid_marks=True, width=6.2, height=8.3)

# add an image to each card
img = image("*", x=0, y=-0.2, width=6.3, height=8.8)
Card('*', img)

# card back
rect = rectangle(
    x=0.65, y=0.5, height=7.3, width=5, fill="black",
    rounded=True)
CardBack("*", rect)

Save()
