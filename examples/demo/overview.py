# -*- coding: utf-8 -*-
"""
An overview of protograf capabilities

Written by: Derek Hohls
Created on: 29 November 2025

Font sources:
    * https://fonts.google.com/specimen/Eagle+Lake
    * https://fonts.google.com/specimen/Quintessential
    * https://github.com/toddfast/game-icons-net-font (Icons)
"""
from protograf import *

Create(
   filename="overview.pdf", margin=1, page_grid=2)

# ---- default & common
txt = Default(x=5, font_size=20, align="left", font_name="Courier-Bold")
ctxt = Default(x=5, font_size=20, align="left")
header = Common(x=10, y=0, font_size=24, font_name="Helvetica", align="centre")

# ---- title
Image("protograf_slogan.png", x=3.5, y=8, height=3.6, width=12)
Text('A Brief Tour...', font_size=48, stroke="#3286AD", x=9.5, y=15)
PageBreak()

# ---- simple
Rectangle()
Text('... a rectangle!', default=ctxt)
PageBreak()


# ---- base
Rectangle()
Text('What does the script look like?', default=ctxt, y=6, x=1)
Text("""from protograf import *

Create(
  filename='overview.pdf',
  margin=1, 
  page_grid=2
)
Rectangle()
Save()""",
  box=True,
  font_name="Courier-Bold",
  font_size=24,
  align="left",
  x=1, y=8,
  height=15,
  width=15)
Text("A protograf script", common=header)
PageBreak()


# ---- styled
Rectangle(width=3, height=4)
Text('Rectangle(\n width=3, height=4)', default=txt, y=1.5)
Rectangle(y=6.5, width=3, height=4, fill="yellow", stroke="red", stroke_width=4)
Text('Rectangle(\n width=3, height=4, y=6,\n fill="yellow", stroke="red",\n stroke_width=4)', default=txt, y=7)
Rectangle(y=12, width=3, height=4, label="Hi!", label_size=18)
Text('Rectangle(\n width=3, height=4, y=11,\n label="Hi!,\n label_size=18")', default=txt, y=12.5)
Rectangle(y=17.5, width=3, height=4, hatches_count=5)
Text('Rectangle(\n width=3, height=4, y=16,\n hatches_count=5)', default=txt, y=18)
Rectangle(
    y=23, width=3, height=4,
    notch_style='bite', notch=0.5,
    radii_shapes=[('*', dot())])
Text('Rectangle(\n width=3, height=4, y=21,\n notch_style="bite",\n notch=0.5, \n radii_shapes=[("*", dot())])', default=txt, y=23.5)
Text("Styling a Rectangle", common=header)
PageBreak()


# ---- filled shapes
Text("Shapes", common=header)
shp = Default(title_stroke="black", title_size=18)
Arrow(x=3, y=27,  height=2, width=1,
      title="Arrow", default=shp, fill_stroke="plum")
Cross(cx=9, cy=26, height=3, width=3, thickness=1,
      title="Cross", default=shp, fill_stroke="plum")
Sector(cx=16, cy=27, radius=3, angle_start=68, angle_width=44,
      title="Sector", default=shp, fill_stroke="plum")
Pod(cx=3, cy=21, length=5, dx=2,
    title="Pod", default=shp, fill_stroke="tomato")
Ellipse(cx=9, cy=21, width=5, height=3,
        title="Ellipse", default=shp, fill_stroke="tomato")
Stadium(cx=16, cy=21, width=3, height=2,
        title="Stadium", default=shp, fill_stroke="tomato")
Hexagon(cx=3, cy=15, side=2, orientation="flat",
        title="Hexagon", default=shp, fill_stroke="gold")
Triangle(
    cx=9, cy=15, side=4,
    title="Triangle", default=shp, fill_stroke="gold")
Trapezoid(cx=16, cy=15, width=4, top=2, height=3,
          title="Trapezoid", default=shp, fill_stroke="gold")
Hexagon(cx=3, cy=9, side=2, orientation="pointy",
        title="Hexagon", default=shp, fill_stroke="chartreuse")
Polygon(cx=9, cy=9, radius=2, sides=8,
        title="Polygon", default=shp, fill_stroke="chartreuse")
