"""
`counters2` example for protograf

Written by: Derek Hohls
"""
from protograf import *

Create()
CounterSheet()
mytext1 = text("C", font_size=24, x=1.2, y=1.5)
myrect1 = rectangle(x=0.25, y=0.25, height=2, width=2, fill_stroke="yellow")
Counter("1-70", myrect1, mytext1)
Save()
