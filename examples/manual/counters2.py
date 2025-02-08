"""
`counters2` example for protograf

Written by: Derek Hohls
Created on: 22 September 2024
"""
from protograf import *

Create()
CounterSheet()
# create a list of text elements for the counters, containing single letters
mytext1 = text(text=excels(1,70), font_size=24, x=1.2, y=1.1)
Counter("1-70", mytext1)
Save()