Circle(cx=16, cy=9, radius=2,
       title="Circle", default=shp, fill_stroke="chartreuse")
Star(cx=3, cy=3, vertices=5, radius=2,
     title="Star", default=shp, fill_stroke="cyan")
Rhombus(cx=16, cy=3, width=3, height=5,
        title="Rhombus", default=shp, fill_stroke="cyan")
Square(cx=9, cy=3, side=3,
       title="Square", default=shp, fill_stroke="cyan")
Dot(cx=3, cy=0, dot_width=12, title="Dot", default=shp, fill_stroke="red")
PageBreak()


# ---- shape properties
cmm = circle(radius=0.25, fill_stroke="cyan")
# ---- * circle hatches
Circle(
    cx=2, cy=2, radius=1.5,
    hatches_count=5, hatches_stroke="red",
    hatches='n d')
# ---- * circle radii
Circle(
    cx=2, cy=6, radius=1.5,
    fill=None,
    radii=[45, 135, 225, 315],
    radii_stroke_width=2,
    radii_dotted=True,
    radii_offset=1,
    radii_length=1.25)
# ---- * circle radii shapes
Circle(
    cx=2, cy=10, radius=1.5,
    radii_shapes=[
        ('30 90 150 210 270 330', 
         circle(radius=0.25, fill_stroke="cyan", label="S")),
    ],
    radii_shapes_rotated=True)
# ---- * circle slices
Circle(
    cx=2, cy=14, radius=1.5,
    slices=["red", "gold", "aqua", "red", "gold", "aqua"],
    rotation=30,
    dot=0.05)
# ---- * circle petals_sun
Circle(
    cx=2, cy=18, radius=1.5,
    fill_stroke="yellow",
    petals=8,
    petals_style="s",
    petals_offset=0.1,
    petals_stroke_width=2,
    petals_height=0.5,
    petals_stroke="red",
    petals_fill="yellow",
    title="petals", default=shp)
# ---- * circle nested
Circle(
   cx=2, cy=24, radius=1.5, 
   nested=4,
   dotted=True, 
   stroke="red", fill="yellow",
   title="nested", default=shp)
# ---- RECTANGLE
# ---- * rect hatches
Rectangle(
   x=6, y=1,
   height=3, width=2.5,
   hatches_count=5,
   hatches_stroke_width=2, 
   hatches_stroke="red",
   hatches='ne')
# ---- * rect radii
Rectangle(
   x=6, y=5,
   height=3, width=2.5,
   radii="*")
# ---- * rect radii shapes
Rectangle(
    x=6, y=9,
    height=3, width=2.5,
    radii_shapes=[
        ('ne', circle(common=cmm, label="ne")),
        ('se', circle(common=cmm, label="se")),
        ('sw', circle(common=cmm, label="sw")),
        ('nw', circle(common=cmm, label="nw")),
    ],
    radii_shapes_rotated=True)
# ---- * rect slices
Rectangle(
    x=6, y=13,
    height=3, width=2.5,
    slices=['tomato', 'aqua', 'gold', 'chartreuse'],
    fill=None)
# ---- * rect chevron
Rectangle(
    x=6, y=17,
    height=3, width=2.5,
    chevron='N',
    chevron_height=0.5,
    title="chevron", default=shp)
# ---- * rect prow
Rectangle(
    x=6, y=23,
    height=3, width=2.5,
    fill="silver",
    stroke="darkgrey", stroke_width=2,
    prows=[
        ("n", 1, (0.44, 0.44)),
        ("s", 0.3, (0.2, 0.2)),
    ],
    title="prow", default=shp
)
# ---- HEXAGON
# ---- * hex hatches
Hexagon(
    cx=12, cy=2, height=3, 
    hatches_count=5,
    hatches_stroke_width=2, 
    hatches_stroke="red",
    hatches='ne')
# ---- * hex radii
Hexagon(
    cx=12, cy=6, height=3, 
    radii="*")
