"""
Show customised HexHex grid for protograf

Written by: Derek Hohls
Created on: 20 December 2025
"""

from protograf import *

Create(filename="customised_hexhex.pdf",
       paper="A7",
       margin_left=0.5,
       margin_right=0.3,
       margin_bottom=0.2,
       margin_top=0.5,
       font_size=8,
       stroke_width=0.5)

txt = Common(x=0, y=0, font_size=12, align="left")

Text(common=txt, text="HexHex Grid START...")
PageBreak()

# ---- default
Blueprint()
Text(common=txt, text="HexHex: default")
HexHex(height=0.5)
PageBreak()

# ---- shape
Blueprint()
Text(common=txt, text="HexHex: shape")
HexHex(
    cx=3, cy=5,
    height=1.2,
    rings=3,
    shape=hexagon(height=0.5, fill_stroke="tomato")
)
PageBreak()

# ---- numbered
Blueprint()
Text(common=txt, text="HexHex: numbered")
HexHex(
    cx=2, cy=3,
    height=0.5,
    rings=3,
    show_sequence=True) #,shape=dot() fill=None)
HexHex(
    cx=4, cy=6,
    height=0.5,
    rings=3,
    show_counter=True) #,shape=dot() fill=None)
PageBreak()


# ---- lines
Blueprint()
Text(common=txt, text="HexHex: grid (lines & shape)")
HexHex(
    cx=2, cy=3,
    height=0.5,
    rings=3,
    fill=None,
    shape=None,  # grid only!
    grid_lines=True)
HexHex(
    cx=4, cy=6,
    height=0.5,
    rings=3,
    shape=circle(radius=0.1, fill_stroke="gold"),
    grid_lines=True,
    grid_lines_fill="springgreen",
    grid_lines_stroke="red",
    grid_lines_stroke_width=2)
PageBreak()

# ---- layout
Blueprint()
Text(common=txt, text="HexHex: ring layout")

wcirc = circle(radius=0.25, fill="white")
pcirc = circle(radius=0.25, fill="palegreen")
scirc = circle(radius=0.25, fill="springgreen")
tcirc = circle(radius=0.25, fill="tomato")
gcirc = circle(radius=0.25, fill="gold")
bcirc = circle(radius=0.25, fill="royalblue")
HexHex(
   cx=2, cy=3, rings=4,
   height=0.5,
   shapes=[
       (0, [wcirc]),
       (1, [pcirc]*6),
       (2, [scirc]*12),
       (3, [tcirc]*3 + [None] + [gcirc]*5 + [None] + [bcirc]*5 + [None] + [tcirc]*2),]
)

Gr = hexagon(height=0.5, fill="darkgray")
Br = hexagon(height=0.5, fill="chocolate")
Yl = hexagon(height=0.5, fill="sandybrown")
HexHex(
   cx=4, cy=7, rings=4,
   height=0.5,
   shapes=[
       (0, [Yl]),
       (1, [Br, Gr]*3),
       (2, [Gr, Yl, Br, Yl]*3),
       (3, [Yl, Br, Gr, Yl, Gr, Br]*3),
           (4, [Br, Gr, Yl, Br, Gr, Br, Yl, Gr]*3),]
)
PageBreak()

# ---- END
Text(common=txt, text="HexHex Grid END...")

Save(
     output='png',
     dpi=300,
     directory="../docs/source/images/custom/hexhex",
     names=[
        None,
        "default",
        "shape",
        "numbered",
        "lines",
        "ring",
        None])
