"""
Show customised shapes - and useful overides - for protograf

Written by: Derek Hohls
Created on: 29 March 2024

Sources and Credit:
    * SVG from https://thenounproject.com/icon/typewriter-3933515/
"""

from protograf import *

Create(filename="customised_shapes.pdf",
       paper="A8",
       margin_left=0.5,
       margin_right=0.3,
       margin_bottom=0.2,
       margin_top=0.5,
       font_size=8,
       stroke_width=0.5,
       )

Footer(draw=False)

txt = Common(x=0, y=0, font_size=8, align="left")

Text(common=txt, text="Shapes START...")
Text(x=0, y=6, font_size=8, align="left", text=Today())
PageBreak()

# ---- blueprint custom
Blueprint(subdivisions=5, stroke_width=0.5, style='invert')
Text(common=txt, text="Blueprint: style & subdivisions")
PageBreak()

# ---- dot & cross
Blueprint()
Text(common=txt, text="Dots & Crosses")
Rhombus(cx=1, cy=5, side=2, dot=0.1, dot_stroke="red")
Rhombus(cx=3, cy=5, side=2, cross=0.25, cross_stroke="red", cross_stroke_width=1)
Polygon(cx=1, cy=3, sides=8, radius=1, dot=0.1, dot_stroke="orange")
Polygon(cx=3, cy=3, sides=8, diameter=2, cross=0.25, cross_stroke="orange", cross_stroke_width=1)
Stadium(cx=1, cy=1, side=1, stroke="blue", dot=0.1)
Stadium(cx=3, cy=1, side=1, stroke="blue", cross=0.25, cross_stroke_width=1)
PageBreak()

# ---- centre placement
Blueprint()
Text(common=txt, text="Centred")
shp_font = Common(font_size=6, stroke="red")
Trapezoid(common=shp_font, cx=1, cy=5, heading="Trapezoid cx=1;cy=5")
Rhombus(common=shp_font, cx=3, cy=5, heading="Rhombus cx=3;cy=5")
Star(common=shp_font, cx=1, cy=3, heading="Star cx=1;cy=3")
Ellipse(common=shp_font, cx=3, cy=3, width=2, height=1, heading="Ellipse cx=3;cy=3")
Polygon(common=shp_font, cx=2, cy=1, radius=0.8, sides=7, heading="Polygon-7 cx2=;cy=1")
PageBreak()

# ---- RA triangles
Blueprint()
Text(common=txt, text="Right Angled Triangle")
RightAngledTriangle(x=1, y=1, flip="north", hand="east", label="NE", fill="yellow")
RightAngledTriangle(x=2, y=2, flip="south", hand="east", label="SE", fill="green")
RightAngledTriangle(x=2, y=3, flip="north", hand="west", label="NW", fill="red")
RightAngledTriangle(x=3, y=4, flip="south", hand="west", label="SW", fill="blue")
PageBreak()

# ---- compass
Blueprint()
Text(common=txt, text="Compass")
Compass(cx=3, cy=1, perimeter='hexagon', radius=0.5, radii_stroke_width=2)
Compass(cx=1, cy=5, perimeter='circle', radius=0.5, directions="ne nw s")
Compass(cx=2, cy=3, perimeter='rectangle', directions="*", height=2, width=3, radii_stroke="red")
PageBreak()

# ---- lines (multiple) labels
Blueprint()
Text(common=txt, text="Lines")
Lines(x=1, x1=4, y=1, y1=1, rows=2, height=1.0, label_size=8, label="rows; ht=1.0")
Lines(x=1, x1=1, y=3, y1=6, cols=2, width=1.5, label_size=8, label="col; wd=1.5")
PageBreak()

# ---- starfield
Blueprint()
Text(common=txt, text="StarField: rectangle; multi-color")
Rectangle(x=0, y=0, height=3, width=3, fill="black")
StarField(
    enclosure=rectangle(x=0, y=0, height=3, width=3),
    density=80,
    colors=["white", "white", "red", "green", "blue", ],
    sizes=[0.4],
    seeding=42.3)
PageBreak()

Blueprint()
Text(common=txt, text="StarField: circle; multi-size")
Circle(x=0, y=0, radius=1.5, fill="black")
StarField(
    enclosure=circle(x=0, y=0, radius=1.5),
    density=30,
    sizes=[0.15, 0.15, 0.15, 0.15, 0.3, 0.3, 0.5],
    seeding=42.3)
