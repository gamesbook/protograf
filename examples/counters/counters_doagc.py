"""
A counters script example for protograf

Written by: Derek Hohls
Created on: 2 August 2025

Notes:
    * The "Destruction of Army Group Center" game is copyright SPI, 1973
    * The fonts used for counters are `Univers LT Std` and `JZNATO V11  3x2`

      * https://github.com/jzedwards/jzfonts
      * https://www.cdnfonts.com/univers-lt-std.font
"""
from protograf import *

Create(filename='doagc.pdf', margin_left=1.5, margin_top=1.5, paper="A4-l")

GERMAN = "#96B1A8"
RUSSIAN = "#B98B40"
UKRAINE = "#778882"

# color swathes
german1 = rectangle(x=-1, y=-1, height=19, width=15, fill_stroke=GERMAN)
russian1 = rectangle(x=13.25, y=-1, height=19, width=14, fill_stroke=RUSSIAN)
german2 = rectangle(x=13.25, y=14, height=4, width=2.5, fill_stroke=GERMAN)
ukraine1 = rectangle(x=15.5, y=14, height=4, width=7.8, fill_stroke=UKRAINE)
# page text
Font("Univers LT Std")
game = text(
    text="Destruction of Army Group Center", align='centre',
    font_size=24, x=12, y=-0.25)
label_ger = text(text="Germans", font_size=16, x=1.5, y=-0.25)
label_rus = text(text="Soviets", font_size=16, x=25.5, y=-0.25)
label_ukr = text(text="German Ukraine Reinf.", font_size=16, x=20, y=17.5)

# load data
# 1st row has these headers: Nationality, UnitType, Combat, Movement, ID, Size, Note
Data(filename="DOAGC.xlsx")

# create counters
CounterSheet(
    width=1.27, height=1.27,
    grid_marks=True,
    grid_marks_stroke="dimgray",
    grid_marks_length=0.5,
    spacing_x=1, spacing_y=1,
    grouping_cols=10, grouping_rows=2,
    zones=[
        ('1', german1),
        ('1', russian1),
        ('1', german2),
        ('1', ukraine1),
        ('1', game),
        ('1', label_rus),
        ('1', label_ger),
        ('1', label_ukr),
    ]
    )

# national colors
basic = Common(x=0, y=0, width=1.27, height=1.27, stroke_width=0.1, stroke='black')
german = rectangle(common=basic, fill=GERMAN)
russian = rectangle(common=basic, fill=RUSSIAN)
ukrainian = rectangle(common=basic, fill=UKRAINE)
blank = rectangle(common=basic, fill=None)

# counters fills
Counter("all", S("{{ Nationality  == 'German' }}", german))
Counter("all", S("{{ Nationality  == 'Russian' }}", russian))
Counter("all", S("{{ Nationality  == 'Ukrainian' }}", ukrainian))
Counter("all", S("{{ Nationality  == '-' }}", blank))

# counter symbols
Font("JZNATO V11  3x2")
symb = Common(x=0.65, y=0.6, align='centre', font_size=10)
Counter("all",
     S("{{ UnitType == 'INF' }}", text(common=symb, text="1")),
     S("{{ UnitType == 'ARM' }}", text(common=symb, text="-")),
     S("{{ UnitType == 'MEC' }}", text(common=symb, text="9")),
     S("{{ UnitType == 'SKI' }}", text(common=symb, text="K")),
     S("{{ UnitType == 'CAV' }}", text(common=symb, text="!")),
)

# counter ID
Font("Univers LT Std")
ident = text(
    text=T('{{ID}}'),
    font_size=5,
    x=0.3, y=0.15, width=0.6, height=0.6,
    wrap=True, align='centre',rotation=90)
Counter("all", ident)

# counter unit size
unit_size = text(
    text=T('{{Size}}'), align='centre',
    font_size=4,
    x=0.65, y=0.3)
Counter("all", unit_size)

# counter unit strength
Font("Univers LT Std", style="bold")
unit_attr = text(
    text=T('{{Combat}}-{{Movement}}'), align='centre',
    font_size=12,
    x=0.65, y=1)
Counter("all", S("{{ Note != 'blank!' }}", unit_attr))

# special
trk = line(x=0.2, y=0.4, length=0.8, stroke_width=1)
crc = circle(cx=1, cy=0.4, radius=0.1, fill_stroke="black")
rail = group(trk, crc, unit_size)
Counter("all", S("{{ UnitType == 'RAIL' }}", rail))

# turn
turn1 = text(
    text="GAME", align='centre',
    font_size=8,
    x=0.65, y=0.5)
turn2 = text(
    text="TURN", align='centre',
    font_size=8,
    x=0.65, y=1)
Counter("179", turn1, turn2)

Save()
