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
Rhombus(cx=1, cy=5, side=1.25, dot=0.1, dot_stroke="red")
Rhombus(cx=3, cy=5, side=1.25, cross=0.25, cross_stroke="red", cross_stroke_width=1)
Polygon(cx=1, cy=3, sides=8, radius=1, dot=0.1, dot_stroke="orange")
Polygon(cx=3, cy=3, sides=8, diameter=2, cross=0.25, cross_stroke="orange", cross_stroke_width=1)
Stadium(cx=1, cy=1, side=0.66, stroke="blue", dot=0.1)
Stadium(cx=3, cy=1, side=0.66, stroke="blue", cross=0.25, cross_stroke_width=1)
PageBreak()

# ---- centre placement
Blueprint()
Text(common=txt, text="Centred")
shp_font = Common(font_size=6, stroke="red")
Trapezoid(common=shp_font, cx=1, cy=5, heading="Trapezoid cx=1;cy=5")
Rhombus(common=shp_font, cx=3, cy=5, title="Rhombus cx=3;cy=5")
Star(common=shp_font, cx=1, cy=3, heading="Star cx=1;cy=3")
Ellipse(common=shp_font, cx=3, cy=3, width=2, height=1, title="Ellipse cx=3;cy=3")
Polygon(common=shp_font, cx=2, cy=1, radius=0.8, sides=7, heading="Polygon-7 cx2=;cy=1")
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
DotGrid(stroke="darkgray",
        x=0, y=0,
        width=0.5, height=0.5, dot_width=1,
        margin_fit=False) #, offset_y=0.25)
PageBreak()

# ---- dotgrid - rows & cols
Blueprint()
Text(common=txt, text="DotGrid: rows&cols")
DotGrid(stroke="darkgray",
        width=0.5, height=0.5,
        rows=14, cols=10,
        dot_width=1)
PageBreak()

# ---- arc
Blueprint()
Text(common=txt, text="Arc: 'inside' square & nested")
Rectangle(x=1, y=1, height=2, width=2, dot=0.02,
          stroke="red", fill=None,
          title="Arc(cx=1, cy=3, radius=2)")
Arc(cx=1, cy=3, radius=2)  #, angle_start=0, angle_width=90)
Arc(cx=1, cy=6, radius=2, nested=6, angle_start=15, angle_width=60)
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

# ---- cross - custom
Blueprint()
Text(common=txt, text="Cross: customised")
crs = Common(height=1.8, width=1.2, arm_fraction=0.70)
Cross(stroke_width=1, stroke="red", fill="gold")
Cross(cx=3, cy=1, thickness=0.33, fill_stroke="red")
Cross(cx=1, cy=3, common=crs,)
Cross(cx=3, cy=2.5, common=crs,
      title="Title", label="Label", heading="Heading")
Cross(cx=3, cy=5, common=crs,
      dot=0.1, cross=0.5)
Cross(cx=1, cy=5, common=crs, rotation=45)
PageBreak()

# ---- polygon radii
Blueprint()
Text(common=txt, text="Polygon: radii (default & custom)")
Polygon(cx=2, cy=4, sides=8, radius=1, radii="1,3,7")
Polygon(
    cx=2, cy=1, sides=10, radius=1, radii="*",
    radii_offset=0.75, radii_length=0.25, radii_stroke_width=1,
    dot=0.1, dot_stroke="red")
PageBreak()

# ---- polygon perbii
Blueprint()
Text(common=txt, text="Polygon: perbii (default & custom)")
Polygon(cx=2, cy=4, sides=8, radius=1, perbii='*')
Polygon(
    cx=2, cy=1, sides=8, radius=1,
    perbii="2,4,7",
    perbii_offset=0.25, perbii_length=0.5, perbii_stroke_width=1,
    dot=0.1, dot_stroke="red")
PageBreak()

# ---- polygon slices
Blueprint()
Text(common=txt, text="Polygon: slices")
Polygon(
    cx=2, cy=3, sides=8, radius=1,
    slices=['red', 'orange', 'yellow', 'green',
            'aqua', 'pink', 'violet', 'purple'])
PageBreak()

# ---- date formats
Blueprint()
Text(common=txt, text="Today: format and styles")
dtext = Common(x=0.25, align="left", font_size=8)
Text(common=dtext, y=1, text="1.  "+Today())
Text(common=dtext, y=2, text="2.  "+Today(details="date", style="usa"))
Text(common=dtext, y=3, text="3.  "+Today(details="date", style="eur"))
Text(common=dtext, y=4, text="4.  "+Today(details="datetime", style="usa"))
Text(common=dtext, y=5, text="5.  "+Today(details="datetime", style="eur"))
PageBreak()

