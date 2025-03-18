"""
PNG to GIF example for protograf

Written by: Derek Hohls
Created on: 1 December 2024
"""
from protograf import *

Create(filename="rolling.pdf",
       paper="A8",  #A8
       margin=0.75, margin_right=0.25, margin_top=0.25,
       font_size=8,
       stroke_width=0.5,
       )

# ---- commons
header = Common(x=0, y=6, font_size=8, align="left")

# ---- line 1
text = 'never gonna give you up'
for squares in range(len(text) + 1):
    y = 1
    z = 0.5
    Blueprint()
    Text(common=header, text="rolling")
    for t in range(squares):
        z = z + 0.5
        if text[t] == ' ':
            y = y + 1
            z = 0.5
            continue
        Rectangle(side=0.5, rounding=0.1, x=z, y=y, label=text[t])
    PageBreak()

# ---- line 2
text = 'never gonna let you down'
for squares in range(len(text) + 1):
    y = 5
    z = 0.5
    Blueprint()
    Text(common=header, text="rolling")
    for t in range(squares):
        z = z + 0.5
        if text[t] == ' ':
            y = y - 1
            z = 0.5
            continue
        Rectangle(side=0.5, rounding=0.1, x=z, y=y, label=text[t])
    PageBreak()

Save(
    output='gif',
    directory="../docs/source/examples/images/various",
    dpi=300,
    framerate=0.1, # seconds-delay-per-frame
)