# ---- * hex radii shapes
Hexagon(
    cx=12, cy=10, height=3, 
    radii_shapes=[
        ('ne', circle(common=cmm, label="ne")),
        ('se', circle(common=cmm, label="se")),
        ('sw', circle(common=cmm, label="sw")),
        ('nw', circle(common=cmm, label="nw")),
    ],
    radii_shapes_rotated=True)
# ---- * hex slices
Hexagon(
    cx=12, cy=14, height=3, 
    slices=['tomato', 'aqua', 'gold', 'chartreuse'],
    fill=None)
# ---- * hex spikes
Hexagon(
    cx=12, cy=18, height=3, 
    spikes=["sw", "nw", "ne", "se"],
    spikes_height=1,
    spikes_width=0.5,
    spikes_stroke="tomato",
    spikes_fill="tomato",
    title="spikes", default=shp)
# ---- * hex paths
Hexagon(
    cx=12, cy=24, height=3,
    paths=["s nw", "n ne", "n nw", "ne s"],
    paths_stroke_width=2, 
    paths_dotted=True,
    title="paths", default=shp)
# ---- TEXT for customised shapes
cstxt = Default(stroke="black", font_size=18, x=15, align="left")
Text("hatches", y=2, default=cstxt)
Text("radii", y=6, default=cstxt)
Text("radii_shapes", y=10, default=cstxt)
Text("slices", y=14, default=cstxt)
Text("Shapes with properties", common=header)
PageBreak()


# ---- Shapes with properties
big = Default(stroke="black", font_size=32, x=9, align="left")
Text('"Gold Coin"', default=big, y=4)
Circle(
    cx=5, cy=22, radius=2,
    fill="#63B1BB", stroke="#63B1BB",
    radii=[135,225],
    radii_offset=1, radii_length=2,
    radii_stroke="white", radii_stroke_width=30,
    centre_shape=circle(radius=1.5, fill="#63B1BB", stroke="#63B1BB"),
    radii_shapes=[(45, dot(stroke="white", dot_width=10), 0.75)],
    order_last=["radii_shapes"]
)
Text('"Red Pawn"', default=big, y=10)
Circle(
    cx=5, cy=4, radius=2,
    fill="gold", stroke_width=2, 
    radii=steps(0,360,15),
    centre_shape=circle(
        radius=1.5,
        fill="gold", label="5", font_size=48)
)
Text('"German Cross"', default=big, y=16)
Triangle(
    cx=5, cy=11, side=4,
    fill_stroke="red",
    radii_shapes=[('n', circle(fill_stroke="red", radius=1))],
)
Text('"XOK Fish"', default=big, y=22)
Rectangle(
    height=4.2, width=4.2, x=3, y=14,
    fill="white", stroke="black", stroke_width=3,
    hatches_stroke_width=33, hatches_stroke="black",
    hatches='o', hatches_count=1,
    notch=1, notch_style='step',
    centre_shape=rectangle(
        height=4.2, width=4.2, 
        fill=None, stroke="white", stroke_width=4.5)
)
Text('Shapes => "Things"', common=header)
PageBreak()


# ---- Lines & arrowheads
ctxt = Default(x=5, font_size=20, align="left")
Text(text="Line: arrow styles", default=ctxt, y=2)
arr1 = Default(arrow_width=0.2, arrow_height=0.3, stroke_width=0.8, x=0, x1=3)
Line(y=1, y1=1, arrow=True, default=arr1)
Line(y=1.5, y1=1.5, arrow_style='notch', default=arr1)
Line(y=2, y1=2, arrow_style='angle', default=arr1)
Line(y=2.5, y1=2.5, arrow_style='spear', default=arr1)
Text(text="Line: arrow positions", default=ctxt, y=4)
Line(y=3, y1=3,
     dotted=True,
     arrow_position=0.6,
     arrow_double=True,
     default=arr1)
Line(y=3.5, y1=3.5, 
     arrow_position=[0.25, 0.5, 0.75], 
     default=arr1)
Line(y=4, y1=4, 
     arrow_position=[1.0, 0.93], 
     default=arr1)
Line(y=4.5, y1=4.5,
     arrow_style='spear',
     arrow_height=0.15, 
     default=arr1)
Line(y=4.5, y1=4.5,
     arrow_style='angle',
     arrow_width=0.15,
     arrow_position=[0.1, 0.15, 0.2], 
     default=arr1)
