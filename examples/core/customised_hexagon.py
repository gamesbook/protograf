"""
Show customised Hexagon for protograf

Written by: Derek Hohls
Created on: 19 September 2024
"""

from protograf import *

Create(filename="customised_hexagon.pdf",
       paper="A8",
       margin_left=0.5,
       margin_right=0.3,
       margin_bottom=0.2,
       margin_top=0.5,
       font_size=8,
       stroke_width=0.5)

txt = Common(x=0, y=0, font_size=8, align="left")

Text(common=txt, text="Hexagon START...")
PageBreak()

# ---- centre placement
Blueprint()
Text(common=txt, text="Hexagon: cx & cy")
Hexagon(cx=2, cy=1)
Hexagon(cx=2, cy=3, orientation='pointy')
PageBreak()

# ---- dot & cross
Blueprint()
Text(common=txt, text="Hexagon: dot & cross")
Hexagon(x=-0.25, y=4, height=2,
        dot=0.1, dot_stroke="red")
Hexagon(x=1.75, y=3.5, height=2,
        cross=0.25, cross_stroke="red", cross_stroke_width=1)
Hexagon(x=0, y=1, height=2,
        dot=0.1, dot_stroke="red",
        orientation='pointy')
Hexagon(x=2, y=1, height=2,
        cross=0.25, cross_stroke="red", cross_stroke_width=1,
        orientation='pointy')
PageBreak()

# ---- hatches - flat
Blueprint()
Text(common=txt, text="Hexagon: flat; hatches")
hxgn = Common(x=1, height=1.5, hatch_count=5, hatch_stroke="red", orientation='flat')
Hexagon(common=hxgn, y=0, hatch='e', label="e/w")
Hexagon(common=hxgn, y=2, hatch='ne', label="ne/sw")
Hexagon(common=hxgn, y=4, hatch='nw', label="nw/se")
PageBreak()

# ---- hatches - pointy
Blueprint()
Text(common=txt, text="Hexagon: pointy; hatches")
hxgn = Common(x=1, height=1.5, hatch_count=5, hatch_stroke="red", orientation='pointy')
Hexagon(common=hxgn, y=0, hatch='n', label="n/s")
Hexagon(common=hxgn, y=2, hatch='ne', label="ne/sw")
Hexagon(common=hxgn, y=4, hatch='nw', label="nw/se")
PageBreak()

# ---- text - flat
Blueprint()
Text(common=txt, text="Hexagon: flat; text")
Hexagon(
    y=2,
    height=2,
    title="Title",
    label="Label",
    heading="Heading")
PageBreak()

# ---- text - pointy
Blueprint()
Text(common=txt, text="Hexagon: pointy; text")
Hexagon(
    y=2,
    height=2,
    orientation='pointy',
    title="Title",
    label="Label",
    heading="Heading")
PageBreak()

# ---- radii - flat
Blueprint(stroke_width=0.5)
Text(common=txt, text="Hexagon: flat; radii")
hxg = Common(height=1.5, dot=0.05, dot_stroke="red", orientation="flat", font_size=8)
Hexagon(common=hxg, x=0.25, y=0.25, radii='sw', label="SW")
Hexagon(common=hxg, x=0.25, y=2.15, radii='w', label="W")
Hexagon(common=hxg, x=0.25, y=4, radii='nw', label="NW")
Hexagon(common=hxg, x=2.25, y=4, radii='ne', label="NE")
Hexagon(common=hxg, x=2.25, y=2.15, radii='e', label="E")
Hexagon(common=hxg, x=2.25, y=0.25, radii='se', label="SE")
PageBreak()

# ---- radii - pointy
Blueprint(stroke_width=0.5)
Text(common=txt, text="Hexagon: pointy; radii")
hxg = Common(height=1.5, dot=0.05, dot_stroke="red", orientation="pointy", font_size=8)
Hexagon(common=hxg, x=0.25, y=0.25, radii='sw', label="SW")
Hexagon(common=hxg, x=0.25, y=2.15, radii='nw', label="NW")
Hexagon(common=hxg, x=0.25, y=4, radii='n', label="N")
Hexagon(common=hxg, x=2.25, y=4, radii='ne', label="NE")
Hexagon(common=hxg, x=2.25, y=0.25, radii='s', label="S")
Hexagon(common=hxg, x=2.25, y=2.15, radii='se', label="SE")
PageBreak()

