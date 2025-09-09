"""
Show customised Rectangle for protograf

Written by: Derek Hohls
Created on: 17 November 2024
"""

from protograf import *

Create(filename="customised_commands.pdf",
       paper="A8",
       margin_left=0.5,
       margin_right=0.3,
       margin_bottom=0.2,
       margin_top=0.5,
       font_size=8,
       stroke_width=0.5)

txt = Common(x=0, y=0, font_size=8, align="left")

Text(common=txt, text="Commands START...")
PageBreak()

# ---- loop and if
Blueprint()
Text(common=txt, text="Loop and If")
for count in range(1, 5):
    if count < 3:
        Circle(x=1, y=count, label=count)
    else:
        Rectangle(x=1, y=count, label=count)
PageBreak()

# ---- functions
def capitol(a=0, b=1, c="red"):
    Circle(cx=a+1, cy=b, radius=0.5, fill_stroke=c)
    Rectangle(x=a, y=b, height=1, width=2, fill_stroke=c,
              notch_y=0.1, notch_x=0.5, notch_directions="nw ne",)
    EquilateralTriangle(cx=a+1, cy=b-0.5, side=0.25, fill_stroke=c)

Blueprint()
Text(common=txt, text="Function")
capitol()
capitol(a=1, b=3, c="gold")
capitol(a=2, b=5, c="chartreuse")
PageBreak()

Blueprint()
Text(common=txt, text="Font Command")
Font("Helvetica", size=9, stroke="gold")
Text(text="Helvetica 9pt gold", x=0, y=1, align="left")
Font("Courier", size=10, stroke="cyan")
Text(text="Courier 10pt aqua", x=0, y=2, align="left")
Font("Times-Roman", size=11, stroke="tomato")
Text(text="Times-Roman 11pt red", x=0, y=3, align="left")
Font("Arial", size=12, stroke="black")
Text(text="Arial 12pt black", x=0, y=4, align="left")
PageBreak()

# ---- END
Text(common=txt, text="Command END...")

Save(
     output='png',
     dpi=300,
     directory="../docs/source/images/custom/commands",
     names=[
        None,
        "loop", "function", "fonts",
        None])
