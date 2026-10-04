# -*- coding: utf-8 -*-
"""
Example code for protograf

Written by: Derek Hohls
Created on: 27 September 2026
"""
from protograf import *

Create(
    filename="abstracts.pdf",
    paper_height=10,
    paper_width=10,
    margin=1,
    page_grid=1)

header = Common(x=0, y=0, font_size=12, align="left")
footer = Common(x=0, y=8.5, font_size=12, align="left")

# ---- default Abstract Game Grid
Text("Abstract Game: Default Board", common=header)
agd = AbstractGame()
AbstractState(board=agd)
PageBreak()

# ---- Chess - setup
Text("Chess Game: Setup", common=header)
agcs = AbstractGame(name="chess")
AbstractState(board=agcs, setup=True)
PageBreak()

# ---- Chess - customised board
agcs = AbstractGame(
    name="chess",
    fills=["#FFCE9E", "#D18B47"],  # browns
    frame=True,
    frame_width=15,
    frame_stroke="brown",
    label=True,
    label_stroke="#FFCE9E",
    label_offset_row=0.275,
    label_offset_col=0.25,
)
AbstractState(board=agcs, setup=True)
Text("Chess Game: Frame, Colors & Labels", common=header)
PageBreak()

# ---- Chess - positions
Text("Chess Game: Positions", common=header)
agcp = AbstractGame(name="chess")
AbstractState(
    board=agcp,
    positions="""
    r..qr.k.
    p....pbp
    bp...np.
    ...p....
    ........
    BPN.P.P.
    P.Q.NnBP
    R..R..K.
    """
)
Text("Fischer(B) vs Byrne(W);"
     " 1963/64 USA Chess Championship;"
     " end move 15",
     x=0, y=8.5, font_size=7, align="left")
PageBreak()

# ---- Chess - custom board areas
Text("Chess Game: Custom Squares", common=header)
htch = Default(
    hatches='ne',
    hatches_count=15,
    hatches_stroke_width=1,
    hatches_stroke="dimgray")
sqr = Default(
    fill="white",
    stroke=None,
    height=1,
    width=1)
sqDark = rectangle(default=[sqr, htch])
sqLite = rectangle(default=sqr)

agcb = AbstractGame(
    name="chess",
    areas=[sqLite, sqDark],
    label=True,
)
AbstractState(board=agcb, setup=True)
PageBreak()

# ---- Shogi - setup
Text("Shogi Game: Setup", common=footer)
agss = AbstractGame(name="shogi", label=True)
AbstractState(board=agss, setup=True)
PageBreak()

# ---- Shogi - positions
Text("Shogi Game: Positions (International)", common=footer)
agcp = AbstractGame(
    name="shogi",
    fills=['#D8A300'],
    stroke_width=1.5,
    stroke="white",
    pieces_type="shogi-int")
AbstractState(
    board=agcp,
    positions="""
    L..R..K..
    P.S.NnB.P
    B..PN.P.P
    .........
    ...s.....
    ....p....
    p....pb.p
    bp...n.p.
    l...r.k..
    """
)
PageBreak()

# ---- Checkers - setup
Text("Checkers Game: Setup", common=header)
agks = AbstractGame(name="checkers")
AbstractState(board=agks, setup=True)
PageBreak()

# ---- Hexagons - default
Text("Hexagons: default", common=header)
aghd = AbstractGame(name="hexagons")
AbstractState(board=aghd)
PageBreak()

# ---- Hexagons - hex game
Text("Hexagons: Hex Game", common=header)
aghh = AbstractGame(name="hex")
AbstractState(board=aghh)
PageBreak()

# ---- Hexagons - pattern
Text("Hexagons: pattern", common=header)
aghp = AbstractGame(
    name="hexagons",
    rows=5,
    cols=7,
    pattern = """
    . O O O 0 O .
     0 O O 0 0 O .
    O O . . . O O
     0 O O O 0 O .
    . O O 0 0 O .
    """)
AbstractState(
    board=aghp,
    positions="B3W/B4W/B2W/B4W/B3W")  # SHOULD ignore blank cells!!
# PageBreak()


Save(
    output='png',
    dpi=300,
    directory="../docs/source/images/objects",
    names=[
        'abstracts_default',
        'abstracts_chess_setup',
        'abstracts_chess_customised',
        'abstracts_chess_positions',
        'abstracts_chess_custom_board',
        'abstracts_shogi_setup',
        'abstracts_shogi_positions',
        'abstracts_checkers_setup',
        'abstracts_hexagons_default',
        'abstracts_hexagons_hexgame',
        'abstracts_hexagons_pattern',
    ]
)
