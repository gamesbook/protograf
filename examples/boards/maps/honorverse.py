"""
Map of the "Honor Harrington Universe" (aka Honoverse) for protograf

Developed by: Derek Hohls
Created on: 18 April 2025

Notes:

    Primary map sources used to create this map are from:

    * https://www.gotshifted.com/honorverseglossary/MAPS.html
    * https://www.gotshifted.com/honorverseglossary/Book%20Originals.html

    Any errors are mine - NOT the original sources!
"""
from protograf import *

Create(filename="honorverse.pdf", margin=1.0, paper="A2-l")

# source used to create the star locations
#Image("honorverse.png", x=0, y=0, width=57.4, height=37.2)

MIDGARD = "#80BFFF"
ANDERMAN = "#FFBF80"
SILESIA = "#80FFBF"
ASGARD = "#80FFFF"
MATAPAN = "#BFFF80"
SOLARIAN_CORE = "#468C46"
SOLARIAN_SHELL = "#59B359"
SOLARIAN_INNER = "#6CD96C"
SOLARIAN_OUTER = "#80FF80"
SOLARIAN_VERGE = "#9ACD32"
TALBOTT = "#BF80FF"
PHOENIX = "#FFFF80"
HAVEN = "#FF80FF"
MANTICORE = "#C0C0C0"
MONICA =  "#BDB76B" # "#A0522D"

DARK_MODE = True  # True to use Black background
if DARK_MODE:
    WORMHOLE = "red"
    STAR = "white"
    CAPITAL = "red"
    GRID = "black"
    SCALE = "white"
else:
    WORMHOLE = "red"
    STAR = "black"
    CAPITAL = "red"
    GRID = None
    SCALE = "black"

THE_FONT = "Helvetica"

# grid / overlay
#Blueprint(numbering_x=15, edges="n w e s",
#          subdivisions=5, stroke_width=0.5,
#          edges_x=30, edges_y=20)
Rectangle(x=0, y=0, height=38, width=56, stroke="#587CBC", fill=GRID)
Grid(x=0, y=0, side=4, stroke="#587CBC")

# empires
Ellipse(cx=27.5, cy=3, height=5.5, width=4, fill=None, stroke=SILESIA, stroke_width=10)
Circle(cx=22, cy=7, radius=4, fill=None, stroke=ANDERMAN, stroke_width=10)
Ellipse(cx=15, cy=3, height=5.5, width=7, fill=None, stroke=MIDGARD, stroke_width=10)
Ellipse(cx=10, cy=13, height=3, width=4, fill=None, stroke=MATAPAN, stroke_width=10)
Circle(cx=11, cy=18, radius=2, fill=None, stroke=ASGARD, stroke_width=10)
Circle(cx=40, cy=6, radius=5.5, fill=None, stroke=HAVEN, stroke_width=10)
Ellipse(cx=30.5, cy=10, height=5, width=8, fill=None, stroke=MANTICORE, stroke_width=10)
Circle(cx=11, cy=29, radius=5.5, fill=None, stroke=TALBOTT, stroke_width=10)
Circle(cx=28.2, cy=32.7, radius=4.1, fill=None, stroke=SOLARIAN_CORE, stroke_width=10)
Circle(cx=28.2, cy=32.7, radius=6.5, fill=None, stroke=SOLARIAN_SHELL, stroke_width=8)
Circle(cx=28.2, cy=32.7, radius=8.5, fill=None, stroke=SOLARIAN_INNER, stroke_width=6)
Circle(cx=28.2, cy=32.7, radius=11.3, fill=None, stroke=SOLARIAN_OUTER, stroke_width=4)
Circle(cx=28.2, cy=32.7, radius=18, fill=None, stroke=SOLARIAN_VERGE, stroke_width=2, dotted=True)
Ellipse(cx=55, cy=29.5, height=2.5, width=1.5, fill=None, stroke=PHOENIX, stroke_width=10)
Ellipse(cx=5.1, cy=34.5, height=1.5, width=2, fill=None, stroke=MONICA, stroke_width=10)

