"""
Show customised Triangle for protograf

Written by: Derek Hohls
Created on: 25 October 2025

"""
from protograf import *

Create(filename="customised_triangle.pdf",
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
a_dot = dot(dot_width=4, fill="white")

Text(common=txt, text="Triangle START...")
PageBreak()

# ---- triangle - equilateral
Blueprint()
Text(common=txt, text="Triangle: equilateral")
Triangle(
    cx=2, cy=3, side=3,
    stroke_width=1,
    fill="gold",
    title="Equilateral")
PageBreak()

# ---- triangle - isosceles
Blueprint()
Text(common=txt, text="Triangle: isosceles")
Triangle(
    x=0.5, y=5, side=3, height=4,
    stroke_width=1,
    fill="lime",
    title="Isosceles")
PageBreak()

# ---- triangle - irregular
Blueprint()
Text(common=txt, text="Triangle: irregular")
Triangle(
    x=1, y=4, side=3, side2=4.5, side3=2.5,
    stroke_width=1,
    fill="tomato",
    title="Irregular")
PageBreak()

# ---- triangle - dot&cross
Blueprint()
Text(common=txt, text="Triangle: dot; cross")
Triangle(
    x=1, y=2, side=2,
    stroke_width=1,
    dot=.05,
    cross=0.33, cross_stroke="red",
    cross_stroke_width=1,
    title="Equilateral")
Triangle(
    x=1, y=4,
    side=2, height=1.25,
    stroke_width=1,
    dot=.05,
    cross=0.33, cross_stroke="red",
    cross_stroke_width=1,
    title="Isosceles")
Triangle(
    x=1.25, y=5.5,
    side=2, side2=2.5, side3=1.25,
    stroke_width=1,
    dot=.05,
    cross=0.33, cross_stroke="red",
    cross_stroke_width=1,
    title="Irregular")
PageBreak()

# ---- triangle - hatch
Blueprint()
Text(common=txt, text="Triangle: hatch")
Triangle(
    x=1, y=2, side=2,
    hatches_count=5,
    hatches_stroke="red",
    title="Equilateral")
Triangle(
    x=1, y=4,
    side=2, height=1.25,
    hatches_count=5,
    hatches_stroke="red",
    title="Isosceles")
Triangle(
    x=1.25, y=5.5,
    side=2, side2=2.5, side3=1.25,
    hatches_count=5,
    hatches_stroke="red",
    title="Irregular")
PageBreak()

# ---- triangle - rotation
Blueprint()
Text(common=txt, text="Triangle: rotation")
Triangle(
    x=1, y=2, side=2,
    stroke_width=1,
    rotation=45,
    dot=.05,
    heading="Up",
    title="Equilateral")
Triangle(
    x=1, y=4,
    side=2, height=1.25,
    stroke_width=1,
    rotation=45,
    dot=.05,
    heading="Up",
    title="Isosceles")
Triangle(
    x=1.25, y=5.5,
    side=2, side2=2.5, side3=1.25,
    stroke_width=1,
    rotation=45,
    dot=.05,
    heading="Up",
    title="Irregular")
PageBreak()

# ---- triangle - radii
Blueprint()
Text(common=txt, text="Triangle: radii")
Triangle(
    x=1, y=2, side=2,
    stroke_width=1,
    radii="n se sw",
    centre_shapes=[(a_dot)],
    title="Equilateral")
Triangle(
    x=1, y=4,
    side=2, height=1.25,
    stroke_width=1,
    radii="n se sw",
    centre_shapes=[(a_dot)],
    title="Isosceles")
Triangle(
    x=1.25, y=5.5,
    side=2, side2=2.5, side3=1.25,
    stroke_width=1,
    radii="n se sw",
    centre_shapes=[(a_dot)],
    title="Irregular")
PageBreak()

# ---- triangle - perbii
Blueprint()
Text(common=txt, text="Triangle: perbii")
Triangle(
    x=1, y=2, side=2,
    stroke_width=1,
    perbii="s ne nw",
    centre_shapes=[(a_dot)],
    title="Equilateral")
Triangle(
    x=1, y=4,
    side=2, height=1.25,
    stroke_width=1,
    perbii="s ne nw",
    centre_shapes=[(a_dot)],
    title="Isosceles")
Triangle(
    x=1.25, y=5.5,
    side=2, side2=2.5, side3=1.25,
    stroke_width=1,
    perbii="s ne nw",
    centre_shapes=[(a_dot)],
    title="Irregular")
PageBreak()

# ---- triangle - slices
Blueprint()
Text(common=txt, text="Triangle: slices")
Triangle(
    x=1, y=2, side=2,
    stroke_width=1,
    slices=["tomato", "gold", "lime"],
    centre_shapes=[(a_dot)],
    title="Equilateral")
Triangle(
    x=1, y=4,
    side=2, height=1.25,
    stroke_width=1,
    slices=["tomato", "gold", "lime"],
    centre_shapes=[(a_dot)],
    title="Isosceles")
Triangle(
    x=1.25, y=5.5,
    side=2, side2=2.5, side3=1.25,
    stroke_width=1,
    slices=["tomato", "gold", "lime"],
    centre_shapes=[(a_dot)],
    title="Irregular")
PageBreak()

# ---- triangle - pivot
Blueprint()
Text(common=txt, text="Triangle: pivot")
Triangle(
    x=1, y=2, side=2,
    stroke_width=1,
    pivot=30,
    dot=.05,
    title="Equilateral")
Triangle(
    x=1, y=4,
    side=2, height=1.25,
    stroke_width=1,
    pivot=30,
    dot=.05,
    title="Isosceles")
Triangle(
    x=1.25, y=5.5,
    side=2, side2=2.5, side3=1.25,
    stroke_width=1,
    pivot=30,
    dot=.05,
    title="Irregular")
PageBreak()

# ---- triangle - irregular - options
Blueprint(numbering=False)
Text(common=txt, text="Triangle: irregular")

Triangle(
    x=0, y=2,
    side=1.5, side2=1.75, side3=2.55,
    stroke_width=0.5,
    dot=0.06,
    title="3xsides",
    title_size=7)
Triangle(
    x=2, y=2,
    side=1.5, side2=1.75, side3=2.55,
    pivot=30,
    stroke_width=0.5,
    dot=0.06,
    title="pivot:30",
    title_size=7)

Triangle(
    x=0, y=4,
    side=1.5, side2=1.75, angle=115,
    stroke_width=0.5,
    dot=0.06,
    title="2xsides; 115",
    title_size=7)
Triangle(
    x=2, y=4,
    side=2, side2=1.5,  # angle will be 90!
    stroke_width=0.5,
    dot=0.06,
    title="2xsides; rightangle",
    title_size=7)

Triangle(
    x=0, y=6,
    side=1.5, side2=1.5, side3=1.5,
    pivot=30,
    stroke_width=0.5,
    dot=0.06,
    title="equi; pivot:45",
    title_size=7)
Triangle(
    x=3.5, y=6,
    side=1.25, side2=1.75, side3=1.75,
    pivot=90,
    stroke_width=0.5,
    dot=0.06,
    title="iso; pivot:90",
    title_size=7)

PageBreak()

# ---- END
Text(common=txt, text="Triangle END...")

#Save()
Save(
     output="png",
     dpi=300,
     directory="../docs/source/images/custom/triangle",
     names=[
        None,
        "triangle_equilateral",
        "triangle_isosceles",
        "triangle_irregular",
        "triangle_dot_cross",
        "triangle_hatch",
        "triangle_rotation",
        "triangle_radii",
        "triangle_perbii",
        "triangle_slices",
        "triangle_pivot",
        "triangle_irregular_options",
        None,
        ])