PageBreak()

Blueprint()
Text(common=txt, text="StarField: poly; multi-color&size")
plys = Common(x=1.5, y=1.4, sides=10, radius=1.5)
Polygon(common=plys, fill="black")
StarField(
    enclosure=polygon(x=1.5, y=1.4, sides=10, radius=1.5),
    density=50,
    colors=["white", "white", "white", "red", "green", "blue", ],
    sizes=[0.15, 0.15, 0.15, 0.15, 0.3, 0.3, 0.45],
    seeding=42.3)
PageBreak()

# ---- equilateral triangle: hatch
Blueprint()
Text(common=txt, text="Equilateral Triangle; flip; hatch")
EquilateralTriangle(
    x=2, y=1, flip="north", hand="east", label="NE", fill="gold")
EquilateralTriangle(
    x=2, y=1, flip="south", hand="east", label="SE", fill="chartreuse")
EquilateralTriangle(
    x=2, y=1, flip="north", hand="west", label="NW", fill="red")
EquilateralTriangle(
    x=2, y=1, flip="south", hand="west", label="SW", fill="blue")
EquilateralTriangle(
    x=1, y=4, side=1.5,
    hatch_count=5, hatch_stroke="red",
    title='Title', heading='Head')
EquilateralTriangle(
    x=1, y=5.5, side=1.5, stroke_width=1,
    rotation=45, dot=.05)
PageBreak()

# ---- RA Triangle
Blueprint()
Text(common=txt, text="Right Angled Triangle: flip/hand")
eqt = Common(x=2, y=2, side=2)
RightAngledTriangle(common=eqt, flip="north", hand="east", label="NE", fill="yellow")
RightAngledTriangle(common=eqt, flip="south", hand="east", label="SE", fill="green")
RightAngledTriangle(common=eqt, flip="north", hand="west", label="NW", fill="red")
RightAngledTriangle(common=eqt, flip="south", hand="west", label="SW", fill="blue")
PageBreak()

# ---- sectors
Blueprint()
Text(common=txt, text="Sectors: 3 with same centre")
sctm = Common(cx=2, cy=3, radius=2, fill="black", angle_width=43,)
Sector(common=sctm, angle_start=40)
Sector(common=sctm, angle_start=160)
Sector(common=sctm, angle_start=280)
PageBreak()

# ---- grid
Text(common=txt, text='Grid: gray; 1/3"; thick')
Grid(side=0.85, stroke="gray", stroke_width=1)
PageBreak()

# ---- dotgrid - Moleskin
Text(common=txt, text='DotGrid: "Moleskine" setting')
DotGrid(stroke="darkgray", width=0.5, height=0.5, dot_point=1, offset_y=0.25)
PageBreak()

# ---- dotgrid - rows & cols
Blueprint()
Text(common=txt, text="DotGrid: rows&cols")
DotGrid(stroke="darkgray",
        width=0.5, height=0.5,
        rows=14, cols=10,
        dot_point=1)
PageBreak()

# ---- arc
Blueprint()
Text(common=txt, text="Arc; 'inside' square")
Rectangle(x=1, y=1, height=2, width=2, dot=0.02,
          stroke="red", fill=None,
          title="Arc(cx=1, cy=3, radius=2)")
Arc(cx=1, cy=3, radius=2)  #, angle_start=0, angle_width=90)
PageBreak()

# ---- stadium edges
Blueprint()
Text(common=txt, text="Stadium: edges")
Stadium(x=0, y=1, height=1, width=1, edges='n', fill="tan", label="north")
Stadium(x=3, y=1, height=1, width=1, edges='s', fill="tan", label="south")
Stadium(x=0, y=3, height=1, width=1, edges='e', fill="tan", label="east")
Stadium(x=3, y=4, height=1, width=1, edges='w', fill="tan", label="west")
PageBreak()

# ---- trapezoid flip
Blueprint()
Text(common=txt, text="Trapezoid: flip")
Trapezoid(
    x=1, y=2,
    width=3, top=2,
    flip="south",
    label="flip",
    hand="east", fill="yellow")
PageBreak()

# ---- chord
Blueprint()
Text(common=txt, text="Chord: 135 to 45 degrees")
Chord(shape=Circle(radius=1, fill=None), angle=135, angle1=45, label="chord")
PageBreak()