# ---- rotation - image
Blueprint()
Text(common=txt, text="Image: scaling + rotation")
Image("sholes_typewriter.png",
      width=2, height=2,
      x=0, y=0, title="PNG")
Image("sholes_typewriter.png",
      width=1.5, height=1.5,
      x=2, y=0, title="60\u00B0", rotation=60)
Image("noun-typewriter-3933515.svg",
      width=2, height=2,
      x=0, y=3, title="SVG")
Image("noun-typewriter-3933515.svg",
      width=1.5, height=1.5,
      x=2, y=3, title="45\u00B0", rotation=45)
PageBreak()

# ---- rotation - rhombus
Blueprint()
Text(common=txt, text="Rhombus: red => rotation 60\u00B0")
Rhombus(cx=2, cy=3, width=1.5, height=2*equilateral_height(1.5), dot=0.06,
        fill=None, stroke="black")
Rhombus(cx=2, cy=3, width=1.5, height=2*equilateral_height(1.5), dot=0.03,
        fill=None, stroke="red", rotation=60)
PageBreak()

# ---- rotation - stadium
Blueprint()
Text(common=txt, text="Stadium: red => rotation 60\u00B0")
Stadium(cx=2, cy=3, width=1.25, height=2, dot=0.06)
Stadium(cx=2, cy=3, width=1.25, height=2,
        stroke="red", stroke_width=.3, rotation=60, dot=0.04)
PageBreak()

# ---- slices - rhombus
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

# ---- rotation - polygon
Blueprint()
Text(common=txt, text="Polygon: rotation")
poly6 = Common(fill=None, sides=6, diameter=1, stroke_width=1)
Polygon(common=poly6, cy=1, cx=1.0, label="0")
Polygon(common=poly6, cy=2, cx=1.5, rotation=15, label="15")
Polygon(common=poly6, cy=3, cx=2.0, rotation=30, label="30")
Polygon(common=poly6, cy=4, cx=2.5, rotation=45, label="45")
Polygon(common=poly6, cy=5, cx=3.0, rotation=60, label="60")
PageBreak()

# ---- polygon sizes
Blueprint()
Text(common=txt, text="Polygon: sizes")
Polygon(cx=1, cy=5, sides=7, radius=1, label="Seven")
Polygon(cx=2, cy=3, sides=6, radius=1, label="Six")
Polygon(cx=3, cy=1, sides=5, radius=1, label="Five")
PageBreak()

# ---- grid - cols and rows
Blueprint()
Text(common=txt, text='Grid: gray; 3x4; thick')
Grid(x=0.5, y=0.5, cols=3, rows=4, height=1.25, width=1,
     stroke="gray", stroke_width=1,
     heading="Heading", label="Label", title="Title")
PageBreak()

# ---- grid - ignore_margins
Blueprint()
Text(common=txt, text='Grid: ignore margins')
Grid(x=0, y=0,
     height=0.9, width=1,
     stroke="gray", stroke_width=1,
     margin_fit=False,
     label="Grid Label")
PageBreak()

# ---- grid - omit edges
Blueprint()
Text(common=txt, text='Grid: omit edges')
Grid(x=0.5, y=0.5, rows=3, cols=3,
     side=0.5, stroke_width=0.5,
     omit_left=True)
Grid(x=2.5, y=0.5, rows=3, cols=3,
     side=0.5, stroke_width=0.5,
     omit_bottom=True)
Grid(x=1.5, y=2.5, rows=3, cols=3,
     side=0.5, stroke_width=0.5,
     omit_outer=True)
Grid(x=0.5, y=4.5, rows=3, cols=3,
     side=0.5, stroke_width=0.5,
     omit_top=True)
Grid(x=2.5, y=4.5, rows=3, cols=3,
     side=0.5, stroke_width=0.5,
     omit_right=True)

PageBreak()

# ---- line - custom
Blueprint()
Text(common=txt, text='Line: locations; styles')
Line(x=0, y=0.5, stroke_width=0.2, dotted=True, label="0.2", font_size=6)
Line(x=1, y=0.5, stroke_width=0.4, dotted=True, label="0.4", font_size=6)
Line(x=2, y=0.5, stroke_width=0.8, dotted=True, label="0.8", font_size=6)
Line(x=3, y=0.5, stroke_width=1.6, dotted=True, label="1.6", font_size=6)

Line(x=1, y=1, length=2, stroke="chartreuse", stroke_width=10)
Line(x=1, y=1.5, length=2, stroke="aqua", stroke_width=10, stroke_ends="rounded")
Line(x=1, y=2, length=2, stroke="gold", stroke_width=10, stroke_ends="squared")

