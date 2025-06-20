"""
Page annotation (grid and margins) example for protograf

Written by: Derek Hohls
Created on: 13 June 2025
"""
from protograf import *

# create deck
Create(filename="blank.pdf",
       paper='A8',
       margin=0.5,
       stroke_width=0.5,
       page_grid=0.5,
       margin_debug=True,
)

# Save()
Save(
    output='png',
    dpi=300,
    directory="../docs/source/images/customised",
    names=[
        "blank_grid",
    ]
)
