# -*- coding: utf-8 -*-
"""
Common constants used in protograf

Notes:
    * https://www.a2-size.com/american-paper-sizes/
    * https://en.wikipedia.org/wiki/Paper_size#Overview_of_ISO_paper_sizes
"""
from pymupdf.utils import getColorList

BGG_IMAGES = "cf.geekdo-images.com"
COLOR_NAMES = getColorList()
CACHE_DIRECTORY = ".protograf"  # append to the user's home directory
DEBUG_COLOR = "#B0C4DE"
DEFAULT_CARD_WIDTH = 180  # pt (2.5")
DEFAULT_CARD_HEIGHT = 252  # pt (3.5")
DEFAULT_CARD_RADIUS = 72  # pt (1")
DEFAULT_CARD_COUNT = 9
DEFAULT_COUNTER_RADIUS = 18  # pt (1/4")
DEFAULT_COUNTER_SIZE = 72  # pt (1")
DEFAULT_DPI = 300
DEFAULT_FONT = "Helvetica"
DEFAULT_MARGIN_SIZE = 18  # pt (1/4")

GRID_SHAPES_WITH_CENTRE = [
    "CircleShape",
    "CompassShape",
    "DotShape",
    "EllipseShape",
    "HexShape",
    "PolygonShape",
    "RectangleShape",
    "RhombusShape",
    "SquareShape",
    "StadiumShape",
    "StarShape",
    "TrapezoidShape",
]
GRID_SHAPES_NO_CENTRE = [
    "TextShape",
]
# NOT GRID:  ArcShape, BezierShape, PolylineShape, ChordShape

# following shapes must have vertices accessible WITHOUT calling draw()
SHAPES_FOR_TRACK = [
    "LineShape",
    "PolygonShape",
    "PolylineShape",
    "RectangleShape",
    "RhombusShape",
    "SquareShape",
]

COLORS_SVG = {
    "black": "#000000",
    "navy": "#000080",
    "darkblue": "#00008b",
    "mediumblue": "#0000cd",
    "blue": "#0000ff",
    "darkgreen": "#006400",
    "green": "#008000",
    "teal": "#008080",
    "darkcyan": "#008b8b",
    "deepskyblue": "#00bfff",
    "darkturquoise": "#00ced1",
    "mediumspringgreen": "#00fa9a",
    "lime": "#00ff00",
    "springgreen": "#00ff7f",
    "aqua": "#00ffff",
    "cyan": "#00ffff",
    "midnightblue": "#191970",
    "dodgerblue": "#1e90ff",
    "lightseagreen": "#20b2aa",
    "forestgreen": "#228b22",
    "seagreen": "#2e8b57",
    "darkslategray": "#2f4f4f",
    "darkslategrey": "#2f4f4f",
    "limegreen": "#32cd32",
    "mediumseagreen": "#3cb371",
    "turquoise": "#40e0d0",
    "royalblue": "#4169e1",
    "steelblue": "#4682b4",
    "darkslateblue": "#483d8b",
    "mediumturquoise": "#48d1cc",
    "indigo ": "#4b0082",
    "darkolivegreen": "#556b2f",
    "cadetblue": "#5f9ea0",
    "cornflowerblue": "#6495ed",
    "mediumaquamarine": "#66cdaa",
    "dimgray": "#696969",
    "dimgrey": "#696969",
    "slateblue": "#6a5acd",
    "olivedrab": "#6b8e23",
    "slategray": "#708090",
    "slategrey": "#708090",
    "lightslategray": "#778899",
    "lightslategrey": "#778899",
    "mediumslateblue": "#7b68ee",
    "lawngreen": "#7cfc00",
    "chartreuse": "#7fff00",
    "aquamarine": "#7fffd4",
    "maroon": "#800000",
    "purple": "#800080",
    "olive": "#808000",
    "gray": "#808080",
    "grey": "#808080",
    "skyblue": "#87ceeb",
    "lightskyblue": "#87cefa",
    "blueviolet": "#8a2be2",
    "darkred": "#8b0000",
    "darkmagenta": "#8b008b",
    "saddlebrown": "#8b4513",
    "darkseagreen": "#8fbc8f",
    "lightgreen": "#90ee90",
    "mediumpurple": "#9370d8",
    "darkviolet": "#9400d3",
    "palegreen": "#98fb98",
    "darkorchid": "#9932cc",
    "yellowgreen": "#9acd32",
    "sienna": "#a0522d",
    "brown": "#a52a2a",
    "darkgray": "#a9a9a9",
    "darkgrey": "#a9a9a9",
    "lightblue": "#add8e6",
    "greenyellow": "#adff2f",
    "paleturquoise": "#afeeee",
    "lightsteelblue": "#b0c4de",
    "powderblue": "#b0e0e6",
    "firebrick": "#b22222",
    "darkgoldenrod": "#b8860b",
    "mediumorchid": "#ba55d3",
    "rosybrown": "#bc8f8f",
    "darkkhaki": "#bdb76b",
    "silver": "#c0c0c0",
    "mediumvioletred": "#c71585",
    "indianred ": "#cd5c5c",
    "peru": "#cd853f",
    "chocolate": "#d2691e",
    "tan": "#d2b48c",
    "lightgray": "#d3d3d3",
    "lightgrey": "#d3d3d3",
    "palevioletred": "#d87093",
    "thistle": "#d8bfd8",
    "orchid": "#da70d6",
    "goldenrod": "#daa520",
    "crimson": "#dc143c",
    "gainsboro": "#dcdcdc",
    "plum": "#dda0dd",
    "burlywood": "#deb887",
    "lightcyan": "#e0ffff",
    "lavender": "#e6e6fa",
    "darksalmon": "#e9967a",
    "violet": "#ee82ee",
    "palegoldenrod": "#eee8aa",
    "lightcoral": "#f08080",
    "khaki": "#f0e68c",
    "aliceblue": "#f0f8ff",
    "honeydew": "#f0fff0",
    "azure": "#f0ffff",
    "sandybrown": "#f4a460",
    "wheat": "#f5deb3",
    "beige": "#f5f5dc",
    "whitesmoke": "#f5f5f5",
    "mintcream": "#f5fffa",
    "ghostwhite": "#f8f8ff",
    "salmon": "#fa8072",
    "antiquewhite": "#faebd7",
    "linen": "#faf0e6",
    "lightgoldenrodyellow": "#fafad2",
    "oldlace": "#fdf5e6",
    "red": "#ff0000",
    "fuchsia": "#ff00ff",
    "magenta": "#ff00ff",
    "deeppink": "#ff1493",
    "orangered": "#ff4500",
    "tomato": "#ff6347",
    "hotpink": "#ff69b4",
    "coral": "#ff7f50",
    "darkorange": "#ff8c00",
    "lightsalmon": "#ffa07a",
    "orange": "#ffa500",
    "lightpink": "#ffb6c1",
    "pink": "#ffc0cb",
    "gold": "#ffd700",
    "peachpuff": "#ffdab9",
    "navajowhite": "#ffdead",
    "moccasin": "#ffe4b5",
    "bisque": "#ffe4c4",
    "mistyrose": "#ffe4e1",
    "blanchedalmond": "#ffebcd",
    "papayawhip": "#ffefd5",
    "lavenderblush": "#fff0f5",
    "seashell": "#fff5ee",
    "cornsilk": "#fff8dc",
    "lemonchiffon": "#fffacd",
    "floralwhite": "#fffaf0",
    "snow": "#fffafa",
    "yellow": "#ffff00",
    "lightyellow": "#ffffe0",
    "ivory": "#fffff0",
    "white": "#ffffff",
}

# 18xx colors from https://github.com/XeryusTC/map18xx/blob/master/src/tile.rs
COLORS_18XX = {
    "18xx_ground": "#fdd9b5",  # sandy tan
    "18xx_yellow": "#fdee00",  # aureolin
    "18xx_green": "#00a550",  # pigment green
    "18xx_russet": "#cd7f32",  # bronze
    "18xx_grey": "#acacac",  # silver chalice
    "18xx_brown": "#7b3f00",  # chocolate
    "18xx_red": "#dc143c",  # crimson
    "18xx_blue": "#007fff",  # azure
    "18xx_barrier": "#660000",  # blood red
    "18xx_white": "#ffffff",  # white
}

BUILT_IN_FONTS = [
    "helv",
    "Helvetica",
    "heit",
    "Helvetica-Oblique",
    "hebo",
    "Helvetica-Bold",
    "hebi",
    "Helvetica-BoldOblique",
    "cour",
    "Courier",
    "coit",
    "Courier-Oblique",
    "cobo",
    "Courier-Bold",
    "cobi",
    "Courier-BoldOblique",
    "tiro",
    "Times-Roman",
    "tiit",
    "Times-Italic",
    "tibo",
    "Times-Bold",
    "tibi",
    "Times-BoldItalic",
    "symb",
    "Symbol",
    "zadb",
    "ZapfDingbats",
]

STANDARD_CARD_SIZES = {  # width/height
    "bridge": {"mm": (57.2, 88.9), "in": (2.25, 3.5), "pt": (162, 252)},
    "business": {"mm": (88.9, 50.8), "in": (3.5, 2), "pt": (252, 144)},
    "mtg": {"mm": (63.5, 88.9), "in": (2.5, 3.5), "pt": (180, 252)},  # poker
    "mini": {"mm": (44.5, 63.5), "in": (1.75, 2.5), "pt": (126, 180)},
    "minieuropean": {
        "mm": (44.0, 67.0),
        "in": (1.732, 2.638),
        "pt": (124.724, 189.921),
    },
    "miniamerican": {"mm": (41.0, 63.0), "in": (1.51, 2.48), "pt": (116.22, 178.583)},
    "poker": {"mm": (63.5, 88.9), "in": (2.5, 3.5), "pt": (180, 252)},
    "skat": {"mm": (58.9, 90.7), "in": (2.32, 3.58), "pt": (166.96, 257.1)},
    "tarot": {"mm": (69.9, 120.7), "in": (2.75, 4.75), "pt": (198, 342)},
}