Line(x=0, y=2.5, length=4, stroke="pink", stroke_width=2)
Line(x=0, y=3.6, length=4.1, angle=15, stroke="red", label="15", font_size=6)
Line(x=0, y=5, x1=4, y1=5.9, stroke="blue", stroke_width=1,
     dashed=[0.2, 0.1], label="dashed:[0.2,0.1]", font_size=6)

Line(x=0, y=4, x1=4, y1=4, stroke="purple", stroke_width=1,
     wave_style='wave', wave_height=1.9)
Line(x=0, y=4, x1=4, y1=4, stroke="firebrick", stroke_width=1,
     wave_style='sawtooth', wave_height=0.1)
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

# ---- line - connections: circle
Blueprint(stroke_width=0.5)
Text(common=txt, text="Line: connections; circles")
cc = Circle(cx=2, cy=3, radius=0.5)
cy = Circle(cx=1, cy=1, radius=0.5, fill_stroke="yellow")
Line(connections=[cc, cy])
ca = Circle(cx=1, cy=5, radius=0.5, fill_stroke="aqua")
Line(connections=[cc, ca])
cr = Circle(cx=3, cy=1, radius=0.5, fill_stroke="red")
Line(connections=[cc, cr])
co = Circle(cx=3, cy=5, radius=0.5, fill_stroke="orange")
Line(connections=[cc, co])
# orthogonal
Line(connections=[cy, cr, co, ca, cy], stroke_width=2)
PageBreak()

# ---- line - connections: shapes
Blueprint(stroke_width=0.5)
Text(common=txt, text="Line: connections; shapes")
s1 = Square(cx=1, cy=4, side=1, fill="yellow")
s2 = Square(cx=3, cy=2, side=1)
Line(
    connections=[(s1, 'v', 'ne'), (s2, 'p', 'w')],
    stroke="red",
    stroke_width=2)
PageBreak()

# ---- line - connections - arrow
Blueprint(stroke_width=0.5)
Text(common=txt, text="Line: connections; arrow")
cc = Circle(cx=1.5, cy=3.5, radius=0.5)
cy = Circle(cx=1, cy=1, radius=0.5, fill_stroke="yellow")
co = Circle(cx=3, cy=5, radius=0.5, fill_stroke="orange")
Line(connections=[cy, cc, co],
     stroke="red",
     stroke_width=1,
     arrow=True,
     )
PageBreak()

# ---- line - connections - dot&spoke
Blueprint(stroke_width=0.5)
Text(common=txt, text="Line: connections; dot&spoke")
cc = Dot(cx=1.5, cy=3.5, dot_width=2)
cr = Circle(cx=3, cy=1, radius=0.5, fill_stroke="red")
co = Circle(cx=3, cy=5, radius=0.5, fill_stroke="orange")
ca = Circle(cx=1, cy=5, radius=0.5, fill_stroke="aqua")
Line(connections=[cc, cr, co, ca],
     connections_style='spoke',
     stroke="green",
     stroke_width=1,
     arrow=True,
     )
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

# ---- star_custom
Blueprint(stroke_width=0.5)
Text(common=txt, text="Star: custom")
Star(cx=1, cy=1, radius=1,
     fill="red",
     stroke="gold",
     stroke_width=2,
     inner_fraction=0.4,
)
Star(cx=2, cy=3, radius=1,
     rays=6,
     show_radii="*",
     rotation=30,
)
Star(cx=3, cy=5, radius=1,
     fill=None,
     rays=12,
     inner_fraction=0.1,
)
PageBreak()

# ---- star_slices
Blueprint()
Text(common=txt, text="Star: slices")
Star(cx=2, cy=1, radius=1,
     rays=4,
     inner_fraction=0.33,
     stroke_width=2,
     slices=["black", "white"],
     dot=0.02,
     dot_stroke="red",
 )
Star(cx=2, cy=4, radius=1,
     slices=[
        "#CE8F0C",
        "#F8C40C",
        "#F3BA0B",
        "#DB9F0D",
        "#F8C609",
        "#CE8F0C",
        "#F7C30D",
        "#D59A0E",
        "#CE8F0C",
        "#F7C615",
    ]
)
PageBreak()

# ---- polyshape
Blueprint(stroke_width=0.5)
Text(common=txt, text="Polyshape: default")
Polyshape(points=[(1, 2), (1, 1), (2, 0), (3, 1), (3, 2)])
# Polyshape(x=1, y=3,
#          steps='0.5,0 0,1.5 1.5,0 0,-1.5 0.5,0 0,0.5 -2.5,0 0,-0.5')
PageBreak()