# ---- polygon radii
Blueprint()
Text(common=txt, text="Polygon: radii (default & custom)")
Polygon(cx=2, cy=4, sides=8, radius=1, radii=True)
Polygon(
    cx=2, cy=1, sides=10, radius=1, radii=True,
    radii_offset=0.75, radii_length=0.25, radii_stroke_width=1,
    dot=0.1, dot_stroke="red")
PageBreak()

# ---- polygon perbis
Blueprint()
Text(common=txt, text="Polygon: perbis (default & custom)")
Polygon(cx=2, cy=4, sides=8, radius=1, perbis='*')
Polygon(
    cx=2, cy=1, sides=8, radius=1,
    perbis="2,4,7",
    perbis_offset=0.25, perbis_length=0.5, perbis_stroke_width=1,
    dot=0.1, dot_stroke="red")
PageBreak()

# ---- dates
Blueprint()
Text(common=txt, text="Dates: format and styles")
dtext = Common(x=0.25, align="left", font_size=8)
Text(common=dtext, y=1, text="1.  "+Today())
Text(common=dtext, y=2, text="2.  "+Today(details="date", style="usa"))
Text(common=dtext, y=3, text="3.  "+Today(details="date", style="eur"))
Text(common=dtext, y=4, text="4.  "+Today(details="datetime", style="usa"))
Text(common=dtext, y=5, text="5.  "+Today(details="datetime", style="eur"))
PageBreak()

# ---- rotation: image
Blueprint()
Text(common=txt, text="Images: normal & rotation")
Image("sholes_typewriter.png",
      width=1.5, height=1.5,
      x=0, y=0, title="PNG")
Image("sholes_typewriter.png",
      width=1.5, height=1.5,
      x=2, y=0, title="60\u00B0", rotation=60)
Image("noun-typewriter-3933515.svg",
      width=1.5, height=1.5,
      x=0, y=3, title="SVG")
Image("noun-typewriter-3933515.svg",
      width=1.5, height=1.5,
      x=2, y=3, title="45\u00B0", rotation=45)
PageBreak()

# ---- rotation: rhombus
Blueprint()
Text(common=txt, text="Rhombus: red => rotation 60\u00B0")
Rhombus(cx=2, cy=3, width=1.5, height=2*equilateral_height(1.5), dot=0.06,
        fill=None, stroke="black")
Rhombus(cx=2, cy=3, width=1.5, height=2*equilateral_height(1.5), dot=0.03,
        fill=None, stroke="red", rotation=60)
PageBreak()

# ---- rotation: stadium
Blueprint()
Text(common=txt, text="Stadium: red => rotation 60\u00B0")
Stadium(cx=2, cy=3, width=1.25, height=2, dot=0.06)
Stadium(cx=2, cy=3, width=1.25, height=2,
        stroke="red", stroke_width=.3, rotation=60, dot=0.04)
PageBreak()

# ---- slices: rhombus
Blueprint()
Text(common=txt, text="Rhombus: slices")
Rhombus(cx=2, cy=3, height=3, width=2,
        slices=["red", "blue", "gold", "aqua"],
)
Rhombus(cx=1, cy=1, height=2, width=1,
        slices=["red", "blue"],
)
Rhombus(cx=3, cy=5, height=2, width=1,
        slices=["gold", "aqua", True],
)
Rhombus(cx=3, cy=1, height=2, width=1,
        slices=[None, "blue", None, "aqua"],
)
Rhombus(cx=1, cy=5, height=2, width=1,
        slices=["red", None, "gold", None],
)
PageBreak()

# ---- rotation: polygon
Blueprint()
Text(common=txt, text="Polygon: rotation (flat)")
poly6 = Common(fill=None, sides=6, diameter=1, stroke_width=1, orientation='flat')
Polygon(common=poly6, y=1, x=1.0, label="0")
Polygon(common=poly6, y=2, x=1.5, rotation=15, label="15")
Polygon(common=poly6, y=3, x=2.0, rotation=30, label="30")
Polygon(common=poly6, y=4, x=2.5, rotation=45, label="45")
Polygon(common=poly6, y=5, x=3.0, rotation=60, label="60")
PageBreak()