# ---- polylines
Text(text="Polylines: sawtooth style", default=ctxt, y=6)
Polyline(
    points='0,5 1,6 2,5 3,6',
    stroke="red", stroke_width=2,
    wave_style="sawtooth", 
    wave_height=0.03,)
Text(text="Polylines: wave style", default=ctxt, y=7)
Polyline(
    points='0,6 1,7 2,6 3,7',
    stroke="purple", stroke_width=2,
    wave_style="wave", 
    wave_height=0.05,)
Text(text="Polylines: dotted + arrows", default=ctxt, y=8)
Polyline(
    points='0,7 1,8 2,7 3,8',
    stroke_width=3,
    dotted=True,
    arrow_style='notch',
    arrow_double=True
)
# ---- line: connections
Text("Line: connections", default=ctxt, y=16, x=0)
cc = Circle(cx=2, cy=12, radius=0.5)
cy = Circle(cx=1, cy=10, radius=0.5, fill_stroke="gold")
Line(connections=[cc, cy], stroke_width=4, stroke="lime")
ca = Circle(cx=1, cy=14, radius=0.5, fill_stroke="aqua")
Line(connections=[cc, ca], stroke_width=6, dashed=[0.2, 0.1])
cr = Circle(cx=3, cy=10, radius=0.5, fill_stroke="tomato")
Line(connections=[cc, cr], stroke_width=2, wave_style='sawtooth', wave_height=0.06)
co = Circle(cx=3, cy=14, radius=0.5, fill_stroke="orange")
Line(connections=[cc, co], stroke_width=4, stroke="lime")
Line(connections=[cy, cr, co, ca, cy], stroke_width=2)
# ---- line: connections - arrow
Text("...connections: arrow", default=ctxt, y=16, x=6)
cc = Circle(cx=8.5, cy=12.5, radius=0.5)
cy = Circle(cx=8, cy=10, radius=0.5, fill_stroke="gold")
co = Circle(cx=10, cy=14, radius=0.5, fill_stroke="orange")
Line(connections=[cy, cc, co],
     stroke="red",
     stroke_width=1.5,
     arrow=True,
     default=arr1
     )
# ---- line: connections - dot&spoke
Text("... dot&spoke", default=ctxt, y=16, x=14)
cc = Dot(cx=14.5, cy=12.5, dot_width=10, stroke="aqua")
cr = Circle(cx=16, cy=10, radius=0.5, fill_stroke="red")
co = Circle(cx=16, cy=14, radius=0.5, fill_stroke="orange")
ca = Circle(cx=14, cy=14, radius=0.5, fill_stroke="gold")
Line(connections=[cc, cr, co, ca],
     connections_style='spoke',
     stroke="green",
     stroke_width=1.5,
     # arrow=True,
     arrow_double=True,
     default=arr1
     )
# ---- polyline - snail
Text("Polyline: snail", default=ctxt, y=26, x=2)
Polyline(
    x=2, y=18,
    snail="s 0.4 j0.1 "*12,
    stroke_width=4,
    stroke="orange")
Polyline(
    x=6, y=18,
    snail="e 2 s 2 w 2 n 2 s j2 "*3,
    stroke_width=2,
    stroke="blue")

snail_line = "n 6 e 4 -45 4 w 2 sw 6 **"
Polyline(
    x=12, y=23,
    snail=snail_line,
    stroke_width=2,
)
Text("Polyline: snail + scaled", default=ctxt, y=26, x=11)
Polyline(
    x=12, y=23,
    snail=snail_line,
    stroke_width=2,
    scaling=0.5
)
Text("Lines and Polylines", common=header)
PageBreak()


# ---- polyshapes
Text(text="Polyshape- wave style line", default=ctxt, y=3)
Polyshape(
    points=[(0, 5), (0, 2), (2, 1), (4, 2), (4, 5)],
    wave_style="wave", wave_height=0.06,
    stroke_width=1,
    fill="gold")
Text(text="Polyshape - snail (rotation)", default=ctxt, y=8)
Polyshape(
    x=0, y=8,
    snail="4 r160 "*9,
    stroke_width=1,
    #scaling=0.25,
    stroke="red",
    fill="yellow")