# ---- polyshape - custom
Blueprint(stroke_width=0.5)
Text(common=txt, text="Polyshape: custom")
Polyshape(
    x=0, y=1,
    points=[(1, 2), (1, 1), (2, 0), (3, 1), (3, 2)],
    cx=2, cy=1,
    label='A House',
    label_stroke="seagreen",
    cross=0.5,
    fill="sandybrown",
    stroke="peru",
)
Polyshape(
    x=1, y=4,
    steps='0.5,0 0,1.5 1.5,0 0,-1.5 0.5,0 0,0.5 -2.5,0 0,-0.5',
    stroke="sandybrown", stroke_width=3, fill="seagreen")
PageBreak()

# ---- shapeshape - offset + string
Blueprint(stroke_width=0.5)
Text(common=txt, text="Polyshape: offset")
Polyshape(
    points="0,0 0,1 2,0 2,1 0,0",
    cx=1, cy=0.5,
    fill="gold",
    label="Left ....... Right")
Polyshape(
    x=1, y=2,
    points="0,0 0,1 2,0 2,1 0,0",
    fill="chartreuse",
    label="Left ....... Right")
PageBreak()

# ---- polyshape - snail
Blueprint(stroke_width=0.5)
Text(common=txt, text="Polyshape: snail")
Polyshape(
    x=0.5, y=1.5,
    snail="ne 1 r65 1 ne 1.5 r125 1.44 **",
    stroke_width=1,
    #scaling=0.25,
    stroke="red",
    fill="tan")
Polyshape(
    x=1, y=2.5,
    snail="2 r160 "*9,
    stroke_width=0.5,
    #scaling=0.25,
    stroke="red",
    fill="yellow")
Polyshape(
    x=1.5, y=4,
    snail='w .5 s .5 e 2.5 n .5 w .5 s 1.5 w 1.5 n .5',
    stroke="sandybrown",
    stroke_width=3,
    fill="seagreen")
Polyshape(
    x=2, y=4.75,
    snail='w .5 s .5 e 2.5 n .5 w .5 s 1.5 w 1.5 n .5',
    scaling=0.25,
    stroke="sandybrown",
    stroke_width=1,
    fill="seagreen")
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

# ---- polyline - custom
Blueprint(stroke_width=0.5)
Text(common=txt, text="Polyline: custom")
Polyline(points=[(1, 2), (1, 1), (2, 0), (3, 1), (3, 2)],
         stroke_width=1, stroke="red")
Polyline(x=1, y=3, stroke_width=1,
         steps='0.5,0 0,1.5 1.5,0 0,-1.5 0.5,0 0,0.5 -2.5,0')
PageBreak()

# ---- polyline - arrows
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

# ---- polyline - snail
Blueprint(stroke_width=0.5)
Text(common=txt, text="Polyline: snail")
snail_line = "n 3 e 2 -45 2 w 1 sw 3 **"
Polyline(
    y=0.5,
    snail="2 s 1 w 2 n 0.5",
    stroke_width=1,
    stroke="red",
    arrow=True)
Polyline(
    x=0, y=5,
    snail=snail_line,
    stroke_width=1,
)
Polyline(
    x=0, y=5,
    snail=snail_line,
    stroke_width=1,
    scaling=0.5
)
Polyline(
    y=3, x=2,
    snail="e 1 s 1 w 1 n 1 s j1 "*3,
    stroke_width=2,
    stroke="blue")
Polyline(
    x=3.5, y=1,
    snail="s 0.4 j0.1 "*8,
    stroke_width=1,
    stroke="green")
PageBreak()

# ---- polyline - snail - curve
Blueprint(stroke_width=0.5)
Text(common=txt, text="Polyline: snail; curves")
Polyline(
    y=1, x=0,
    snail="(1.118 60 1) (1.118 -60 1) "*2,
    stroke_width=1,
    stroke="red")
Polyline(
    y=2, x=0,
    snail="(1.118 60 1) (1.118 -60 1) "*8,
    scaling=0.25,
    stroke_width=1,
    stroke="red")
Polyline(
    y=4, x=0,
    snail="a45 (0.6 60 0.707) e 0.5 "*3,
    stroke_width=1,
    stroke="red")
Polyline(
    y=5, x=2,
    snail="r60 (1.118 r60 1) * "*6,
    stroke_width=1,
    stroke="red")

PageBreak()

