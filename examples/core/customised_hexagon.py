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

# ---- centre
Blueprint()
Text(common=txt, text="Hexagon: cx & cy")
Hexagon(cx=2, cy=1)
Hexagon(cx=2, cy=3, orientation='pointy')
PageBreak()

# ---- dot_cross
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

# ---- hatch_flat
Blueprint()
Text(common=txt, text="Hexagon: flat; hatches")
hxgn = Common(x=1, height=1.5, hatch_count=5, hatch_stroke="red", orientation='flat')
Hexagon(common=hxgn, y=0, hatch='e', label="e/w")
Hexagon(common=hxgn, y=2, hatch='ne', label="ne/sw")
Hexagon(common=hxgn, y=4, hatch='nw', label="nw/se")
PageBreak()

# ---- hatch_pointy
Blueprint()
Text(common=txt, text="Hexagon: pointy; hatches")
hxgn = Common(x=1, height=1.5, hatch_count=5, hatch_stroke="red", orientation='pointy')
Hexagon(common=hxgn, y=0, hatch='n', label="n/s")
Hexagon(common=hxgn, y=2, hatch='ne', label="ne/sw")
Hexagon(common=hxgn, y=4, hatch='nw', label="nw/se")
PageBreak()

# ---- text_flat
Blueprint()
Text(common=txt, text="Hexagon: flat; text")
Hexagon(
    y=2,
    height=2,
    title="Title",
    label="Label",
    heading="Heading")
PageBreak()

# ---- text_pointy
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

# ---- radii_flat
Blueprint(stroke_width=0.5)
Text(common=txt, text="Hexagon: flat; radii")
hxg = Common(height=1.5, dot=0.05, dot_stroke="red", orientation="flat", font_size=8)
Hexagon(common=hxg, x=0.25, y=0.25, radii='sw', label="SW")
Hexagon(common=hxg, x=0.25, y=2.15, radii='w', label="W")
Hexagon(common=hxg, x=0.25, y=4.1, radii='nw', label="NW")
Hexagon(common=hxg, x=2.25, y=4.1, radii='ne', label="NE")
Hexagon(common=hxg, x=2.25, y=2.15, radii='e', label="E")
Hexagon(common=hxg, x=2.25, y=0.25, radii='se', label="SE")
PageBreak()

# ---- radii_pointy
Blueprint(stroke_width=0.5)
Text(common=txt, text="Hexagon: pointy; radii")
hxg = Common(height=1.5, dot=0.05, dot_stroke="red", orientation="pointy", font_size=8)
Hexagon(common=hxg, x=0.25, y=0.25, radii='sw', label="SW")
Hexagon(common=hxg, x=0.25, y=2.15, radii='nw', label="NW")
Hexagon(common=hxg, x=0.25, y=4.1, radii='n', label="N")
Hexagon(common=hxg, x=2.25, y=4.1, radii='ne', label="NE")
Hexagon(common=hxg, x=2.25, y=0.25, radii='s', label="S")
Hexagon(common=hxg, x=2.25, y=2.15, radii='se', label="SE")
PageBreak()

# ---- borders_flat
Blueprint(stroke_width=0.5)
Text(common=txt, text="Hexagon: flat; borders")
hxg = Common(height=1.5, orientation="flat", font_size=8)
Hexagon(common=hxg, x=0.25, y=0.25, borders=('sw', 2, "gold"), label="SW")
Hexagon(common=hxg, x=0.25, y=2.15, borders=('nw', 2, "gold"), label="NW")
Hexagon(common=hxg, x=0.25, y=4.10, borders=('n', 2, "gold"), label="N")
Hexagon(common=hxg, x=2.25, y=4.10, borders=('s', 2, "gold"), label="S")
Hexagon(common=hxg, x=2.25, y=0.25, borders=('ne', 2, "gold"), label="NE")
Hexagon(common=hxg, x=2.25, y=2.15, borders=('se', 2, "gold"), label="SE")
PageBreak()

