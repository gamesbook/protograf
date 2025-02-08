"""Purpose: Show various `basic` examples for protograf

Written by: Derek Hohls
Created on: 29 February 2016
Last Update: 5 January 2025

Sources and Credit:
    * pattern from http://elemisfreebies.com/11/07/20-abstract-patterns/
    * SVG from https://thenounproject.com/icon/typewriter-3933515/
"""

from protograf import *

Create(filename="demo.pdf", margin=1, margin_top=0.25)
Footer()

# one BIG hex
Hexagon(
    cx=9.5, cy=14,
    side=10,
    fill_stroke=forestgreen,
    label="WELCOME!\nto a \nprotograf\ndemo",
    label_size=30,
    label_stroke=white,
    label_my=1.7)
# the track of the signs...
sign = circle(cx=0, cy=0, radius=2.7, label='{{sequence}}', fill=None, stroke_width=18,
              radii=[0,90,180,270], radii_stroke_width=18,)
iron = circle(common=sign, stroke=black)
wood = circle(common=sign, stroke=sienna)
bronze = circle(common=sign, stroke=goldenrod)
stone = circle(common=sign, stroke=grey)
fire = circle(common=sign, stroke=gold)
water = circle(common=sign, stroke=snow)
Track(
    polygon(cx=9.5, cy=14, sides=6, radius=6),
    shapes=[water, wood, stone, iron, bronze, fire],
    clockwise=True,
    rotation_style='i',
    start=6)
PageBreak()

# ---- header text
header_font = Common(font_size=18, align="left")
header = Common(x=0, y=27, font_size=24, align="left")

# ---- default labels and blueprint
Blueprint()
Text(common=header, text="Blueprint plus shapes with labels")
Polygon(x=4, y=24.5, radius=2, angle=30, label="polygon6")
Polygon(x=10, y=24.5, radius=2, sides=8, angle=22.5, label="polygon8")
Polygon(x=16, y=24.5, radius=2.5, sides=2.5, angle=30, label="polygon3")
Rectangle(x=2, y=18.5, width=5, height=3, label="rectangle")
Trapezoid(x=14, y=13, width=4.1, top=3, height=3, label="trapezoid")
Stadium(x=14.5, y=19, width=3, height=2, label="stadium")
Hexagon(x=2, y=13, side=2, label="hexagon")
Hexagon(x=8, y=13, side=2, orientation="pointy", label="hexagon")
Star(x=11, y=9, vertices=5, radius=2, label="star")
Circle(cx=16, cy=9, radius=2, label="circle")
Ellipse(x=2, y=7, width=5, height=3, label="ellipse")
Rhombus(x=8.5, y=1, width=3, height=5, label="rhombus")
Compass(cx=4, cy=3, radius=2, title="compass")
Square(x=14, y=1, side=4, label="square")
PageBreak()

# ---- centre shapes and blueprint + label
Blueprint()
Text(common=header, text="Centred shapes with centre point and x-y label")
dot = Common(dot=0.2, dot_stroke=yellow)

Rectangle(cx=3, cy=23, width=5, height=3, label="rectangle:3-23", common=dot)
EquilateralTriangle(x=7, y=21, side=4, label="triangle:9-22", common=dot)
Stadium(cx=15, cy=23, width=3, height=2, label="stadium:15-23", common=dot)

Hexagon(cx=3, cy=17, side=2, label="hexagon:3-17", orientation="flat", common=dot)
Ellipse(cx=9, cy=17, width=5, height=3, label="ellipse:9-17", common=dot)
Trapezoid(cx=16, cy=17, width=4, top=2, height=3, label="trapezoid:16-17", common=dot)

Hexagon(cx=3, cy=11, side=2, label="hexagon:3-11", orientation="pointy", common=dot)
Compass(cx=9, cy=11, radius=2, label="compass:9-11", common=dot)
Circle(cx=16, cy=11, radius=2, label="circle:16-11", common=dot)

