# -*- coding: utf-8 -*-
"""
Example protograf code for creating various "real world" things

Written by: Derek Hohls
Created on: 19 August 2024

Credits:
    tmwtgg.jpg: https://unsplash.com/photos/tropical-islands-rise-from-the-emerald-green-ocean-5xMpaSXnBwc

"""
from protograf import *

Create(filename="objects.pdf",
       margin=1,
       margin_top=0.25)

header = Common(x=0, y=1, font_size=24, align="left")
header_font = Common(font_size=16, align="left")
fidred = "#CC0033"

# ---- PAGE 1 ===>

Text(common=header, text="Miscellaneous Things #1")


Text(common=header_font, x=6, y=4,
     text="Coin: circle with steps-created radii + inner circle")
# circles with 24 radii - i.e. one every 15 degrees
Circle(
   cx=3, cy=4, radius=2,
   fill="skyblue", stroke_width=2, radii=steps(0,360,15))
Circle(
   cx=3, cy=4, radius=1.5,
   fill="skyblue", label="5", font_size=48)


Text(align="left", x=9, y=8, wrap=True, width=10, height=4, font_size=16,
     text='Warning Sign: rounded rectangles + a sequence of "E" (east) chevrons')
Rectangle(x=1, y=7.8, width=7.5, height=3, rounded=0.5,
          stroke="black", fill="black")
Rectangle(x=1.1, y=7.9, width=7.3, height=2.8, rounded=0.5,
          stroke_width=2, stroke="yellow", fill=None)
Sequence(
    rectangle(x=1.5, y=7.9, width=1, height=2.8,
              chevron='E', chevron_height=1,
              stroke="yellow", fill="yellow"),
    setting=(1, 3),
    interval_x=2)


Text(common=header_font, x=5, y=13,
     text="Leaded Window: rectangle with diagonal hatches")
Rectangle(
    x=2, y=12,
    height=3, width=2,
    hatch_count=7, hatch_stroke_width=0.1, hatch='d', hatch_stroke="black",
    stroke="saddlebrown", stroke_width=2, fill="lightcyan")


Text(common=header_font, x=5, y=17,
     text="Paned Window: rectangle with single orthogonal hatch")
Rectangle(
    x=2, y=16,
    height=3, width=2,
    hatch_count=1, hatch_stroke_width=1, hatch='o', hatch_stroke="sienna",
    stroke="sienna", stroke_width=3, fill="lightcyan")


Text(common=header_font, x=5, y=21,
     text="Start Player Token: circles + radii at angles")
Polygon(cx=3, cy=21, height=3, sides=8, fill="black")
Circle(cx=3, cy=21, fill="black", radius=1.25,
       radii=steps(0, 315, 45),
       radii_stroke="gold", radii_stroke_width=2)
Circle(cx=3, cy=21, stroke="black", fill="gold", radius=0.5, stroke_width=5)


Text(common=header_font, x=5, y=26,
     text="Doorway: stadium with dashed line; circle + radii")
Stadium(x=1.503, y=25.003, height=3.003, width=3.003,
        fill="white", edges="n",
        stroke="#CC0033", stroke_width=5, dashed=[0.3,0.05],)
Circle(cx=3, cy=25, radius=1.3,
       stroke="sienna", stroke_width=5, fill="skyblue",
       radii=[150,90,30], radii_stroke="sienna", radii_stroke_width=3)
Circle(cx=3, cy=25, radius=0.3,
       stroke="sienna", stroke_width=5, fill="sienna")
Rectangle(x=1.7, y=25.1, height=2.9, width=2.6,
          stroke="sienna", stroke_width=5, fill="skyblue")

PageBreak()

# ---- PAGE 2 ===>

Text(common=header,
     text="Miscellaneous Things #2")


Text(common=header_font, x=7, y=2.5, text="Sets of check boxes (loop + 3 x sequence)")
for s in steps(0, 6, 2.2):
    Sequence(
        [rectangle(fill_stroke="black", x=s+0.05, y=2.05, height=0.5, width=0.5),
         rectangle(stroke="black", x=s+0, y=2, height=0.5, width=0.5)],
        setting=(1, 3),
        interval_x=0.6)


Text(common=header_font, x=5, y=5,
     text="Wormhole: multiple, rotated, 6-sided polygons")
poly6 = Common(x=2, y=5, fill=None, sides=6, stroke_width=1)
Polygon(common=poly6, radius=1.50)
Polygon(common=poly6, radius=1.35, rotation=15)
Polygon(common=poly6, radius=1.20, rotation=30)
Polygon(common=poly6, radius=1.05, rotation=45)
Polygon(common=poly6, radius=1.05, rotation=60)
Polygon(common=poly6, radius=0.90, rotation=15)
Polygon(common=poly6, radius=0.75, rotation=30)
Polygon(common=poly6, radius=0.60, rotation=45)
Polygon(x=2, y=5, fill="black", radius=0.60, rotation=60)