Blueprint()
Text(common=txt, text="Polygon: rotation (pointy)")
poly6 = Common(fill=None, sides=6, diameter=1, stroke_width=1, orientation='pointy')
Polygon(common=poly6, y=1, x=1.0, label="0")
Polygon(common=poly6, y=2, x=1.5, rotation=15, label="15")
Polygon(common=poly6, y=3, x=2.0, rotation=30, label="30")
Polygon(common=poly6, y=4, x=2.5, rotation=45, label="45")
Polygon(common=poly6, y=5, x=3.0, rotation=60, label="60")
PageBreak()

# ---- polygon sizes
Blueprint()
Text(common=txt, text="Polygon: sizes")
Polygon(cx=1, cy=5, sides=7, radius=1, label="Seven")
Polygon(cx=2, cy=3, sides=6, radius=1, label="Six")
Polygon(cx=3, cy=1, sides=5, radius=1, label="Five")
PageBreak()

# ---- grid cols and rows
Blueprint()
Text(common=txt, text='Grid: gray; 3x4; thick')
Grid(x=0.5, y=0.5, cols=3, rows=4, height=1.25, width=1, stroke="gray", stroke_width=1)
PageBreak()

# ---- line - custom
Blueprint()
Text(common=txt, text='Line: locations; styles')
Line(x=0, y=0.5, stroke_width=0.2, dotted=True, label="0.2", font_size=6)
Line(x=1, y=0.5, stroke_width=0.4, dotted=True, label="0.4", font_size=6)
Line(x=2, y=0.5, stroke_width=0.8, dotted=True, label="0.8", font_size=6)
Line(x=3, y=0.5, stroke_width=1.6, dotted=True, label="1.6", font_size=6)
Line(x=0, y=2, length=4, stroke="gold", stroke_width=2)
Line(x=1, y=1.5, length=2, stroke="chartreuse", stroke_width=10, rounded=True)
Line(x=0, y=3, length=4.1, angle=15, stroke="red", label="15", font_size=6)
Line(x=0, y=4, x1=4, y1=5, stroke="blue", stroke_width=1,
     dashed=[0.2, 0.1], label="dashed:[0.2,0.1]", font_size=6)
PageBreak()

# ---- center line from angle
Blueprint(stroke_width=0.5)
Text(common=txt, text="Line: angle")

Line(cx=1, cy=1, angle=45, length=2, stroke="red")
Line(cx=3, cy=1, angle=225, length=2, stroke_width=1.5)

Circle(cx=2, cy=3, radius=1)
Line(cx=2, cy=3, angle=45, length=2, stroke="red", arrow_width=0.2)
Line(cx=2, cy=3, angle=135, length=2, stroke_width=1.5, arrow_width=0.2)

Line(cx=1, cy=5, angle=135, length=2, stroke_width=1.5)
Line(cx=3, cy=5, angle=315, length=2, stroke="red")
PageBreak()

# ---- bezier - custom
Blueprint()
Text(common=txt, text="Bezier line")
Bezier(x=0, y=1, x1=4, y1=3, x2=3, y2=4, x3=4, y3=6, stroke_width=1)
PageBreak()

# ---- ellipse - custom
Blueprint()
Text(common=txt, text="Ellipse: centre; tall")
Ellipse(cx=2, cy=3, width=3, height=4, dot=0.1)
PageBreak()

# ---- rectangle - custom
Blueprint()
Text(common=txt, text="Rectangle: centre; tall")
Rectangle(cx=2, cy=3, width=3, height=4, dot=0.1)
PageBreak()

# ---- square - custom
Blueprint()
Text(common=txt, text="Square: centre; dot")
Square(cx=2, cy=3, side=3, dot=0.1)
PageBreak()

# ---- trapezoid - custom
Blueprint()
Text(common=txt, text="Trapezoid: centre; dot")
Trapezoid(cx=2, cy=3, width=3, top=2, height=4, flip='s', dot=0.1)
PageBreak()

# ---- image - base
Blueprint()
Text(common=txt, text="Image: default")
Image("sholes_typewriter.png")
PageBreak()

# ---- text for shapes
Blueprint(stroke_width=0.5)
Text(common=txt, text="Shape text: default and custom")
Hexagon(
    cx=2, cy=1.5, height=1.5,
    title="Title", label="Label", heading="Heading")
Rectangle(
    x=0.5, y=3, width=3, height=2,
    label="red; size=14", label_stroke="red", label_size=14)
PageBreak()

