# -*- coding: utf-8 -*-
"""
Show default shapes - and useful overrides - for protograf

Written by: Derek Hohls
Created on: 20 March 2024
"""

from protograf import *

Create(filename="default_shapes.pdf",
       paper="A8",
       margin=0.75,
       margin_right=0.2, margin_top=0.2,
       font_size=8,
       stroke_width=0.5)

header = Common(x=0, y=6, font_size=8, align="left")

Blueprint(stroke_width=0.5)
Text(common=header, text="Blueprint")
PageBreak()

Blueprint(subdivisions=5, stroke_width=0.8)
Text(common=header, text="Blueprint: subdivisions=5")
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Text")
Text(text="Hello World")
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Line")
Line()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rectangle")
Rectangle()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Circle")
Circle()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Hexagon")
Hexagon()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Hexagon: pointy")
Hexagon(orientation="pointy")
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Rhombus")
Rhombus()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Trapezoid")
Trapezoid()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Star")
Star()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Ellipse")
Ellipse()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Polygon")
Polygon()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Arrow")
Arrow()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="RightAngledTriangle")
RightAngledTriangle()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="EquilateralTriangle")
EquilateralTriangle()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Compass")
Compass()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Hexagons: rows=2, cols=2")
Hexagons(rows=2, cols=2, margin_bottom=0, margin_left=0)
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Grid")
Grid()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Arc")
Arc()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Bezier")
Bezier()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Polyline")
# Polyline() # will get FEEDBACK
Polyline(points=[(0, 0), (1, 1), (2, 0)])
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Polyshape")
Polyshape(points="0,0 1,1 2,0")
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Sector")
Sector()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Sequence")
Sequence(text())
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Square")
Square()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text='Stadium ("pill")')
Stadium()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="StarField")
Rectangle(x=0, y=0, fill=black)
StarField(seed=42.3)
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Dot")
Dot()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="DotGrid")
DotGrid()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Fill & Stroke")
Rectangle(fill=yellow, stroke=red, stroke_width=6)
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Transparency")
Rectangle(x=1, y=3, height=1, width=2, fill="#008000", stroke=silver, transparency=25, label="25%")
Rectangle(x=1, y=4, height=1, width=2, fill="#008000", stroke=silver, transparency=50, label="50%")
Rectangle(x=1, y=5, height=1, width=2, fill="#008000", stroke=silver, transparency=75, label="75%")
Rectangle(x=0, y=0, height=2, width=2, fill=yellow, stroke=yellow)
Rectangle(x=1, y=1, height=2, width=2, fill=red, stroke=red, transparency=50)
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Track: Rectangle: SW~clockwise")
Track()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Chord: 135 to 45 degrees")
Chord(shape=Circle(), angle=135, angle1=45)
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text='RectangularLocations: "invisible"')
Layout(RectangularLocations())
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text='RectangularLocations: "debug"')
Layout(RectangularLocations(), debug='normal')
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text='Lines')
Lines()
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Match Fill and Stroke")
Circle(fill_stroke=aqua)
PageBreak()

Save(output='png',
     dpi=300,
     directory="../docs/source/images/defaults",
     names=[
        'blueprint', 'blueprint-sub', 'text', 'line', 'rectangle',
        'circle', 'hexagon-flat', 'hexagon-pointy', 'rhombus',
        'trapezoid', 'star', 'ellipse', 'polygon',  'arrow',
        'rightangle',  'equiangle', 'compass',  'hexagons-2x2',
        'grid', 'arc', 'bezier', 'polyline',
        'shape', 'sector', 'sequence', 'square',
        'stadium', 'starfield', 'dot', 'dotgrid', 'fill-stroke',
        'transparency', 'track-rectangle', 'chord',
        'rectangular_layout', 'rectangular_layout_debug', 'lines',
        'fill-and-stroke'
     ])