PAPER_SIZES = {
    "4A0": {"mm": (1682, 2378), "pt": (4768, 6741)},
    "2A0": {"mm": (1189, 1682), "pt": (3370, 4768)},
    "A0": {"mm": (841, 1189), "pt": (2384, 3370)},
    "A1": {"mm": (594, 841), "pt": (1684, 2384)},
    "A2": {"mm": (420, 594), "pt": (1191, 1684)},
    "A3": {"mm": (297, 420), "pt": (842, 1191)},
    "A4": {"mm": (210, 297), "pt": (595, 842), "in": (8.27, 11.69)},
    "A5": {"mm": (148, 210), "pt": (420, 595)},
    "A6": {"mm": (105, 148), "pt": (298, 420)},
    "A7": {"mm": (74, 105), "pt": (210, 298)},
    "A8": {"mm": (52, 74), "pt": (147, 210)},
    "A9": {"mm": (37, 52), "pt": (105, 147)},
    "A10": {"mm": (26, 37), "pt": (74, 105)},
    "B0": {"mm": (1000, 1414), "pt": (2835, 4008)},
    "B1": {"mm": (707, 1000), "pt": (2004, 2835)},
    "B2": {"mm": (500, 707), "pt": (1417, 2004)},
    "B3": {"mm": (353, 500), "pt": (1001, 1417)},
    "B4": {"mm": (250, 353), "pt": (709, 1001)},
    "B5": {"mm": (176, 250), "pt": (499, 709)},
    "B6": {"mm": (125, 176), "pt": (354, 499)},
    "B7": {"mm": (88, 125), "pt": (249, 354)},
    "B8": {"mm": (62, 88), "pt": (176, 249)},
    "B9": {"mm": (44, 62), "pt": (125, 176)},
    "B10": {"mm": (31, 44), "pt": (88, 125)},
    "C0": {"mm": (917, 1297), "pt": (2599, 3677)},
    "C1": {"mm": (648, 917), "pt": (1837, 2599)},
    "C2": {"mm": (458, 648), "pt": (1298, 1837)},
    "C3": {"mm": (324, 458), "pt": (918, 1298)},
    "C4": {"mm": (229, 324), "pt": (649, 918)},
    "C5": {"mm": (162, 229), "pt": (459, 649)},
    "C6": {"mm": (114, 162), "pt": (323, 459)},
    "C7": {"mm": (81, 114), "pt": (230, 323)},
    "C8": {"mm": (57, 81), "pt": (162, 230)},
    "C9": {"mm": (40, 57), "pt": (113, 162)},
    "C10": {"mm": (28, 40), "pt": (79, 113)},
    "Letter": {"mm": (215.9, 279.4), "pt": (612, 792), "in": (8.5, 11)},
    "Tabloid": {"mm": (279.4, 431.8), "pt": (792, 1224), "in": (11, 17)},
    "Ledger": {"mm": (431.8, 279.4), "pt": (1224, 792), "in": (17, 11)},
    "Legal": {"mm": (215.9, 355.6), "pt": (612, 1008), "in": (8.5, 14)},
    "JuniorLegal": {"mm": (127, 203.2), "pt": (360, 576), "in": (5, 8)},
    "Statement": {"mm": (139.7, 215.9), "pt": (396, 612), "in": (5.5, 8.5)},
    "Executive": {"mm": (184.2, 266.7), "pt": (522, 756), "in": (7.25, 10.5)},
    "Folio": {"mm": (215.9, 330.2), "pt": (612, 936), "in": (8.5, 13)},
    "Quarto": {"mm": (228.6, 279.4), "pt": (648, 792), "in": (9, 11)},
    "BusinessCard": {"mm": (88.9, 50.8), "pt": (252, 144), "in": (3.5, 2)},
    "Notelet": {"mm": (95.3, 95.3), "pt": (270, 270), "in": (3.75, 3.75)},
}