systems = [
    # NEUTRAL
    ("N01", "Aphid", 32.35, 3, "neutral", ""),
    ("N00", "Gemini", 30.85, 5.25, "neutral", ""),
    ("N00", "Nuada", 31.65, 5.55, "neutral", ""),
    ("N00", "Hannah's Star", 30.65, 5.9, "neutral", ""),
    ("N00", "Reiko", 30.6, 7.2, "neutral", ""),
    ("N00", "Yalta", 32.05, 5.95, "neutral", ""),
    ("N00", "Santander", 32.35, 7.3, "neutral", ""),
    ("N00", "Suichien", 31.7, 6.85, "neutral", ""),
    ("N00", "Sallah", 34.65, 8.25, "neutral", ""),
    #("N00", "Candor", 0, 0, "neutral", "",),
    ("N00", "Adler", 35.1, 9.2, "neutral", ""),
    ("N00", "Micah", 35.2, 9.55, "neutral", ""),
    ("N00", "Elric", 35.45, 10.85, "neutral",  "",),

    # Manticore Kingdom
    ("M01", "Manticore", 31, 10.2, "manti", "capital"),
    ("M99", "Marsh", 25.5, 4, "manti", ""),
    ("M02", "Basilisk", 31, 1, "manti", ""),
    ("M12", "Talbot", 33.6, 7.8, "manti",  "",),
    ("M13", "Chelsea", 33.1, 8.55, "manti",  "",),
    ("M14", "Mendoza", 32.4, 8.3, "manti",  "",),
    ("M16", "Hancock", 31.3, 8.05, "manti",  "",),
    ("M17", "Zanzibar", 31.4, 8.7, "manti",  "",),
    ("M18", "Klein Station", 32.25, 8.9, "manti",  "",),
    ("M19", "Talisman", 31.45, 9.35, "manti",  "",),
    ("M27", "Quest", 34.0, 9.7, "manti",  "",),
    ("M28", "Casca", 33.25, 10.05, "manti",  "",),
    ("M30", "Yeltsin", 32.3, 9.9, "manti",  "",),
    ("M31", "Clearaway", 31.65, 10.35, "manti",  "",),
    ("M32", "Zuckerman", 32.1, 10.75, "manti",  "",),
    ("M33", "Doreas", 32.8, 11.1, "manti",  "",),
    ("M34", "Grendelsbane", 33.4, 11.6, "manti",  "",),
    ("M35", "Minette", 33.35, 10.75, "manti",  "",),
    ("M35", "Ramon", 31.6, 11.3, "manti",  "",),
    ("M36", "Endicott", 32.3, 9.7, "manti",  "up",),
    ("M37", "Candor", 32.9, 10.45, "manti",  "",),
    ("M40", "Quentin", 32.5, 11.5, "manti",  "",),
    ("M41", "Minorca", 29.4, 8.45, "manti",  "",),
    ("M42", "Alizon", 30.8, 8.8, "manti",  "",),
    ("M43", "Yorik", 30.75, 8.3, "manti",  "",),
    ("M44", "Clairmont", 33.7, 9.25, "manti",  "",),
    ("M45", "Reevesport", 29.15, 6.7, "manti",  "",),
    ("M46", "Poicters", 32.7, 7.8, "manti",  "",),

    # People's Republic of Haven
    ("H00", "Haven", 41.3, 3.7, "haven", "capital"),
    ("H01", "Hallman", 39.9, 5.2, "haven", ""),
    ("H02", "Tahlman", 39.0, 6.2, "haven", ""),
    ("H03", "Samson", 36.65, 7.2, "haven", ""),
    ("H04", "Solan", 38.5, 7.2, "haven", ""),
    ("H05", "Macgregor", 37.65, 7.65, "haven", ""),
    ("H06", "Owens", 37.05, 7.65, "haven", ""),
    ("H07", "Mylar", 37.1, 8.1, "haven", ""),
    ("H08", "Barnett", 37.35, 7.65, "haven", "up"),
    ("H09", "Seljuk", 35.15, 7.15, "haven", ""),
    ("H10", "Madras", 35.55, 7.7, "haven", ""),
    ("H15", "Seaford 9", 31.7, 7.8, "haven", ""),
    ("H20", "Trevor's Star", 39, 6.55, "haven", ""),
    ("H21", "Corrigan", 35.7, 8.6, "haven", ""),
    ("H22", "Mathias", 36.5, 9.25, "haven", ""),
    ("H25", "Treadway", 35.3, 10.1, "haven", ""),
    ("H29", "Solway", 35.55, 11.55, "haven",  "",),
    ("H30", "Cerberus", 39.7, 0.7, "haven", ""),
    ("H31", "Chantilly", 39.55, 2.15, "haven", ""),
    ("H32", "Des Moines", 40.35, 2.45, "haven", ""),
    ("H33", "Lorn", 39.0, 3.0, "haven", ""),
    ("H34", "Hera", 39.7, 3.3, "haven", ""),
    ("H35", "Daniel", 40.7, 2.9, "haven", ""),
    ("H36", "Solor", 42.6, 2.6, "haven", ""),
    ("H37", "Augusta", 42.7, 3.3, "haven", ""),
    ("H38", "Gaston", 39.5, 4.0, "haven", ""),
    ("H39", "Joubert", 40.3, 3.95, "haven", ""),
    ("H40", "Tambourin", 40.7, 4.3, "haven", ""),
    ("H40", "Fordyce", 42.8, 4.1, "haven", ""),
    ("H41", "Joust", 39.1, 4.5, "haven", ""),
    ("H42", "Saseboe", 39.85, 4.5, "haven", ""),
    ("H43", "Loval", 40.05, 4.7, "haven", ""),
    ("H44", "Tequila", 39.7, 5.45, "haven", ""),
    ("H45", "Elf", 40.65, 5.45, "haven", ""),
    ("H46", "Slocum", 42.1, 5.15, "haven", ""),
    ("H47", "Michael", 40.1, 5.85, "haven", ""),
    ("H48", "Suarez", 42.1, 6.95, "haven", ""),
    ("H50", "Secour", 37., 5.05, "haven", ""),
    ("H51", "Helmsport", 35.95, 5.4, "haven", ""),
    ("H52", "Cascabel", 36.45, 5.55, "haven", ""),
    ("H53", "Hyacinth", 36.1, 6.0, "haven", ""),
    ("H54", "Maastricht", 38.45, 5.95, "haven", ""),
    ("H55", "Lowell", 36.9, 6.2, "haven", ""),
    ("H56", "Franconia", 36.2, 6.25, "haven", ""),
    ("H57", "Hyacinth", 36.1, 6.0, "haven", ""),
    ("H58", "Sun-Yat", 36.2, 6.7, "haven", ""),
    ("H59", "Runciman", 37.25, 6.75, "haven", ""),
    ("H60", "Thetis", 38.05, 6.7, "haven", ""),
    ("H61", "Gaulf", 39.05, 7.65, "haven", ""),
    ("H62", "Seabring", 36.3, 8.45, "haven", ""),
    ("H63", "Stocum", 38.25, 8.25, "haven", ""),
    ("H64", "Welladay", 37.6, 8.75, "haven", ""),
    ("H67", "Barnes", 36.8, 9.45, "haven", ""),
    ("H68", "Allman", 37.1, 9.9, "haven", ""),
    ("H69", "Casca", 39.35, 8.9, "haven", ""),

    # Anderman Empire
    ("A01", "Durendel", 21.7, 8.4, "anderman", ""),
    ("A02", "Gregor B", 23.4, 8.2, "anderman", ""),
    ("A03", "New Berlin", 22.1, 6.5, "anderman", "capital"),

    # Migard Federation
    ("G01", "Midgard", 14.45, 4.35, "midgard", ""),

    # Phoenix Cluster
    ("X01", "Terra Haute", 55.2, 28.85, "phoenix",  "",),
    ("X01", "Hennessy", 55.3, 29.9, "phoenix",  "",),

    # Matapan
    ("P01", "Matapan", 10.6, 12.9, "matapan",  "",),
    ("P01", "Matapan Nova", 10.15, 13.4, "matapan",  "",),

    # Asgard
    ("001", "Asgard", 11.25, 18.5, "asgard",  "",),

    # NEUTRAL
    ("N00", "Kay", 40.2, 15.2, "neutral",  "",),
    ("N00", "Congo", 43.0, 14.8, "neutral",  "",),
    ("N00", "Osmani", 0.5, 22.0, "neutral",  "",),
    ("N00", "Corovix", 3.15, 20.95, "neutral",  "",),
    ("N00", "Tyrel", 1.6, 24.15, "neutral",  "",),
    ("N00", "Selkirk", 4.75, 23.65, "neutral",  "",),
    ("N00", "Chomanand", 7.35, 22.0, "neutral",  "",),
    ("N00", "Portillo", 12.2, 20.8, "neutral",  "",),
    ("N00", "Taimu", 13.25, 19.7, "neutral",  "",),
    #("N00", "", 0, 0, "neutral",  "",),

    # Republic of Monica
    ("Y01", "Taylor", 4.8, 34.6, "monica",  "",),
    ("Y02", "Monica", 5.4, 34.1, "monica",  "",),

    ("N00", "Zale", 2.5, 33.5, "neutral",  "",),
    ("N00", "Erewhon", 44.15, 15.7, "neutral",  "",),
    ("N00", "Babilha", 19.75, 22.95, "neutral", ""),
    ("N00", "Rasmussen", 18.1, 20.25, "neutral", ""),
    ("N00", "Basra", 34.15, 17.7, "neutral", ""),
    ("N00", "Okada", 31.55, 19.7, "neutral", ""),
    ("N00", "Alt", 36.7, 21.0, "neutral", ""),
    ("N00", "Degenhart", 37.0, 17.15, "neutral", ""),
    ("N00", "Limbo", 35.35, 23.35, "neutral", ""),
    ("N00", "Johansen", 38.1, 23.35, "neutral", ""),
    ("N00", "Meroa", 39.8, 23.9, "neutral", ""),
    ("N00", "Aral", 38.85, 25.45, "neutral", ""),
    ("N00", "Dockhorn", 41.35, 26.2, "neutral", ""),
    ("N00", "Sherkan", 34.45, 21.7, "neutral", ""),
    ("N00", "Theron", 34.3, 19.7, "neutral", ""),
    ("N00", "Tiberian", 38.65, 16.15, "neutral", ""),

    # Solarian League
    ("L03", "Beowulf", 27.8, 30.9, "solarian", ""),
    ("L02", "Sasebo", 22.0, 33.8, "solarian", ""),
    ("L01", "Sol", 28.2, 32.7, "solarian", "capital"),
    ("L04", "Spargue", 42.3, 17.2, "solarian", ""),
    ("L05", "Poul", 41.35, 18.85, "solarian", ""),
    ("L06", "Maya", 43.45, 18.3, "solarian", ""),
    ("L07", "Isaac", 47.5, 17.85, "solarian", ""),
    ("L08", "Randal", 40.15, 20.6, "solarian", ""),
    ("L09", "Edwin", 42.4, 20.5, "solarian", ""),
    ("L10", "Robert", 44.5, 21.0, "solarian", ""),
    ("L11", "Murray", 48.05, 21.3, "solarian", ""),
    ("L12", "Sankar", 28.9, 22.25, "solarian", ""),
    ("L13", "Lima", 31.1, 24.2, "solarian", ""),
    ("L14", "Ajax", 32.5, 23.85, "solarian", ""),
    ("L20", "Howard", 7.9, 35.1, "solarian",  "",),
    ("L21", "Saltash", 13.6, 36.6, "solarian",  "",),
    ("L22", "Meyers", 3.55, 36.45, "solarian",  "",),

    # Talbot Cluster
    ("T01", "Lynx", 15.3, 30.4, "talbott", ""),
    ("T02", "Pequod", 7.9, 25.3, "talbott", ""),
    ("T03", "Celebrant", 11.5, 25.15, "talbott", ""),
    ("T04", "New Tuscany", 7.4, 26.9, "talbott", ""),
    ("T05", "Prairie", 10.6, 27.6, "talbott", ""),
    ("T06", "Nuncio", 14.25, 26.9, "talbott", ""),
    ("T07", "Scarlet", 5.8, 28.5, "talbott", ""),
    ("T08", "Redoubt", 8.95, 27.9, "talbott", ""),
    ("T09", "San Miguel", 10.6, 28.0, "talbott", ""),
    ("T10", "Rembrandt", 11.7, 27.4, "talbott", ""),
    ("T11", "Mainwaring", 13.75, 27.9, "talbott", ""),
    ("T12", "Alarian", 6.85, 29.1, "talbott", ""),
    ("T13", "Spindle", 12.3, 29.05, "talbott", ""),
    ("T14", "Dresden", 8.95, 29.55, "talbott", ""),
    ("T15", "Split", 14.9, 29.1, "talbott", ""),
    ("T16", "Talbott", 7.9, 30.7, "talbott", "capital"),
    ("T17", "Tillerman", 6.85, 31.3, "talbott", ""),
    ("T18", "Montana", 10.0, 31.9, "talbott", ""),

    # NEUTRAL
    ("N00", "Fosbee", 17.6, 26.8, "neutral",  "",),

    # Silesian Confed
    ("S01", "Willis", 28.3, 0.7, "silesia", "up"),
    ("S02", "Hendrikson", 28.4, 0.8, "silesia", "right"),
    ("S03", "Jarmon", 28.3, 0.9, "silesia", "right"),
    ("S04", "Terrance", 29.15, 1.55, "silesia", ""),
    ("S05", "Tumult", 28.1, 1.6, "silesia", ""),
    ("S06", "Sarah", 27.15, 1.1, "silesia", ""),
    ("S07", "Carlton", 26.55, 1.2, "silesia", ""),
    ("S08", "Silesia", 27.6, 2.9, "silesia", "capital"),
    ("S09", "Brinkman", 26.95, 2.55, "silesia", ""),
    ("S10", "Hume", 26.3, 2.55, "silesia", ""),
    ("S11", "Breslau", 25.8, 2.65, "silesia", ""),
    ("S12", "Telmach", 26.6, 3.05, "silesia", ""),
    ("S13", "Libau", 25.7, 3.15, "silesia", ""),
    ("S14", "Gosset", 26.0, 2.85, "silesia", ""),
    ("S15", "Lua Hiller", 26.45, 3.55, "silesia", "up"),
    ("S16", "Hillman", 29.1, 3.35, "silesia", ""),
    ("S17", "Tyler's Star", 27.25, 3.3, "silesia", ""),
    ("S18", "Zorester", 26.55, 3.75, "silesia", ""),
    ("S19", "Lutrell", 28.5, 3.7, "silesia", "up"),
    ("S20", "Posnan", 27.2, 3.7, "silesia", ""),
    ("S21", "Arendscheldt", 27.5, 3.6, "silesia", "right"),
    ("S22", "Sigma", 27.8, 3.85, "silesia", ""),
    ("S23", "Creswell", 27.45, 4.3, "silesia", ""),
    ("S24", "Hera", 28.1, 4.15, "silesia", ""),
    ("S25", "Saginaw", 28.45, 4.45, "silesia", ""),
    ("S26", "Pysche", 27.6, 4.6, "silesia", ""),
    ("S27", "Saschen", 26.15, 3.9, "silesia", ""),
    ("S28", "Trellis", 26.4, 4.25, "silesia", ""),
    ("S29", "Slocum", 26.65, 4.5, "silesia", ""),
    ("S30", "Sharon's Star", 27.2, 3.9, "silesia", ""),
    ("S31", "Magyar", 26.85, 4.1, "silesia", ""),
    ("S32", "Schiller", 26.65, 4.05, "silesia", ""),
    ]

