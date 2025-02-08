# -*- coding: utf-8 -*-
"""
Example code for protograf

Written by: Derek Hohls
Created on: 19 August 2024
"""
from protograf import *

Create(filename="objects.pdf", margin=1, margin_top=0.25)

header = Common(x=0, y=27, font_size=24, align="left")
header_font = Common(font_size=16, align="left")

# ---- PAGE 1 ===>

Text(common=header, text="Miscellaneous Objects #1")
#Blueprint()

Text(common=header_font, x=6, y=23, text="Coin: circle with step-created radii + an inner circle")
# circles 24 radii - i.e. one every 15 degrees
Circle(cx=3, cy=23, radius=2, fill=skyblue, stroke_width=2, radii=steps(0,360,15))
Circle(cx=3, cy=23, radius=1.5, fill=skyblue, label="5", font_size=48)

Text(align="left", x=9, y=20, wrap=True, width=10, height=4, font_size=16,
     text='<b>Warning Sign:</b> rounded rectangles plus a sequence of "E" (east) chevrons')
Rectangle(x=1, y=17, width=7.5, height=3, rounded=0.5, stroke=black, fill=black)
Rectangle(x=1.1, y=17.1, width=7.3, height=2.8, rounded=0.5, stroke_width=2, stroke=yellow, fill=None)
Sequence(
    rectangle(x=1.5, y=17.1, width=1, height=2.8,
              chevron='E', chevron_height=1, stroke=yellow, fill=yellow),
    setting=(1, 3),
    interval_x=2,
)

Text(common=header_font, x=5, y=15, text="Leaded Window: rectangle with diagonal hatches")
Rectangle(
    x=2, y=13.5,
    height=3, width=2,
    hatch_count=7, hatch_width=0.1, hatch='d', hatch_stroke=black,
    stroke=saddlebrown, stroke_width=2, fill=lightcyan)

Text(common=header_font, x=5, y=11, text="Paned Window: rectangle with single orthogonal hatch")
Rectangle(
    x=2, y=9.5,
    height=3, width=2,
    hatch_count=1, hatch_width=1, hatch='o', hatch_stroke=sienna,
    stroke=sienna, stroke_width=3, fill=lightcyan)

Text(common=header_font, x=5, y=7, text="Start Player Token: circles + radii using steps() function")
Polygon(cx=3, cy=7.5, height=3, sides=8, fill=black)
Circle(x=1.75, y=6.25, fill=black, radius=1.25,
       radii=[0,45,90,135,180,225,270,315], radii_stroke=gold, radii_stroke_width=2)
Circle(x=2.5, y=7, stroke=black, fill=gold, radius=0.5, stroke_width=5)

Text(common=header_font, x=5, y=3, text="Doorway: stadiums, dashline + radii")
Stadium(x=1.5, y=1, height=3, width=3, fill=skyblue, stroke=darkgrey, stroke_width=8, edges="n")
Stadium(x=1.503, y=1.003, height=3.003, width=3.003, fill=None, edges="n",
        stroke=fidred, stroke_width=5,
        dashed=[0.3, 0.05, 0.05, 0.0],)
Circle(cx=3, cy=4, stroke=sienna, stroke_width=5, fill=skyblue, radius=1.3,
       radii=[30,90,150], radii_stroke=sienna, radii_stroke_width=3)
Circle(cx=3, cy=4, stroke=sienna, stroke_width=5, fill=sienna, radius=0.3)
Rectangle(x=1.7, y=0.9, height=3, width=2.6,
          stroke=sienna, stroke_width=5, fill=skyblue)
PageBreak()

# ---- PAGE 2 ===>

Text(common=header, text="Miscellaneous Objects #2")
#Blueprint()

