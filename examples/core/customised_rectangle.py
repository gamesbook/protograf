"""
Show customised Rectangle for protograf

Written by: Derek Hohls
Created on: 19 September 2024
"""

from protograf import *

Create(filename="customised_rectangle.pdf",
       paper="A8",
       margin=0.75,
       margin_right=0.2, margin_top=0.2,
       font_size=8,
       stroke_width=0.5)

Footer(draw=False)

txt = Common(x=0, y=6, font_size=8, align="left")

Text(common=txt, text="Rectangle START...")
PageBreak(footer=True)

# ---- centre placement
Blueprint()
Text(common=txt, text="Rectangle: cx=2, cy=3")
Rectangle(cx=2, cy=3)
PageBreak()

# ---- notches
Blueprint()
Text(common=txt, text="Rectangle & Notches")
Rectangle(
    x=2, y=1,
    height=2, width=1,
    notch=0.25,
    label="notch:0.5",
    label_size=5,
    )
Rectangle(
    x=1, y=4,
    height=1, width=2,
    notch_y=0.25,
    notch_x=0.5,
    notch_corners="NW SE",
    label="notch:.25/.5 loc: NW, SE",
    label_size=5,
    )
PageBreak()

# ---- dot & cross
Blueprint()
Text(common=txt, text="Rectangle: dot & cross")
Rectangle(height=3, width=2, cross=0.75, dot=0.15)
PageBreak()

# ---- hatches
Blueprint()
Text(common=txt, text="Rectangle: hatches + directions")
htch = Common(height=1.5, width=1, hatch_count=5, hatch_width=0.1, hatch_stroke="red")
Rectangle(common=htch, x=0, y=0,  hatch='w', label="W")
Rectangle(common=htch, x=1.5, y=0, hatch='e', label="E")
Rectangle(common=htch, x=3, y=0, hatch='ne', label="NE\nSW")

Rectangle(common=htch, x=1.5, y=2, hatch='n', label="N")
Rectangle(common=htch, x=0, y=2,  hatch='s', label="S")
Rectangle(common=htch, x=3, y=2, hatch='nw', label="NW\nSE")

Rectangle(common=htch, x=0, y=4, label="all")
Rectangle(common=htch, x=1.5, y=4, hatch='o', label="O")
Rectangle(common=htch, x=3, y=4, hatch='d', label="D")

PageBreak()

# ---- rounding + hatches
Blueprint()
Text(common=txt, text="Rectangle: rounding; hatches")
rct = Common(x=0.5, height=1.5, width=3.0, stroke_width=.5,
             hatch_stroke="red", hatch='o')
Rectangle(common=rct, y=0.0, rounding=0.1, hatch_count=10)
Rectangle(common=rct, y=2.0, rounding=0.5, hatch_count=3)
# Rectangle(common=rct, y=4.0, rounding=0.75, hatch_count=15)  # FAILS!
PageBreak()

# ---- chevron
Blueprint()
Text(common=txt, text="Rectangle: chevron")
Rectangle(
    x=3, y=2,
    height=2, width=1,
    font_size=4,
    chevron='N',
    chevron_height=0.5,
    label="chevron:N:0.5",
    title="title-N",
    heading="head-N",
    )
Rectangle(
    x=0, y=2,
    height=2, width=1,
    font_size=4,
    chevron='S',
    chevron_height=0.5,
    label="chevron:S:0.5",
    title="title-S",
    heading="head-S",
    )
Rectangle(
    x=1, y=4.5,
    height=1, width=2,
    font_size=4,
    chevron='W',
    chevron_height=0.5,
    label="chevron:W:0.5",
    title="title-W",
    heading="head-W",
    )
Rectangle(
    x=1, y=0.5,
    height=1, width=2,
    font_size=4,
    chevron='E',
    chevron_height=0.5,
    label="chevron:E:0.5",
    title="title-E",
    heading="head-E",
    )
PageBreak()

# ---- peaks
Blueprint()
Text(common=txt, text="Rectangle: peaks")
Rectangle(x=1, y=1, width=2, height=1, peaks=[("*",0.2)], font_size=6, label="peaks = *")
Rectangle(x=1, y=4, width=2, height=1.5, peaks=[("s",1), ("e",0.25)], font_size=6, label="points = s")
PageBreak()

# ---- rotation
Blueprint()
Text(common=txt, text="Rectangle: red => rotation 45\u00B0")
Rectangle(cx=2, cy=3, width=1.5, height=3, dot=0.06)
Rectangle(cx=2, cy=3, width=1.5, height=3, fill=None,
          stroke="red", stroke_width=.3, rotation=45, dot=0.04)
PageBreak()

# ---- notches
Blueprint()
Text(common=txt, text="Rectangle : Notch Styles")
styles = Common(height=1, width=3.5, x=0.25, notch=0.25, label_size=7, fill=silver)
Rectangle(common=styles, y=0, notch_style='snip', label='Notch: snip (s)')
Rectangle(common=styles, y=1.5, notch_style='step', label='Notch: step (t)')
Rectangle(common=styles, y=3, notch_style='fold', label='Notch: fold (o)')
Rectangle(common=styles, y=4.5, notch_style='flap', label='Notch: flap (l)')
# Rectangle(common=styles, y=5, label='Notch: bite (NOT WORKING)')
PageBreak()

# ---- rectangle - borders
Blueprint(stroke_width=0.5)
Text(common=txt, text="Rectangle: borders")
Rectangle(
    y=3, height=2, width=2, stroke=None, fill="gold",
    borders=[
        ("n", 3, silver, True),
        ("s", 2),
    ]
)
Rectangle(
    y=0, height=2, width=2, stroke_width=1.9,
    borders=[
        ("w", 2, gold),
        ("n", 2, lime, True),
        ("e", 2, tomato, [0.1,0.2,0.1,0]),
    ]
)
PageBreak()

# ---- END
Text(common=txt, text="Rectangle END...")
PageBreak(footer=True)

Save(
     output='png',
     dpi=300,
     directory="../docs/source/images/custom/rectangle",
     names=[
        None,
        "centre", "notch", "dot_cross", "hatch", "rounding", "chevron",
        "peak", "rotation", "notch_style", "borders",
        None])
