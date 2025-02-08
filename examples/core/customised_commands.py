"""
Show customised Rectangle for protograf

Written by: Derek Hohls
Created on: 17 November 2024
"""

from protograf import *

Create(filename="customised_commands.pdf",
       paper=A8,
       margin=0.75,
       margin_right=0.2, margin_top=0.2,
       font_size=8,
       stroke_width=0.5)

txt = Common(x=0, y=6, font_size=8, align="left")

Text(common=txt, text="Commands START...")
PageBreak(footer=True)

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
def capitol(a=0, b=0, c=red):
    Circle(cx=a+1, cy=b+1, radius=0.5, fill_stroke=c)
    Rectangle(x=a, y=b, height=1, width=2, fill_stroke=c,
              notch_y=0.1, notch_x=0.5, notch_corners="nw ne",)
    EquilateralTriangle(cx=a+1, cy=b+1.5, side=0.25, fill_stroke=c)

Blueprint()
Text(common=txt, text="Function")
capitol()
capitol(a=1, b=2, c=gold)
capitol(a=2, b=4, c=lime)
PageBreak()

Blueprint()
Text(common=txt, text="Font Command")
Font("Helvetica")
Text(text="Helvetica 12pt black", x=0, y=5, align="left")
Font("Times-Roman", size=11, stroke=tomato)
Text(text="Times-Roman 11pt red", x=0, y=4, align="left")
Font("Courier", size=10, stroke=aqua)
Text(text="Courier 10pt aqua", x=0, y=3, align="left")
Font("Verdana", size=9, stroke=gold)
Text(text="Verdana 9pt gold", x=0, y=2, align="left")
PageBreak()


# ---- END
Text(common=txt, text="Command END...")
PageBreak(footer=True)

Save(
     output='png',
     dpi=300,
     directory="docs/source/images/custom/commands",
     names=[
        None,
        "loop", "function", "fonts",
        None])