# ---- borders_pointy
Blueprint(stroke_width=0.5)
Text(common=txt, text="Hexagon: pointy; borders")
hxg = Common(height=1.5, orientation="pointy", font_size=8)
Hexagon(common=hxg, x=0.25, y=0.25, borders=('sw', 2, "gold"), label="SW")
Hexagon(common=hxg, x=0.25, y=2.15, borders=('nw', 2, "gold"), label="NW")
Hexagon(common=hxg, x=0.25, y=4.10, borders=('w', 2, "gold"), label="W")
Hexagon(common=hxg, x=2.25, y=4.10, borders=('e', 2, "gold"), label="E")
Hexagon(common=hxg, x=2.25, y=0.25, borders=('ne', 2, "gold"), label="NE")
Hexagon(common=hxg, x=2.25, y=2.15, borders=('se', 2, "gold"), label="SE")
PageBreak()

# ---- perbis_flat
Blueprint(stroke_width=0.5)
Text(common=txt, text="Hex Flat: perbis")
hxg = Common(height=1.5, dot=0.05, dot_stroke="red", orientation="flat", font_size=8)
Hexagon(common=hxg, x=0.25, y=0.25, perbis='sw', label="SW")
Hexagon(common=hxg, x=0.25, y=2.15, perbis='nw', label="NW")
Hexagon(common=hxg, x=0.25, y=4.1, perbis='n', label="N")
Hexagon(common=hxg, x=2.25, y=4.1, perbis='ne', label="NE")
Hexagon(common=hxg, x=2.25, y=0.25, perbis='s', label="S")
Hexagon(common=hxg, x=2.25, y=2.15, perbis='se', label="SE")
PageBreak()

# ---- perbis_pointy
Blueprint(stroke_width=0.5)
Text(common=txt, text="Hex Pointy: perbis")
hxg = Common(height=1.5, dot=0.05, dot_stroke="red", orientation="pointy", font_size=8)
Hexagon(common=hxg, x=0.25, y=0.25, perbis='sw', label="SW")
Hexagon(common=hxg, x=0.25, y=2.15, perbis='w', label="W")
Hexagon(common=hxg, x=0.25, y=4.1, perbis='nw', label="NW")
Hexagon(common=hxg, x=2.25, y=4.1, perbis='ne', label="NE")
Hexagon(common=hxg, x=2.25, y=2.15, perbis='e', label="E")
Hexagon(common=hxg, x=2.25, y=0.25, perbis='se', label="SE")
PageBreak()

# ---- perbis_all
Blueprint(stroke_width=0.5)
Text(common=txt, text="Hex Flat&Pointy: perbis: *")
hxg = Common(height=1.5, dot=0.05, dot_stroke="red", font_size=8)
Hexagon(common=hxg, cx=2, cy=2, perbis='*', orientation="flat")
Hexagon(common=hxg, cx=2, cy=4, perbis='*', orientation="pointy")
PageBreak()

# ---- slices_flat
Blueprint(stroke_width=0.5)
Text(common=txt, text="Hex Flat: slices")
hxg = Common(height=1.5, dot=0.05, dot_stroke="white", font_size=8)
Hexagon(common=hxg, cx=1.5, cy=1.5, slices=['red', 'blue'], orientation="flat")
Hexagon(common=hxg, cx=1.5, cy=3.5,
        slices=['red', 'orange', 'yellow', 'green', 'blue', 'pink'],
        orientation="flat")
PageBreak()

# ---- slices_pointy
Blueprint(stroke_width=0.5)
Text(common=txt, text="Hex Pointy: slices")
hxg = Common(height=1.5, dot=0.05, dot_stroke="white", font_size=8)
Hexagon(common=hxg, cx=1.5, cy=1.5,  slices=['red', 'blue'], orientation="pointy")
Hexagon(common=hxg, cx=1.5, cy=3.5,
        slices=['red', 'orange', 'yellow', 'green', 'blue', 'pink'],
        orientation="pointy")
PageBreak()

# ---- paths
Blueprint(stroke_width=0.5)
Text(common=txt, text="Hex Paths")
hxg = Common(height=1.5, dot=0.05, dot_stroke="red", font_size=8)
Hexagon(common=hxg, x=0.25, y=0.25, orientation="pointy",
        paths=["ne sw", "e w",  "se nw"])