Text(text="Polyshapes - snail (scaling)", default=ctxt, y=13)
psh = Default(
    snail='w 1 s 1 e 5 n 1 w 1 s 3 w 3 n 1',
    stroke="sandybrown",
    fill="seagreen",)
Polyshape(
    x=0, y=12,
    default=psh,
    stroke_width=4)
Polyshape(
    x=1.25, y=13.5,
    default=psh,
    scaling=0.25,
    stroke_width=3)
Text("Polyshapes", common=header)
PageBreak()


# ---- assorted objects
Text("StarField (with Polyon)", default=ctxt, y=1)
Polygon(x=2.5, y=1.4, sides=10, radius=1.5, fill="black")
StarField(
    enclosure=polygon(x=2.5, y=1.4, sides=10, radius=1.5),
    density=40,
    colors=["white", "white", "white", "red", "green", "blue", ],
    sizes=[0.3, 0.3, 0.3, 0.35, 0.5, 0.6, 0.65],
    seeding=42.3)
Text("Cube / shades", default=ctxt, y=5)
Cube(
    x=1, y=3.5, height=3,
    shades=["#FFDC17", "#957F0A", "#CCB412"],
    radii_stroke="dimgray",
    radii_stroke_width=1)
Text("D6 [die] / shades", default=ctxt, y=9)
D6(
    x=1, y=7.5, side=2, 
    roll=5, 
    pip_fill="gold", 
    pip_stroke="orange",
    fill="red", 
    rounding=0.2)
D6(
    x=3, y=9.5, side=1.75, 
    roll=4, 
    pip_fill="white",
    pip_shape="diamond",
    pip_stroke="aqua",
    fill="blue", 
    pip_fraction=0.15)
Text("QR Code", default=ctxt, y=13)
QRCode(
    'qrcode2.png',
    text="https://protograf.readthedocs.io/en/latest/",
    x=1, y=12,
    height=2.5, width=2.5,
    fill="gray",
    stroke="red",
    scaling=5,
)
Text("Tetronimo", default=ctxt, y=16)
Tetromino(
    x=0, y=15, side=1.5, 
    letter="T", 
    outline_width=1)
Text("Polyonimo", default=ctxt, y=20)
Polyomino(
    x=0, y=19, side=1.5,
    pattern=['101', '010'],
    fill_stroke="silver",
    outline_stroke='red', outline_width=2)
Text("Pentonimo", default=ctxt, y=25)
Pentomino(
    x=0, y=23, side=1.5,
    letter="F", 
    flip="south", 
    stroke=None,
    fill="gold",
    outline_stroke="black", 
    outline_width=1)
Text("Specialised Shapes", common=header)
PageBreak()

# ---- text
Blueprint()
Text("Plain, default, text")
Text("Default Text()", default=ctxt, y=1)
basic = Common(
    wrap=True,
    x=0,
    width=5, height=2.5,
    font_size=14,
    align="left")
Text(common=basic,
     y=1.5,
     fill="white",
     outlined=True,
     text="Outlined; white fill")
Text(common=basic,
     y=2.5,
     fill=None,
     outlined=True,
     text_stroke_width=0.1,
     text="Outlined; no fill; text_stroke_width=.1")
Text(common=basic,
     y=4,
     fill="yellow",
     outlined=True,
     text_stroke_width=0.02,
     text="Outlined; yellow fill; text_stroke_width=.02")
Text("Outlined Text()", default=ctxt, y=3)

Text(x=2.5, y=6.5, text="Line text 1,1 - rotate 20", font_size=14, rotation=20)
Text("Rotated Text()", default=ctxt, y=6.5)
Text(font_size=14, x=0, y=8, width=5, height=2, wrap=True,
     text="Wrap textbox - 5-by-2 - rotate 90", rotation=90)
Text("Rotated textbox", default=ctxt, y=9)

Text(wrap=True,
     x=0, y=11, width=4.8, height=3,
     font_size=16,  fill="black", stroke="black",
     font_name="Times-Roman", align="right",
     transform='title',
     text="Times-Roman 16pt in title case to the right")