# ---- centred shapes
Blueprint()
Text(common=txt, text="Centred Shape")
small_star = star(radius=0.25)
Hexagon(x=0.5, y=0.5, height=1, centre_shape=small_star)
Square(x=2.5, y=0.5, height=1, centre_shape=small_star)
Rectangle(x=0.25, y=2.5, height=1, width=1.5, centre_shape=small_star)
Circle(cx=3, cy=3, radius=0.5, centre_shape=small_star)
Polygon(cx=1, cy=5, radius=0.5, sides=8, centre_shape=small_star)
Triangle(cx=3, cy=5, side=1.25, centre_shape=small_star)
PageBreak()

# ---- centre shape - move
Blueprint()
Text(common=txt, text="Centred Shape: move + double")
small_star = star(radius=0.25)
small_circle = circle(radius=0.33, fill="gray", centre_shape=small_star)
Hexagon(x=1, y=0.5, height=2,
        dot=0.1,
        hatches_count=5,
        centre_shape=small_circle)
Hexagon(x=1, y=3, height=2,
        centre_shape=small_circle,
        centre_shape_mx=0.3, centre_shape_my=0.6)
PageBreak()

# ---- centred shapes - customised
Blueprint()
Text(common=txt, text="Centre shape: customised")
Rectangle(x=0, y=1, side=1,
          centre_shape=polygon(
              radius=0.4,
              sides=7,
              fill=None,
              perbii='*',
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
              side=0.3,
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
              hatches='d', hatches_count=5,
              borders=[("n s", 2, "black")]))
