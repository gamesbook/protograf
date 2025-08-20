"""
Show customised Circles - and useful overides - for protograf

Written by: Derek Hohls
Created on: 29 September 2024
"""

from protograf import *

Create(filename="customised_circles.pdf",
       paper="A8",
       margin_left=0.5,
       margin_right=0.3,
       margin_bottom=0.2,
       margin_top=0.5,
       font_size=8,
       stroke_width=0.5)


txt = Common(x=0, y=0, font_size=8, align="left")

Text(common=txt, text="Circle START...")
PageBreak()

# ---- circle hatch
Blueprint()
Text(common=txt, text="Circle: hatches")
htc = Common(radius=0.7, hatch_count=5, hatch_stroke="red")
Circle(common=htc, cx=2, cy=5.2, label='5')  # all directions
Circle(common=htc, cx=1, cy=3.7, hatch='o', label='o')
Circle(common=htc, cx=3, cy=3.7, hatch='d', label='d')
Circle(common=htc, cx=1, cy=2.2, hatch='e', label='e')
Circle(common=htc, cx=3, cy=2.2, hatch='n', label='n')
Circle(common=htc, cx=1, cy=0.7, hatch='ne', label='ne')
Circle(common=htc, cx=3, cy=0.7, hatch='nw', label='nw')
PageBreak()

# ---- circle dot_cross
Blueprint()
Text(common=txt, text="Circle: Dot & Cross")
Circle(cx=1, cy=3, radius=1, dot=0.1, dot_stroke="green")
Circle(cx=3, cy=3, radius=1, cross=0.25, cross_stroke="green", cross_stroke_width=1)
PageBreak()

# ---- circle radii
Blueprint()
Text(common=txt, text="Circle: radii (single & overlapped)")
Circle(x=0, y=0,
       radius=2,
       fill=None,
       radii=[45,135,225,315],
       radii_stroke_width=1,
       radii_dotted=True,
       radii_offset=1,
       radii_length=1.25
       )
Circle(x=0, y=0,
       radius=2,
       fill=None,
       radii=[0,90,180,270],
       radii_stroke_width=3,
       radii_stroke="red")
Circle(cx=3, cy=5,
       radius=1,
       fill="green",
       stroke="orange",
       stroke_width=1,
       radii=[0,90,180,270,45,135,225,315],
       radii_stroke_width=8,
       radii_stroke="orange",
       radii_length=0.8)
PageBreak()

# ---- circle petals_triangle
Blueprint()
Text(common=txt, text="Circle: petals; triangle style")
Circle(cx=2, cy=1.5, radius=1,
        petals=11,
        petals_offset=0.25,
        petals_stroke_width=1,
        petals_dotted=1,
        petals_height=0.25,
        petals_fill="gray")
Circle(cx=2, cy=4.5, radius=1,
       stroke="yellow",
       fill=None,
       stroke_width=0.001,
       petals=8,
       petals_stroke_width=3,
       petals_height=0.25,
       petals_stroke="red",
       petals_fill="yellow"
)
PageBreak()

# ---- circle petals_petal
Blueprint()
Text(common=txt, text="Circle: petals; petal style")
Circle(cx=2, cy=1.5, radius=1,
       petals=11,
       petals_style="petal",
       petals_offset=0.2,
       petals_stroke_width=1,
       petals_dotted=1,
       petals_height=0.5,
       petals_fill="gray")

Circle(cx=2, cy=4.5, radius=1,
       fill_stroke="yellow",
       petals=8,
       petals_style="p",
       petals_offset=0.1,
       petals_stroke_width=2,
       petals_height=0.8,
       petals_stroke="red",
       petals_fill="yellow")
PageBreak()

# ---- circle radi_labels
Blueprint()
Text(common=txt, text="Radii: Labels")
Circle(cx=1, cy=5, radius=1,
       radii=[30, 150, 270],
       radii_labels="ABC",
       dot=0.05)
Circle(cx=3, cy=3, radius=1,
       radii=[30, 150, 270],
       radii_labels="A,B,C",
       radii_labels_rotation=90,
       dot=0.05)
Circle(cx=1, cy=1, radius=1,
       radii=[30, 150, 270],
       radii_stroke="white",
       radii_labels=["A", "B", "C"],
       radii_labels_rotation=270,
       radii_labels_stroke="red",
       radii_labels_font="Courier",
       dot=0.05)
PageBreak()

# ---- circle slices
Blueprint()
Text(common=txt, text="Slices")
Circle(cx=1, cy=1, radius=1,
       slices=["red", "gold", "aqua"],
       dot=0.05)
Circle(cx=2, cy=3, radius=1,
       slices=["red", None, "red", None, "red", None],
       dot=0.05)
Circle(cx=3, cy=5, radius=1,
       slices=["red", "gold", "aqua", "red", "gold", "aqua"],
       rotation=30,
       dot=0.05)
Circle(cx=3, cy=1, radius=1,
       slices=["black", "grey", "silver"],
       slices_fractions=[0.33, 0.75, 0.5])
Circle(cx=1, cy=5, radius=1, fill="gold",
       slices=["black", None, "grey", "silver"],
       slices_fractions=[0.33, None, 1.5, 0.75],
       slices_angles=[60, 45, 45, 120])
PageBreak()

# ---- END
Text(common=txt, text="Circle END...")

Save(
     output='png',
     dpi=300,
     directory="../docs/source/images/custom/circle",
     names=[
        None,
        "hatch",
        "dot_cross",
        "radii",
        "petals_triangle",
        "petals_petal",
        "radii_labels",
        "circle_slices",
        None])