Star(cx=3, cy=5, vertices=5, radius=2, label="star:3-5", common=dot)
Rhombus(cx=16, cy=5, width=3, height=5, label="rhombus:16-5", common=dot)
Square(cx=9, cy=5, side=3, label="square:9-5", common=dot)

Dot(x=9.5, y=1, dot_point=6, label="dot:1-9.5")

PageBreak()

# ---- centre shapes and blueprint + heading
Blueprint()
Text(common=header, text="Centred shapes with centre point and x-y heading")
dot = Common(dot=0.2, dot_stroke=blue)

Rectangle(cx=3, cy=23, width=5, height=3, heading="rectangle:3-23", common=dot)
EquilateralTriangle(x=7, y=21, side=4, heading="triangle:9-22", common=dot)
Stadium(cx=15, cy=23, width=3, height=2, heading="stadium:15-23", common=dot)

Hexagon(cx=3, cy=17, side=2, heading="hexagon:3-17", orientation="flat", common=dot)
Ellipse(cx=9, cy=17, width=5, height=3, heading="ellipse:9-17", common=dot)
Trapezoid(cx=16, cy=17, width=4, top=2, height=3, heading="trapezoid:16-17", common=dot)

Hexagon(cx=3, cy=11, side=2, heading="hexagon:3-11", orientation="pointy", common=dot)
Compass(cx=9, cy=11, radius=2, heading="compass:9-11", common=dot)
Circle(cx=16, cy=11, radius=2, heading="circle:16-11", common=dot)

Star(cx=3, cy=5, vertices=5, radius=2, heading="star:3-5", common=dot)
Rhombus(cx=16, cy=5, width=3, height=5, heading="rhombus:16-5", common=dot)
Square(cx=9, cy=5, side=3, heading="square:9-5", common=dot)

Dot(x=9.5, y=1, dot_point=6, heading="dot:1-9.5")

PageBreak()

# ---- centre shapes and blueprint + title
Blueprint()
Text(common=header, text="Centred shapes with centre point and x-y title")
dot = Common(dot=0.2, dot_stroke=green)

Rectangle(cx=3, cy=23, width=5, height=3, title="rectangle:3-23", common=dot)
EquilateralTriangle(x=7, y=21, side=4, title="triangle:9-22", common=dot)
Stadium(cx=15, cy=23, width=3, height=2, title="stadium:15-23", common=dot)

Hexagon(cx=3, cy=17, side=2, title="hexagon:3-17", orientation="flat", common=dot)
Ellipse(cx=9, cy=17, width=5, height=3, title="ellipse:9-17", common=dot)
Trapezoid(cx=16, cy=17, width=4, top=2, height=3, title="trapezoid:16-17", common=dot)

Hexagon(cx=3, cy=11, side=2, title="hexagon:3-11", orientation="pointy", common=dot)
Compass(cx=9, cy=11, radius=2, title="compass:9-11", common=dot)
Circle(cx=16, cy=11, radius=2, title="circle:16-11", common=dot)

Star(cx=3, cy=5, vertices=5, radius=2, title="star:3-5", common=dot)
Rhombus(cx=16, cy=5, width=3, height=5, title="rhombus:16-5", common=dot)
Square(cx=9, cy=5, side=3, title="square:9-5", common=dot)

Dot(x=9.5, y=1, dot_point=6, title="dot:1-9.5")

PageBreak()