# ---- label offsets
Blueprint(stroke_width=0.5)
Text(common=txt, text="Shape label: offsets")
rct = Common(height=1.0, width=1.75, stroke_width=.5, label_size=7)
Rectangle(common=rct, x=0, y=0.0, label="offset -x, -y", label_mx=-0.2, label_my=-0.2)
Rectangle(common=rct, x=0, y=1.5, label="offset -x", label_mx=-0.3)
Rectangle(common=rct, x=0, y=3.0, label="offset -x, +y", label_mx=-0.2, label_my=0.2)
Rectangle(common=rct, x=0, y=4.5, label="offset +y", label_my=0.2)
Rectangle(common=rct, x=2, y=0.0, label="offset +x, -y", label_mx=0.2, label_my=-0.2)
Rectangle(common=rct, x=2, y=1.5, label="offset +x", label_mx=0.3)
Rectangle(common=rct, x=2, y=3.0, label="offset +x, +y", label_mx=0.2, label_my=0.2)
Rectangle(common=rct, x=2, y=4.5, label="offset -y", label_my=-0.2)
PageBreak()

# ---- star shape
Blueprint(stroke_width=0.5)
Text(common=txt, text="Star: rotation (36\u00B0)")
Star(cx=2, cy=3, radius=2, fill_stroke="yellow", rotation=36)
PageBreak()

# ---- polyshape
Blueprint(stroke_width=0.5)
Text(common=txt, text="Polyshape: default")
Polyshape(points=[(1, 2), (1, 1), (2, 0), (3, 1), (3, 2)])
Polyshape(x=1, y=3,
         steps='0.5,0 0,1.5 1.5,0 0,-1.5 0.5,0 0,0.5 -2.5,0 0,-0.5')
PageBreak()

# ---- polyshape - custom
Blueprint(stroke_width=0.5)
Text(common=txt, text="Polyshape: custom")
Polyshape(
      points=[(1, 2), (1, 1), (2, 0), (3, 1), (3, 2)],
      cx=2, cy=1,
      label='A House',
      label_stroke="seagreen",
      cross=0.5,
      fill="sandybrown",
      stroke="peru",
)
Polyshape(x=1, y=3,
         steps='0.5,0 0,1.5 1.5,0 0,-1.5 0.5,0 0,0.5 -2.5,0 0,-0.5',
         stroke="sandybrown", stroke_width=3, fill="seagreen")
PageBreak()

# ---- shapeshape - offset + string
Blueprint(stroke_width=0.5)
Text(common=txt, text="Polyshape: offset")
Polyshape(
    points="0,0 0,1 2,0 2,1 0,0",
    cx=1, cy=0.5,
    fill="chartreuse", label="Left ....... Right")
Polyshape(
    points="0,0 0,1 2,0 2,1 0,0",
    cx=1, cy=0.5,
    fill="gold", label="Left ....... Right",
    x=1, y=2)
PageBreak()

# ---- rectangles - basic
Blueprint(stroke_width=0.5)
Text(common=txt, text="Rectangles: rows & cols")
Rectangles(rows=3, cols=2, stroke_width=1)
PageBreak()

# ---- rectangles - custom
Blueprint(stroke_width=0.5)
Text(common=txt, text="Rectangles: custom")
Rectangles(rows=4, cols=2, width=1.5, height=1.25, dotted=True, fill="chartreuse")
PageBreak()

# ---- rhombus - custom
Blueprint()
Text(common=txt, text="Rhombus: centre; dot")
Rhombus(cx=2, cy=3, width=2, height=3, dot=0.1)
PageBreak()

# ---- rhombus - borders
Blueprint()
Text(common=txt, text="Rhombus: borders")
Rhombus(cx=2, cy=3, width=2, height=3, stroke_width=1.9,
    borders=[
        ("nw", 2, "gold"),
        ("ne", 2, "chartreuse", True),
        ("se", 2, "tomato", [0.1, 0.2]),
        ("sw", 2)
    ]
)
PageBreak()

# ---- trapezoid - borders
Blueprint()
Text(common=txt, text="Trapezoid: borders")
Trapezoid(
    cx=2, cy=3,
    width=2, height=2, top=1.5, stroke_width=2,
    borders=[
        ("w", 2, "gold"),
        ("e", 2, "chartreuse", True),
        ("n", 2, "tomato", [0.1, 0.2]),
        ("s", 2)
    ]
)
PageBreak()