wormholes = [
    ("Manticore", "Basilisk", 210),
    ("Manticore", "Trevor's Star", 210),
    ("Manticore", "Gregor B", 180),
    ("Manticore", "Matapan", 472),
    ("Manticore", "Beowulf", 475),
    ("Manticore", "Lynx", 612),
    ("Manticore", "Hennessy", 712),

    ("Erewhon", "Terra Haute", 390),
    ("Erewhon", "Sasebo", 740),  # was JOSHUA:359

    ("Asgard", "Midgard", 360),
    ("Asgard", "Durendel", 365),
    ("Asgard", "Matapan Nova", 130),
    ]

wormhole = Common(stroke_width=2, stroke=WORMHOLE)
stop_coords, start_coords = None, None
for worm in wormholes:
    start, stop = worm[0], worm[1]
    for system in systems:
        if stop == system[1]:
            stop_coords = (system[2], system[3])
        if start == system[1]:
            start_coords = (system[2], system[3])
    if stop_coords and start_coords:
        Line(
            common=wormhole,
            x=start_coords[0], y=start_coords[1],
            x1=stop_coords[0], y1=stop_coords[1],
        )

for system in systems:
    # print(system)
    if "capital" in system[5]:
        Circle(
            cx=system[2], cy=system[3], radius=0.1,
            fill=CAPITAL, label_stroke=STAR,
            label_size=8, label=system[1], label_my=0.2)
    else:
        if "neutral" in system[4]:
            ICON = 'I'
        else:
            ICON = 'H'
        if 'manti' in system[4]:
            ICON = 'J'
        Text(
            x=system[2],
            y=system[3] + 0.1,
            stroke=STAR,
            font_size=8,
            font_name='zapfdingbats',
            text=ICON
        )
        dx, dy = 0, 0
        align = "centre"
        if "up" in system[5]:
            dy = -0.15
        else:
            dy = 0.2
        if "right" in system[5]:
            dx = 0.1
            dy = 0.05
            align = 'left'
        Text(
            x=system[2] + dx,
            y=system[3] + dy,
            stroke=STAR,
            font_size=4,
            align=align,
            font_name=THE_FONT,
            text=system[1],
        )