LABELS_AVERY = [
    {
        "3363": {
            "id": "LP18/63",
            "shape": "rectangle",
            "number": 18,
            "width": 45.7,
            "height": 46.6,
        }
    },
    {
        "3421": {
            "id": "LP33/70S",
            "shape": "rectangle",
            "number": 33,
            "width": 70,
            "height": 25.4,
        }
    },
    {
        "3422^": {
            "id": "LP24/70S",
            "shape": "rectangle",
            "number": 24,
            "width": 70,
            "height": 35,
        }
    },
    {
        "3423^": {
            "id": "LP16/105S",
            "shape": "rectangle",
            "number": 16,
            "width": 105,
            "height": 35,
        }
    },
    {
        "3425^": {
            "id": "LP10/105S",
            "shape": "rectangle",
            "number": 10,
            "width": 105,
            "height": 57,
        }
    },
    {
        "3426^": {
            "id": "LP8/105S",
            "shape": "rectangle",
            "number": 8,
            "width": 105,
            "height": 70,
        }
    },
    {
        "3448": {
            "id": "LP24/70",
            "shape": "rectangle",
            "number": 24,
            "width": 70,
            "height": 37,
        }
    },
    {
        "3449": {
            "id": "LP24/70",
            "shape": "rectangle",
            "number": 24,
            "width": 70,
            "height": 37,
        }
    },
    {
        "3450": {
            "id": "LP24/70",
            "shape": "rectangle",
            "number": 24,
            "width": 70,
            "height": 37,
        }
    },
    {
        "3451": {
            "id": "LP24/70",
            "shape": "rectangle",
            "number": 24,
            "width": 70,
            "height": 37,
        }
    },
    {
        "3452": {
            "id": "LP16/105",
            "shape": "rectangle",
            "number": 16,
            "width": 105,
            "height": 37,
        }
    },
    {
        "3453": {
            "id": "LP16/105",
            "shape": "rectangle",
            "number": 16,
            "width": 105,
            "height": 37,
        }
    },
    {
        "3454": {
            "id": "LP16/105",
            "shape": "rectangle",
            "number": 16,
            "width": 105,
            "height": 37,
        }
    },
    {
        "3455": {
            "id": "LP16/105",
            "shape": "rectangle",
            "number": 16,
            "width": 105,
            "height": 37,
        }
    },
    {
        "3456": {
            "id": "LP4/105",
            "shape": "rectangle",
            "number": 4,
            "width": 105,
            "height": 149,
        }
    },
    {
        "3457": {
            "id": "LP4/105",
            "shape": "rectangle",
            "number": 4,
            "width": 105,
            "height": 149,
        }
    },
    {
        "3458": {
            "id": "LP4/105",
            "shape": "rectangle",
            "number": 4,
            "width": 105,
            "height": 149,
        }
    },
    {
        "3459": {
            "id": "LP4/105",
            "shape": "rectangle",
            "number": 4,
            "width": 105,
            "height": 149,
        }
    },
    {
        "3470": {
            "id": "LP1/210H",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "3470": {
            "id": "LP1/210J",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "3470": {
            "id": "LP1/210V",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "3471": {
            "id": "LP1/210H",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "3471": {
            "id": "LP1/210J",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "3471": {
            "id": "LP1/210V",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "3472": {
            "id": "LP1/210H",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "3472": {
            "id": "LP1/210J",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "3472": {
            "id": "LP1/210V",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "3473": {
            "id": "LP1/210H",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "3473": {
            "id": "LP1/210J",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "3473": {
            "id": "LP1/210V",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "3474": {
            "id": "LP24/70",
            "shape": "rectangle",
            "number": 24,
            "width": 70,
            "height": 37,
        }
    },
    {
        "3475": {
            "id": "LP24/70SS",
            "shape": "rectangle",
            "number": 24,
            "width": 70,
            "height": 36,
        }
    },
    {
        "3478": {
            "id": "LP1/210H",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "3478": {
            "id": "LP1/210J",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "3478": {
            "id": "LP1/210V",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "3483": {
            "id": "LP4/105",
            "shape": "rectangle",
            "number": 4,
            "width": 105,
            "height": 149,
        }
    },
    {
        "3484": {
            "id": "LP16/105",
            "shape": "rectangle",
            "number": 16,
            "width": 105,
            "height": 37,
        }
    },
    {
        "3489": {
            "id": "LP30/70",
            "shape": "rectangle",
            "number": 30,
            "width": 70,
            "height": 30,
        }
    },
    {
        "3490": {
            "id": "LP24/70SS",
            "shape": "rectangle",
            "number": 24,
            "width": 70,
            "height": 36,
        }
    },
    {
        "3652": {
            "id": "LP21/70",
            "shape": "rectangle",
            "number": 21,
            "width": 70,
            "height": 42.4,
        }
    },
    {
        "3653": {
            "id": "LP14/105",
            "shape": "rectangle",
            "number": 14,
            "width": 105,
            "height": 42.5,
        }
    },
    {
        "3655": {
            "id": "LP2/210",
            "shape": "rectangle",
            "number": 2,
            "width": 210,
            "height": 149,
        }
    },
    {
        "3668": {
            "id": "LP56/52",
            "shape": "rectangle",
            "number": 56,
            "width": 52.5,
            "height": 21.3,
        }
    },
    {
        "3669^": {
            "id": "LP15/70S",
            "shape": "rectangle",
            "number": 15,
            "width": 70,
            "height": 50,
        }
    },
    {
        "6070": {
            "id": "LP4/99",
            "shape": "rectangle",
            "number": 4,
            "width": 99.1,
            "height": 139,
        }
    },
    {
        "6071": {
            "id": "LP4/99",
            "shape": "rectangle",
            "number": 4,
            "width": 99.1,
            "height": 139,
        }
    },
    {
        "6072": {
            "id": "LP4/99",
            "shape": "rectangle",
            "number": 4,
            "width": 99.1,
            "height": 139,
        }
    },
    {
        "6073": {
            "id": "LP4/99",
            "shape": "rectangle",
            "number": 4,
            "width": 99.1,
            "height": 139,
        }
    },
    {
        "6093": {
            "id": "LP4/105",
            "shape": "rectangle",
            "number": 4,
            "width": 105,
            "height": 149,
        }
    },
    {
        "6094": {
            "id": "LP1/210H",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "6094": {
            "id": "LP1/210J",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "6094": {
            "id": "LP1/210V",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "6102": {
            "id": "LP48/45",
            "shape": "rectangle",
            "number": 48,
            "width": 45.7,
            "height": 21.2,
        }
    },
    {
        "6104": {
            "id": "LP27/63",
            "shape": "rectangle",
            "number": 27,
            "width": 45.7,
            "height": 29.6,
        }
    },
    {
        "6110": {
            "id": "LP1/210H",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "6110": {
            "id": "LP1/210J",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "6110": {
            "id": "LP1/210V",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "6119": {
            "id": "LP1/210H",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "6119": {
            "id": "LP1/210J",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "6119": {
            "id": "LP1/210V",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "6120": {
            "id": "LP4/105",
            "shape": "rectangle",
            "number": 4,
            "width": 105,
            "height": 149,
        }
    },
    {
        "6122": {
            "id": "LP24/70SS",
            "shape": "rectangle",
            "number": 24,
            "width": 70,
            "height": 36,
        }
    },
    {
        "6124": {
            "id": "LP4/105",
            "shape": "rectangle",
            "number": 4,
            "width": 105,
            "height": 149,
        }
    },
    {
        "6125": {
            "id": "LP1/210H",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "6125": {
            "id": "LP1/210J",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "6125": {
            "id": "LP1/210V",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "6174": {
            "id": "LP21/70",
            "shape": "rectangle",
            "number": 21,
            "width": 70,
            "height": 42.4,
        }
    },
    {
        "6176": {
            "id": "LP2/210",
            "shape": "rectangle",
            "number": 2,
            "width": 210,
            "height": 149,
        }
    },
    {
        "AB1900": {
            "id": "LPCD117",
            "shape": "circle",
            "number": 2,
            "width": 117,
            "height": 117,
        }
    },
    {
        "AB7000": {
            "id": "LPCD117",
            "shape": "circle",
            "number": 2,
            "width": 117,
            "height": 117,
        }
    },
    {
        "C2160": {
            "id": "LP21/63",
            "shape": "rectangle",
            "number": 21,
            "width": 45.7,
            "height": 38.1,
        }
    },
    {
        "C2244^": {
            "id": "LP6/72R",
            "shape": "circle",
            "number": 6,
            "width": 72,
            "height": 72,
        }
    },
    {
        "C2246": {
            "id": "LP1/210H",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "C2246": {
            "id": "LP1/210J",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "C2246": {
            "id": "LP1/210V",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "C2651": {
            "id": "LP65/38",
            "shape": "rectangle",
            "number": 65,
            "width": 38.1,
            "height": 21.2,
        }
    },
    {
        "C4167": {
            "id": "LP1/199",
            "shape": "rectangle",
            "number": 1,
            "width": 199.6,
            "height": 289.1,
        }
    },
    {
        "C6074": {
            "id": "LPCD117",
            "shape": "circle",
            "number": 2,
            "width": 117,
            "height": 117,
        }
    },
    {
        "C9169": {
            "id": "LP4/99",
            "shape": "rectangle",
            "number": 4,
            "width": 99.1,
            "height": 139,
        }
    },
    {
        "C9660": {
            "id": "LPCD117",
            "shape": "circle",
            "number": 2,
            "width": 117,
            "height": 117,
        }
    },
    {
        "C9780": {
            "id": "LPCD117",
            "shape": "circle",
            "number": 2,
            "width": 117,
            "height": 117,
        }
    },
    {
        "CL7059": {
            "id": "LP24/63",
            "shape": "rectangle",
            "number": 24,
            "width": 45.7,
            "height": 33.9,
        }
    },
    {
        "CL7069": {
            "id": "LP4/99",
            "shape": "rectangle",
            "number": 4,
            "width": 99.1,
            "height": 139,
        }
    },
    {
        "DL01": {
            "id": "LP1/210H",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "DL01": {
            "id": "LP1/210J",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "DL01": {
            "id": "LP1/210V",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "DL04": {
            "id": "LP4/105",
            "shape": "rectangle",
            "number": 4,
            "width": 105,
            "height": 149,
        }
    },
    {
        "DL08": {
            "id": "LP8/105",
            "shape": "rectangle",
            "number": 8,
            "width": 105,
            "height": 74.2,
        }
    },
    {
        "DL16": {
            "id": "LP16/105",
            "shape": "rectangle",
            "number": 16,
            "width": 105,
            "height": 37,
        }
    },
    {
        "DL24^": {
            "id": "LP24/70S",
            "shape": "rectangle",
            "number": 24,
            "width": 70,
            "height": 35,
        }
    },
    {
        "DL24NZ": {
            "id": "LP24/70",
            "shape": "rectangle",
            "number": 24,
            "width": 70,
            "height": 37,
        }
    },
    {
        "DPS01": {
            "id": "LP1/210J",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "DPS02": {
            "id": "LP1/210V",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "DPS02": {
            "id": "LP2/210",
            "shape": "rectangle",
            "number": 2,
            "width": 210,
            "height": 149,
        }
    },
    {
        "DPS02": {
            "id": "LP2/210",
            "shape": "rectangle",
            "number": 2,
            "width": 210,
            "height": 149,
        }
    },
    {
        "DPS03": {
            "id": "LP1/210H",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "DPS08": {
            "id": "LP8/105S",
            "shape": "rectangle",
            "number": 8,
            "width": 105,
            "height": 71,
        }
    },
    {
        "DPS10": {
            "id": "LP10/105",
            "shape": "rectangle",
            "number": 10,
            "width": 105,
            "height": 59.6,
        }
    },
    {
        "DPS16": {
            "id": "LP16/105",
            "shape": "rectangle",
            "number": 16,
            "width": 105,
            "height": 37,
        }
    },
    {
        "DPS24": {
            "id": "LP24/70SS",
            "shape": "rectangle",
            "number": 24,
            "width": 70,
            "height": 36,
        }
    },
    {
        "DPS30": {
            "id": "LP30/70",
            "shape": "rectangle",
            "number": 30,
            "width": 70,
            "height": 30,
        }
    },
    {
        "DPSO4": {
            "id": "LP4/105",
            "shape": "rectangle",
            "number": 4,
            "width": 105,
            "height": 149,
        }
    },
    {
        "E3210": {
            "id": "LP189/25",
            "shape": "rectangle",
            "number": 189,
            "width": 25.4,
            "height": 10,
        }
    },
    {
        "E3211": {
            "id": "LP65/38",
            "shape": "rectangle",
            "number": 65,
            "width": 38.1,
            "height": 21.2,
        }
    },
    {
        "E3212": {
            "id": "LP14/99",
            "shape": "rectangle",
            "number": 14,
            "width": 99.1,
            "height": 38.1,
        }
    },
    {
        "E3230": {
            "id": "LP24/63",
            "shape": "rectangle",
            "number": 24,
            "width": 45.7,
            "height": 33.9,
        }
    },
    {
        "E3410": {
            "id": "LP4/99",
            "shape": "rectangle",
            "number": 4,
            "width": 99.1,
            "height": 139,
        }
    },
    {
        "E3411": {
            "id": "LP2/195OV",
            "shape": "oval",
            "number": 2,
            "width": 195,
            "height": 139,
        }
    },
    {
        "E3411": {
            "id": "LP2/199",
            "shape": "rectangle",
            "number": 2,
            "width": 199.6,
            "height": 143.5,
        }
    },
    {
        "J2356": {
            "id": "LP1/210H",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "J2356": {
            "id": "LP1/210J",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "J2356": {
            "id": "LP1/210V",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "J4720": {
            "id": "LP48/45",
            "shape": "rectangle",
            "number": 48,
            "width": 45.7,
            "height": 21.2,
        }
    },
    {
        "J4721": {
            "id": "LP27/63",
            "shape": "rectangle",
            "number": 27,
            "width": 45.7,
            "height": 29.6,
        }
    },
    {
        "J4722": {
            "id": "LP10/96",
            "shape": "rectangle",
            "number": 10,
            "width": 96,
            "height": 50.8,
        }
    },
    {
        "J4773": {
            "id": "LP24/63",
            "shape": "rectangle",
            "number": 24,
            "width": 45.7,
            "height": 33.9,
        }
    },
    {
        "J4774": {
            "id": "LP4/99",
            "shape": "rectangle",
            "number": 4,
            "width": 99.1,
            "height": 139,
        }
    },
    {
        "J4775": {
            "id": "LP1/210H",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "J4775": {
            "id": "LP1/210J",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "J4775": {
            "id": "LP1/210V",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "J4776": {
            "id": "LP1/199",
            "shape": "rectangle",
            "number": 1,
            "width": 199.6,
            "height": 289.1,
        }
    },
    {
        "J4791": {
            "id": "LP48/45",
            "shape": "rectangle",
            "number": 48,
            "width": 45.7,
            "height": 21.2,
        }
    },
    {
        "J4792": {
            "id": "LP27/63",
            "shape": "rectangle",
            "number": 27,
            "width": 45.7,
            "height": 29.6,
        }
    },
    {
        "J5101": {
            "id": "LP20/38",
            "shape": "rectangle",
            "number": 20,
            "width": 38,
            "height": 69,
        }
    },
    {
        "J5102": {
            "id": "LP14/63",
            "shape": "rectangle",
            "number": 14,
            "width": 63.5,
            "height": 38,
        }
    },
    {
        "J5103": {
            "id": "LP10/38",
            "shape": "rectangle",
            "number": 10,
            "width": 38,
            "height": 135,
        }
    },
    {
        "J6115": {
            "id": "LPCD117",
            "shape": "circle",
            "number": 2,
            "width": 117,
            "height": 117,
        }
    },
    {
        "J8159": {
            "id": "LP24/63",
            "shape": "rectangle",
            "number": 24,
            "width": 45.7,
            "height": 33.9,
        }
    },
    {
        "J8160": {
            "id": "LP21/63",
            "shape": "rectangle",
            "number": 21,
            "width": 45.7,
            "height": 38.1,
        }
    },
    {
        "J8161": {
            "id": "LP18/63",
            "shape": "rectangle",
            "number": 18,
            "width": 45.7,
            "height": 46.6,
        }
    },
    {
        "J8162": {
            "id": "LP16/99",
            "shape": "rectangle",
            "number": 16,
            "width": 99.1,
            "height": 34,
        }
    },
    {
        "J8163": {
            "id": "LP14/99",
            "shape": "rectangle",
            "number": 14,
            "width": 99.1,
            "height": 38.1,
        }
    },
    {
        "J8164": {
            "id": "LP12/63",
            "shape": "rectangle",
            "number": 12,
            "width": 45.7,
            "height": 72,
        }
    },
    {
        "J8165": {
            "id": "LP8/90OV",
            "shape": "oval",
            "number": 8,
            "width": 90,
            "height": 62,
        }
    },
    {
        "J8165": {
            "id": "LP8/99",
            "shape": "rectangle",
            "number": 8,
            "width": 99.1,
            "height": 67.7,
        }
    },
    {
        "J8166": {
            "id": "LP6/99",
            "shape": "rectangle",
            "number": 6,
            "width": 99.1,
            "height": 93.1,
        }
    },
    {
        "J8167": {
            "id": "LP1/199",
            "shape": "rectangle",
            "number": 1,
            "width": 199.6,
            "height": 289.1,
        }
    },
    {
        "J8168": {
            "id": "LP2/195OV",
            "shape": "oval",
            "number": 2,
            "width": 195,
            "height": 139,
        }
    },
    {
        "J8168": {
            "id": "LP2/199",
            "shape": "rectangle",
            "number": 2,
            "width": 199.6,
            "height": 143.5,
        }
    },
    {
        "J8169": {
            "id": "LP4/99",
            "shape": "rectangle",
            "number": 4,
            "width": 99.1,
            "height": 139,
        }
    },
    {
        "J8170": {
            "id": "LP24/134",
            "shape": "rectangle",
            "number": 24,
            "width": 134,
            "height": 11,
        }
    },
    {
        "J8171": {
            "id": "LP4/200",
            "shape": "rectangle",
            "number": 4,
            "width": 200,
            "height": 60,
        }
    },
    {
        "J8172": {
            "id": "LP18/100",
            "shape": "rectangle",
            "number": 18,
            "width": 100,
            "height": 30,
        }
    },
    {
        "J8173": {
            "id": "LP10/95OV",
            "shape": "oval",
            "number": 10,
            "width": 95,
            "height": 53,
        }
    },
    {
        "J8173": {
            "id": "LP10/99",
            "shape": "rectangle",
            "number": 10,
            "width": 99.1,
            "height": 57,
        }
    },
    {
        "J8177": {
            "id": "LP12/99",
            "shape": "rectangle",
            "number": 12,
            "width": 99.1,
            "height": 42.3,
        }
    },
    {
        "J8359": {
            "id": "LP24/63",
            "shape": "rectangle",
            "number": 24,
            "width": 45.7,
            "height": 33.9,
        }
    },
    {
        "J8360": {
            "id": "LP21/63",
            "shape": "rectangle",
            "number": 21,
            "width": 45.7,
            "height": 38.1,
        }
    },
    {
        "J8361": {
            "id": "LP18/63",
            "shape": "rectangle",
            "number": 18,
            "width": 45.7,
            "height": 46.6,
        }
    },
    {
        "J8362": {
            "id": "LP16/99",
            "shape": "rectangle",
            "number": 16,
            "width": 99.1,
            "height": 34,
        }
    },
    {
        "J8363": {
            "id": "LP14/99",
            "shape": "rectangle",
            "number": 14,
            "width": 99.1,
            "height": 38.1,
        }
    },
    {
        "J8364": {
            "id": "LP12/63",
            "shape": "rectangle",
            "number": 12,
            "width": 45.7,
            "height": 72,
        }
    },
    {
        "J8365": {
            "id": "LP8/90OV",
            "shape": "oval",
            "number": 8,
            "width": 90,
            "height": 62,
        }
    },
    {
        "J8365": {
            "id": "LP8/99",
            "shape": "rectangle",
            "number": 8,
            "width": 99.1,
            "height": 67.7,
        }
    },
    {
        "J8366": {
            "id": "LP6/99",
            "shape": "rectangle",
            "number": 6,
            "width": 99.1,
            "height": 93.1,
        }
    },
    {
        "J8367": {
            "id": "LP1/199",
            "shape": "rectangle",
            "number": 1,
            "width": 199.6,
            "height": 289.1,
        }
    },
    {
        "J8368": {
            "id": "LP2/195OV",
            "shape": "oval",
            "number": 2,
            "width": 195,
            "height": 139,
        }
    },
    {
        "J8368": {
            "id": "LP2/199",
            "shape": "rectangle",
            "number": 2,
            "width": 199.6,
            "height": 143.5,
        }
    },
    {
        "J8369": {
            "id": "LP4/99",
            "shape": "rectangle",
            "number": 4,
            "width": 99.1,
            "height": 139,
        }
    },
    {
        "J8371": {
            "id": "LP4/200",
            "shape": "rectangle",
            "number": 4,
            "width": 200,
            "height": 60,
        }
    },
    {
        "J8551": {
            "id": "LP65/38",
            "shape": "rectangle",
            "number": 65,
            "width": 38.1,
            "height": 21.2,
        }
    },
    {
        "J8559": {
            "id": "LP24/63",
            "shape": "rectangle",
            "number": 24,
            "width": 45.7,
            "height": 33.9,
        }
    },
    {
        "J8560": {
            "id": "LP21/63",
            "shape": "rectangle",
            "number": 21,
            "width": 45.7,
            "height": 38.1,
        }
    },
    {
        "J8562": {
            "id": "LP16/99",
            "shape": "rectangle",
            "number": 16,
            "width": 99.1,
            "height": 34,
        }
    },
    {
        "J8563": {
            "id": "LP14/99",
            "shape": "rectangle",
            "number": 14,
            "width": 99.1,
            "height": 38.1,
        }
    },
    {
        "J8565": {
            "id": "LP8/90OV",
            "shape": "oval",
            "number": 8,
            "width": 90,
            "height": 62,
        }
    },
    {
        "J8565": {
            "id": "LP8/99",
            "shape": "rectangle",
            "number": 8,
            "width": 99.1,
            "height": 67.7,
        }
    },
    {
        "J8567": {
            "id": "LP1/210H",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "J8567": {
            "id": "LP1/210J",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "J8567": {
            "id": "LP1/210V",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "J8570": {
            "id": "LPCD117",
            "shape": "circle",
            "number": 2,
            "width": 117,
            "height": 117,
        }
    },
    {
        "J8587": {
            "id": "LP1/210H",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "J8587": {
            "id": "LP1/210J",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "J8587": {
            "id": "LP1/210V",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "J8651": {
            "id": "LP65/38",
            "shape": "rectangle",
            "number": 65,
            "width": 38.1,
            "height": 21.2,
        }
    },
    {
        "J8654": {
            "id": "LP40/45",
            "shape": "rectangle",
            "number": 40,
            "width": 45.7,
            "height": 25.4,
        }
    },
    {
        "J8655": {
            "id": "LP12/89",
            "shape": "round_rectangle",
            "number": 12,
            "width": 89,
            "height": 42,
        }
    },
    {
        "J8656": {
            "id": "LP84/46",
            "shape": "rectangle",
            "number": 84,
            "width": 46,
            "height": 11.1,
        }
    },
    {
        "J8657": {
            "id": "LP84/46",
            "shape": "rectangle",
            "number": 84,
            "width": 46,
            "height": 11.1,
        }
    },
    {
        "J8658": {
            "id": "LP189/25",
            "shape": "rectangle",
            "number": 189,
            "width": 25.4,
            "height": 10,
        }
    },
    {
        "J8659": {
            "id": "LP270/18",
            "shape": "rectangle",
            "number": 270,
            "width": 17.8,
            "height": 10,
        }
    },
    {
        "J8660": {
            "id": "LPCD116",
            "shape": "circle",
            "number": 2,
            "width": 116,
            "height": 116,
        }
    },
    {
        "J8666": {
            "id": "LP10/70",
            "shape": "rectangle",
            "number": 10,
            "width": 70,
            "height": 52,
        }
    },
    {
        "J8671": {
            "id": "LP12/76",
            "shape": "rectangle",
            "number": 12,
            "width": 76.2,
            "height": 46.4,
        }
    },
    {
        "J8674": {
            "id": "LP16/145",
            "shape": "rectangle",
            "number": 16,
            "width": 145,
            "height": 17,
        }
    },
    {
        "J8676": {
            "id": "LPCD117",
            "shape": "circle",
            "number": 2,
            "width": 117,
            "height": 117,
        }
    },
    {
        "J8743": {
            "id": "LPCD117",
            "shape": "circle",
            "number": 2,
            "width": 117,
            "height": 117,
        }
    },
    {
        "J8751": {
            "id": "LP65/38",
            "shape": "rectangle",
            "number": 65,
            "width": 38.1,
            "height": 21.2,
        }
    },
    {
        "J8756V": {
            "id": "LP84/46",
            "shape": "rectangle",
            "number": 84,
            "width": 46,
            "height": 11.1,
        }
    },
    {
        "J8766": {
            "id": "LP10/70",
            "shape": "rectangle",
            "number": 10,
            "width": 70,
            "height": 52,
        }
    },
    {
        "J8770": {
            "id": "LPCD117",
            "shape": "circle",
            "number": 2,
            "width": 117,
            "height": 117,
        }
    },
    {
        "J8771": {
            "id": "LP12/76",
            "shape": "rectangle",
            "number": 12,
            "width": 76.2,
            "height": 46.4,
        }
    },
    {
        "J8774": {
            "id": "LP16/145",
            "shape": "rectangle",
            "number": 16,
            "width": 145,
            "height": 17,
        }
    },
    {
        "J8776": {
            "id": "LPCD117",
            "shape": "circle",
            "number": 2,
            "width": 117,
            "height": 117,
        }
    },
    {
        "J8777": {
            "id": "LPCD117",
            "shape": "circle",
            "number": 2,
            "width": 117,
            "height": 117,
        }
    },
    {
        "J8778": {
            "id": "LPCD117",
            "shape": "circle",
            "number": 2,
            "width": 117,
            "height": 117,
        }
    },
    {
        "L3415": {
            "id": "LP24/40R",
            "shape": "circle",
            "number": 24,
            "width": 40,
            "height": 40,
        }
    },
    {
        "L4730": {
            "id": "LP270/18",
            "shape": "rectangle",
            "number": 270,
            "width": 17.8,
            "height": 10,
        }
    },
    {
        "L4731": {
            "id": "LP189/25",
            "shape": "rectangle",
            "number": 189,
            "width": 25.4,
            "height": 10,
        }
    },
    {
        "L4733": {
            "id": "LP4/99",
            "shape": "rectangle",
            "number": 4,
            "width": 99.1,
            "height": 139,
        }
    },
    {
        "L4734": {
            "id": "LP2/195OV",
            "shape": "oval",
            "number": 2,
            "width": 195,
            "height": 139,
        }
    },
    {
        "L4734": {
            "id": "LP2/199",
            "shape": "rectangle",
            "number": 2,
            "width": 199.6,
            "height": 143.5,
        }
    },
    {
        "L4735": {
            "id": "LP1/210H",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "L4735": {
            "id": "LP1/210J",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "L4735": {
            "id": "LP1/210V",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "L4736": {
            "id": "LP48/45",
            "shape": "rectangle",
            "number": 48,
            "width": 45.7,
            "height": 21.2,
        }
    },
    {
        "L4737": {
            "id": "LP27/63",
            "shape": "rectangle",
            "number": 27,
            "width": 45.7,
            "height": 29.6,
        }
    },
    {
        "L4743": {
            "id": "LP12/99",
            "shape": "rectangle",
            "number": 12,
            "width": 99.1,
            "height": 42.3,
        }
    },
    {
        "L4744": {
            "id": "LP10/96",
            "shape": "rectangle",
            "number": 10,
            "width": 96,
            "height": 50.8,
        }
    },
    {
        "L4760": {
            "id": "LP7/192",
            "shape": "rectangle",
            "number": 7,
            "width": 192,
            "height": 39,
        }
    },
    {
        "L4761": {
            "id": "LP4/192",
            "shape": "rectangle",
            "number": 4,
            "width": 192,
            "height": 62,
        }
    },
    {
        "L4762": {
            "id": "LP7/192",
            "shape": "rectangle",
            "number": 7,
            "width": 192,
            "height": 39,
        }
    },
    {
        "L4763": {
            "id": "LP7/192",
            "shape": "rectangle",
            "number": 7,
            "width": 192,
            "height": 39,
        }
    },
    {
        "L4764": {
            "id": "LP7/192",
            "shape": "rectangle",
            "number": 7,
            "width": 192,
            "height": 39,
        }
    },
    {
        "L4765": {
            "id": "LP7/192",
            "shape": "rectangle",
            "number": 7,
            "width": 192,
            "height": 39,
        }
    },
    {
        "L4770": {
            "id": "LP40/45",
            "shape": "rectangle",
            "number": 40,
            "width": 45.7,
            "height": 25.4,
        }
    },
    {
        "L4772": {
            "id": "LP12/99",
            "shape": "rectangle",
            "number": 12,
            "width": 99.1,
            "height": 42.3,
        }
    },
    {
        "L4773": {
            "id": "LP24/63",
            "shape": "rectangle",
            "number": 24,
            "width": 45.7,
            "height": 33.9,
        }
    },
    {
        "L4774": {
            "id": "LP4/99",
            "shape": "rectangle",
            "number": 4,
            "width": 99.1,
            "height": 139,
        }
    },
    {
        "L4775": {
            "id": "LP1/210H",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "L4775": {
            "id": "LP1/210J",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "L4775": {
            "id": "LP1/210V",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "L4776": {
            "id": "LP12/99",
            "shape": "rectangle",
            "number": 12,
            "width": 99.1,
            "height": 42.3,
        }
    },
    {
        "L4778": {
            "id": "LP48/45",
            "shape": "rectangle",
            "number": 48,
            "width": 45.7,
            "height": 21.2,
        }
    },
    {
        "L4784": {
            "id": "LP27/63",
            "shape": "rectangle",
            "number": 27,
            "width": 45.7,
            "height": 29.6,
        }
    },
    {
        "L4790": {
            "id": "LP65/38",
            "shape": "rectangle",
            "number": 65,
            "width": 38.1,
            "height": 21.2,
        }
    },
    {
        "L4791": {
            "id": "LP65/38",
            "shape": "rectangle",
            "number": 65,
            "width": 38.1,
            "height": 21.2,
        }
    },
    {
        "L4792": {
            "id": "LP65/38",
            "shape": "rectangle",
            "number": 65,
            "width": 38.1,
            "height": 21.2,
        }
    },
    {
        "L4793": {
            "id": "LP65/38",
            "shape": "rectangle",
            "number": 65,
            "width": 38.1,
            "height": 21.2,
        }
    },
    {
        "L5103": {
            "id": "LP10/38",
            "shape": "rectangle",
            "number": 10,
            "width": 38,
            "height": 135,
        }
    },
    {
        "L6003": {
            "id": "LP27/63",
            "shape": "rectangle",
            "number": 27,
            "width": 45.7,
            "height": 29.6,
        }
    },
    {
        "L6004": {
            "id": "LP27/63",
            "shape": "rectangle",
            "number": 27,
            "width": 45.7,
            "height": 29.6,
        }
    },
    {
        "L6005": {
            "id": "LP1/210H",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "L6005": {
            "id": "LP1/210J",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "L6005": {
            "id": "LP1/210V",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "L6006": {
            "id": "LP1/210H",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "L6006": {
            "id": "LP1/210J",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "L6006": {
            "id": "LP1/210V",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "L6007": {
            "id": "LP1/210H",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "L6007": {
            "id": "LP1/210J",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "L6007": {
            "id": "LP1/210V",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "L6008": {
            "id": "LP189/25",
            "shape": "rectangle",
            "number": 189,
            "width": 25.4,
            "height": 10,
        }
    },
    {
        "L6009": {
            "id": "LP48/45",
            "shape": "rectangle",
            "number": 48,
            "width": 45.7,
            "height": 21.2,
        }
    },
    {
        "L6011": {
            "id": "LP27/63",
            "shape": "rectangle",
            "number": 27,
            "width": 45.7,
            "height": 29.6,
        }
    },
    {
        "L6012": {
            "id": "LP10/96",
            "shape": "rectangle",
            "number": 10,
            "width": 96,
            "height": 50.8,
        }
    },
    {
        "L6013": {
            "id": "LP1/210H",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "L6013": {
            "id": "LP1/210J",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "L6013": {
            "id": "LP1/210V",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "L6015": {
            "id": "LPCD117",
            "shape": "circle",
            "number": 2,
            "width": 117,
            "height": 117,
        }
    },
    {
        "L6023": {
            "id": "LP21/63",
            "shape": "rectangle",
            "number": 21,
            "width": 45.7,
            "height": 38.1,
        }
    },
    {
        "L6025": {
            "id": "LP18/63",
            "shape": "rectangle",
            "number": 18,
            "width": 45.7,
            "height": 46.6,
        }
    },
    {
        "L6032": {
            "id": "LP24/63",
            "shape": "rectangle",
            "number": 24,
            "width": 45.7,
            "height": 33.9,
        }
    },
    {
        "L6033": {
            "id": "LP24/63",
            "shape": "rectangle",
            "number": 24,
            "width": 45.7,
            "height": 33.9,
        }
    },
    {
        "L6034": {
            "id": "LP24/63",
            "shape": "rectangle",
            "number": 24,
            "width": 45.7,
            "height": 33.9,
        }
    },
    {
        "L6035": {
            "id": "LP24/63",
            "shape": "rectangle",
            "number": 24,
            "width": 45.7,
            "height": 33.9,
        }
    },
    {
        "L6036": {
            "id": "LP189/25",
            "shape": "rectangle",
            "number": 189,
            "width": 25.4,
            "height": 10,
        }
    },
    {
        "L6037": {
            "id": "LP189/25",
            "shape": "rectangle",
            "number": 189,
            "width": 25.4,
            "height": 10,
        }
    },
    {
        "L6038": {
            "id": "LP48/45",
            "shape": "rectangle",
            "number": 48,
            "width": 45.7,
            "height": 21.2,
        }
    },
    {
        "L6039": {
            "id": "LP48/45",
            "shape": "rectangle",
            "number": 48,
            "width": 45.7,
            "height": 21.2,
        }
    },
    {
        "L6040": {
            "id": "LP48/45",
            "shape": "rectangle",
            "number": 48,
            "width": 45.7,
            "height": 21.2,
        }
    },
    {
        "L6041": {
            "id": "LP48/45",
            "shape": "rectangle",
            "number": 48,
            "width": 45.7,
            "height": 21.2,
        }
    },
    {
        "L6043": {
            "id": "LPCD117",
            "shape": "circle",
            "number": 2,
            "width": 117,
            "height": 117,
        }
    },
    {
        "L6044": {
            "id": "LPCD117",
            "shape": "circle",
            "number": 2,
            "width": 117,
            "height": 117,
        }
    },
    {
        "L6045": {
            "id": "LPCD117",
            "shape": "circle",
            "number": 2,
            "width": 117,
            "height": 117,
        }
    },
    {
        "L6046": {
            "id": "LPCD117",
            "shape": "circle",
            "number": 2,
            "width": 117,
            "height": 117,
        }
    },
    {
        "L6047": {
            "id": "LPCD117",
            "shape": "circle",
            "number": 2,
            "width": 117,
            "height": 117,
        }
    },
    {
        "L6048": {
            "id": "LP189/25",
            "shape": "rectangle",
            "number": 189,
            "width": 25.4,
            "height": 10,
        }
    },
    {
        "L6049": {
            "id": "LP189/25",
            "shape": "rectangle",
            "number": 189,
            "width": 25.4,
            "height": 10,
        }
    },
    {
        "L6050": {
            "id": "LP2/195OV",
            "shape": "oval",
            "number": 2,
            "width": 195,
            "height": 139,
        }
    },
    {
        "L6050": {
            "id": "LP2/199",
            "shape": "rectangle",
            "number": 2,
            "width": 199.6,
            "height": 143.5,
        }
    },
    {
        "L6051": {
            "id": "LP2/195OV",
            "shape": "oval",
            "number": 2,
            "width": 195,
            "height": 139,
        }
    },
    {
        "L6051": {
            "id": "LP2/199",
            "shape": "rectangle",
            "number": 2,
            "width": 199.6,
            "height": 143.5,
        }
    },
    {
        "L6052": {
            "id": "LP2/195OV",
            "shape": "oval",
            "number": 2,
            "width": 195,
            "height": 139,
        }
    },
    {
        "L6052": {
            "id": "LP2/199",
            "shape": "rectangle",
            "number": 2,
            "width": 199.6,
            "height": 143.5,
        }
    },
    {
        "L6053": {
            "id": "LP2/195OV",
            "shape": "oval",
            "number": 2,
            "width": 195,
            "height": 139,
        }
    },
    {
        "L6053": {
            "id": "LP2/199",
            "shape": "rectangle",
            "number": 2,
            "width": 199.6,
            "height": 143.5,
        }
    },
    {
        "L6054": {
            "id": "LP14/99",
            "shape": "rectangle",
            "number": 14,
            "width": 99.1,
            "height": 38.1,
        }
    },
    {
        "L6055": {
            "id": "LP14/99",
            "shape": "rectangle",
            "number": 14,
            "width": 99.1,
            "height": 38.1,
        }
    },
    {
        "L6056": {
            "id": "LP14/99",
            "shape": "rectangle",
            "number": 14,
            "width": 99.1,
            "height": 38.1,
        }
    },
    {
        "L6057": {
            "id": "LP14/99",
            "shape": "rectangle",
            "number": 14,
            "width": 99.1,
            "height": 38.1,
        }
    },
    {
        "L6103": {
            "id": "LP48/45",
            "shape": "rectangle",
            "number": 48,
            "width": 45.7,
            "height": 21.2,
        }
    },
    {
        "L6105": {
            "id": "LP27/63",
            "shape": "rectangle",
            "number": 27,
            "width": 45.7,
            "height": 29.6,
        }
    },
    {
        "L6111": {
            "id": "LP1/210H",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "L6111": {
            "id": "LP1/210J",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "L6111": {
            "id": "LP1/210V",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "L6112": {
            "id": "LP24/40R",
            "shape": "circle",
            "number": 24,
            "width": 40,
            "height": 40,
        }
    },
    {
        "L6113": {
            "id": "LP48/45",
            "shape": "rectangle",
            "number": 48,
            "width": 45.7,
            "height": 21.2,
        }
    },
    {
        "L6114": {
            "id": "LP27/63",
            "shape": "rectangle",
            "number": 27,
            "width": 45.7,
            "height": 29.6,
        }
    },
    {
        "L6117": {
            "id": "LPCD117",
            "shape": "circle",
            "number": 2,
            "width": 117,
            "height": 117,
        }
    },
    {
        "L6140": {
            "id": "LP40/45",
            "shape": "rectangle",
            "number": 40,
            "width": 45.7,
            "height": 25.4,
        }
    },
    {
        "L6141": {
            "id": "LP24/63",
            "shape": "rectangle",
            "number": 24,
            "width": 45.7,
            "height": 33.9,
        }
    },
    {
        "L6145": {
            "id": "LP40/45",
            "shape": "rectangle",
            "number": 40,
            "width": 45.7,
            "height": 25.4,
        }
    },
    {
        "L6146": {
            "id": "LP24/63",
            "shape": "rectangle",
            "number": 24,
            "width": 45.7,
            "height": 33.9,
        }
    },
    {
        "L7051": {
            "id": "LP65/38",
            "shape": "rectangle",
            "number": 65,
            "width": 38.1,
            "height": 21.2,
        }
    },
    {
        "L7060": {
            "id": "LP21/63",
            "shape": "rectangle",
            "number": 21,
            "width": 45.7,
            "height": 38.1,
        }
    },
    {
        "L7063": {
            "id": "LP14/99",
            "shape": "rectangle",
            "number": 14,
            "width": 99.1,
            "height": 38.1,
        }
    },
    {
        "L7065": {
            "id": "LP65/38",
            "shape": "rectangle",
            "number": 65,
            "width": 38.1,
            "height": 21.2,
        }
    },
    {
        "L7068": {
            "id": "LP2/195OV",
            "shape": "oval",
            "number": 2,
            "width": 195,
            "height": 139,
        }
    },
    {
        "L7068": {
            "id": "LP2/199",
            "shape": "rectangle",
            "number": 2,
            "width": 199.6,
            "height": 143.5,
        }
    },
    {
        "L7069": {
            "id": "LP4/99",
            "shape": "rectangle",
            "number": 4,
            "width": 99.1,
            "height": 139,
        }
    },
    {
        "L7074": {
            "id": "LP1/199",
            "shape": "rectangle",
            "number": 1,
            "width": 199.6,
            "height": 289.1,
        }
    },
    {
        "L7077": {
            "id": "LP1/199",
            "shape": "rectangle",
            "number": 1,
            "width": 199.6,
            "height": 289.1,
        }
    },
    {
        "L7084": {
            "id": "LP84/46",
            "shape": "rectangle",
            "number": 84,
            "width": 46,
            "height": 11.1,
        }
    },
    {
        "L7102": {
            "id": "LP7/192",
            "shape": "rectangle",
            "number": 7,
            "width": 192,
            "height": 39,
        }
    },
    {
        "L7159": {
            "id": "LP24/63",
            "shape": "rectangle",
            "number": 24,
            "width": 45.7,
            "height": 33.9,
        }
    },
    {
        "L7159X": {
            "id": "LP24/63",
            "shape": "rectangle",
            "number": 24,
            "width": 45.7,
            "height": 33.9,
        }
    },
    {
        "L7160": {
            "id": "LP21/63",
            "shape": "rectangle",
            "number": 21,
            "width": 45.7,
            "height": 38.1,
        }
    },
    {
        "L7160X": {
            "id": "LP21/63",
            "shape": "rectangle",
            "number": 21,
            "width": 45.7,
            "height": 38.1,
        }
    },
    {
        "L7161": {
            "id": "LP18/63",
            "shape": "rectangle",
            "number": 18,
            "width": 45.7,
            "height": 46.6,
        }
    },
    {
        "L7161X": {
            "id": "LP18/63",
            "shape": "rectangle",
            "number": 18,
            "width": 45.7,
            "height": 46.6,
        }
    },
    {
        "L7162": {
            "id": "LP16/99",
            "shape": "rectangle",
            "number": 16,
            "width": 99.1,
            "height": 34,
        }
    },
    {
        "L7162X": {
            "id": "LP16/99",
            "shape": "rectangle",
            "number": 16,
            "width": 99.1,
            "height": 34,
        }
    },
    {
        "L7163B": {
            "id": "LP14/99",
            "shape": "rectangle",
            "number": 14,
            "width": 99.1,
            "height": 38.1,
        }
    },
    {
        "L7163": {
            "id": "LP14/99",
            "shape": "rectangle",
            "number": 14,
            "width": 99.1,
            "height": 38.1,
        }
    },
    {
        "L7163R": {
            "id": "LP14/99",
            "shape": "rectangle",
            "number": 14,
            "width": 99.1,
            "height": 38.1,
        }
    },
    {
        "L7163X": {
            "id": "LP14/99",
            "shape": "rectangle",
            "number": 14,
            "width": 99.1,
            "height": 38.1,
        }
    },
    {
        "L7163Y": {
            "id": "LP14/99",
            "shape": "rectangle",
            "number": 14,
            "width": 99.1,
            "height": 38.1,
        }
    },
    {
        "L7164": {
            "id": "LP12/63",
            "shape": "rectangle",
            "number": 12,
            "width": 45.7,
            "height": 72,
        }
    },
    {
        "L7165": {
            "id": "LP8/90OV",
            "shape": "oval",
            "number": 8,
            "width": 90,
            "height": 62,
        }
    },
    {
        "L7165": {
            "id": "LP8/99",
            "shape": "rectangle",
            "number": 8,
            "width": 99.1,
            "height": 67.7,
        }
    },
    {
        "L7165X": {
            "id": "LP8/90OV",
            "shape": "oval",
            "number": 8,
            "width": 90,
            "height": 62,
        }
    },
    {
        "L7165X": {
            "id": "LP8/99",
            "shape": "rectangle",
            "number": 8,
            "width": 99.1,
            "height": 67.7,
        }
    },
    {
        "L7166": {
            "id": "LP6/99",
            "shape": "rectangle",
            "number": 6,
            "width": 99.1,
            "height": 93.1,
        }
    },
    {
        "L7166X": {
            "id": "LP6/99",
            "shape": "rectangle",
            "number": 6,
            "width": 99.1,
            "height": 93.1,
        }
    },
    {
        "L7167": {
            "id": "LP1/199",
            "shape": "rectangle",
            "number": 1,
            "width": 199.6,
            "height": 289.1,
        }
    },
    {
        "L7168": {
            "id": "LP2/195OV",
            "shape": "oval",
            "number": 2,
            "width": 195,
            "height": 139,
        }
    },
    {
        "L7168": {
            "id": "LP2/199",
            "shape": "rectangle",
            "number": 2,
            "width": 199.6,
            "height": 143.5,
        }
    },
    {
        "L7169": {
            "id": "LP4/99",
            "shape": "rectangle",
            "number": 4,
            "width": 99.1,
            "height": 139,
        }
    },
    {
        "L7170": {
            "id": "LP24/134",
            "shape": "rectangle",
            "number": 24,
            "width": 134,
            "height": 11,
        }
    },
    {
        "L7171A": {
            "id": "LP4/200",
            "shape": "rectangle",
            "number": 4,
            "width": 200,
            "height": 60,
        }
    },
    {
        "L7171B": {
            "id": "LP4/200",
            "shape": "rectangle",
            "number": 4,
            "width": 200,
            "height": 60,
        }
    },
    {
        "L7171G": {
            "id": "LP4/200",
            "shape": "rectangle",
            "number": 4,
            "width": 200,
            "height": 60,
        }
    },
    {
        "L7171": {
            "id": "LP4/200",
            "shape": "rectangle",
            "number": 4,
            "width": 200,
            "height": 60,
        }
    },
    {
        "L7171R": {
            "id": "LP4/200",
            "shape": "rectangle",
            "number": 4,
            "width": 200,
            "height": 60,
        }
    },
    {
        "L7171Y": {
            "id": "LP4/200",
            "shape": "rectangle",
            "number": 4,
            "width": 200,
            "height": 60,
        }
    },
    {
        "L7172": {
            "id": "LP18/100",
            "shape": "rectangle",
            "number": 18,
            "width": 100,
            "height": 30,
        }
    },
    {
        "L7173B": {
            "id": "LP10/95OV",
            "shape": "oval",
            "number": 10,
            "width": 95,
            "height": 53,
        }
    },
    {
        "L7173B": {
            "id": "LP10/99",
            "shape": "rectangle",
            "number": 10,
            "width": 99.1,
            "height": 57,
        }
    },
    {
        "L7173": {
            "id": "LP10/95OV",
            "shape": "oval",
            "number": 10,
            "width": 95,
            "height": 53,
        }
    },
    {
        "L7173": {
            "id": "LP10/99",
            "shape": "rectangle",
            "number": 10,
            "width": 99.1,
            "height": 57,
        }
    },
    {
        "L7173X": {
            "id": "LP10/95OV",
            "shape": "oval",
            "number": 10,
            "width": 95,
            "height": 53,
        }
    },
    {
        "L7173X": {
            "id": "LP10/99",
            "shape": "rectangle",
            "number": 10,
            "width": 99.1,
            "height": 57,
        }
    },
    {
        "L7177": {
            "id": "LP12/99",
            "shape": "rectangle",
            "number": 12,
            "width": 99.1,
            "height": 42.3,
        }
    },
    {
        "L7263": {
            "id": "LP14/99",
            "shape": "rectangle",
            "number": 14,
            "width": 99.1,
            "height": 38.1,
        }
    },
    {
        "L7263R": {
            "id": "LP14/99",
            "shape": "rectangle",
            "number": 14,
            "width": 99.1,
            "height": 38.1,
        }
    },
    {
        "L7263Y": {
            "id": "LP14/99",
            "shape": "rectangle",
            "number": 14,
            "width": 99.1,
            "height": 38.1,
        }
    },
    {
        "L7363P": {
            "id": "LP14/99",
            "shape": "rectangle",
            "number": 14,
            "width": 99.1,
            "height": 38.1,
        }
    },
    {
        "L7409": {
            "id": "LP51/57",
            "shape": "rectangle",
            "number": 51,
            "width": 57,
            "height": 15,
        }
    },
    {
        "L7551": {
            "id": "LP65/38",
            "shape": "rectangle",
            "number": 65,
            "width": 38.1,
            "height": 21.2,
        }
    },
    {
        "L7556": {
            "id": "LP84/46",
            "shape": "rectangle",
            "number": 84,
            "width": 46,
            "height": 11.1,
        }
    },
    {
        "L7559": {
            "id": "LP24/63",
            "shape": "rectangle",
            "number": 24,
            "width": 45.7,
            "height": 33.9,
        }
    },
    {
        "L7560": {
            "id": "LP21/63",
            "shape": "rectangle",
            "number": 21,
            "width": 45.7,
            "height": 38.1,
        }
    },
    {
        "L7562": {
            "id": "LP16/99",
            "shape": "rectangle",
            "number": 16,
            "width": 99.1,
            "height": 34,
        }
    },
    {
        "L7563": {
            "id": "LP14/99",
            "shape": "rectangle",
            "number": 14,
            "width": 99.1,
            "height": 38.1,
        }
    },
    {
        "L7565": {
            "id": "LP8/90OV",
            "shape": "oval",
            "number": 8,
            "width": 90,
            "height": 62,
        }
    },
    {
        "L7565": {
            "id": "LP8/99",
            "shape": "rectangle",
            "number": 8,
            "width": 99.1,
            "height": 67.7,
        }
    },
    {
        "L7567": {
            "id": "LP1/210H",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "L7567": {
            "id": "LP1/210J",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "L7567": {
            "id": "LP1/210V",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "L7568": {
            "id": "LP1/210H",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "L7568": {
            "id": "LP1/210J",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "L7568": {
            "id": "LP1/210V",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "L7568": {
            "id": "LP2/195OV",
            "shape": "oval",
            "number": 2,
            "width": 195,
            "height": 139,
        }
    },
    {
        "L7568": {
            "id": "LP2/199",
            "shape": "rectangle",
            "number": 2,
            "width": 199.6,
            "height": 143.5,
        }
    },
    {
        "L7630": {
            "id": "LP12/64R",
            "shape": "circle",
            "number": 12,
            "width": 63.5,
            "height": 63.5,
        }
    },
    {
        "L7636": {
            "id": "LP48/45",
            "shape": "rectangle",
            "number": 48,
            "width": 45.7,
            "height": 21.2,
        }
    },
    {
        "L7644": {
            "id": "LP9/133",
            "shape": "rectangle",
            "number": 9,
            "width": 133,
            "height": 29.6,
        }
    },
    {
        "L7650": {
            "id": "LP12/64R",
            "shape": "circle",
            "number": 12,
            "width": 63.5,
            "height": 63.5,
        }
    },
    {
        "L7651": {
            "id": "LP65/38",
            "shape": "rectangle",
            "number": 65,
            "width": 38.1,
            "height": 21.2,
        }
    },
    {
        "L7651P": {
            "id": "LP65/38",
            "shape": "rectangle",
            "number": 65,
            "width": 38.1,
            "height": 21.2,
        }
    },
    {
        "L7651Y": {
            "id": "LP65/38",
            "shape": "rectangle",
            "number": 65,
            "width": 38.1,
            "height": 21.2,
        }
    },
    {
        "L7654": {
            "id": "LP40/45",
            "shape": "rectangle",
            "number": 40,
            "width": 45.7,
            "height": 25.4,
        }
    },
    {
        "L7655": {
            "id": "LP12/89",
            "shape": "round_rectangle",
            "number": 12,
            "width": 89,
            "height": 42,
        }
    },
    {
        "L7656": {
            "id": "LP84/46",
            "shape": "rectangle",
            "number": 84,
            "width": 46,
            "height": 11.1,
        }
    },
    {
        "L7657": {
            "id": "LP270/18",
            "shape": "rectangle",
            "number": 270,
            "width": 17.8,
            "height": 10,
        }
    },
    {
        "L7658": {
            "id": "LP189/25",
            "shape": "rectangle",
            "number": 189,
            "width": 25.4,
            "height": 10,
        }
    },
    {
        "L7660": {
            "id": "LPCD116",
            "shape": "circle",
            "number": 2,
            "width": 116,
            "height": 116,
        }
    },
    {
        "L7664": {
            "id": "LP8/71",
            "shape": "rectangle",
            "number": 8,
            "width": 71,
            "height": 70,
        }
    },
    {
        "L7665": {
            "id": "LP24/72",
            "shape": "rectangle",
            "number": 24,
            "width": 72,
            "height": 21.11,
        }
    },
    {
        "L7666": {
            "id": "LP10/70",
            "shape": "rectangle",
            "number": 10,
            "width": 70,
            "height": 52,
        }
    },
    {
        "L7667": {
            "id": "LP9/133",
            "shape": "rectangle",
            "number": 9,
            "width": 133,
            "height": 29.6,
        }
    },
    {
        "L7668": {
            "id": "LP15/59",
            "shape": "rectangle",
            "number": 15,
            "width": 59,
            "height": 51,
        }
    },
    {
        "L7670": {
            "id": "LP12/64R",
            "shape": "circle",
            "number": 12,
            "width": 63.5,
            "height": 63.5,
        }
    },
    {
        "L7670R": {
            "id": "LP12/64R",
            "shape": "circle",
            "number": 12,
            "width": 63.5,
            "height": 63.5,
        }
    },
    {
        "L7670Y": {
            "id": "LP12/64R",
            "shape": "circle",
            "number": 12,
            "width": 63.5,
            "height": 63.5,
        }
    },
    {
        "L7671": {
            "id": "LP12/76",
            "shape": "rectangle",
            "number": 12,
            "width": 76.2,
            "height": 46.4,
        }
    },
    {
        "L7674": {
            "id": "LP16/145",
            "shape": "rectangle",
            "number": 16,
            "width": 145,
            "height": 17,
        }
    },
    {
        "L7676": {
            "id": "LPCD117",
            "shape": "circle",
            "number": 2,
            "width": 117,
            "height": 117,
        }
    },
    {
        "L7678": {
            "id": "LPCD117",
            "shape": "circle",
            "number": 2,
            "width": 117,
            "height": 117,
        }
    },
    {
        "L7680": {
            "id": "LP65/38",
            "shape": "rectangle",
            "number": 65,
            "width": 38.1,
            "height": 21.2,
        }
    },
    {
        "L7690": {
            "id": "LP65/38",
            "shape": "rectangle",
            "number": 65,
            "width": 38.1,
            "height": 21.2,
        }
    },
    {
        "L7701": {
            "id": "LP4/192",
            "shape": "rectangle",
            "number": 4,
            "width": 192,
            "height": 62,
        }
    },
    {
        "L7760": {
            "id": "LPCD117",
            "shape": "circle",
            "number": 2,
            "width": 117,
            "height": 117,
        }
    },
    {
        "L7765": {
            "id": "LP8/90OV",
            "shape": "oval",
            "number": 8,
            "width": 90,
            "height": 62,
        }
    },
    {
        "L7765": {
            "id": "LP8/99",
            "shape": "rectangle",
            "number": 8,
            "width": 99.1,
            "height": 67.7,
        }
    },
    {
        "L7768": {
            "id": "LP2/195OV",
            "shape": "oval",
            "number": 2,
            "width": 195,
            "height": 139,
        }
    },
    {
        "L7768": {
            "id": "LP2/199",
            "shape": "rectangle",
            "number": 2,
            "width": 199.6,
            "height": 143.5,
        }
    },
    {
        "L7769": {
            "id": "LP4/99",
            "shape": "rectangle",
            "number": 4,
            "width": 99.1,
            "height": 139,
        }
    },
    {
        "L7776": {
            "id": "LPCD117",
            "shape": "circle",
            "number": 2,
            "width": 117,
            "height": 117,
        }
    },
    {
        "L7780": {
            "id": "LP24/40R",
            "shape": "circle",
            "number": 24,
            "width": 40,
            "height": 40,
        }
    },
    {
        "L7781": {
            "id": "LP40/45",
            "shape": "rectangle",
            "number": 40,
            "width": 45.7,
            "height": 25.4,
        }
    },
    {
        "L7782": {
            "id": "LP21/63",
            "shape": "rectangle",
            "number": 21,
            "width": 45.7,
            "height": 38.1,
        }
    },
    {
        "L7783": {
            "id": "LP10/96",
            "shape": "rectangle",
            "number": 10,
            "width": 96,
            "height": 50.8,
        }
    },
    {
        "L7784": {
            "id": "LP1/210H",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "L7784": {
            "id": "LP1/210J",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "L7784": {
            "id": "LP1/210V",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "L7860": {
            "id": "LPCD117",
            "shape": "circle",
            "number": 2,
            "width": 117,
            "height": 117,
        }
    },
    {
        "L7960": {
            "id": "LP21/63",
            "shape": "rectangle",
            "number": 21,
            "width": 45.7,
            "height": 38.1,
        }
    },
    {
        "L7962": {
            "id": "LP16/99",
            "shape": "rectangle",
            "number": 16,
            "width": 99.1,
            "height": 34,
        }
    },
    {
        "L7963": {
            "id": "LP14/99",
            "shape": "rectangle",
            "number": 14,
            "width": 99.1,
            "height": 38.1,
        }
    },
    {
        "L7965": {
            "id": "LP8/90OV",
            "shape": "oval",
            "number": 8,
            "width": 90,
            "height": 62,
        }
    },
    {
        "L7965": {
            "id": "LP8/99",
            "shape": "rectangle",
            "number": 8,
            "width": 99.1,
            "height": 67.7,
        }
    },
    {
        "L7966": {
            "id": "LP6/99",
            "shape": "rectangle",
            "number": 6,
            "width": 99.1,
            "height": 93.1,
        }
    },
    {
        "L7973": {
            "id": "LP10/95OV",
            "shape": "oval",
            "number": 10,
            "width": 95,
            "height": 53,
        }
    },
    {
        "L7973": {
            "id": "LP10/99",
            "shape": "rectangle",
            "number": 10,
            "width": 99.1,
            "height": 57,
        }
    },
    {
        "L7990": {
            "id": "LP8/90OV",
            "shape": "oval",
            "number": 8,
            "width": 90,
            "height": 62,
        }
    },
    {
        "L7990": {
            "id": "LP8/99",
            "shape": "rectangle",
            "number": 8,
            "width": 99.1,
            "height": 67.7,
        }
    },
    {
        "L7990R": {
            "id": "LP8/90OV",
            "shape": "oval",
            "number": 8,
            "width": 90,
            "height": 62,
        }
    },
    {
        "L7990R": {
            "id": "LP8/99",
            "shape": "rectangle",
            "number": 8,
            "width": 99.1,
            "height": 67.7,
        }
    },
    {
        "L7992": {
            "id": "LP10/95OV",
            "shape": "oval",
            "number": 10,
            "width": 95,
            "height": 53,
        }
    },
    {
        "L7992": {
            "id": "LP10/99",
            "shape": "rectangle",
            "number": 10,
            "width": 99.1,
            "height": 57,
        }
    },
    {
        "L7993": {
            "id": "LP8/90OV",
            "shape": "oval",
            "number": 8,
            "width": 90,
            "height": 62,
        }
    },
    {
        "L7993": {
            "id": "LP8/99",
            "shape": "rectangle",
            "number": 8,
            "width": 99.1,
            "height": 67.7,
        }
    },
    {
        "L7994": {
            "id": "LP4/99",
            "shape": "rectangle",
            "number": 4,
            "width": 99.1,
            "height": 139,
        }
    },
    {
        "L7995": {
            "id": "LP6/99",
            "shape": "rectangle",
            "number": 6,
            "width": 99.1,
            "height": 93.1,
        }
    },
    {
        "L7996": {
            "id": "LP2/195OV",
            "shape": "oval",
            "number": 2,
            "width": 195,
            "height": 139,
        }
    },
    {
        "L7996": {
            "id": "LP2/199",
            "shape": "rectangle",
            "number": 2,
            "width": 199.6,
            "height": 143.5,
        }
    },
    {
        "L7997": {
            "id": "LP1/199",
            "shape": "rectangle",
            "number": 1,
            "width": 199.6,
            "height": 289.1,
        }
    },
    {
        "LR3463": {
            "id": "LP4/105",
            "shape": "rectangle",
            "number": 4,
            "width": 105,
            "height": 149,
        }
    },
    {
        "LR3475": {
            "id": "LP24/70SS",
            "shape": "rectangle",
            "number": 24,
            "width": 70,
            "height": 36,
        }
    },
    {
        "LR3478": {
            "id": "LP1/210H",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "LR3478": {
            "id": "LP1/210J",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "LR3478": {
            "id": "LP1/210V",
            "shape": "rectangle",
            "number": 1,
            "width": 210,
            "height": 298,
        }
    },
    {
        "LR3655": {
            "id": "LP2/210",
            "shape": "rectangle",
            "number": 2,
            "width": 210,
            "height": 149,
        }
    },
    {
        "LR4760": {
            "id": "LP7/192",
            "shape": "rectangle",
            "number": 7,
            "width": 192,
            "height": 39,
        }
    },
    {
        "LR4761": {
            "id": "LP4/192",
            "shape": "rectangle",
            "number": 4,
            "width": 192,
            "height": 62,
        }
    },
    {
        "LR7159": {
            "id": "LP24/63",
            "shape": "rectangle",
            "number": 24,
            "width": 45.7,
            "height": 33.9,
        }
    },
    {
        "LR7160": {
            "id": "LP21/63",
            "shape": "rectangle",
            "number": 21,
            "width": 45.7,
            "height": 38.1,
        }
    },
    {
        "LR7162": {
            "id": "LP16/99",
            "shape": "rectangle",
            "number": 16,
            "width": 99.1,
            "height": 34,
        }
    },
    {
        "LR7163": {
            "id": "LP14/99",
            "shape": "rectangle",
            "number": 14,
            "width": 99.1,
            "height": 38.1,
        }
    },
    {
        "LR7165": {
            "id": "LP8/90OV",
            "shape": "oval",
            "number": 8,
            "width": 90,
            "height": 62,
        }
    },
    {
        "LR7165": {
            "id": "LP8/99",
            "shape": "rectangle",
            "number": 8,
            "width": 99.1,
            "height": 67.7,
        }
    },
    {
        "LR7167": {
            "id": "LP1/199",
            "shape": "rectangle",
            "number": 1,
            "width": 199.6,
            "height": 289.1,
        }
    },
    {
        "LR7168": {
            "id": "LP2/195OV",
            "shape": "oval",
            "number": 2,
            "width": 195,
            "height": 139,
        }
    },
    {
        "LR7168": {
            "id": "LP2/199",
            "shape": "rectangle",
            "number": 2,
            "width": 199.6,
            "height": 143.5,
        }
    },
    {
        "LR7651": {
            "id": "LP65/38",
            "shape": "rectangle",
            "number": 65,
            "width": 38.1,
            "height": 21.2,
        }
    },
    {
        "M3483": {
            "id": "LP4/105",
            "shape": "rectangle",
            "number": 4,
            "width": 105,
            "height": 149,
        }
    },
    {
        "M3490": {
            "id": "LP24/70SS",
            "shape": "rectangle",
            "number": 24,
            "width": 70,
            "height": 36,
        }
    },
    {
        "M8167": {
            "id": "LP1/199",
            "shape": "rectangle",
            "number": 1,
            "width": 199.6,
            "height": 289.1,
        }
    },
    {
        "M8359": {
            "id": "LP24/63",
            "shape": "rectangle",
            "number": 24,
            "width": 45.7,
            "height": 33.9,
        }
    },
    {
        "M8360": {
            "id": "LP21/63",
            "shape": "rectangle",
            "number": 21,
            "width": 45.7,
            "height": 38.1,
        }
    },
    {
        "MP7160": {
            "id": "LP21/63",
            "shape": "rectangle",
            "number": 21,
            "width": 45.7,
            "height": 38.1,
        }
    },
    {
        "MP7163": {
            "id": "LP14/99",
            "shape": "rectangle",
            "number": 14,
            "width": 99.1,
            "height": 38.1,
        }
    },
    {
        "S161006R": {
            "id": "LPCD117",
            "shape": "circle",
            "number": 2,
            "width": 117,
            "height": 117,
        }
    },
]
