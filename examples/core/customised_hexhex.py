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
Text(common=txt, text="HexHex: lines")
HexHex(
    cx=2, cy=3,
    height=0.5,
    rings=3,
    fill=None,
    grid_lines=True)
HexHex(
    cx=4, cy=6,
    height=0.5,
    rings=3,
    fill=None,
    shape=None,  # grid only!
    grid_lines=True,
    grid_lines_stroke="red",
    grid_lines_stroke_width=2)
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
        "numbered",
        "lines",
        None])