# ---- borders - flat
Blueprint(stroke_width=0.5)
Text(common=txt, text="Hexagon: flat; borders")
hxg = Common(height=1.5, orientation="flat", font_size=8)
Hexagon(common=hxg, x=0.25, y=0.25, borders=('sw', 2, "gold"), label="SW")
Hexagon(common=hxg, x=0.25, y=2.15, borders=('nw', 2, "gold"), label="NW")
Hexagon(common=hxg, x=0.25, y=4.00, borders=('n', 2, "gold"), label="N")
Hexagon(common=hxg, x=2.25, y=4.00, borders=('s', 2, "gold"), label="S")
Hexagon(common=hxg, x=2.25, y=0.25, borders=('ne', 2, "gold"), label="NE")
Hexagon(common=hxg, x=2.25, y=2.15, borders=('se', 2, "gold"), label="SE")
PageBreak()

# ---- borders - pointy
Blueprint(stroke_width=0.5)
Text(common=txt, text="Hexagon: pointy; borders")
hxg = Common(height=1.5, orientation="pointy", font_size=8)
Hexagon(common=hxg, x=0.25, y=0.25, borders=('sw', 2, "gold"), label="SW")
Hexagon(common=hxg, x=0.25, y=2.15, borders=('nw', 2, "gold"), label="NW")
Hexagon(common=hxg, x=0.25, y=4.00, borders=('w', 2, "gold"), label="W")
Hexagon(common=hxg, x=2.25, y=4.00, borders=('e', 2, "gold"), label="E")
Hexagon(common=hxg, x=2.25, y=0.25, borders=('ne', 2, "gold"), label="NE")
Hexagon(common=hxg, x=2.25, y=2.15, borders=('se', 2, "gold"), label="SE")
PageBreak()

# ---- perbis - flat
Blueprint(stroke_width=0.5)
Text(common=txt, text="Hex Flat: perbis")
hxg = Common(height=1.5, dot=0.05, dot_stroke="red", orientation="flat", font_size=8)
Hexagon(common=hxg, x=0.25, y=0.25, perbis='sw', label="SW")
Hexagon(common=hxg, x=0.25, y=2.15, perbis='nw', label="NW")
Hexagon(common=hxg, x=0.25, y=4, perbis='n', label="N")
Hexagon(common=hxg, x=2.25, y=4, perbis='ne', label="NE")
Hexagon(common=hxg, x=2.25, y=0.25, perbis='s', label="S")
Hexagon(common=hxg, x=2.25, y=2.15, perbis='se', label="SE")
PageBreak()

# ---- perbis - pointy
Blueprint(stroke_width=0.5)
Text(common=txt, text="Hex Pointy: perbis")
hxg = Common(height=1.5, dot=0.05, dot_stroke="red", orientation="pointy", font_size=8)
Hexagon(common=hxg, x=0.25, y=0.25, perbis='sw', label="SW")
Hexagon(common=hxg, x=0.25, y=2.15, perbis='w', label="W")
Hexagon(common=hxg, x=0.25, y=4, perbis='nw', label="NW")
Hexagon(common=hxg, x=2.25, y=4, perbis='ne', label="NE")
Hexagon(common=hxg, x=2.25, y=2.15, perbis='e', label="E")
Hexagon(common=hxg, x=2.25, y=0.25, perbis='se', label="SE")
PageBreak()

# ---- perbis - all
Blueprint(stroke_width=0.5)
Text(common=txt, text="Hex Flat&Pointy: perbis: *")
hxg = Common(height=1.5, dot=0.05, dot_stroke="red", font_size=8)
Hexagon(common=hxg, cx=2, cy=2, perbis='*', orientation="flat")
Hexagon(common=hxg, cx=2, cy=4, perbis='*', orientation="pointy")
PageBreak()

# ---- END
Text(common=txt, text="Hexagon END...")

Save(
     output='png',
     dpi=300,
     directory="../docs/source/images/custom/hexagon",
     names=[
        None,
        "centre", "dot_cross",
        "hatch_flat", "hatch_pointy",
        "hatch_text_flat", "hatch_text_pointy",
        "radii_flat", "radii_pointy",
        "borders_flat", "borders_pointy",
        "perbis_flat", "perbis_pointy", "perbis_all",
        None])