# ---- rotation all shapes + label
Blueprint()
Text(common=header, text="Rotated shapes with labels")
Polygon(x=4, y=24.5, radius=2, rotation=45, stroke_width=2, label="polygon6")
Polygon(x=10, y=24.5, radius=2, sides=8, angle=22.5, rotation=45, stroke_width=2, label="polygon8")
Polygon(x=16, y=24.5, radius=2.5, sides=3, rotation=45, stroke_width=2, label="polygon3")
Rectangle(x=2, y=18.5, width=6, height=3, rotation=45, stroke_width=2, label="rectangle")
Trapezoid(x=14, y=13, width=4, top=2, height=3, rotation=45, stroke_width=2, label="Trapezoid")
Stadium(x=14.5, y=19, width=3, height=2, rotation=45, stroke_width=2, label="stadium")
Hexagon(x=2, y=13, side=2, rotation=45, stroke_width=2, label="hexagon")
Hexagon(x=8, y=13, side=2, orientation="pointy", rotation=45, stroke_width=2, label="hexagon")
Star(x=10, y=9, vertices=5, radius=2, rotation=45, stroke_width=2, label="star")
Circle(cx=16, cy=9, radius=2, rotation=45, stroke_width=2, label="circle")
Ellipse(cx=4, cy=9, width=5, height=3, rotation=45, stroke_width=2, label="ellipse")
Rhombus(x=8.5, y=1, width=3, height=5, rotation=45, stroke_width=2, label="rhombus")
Square(x=14, y=1, side=4, rotation=45, stroke_width=2, label="square")
PageBreak()

# ---- filled shapes
Blueprint()
Text(common=header, text="Filled shapes")
Rectangle(cx=3, cy=23, width=5, height=3,
          title="rectangle:3-23", title_stroke=black, fill_stroke=tomato)
EquilateralTriangle(
    x=7, y=21, side=4,
    title="triangle:9-22", title_stroke=black, fill_stroke=tomato)
Stadium(x=13.5, y=22, width=3, height=2,
        title="stadium:15-23", title_stroke=black, fill_stroke=tomato)
Hexagon(cx=3, cy=17, side=2, orientation="flat",
        title="hexagon:3-17", title_stroke=black, fill_stroke=gold)
Ellipse(cx=9, cy=17, width=5, height=3,
        title="ellipse:9-17", title_stroke=black, fill_stroke=gold)
Trapezoid(cx=16, cy=17, width=4, top=2, height=3,
          title="trapezoid:16-17", title_stroke=black, fill_stroke=gold)
Hexagon(cx=3, cy=11, side=2, orientation="pointy",
        title="hexagon:3-11", title_stroke=black, fill_stroke=lime)
Compass(cx=9, cy=11, radius=2,
        title="compass:9-11", title_stroke=black, fill_stroke=lime)
Circle(cx=16, cy=11, radius=2,
       title="circle:16-11", title_stroke=black, fill_stroke=lime)
Star(cx=3, cy=5, vertices=5, radius=2,
     title="star:3-5", title_stroke=black, fill_stroke=aqua)
Rhombus(cx=16, cy=5, width=3, height=5,
        title="rhombus:16-5", title_stroke=black, fill_stroke=aqua)
Square(cx=9, cy=5, side=3,
       title="square:9-5", title_stroke=black, fill_stroke=aqua)
Dot(x=9.5, y=1, dot_point=6, title="dot:1-9.5")
PageBreak()

# ---- lines and polyshapes & polylines
Text(common=header, text="Polyshapes, Polylines and lines")
Polyline(
    points=[(0, 13), (2, 15), (4, 13), (6, 15), (8, 13), (10, 15), (12, 13)],
    stroke=grey)
Polyline(points="0,11 2,13 4,11 6,13 8,11 10,13 12,11", stroke=grey)
Line(x=1, y=1, length=30, angle=55.3, stroke=tomato, stroke_width=3)  # thick diagonal
Line(x=0, y=3, x1=19, y1=3, stroke=black, stroke_width=2)
Line(
    x=0,
    y=9,
    x1=19,
    y1=9,
    dashed=[0.2, 0.2, 0.2, 0.2, 1.0, 0.0],
    stroke=lime,
    stroke_width=2,
    label="dashed=[0.2, 0.2, 0.2, 0.2, 1, 0]",
)
Line(x=0, y=5, x1=19, y1=5, dotted=True, stroke=blue, stroke_width=2, label="dotted")
# house
points = [
    (2, 17),
    (2, 20),
    (5, 21),
    (8, 20),
    (8, 17),
    (6, 17),
    (6, 18.5),
    (4, 18.5),
    (4, 17),
    (1, 17),
]
Polyshape(cx=5, cy=19.5, points=points, stroke=bisque, fill=tomato,
          label="Store", label_size=24)