# ---- arrow - sizes
Blueprint()
Text(common=txt, text="Arrow: sizes")
Arrow(x=1, y=5, height=1, width=0.5, head_height=0.5, head_width=0.75)
Arrow(x=2, y=5, height=1, width=0.5, head_height=0.5, head_width=0.75, tail_width=0.75,
      stroke="tomato", fill="lightsteelblue", stroke_width=2, transparency=50)
Arrow(x=3, y=5, height=1, width=0.5, head_height=0.5, head_width=0.75, tail_width=0.01,
      fill_stroke="gold")
Arrow(x=1, y=3, height=1, width=0.25, head_height=0.5, head_width=1, points_offset=-0.25,
      fill="chartreuse")
Arrow(x=2, y=3, height=1, width=0.25, head_height=1, head_width=0.75, points_offset=0.25,
      fill="tomato")
Arrow(x=3, y=3, height=1, width=0.5, head_height=0.5, head_width=0.5, tail_notch=0.25,
      stroke="black", fill="cyan", stroke_width=1)
PageBreak()

# ---- arrow - rotate, text
Blueprint()
Text(common=txt, text="Arrow: dot, cross, text & rotation")
Arrow(x=1, y=5.5, title="The Arrow", heading="An arrow", dot=0.1, cross=0.5)
Arrow(x=2.5, y=3, title="0\u00B0", dot=0.15, dotted=True)
Arrow(x=2.5, y=3, title="45\u00B0", dot=0.1,
      fill=None, stroke="red", dot_stroke="red", rotation=45)
Arrow(x=3, y=5.5, label="arrow")
PageBreak()

# ---- arrowhead
Blueprint(stroke_width=0.5)
Text(common=txt, text="Line: arrow styles")
Line(x=0.5, y=1, x1=0.5, y1=0, arrow=True, stroke="black")
Line(x=1.5, y=1, x1=1.5, y1=0, arrow_style='notch')
Line(x=2.5, y=1, x1=2.5, y1=0, arrow_style='angle')
Line(x=3.5, y=1, x1=3.5, y1=0, arrow_style='spear')

dbl_ang = Common(
    arrow_style='angle',
    arrow_double=True)
Line(common=dbl_ang, x=0, y=1.75, x1=1, y1=1.25)
Line(common=dbl_ang, x=2, y=1.5, x1=1, y1=1.5)
Line(common=dbl_ang, x=2, y=1.25, x1=3, y1=1.75)
Line(common=dbl_ang, x=3, y=1.5, x1=4, y1=1.5)

Line(x=0, y=3, x1=1, y1=2, arrow=True)
Line(x=1, y=3, x1=2, y1=2, arrow_style='notch', stroke="tomato")
Line(x=2, y=3, x1=3, y1=2, arrow_style='angle', stroke="chartreuse")
Line(x=3, y=3, x1=4, y1=2, arrow_style='spear', stroke="aqua")

bigger = Common(arrow_width=0.2, arrow_height=0.3)
Line(common=bigger, x=0, y=4, x1=1, y1=3,)
Line(common=bigger, x=1, y=4, x1=2, y1=3, arrow_style='notch')
Line(common=bigger, x=2, y=4, x1=3, y1=3, arrow_style='angle')
Line(common=bigger, x=3, y=4, x1=4, y1=3, arrow_style='spear')

big_color = Common(
    arrow_width=0.2, arrow_height=0.3,
    arrow_fill="yellow", arrow_stroke="red")
Line(common=big_color, x=0, y=5, x1=1, y1=4,)
Line(common=big_color, x=1, y=5, x1=2, y1=4, arrow_style='notch')
Line(common=big_color, x=2, y=5, x1=3, y1=4, arrow_style='angle')
Line(common=big_color, x=3, y=5, x1=4, y1=4, arrow_style='spear')

Line(x=0.5, y=6, x1=0.5, y1=5,
     stroke_width=1,
     dotted=True,
     arrow_position=0.66,
     arrow_double=True)
Line(x=1, y=6, x1=2, y1=5, arrow_position=[0.25, 0.5, 0.75])
Line(x=2.5, y=6, x1=2.5, y1=5, arrow_position=[1.0, 0.93])
Line(x=3, y=6, x1=4, y1=5,
     arrow_style='spear',
     arrow_height=0.15)
Line(x=3, y=6, x1=4, y1=5,
     arrow_style='angle',
     arrow_width=0.15,
     arrow_position=[0.1, 0.15, 0.2])
