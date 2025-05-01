"""
PNG to GIF example for protograf; words credit to Rick Astley

Written by: Derek Hohls
Created on: 1 December 2024
"""
from protograf import *

Create(filename="rolling.pdf",
       paper="A8",
       margin_left=0.5,
       margin_right=0.3,
       margin_bottom=0.2,
       margin_top=0.5,
       font_size=8,
       stroke_width=0.5,
       )

# ---- commons
header = Common(x=0, y=0, font_size=8, align="left")

# ---- line 1
text = 'never gonna give you up'
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

# ---- line 2
text = 'never gonna let you down'
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

Save(
    output='gif',
    directory="../docs/source/examples/images/various",
    dpi=300,
    framerate=0.1,  # seconds-delay-per-frame
)