Polyshape(x=25, y=4, points="0,0 0,1 2,0 2,1 0,0", fill_stroke=gold)
PageBreak()

# ---- bezier / arc
Blueprint()
Text(common=header, text="Bezier line and arc")
Bezier(x=2, y=7, x1=12, y1=9, x2=12, y2=16, x3=17, y3=20, stroke=blue, stroke_width=2)
Arc(x=1, y=7, x1=4, y1=4, stroke=tomato, stroke_width=4)
PageBreak()

# ---- common, with angled lines
Blueprint()
Text(common=header, text="Lines drawn manually using angles (default origin)")
cmm = Common(x=0, y=0, length=19, dots=True, stroke=darkmagenta, stroke_width=2)
Line(common=cmm, label="No angle (flat)")
Line(common=cmm, angle=15, label="15 degrees")
Line(common=cmm, angle=30, label="30 degrees")
Line(common=cmm, angle=45, label="45 degrees")
Line(common=cmm, angle=60, label="60 degrees")
Line(common=cmm, angle=75, label="75 degrees")
Line(common=cmm, angle=90, label="90 degrees")
PageBreak()

# ---- common, with angled lines via loop
Blueprint()
Text(common=header, text="Lines drawn via angles (via loop; 5 degrees steps)")
for angle in range(0, 91, 5):
    Line(common=cmm, angle=angle)
PageBreak()

# ---- school book page with margin
Text(common=header, text="Lines -> school book page")
Lines(x=0, x1=19, y=0, y1=0, rows=28, height=1.0, stroke=lightsteelblue)
Line(x=2, x1=2, y=0, y1=27, stroke=orangered)
PageBreak()

# ---- school book page - landscape
Text(common=header, text="Lines -> school book page; landscape")
Lines(x=0, x1=0, y=0, y1=28.5, cols=20, width=1.0, stroke=lightsteelblue)
Line(x=0, x1=19, y=2, y1=2, stroke=orangered)
PageBreak()

# ---- set of stickers
Text(common=header, text="Rectangles (6x13)")
Rectangles(
    rows=13,
    cols=6,
    width=3,
    height=2,
    rounding=0.4,
    margin=1,
    fill=gold,
    stroke=lime,
)
PageBreak()

# ---- grid: graph paper
Text(common=header, text='"Graph Paper" -> Grid (95x135) and Grid (19x27)')
Grid(cols=95, rows=135, size=0.2, stroke=mediumseagreen, stroke_width=0.9)
Grid(cols=19, rows=27, size=1.0, stroke=mediumseagreen, stroke_width=1.5)
PageBreak()

# ---- hexagons ~2cm grid - numbered "wargame" style
Hexagons(
    rows=11,
    cols=9,
    side=1.69,
    margin_left=-1.69,
    margin_bottom=-2.529,
    dot=0.05,
    dot_stroke=black,
    coord_elevation="top",
    coord_font_size=9,
    coord_stroke=darkslategrey,
    fill=white,
    stroke=darkslategrey,
    caltrops="medium",
)
Text(common=header, text="Hexagons (dot; coords; caltrops)")
PageBreak()

# ---- images and various text descriptors
Text(common=header, text="Rectangles and images (with transparency)")
Rectangle(x=5.9, y=15.9, width=7.2, height=6.2, stroke=silver, fill=gold)
Image(
    "sholes_typewriter.png",  # has transparent background
    x=6,
    y=16,
    width=7,
    height=6,
    font_size=18,
    label="sholes typewriter",
    label_stroke=tomato,
    heading="Sholes Typewriter (PNG)",
    heading_stroke=turquoise,
    title="Fig 2. The Sholes Typewriter",
    title_stroke=lime,
)