# LEGEND
Rectangle(x=0, y=37, height=5, width=57,
          fill="white", stroke="white")
Line(x=0, y=37, x1=56, y1=37, stroke="#587CBC")
Text(x=30, y=39, font_name=THE_FONT, font_size=40,
     text="Honor Harrington Universe")

# empires
Circle(cx=1, cy=37.4, radius=0.3,
       stroke=MIDGARD, stroke_width=4)
Text(x=1.5, y=37.6, font_name=THE_FONT, font_size=18,
     text="Midgard Federation", align="left")
Circle(cx=1, cy=38.2, radius=0.3,
       stroke=ANDERMAN, stroke_width=4)
Text(x=1.5, y=38.4, font_name=THE_FONT, font_size=18,
     text="Anderman Empire", align="left")
Circle(cx=1, cy=38.9, radius=0.3,
       stroke=SILESIA, stroke_width=4)
Text(x=1.5, y=39.2, font_name=THE_FONT, font_size=18,
     text="Silesia", align="left")
Circle(cx=1, cy=39.65, radius=0.3,
       stroke=MANTICORE, stroke_width=4)
Text(x=1.5, y=39.85, font_name=THE_FONT, font_size=18,
     text="Star Kingdom of Manticore", align="left")
Circle(cx=1, cy=40.4, radius=0.3,
       stroke=HAVEN, stroke_width=4)
