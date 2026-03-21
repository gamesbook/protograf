"""
Show customised Lines - and useful overides - for protograf

Written by: Derek Hohls
Created on: 19 March 2026
"""

from protograf import *

Create(filename="customised_line.pdf",
       paper="A8",
       margin_left=0.5,
       margin_right=0.3,
       margin_bottom=0.2,
       margin_top=0.5,
       font_size=8,
       stroke_width=0.5,
       # cached_fonts=False,  # force reindex of all fonts
       )

txt = Common(x=0, y=0, font_size=8, align="left")

Text(common=txt, text="Line START...")
Text(x=0, y=6, font_size=8, align="left", text=Today())
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

# ---- line - custom - curve
Blueprint()
Text(common=txt, text='Line: locations; styles; curve')
Line(x=0, y=0.5, stroke_width=0.2, dotted=True, label="0.2", font_size=6, curve=0.25)
Line(x=1, y=0.5, stroke_width=0.4, dotted=True, label="0.4", font_size=6, curve=0.25)
Line(x=2, y=0.5, stroke_width=0.8, dotted=True, label="0.8", font_size=6, curve=0.25)
Line(x=3, y=0.5, stroke_width=1.6, dotted=True, label="1.6", font_size=6, curve=0.25)

Line(x=1, y=1, length=2, stroke="chartreuse", stroke_width=10, curve=0.25)
Line(x=1, y=1.5, length=2, stroke="aqua", stroke_width=10, stroke_ends="rounded", curve=0.25)
Line(x=1, y=2, length=2, stroke="gold", stroke_width=10, stroke_ends="squared", curve=0.25)
Line(x=0, y=2.5, length=4, stroke="pink", stroke_width=2, curve=0.25)

Line(x=0, y=3.6, length=4.1, angle=15, stroke="red", label="15", font_size=6, curve=0.5)
Line(x=0, y=3.6, length=4.1, angle=-15, stroke="red", label="-15", font_size=6, curve=-0.5)


Line(x=0, y=5, x1=4, y1=5.9, stroke="blue", stroke_width=1,
     dashed=[0.2, 0.1], label="dashed:[0.2,0.1]", font_size=6, curve=0.25)

PageBreak()

# ---- center line from angle
Blueprint(stroke_width=0.5)
Text(common=txt, text="Line: angle")

Line(cx=1, cy=1, angle=45, length=2, stroke="red", arrow_style="circle")
Line(cx=3, cy=1, angle=225, length=2, stroke_width=1.5,
     arrow_style="circle", arrow_width=0.2)

Circle(cx=2, cy=3, radius=1)
Line(cx=2, cy=3, angle=45, length=2, stroke="red", arrow_width=0.2)
Line(cx=2, cy=3, angle=135, length=2, stroke_width=1.5, arrow_width=0.2)

Line(cx=1, cy=5, angle=135, length=2, stroke_width=1.5,
     arrow_style="circle", arrow_width=0.2)
Line(cx=3, cy=5, angle=315, length=2, stroke="red", arrow_style="circle")
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
Line(connections=[cy, cr, co, ca, cy],
     stroke_width=2, stroke="green", curve=0.5)
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
Line(
    connections=[(s1, 'p', 'e'), (s2, 'v', 'se')],
    stroke="blue",
    stroke_width=2,
    curve=-0.5)
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

# ---- line - connections - curved
Blueprint(stroke_width=0.5)
Text(common=txt, text="Line: connections; curve")
cc = Dot(cx=1.5, cy=3.5, dot_width=2)
cr = Circle(cx=3, cy=1, radius=0.5, fill_stroke="red")
co = Circle(cx=3, cy=5, radius=0.5, fill_stroke="orange")
ca = Circle(cx=1, cy=5, radius=0.5, fill_stroke="aqua")
Line(connections=[cc, cr, co, ca],
     connections_style='spoke',
     stroke="green",
     stroke_width=1,
     arrow=True,
     curve=0.5,
     )
PageBreak()

# ---- line - centred shapes
Blueprint(stroke_width=0.5)
Text(common=txt, text='Line: centred shapes')
crc = circle(radius=0.15)
ttt = text("Aa", font_size=10)
crs = cross(height=0.6, width=0.6)
ell = ellipse(height=0.4, width=0.6)
ply = polygon(side=0.2, sides=5)
rho = rhombus(side=0.3)

Line(x=0, y=0.5, length=1.5,
     centre_shapes=[crc])
