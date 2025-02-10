# -*- coding: utf-8 -*-
"""
A dynamic boardgame example for protograf

Written by: Derek Hohls
Created on: 2 December 2024
"""

from protograf import *

Create(filename="tictactoe.pdf", paper=A8, margin=0.2, stroke_width=0.5)

# board & pieces
rect = RectangularLocations(cols=3, rows=3, interval=1.25, y=2)
me = circle(radius=0.5, fill_stroke=white)
you = circle(radius=0.5, fill_stroke=black)
# turns
turns = [(me,1,1), (you,2,2), (me,1,3), (you,1,2), (me,2,1), (you,2,3), (me,3,1)]
shapes = []
locations = []
# create display
for number, turn in enumerate(turns):
    shapes = shapes + [turn[0]]
    locations = locations + [(turn[1], turn[2])]
    Text(x=1.5, y=5.5, font_size=7, align="left",
         text="TicTacToe #" + str(number + 1))
    Layout(rect, shapes=[rectangle(fill=lime, side=1.25)])
    Layout(rect, shapes=shapes, locations=locations)
    PageBreak()
# output
Save(
    output='gif',
    directory="../docs/source/examples/images/boards/abstract/",
    dpi='300',
    framerate=0.5)