Rectangle(x=6, y=6, width=7, height=6.25, stroke=silver, fill=gold)
Image(
    # "Typewriter_Vector.svg",
    "noun-typewriter-3933515.svg",
    x=6,
    y=6,
    width=7,
    height=6,
    font_size=18,
    label="noun typewriter",
    label_stroke=tomato,
    heading="Noun Project Typewriter (SVG)",
    heading_stroke=turquoise,
    title="Fig 3. A nounproject.com Typewriter (AlekZakaUddin, CC BY 3.0)",
    title_stroke=lime,
    scaling=0.6,
)
PageBreak()

# ---- text alignment (default is centre);
Text(common=header, text="Text: face, styling, wrap and align")

Rectangle(x=0.75, y=23.5, width=7.5, height=3, stroke_width=1, stroke=grey) #, heading="Aligments")
Text(text="sholes\ntypewriter!", x=4.5, y=26)  #  add line break via \n
Text(text="sholes * typewriter!", x=4.5, y=25, align="centre")
Text(text="sholes typewriter! *", x=4.5, y=24.5, align="right")
Text(text="* sholes typewriter!", x=4.5, y=24, align="left")

# ---- auto-text wrapping & justification
LATIN = """At cum perfecto praesent, ne causae voluptua <i>reprimique</i> usu,
his id odio tamquam <strike>senserit</strike>.<br/>
<br/>
Eu facete audire assentor usu. Legendos reformidans et vel. Ignota <u>seprehendunt</u>
nam an, vix ad veri maiorum vivendo. Per at ullum iracundia intellegam, alii
nonumy deterruisset ne sed, cum cu quet reque <b>signiferumque</b>.<br/>
<br/>
<font face="times" color="red" size="15">Qui at primis regione consetetur.</font>
Id vis viris antiopam gloriatur, muscipit ex has, an ius mazim.
"""
# path for img assumes this file is called from the project root ...
IMAGE = LATIN + '<img src="examples/core/13.png" height="10" valign="bottom"/>' +\
    ' per at ullum iracundia intellegam.'

header = Common(x=1, font_size=18, align="left", width=2.5, height=2, wrap=True)

Rectangle(x=4.5, y=1, width=10, height=5.5, stroke_width=1, stroke=grey)
Text(
    x=4.5, y=6.5, width=10, height=5, wrap=True, align="left", text=IMAGE, stroke=aqua
)
Text(common=header, y=4, text="Align: Left")

Rectangle(x=4.5, y=7, width=10, height=5, stroke_width=1, stroke=grey)
Text(x=4.5, y=12, width=10, height=5, wrap=True, align="right", text=LATIN)
Text(common=header, y=10, text="Align: Right")

Rectangle(x=4.5, y=12.5, width=10, height=5, stroke_width=1, stroke=grey)
Text(x=4.5, y=17.5, width=10, height=5, wrap=True, align="centre", text=LATIN)
Text(common=header, y=16, text="Align: Centre")

Rectangle(x=4.5, y=18, width=10, height=5, stroke_width=1, stroke=grey)
Text(x=4.5, y=23, width=10, height=5, wrap=True, align="justify", text=LATIN)
Text(common=header, y=21, text="Align: Justify")

PageBreak()

# ---- cards
# Deck(cards=9)
# Card("1-3", circle(cx=3, cy=4.2))
# Card("4", image("sholes_typewriter.png", x=3, y=5, width=3, height=3))
# Card("5", image("sholes_typewriter.png", x=3, y=5, width=3, height=3, rotation=30))
# Card("6", image("sholes_typewriter.png", x=3, y=5, width=3, height=3, rotation=60))
# Card("7", image("noun-typewriter-3933515.svg", x=3, y=5, width=3, height=3, scaling=0.3))
# Card("8", image("noun-typewriter-3933515.svg", x=3, y=5, width=3, height=3, scaling=0.3, rotation=30))
# Card("9", image("noun-typewriter-3933515.svg", x=3, y=5, width=3, height=3, scaling=0.3, rotation=60))
# PageBreak()

# one BIG hex
Hexagon(
    cx=9.5, cy=14,
    side=10,
    label="THIS IS THE END...\nof a basic\nprotograf demo!",
    label_size=30,
    label_my=1.3)

PageBreak()
# Save(output='png', dpi=300)
Save()
