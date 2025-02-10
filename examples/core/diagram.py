"""
`diagram` examples for protograf

Written by: Derek Hohls
Created on: 29 February 2016
"""
from protograf import *

Create(filename='diagram.pdf', margin=1)

# create people "boxes"
ceo = Rectangle(x=7, y=24, width=5, height=3, label="CEO")
vp_sales = Rectangle(x=1, y=20, width=5, height=3, label="VP Sales")
vp_rsrch = Rectangle(x=7, y=20, width=5, height=3, label="VP Research")
vp_prods = Rectangle(x=13, y=20, width=5, height=3, label="VP Products")

# link the "boxes"
Connect(ceo, vp_sales, style='direct')
Connect(ceo, vp_rsrch, style='direct')
Connect(ceo, vp_prods, style='direct')

PageBreak()

# ---- arrangement A
centralA = Rectangle(x=8, y=13, width=4, height=3, label="Central A")
top_rightA = Rectangle(x=13, y=18, width=4, height=3, label="TopRight")
top_leftA = Rectangle(x=3, y=18, width=4, height=3, label="TopLeft")
bottom_rightA = Rectangle(x=13, y=8, width=4, height=3, label="BottomRight")
bottom_leftA = Rectangle(x=3, y=8, width=4, height=3, label="BottomLeft")

Connect(centralA, top_rightA, style='path')
Connect(centralA, top_leftA, style='path')

PageBreak()

# ---- arrangement B
centralB = Rectangle(x=8, y=13, width=4, height=3, label="Central B")
top_rightB = Rectangle(x=13, y=15, width=4, height=3, label="TopRight")
top_leftB = Rectangle(x=3, y=15, width=4, height=3, label="TopLeft")
bottom_rightB = Rectangle(x=13, y=11, width=4, height=3, label="BottomRight")
bottom_leftB = Rectangle(x=3, y=11, width=4, height=3, label="BottomLeft")

Connect(centralB, top_rightB, style='path')
Connect(centralB, top_leftB, style='path')

PageBreak()

# ---- arrangement C
centralC = Rectangle(x=8, y=13, width=4, height=3, label="Central C")
top_rightC = Rectangle(x=11, y=18, width=4, height=3, label="TopRight")
top_leftC = Rectangle(x=5, y=18, width=4, height=3, label="TopLeft")
bottom_rightC = Rectangle(x=11, y=8, width=4, height=3, label="BottomRight")
bottom_leftC = Rectangle(x=5, y=8, width=4, height=3, label="BottomLeft")

Connect(centralC, top_rightC, style='path')
Connect(centralC, top_leftC, style='path')

PageBreak()

# ---- arrangement D
centralD = Rectangle(x=8, y=13, width=4, height=3, label="Central D")
top_D = Rectangle(x=8, y=18, width=4, height=3, label="Top")
left_D = Rectangle(x=2, y=13, width=4, height=3, label="Left")
right_D = Rectangle(x=14, y=13, width=4, height=3, label="Right")
bottom_D = Rectangle(x=8, y=8, width=4, height=3, label="Bottom")

Connect(centralD, top_D, style='path')
Connect(centralD, left_D, style='path')
Connect(centralD, right_D, style='path')
Connect(centralD, bottom_D, style='path')

PageBreak()

# Save()
Save(
    output='png',
    dpi=300,
    directory="../docs/source/images/customised",
    names=[
        "diagram_basic", "diagram_a", "diagram_b", "diagram_c", "diagram_d",
    ]
)