Line(x=2, y=0.5, length=1.5,
     centre_shapes=[ttt])
Line(x=0, y=1.5, length=1.5,
     centre_shapes=[crs])
Line(x=2, y=1.5, length=1.5,
     centre_shapes=[ply])
Line(x=0, y=2.5, length=1.5,
     centre_shapes=[ell])
Line(x=2, y=2.5, length=1.5,
     centre_shapes=[rho])

Line(x=0, y=4, length=2,
     angle=30,
     centre_shapes=[crc],
     centre_shapes_rotated =True)
Line(x=2, y=4, length=2,
     angle=30,
     centre_shapes=[ttt],
     centre_shapes_rotated =True)
Line(x=0, y=5, length=2,
     angle=30,
     centre_shapes=[crs],
     centre_shapes_rotated =True)
Line(x=2, y=5, length=2, angle=30,
     centre_shapes=[ply],
     centre_shapes_rotated =True)
Line(x=0, y=6, length=2, angle=30,
     centre_shapes=[ell],
     centre_shapes_rotated =True)
Line(x=2, y=6, length=2,
     angle=30,
     centre_shapes=[rho],
     centre_shapes_rotated =True)
PageBreak()

# ---- line - centred shapes - curve
Blueprint(stroke_width=0.5)
Text(common=txt, text='Line: centred shapes on curve')
crc = circle(radius=0.15)
ttt = text("Aa", font_size=10)
crs = cross(height=0.6, width=0.6)
ell = ellipse(height=0.4, width=0.6)
ply = polygon(side=0.2, sides=5)
rho = rhombus(side=0.3)

shrt = Common(length=1.51, curve=0.25)
Line(x=0, y=0.5, common=shrt,
     centre_shapes=[crc])
Line(x=2, y=0.5, common=shrt,
     centre_shapes=[ttt])
Line(x=0, y=1.5, common=shrt,
     centre_shapes=[crs])
Line(x=2, y=1.5, common=shrt,
     centre_shapes=[ply])
Line(x=0, y=2.5, common=shrt,
     centre_shapes=[ell])
Line(x=2, y=2.5, common=shrt,
     centre_shapes=[rho])

lng = Common(length=2, curve=0.25)
Line(x=0, y=4, common=lng,
     angle=30,
     centre_shapes=[crc],
     centre_shapes_rotated =True)
Line(x=2, y=4, common=lng,
     angle=30,
     centre_shapes=[ttt],
     centre_shapes_rotated =True)
Line(x=0, y=5, common=lng,
     angle=30,
     centre_shapes=[crs],
     centre_shapes_rotated =True)
Line(x=2, y=5, common=lng, angle=30,
     centre_shapes=[ply],
     centre_shapes_rotated =True)
Line(x=0, y=6, common=lng, angle=30,
     centre_shapes=[ell],
     centre_shapes_rotated =True)
Line(x=2, y=6, common=lng,
     angle=30,
     centre_shapes=[rho],
     centre_shapes_rotated =True)
PageBreak()


# ---- line - curves
Blueprint(stroke_width=0.5)
Text(common=txt, text='Line: curves')

tl = Common(x=1, y=1, length=1, curve=0.5)
Line(common=tl, angle=60)
Line(common=tl, angle=120)
Line(common=tl, angle=180)
Line(common=tl, angle=240)
Line(common=tl, angle=300)
Line(common=tl, angle=360)

tr = Common(x=3, y=1, length=1, curve=-0.5, stroke="red")
Line(common=tr, angle=60)
Line(common=tr, angle=120)
Line(common=tr, angle=180)
Line(common=tr, angle=240)
Line(common=tr, angle=300)
Line(common=tr, angle=360)

Line(x=0.5, y=4, length=1, curve=1.5)
Line(x=2.5, y=2.5, length=1, curve=-1.5)

Line(x=2, y=5.5, length=1, angle=90, curve=1.5)
Line(x=2.5, y=5.5, length=1, angle=90, curve=-1.5)

PageBreak()


# ---- END
Text(common=txt, text="Line END...")

Save(
     output='png',
     dpi=300,
     directory="../docs/source/images/customised",
     names=[
        None,
        "line_custom",
        "line_custom_curve",
        "line_centred",
        "line_connections_circle",
        "line_connections_shapes",
        "line_connections_arrow",
        "line_connections_spoke",
        "line_connections_curve",
        "line_centre_shapes",
        "line_centre_shapes_curve",
        "line_curves",
        None])
