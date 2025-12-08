# -*- coding: utf-8 -*-
"""
An overview of protograf capabilities

Written by: Derek Hohls
Created on: 29 November 2025
Notes:
    Chess font from: http://www.enpassant.dk/chess/fontimg/alpha.htm
"""
from protograf import *

Create(
   filename="overview.pdf", margin=1, page_grid=2)

# ---- default & common
lbl = Default(x=5, font_size=19, align="left")
txt = Default(x=5, font_size=19, align="left", font_name="Courier")
header = Common(x=0, y=28, font_size=24, align="left")

# ---- title
Image("protograf_slogan.png", x=3.5, y=8, height=3.6, width=12)
Text('A Brief Tour...', font_size=48, stroke="#3286AD", x=9.5, y=15)
PageBreak()

# ---- simple
Rectangle()
Text('... a rectangle!', default=lbl)
PageBreak()

# ---- base
Rectangle()
Text('What does the script look like?', default=lbl, y=6, x=1)
Text("""from protograf import *

Create(
 filename='overview.pdf',
 margin=1, page_grid=2)
Rectangle()
Save()""",
  box=True,
  font_name="Courier",
  font_size=24,
  align="left",
  x=1, y=8,
  height=15,
  width=15)
PageBreak()

# ---- styled
Rectangle(width=3, height=4)
Text('Rectangle(\n width=3, height=4)', default=txt, y=1)
Rectangle(y=6, width=3, height=4, fill="yellow", stroke="red", stroke_width=4)
Text('Rectangle(\n y=6, \n width=3, height=4,\n fill="yellow", stroke="red",\n stroke_width=4)', default=txt, y=6)
Rectangle(y=11, width=3, height=4, label="Hi!", label_size=18)
Text('Rectangle(\n y=11, \n width=3, height=4,\n label="Hi!,\n label_size=18")', default=txt, y=11)
Rectangle(y=16, width=3, height=4, hatches_count=5)
Text('Rectangle(\n y=16, \n width=3, height=4,\n hatches_count=5)', default=txt, y=16)
Rectangle(
    y=21, width=3, height=4,
    notch_style='bite', notch=0.5,
    radii_shapes=[('*', dot())])
Text('Rectangle(\n y=21, \n width=3, height=4,\n notch_style="bite",\n notch=0.5, \n radii_shapes=[("*", dot())]', default=txt, y=21)
PageBreak()

# ---- filled shapes
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
Dot(cx=9, cy=0, dot_width=12, title="Dot", default=shp, fill_stroke="red")
PageBreak()

# ---- shape properties
# Blueprint()
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
ctxt = Default(stroke="black", font_size=18, x=15, align="left")
Text("hatches", y=2, default=ctxt)
Text("radii", y=6, default=ctxt)
Text("radii_shapes", y=10, default=ctxt)
Text("slices", y=14, default=ctxt)
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
PageBreak()

# ---- assorted objects
ctxt = Default(stroke="black", font_size=20, x=5, align="left")
Text("StarField (with Polyon)", default=ctxt, y=1)
Polygon(x=2.5, y=1.4, sides=10, radius=1.5, fill="black")
StarField(
    enclosure=polygon(x=2.5, y=1.4, sides=10, radius=1.5),
    density=40,
    colors=["white", "white", "white", "red", "green", "blue", ],
    sizes=[0.3, 0.3, 0.3, 0.35, 0.5, 0.6, 0.65],
    seeding=42.3)
Text("Cube / shades", default=ctxt, y=6)
Cube(
    x=1, y=4.5, height=3,
    shades=["#FFDC17", "#957F0A", "#CCB412"],
    radii_stroke="dimgray",
    radii_stroke_width=1)
Text("D6 [die] / shades", default=ctxt, y=11)
D6(
    x=1, y=9, side=2, 
    roll=5, 
    pip_fill="gold", 
    pip_stroke="orange",
    fill="red", 
    rounding=0.2)
D6(
    x=3, y=11, side=1.75, 
    roll=4, 
    pip_fill="white",
    pip_shape="diamond",
    pip_stroke="aqua",
    fill="blue", 
    pip_fraction=0.15)
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
PageBreak()

# ---- lines and polyshapes & polylines
Text(common=header, text="Polyshapes, Polylines and lines")
Line(x=0, y=2, x1=19, y1=2, stroke="black", stroke_width=2)
Polyline(
    points='1,3 1,4 2,4 4,3',
    stroke="red", stroke_width=2,
    wave_style="sawtooth", wave_height=0.03,)
Polyline(
    points='1,5 1,6 2,6 4,5',
    stroke="purple", stroke_width=2,
    wave_style="wave", wave_height=0.05,)
Polyline(
    points=[(0, 13), (2, 15), (4, 13), (6, 15), (8, 13), (10, 15), (12, 13)],
    stroke="gray")
Line(x=1, y=20, length=25.5, angle=45, stroke="tomato", stroke_width=3)  # thick diagonal
PageBreak()

# ---- grid: graph paper
Text(common=header, text='"Graph Paper" -> Grid (95x135) and Grid (19x27)')
Grid(cols=95, rows=135, size=0.2, stroke="mediumseagreen", stroke_width=0.9)
Grid(cols=19, rows=27, size=1.0, stroke="mediumseagreen", stroke_width=1.5)
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
Text(common=header, text="Hexagons (dot; coords; caltrops)")
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
PageBreak()


    
Save()