Hexagon(common=hxg, x=0.25, y=2.15,  orientation="pointy",
        paths=["ne e", "e se", "se sw", "sw w", "w nw", "nw ne"],
        paths_stroke="gold")
Hexagon(common=hxg, x=0.25, y=4.1,  paths=["sw ne", "se nw", "s n"])
Hexagon(common=hxg, x=2.25, y=4.1,
        paths=["s ne", "se sw", "s nw", "nw ne", "n se", "n sw"],
        paths_dotted=True)
Hexagon(common=hxg, x=2.25, y=2.15,
        paths=["ne n", "ne se", "se s", "sw s", "sw nw", "nw n"],
        paths_stroke="gold")
Hexagon(common=hxg, x=2.25, y=0.25,  orientation="pointy",
        paths=["ne se", "e sw", "se w", "sw nw", "w ne", "nw e"],
        paths_dotted=True)
PageBreak()

# ---- spikes
Blueprint(stroke_width=0.5)
Text(common=txt, text="Hex Spikes")
hxg = Common(height=1.5, dot=0.05, dot_stroke="red",
             spikes_width=0.25)
Hexagon(common=hxg, x=0.25, y=0.25, orientation="pointy",
        spikes=["ne", "w",  "se"],
        spikes_height=0.5)
Hexagon(common=hxg, x=2.25, y=4.1,
        spikes=["s", "sw", "nw", "ne", "se", "n"],
        spikes_dotted=True,
        spikes_height=-0.5)
Hexagon(common=hxg, x=2.25, y=0.25,  orientation="pointy",
        spikes=["ne", "se", "sw", "w", "nw", "e"],
        spikes_height=-0.5,
        spikes_dotted=True)
Hexagon(common=hxg, x=0.25, y=2.15,  orientation="pointy",
        spikes=["ne", "se", "sw", "w", "nw", "e"],
        spikes_stroke="gold",
        spikes_fill="gold")
Hexagon(common=hxg, x=0.25, y=4.1,
        spikes=["ne", "nw", "s"],
        spikes_height=0.5)
Hexagon(common=hxg, x=2.25, y=2.15,
        spikes=["s", "sw", "nw", "ne", "se", "n"],
        spikes_height=0.5,
        spikes_stroke="gold",
        spikes_fill="gold")
PageBreak()

# ---- order
Blueprint(stroke_width=0.5)
Text(common=txt, text="Hex Order")
hxg = Common(height=1.5,
             dot=0.05, dot_stroke="red",
             spikes_width=0.25)
Hexagon(common=hxg, x=0.25, y=0.1,
        slices=['red', 'orange', 'yellow'],
        spikes=["ne", "nw", "s"],
        spikes_height=-0.7)
Hexagon(common=hxg, x=2.25, y=0.1,
        slices=['red', 'orange', 'yellow'],
        spikes=["ne", "nw", "s"],
        spikes_height=-0.7,
        order_first=["spikes"])
Hexagon(common=hxg, x=0.25, y=2.1,
        hatch_count=5, hatch_stroke="red",
        hatch_stroke_width=2, hatch='nw',
        radii='sw e',
        radii_stroke_width=2)
Hexagon(common=hxg, x=2.25, y=2.1,
        hatch_count=5, hatch_stroke="red",
        hatch_stroke_width=2, hatch='nw',
        radii='sw e',
        radii_stroke_width=2,
        order_last=["hatches"])
Hexagon(common=hxg, x=0.25, y=4.1,
        perbis='sw n')
Hexagon(common=hxg, x=2.25, y=4.1,
        perbis='sw n',
        order_all=["base", "dot"])

PageBreak()

# ---- END
Text(common=txt, text="Hexagon END...")

Save(
     output='png',
     dpi=300,
     directory="../docs/source/images/custom/hexagon",
     names=[
        None,
        "centre",
        "dot_cross",
        "hatch_flat", "hatch_pointy",
        "hatch_text_flat", "hatch_text_pointy",
        "radii_flat", "radii_pointy",
        "borders_flat", "borders_pointy",
        "perbis_flat", "perbis_pointy",
        "perbis_all",
        "slices_flat", "slices_pointy",
        'hex_paths',
        'hex_spikes',
        'hex_order',
        None])