PageBreak()

# ---- polyline custom
Blueprint(stroke_width=0.5)
Text(common=txt, text="Polyline: custom")
Polyline(points=[(1, 2), (1, 1), (2, 0), (3, 1), (3, 2)],
         stroke_width=1, stroke="red")
Polyline(x=1, y=3, stroke_width=1,
         steps='0.5,0 0,1.5 1.5,0 0,-1.5 0.5,0 0,0.5 -2.5,0')
PageBreak()

# ---- polyline arrows
Blueprint(stroke_width=0.5)
Text(common=txt, text="Polyline: arrow")
Polyline(
    points=[(1, 3), (2, 4), (2.5, 2), (3, 3), (3.5, 1)],
    stroke_width=1,
    arrow=True
)
Polyline(
    points=[(1, 5), (3, 5)],
    stroke_width=1,
    dotted=True,
    arrow_style='notch',
    arrow_double=True
)
PageBreak()

# ---- Centred Shapes
Blueprint()
Text(common=txt, text="Centred Shapes")
small_star = star(radius=0.25)
Hexagon(x=0.5, y=0.5, height=1, centre_shape=small_star)
Square(x=2.5, y=0.5, height=1, centre_shape=small_star)
Rectangle(x=0.5, y=2.5, height=1, width=1.25, centre_shape=small_star)
Circle(cx=3, cy=3, radius=0.5, centre_shape=small_star)
Polygon(cx=1, cy=5, radius=0.5, sides=8, centre_shape=small_star)
EquilateralTriangle(x=2.35, y=5.5, side=1.25, centre_shape=small_star)
PageBreak()

# ---- Centred Shapes - move
Blueprint()
Text(common=txt, text="Centred Shape: move + double")
small_star = star(radius=0.25)
small_circle = circle(radius=0.33, fill="gray", centre_shape=small_star)
Hexagon(x=1, y=0.5, height=2,
        dot=0.1,
        hatch_count=5,
        centre_shape=small_circle)
Hexagon(x=1, y=3, height=2,
        centre_shape=small_circle,
        centre_shape_mx=0.3, centre_shape_my=0.6)
PageBreak()

# ---- Centred Shapes - customised
Blueprint()
Text(common=txt, text="Centred Shape: customised")
Rectangle(x=0, y=1, side=1,
          centre_shape=polygon(
              radius=0.4,
              sides=7,
              fill=None,
              perbis='*',
              stroke="red"))
Rectangle(x=1, y=2, side=1,
          centre_shape=circle(
              radius=0.3,
              radii=[0,60,120,180,240,300],
              fill=None,
              stroke="green"))
Rectangle(x=2, y=1, side=1,
          centre_shape=hexagon(
              radius=0.4,
              stroke="purple",
              fill=None,
              borders=[("sw n se", 2)]))
Rectangle(x=3, y=2, side=1,
          centre_shape=stadium(
              side=0.4,
              stroke="orange"))
Rectangle(x=0, y=3, side=1,
          centre_shape=ellipse(
              height=0.8,
              width=0.5,
              fill=None,
              stroke="olive"))
Rectangle(x=1, y=4, side=1,
          centre_shape=square(
              side=0.6,
              stroke="gold",
              fill=None,
              hatch='d', hatch_count=5,
              borders=[("n s", 2, "black")]))
Rectangle(x=2, y=3, side=1,
          centre_shape=rhombus(
              side=0.8,
              stroke="gray",
              fill=None,
              borders=[("ne sw", 2, "black")]))
Rectangle(x=3, y=4, side=1,
          centre_shape=trapezoid(
              width=0.6, top=0.4, height=0.8,
              stroke="aqua",
              fill=None,
              flip='south',
              borders=[("e w", 2, "black")]))
PageBreak()

# ---- QR Code
Blueprint()
Text(common=txt, text="QR Code")
QRCode('qrcode1.png', text="Help")
QRCode(
    'qrcode2.png',
    text="Help me ObiWan",
    x=1, y=3,
    height=2, width=2,
    fill="gray",
    stroke="red",
    scaling=5,
)
PageBreak()

# ---- image - sliced
Blueprint()
Text(common=txt, text="Image: sliced")
Image("sholes_typewriter.png", sliced='l',
      width=1, height=3, x=0, y=0)