Text(x=1.5, y=40.6, font_name=THE_FONT, font_size=18,
     text="People's Republic of Haven", align="left")
Circle(cx=11, cy=37.4, radius=0.3,
       stroke=MATAPAN, stroke_width=4)
Text(x=11.5, y=37.6, font_name=THE_FONT, font_size=18,
     text="Matapan", align="left")
Circle(cx=11, cy=38.2, radius=0.3,
       stroke=ASGARD, stroke_width=4)
Text(x=11.5, y=38.4, font_name=THE_FONT, font_size=18,
     text="Asgard", align="left")
Circle(cx=11, cy=38.9, radius=0.3,
       stroke=TALBOTT, stroke_width=4)
Text(x=11.5, y=39.2, font_name=THE_FONT, font_size=18,
     text="Talbot Cluster", align="left")
Circle(cx=11, cy=39.65, radius=0.3,
       stroke=MONICA, stroke_width=4)
Text(x=11.5, y=39.85, font_name=THE_FONT, font_size=18,
     text="Republic of Monica", align="left")
Circle(cx=11, cy=40.4, radius=0.3,
       stroke=PHOENIX, stroke_width=4)
Text(x=11.5, y=40.6, font_name=THE_FONT, font_size=18,
     text="Phoenix Foundation", align="left")