Rectangle(x=2, y=3, side=1,
          centre_shape=rhombus(
              side=0.6,
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

# ---- Centred Shapes
Blueprint()
Text(common=txt, text="Centred Shapes (with offsets)")
small_dot = dot(dot_width=4, fill="red")
big_dot = dot(dot_width=8)
Hexagon(x=0.5, y=0.5, height=1, centre_shapes=[(small_dot), (big_dot, 0.2, 0.2)])
Rhombus(x=2.4, y=0.3, height=1.5,  width=1.25, centre_shapes=[(small_dot), (big_dot, 0.2, 0.2)])
Rectangle(x=0.5, y=2.5, height=1, width=1.25, centre_shapes=[(small_dot), (big_dot, 0.2, 0.2)])
Circle(cx=3, cy=3, radius=0.5, centre_shapes=[(small_dot), (big_dot, 0.2, 0.2)])
Polygon(cx=1, cy=5, radius=0.5, sides=8, centre_shapes=[(small_dot), (big_dot, 0.2, 0.2)])
Triangle(cx=3, cy=5, side=1.25, centre_shapes=[(small_dot), (big_dot, 0.2, 0.2)])
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

# ---- image - label heading title
Blueprint()
Text(common=txt, text="Image: label, heading, title")
Rectangle(width=2.26, height=2, x=1, y=0.5,
          dotted=True, fill="silver")
Image("sholes_typewriter.png",
      width=2.26, height=2, x=1, y=0.5,
      label="Label", label_stroke='red',
      cross=True)
Rectangle(width=2.26, height=2, x=1, y=3.5,
          dotted=True, fill="silver")
Image("sholes_typewriter.png",
      width=2.26, height=2, x=1, y=3.5,
      heading="Heading",
      title="Title",
      dot=0.1, dot_stroke='red')
PageBreak()

# ---- image - operations
Blueprint()
Text(common=txt, text="Image: operations")
image_file = "fantasy-forest-with-old-bridges.png"
Image(image_file,
      width=2, height=2,
      x=0, y=0)
Image(image_file,
      width=1.5, height=1.5,
      x=2, y=0,
      operation=['c', 100, 75, -75]
)
Image(image_file,
      width=1.5, height=1.5,
      x=2.5, y=0.5,
      operation=['c', 100, -75, 75]
)
Image(image_file,
      width=2, height=2,
      x=0, y=2,
      operation=['r', 50]
)
Image(image_file,
      width=2, height=2,
      x=2, y=2,
      operation=['e', (160, 240)]
)
Image(image_file,
      width=2, height=2,
      x=0, y=4,
      operation=['p', 140, 5]
)
Image(image_file,
      width=2, height=2,
      x=2, y=4,
      operation=['b', 20]
)
PageBreak()

# ---- image - align
Blueprint()
Text(common=txt, text="Image: align")
rdot = Common(fill_stroke="red", radius=0.05)
image_file = "fantasy-forest-with-old-bridges.png"
Image(image_file,
      width=1, height=1,
      x=0.5, y=0.5,
      title="no align")
Circle(common=rdot, cx=0.5, cy=0.5)
Image(image_file,
      width=1, height=1,
      cx=3, cy=1,
      title="centre x,y")
Image(image_file,
      width=1, height=1,
      x=2, y=4,
      align_horizontal="right",
      align_vertical="bottom",
      title="bottom-right")
Circle(common=rdot, cx=2, cy=4)
Image(image_file,
      width=1, height=1,
      x=2, y=2,
      align_horizontal="left",
      align_vertical="top",
      title="top-left")
Circle(common=rdot, cx=2, cy=2)
Image(image_file,
      width=1, height=1,
      x=0, y=5,
      align_horizontal="left",
      align_vertical="mid",
      title="mid-left")
Circle(common=rdot, cx=0, cy=5)
Image(image_file,
      width=1, height=1,
      x=3, y=5,
      align_horizontal="centre",
      align_vertical="mid",
      title="mid-centre")
Circle(common=rdot, cx=3, cy=5)
PageBreak()

# ---- shape rotation I
Blueprint()
Text(common=txt, text="Rotation I (cross & label)")
props = Common(
    stroke="black",
    cross=0.5, cross_stroke="red", cross_stroke_width=1,
    rotation=45, label_size=6)
Rectangle(cx=1, cy=5, height=1, width=1.5, common=props, label="rectangle")
Rhombus(cx=3, cy=5, side=1.25, common=props, label="rhombus")
Polygon(cx=1, cy=3, sides=6, side=0.75, common=props, label="polygon")
Stadium(cx=3, cy=3, side=0.6, common=props, label="stadium")
Star(x=1, y=1, vertices=5, radius=0.75, common=props, label="star")
Ellipse(cx=3, cy=1, height=1, width=1.5, common=props, label="ellipse")
PageBreak()

# ---- shape rotation II
Blueprint()
Text(common=txt, text="Rotation II (cross & label)")
props = Common(
    stroke="black",
    cross=0.5, cross_stroke="red", cross_stroke_width=1,
    rotation=45, label_size=6)
Square(cx=1, cy=1, side=1.25, common=props, label="square")
Trapezoid(cx=3, cy=1, width=1.25, top=0.75, height=1, common=props, label="trapezoid")
Hexagon(cx=1, cy=3, side=0.75, common=props, label="hex:flat")
Hexagon(cx=3, cy=3, side=0.75, orientation="pointy", common=props, label="hex:pointy")
Triangle(cx=1, cy=5, side=1.5, common=props, label="tri:equi")
Triangle(x=2.5, y=5.5, side=1, height=1.5, common=props, label="tri:isos")
PageBreak()

# ---- shape hatches-and-rotation
Blueprint()
Text(common=txt, text="Hatches & Rotate")
htch = Common(
    fill='lightgray', stroke=None,
    hatches_count=5,
    hatches='w',
    hatches_stroke_width=0.75,
    hatches_stroke="red")

Hexagon(
    common=htch,
    cx=2, cy=1, height=1.5,
    rotation=30,
    )
Triangle(
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

# ---- wave styles
Blueprint()
Text(common=txt, text="Wave Styles")

Line(
    x=0, y=0.5, length=1.5, stroke="purple", stroke_width=1,
    wave_style='wave', wave_height=0.1)
Line(
    x=2, y=0.5, length=1.5, stroke="firebrick", stroke_width=1,
    wave_style='sawtooth', wave_height=0.1)
Polygon(
    perbii_stroke="purple", perbii_stroke_width=1,
    perbii_wave_style='wave', perbii_wave_height=0.1,
    cx=1, cy=1.5, sides=8, radius=0.75,
    perbii="2,4,7")
Polygon(
    radii_stroke="firebrick", radii_stroke_width=1,
    radii_wave_style='sawtooth', radii_wave_height=0.1,
    cx=3, cy=1.5, sides=8, radius=0.75,
    radii="*")
Rectangle(
    perbii_stroke="purple", perbii_stroke_width=1,
    perbii_wave_style='wave', perbii_wave_height=0.1,
    cx=1, cy=3.25, height=1, width=2,
    perbii="n s e w",
)
Circle(
    radii_stroke="firebrick", radii_stroke_width=1,
    radii_wave_style='sawtooth', radii_wave_height=0.1,
    cx=3, cy=3.25, radius=0.75,
    radii=[60,180,300],
)
Hexagon(
    cx=1, cy=5, radius=0.75,
    perbii='*',
    perbii_stroke="purple", perbii_stroke_width=1,
    perbii_wave_style='wave', perbii_wave_height=0.1
)
Hexagon(
    cx=3, cy=5, radius=0.75,
    radii="ne se w",
    radii_stroke="firebrick", radii_stroke_width=1,
    radii_wave_style='sawtooth', radii_wave_height=0.1
)
PageBreak()

# ---- poly wave styles
Blueprint()
Text(common=txt, text="Poly... waves")
Polyshape(
    points=[(1, 2), (1, 1), (2, 0), (3, 1), (3, 2)],
    wave_style="wave", wave_height=0.03,
    fill="gold")
Polyline(points='1,3 1,4 2,4 4,3',
         stroke="red", stroke_width=2,
         wave_style="sawtooth", wave_height=0.03,)
Polyline(points='1,5 1,6 2,6 4,5',
         stroke="purple", stroke_width=2,
         wave_style="wave", wave_height=0.05,)
PageBreak()

# ---- vertex shapes
Blueprint()
Text(common=txt, text="Vertex Shapes")
Rectangle(
    cx=1, cy=1,
    height=1,
    width=1.5,
    vertex_shapes=[circle(radius=0.15, label="R")]*4,
    vertex_shapes_rotated=True)
Hexagon(
    cx=3, cy=1,
    radius=1,
    vertex_shapes=[circle(radius=0.15, label="H")]*6,
    vertex_shapes_rotated=True)
Polygon(
    cx=1, cy=3,
    sides=5,
    radius=1,
    vertex_shapes=[circle(radius=0.15, label="P")]*5,
    vertex_shapes_rotated=True)
Trapezoid(
    cx=3, cy=3,
    width=1.5, top=1, height=1.25,
    vertex_shapes=[circle(radius=0.15, label="T")]*5,
    vertex_shapes_rotated=True)
Triangle(
    cx=1, cy=5,
    side=1.5,
    vertex_shapes=[circle(radius=0.15, label="E")]*3,
    vertex_shapes_rotated=True)
Star(
    cx=3, cy=5,
    radius=1,
    rays=5,
    vertex_shapes=[circle(radius=0.15, label="S")]*5,
    vertex_shapes_rotated=True)
PageBreak()

# ---- radii shapes
Blueprint()
Text(common=txt, text="Radii shapes")
ccom = Common(radius=0.15, fill="gold", label_size=6)
Hexagon(
    cx=1, cy=1,
    radius=0.8,
    orientation="pointy",
    radii_shapes=[
        ('n', circle(common=ccom, label="n")),
        ('se', circle(common=ccom, label="se"), 1.25),
        ('sw', circle(common=ccom, label="sw"), 0.5 ),
    ],
    radii_shapes_rotated=True,
)
Hexagon(
    cx=3, cy=1,
    radius=0.8,
    radii_shapes=[
       ('ne', circle(common=ccom, label="ne")),
       ('se', circle(common=ccom, label="se"), 1.25),
       ('sw', circle(common=ccom, label="sw"), 0.5),
    ],
    radii_shapes_rotated=True,
)
Rectangle(
    cx=1, cy=3,
    height=1, width=1.5,
    radii_shapes=[
        ('ne', circle(common=ccom, label="ne")),
        ('se', circle(common=ccom, label="se")),
        ('sw', circle(common=ccom, label="sw")),
        ('nw', circle(common=ccom, label="nw")),
    ],
    radii_shapes_rotated=True,
)
Rhombus(
    cx=3, cy=3,
    width=1, height=1.5,
    radii_shapes=[
        ('n', circle(common=ccom, label="n")),
        ('s', circle(common=ccom, label="s")),
        ('e', circle(common=ccom, label="e")),
        ('w', circle(common=ccom, label="w")),
    ],
    radii_shapes_rotated=True,
)
Triangle(
    cx=1, cy=5,
    side=1.25,
    radii_shapes=[
        ('n', circle(common=ccom, label="n")),
        ('se', circle(common=ccom, label="se")),
        ('sw', circle(common=ccom, label="sw")),
    ],
    radii_shapes_rotated=True,
)
Circle(
    cx=3, cy=5,
    radius=0.75,
    radii_shapes=[
        ('30 90 150 210 270 330', circle(common=ccom, label="A")),
    ],
    radii_shapes_rotated=True,
)
PageBreak()

# ---- perbii shapes
Blueprint()
Text(common=txt, text="Perbii shapes")
ccom = Common(radius=0.15, fill="gold", label_size=6)
Hexagon(
    cx=1, cy=1,
    radius=0.8,
    orientation="pointy",
    perbii_shapes=[
        ('ne', circle(common=ccom, label="ne")),
        ('se', circle(common=ccom, label="se"), 1.25),
        ('w', circle(common=ccom, label="w"), 0.5 ),
    ],
    perbii_shapes_rotated=True,
)
Hexagon(
    cx=3, cy=1,
    radius=0.8,
    perbii_shapes=[
       ('n', circle(common=ccom, label="n")),
       ('se', circle(common=ccom, label="se"), 1.25),
       ('sw', circle(common=ccom, label="sw"), 0.5),
    ],
    perbii_shapes_rotated=True,
)
Rectangle(
    cx=1, cy=3,
    height=1, width=1.5,
    perbii_shapes=[
        ('n', circle(common=ccom, label="n")),
        ('s', circle(common=ccom, label="s.")),
        ('w', circle(common=ccom, label="w")),
        ('e', circle(common=ccom, label="e")),
    ],
    perbii_shapes_rotated=True,
)
Rhombus(
    cx=3, cy=3,
    width=1, height=1.5,
    perbii="ne se nw sw",
    perbii_shapes=[
        ('ne', circle(common=ccom, label="ne")),
        ('se', circle(common=ccom, label="se")),
        ('nw', circle(common=ccom, label="nw")),
        ('sw', circle(common=ccom, label="sw")),
    ],
    perbii_shapes_rotated=True,
)
Triangle(
    cx=1, cy=5,
    side=1.25,
    perbii_shapes=[
        ('ne', circle(common=ccom, label="ne")),
        ('s', circle(common=ccom, label="s.")),
        ('nw', circle(common=ccom, label="nw")),
    ],
    perbii_shapes_rotated=True,
)
PageBreak()

# ---- pod: custom 1
Blueprint()
Text(common=txt, text="Pod: customised #1")
Pod()
Pod(cx=3, cy=1,
    center_line=True)
Pod(x=1, y=2, rotation=30)
Pod(cx=3, cy=2, rotation=90)
Pod(cx=2, cy=3,
    length=2)
Pod(cx=2, cy=5,
    heading="Head",
    title="Title",
    label="Label")
PageBreak()

# ---- pod: custom 2
Blueprint()
Text(common=txt, text="Pod: customised #2")
Pod(cx=2, cy=1,
    length=2,
    center_line=True,
    fill="gold",
    stroke="red",
    stroke_width=1)
Pod(cx=1, cy=3,
    dy1=1,
    fill="tan")
Pod(cx=3, cy=3,
    dy1=1, dx1=0.1,
    fill="aqua")
Pod(cx=1, cy=4.5,
    dy1=0.1,
    dy2=0.5, dx2=-1.2,
    fill="silver")
Pod(cx=3, cy=4.5,
    dx1=-0.6, dy1=-0.5,
    dx2=0.15, dy2=-1,
    fill_stroke="tomato",
    rotation=-90)
PageBreak()

# ---- END
Text(common=txt, text="Shapes END...")

# ---- SAVE
#Save()
Save(
     output='png',
     dpi=300,
     directory="../docs/source/images/customised",
     names=[
        None,
        "blueprint_subdiv", "dots_crosses", "centred",
        "lines",
        "starfield_rectangle", "starfield_circle", "starfield_poly",
        "sectors", "grid_gray",
        "dotgrid_moleskine", "dotgrid_rowscols", "arc",
        "stadium_edges", "trapezoid_flip", "chord", "cross",
        "polygon_radii", "polygon_perbii", "polygon_slices",
        "dates_formats",
        "images_normal_rotation", "rhombus_red_rotation",
        "stadium_red_rotation",
        "slices_rhombus",
        "polygon_rotation_flat",
        "polygon_sizes",
        "grid_3x4", "grid_ignore_margins", "grid_omit_edges",
        "line_custom", "line_centred",
        "line_connections_circle", "line_connections_shapes",
        "line_connections_arrow", "line_connections_spoke",
        "bezier_custom", "ellipse_custom", "rectangle_custom",
        "square_custom", "trapezoid_custom", "image_default",
        "descriptions", "label_offset",
        "star_custom", "star_slices",
        "polyshape_default", "polyshape_custom", "polyshape_offset",
        "polyshape_snail",
        "rectangles_rowcol", "rectangles_custom", "rhombus_custom",
        "rhombus_borders", "trapezoid_borders",
        "arrow_sizes", "arrow_rotate", "arrowheads",
        "polyline_basic", "polyline_arrow", "polyline_snail", "polyline_snail_curve",
        "shape_centred", "shape_centred_move", "shape_centred_custom",
        "shapes_centred",
        "qr_code",
        "image_sliced", "image_label",
        "image_operations", "image_align",
        "shape_rotation",
        "shape_rotation_two",
        "shape_hatches_and_rotation",
        "table_defaults", "table_custom",
        "perbii_styled",
        "poly_waves",
        "vertex_shapes",
        "radii_shapes",
        "perbii_shapes",
        "pod_custom",
        "pod_customised",
        None])