Image("sholes_typewriter.png", sliced='c',
      width=1, height=3, x=1.5, y=0)
Image("sholes_typewriter.png", sliced='r',
      width=1, height=3, x=3, y=0)
Image("sholes_typewriter.png", sliced='t',
      width=3, height=1, x=0, y=3)
Image("sholes_typewriter.png", sliced='m',
      width=3, height=1, x=0.5, y=4)
Image("sholes_typewriter.png", sliced='b',
      width=3, height=1, x=1.25, y=5)
PageBreak()

# ---- shape rotation
Blueprint()
Text(common=txt, text="Rotation (cross & label)")
props = Common(
    stroke="black",
    cross=0.5, cross_stroke="red", cross_stroke_width=1,
    rotation=45, label_size=6)
Rectangle(cx=1, cy=5, height=1, width=1.5, common=props, label="rectangle")
Rhombus(cx=3, cy=5, side=2, common=props, label="rhombus")
Polygon(cx=1, cy=3, sides=6, side=0.75, common=props, label="polygon")
Stadium(cx=3, cy=3, side=1, common=props, label="stadium")
Star(x=1, y=1, vertices=5, radius=0.75, common=props, label="star")
Ellipse(cx=3, cy=1, height=1, width=1.5, common=props, label="ellipse")
PageBreak()

# ---- shape hatch-and-rotation
Blueprint()
Text(common=txt, text="Hatch & Rotate")
htch = Common(
    fill='lightgray', stroke=None,
    hatch_count=5, hatch_width=0.75,
    hatch='w', hatch_stroke="red")

Hexagon(
    common=htch,
    cx=2, cy=1, height=1.5,
    rotation=30,
    )
EquilateralTriangle(
    common=htch,
    cx=1, cy=3, side=1.5,
    rotation=30,
    )
Rectangle(
    common=htch,
    x=0.5, y=4, height=1.5, width=1,
    rotation=30,
)
Circle(
   common=htch,
   cx=3, cy=3, radius=0.75,
   rotation=30,
)
Rhombus(
   common=htch,
   cx=3, cy=5, height=2, width=1.5,
   rotation=30,
)
PageBreak()

# ---- table - defaults
Blueprint()
Text(common=txt, text="Table: defaults")
Table(cols=2, rows=2)
Table(y=2.5, width=3, height=2, cols=3, rows=4)
PageBreak()

# ---- table - styled
Blueprint()
Text(common=txt, text="Table: styled")
Table(y=0,
      width=3, height=2.5,
      cols=5, rows=6,
      stroke="red", dotted=True)
Table(y=3, x=0,
      cols=[0.5, 1, 1.25, 0.75],
      rows=[0.75, 0.5, 0.5, 0.75],
      stroke="blue", fill="aqua")
PageBreak()

# ---- END
Text(common=txt, text="Shapes END...")

Save(
     output='png',
     dpi=300,
     directory="../docs/source/images/customised",
     names=[
        None,
        "blueprint_subdiv", "dots_crosses", "centred", "right_angled_triangle",
        "compass", "lines", "starfield_rectangle", "starfield_circle",
        "starfield_poly", "equilateral_triangle", "right_angled_triangle_flip",
        "sectors", "grid_gray", "dotgrid_moleskine", "dotgrid_rowscols", "arc",
        "stadium_edges", "trapezoid_flip", "chord",
        "polygon_radii", "polygon_perbis",
        "dates_formats",
        "images_normal_rotation", "rhombus_red_rotation",
        "stadium_red_rotation",
        "slices_rhombus",
        "polygon_rotation_flat",
        "polygon_rotation_pointy", "polygon_sizes", "grid_3x4",
        "line_custom", "line_centred",
        "bezier_custom", "ellipse_custom", "rectangle_custom",
        "square_custom", "trapezoid_custom", "image_default",
        "descriptions", "label_offset", "star_custom",
        "polyshape_default", "polyshape_custom", "polyshape_offset",
        "rectangles_rowcol", "rectangles_custom", "rhombus_custom",
        "rhombus_borders", "trapezoid_borders",
        "arrow_sizes", "arrow_rotate", "arrowheads",
        "polyline_basic", "polyline_arrow",
        "shape_centred", "shape_centred_move", "shape_centred_custom",
        "qr_code", "image_sliced",
        "shape_rotation", "shape_hatch_and_rotation",
        "table_defaults", "table_custom",
        None])