Circle(cx=41, cy=37.4, radius=0.3,
       stroke=SOLARIAN_CORE, stroke_width=4)
Text(x=41.5, y=37.6, font_name=THE_FONT, font_size=18,
     text="Solarian League", align="left")
Circle(cx=41, cy=38.2, radius=0.3,
       stroke=SOLARIAN_SHELL, stroke_width=4)
Text(x=41.5, y=38.4, font_name=THE_FONT, font_size=18,
     text="The Shell", align="left")
Circle(cx=41, cy=38.9, radius=0.3,
       stroke=SOLARIAN_INNER, stroke_width=4)
Text(x=41.5, y=39.2, font_name=THE_FONT, font_size=18,
     text="Inner Protectorate", align="left")
Circle(cx=41, cy=39.65, radius=0.3,
       stroke=SOLARIAN_OUTER, stroke_width=4)
Text(x=41.5, y=39.85, font_name=THE_FONT, font_size=18,
     text="Outer Protectorate", align="left")
Circle(cx=41, cy=40.4, radius=0.3,
       stroke=SOLARIAN_VERGE, stroke_width=4, dotted=True)
Text(x=41.5, y=40.6, font_name=THE_FONT, font_size=18,
     text="The Verge", align="left")


Text(x=50, y=37.6, font_name='zapfdingbats', font_size=18, text=" H")
Text(x=50.5, y=37.6, font_name=THE_FONT, font_size=18,
     text="Empire's System", align="left")

Text(x=50, y=38.4, font_name='zapfdingbats', font_size=18, text="I")
Text(x=50.5, y=38.4,font_name=THE_FONT, font_size=18,
     text="Neutral System", align="left")

Text(x=50, y=39.2, font_name='zapfdingbats', font_size=18, text="J")
Text(x=50.5, y=39.2, font_name=THE_FONT, font_size=18,
     text="Manticore System", align="left")

Line(x=49.5, y=39.65, stroke_width=4, stroke=WORMHOLE)
Text(x=50.5, y=39.85, font_name=THE_FONT, font_size=18,
     text="Wormhole Link", align="left")

Line(x=48, y=34, x1=52, y1=34,
     stroke_width=4, stroke=SCALE,
     label="100 light years", label_my=-0.4)

Save()