Text(common=header_font, x=5, y=9,
     text="Mars Base: rectangle borders + circles with offset radii")
Circle(
   cx=1, cy=9, radius=0.8,
   fill="lightcoral", stroke="firebrick", stroke_width=6)
Circle(
   cx=3.5, cy=9, radius=0.8,
   fill="lightcoral", stroke="firebrick", stroke_width=6)
Rectangle(
    x=1.55, y=8.5, height=1, width=1.4, fill="lightcoral", stroke=None,
    borders=("n s", 6, "firebrick"))
Circle(cx=1, cy=9, radius=0.35, fill=None,
       stroke="firebrick", stroke_width=1,
       radii=[33, 90, 150, 210, 270, 327], radii_offset=0.7,
       radii_stroke_width=1, radii_stroke="firebrick")
Circle(cx=3.5, cy=9, radius=0.35, fill=None,
       stroke="firebrick", stroke_width=1,
       radii=[30, 90, 147, 213, 270, 330], radii_offset=0.7,
       radii_stroke_width=1, radii_stroke="firebrick")


Text(common=header_font, x=5, y=12.5,
     text="German Cross: rectangle with 'o' hatch and 'step' notch")
Rectangle(
    height=2.8, width=2.8, x=0.5, y=11,
    fill="white", stroke="black", stroke_width=2,
    hatch_stroke_width=22, hatch_stroke="black",
    hatch='o', hatch_count=1,
    notch=0.7, notch_style='step')
Rectangle(
    height=2.8, width=2.8, x=0.5, y=11,
    fill=None, stroke="white", stroke_width=3)


Text(common=header_font, x=5, y=16,
     text="Atom: ellipses with rotation + centre circle")
atom = Common(cx=2, cy=16, width=3, height=1, stroke_width=1, stroke="red", fill=None)
for degrees in [30,150,270]:
    Ellipse(common=atom, rotation=degrees)
Circle(cx=2, cy=16, radius=0.2, fill_stroke="red")


Text(common=header_font, x=5, y=19,
     text="Gear: nested circles; one with 8 offset radii")
Circle(cx=2, cy=19, radius=0.5,
       fill=None, stroke="dimgray", stroke_width=8,
       radii=[0,45,90,135,180,225,270,315],
       radii_offset=0.6, radii_length=0.2,
       radii_stroke="dimgray", radii_stroke_width=8)
Circle(cx=2, cy=19, radius=0.15, fill_stroke="dimgray")


Text(common=header_font, x=5, y=22,
     text="XOK Fish: two circles with 2 thick, offset, radii")
Circle(cx=2, cy=22, radius=1,
       fill="#63B1BB", stroke="#63B1BB",
       radii=[135,225],
       radii_offset=0.5, radii_length=1,
       radii_stroke="white", radii_stroke_width=15)
Circle(cx=2, cy=22, radius=0.75, fill="#63B1BB", stroke="#63B1BB")
Dot(x=2.5, y=21.5, stroke="white", dot_point=5)


Text(common=header_font, x=5, y=25,
     text="Sonar screen: nested; offset radii; and slices")
Circle(cx=2, cy=25, radius=1.25,
       fill="#105729", stroke="#27B633",
       nested=6,
       slices=["#077D25"], slices_angles=[30],
       slices_transparency=20,
       # hatches='o', hatch_stroke="#035320",
       radii=steps(0, 360, 5),
       radii_offset=1.1, radii_length=0.125,
       radii_stroke="#01F91E", radii_stroke_width=1.25)

PageBreak()

# ---- PAGE 3 ===>

Text(common=header,
     text="Miscellaneous Things #3")

Text(common=header_font, x=8, y=3,
     text="Camera Frame:")
Text(common=header_font, x=8, y=4,
     text="- Image")
Text(common=header_font, x=8, y=4.75,
     text="- Rectangle: corners; centred shape; perbis")
Text(common=header_font, x=8, y=5.5,
     text="- Dot & Texts")
Image("tmwtgg.jpg",
      width=6.4, height=3.6,
      x=1, y=2)
Rectangle(
    width=6, height=3.2, x=1.2, y=2.2,
    fill=None, stroke=None,
    corner=0.4,
    corner_stroke_width=2,
    centre_shape=rectangle(
        width=2, height=2,
        fill=None, stroke=None,
        corner=0.3,
        corner_stroke="silver",
        corner_stroke_width=1.5),
    perbis="*",
    perbis_stroke_width=2,
    perbis_length=0.4,
    perbis_offset=1.8,
    # perbis_offset_y=3,
    cross=0.5,
    cross_stroke="white",
    cross_stroke_width=1.5)
Dot(fill_stroke="red", dot_point=9, x=1.3, y=2.3)
Text(text="REC",
     x=2.25, y=2.55, stroke="red")
Text(text="00:00:00",
     x=6.5, y=5.3, stroke="white", font_size=10)

# rectangle(
#     width=2, height=1.1, fill=None,
#     stroke=None, corner=0.3, corner_stroke_width=2_

Save()