Text(common=header_font, x=5, y=25, text="Wormhole: rotation, nested hexagons")
poly6 = Common(x=2, y=25, fill=None, sides=6, stroke_width=1)
Polygon(common=poly6, radius=1.50)
Polygon(common=poly6, radius=1.35, rotation=15)
Polygon(common=poly6, radius=1.20, rotation=30)
Polygon(common=poly6, radius=1.05, rotation=45)
Polygon(common=poly6, radius=1.05, rotation=60)
Polygon(common=poly6, radius=0.90, rotation=15)
Polygon(common=poly6, radius=0.75, rotation=30)
Polygon(common=poly6, radius=0.60, rotation=45)
Polygon(x=2, y=25, fill=black, radius=0.60, rotation=60)

Text(common=header_font, x=5, y=22,
     text="XOK Fish: nested circles with 2 thick offset radii")
Circle(cx=2, cy=22, radius=1,
       fill="#63B1BB", stroke="#63B1BB",
       radii=[135,225],
       radii_offset=1.05, radii_length=0.4, radii_stroke=white, radii_stroke_width=15)
Circle(cx=2, cy=22, radius=0.75, fill="#63B1BB", stroke="#63B1BB")
Dot(x=2.5, y=22.5, stroke=white, dot_point=3)

Text(common=header_font, x=5, y=19, text="Gear: nested circles; one with 8 offset radii")
Circle(cx=2, cy=19, radius=0.5,
       fill=None, stroke=grey, stroke_width=8,
       radii=[0,45,90,135,180,225,270,315],
       radii_offset=0.8, radii_length=0.2, radii_stroke=grey, radii_stroke_width=8)
Circle(cx=2, cy=19, radius=0.15, fill_stroke=grey)

Text(common=header_font, x=5, y=16, text="Atom: ellipses with rotation; circle")
atom = Common(cx=2, cy=16, width=3, height=1, stroke_width=1, outline=red)
for degrees in [30,150,270]:
    Ellipse(common=atom, rotation=degrees)
Circle(cx=2, cy=16, radius=0.2, fill_stroke=red)

Text(common=header_font, x=5, y=12.5,
     text="German Cross: rectangle with 'o' hatch and 'step' notch")
Rectangle(
    height=2.8, width=2.8, x=0.5, y=11, fill=white, stroke=black, stroke_width=2,
    hatch_width=22, hatch_stroke=black, hatch='o', hatch_count=1,
    notch=0.7, notch_style='step')
Rectangle(
    height=2.8, width=2.8, x=0.5, y=11, fill=None, stroke=white, stroke_width=3)

Text(common=header_font, x=5, y=9,
     text="Mars Base: rectangle borders; circles with offset radii")
Circle(cx=1, cy=9, radius=0.8, fill=lightcoral, stroke=firebrick, stroke_width=6)
Circle(cx=3.5, cy=9, radius=0.8, fill=lightcoral, stroke=firebrick, stroke_width=6)
Rectangle(
    x=1.55, y=8.5, height=1, width=1.4, fill=lightcoral, stroke=None,
    borders=("n s", 6, firebrick))
Circle(cx=1, cy=9, radius=0.35, fill=None, stroke=firebrick, stroke_width=1,
       radii=[33, 90, 150, 210, 270, 327], radii_offset=0.7,
       radii_stroke_width=1, radii_stroke=firebrick)
Circle(cx=3.5, cy=9, radius=0.35, fill=None, stroke=firebrick, stroke_width=1,
       radii=[30, 90, 147, 213, 270, 330], radii_offset=0.7,
       radii_stroke_width=1, radii_stroke=firebrick)

Text(common=header_font, x=7, y=7, text="Sets of check boxes (loop + sequence)")
for s in steps(0, 6, 2.2):
    Sequence(
        [rectangle(fill_stroke=black, x=s+0.05, y=6.95, height=0.5, width=0.5),
         rectangle(stroke=black, x=s+0, y=7, height=0.5, width=0.5)],
        setting=(1, 3),
        interval_x=0.6)

Save(output='png')