Text("Wrap textbox: transformed & aligned text", default=ctxt, y=12)

Text(x=0, y=14, width=4.8, height=2.5,
     box_stroke="red", box_fill="yellow",
     box_dotted=True, box_transparency=50,
     style="font-family: Courier; font-size: 16pt; color: blue;",
     text='HTML/CSS; Courier 16pt; blue<br/>')
Text("HTML textbox with its box styled", default=ctxt, y=15)

Text(x=0, y=17, width=4.8, height=1.5, wrap=True,
     align="right", stroke="lime", font_size=18,
     font_name="Eagle Lake", box_fill="lightcyan",
     text="Eagle Lake")
Text("Wrap textbox with custom font", default=ctxt, y=18)

IconFont("Arial")
Text(x=0.5, y=20, width=4, height=2,
     html=True,
     # box_fill="white",
     box_fill="silver",
     text="""
     <div style="
         font-family: Quintessential;
         font-size:16.0px;
         color:blue;
         text-align:center;">
     Return 2 |:openmoji--fish 14:| and get 3 |!\u2666!|
     </div>"""
 )
Text("HTML textbox; custom font; inline icons", default=ctxt, y=21)

IconFont("game-icons-net-20200315a")
Text(x=0.5, y=22.5, width=4, height=2,
     html=True,
     box_fill="silver",
     text="""
     <div style="
         font-family: Quintessential;
         font-size:16.0px;
         color:blue;
         text-align:center;">
     Recyle 2 |;openmoji--fish 16;| and get 4 |!\uEB73 16 green!|
     </div>"""
 )
Text("HTML textbox; custom font; inline icons", default=ctxt, y=23)
Text("(icons via SVG & built-font symbols)", default=ctxt, y=24)

Text(common=header, text='Text: Font & Styling')
PageBreak()

# ---- grid: graph paper
Grid(cols=95, rows=135, size=0.2, stroke="mediumseagreen", stroke_width=0.9)
Grid(cols=19, rows=27, size=1.0, stroke="mediumseagreen", stroke_width=1.5)
Text(common=header, text='"Graph Paper" -> Grid (95x135) + Grid (19x27)')
PageBreak()


# ---- hexagons ~2cm grid - numbered "wargame" style
Hexagons(
    rows=11,
    cols=9,
    side=1.69,
    margin_left=-1.8,
    margin_top=-1.529,
    dot=0.05,
    dot_stroke="black",
    coord_elevation="top",
    coord_font_size=12,
    coord_stroke="darkslategray",
    fill="white",
    stroke="darkslategray",
    caltrops=0.5,
)
Text("Hexagons (dot; coords; caltrops)", common=header)
PageBreak()


# ---- Go board
Grid(
    cols=18, rows=18,
    stroke_width=1
)
DotGrid(
    offset_x=4, offset_y=4,
    side=6,
    cols=3, rows=3,
    dot_width=8
)
Text("""Grid(
  cols=18, rows=18,
  stroke_width=1
)""", default=txt, x=0, y=20)
Text("""DotGrid(
  cols=3, rows=3,
  offset_x=4, offset_y=4,
  side=6,
  dot_width=8
)""", default=txt, x=9, y=20)
Text("Go board", common=header)
PageBreak()

# ---- Dejarik board
Circle(
    cx=10.5, cy=9,
    radius=8,
    stroke_width=16,
    slices=["black", "silver"]*6,
    centre_shapes=[
        circle(radius=5.2, stroke_width=12, slices=["#E0DFDD", "black"]*6, rotation=15),
        circle(radius=1.8, stroke_width=8, fill="silver") 
    ],
    rotation=15
)
Text("""Circle(
  cx=10.5, cy=14, 
  radius=10, stroke_width=20,
  slices=["black", "silver"]*6,
  centre_shapes=[
    circle(radius=6.5, stroke_width=15, 
           slices=["#E0DFDD", "black"]*6, 
           rotation=15),
    circle(radius=2.5, stroke_width=10, 
           fill="silver")],
  rotation=15)""", default=txt, x=0, y=18)
Text("Dejarik board", common=header)
    
Save()
