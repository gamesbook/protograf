# -*- coding: utf-8 -*-
"""
Base shape class for protograf

Notes:
    * https://www.a2-size.com/american-paper-sizes/
    * https://en.wikipedia.org/wiki/Paper_size#Overview_of_ISO_paper_sizes
"""
# lib
from collections import namedtuple
import copy
from enum import Enum
import inspect
import json
import logging
import math
import os
import pathlib
from urllib.parse import urlparse

# third party
import jinja2
from jinja2.environment import Template
from svglib.svglib import svg2rlg
from reportlab.pdfgen import canvas as reportlab_canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont, TTFError
from reportlab.lib.units import cm, inch, mm
from reportlab.lib.pagesizes import (
    A8,
    A7,
    A6,
    A5,
    A4,
    A3,
    A2,
    A1,
    A0,
    LETTER,
    LEGAL,
    ELEVENSEVENTEEN,
    letter,
    legal,
    elevenSeventeen,
    B6,
    B5,
    B4,
    B3,
    B2,
    B0,
    landscape,
)
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import (
    Color,
    aliceblue,
    antiquewhite,
    aqua,
    aquamarine,
    azure,
    beige,
    bisque,
    black,
    blanchedalmond,
    blue,
    blueviolet,
    brown,
    burlywood,
    cadetblue,
    chartreuse,
    chocolate,
    coral,
    cornflowerblue,
    cornsilk,
    crimson,
    cyan,
    darkblue,
    darkcyan,
    darkgoldenrod,
    darkgray,
    darkgrey,
    darkgreen,
    darkkhaki,
    darkmagenta,
    darkolivegreen,
    darkorange,
    darkorchid,
    darkred,
    darksalmon,
    darkseagreen,
    darkslateblue,
    darkslategray,
    darkslategrey,
    darkturquoise,
    darkviolet,
    deeppink,
    deepskyblue,
    dimgray,
    dimgrey,
    dodgerblue,
    floralwhite,
    forestgreen,
    fuchsia,
    gainsboro,
    ghostwhite,
    gold,
    goldenrod,
    gray,
    grey,
    green,
    greenyellow,
    honeydew,
    hotpink,
    indianred,
    indigo,
    ivory,
    khaki,
    lavender,
    lavenderblush,
    lawngreen,
    lemonchiffon,
    lightblue,
    lightcoral,
    lightcyan,
    lightgoldenrodyellow,
    lightgreen,
    lightgrey,
    lightpink,
    lightsalmon,
    lightseagreen,
    lightskyblue,
    lightslategray,
    lightslategrey,
    lightsteelblue,
    lightyellow,
    lime,
    limegreen,
    linen,
    magenta,
    maroon,
    mediumaquamarine,
    mediumblue,
    mediumorchid,
    mediumpurple,
    mediumseagreen,
    mediumslateblue,
    mediumspringgreen,
    mediumturquoise,
    mediumvioletred,
    midnightblue,
    mintcream,
    mistyrose,
    moccasin,
    navajowhite,
    navy,
    oldlace,
    olive,
    olivedrab,
    orange,
    orangered,
    orchid,
    palegoldenrod,
    palegreen,
    paleturquoise,
    palevioletred,
    papayawhip,
    peachpuff,
    peru,
    pink,
    plum,
    powderblue,
    purple,
    red,
    rosybrown,
    royalblue,
    saddlebrown,
    salmon,
    sandybrown,
    seagreen,
    seashell,
    sienna,
    silver,
    skyblue,
    slateblue,
    slategray,
    slategrey,
    snow,
    springgreen,
    steelblue,
    tan,
    teal,
    thistle,
    tomato,
    turquoise,
    violet,
    wheat,
    white,
    whitesmoke,
    yellow,
    yellowgreen,
    fidblue,
    fidred,
    fidlightblue,
    cornflower,
    firebrick,
)
import requests

# local
from protograf.utils import geoms, tools
from protograf.utils.support import LookupType

log = logging.getLogger(__name__)

DEBUG = False
DEBUG_COLOR = lightsteelblue
CACHE_DIRECTORY = ".protograf"  # append to the user's home directory
BGG_IMAGES = "cf.geekdo-images.com"
BUILTIN_FONTS = ["Times-Roman", "Courier", "Helvetica"]

# ---- named tuples
UnitProperties = namedtuple(
    "UnitProperties",
    [
        "page_width",
        "page_height",
        "margin_left",
        "margin_right",
        "margin_bottom",
        "margin_top",
        "x",
        "y",
        "cx",
        "cy",
        "height",
        "width",
        "top",
        "radius",
        "diameter",
        "side",
        "length",
        "spacing_x",
        "spacing_y",
        "offset_x",
        "offset_y",
    ],
)
OffsetProperties = namedtuple(
    "OffsetProperties",
    [
        "off_x",
        "off_y",
        "delta_x",
        "delta_y",
    ],
)
GridShape = namedtuple(
    "GridShape",
    [
        "label",
        "x",
        "y",
        "shape",
    ],
)
Bounds = namedtuple(
    "Bounds",
    [
        "left",
        "right",
        "bottom",
        "top",
    ],
)

# ---- units
UNITS = {"cm": cm, "inch": inch, "mm": mm, "points": "points"}
# ---- colors (ReportLab; 18xx Games)
COLORS = {
    "aliceblue": aliceblue,
    "antiquewhite": antiquewhite,
    "aqua": aqua,
    "aquamarine": aquamarine,
    "azure": azure,
    "beige": beige,
    "bisque": bisque,
    "black": black,
    "blanchedalmond": blanchedalmond,
    "blue": blue,
    "blueviolet": blueviolet,
    "brown": brown,
    "burlywood": burlywood,
    "cadetblue": cadetblue,
    "chartreuse": chartreuse,
    "chocolate": chocolate,
    "coral": coral,
    "cornflower": cornflower,
    "cornflowerblue": cornflowerblue,
    "cornsilk": cornsilk,
    "crimson": crimson,
    "cyan": cyan,
    "darkblue": darkblue,
    "darkcyan": darkcyan,
    "darkgoldenrod": darkgoldenrod,
    "darkgray": darkgray,
    "darkgreen": darkgreen,
    "darkgrey": darkgrey,
    "darkkhaki": darkkhaki,
    "darkmagenta": darkmagenta,
    "darkolivegreen": darkolivegreen,
    "darkorange": darkorange,
    "darkorchid": darkorchid,
    "darkred": darkred,
    "darksalmon": darksalmon,
    "darkseagreen": darkseagreen,
    "darkslateblue": darkslateblue,
    "darkslategray": darkslategray,
    "darkslategrey": darkslategrey,
    "darkturquoise": darkturquoise,
    "darkviolet": darkviolet,
    "deeppink": deeppink,
    "deepskyblue": deepskyblue,
    "dimgray": dimgray,
    "dimgrey": dimgrey,
    "dodgerblue": dodgerblue,
    "fidblue": fidblue,
    "fidlightblue": fidlightblue,
    "fidred": fidred,
    "firebrick": firebrick,
    "floralwhite": floralwhite,
    "forestgreen": forestgreen,
    "fuchsia": fuchsia,
    "gainsboro": gainsboro,
    "ghostwhite": ghostwhite,
    "goldenrod": goldenrod,
    "gold": gold,
    "gray": gray,
    "green": green,
    "greenyellow": greenyellow,
    "grey": grey,
    "honeydew": honeydew,
    "hotpink": hotpink,
    "indianred": indianred,
    "indigo": indigo,
    "ivory": ivory,
    "khaki": khaki,
    "lavenderblush": lavenderblush,
    "lavender": lavender,
    "lawngreen": lawngreen,
    "lemonchiffon": lemonchiffon,
    "lightblue": lightblue,
    "lightcoral": lightcoral,
    "lightcyan": lightcyan,
    "lightgoldenrodyellow": lightgoldenrodyellow,
    "lightgreen": lightgreen,
    "lightgrey": lightgrey,
    "lightpink": lightpink,
    "lightsalmon": lightsalmon,
    "lightseagreen": lightseagreen,
    "lightskyblue": lightskyblue,
    "lightslategray": lightslategray,
    "lightslategrey": lightslategrey,
    "lightsteelblue": lightsteelblue,
    "lightyellow": lightyellow,
    "limegreen": limegreen,
    "lime": lime,
    "linen": linen,
    "magenta": magenta,
    "maroon": maroon,
    "mediumaquamarine": mediumaquamarine,
    "mediumblue": mediumblue,
    "mediumorchid": mediumorchid,
    "mediumpurple": mediumpurple,
    "mediumseagreen": mediumseagreen,
    "mediumslateblue": mediumslateblue,
    "mediumspringgreen": mediumspringgreen,
    "mediumturquoise": mediumturquoise,
    "mediumvioletred": mediumvioletred,
    "midnightblue": midnightblue,
    "mintcream": mintcream,
    "mistyrose": mistyrose,
    "moccasin": moccasin,
    "navajowhite": navajowhite,
    "navy": navy,
    "oldlace": oldlace,
    "olivedrab": olivedrab,
    "olive": olive,
    "orange": orange,
    "orangered": orangered,
    "orchid": orchid,
    "palegoldenrod": palegoldenrod,
    "palegreen": palegreen,
    "paleturquoise": paleturquoise,
    "palevioletred": palevioletred,
    "papayawhip": papayawhip,
    "peachpuff": peachpuff,
    "peru": peru,
    "pink": pink,
    "plum": plum,
    "powderblue": powderblue,
    "purple": purple,
    "red": red,
    "rosybrown": rosybrown,
    "royalblue": royalblue,
    "saddlebrown": saddlebrown,
    "salmon": salmon,
    "sandybrown": sandybrown,
    "seagreen": seagreen,
    "seashell": seashell,
    "sienna": sienna,
    "silver": silver,
    "skyblue": skyblue,
    "slateblue": slateblue,
    "slategray": slategray,
    "slategrey": slategrey,
    "snow": snow,
    "springgreen": springgreen,
    "steelblue": steelblue,
    "tan": tan,
    "teal": teal,
    "thistle": thistle,
    "tomato": tomato,
    "turquoise": turquoise,
    "violet": violet,
    "wheat": wheat,
    "whitesmoke": whitesmoke,
    "white": white,
    "yellowgreen": yellowgreen,
    "yellow": yellow,
    # 18xx colors from https://github.com/XeryusTC/map18xx/blob/master/src/tile.rs
    "GROUND_18XX": "#FDD9B5",  # Sandy Tan
    "YELLOW_18XX": "#FDEE00",  # Aureolin
    "GREEN_18XX": "#00A550",  # Pigment Green
    "RUSSET_18XX": "#CD7F32",  # Bronze
    "GREY_18XX": "#ACACAC",  # Silver Chalice
    "BROWN_18XX": "#7B3F00",  # Chocolate
    "RED_18XX": "#DC143C",  # Crimson
    "BLUE_18XX": "#007FFF",  # Azure
    "BARRIER_18XX": "#660000",  # Blood Red
    "WHITE_18XX": "#FFFFFF",  # White
}
# ---- paper formats
PAGES = {
    "LETTER": LETTER,
    "landscape": landscape,
    "legal": legal,
    "A1": A1,
    "A0": A0,
    "A3": A3,
    "A2": A2,
    "A5": A5,
    "A4": A4,
    "A6": A6,
    "elevenSeventeen": elevenSeventeen,
    "LEGAL": LEGAL,
    "letter": letter,
    "B4": B4,
    "B5": B5,
    "B6": B6,
    "B0": B0,
    "B2": B2,
    "B3": B3,
    "ELEVENSEVENTEEN": ELEVENSEVENTEEN,
    "tabloid": elevenSeventeen,
}
WIDTH = 0.1

CLOCK_ANGLES = [60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 0, 30]


class BaseCanvas:
    """Wrapper/extended class for a ReportLab canvas."""

    def __init__(self, filename=None, paper=None, defaults=None, **kwargs):
        self.jsonfile = kwargs.get("defaults", None)
        self.defaults = {}
        # ---- setup defaults
        if self.jsonfile:
            try:
                with open(self.jsonfile) as data_file:
                    self.defaults = json.load(data_file)
            except (IOError, ValueError):
                filepath = tools.script_path()
                _jsonfile = os.path.join(filepath, self.jsonfile)
                try:
                    with open(_jsonfile) as data_file:
                        self.defaults = json.load(data_file)
                except (IOError, ValueError):
                    tools.feedback(
                        f'Unable to find or load the file "{self.jsonfile}"'
                        f' - also checked in "{filepath}".',
                        True,
                    )
        # ---- override file defaults with BaseCanvas kwargs
        if kwargs:
            _kwargs = kwargs["kwargs"]
            for kwarg in _kwargs:
                self.defaults[kwarg] = _kwargs[kwarg]
            # print(f" *** {self.defaults=}")
        # ---- paper, pagesize & canvas
        _paper = paper or self.defaults.get("paper", A4)
        # **NOTE** ReportLab uses 'pagesize' to track the page dimensions;
        #          the named paper formats, e.g. A4, are just tuples storing
        #          (width, height) values using points units, so A4 is :
        #          (595.2755905511812, 841.8897637795277)
        self.canvas = reportlab_canvas.Canvas(filename=filename, pagesize=_paper)
        # ---- constants
        self.default_length = 1
        self.show_id = False
        # ---- general
        self.shape = None
        self.shape_id = None
        self.sequence = self.defaults.get("sequence", [])
        self.dataset = []
        self.members = []  # card IDs, of which current card is a member
        self._object = None
        self.kwargs = kwargs
        self.run_debug = False
        self.units = self.get_units(self.defaults.get("units"), cm)
        # print(f" *** {self.units=} \n {self.defaults=}")
        # ---- paper & margins
        self.paper = _paper
        self.page_width = self.paper[0] / self.units  # user-units e.g. cm
        self.page_height = self.paper[1] / self.units  # user-units e.g. cm
        # print(f" *** {self.page_height=} {self.page_width=}")
        self.margin = self.defaults.get("margin", 1)
        self.margin_top = self.defaults.get("margin_top", self.margin)
        self.margin_bottom = self.defaults.get("margin_bottom", self.margin)
        self.margin_left = self.defaults.get("margin_left", self.margin)
        self.margin_right = self.defaults.get("margin_right", self.margin)
        # ---- sizes and positions
        self.row = self.defaults.get("row", None)
        self.col = self.defaults.get("col", self.defaults.get("column", None))
        self.side = self.defaults.get("side", 1)  # equal length sides
        self.height = self.defaults.get("height", self.side)
        self.width = self.defaults.get("width", self.side)
        self.top = self.defaults.get("width", self.width * 0.5)
        self.depth = self.defaults.get("depth", self.side)  # diamond
        self.x = self.defaults.get("x", self.defaults.get("left", 1))
        self.y = self.defaults.get("y", self.defaults.get("bottom", 1))
        self.cx = self.defaults.get("cx", None)  # NB! not 0; needed for internal check
        self.cy = self.defaults.get("cy", None)  # NB! not 0; needed for internal check
        self.scaling = self.defaults.get("scaling", None)
        self.dot_point = self.defaults.get("dot_point", 3.0)  # points
        # ---- to be calculated ...
        self.area = None
        self.vertices = []
        # ---- repeats
        self.pattern = self.defaults.get("pattern", None)
        self.repeat = self.defaults.get("repeat", True)
        self.interval = self.defaults.get("interval", 0)
        self.interval_x = self.defaults.get("interval_x", self.interval)
        self.interval_y = self.defaults.get("interval_y", self.interval)
        # ---- rotation / position /elevation
        self.rotation = self.defaults.get("rotation", 0)  # degrees
        self.direction = self.defaults.get("direction", "north")
        self.position = self.defaults.get("position", None)
        self.flip = self.defaults.get("flip", "north")  # north/south
        self.elevation = self.defaults.get("elevation", "horizontal")
        self.facing = self.defaults.get("facing", "out")  # out/in
        # ---- color and transparency
        fill = self.defaults.get("fill", self.defaults.get("fill_color"))
        self.fill = self.get_color(fill, white)
        self.transparency = self.defaults.get("transparency", None)
        self.debug_color = self.get_color(self.defaults.get("debug_color"), DEBUG_COLOR)
        self.fill_stroke = self.defaults.get("fill_stroke", None)
        self.stroke_fill = self.defaults.get("stroke_fill", None)  # alias
        # ---- stroke
        stroke = self.defaults.get("stroke", self.defaults.get("stroke_color"))
        self.stroke = self.get_color(stroke, black)
        self.stroke_width = self.defaults.get("stroke_width", WIDTH)
        self.outline = self.defaults.get("outline", None)
        # ---- overwrite fill & stroke
        if self.stroke_fill:  # alias
            self.stroke = self.stroke_fill
            self.fill = self.stroke_fill
        if self.fill_stroke:
            self.stroke = self.fill_stroke
            self.fill = self.fill_stroke
        # if self.outline:
        #     self.stroke = self.outline
        #     self.fill = None
        # ---- font
        self.font_name = self.defaults.get("font_name", "Helvetica")
        self.font_size = self.defaults.get("font_size", 12)
        self.font_style = self.defaults.get("font_style", None)
        self.font_directory = self.defaults.get("font_directory", None)
        self.style = self.defaults.get("style", None)  # Normal? from reportlab
        self.wrap = self.defaults.get("wrap", False)
        self.align = self.defaults.get("align", "centre")  # centre,left,right,justify
        self._alignment = TA_LEFT  # see to_alignment()
        # ---- grid cut marks
        self.grid_marks = self.defaults.get("grid_marks", 0)
        self.grid_stroke = self.get_color(self.defaults.get("grid_stroke"), grey)
        self.grid_stroke_width = self.defaults.get(
            "grid_stroke_width", self.stroke_width
        )
        self.grid_length = self.defaults.get("grid_length", 0.85)  # 1/3 inch
        self.grid_offset = self.defaults.get("grid_offset", 0)
        # ---- line style
        self.line_stroke = self.defaults.get("line_stroke", WIDTH)
        self.line_width = self.defaults.get("line_width", self.stroke_width)
        self.line_cap = self.defaults.get("line_cap", None)
        self.dotted = self.defaults.get("dotted", self.defaults.get("dotted", False))
        self.dashed = self.defaults.get("dashed", None)
        # ---- text: base
        self.text = self.defaults.get("text", "")
        self.text_size = self.defaults.get("text_size", self.font_size)
        self.text_stroke = self.get_color(self.defaults.get("text_stroke"), self.stroke)
        self.text_stroke_width = self.defaults.get(
            "text_stroke_width", self.stroke_width
        )
        # ---- text: label
        self.label = self.defaults.get("label", "")
        self.label_size = self.defaults.get("label_size", self.font_size)
        self.label_face = self.defaults.get("label_face", self.font_name)
        self.label_stroke = self.get_color(
            self.defaults.get("label_stroke"), self.stroke
        )
        self.label_stroke_width = self.defaults.get(
            "label_stroke_width", self.stroke_width
        )
        self.label_mx = self.defaults.get("label_mx", 0)
        self.label_my = self.defaults.get("label_my", 0)
        self.label_rotation = self.defaults.get("label_rotation", 0)
        # ---- text: title
        self.title = self.defaults.get("title", "")
        self.title_size = self.defaults.get("title_size", self.font_size)
        self.title_face = self.defaults.get("title_face", self.font_name)
        self.title_stroke = self.get_color(
            self.defaults.get("title_stroke", self.stroke)
        )
        self.title_stroke_width = self.defaults.get(
            "title_stroke_width", self.stroke_width
        )
        self.title_mx = self.defaults.get("title_mx", 0)
        self.title_my = self.defaults.get("title_my", 0)
        self.title_rotation = self.defaults.get("title_rotation", 0)
        # ---- text: heading
        self.heading = self.defaults.get("heading", "")
        self.heading_size = self.defaults.get("heading_size", self.font_size)
        self.heading_face = self.defaults.get("heading_face", self.font_name)
        self.heading_stroke = self.get_color(
            self.defaults.get("heading_stroke"), self.stroke
        )
        self.heading_stroke_width = self.defaults.get(
            "heading_stroke_width", self.stroke_width
        )
        self.heading_mx = self.defaults.get("heading_mx", 0)
        self.heading_my = self.defaults.get("heading_my", 0)
        self.heading_rotation = self.defaults.get("heading_rotation", 0)
        # ---- text block
        self.outline_stroke = self.defaults.get("outline_stroke", self.fill)
        self.outline_width = self.defaults.get("outline_width", 0)
        self.leading = self.defaults.get("leading", self.font_size)
        self.transform = self.defaults.get("transform", None)
        # ---- image / file
        self.source = self.defaults.get("source", None)  # file or http://
        self.cache_directory = None  # should be a pathlib.Path object
        self.sliced = ""
        self.image_location = None
        # ---- line / ellipse / bezier / sector
        self.length = self.defaults.get("length", self.default_length)
        self.angle = self.defaults.get("angle", 0)
        self.angle_width = self.defaults.get("angle_width", 90)
        # ---- chord
        self.angle_1 = self.defaults.get("angle1", 0)
        # ---- arrow shape: head and tail
        self.points_offset = self.defaults.get("points_offset", 0)
        self.head_height = self.defaults.get("head_height", self.height)
        self.head_width = self.defaults.get("head_width", 2 * self.width)
        self.tail_width = self.defaults.get("tail_width", 0)  # adjusted in ArrowShape
        self.tail_notch = self.defaults.get("tail_notch", 0)
        # TODO arrow-on-a-line
        self.arrow_style = self.defaults.get("arrow_style", "triangle")
        self.arrow_tail_style = self.defaults.get("arrow_tail_style", None)
        self.arrow_head_fraction = self.defaults.get("arrow_head_fraction", 0.1)
        self.arrow_tail_fraction = self.defaults.get("arrow_tail_fraction", 0.1)
        self.arrow_head_height = self.defaults.get("arrow_head_height", None)
        self.arrow_tail_height = self.defaults.get("tail_height", None)
        self.arrow_head_width = self.defaults.get("head_width", None)
        self.arrow_tail_width = self.defaults.get("tail_width", None)
        self.arrow_tail_fill = self.defaults.get("tail_fill", self.fill)
        self.arrow_head_fill = self.defaults.get("head_fill", self.fill)
        self.arrow_head_stroke = self.defaults.get("head_stroke", self.stroke)
        self.arrow_tail_stroke = self.defaults.get("tail_stroke", self.stroke)
        self.arrow_head_stroke_width = self.defaults.get(
            "arrow_head_stroke_width", self.stroke_width
        )
        self.arrow_tail_stroke_width = self.defaults.get(
            "arrow_tail_stroke_width", self.stroke_width
        )
        # ---- line / bezier
        self.x_1 = self.defaults.get("x1", 0)
        self.y_1 = self.defaults.get("y1", 0)
        # ---- bezier
        self.x_2 = self.defaults.get("x2", 1)
        self.y_2 = self.defaults.get("y2", 1)
        self.x_3 = self.defaults.get("x3", 1)
        self.y_3 = self.defaults.get("y3", 1)
        # ---- rectangle / card
        self.rounding = self.defaults.get("rounding", 0)
        self.rounded = self.defaults.get("rounded", False)
        self.notch = self.defaults.get("notch", 0)
        self.notch_corners = self.defaults.get("notch_corners", "sw nw ne se")
        self.notch_x = self.defaults.get("notch_x", 0)
        self.notch_y = self.defaults.get("notch_y", 0)
        self.notch_style = self.defaults.get("notch_style", "snip")
        self.chevron = self.defaults.get("chevron", "")
        self.chevron_height = kwargs.get("chevron_height", 0)
        self.peaks = kwargs.get("peaks", [])
        self.peaks_dict = {}
        self.borders = kwargs.get("borders", [])
        # ---- stadium
        self.edges = self.defaults.get("edges", "east west")
        # ---- grid / card layout
        self.grid = None  # some Shapes can auto-generate a GridShape
        self.rows = self.defaults.get("rows", 0)
        self.cols = self.defaults.get("cols", self.defaults.get("columns", 0))
        self.frame = self.defaults.get("frame", "rectangle")
        self.offset = self.defaults.get("offset", 0)  # from margin
        self.offset_x = self.defaults.get("offset_x", self.offset)
        self.offset_y = self.defaults.get("offset_y", self.offset)
        self.spacing = self.defaults.get("spacing", 0)  # between cards
        self.spacing_x = self.defaults.get("spacing_x", self.spacing)
        self.spacing_y = self.defaults.get("spacing_y", self.spacing)
        self.grouping = self.defaults.get("grouping", 1)  # no. of cards in a set
        self.grouping_rows = self.defaults.get("grouping_rows", self.grouping)
        self.grouping_cols = self.defaults.get("grouping_cols", self.grouping)
        # ---- circle / star / polygon
        self.diameter = self.defaults.get("diameter", 1)
        self.radius = self.defaults.get("radius", self.diameter / 2.0)
        self.vertices = self.defaults.get("vertices", 5)
        self.sides = self.defaults.get("sides", 6)
        self.points = self.defaults.get("points", [])
        self.x_c = self.defaults.get("xc", 0)
        self.y_c = self.defaults.get("yc", 0)
        # ---- radii (circle, hex & polygon)
        self.radii = self.defaults.get("radii", [])
        self.radii_stroke = self.defaults.get("radii_stroke", self.stroke)
        self.radii_stroke_width = self.defaults.get(
            "radii_stroke_width", self.stroke_width
        )
        self.radii_length = self.defaults.get(
            "radii_length", None
        )  # default: circle radius
        self.radii_offset = self.defaults.get("radii_offset", 0)
        self.radii_cap = self.defaults.get("radii_cap", None)
        self.radii_dotted = self.defaults.get("radii_dotted", self.dotted)
        self.radii_dashed = self.defaults.get("radii_dashed", self.dashed)
        self.radii_labels = self.defaults.get("radii_labels", "")
        self.radii_labels_size = self.defaults.get("radii_labels_size", self.font_size)
        self.radii_labels_face = self.defaults.get("radii_labels_face", self.font_name)
        self.radii_labels_stroke = self.get_color(
            self.defaults.get("radii_labels_stroke"), self.stroke
        )
        self.radii_labels_stroke_width = self.defaults.get(
            "radii_labels_stroke_width", self.stroke_width
        )
        self.radii_labels_rotation = self.defaults.get("radii_labels_rotation", 0)
        # ---- circle
        self.petals = self.defaults.get("petals", 0)
        self.petals_style = self.defaults.get("petals_style", "triangle")
        self.petals_height = self.defaults.get("petals_height", 1)
        self.petals_offset = self.defaults.get("petals_offset", 0)
        self.petals_stroke = self.defaults.get("petals_stroke", self.stroke)
        self.petals_stroke_width = self.defaults.get(
            "petals_stroke_width", self.stroke_width
        )
        self.petals_fill = self.defaults.get("petals_fill", None)
        self.petals_dotted = self.defaults.get("petals_dotted", self.dotted)
        self.petals_dashed = self.defaults.get("petals_dashed", self.dashed)
        # ---- compass
        self.perimeter = self.defaults.get("perimeter", "circle")
        self.directions = self.defaults.get("directions", None)
        # ---- triangle / trapezoid
        self.flip = self.defaults.get("flip", "north")
        # ---- triangle
        self.hand = self.defaults.get("hand", "east")
        # ---- hexagon / circle
        self.centre_shape = self.defaults.get("centre_shape", "")
        self.centre_shape_mx = self.defaults.get("centre_shape_mx", 0)
        self.centre_shape_my = self.defaults.get("centre_shape_my", 0)
        self.dot = self.defaults.get("dot", 0)
        self.dot_stroke = self.get_color(self.defaults.get("dot_stroke"), self.stroke)
        self.dot_stroke_width = self.defaults.get("dot_stroke_width", self.stroke_width)
        self.dot_fill = self.defaults.get("dot_fill", self.dot_stroke)  # colors match
        self.cross = self.defaults.get("cross", 0)
        self.cross_stroke = self.get_color(self.defaults.get("cross_stroke"), black)
        self.cross_stroke_width = self.defaults.get(
            "cross_stroke_width", self.stroke_width
        )
        # ---- hexagon / polygon
        self.orientation = self.defaults.get("orientation", "flat")  # flat|pointy
        self.perbis = self.defaults.get("perbis", None)  # directions
        self.perbis_stroke = self.defaults.get("perbis_stroke", black)
        self.perbis_stroke_width = self.defaults.get(
            "perbis_stroke_width", self.stroke_width
        )
        self.perbis_length = self.defaults.get("perbis_length", None)
        self.perbis_offset = self.defaults.get("perbis_offset", 0)
        self.perbis_cap = self.defaults.get("perbis_cap", None)
        self.perbis_dotted = self.defaults.get("perbis_dotted", self.dotted)
        self.perbis_dashed = self.defaults.get("perbis_dashed", self.dashed)
        # ---- hexagon
        self.caltrops = self.defaults.get("caltrops", None)
        self.caltrops_fraction = self.defaults.get("caltrops_fraction", None)
        self.caltrops_invert = kwargs.get("caltrops_invert", False)
        self.links = self.defaults.get("links", None)
        self.link_stroke_width = self.defaults.get(
            "link_stroke_width", self.stroke_width
        )
        self.link_stroke = self.defaults.get("link_stroke", self.stroke)
        self.link_cap = self.defaults.get("link_cap", self.line_cap)
        # ---- hexagons
        self.hid = self.defaults.get("id", "")  # HEX ID
        self.hex_rows = self.defaults.get("hex_rows", 0)
        self.hex_cols = self.defaults.get("hex_cols", 0)
        self.hex_offset = self.defaults.get("hex_offset", "even")  # even|odd
        self.hex_layout = self.defaults.get("hex_layout", "rectangle")  # rectangle
        self.coord_type_x = self.defaults.get("coord_type_x", "number")  # number|letter
        self.coord_type_y = self.defaults.get("coord_type_y", "number")  # number|letter
        self.coord_start_x = self.defaults.get("coord_start_x", 0)
        self.coord_start_y = self.defaults.get("coord_start_y", 0)
        self.coord_elevation = self.defaults.get(
            "coord_elevation", None
        )  # top|middle|bottom
        self.coord_offset = self.defaults.get("coord_offset", 0)
        self.coord_font_name = self.defaults.get("coord_font_name", "Helvetica")
        self.coord_font_size = self.defaults.get(
            "coord_font_size", int(self.font_size * 0.5)
        )
        self.coord_stroke = self.get_color(self.defaults.get("coord_stroke"), black)
        self.coord_padding = self.defaults.get("coord_padding", 2)
        self.coord_separator = self.defaults.get("coord_separator", "")
        self.coord_prefix = self.defaults.get("coord_prefix", "")
        self.coord_suffix = self.defaults.get("coord_suffix", "")
        self.coord_style = self.defaults.get("coord_style", "")
        self.hidden = self.defaults.get("hidden", [])
        # ---- starfield
        self.enclosure = None
        self.colors = [white]
        self.sizes = [self.defaults.get("stroke_width", WIDTH)]
        self.density = self.defaults.get("density", 10)
        self.star_pattern = "random"
        self.seeding = self.defaults.get("seeding", None)
        # ---- mesh
        self.mesh = self.defaults.get("mesh", None)
        # ---- hatches
        self.hatch_count = self.defaults.get("hatch_count", 0)
        self.hatch = self.defaults.get("hatch", "*")
        self.hatch_stroke = self.defaults.get("hatch_stroke", self.stroke)
        self.hatch_stroke_width = self.defaults.get(
            "hatch_stroke_width", self.stroke_width
        )
        self.hatch_dots = self.defaults.get("hatch_dots", None)
        self.hatch_cap = self.defaults.get("hatch_cap", self.line_cap)
        self.hatch_dashed = self.defaults.get("hatch_dashed", None)  # ---- OTHER
        # defaults for attributes called/set elsewhere e.g. in draw()
        self.use_abs = False
        self.use_abs_1 = False
        self.use_abs_c = False
        self.clockwise = True
        # ---- deck
        self.deck_data = []

    def get_canvas(self):
        """Return reportlab canvas object"""
        return self.canvas

    def get_color(self, name=None, default=black):
        """Get a color by name from a pre-defined dictionary."""
        if name:
            if isinstance(name, Color):
                return name
            return COLORS.get(name, default)
        return default

    def get_units(self, name=None, default=cm):
        """Get units by name from a pre-defined dictionary."""
        if name and isinstance(name, str):
            return UNITS.get(name, default)
        if name and isinstance(name, float):
            return name
        return default

    def get_page(self, name=None, default=A4):
        """Get a paper format by name from a pre-defined dictionary."""
        if name:
            return PAGES.get(name, default)
        return default


class BaseShape:
    """Base class for objects that are drawn on a given canvas."""

    def __init__(self, _object=None, canvas=None, **kwargs):
        self.kwargs = kwargs
        # tools.feedback(f'*** BaseShape {kwargs=}')
        # ---- constants
        self.default_length = 1
        self.show_id = False  # True
        # ---- KEY
        # print(f" *** {canvas=}")
        self.canvas = canvas or BaseCanvas()  # BaseCanvas object
        cnv = self.canvas  # shortcut for use in getting defaults
        # log.debug("Base types %s %s %s",type(self.canvas), type(canvas), type(cnv))
        self._object = _object  # placeholder for an incoming Shape object
        self.shape_id = None
        self.stylesheet = getSampleStyleSheet()
        self.sequence = kwargs.get("sequence", [])  # e.g. card numbers
        self.dataset = []  # list of dict data (loaded from file)
        self.members = []  # card IDs, of which current card is a member
        # ---- general
        self.common = kwargs.get("common", None)
        self.shape = kwargs.get("shape", cnv.shape)
        self.run_debug = kwargs.get("debug", cnv.run_debug)
        self.units = kwargs.get("units", cnv.units)
        # print(f" *** {self.units=}")
        # ---- paper & margins
        self.paper = kwargs.get("paper") or cnv.paper
        self.margin = self.kw_float(kwargs.get("margin", cnv.margin))
        self.margin_top = self.kw_float(kwargs.get("margin_top", self.margin))
        self.margin_bottom = self.kw_float(kwargs.get("margin_bottom", self.margin))
        self.margin_left = self.kw_float(kwargs.get("margin_left", self.margin))
        self.margin_right = self.kw_float(kwargs.get("margin_right", self.margin))
        # ---- grid marks
        self.grid_marks = self.kw_float(kwargs.get("grid_marks", cnv.grid_marks))
        self.grid_stroke = kwargs.get("grid_stroke", cnv.grid_stroke)
        self.grid_stroke_width = self.kw_float(
            kwargs.get("grid_stroke_width", cnv.grid_stroke_width)
        )
        self.grid_length = self.kw_float(kwargs.get("grid_length", cnv.grid_length))
        self.page_width = self.paper[0] / self.units
        self.page_height = self.paper[1] / self.units
        # ---- sizes and positions
        self.row = kwargs.get("row", cnv.row)
        self.col = self.kw_int(kwargs.get("col", kwargs.get("column", cnv.col)))
        self.side = self.kw_float(kwargs.get("side", cnv.side))  # equal length sides
        self.height = self.kw_float(kwargs.get("height", self.side))
        self.width = self.kw_float(kwargs.get("width", self.side))
        self.top = self.kw_float(kwargs.get("top", cnv.top))
        self.depth = self.kw_float(kwargs.get("depth", self.side))  # diamond
        self.x = self.kw_float(kwargs.get("x", kwargs.get("left", cnv.x)))
        self.y = self.kw_float(kwargs.get("y", kwargs.get("bottom", cnv.y)))
        self.cx = self.kw_float(kwargs.get("cx", cnv.cx))  # centre (for some shapes)
        self.cy = self.kw_float(kwargs.get("cy", cnv.cy))  # centre (for some shapes)
        self.scaling = self.kw_float(kwargs.get("scaling", None))  # SVG images
        self.dot_point = self.kw_float(kwargs.get("dot_point", cnv.dot_point))  # points
        # ---- to be calculated ...
        self.area = cnv.area
        self.vertices = cnv.vertices
        # ---- repeats
        self.pattern = kwargs.get("pattern", cnv.pattern)
        self.repeat = kwargs.get("repeat", cnv.repeat)
        self.interval = self.kw_float(kwargs.get("interval", cnv.interval))
        self.interval_x = self.kw_float(kwargs.get("interval_x", cnv.interval_x))
        self.interval_y = self.kw_float(kwargs.get("interval_y", cnv.interval_y))
        # ---- rotation / position /elevation
        self.rotation = self.kw_float(
            kwargs.get("rotation", kwargs.get("rotation", cnv.rotation))
        )  # degree
        self._rotation_theta = math.radians(self.rotation or 0)  # radians
        self.direction = kwargs.get("direction", cnv.direction)
        self.position = kwargs.get("position", cnv.position)
        self.elevation = kwargs.get("elevation", cnv.elevation)
        self.facing = kwargs.get("facing", cnv.facing)
        # ---- line style
        self.line_width = self.kw_float(kwargs.get("line_width", cnv.line_width))
        self.line_cap = kwargs.get("line_cap", cnv.line_cap)
        self.dotted = kwargs.get("dotted", kwargs.get("dots", cnv.dotted))
        self.dashed = kwargs.get("dashed", None)
        # ---- fill color
        self.fill = kwargs.get("fill", kwargs.get("fill_color", cnv.fill))
        # ---- stroke
        self.stroke = kwargs.get("stroke", kwargs.get("stroke_color", cnv.stroke))
        self.fill_stroke = kwargs.get("fill_stroke", cnv.fill_stroke)
        self.outline = kwargs.get("outline", cnv.outline)
        self.stroke_width = self.kw_float(kwargs.get("stroke_width", cnv.stroke_width))
        # ---- overwrite fill&stroke colors
        if self.fill_stroke and self.outline:
            tools.feedback("Cannot set 'fill_stroke' and 'outline' together!", True)
        if self.fill_stroke:
            self.stroke = self.fill_stroke
            self.fill = self.fill_stroke
        if self.outline:
            self.stroke = self.outline
            self.fill = None
        # ---- debug color & transparency
        self.debug_color = kwargs.get("debug_color", cnv.debug_color)
        self.transparency = self.kw_float(kwargs.get("transparency", cnv.transparency))
        # ---- font
        self.font_name = kwargs.get("font_name", cnv.font_name)
        self.font_size = self.kw_float(kwargs.get("font_size", cnv.font_size))
        self.font_style = kwargs.get("font_style", cnv.font_style)
        self.font_directory = kwargs.get("font_directory", cnv.font_directory)
        self.style = kwargs.get("style", cnv.style)  # Normal? from reportlab
        self.wrap = kwargs.get("wrap", cnv.wrap)
        self.align = kwargs.get("align", cnv.align)  # centre,left,right,justify
        self._alignment = TA_LEFT  # see to_alignment()
        # ---- text: base
        self.text = kwargs.get("text", cnv.text)
        self.text_size = self.kw_float(kwargs.get("text_size", cnv.text_size))
        self.text_stroke = kwargs.get("text_stroke", cnv.text_stroke)
        self.text_stroke_width = self.kw_float(
            kwargs.get("text_stroke_width", cnv.text_stroke_width)
        )
        # ---- text: label
        self.label = kwargs.get("label", cnv.label)
        self.label_size = self.kw_float(kwargs.get("label_size", self.font_size))
        self.label_face = kwargs.get("label_face", self.font_name)
        self.label_stroke = kwargs.get("label_stroke", self.stroke)
        self.label_stroke_width = self.kw_float(
            kwargs.get("label_stroke_width", self.stroke_width)
        )
        self.label_mx = self.kw_float(kwargs.get("label_mx", 0))
        self.label_my = self.kw_float(kwargs.get("label_my", 0))
        self.label_rotation = self.kw_float(kwargs.get("label_rotation", 0))
        # ---- text: title
        self.title = kwargs.get("title", cnv.title)
        self.title_size = self.kw_float(kwargs.get("title_size", self.font_size))
        self.title_face = kwargs.get("title_face", self.font_name)
        self.title_stroke = kwargs.get("title_stroke", self.stroke)
        self.title_stroke_width = self.kw_float(
            kwargs.get("title_stroke_width", self.stroke_width)
        )
        self.title_mx = self.kw_float(kwargs.get("title_mx", 0))
        self.title_my = self.kw_float(kwargs.get("title_my", 0))
        self.title_rotation = self.kw_float(kwargs.get("title_rotation", 0))
        # ---- text: heading
        self.heading = kwargs.get("heading", cnv.heading)
        self.heading_size = self.kw_float(kwargs.get("heading_size", self.font_size))
        self.heading_face = kwargs.get("heading_face", self.font_name)
        self.heading_stroke = kwargs.get("heading_stroke", self.stroke)
        self.heading_stroke_width = self.kw_float(
            kwargs.get("heading_stroke_width", self.stroke_width)
        )
        self.heading_mx = self.kw_float(kwargs.get("heading_mx", 0))
        self.heading_my = self.kw_float(kwargs.get("heading_my", 0))
        self.heading_rotation = self.kw_float(kwargs.get("heading_rotation", 0))
        # ---- text block
        self.outline_stroke = kwargs.get("outline_stroke", cnv.outline_stroke)
        self.outline_width = self.kw_float(
            kwargs.get("outline_width", cnv.outline_width)
        )
        self.leading = self.kw_float(kwargs.get("leading", self.font_size))
        self.transform = kwargs.get("transform", cnv.transform)
        # tools.feedback(f"+++ BShp:{self} init {kwargs.get('fill')=} {self.fill=} {kwargs.get('fill_color')=}")
        # ---- image / file
        self.source = kwargs.get("source", cnv.source)  # file or http://
        self.sliced = ""
        self.image_location = None
        # ---- line / ellipse / bezier / arc / polygon
        self.length = self.kw_float(kwargs.get("length", cnv.length))
        self.angle = self.kw_float(
            kwargs.get("angle", cnv.angle)
        )  # anti-clock from flat
        self.angle_width = self.kw_float(
            kwargs.get("angle_width", cnv.angle_width)
        )  # delta degrees
        self._angle_theta = math.radians(self.angle)
        # ---- image
        self.cache_directory = None  # should be a pathlib.Path object
        # ---- chord
        self.angle_1 = self.kw_float(
            kwargs.get("angle1", cnv.angle_1)
        )  # anti-clock from flat
        self._angle_1_theta = math.radians(self.angle_1)
        # ---- arrow shape: head, points and tail
        self.points_offset = self.kw_float(
            kwargs.get("points_offset", cnv.points_offset)
        )
        self.head_height = self.kw_float(kwargs.get("head_height", cnv.head_height))
        self.head_width = self.kw_float(kwargs.get("head_width", cnv.head_width))
        self.tail_width = self.kw_float(kwargs.get("tail_width", cnv.tail_width))
        self.tail_notch = self.kw_float(kwargs.get("tail_notch", cnv.tail_notch))
        # TODO arrow-on-a-line
        self.arrow_style = kwargs.get("arrow_style", cnv.arrow_style)
        self.arrow_tail_style = kwargs.get("arrow_tail_style", cnv.arrow_tail_style)
        # ---- line / bezier / sector
        self.x_1 = self.kw_float(kwargs.get("x1", cnv.x_1))
        self.y_1 = self.kw_float(kwargs.get("y1", cnv.y_1))
        # ---- bezier / sector
        self.x_2 = self.kw_float(kwargs.get("x2", cnv.x_2))
        self.y_2 = self.kw_float(kwargs.get("y2", cnv.y_2))
        self.x_3 = self.kw_float(kwargs.get("x3", cnv.x_3))
        self.y_3 = self.kw_float(kwargs.get("y3", cnv.y_3))
        # ---- rectangle / card
        self.rounding = self.kw_float(kwargs.get("rounding", cnv.rounding))
        self.rounded = kwargs.get("rounded", cnv.rounded)
        self.notch = self.kw_float(kwargs.get("notch", cnv.notch))
        self.notch_corners = kwargs.get("notch_corners", cnv.notch_corners)
        self.notch_x = self.kw_float(kwargs.get("notch_x", cnv.notch_x))
        self.notch_y = self.kw_float(kwargs.get("notch_y", cnv.notch_y))
        self.notch_style = kwargs.get("notch_style", cnv.notch_style)
        self.chevron = kwargs.get("chevron", cnv.chevron)
        self.chevron_height = self.kw_float(
            kwargs.get("chevron_height", cnv.chevron_height)
        )
        self.peaks = kwargs.get("peaks", cnv.peaks)
        self.peaks_dict = {}
        self.borders = kwargs.get("borders", cnv.borders)
        # ---- stadium
        self.edges = kwargs.get("edges", cnv.edges)
        # ---- grid / card layout
        self.rows = self.kw_int(kwargs.get("rows", cnv.rows))
        self.cols = self.kw_int(kwargs.get("cols", kwargs.get("columns", cnv.cols)))
        self.frame = kwargs.get("frame", cnv.frame)
        self.offset = self.kw_float(kwargs.get("offset", cnv.offset))
        self.offset_x = self.kw_float(kwargs.get("offset_x", self.offset))
        self.offset_y = self.kw_float(kwargs.get("offset_y", self.offset))
        self.spacing = self.kw_float(kwargs.get("spacing", cnv.spacing))
        self.spacing_x = self.kw_float(kwargs.get("spacing_x", self.spacing))
        self.spacing_y = self.kw_float(kwargs.get("spacing_y", self.spacing))
        self.grouping = self.kw_int(kwargs.get("grouping", 1))  # no. of cards in a set
        self.grouping_rows = self.kw_int(kwargs.get("grouping_rows", self.grouping))
        self.grouping_cols = self.kw_int(kwargs.get("grouping_cols", self.grouping))
        # ---- circle / star / polygon
        self.diameter = self.kw_float(kwargs.get("diameter", cnv.diameter))
        self.radius = self.kw_float(kwargs.get("radius", cnv.radius))
        self.vertices = self.kw_int(kwargs.get("vertices", cnv.vertices))
        self.sides = kwargs.get("sides", cnv.sides)
        self.points = kwargs.get("points", cnv.points)
        # ---- radii (circle / hexagon / polygon / compass)
        self.radii = kwargs.get("radii", cnv.radii)
        self.radii_stroke = kwargs.get("radii_stroke", self.stroke)
        self.radii_stroke_width = self.kw_float(
            kwargs.get("radii_stroke_width", cnv.radii_stroke_width)
        )
        self.radii_length = self.kw_float(kwargs.get("radii_length", cnv.radii_length))
        self.radii_offset = self.kw_float(kwargs.get("radii_offset", cnv.radii_offset))
        self.radii_cap = kwargs.get("radii_cap", cnv.radii_cap)
        self.radii_dotted = kwargs.get("radii_dotted", cnv.dotted)
        self.radii_dashed = kwargs.get("radii_dashed", cnv.dashed)
        self.radii_labels = kwargs.get("radii_labels", cnv.radii_labels)
        self.radii_labels_size = self.kw_float(
            kwargs.get("radii_labels_size", self.font_size)
        )
        self.radii_labels_face = kwargs.get("radii_labels_face", self.font_name)
        self.radii_labels_stroke = kwargs.get("radii_labels_stroke", self.stroke)
        self.radii_labels_stroke_width = self.kw_float(
            kwargs.get("radii_labels_stroke_width", self.stroke_width)
        )
        self.radii_labels_rotation = self.kw_float(
            kwargs.get("radii_labels_rotation", 0)
        )
        # ---- circle
        self.petals = self.kw_int(kwargs.get("petals", cnv.petals))
        self.petals_style = kwargs.get("petals_style", cnv.petals_style)
        self.petals_height = self.kw_float(
            kwargs.get("petals_height", cnv.petals_height)
        )
        self.petals_offset = self.kw_float(
            kwargs.get("petals_offset", cnv.petals_offset)
        )
        self.petals_stroke = kwargs.get("petals_stroke", cnv.petals_stroke)
        self.petals_stroke_width = self.kw_float(
            kwargs.get("petals_stroke_width", cnv.petals_stroke_width)
        )
        self.petals_fill = kwargs.get("petals_fill", cnv.petals_fill)
        self.petals_dotted = kwargs.get("petals_dotted", cnv.petals_dotted)
        self.petals_dashed = kwargs.get("petals_dashed", cnv.petals_dashed)
        # ---- compass
        self.perimeter = kwargs.get("perimeter", "circle")  # circle|rectangle|hexagon
        self.directions = kwargs.get("directions", None)
        # ---- triangle / trapezoid
        self.flip = kwargs.get("flip", "north")
        # ---- triangle
        self.hand = kwargs.get("hand", "east")
        # ---- hexagon / circle / polygon
        self.centre_shape = kwargs.get("centre_shape", "")
        self.centre_shape_mx = self.kw_float(
            kwargs.get("centre_shape_mx", cnv.centre_shape_mx)
        )
        self.centre_shape_my = self.kw_float(
            kwargs.get("centre_shape_my", cnv.centre_shape_my)
        )
        self.dot_stroke = kwargs.get("dot_stroke", self.stroke)
        self.dot_stroke_width = self.kw_float(
            kwargs.get("dot_stroke_width", cnv.dot_stroke_width)
        )
        self.dot_fill = kwargs.get("dot_fill", self.stroke)
        self.dot = self.kw_float(kwargs.get("dot", cnv.dot))
        self.cross_stroke = kwargs.get("cross_stroke", self.stroke)
        self.cross_stroke_width = self.kw_float(
            kwargs.get("cross_stroke_width", cnv.cross_stroke_width)
        )
        self.cross = self.kw_float(kwargs.get("cross", cnv.cross))
        # ---- hexagon / polygon
        self.orientation = kwargs.get("orientation", cnv.orientation)
        self.perbis = kwargs.get("perbis", cnv.perbis)  # directions
        self.perbis_stroke = kwargs.get("perbis_stroke", cnv.perbis_stroke)
        self.perbis_stroke_width = self.kw_float(
            kwargs.get("perbis_stroke_width", cnv.perbis_stroke_width)
        )
        self.perbis_length = self.kw_float(
            kwargs.get("perbis_length", cnv.perbis_length)
        )
        self.perbis_offset = self.kw_float(
            kwargs.get("perbis_offset", cnv.perbis_offset)
        )
        self.perbis_cap = kwargs.get("perbis_cap", cnv.perbis_cap)
        self.perbis_dotted = kwargs.get("perbis_dotted", cnv.dotted)
        self.perbis_dashed = kwargs.get("perbis_dashed", cnv.dashed)
        # ---- hexagon
        self.caltrops = kwargs.get("caltrops", cnv.caltrops)
        self.caltrops_fraction = self.kw_float(
            kwargs.get("caltrops_fraction", cnv.caltrops_fraction)
        )
        self.caltrops_invert = kwargs.get("caltrops_invert", cnv.caltrops_invert)
        self.links = kwargs.get("links", cnv.links)
        self.link_stroke_width = self.kw_float(
            kwargs.get("link_stroke_width", cnv.link_stroke_width)
        )
        self.link_stroke = kwargs.get("link_stroke", cnv.stroke)
        self.link_cap = kwargs.get("link_cap", cnv.link_cap)
        # ---- hexagons
        self.hid = kwargs.get("id", cnv.hid)  # HEX ID
        self.hex_rows = self.kw_int(kwargs.get("hex_rows", cnv.hex_rows))
        self.hex_cols = self.kw_int(kwargs.get("hex_cols", cnv.hex_cols))
        self.hex_layout = kwargs.get(
            "hex_layout", cnv.hex_layout
        )  # rectangle|circle|diamond|triangle
        self.hex_offset = kwargs.get("hex_offset", cnv.hex_offset)  # even|odd
        self.coord_type_x = kwargs.get(
            "coord_type_x", cnv.coord_type_x
        )  # number|letter
        self.coord_type_y = kwargs.get(
            "coord_type_y", cnv.coord_type_y
        )  # number|letter
        self.coord_start_x = self.kw_int(kwargs.get("coord_start_x", cnv.coord_start_x))
        self.coord_start_y = self.kw_int(kwargs.get("coord_start_y", cnv.coord_start_y))
        self.coord_elevation = kwargs.get(
            "coord_elevation", cnv.coord_elevation
        )  # top|middle|bottom
        self.coord_offset = self.kw_float(kwargs.get("coord_offset", cnv.coord_offset))
        self.coord_font_name = kwargs.get("coord_font_name", cnv.coord_font_name)
        self.coord_font_size = self.kw_float(
            kwargs.get("coord_font_size", cnv.coord_font_size)
        )
        self.coord_stroke = kwargs.get("coord_stroke", cnv.coord_stroke)
        self.coord_padding = self.kw_int(kwargs.get("coord_padding", cnv.coord_padding))
        self.coord_separator = kwargs.get("coord_separator", cnv.coord_separator)
        self.coord_prefix = kwargs.get("coord_prefix", cnv.coord_prefix)
        self.coord_suffix = kwargs.get("coord_suffix", cnv.coord_suffix)
        self.coord_style = kwargs.get("coord_style", "")  # linear|diagonal
        self.hidden = kwargs.get("hidden", cnv.hidden)
        # ---- starfield
        self.enclosure = kwargs.get("enclosure", cnv.enclosure)
        self.colors = kwargs.get("colors", cnv.colors)
        self.sizes = kwargs.get("sizes", cnv.sizes)
        self.density = self.kw_int(kwargs.get("density", cnv.density))
        self.star_pattern = kwargs.get("star_pattern", cnv.star_pattern)
        self.seeding = kwargs.get("seeding", cnv.seeding)
        # ---- mesh
        self.mesh = kwargs.get("mesh", cnv.mesh)
        # ---- hatches
        self.hatch_count = kwargs.get("hatch_count", cnv.hatch_count)
        self.hatch = kwargs.get("hatch", cnv.hatch)
        self.hatch_stroke_width = self.kw_float(
            kwargs.get("hatch_width", cnv.hatch_stroke_width)
        )
        self.hatch_stroke = kwargs.get("hatch_stroke", cnv.stroke)
        self.hatch_cap = kwargs.get("hatch_cap", cnv.hatch_cap)
        self.hatch_dots = kwargs.get("hatch_dots", cnv.dotted)
        self.hatch_dashed = kwargs.get("hatch_dashed", cnv.dashed)
        # ---- deck
        self.deck_data = kwargs.get("deck_data", [])  # list of dicts

        # ---- OTHER
        # defaults for attributes called/set elsewhere e.g. in draw()
        self.use_abs = False
        self.use_abs_1 = False
        self.use_abs_c = False
        # ---- CHECK ALL
        correct, issue = self.check_settings()
        if not correct:
            tools.feedback("Problem with settings: %s." % "; ".join(issue))
        # ---- UPDATE SELF WITH COMMON
        if self.common:
            try:
                attrs = vars(self.common)
            except TypeError:
                tools.feedback(
                    f'Cannot process the Common property "{self.common}"'
                    " - please check!",
                    True,
                )
            for attr in attrs.keys():
                if (
                    attr not in ["canvas", "common", "stylesheet", "kwargs"]
                    and attr[0] != "_"
                ):
                    # tools.feedback(f'{attr=}')
                    common_attr = getattr(self.common, attr)
                    base_attr = getattr(BaseCanvas(), attr)
                    if common_attr != base_attr:
                        setattr(self, attr, common_attr)

        # ---- SET offset properties to correct units
        self._o = self.set_offset_props()
        # ---- SET UNIT PROPS (last!)
        self.set_unit_properties()

    def __str__(self):
        try:
            return f"{self.__class__.__name__}::{self.kwargs}"
        except:
            return f"{self.__class__.__name__}"

    def kw_float(self, value, label: str = ""):
        return tools.as_float(value, label) if value is not None else value

    def kw_int(self, value, label: str = ""):
        return tools.as_int(value, label) if value is not None else value

    def unit(self, item, units=None, skip_none=False, label=""):
        """Convert an item into the appropriate unit system."""
        log.debug("units %s %s :: label: %s", units, self.units, label)
        if item is None and skip_none:
            return None
        if not units:
            units = self.units
        try:
            _item = tools.as_float(item, label)
            return _item * units
        except (TypeError, ValueError):
            _label = f" {label}" if label else ""
            tools.feedback(
                f"Unable to set unit value for{_label}: {item}."
                " Please check that this is a valid value.",
                stop=True,
            )

    def set_unit_properties(self):
        """Convert base properties into unit-based values."""
        # set a "width" value for use in calculations e.g. Track
        if self.radius and not self.width:
            self.width = 2.0 * self.radius
            self.diameter = 2.0 * self.radius
        if self.diameter and not self.width:
            self.width = self.diameter
        if self.side and not self.width:
            self.width = self.side  # square
        if self.side and not self.height:
            self.height = self.side  # square
        if self.diameter and not self.radius:
            self.radius = self.diameter / 2.0
        if self.width and not self.top:
            self.top = 0.5 * self.width

        self._u = UnitProperties(
            self.paper[0],  # width, in points
            self.paper[1],  # height, in points
            self.unit(self.margin_left) if self.margin_left is not None else None,
            self.unit(self.margin_right) if self.margin_right is not None else None,
            self.unit(self.margin_bottom) if self.margin_bottom is not None else None,
            self.unit(self.margin_top) if self.margin_top else None,
            self.unit(self.x) if self.x is not None else None,
            self.unit(self.y) if self.y is not None else None,
            self.unit(self.cx) if self.cx is not None else None,
            self.unit(self.cy) if self.cy is not None else None,
            self.unit(self.height) if self.height is not None else None,
            self.unit(self.width) if self.width is not None else None,
            self.unit(self.top) if self.top is not None else None,
            self.unit(self.radius) if self.radius is not None else None,
            self.unit(self.diameter) if self.diameter is not None else None,
            self.unit(self.side) if self.side is not None else None,
            self.unit(self.length) if self.length is not None else None,
            self.unit(self.spacing_x) if self.spacing_x is not None else None,
            self.unit(self.spacing_y) if self.spacing_y is not None else None,
            self.unit(self.offset_x) if self.offset_x is not None else None,
            self.unit(self.offset_y) if self.offset_y is not None else None,
        )

    def set_offset_props(self, off_x=0, off_y=0):
        """Get OffsetProperties for a Shape."""
        margin_left = (
            self.unit(self.margin_left) if self.margin_left is not None else self.margin
        )
        margin_bottom = (
            self.unit(self.margin_bottom)
            if self.margin_bottom is not None
            else self.margin
        )
        off_x = self.unit(off_x) if off_x is not None else None
        off_y = self.unit(off_y) if off_y is not None else None
        return OffsetProperties(
            off_x, off_y, off_x + margin_left, off_y + margin_bottom
        )

    def set_canvas_props(
        self,
        cnv=None,
        index=None,  # extract from list of potential values (usually Card options)
        fill=None,  # reserve None for 'no fill at all'
        stroke=None,
        stroke_width=None,
        stroke_cap=None,
        dotted=None,
        dashed=None,
        debug=False,
    ):
        """Set Reportlab canvas properties for fill, font, line and colors"""

        def ext(prop):
            if isinstance(prop, str):
                return prop
            try:
                return prop[index]
            except TypeError:
                return prop

        canvas = cnv if cnv else self.canvas.canvas
        try:
            canvas.setFont(ext(self.font_name), ext(self.font_size))
        except AttributeError:
            pass
        except KeyError:
            ff = ext(self.font_name)
            try:
                tools.register_font(
                    font_name=self.font_name,
                    style=self.font_style,
                    directory=self.font_directory,
                )
            except (KeyError, ValueError, TTFError):
                _style = f' with style "{self.font_style}"' if self.font_style else ""
                _dir = f' in "{self.font_directory}"' if self.font_directory else ""
                tools.feedback(
                    f'Unable to find or register font "{ff}"{_style}{_dir}.'
                    " Please check that it is available on your system.",
                    stop=True,
                )
        try:
            if fill in [None, []] and self.fill in [None, []]:
                canvas.setFillColor(white, 0)  # full transparency
                if debug:
                    tools.feedback("~~~ NO fill color set!")
            else:
                _fill = ext(fill) or ext(self.fill)
                canvas.setFillColor(_fill)
                _transparency = ext(self.transparency)
                if _transparency:
                    try:
                        alpha = float(_transparency) / 100.0
                    except Exception:
                        tools.feedback(
                            f'Unable to use "{_transparency}" as transparency'
                            " value - it must be from 1 to 100",
                            True,
                        )
                    try:
                        curr_fill = canvas._fillColorObj
                        alpha_fill = Color(
                            curr_fill.red, curr_fill.green, curr_fill.blue, alpha
                        )
                        if debug:
                            tools.feedback(
                                f"~ Transp. color set: {alpha_fill} vs {_fill}"
                            )
                        _fill = alpha_fill
                        canvas.setFillColor(_fill)
                    except Exception:
                        tools.feedback("Unable to set transparency for {_fill}")
                if debug:
                    tools.feedback(f"~~~ Fill color set: {_fill}")

        except (ValueError, AttributeError):
            issue = f'"{_fill}" is not a valid value' if _fill else "no value provided!"
            tools.feedback(f"Unable to set fill color:- {issue}", True)

        try:
            if stroke in [None, []] and self.stroke in [None, []]:
                canvas.setStrokeColor(black, 0)  # full transparency
                if debug:
                    tools.feedback("~~~ NO stroke color set!")
            else:
                _strk = ext(stroke) or ext(self.stroke)
                canvas.setStrokeColor(_strk)
        except (TypeError, ValueError):
            tools.feedback(
                f'Please check the stroke setting of "{_strk}"; it should be a color value.'
            )
        except AttributeError:
            pass
        try:
            the_stwd = ext(stroke_width) or ext(self.stroke_width)
            canvas.setLineWidth(the_stwd)  # units are points!
        except TypeError:
            tools.feedback(
                f'Please check the stroke_width setting of "{the_stwd}";'
                " it should be a number."
            )
        except AttributeError:
            pass
        # ---- line cap
        _stroke_cap = ext(stroke_cap)
        if _stroke_cap:
            if _stroke_cap in ["r", "rounded"]:
                canvas.setLineCap(1)
            elif _stroke_cap in ["s", "square"]:
                canvas.setLineCap(2)
            else:
                tools.feedback(f'Line cap type "{_stroke_cap}" cannot be used.', False)
        # ---- set line dots / dashed
        _dotted = ext(dotted) or ext(self.dotted)
        _dashed = ext(dashed) or ext(self.dashed)
        if _dotted:
            # _dots = self.values_to_points([0.03, 0.03])
            _dots = [the_stwd, the_stwd]
            canvas.setDash(array=_dots)
        elif _dashed:
            dash_points = self.values_to_points(_dashed)
            canvas.setDash(array=dash_points)
        else:
            canvas.setDash(array=[])

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw an element on a given canvas."""
        self._o = self.set_offset_props(off_x, off_y)
        # self._abs... variable are absolute locations in native units;
        #  They are for internal use only and are not expected
        #  to be called by the user.
        #  If set, they should be used to ignore/bypass any other values
        #  for calculating the starting point or centre point
        #  for drawing a shape
        self._abs_x = kwargs.get("_abs_x", None)
        self._abs_y = kwargs.get("_abs_y", None)
        self._abs_x1 = kwargs.get("_abs_x1", None)
        self._abs_y1 = kwargs.get("_abs_y1", None)
        self._abs_cx = kwargs.get("_abs_cx", None)
        self._abs_cy = kwargs.get("_abs_cy", None)
        self.use_abs = (
            True if self._abs_x is not None and self._abs_y is not None else False
        )
        self.use_abs_1 = (
            True if self._abs_x1 is not None and self._abs_y1 is not None else False
        )
        self.use_abs_c = (
            True if self._abs_cx is not None and self._abs_cy is not None else False
        )
        # tools.feedback(f'*** draw baseshape: {self._abs_x=} {self._abs_y=} {self._abs_cx=} {self._abs_cy=}')

    def check_settings(self) -> tuple:
        """Check that the user-supplied parameters for choices are correct"""
        correct = True
        issue = []
        if self.align:
            if str(self.align).lower() not in [
                "left",
                "right",
                "justify",
                "centre",
                "l",
                "r",
                "j",
                "c",
            ]:
                issue.append(f'"{self.align}" is an invalid align!')
                correct = False
        if self.caltrops:
            if str(self.caltrops).lower() not in [
                "large",
                "medium",
                "small",
                "s",
                "m",
                "l",
            ]:
                issue.append(f'"{self.caltrops}" is an invalid caltrops size!')
                correct = False
        if self.edges:
            if not isinstance(self.edges, list):
                _edges = self.edges.split()
            else:
                _edges = self.edges
            for edge in _edges:
                if str(edge).lower() not in [
                    "north",
                    "south",
                    "east",
                    "west",
                    "n",
                    "e",
                    "w",
                    "s",
                ]:
                    issue.append(f'"{edge}" is an invalid choice in {self.edges}!')
                    correct = False
        if self.flip:
            if str(self.flip).lower() not in ["north", "south", "n", "s"]:
                issue.append(f'"{self.flip}" is an invalid flip!')
                correct = False
        if self.hand:
            if str(self.hand).lower() not in [
                "west",
                "east",
                "w",
                "e",
            ]:
                issue.append(f'"{self.hand}" is an invalid hand!')
                correct = False
        if self.elevation:
            if str(self.elevation).lower() not in [
                "vertical",
                "horizontal",
                "v",
                "h",
            ]:
                issue.append(f'"{self.elevation}" is an invalid elevation!')
                correct = False
        if self.orientation:
            if str(self.orientation).lower() not in ["flat", "pointy", "f", "p"]:
                issue.append(f'"{self.orientation}" is an invalid orientation!')
                correct = False
        if self.perimeter:
            if str(self.perimeter).lower() not in [
                "circle",
                "rectangle",
                "hexagon",
                "c",
                "r",
                "h",
            ]:
                issue.append(f'"{self.perimeter}" is an invalid perimeter!')
                correct = False
        if self.position:
            if str(self.position).lower() not in [
                "top",
                "bottom",
                "center",
                "middle",
                "t",
                "b",
                "c",
                "m",
            ]:
                issue.append(f'"{self.position}" is an invalid position!')
                correct = False
        if self.petals_style:
            if str(self.petals_style).lower() not in [
                "triangle",
                "curve",
                "rectangle",
                "petal",
                "t",
                "c",
                "r",
                "p",
            ]:
                issue.append(f'"{self.petals_style}" is an invalid petals style!')
                correct = False
        # ---- hexagons
        if self.coord_style:
            if str(self.coord_style).lower() not in ["linear", "diagonal", "l", "d"]:
                issue.append(f'"{self.coord_style}" is an invalid coord style!')
                correct = False
        # ---- line arrows
        if self.arrow_style:
            if str(self.arrow_style).lower() not in [
                "line",
                "l",
                "line2",
                "l2",
                "line3",
                "l3",
                "triangle",
                "t",
                "diamond",
                "d",
                "notch",
                "n",
                "spear",
                "s",
                "circle",
                "c",
            ]:
                issue.append(f'"{self.arrow_style}" is an invalid arrow style!')
                correct = False
        if self.arrow_tail_style:
            if str(self.arrow_tail_style).lower() not in [
                "line",
                "l",
                "line2",
                "l2",
                "line3",
                "l3",
                "feather",
                "f",
                "circle",
                "c",
            ]:
                issue.append(
                    f'"{self.arrow_tail_style}" is an invalid arrow tail style!'
                )
                correct = False
        # ---- starfield
        if self.star_pattern:
            if str(self.star_pattern).lower() not in ["random", "cluster", "r", "c"]:
                issue.append(f'"{self.pattern}" is an invalid starfield pattern!')
                correct = False
        # ---- rectangle - notches
        if self.notch_style:
            if str(self.notch_style).lower() not in [
                "snip",
                "s",
                "fold",
                "o",
                "bite",
                "b",
                "flap",
                "l",
                "step",
                "t",
            ]:
                issue.append(f'"{self.notch_style}" is an invalid notch_style!')
                correct = False
        # ---- rectangle - peaks
        if self.peaks:
            if not isinstance(self.peaks, list):
                tools.feedback(f"The peaks '{self.peaks}' is not a valid list!", True)
            for point in self.peaks:
                try:
                    _dir = point[0]
                    value = tools.as_float(point[1], " peaks value")
                    if _dir.lower() not in ["n", "e", "w", "s", "*"]:
                        tools.feedback(
                            f'The peaks direction must be one of n, e, s, w (not "{_dir}")!',
                            True,
                        )
                    if _dir == "*":
                        self.peaks_dict["n"] = value
                        self.peaks_dict["e"] = value
                        self.peaks_dict["w"] = value
                        self.peaks_dict["s"] = value
                    else:
                        self.peaks_dict[_dir] = value
                except Exception:
                    tools.feedback(f'The peaks setting "{point}" is not valid!', True)

        return correct, issue

    def to_alignment(self) -> Enum:
        """Convert local, English-friendly alignments to a Reportlab Enum."""
        if self.align == "centre" or self.align == "center":
            self._alignment = TA_CENTER
        elif self.align == "right":
            self._alignment = TA_RIGHT
        elif self.align == "justify":
            self._alignment = TA_JUSTIFY
        else:
            self._alignment = TA_LEFT
        return self._alignment

    def is_kwarg(self, value) -> bool:
        """Validate if value is in direct kwargs OR in Common _kwargs."""
        if value in self.kwargs:
            return True
        if "common" in self.kwargs:
            if value in self.kwargs["common"]._kwargs:
                return True
        return False

    def load_image(
        self,
        image_location=None,
        scaling: float = None,
        sliced: str = None,
        width_height: tuple = None,
        cache_directory: str = None,
    ) -> tuple:
        """Load an image from file or website.

        Attempt to use local cache directory to retrieve an image
        for web-based assets, if possible.

        If image_location not found; try path in which script located.

        Args:
            image_location:
                full path or URL for image
            scaling:
                resize factor for image
            sliced:
                what fraction of the image to return; one of
                't', 'm', 'b', 'l', 'c', or 'r'
            width_height:
                the (width, height) of the output frame for the image
            cache_directory:
                where to store a local for copy for URL-sourced images

        Returns:
            tuple:
                * Image or SVG;
                * boolean (True if file type is SVG);
                * boolean (True if flie is a directory)

        Notes:
            * https://www.blog.pythonlibrary.org/2018/04/12/adding-svg-files-in-reportlab/
        """

        def slice_image(
            drawing, slice_portion: str = None, width_height: tuple = (1, 1)
        ):
            """Slice off a portion of an image while maintaining its aspect ratio

            Args:
                sliced:
                    what portion of the image to return
                width_height:
                    the (width, height) of the output frame for the image
            """
            if not slice_portion:
                return None
            try:
                _slice = slice_portion.lower()
                if _slice[0] not in ["t", "m", "b", "l", "c", "r"]:
                    tools.feedback(
                        f'The sliced value "{slice_portion}" is not valid!', True
                    )
                img = drawing._image
                img_file = pathlib.Path(img.fileName)
                iwidth = img.size[0]
                iheight = img.size[1]
                icentre = (int(iwidth / 2), int(iheight / 2))
                # calculate height of horizontal slice
                if _slice[0] in ["t", "m", "b"]:
                    slice_height = int(
                        min(iwidth * (width_height[1] / width_height[0]), iheight)
                    )
                # calculate width of vertical slice
                if _slice[0] in ["l", "c", "r"]:
                    slice_width = int(
                        min(iheight * (width_height[0] / width_height[1]), iwidth)
                    )
                # crop - needs a "box" which accepts a tuple with four values for
                #        the rectangle: left, upper, right, and lower
                match _slice[0]:
                    case "t":  # top (horizontal slice)
                        img2 = img.crop((0, 0, iwidth, slice_height))
                    case "m":  # middle (horizontal slice)
                        upper = icentre[1] - int(slice_height / 2)
                        img2 = img.crop((0, upper, iwidth, upper + slice_height))
                    case "b":  # bottom (horizontal slice)
                        img2 = img.crop((0, iheight - slice_height, iwidth, iheight))
                    case "l":  # left (vertical slice)
                        img2 = img.crop((0, 0, slice_width, iheight))
                    case "c":  # centre (vertical slice)
                        middle = icentre[0] - int(slice_width / 2)
                        img2 = img.crop((middle, 0, middle + slice_width, iheight))
                    case "r":  # right (vertical slice)
                        img2 = img.crop((iwidth - slice_width, 0, iwidth, iheight))
                    case _:
                        raise NotImplementedError(f"Cannot process {slice_portion}")
                # create new file with sliced image
                img2_filename = img_file.stem + "_" + _slice[0] + img_file.suffix
                sliced_filename = os.path.join(str(img_file.parent), img2_filename)
                img2.save(sliced_filename)
                return sliced_filename
            except Exception as err:
                tools.feedback(
                    f'The sliced value "{slice_portion}" is not valid! ({err})', True
                )
            return None

        def scale_image(drawing, scaling_factor):
            """Scale a shapes.Drawing() while maintaining aspect ratio"""
            try:
                _scaling_factor = float(scaling_factor)
            except Exception:
                tools.feedback(
                    f"Cannot scale an image with a value of {scaling_factor}", True
                )
            scaling_x = _scaling_factor
            scaling_y = _scaling_factor
            drawing.width = drawing.minWidth() * scaling_x
            drawing.height = drawing.height * scaling_y
            drawing.scale(scaling_x, scaling_y)
            return drawing

        def save_image_from_url(url: str):
            """Download image from network and save locally if not present."""
            loc = urlparse(url)
            filename = loc.path.split("/")[-1]
            image_local = os.path.join(cache_directory, filename)
            if not os.path.exists(image_local):
                image = requests.get(url)
                with open(image_local, "wb") as f:
                    f.write(image.content)
            return image_local

        def image_reader(image_location) -> object:
            """Attempt to load first from local cache, then network."""
            img = None
            image_local = image_location
            if cache_directory:
                if tools.is_url_valid(image_location):
                    image_local = save_image_from_url(image_location)
            img = ImageReader(image_local)
            return img

        img = None
        svg = False
        is_directory = False

        if not image_location:  # nothing to see here... move along
            return img, svg, None
        base_image_location = image_location

        # local files
        if not tools.is_url_valid(image_location):
            # relative paths
            if not os.path.isabs(image_location):
                filepath = tools.script_path()
                image_location = os.path.join(filepath, image_location)
            # no filename
            is_directory = os.path.isdir(image_location)
            if is_directory:
                return img, svg, True
            # check image exists
            if not os.path.exists(image_location):
                tools.feedback(
                    f'Unable to find or open image "{image_location}"', False, True
                )
                return img, svg, True

        try:
            image_location_ext = image_location.strip()[-3:]
            # tools.feedback(f'Loading type: {image_location_ext}')
            if image_location_ext.lower() == "svg":
                svg = True
        except Exception:
            pass

        try:
            if svg:
                if not os.path.exists(image_location):
                    raise IOError
                img = svg2rlg(image_location)
                if scaling:
                    img = scale_image(img, scaling)
            else:
                img = image_reader(image_location)
                if sliced:
                    sliced_filename = slice_image(
                        img, sliced, width_height=width_height
                    )
                    if sliced_filename:
                        img = image_reader(sliced_filename)
            return img, svg, is_directory
        except IOError as err:
            tools.feedback(
                f'Unable to find or open image "{base_image_location}"' f" ({err}).",
                False,
                True,
            )

        return img, svg, is_directory

    def process_template(self, _dict):
        """Set values for properties based on those defined in a dictionary."""
        if _dict.get("x"):
            self.x = _dict.get("x", 1)
        if _dict.get("y"):
            self.y = _dict.get("y", 1)
        if _dict.get("height"):
            self.height = _dict.get("height", 1)
        if _dict.get("width"):
            self.width = _dict.get("width", 1)
        if _dict.get("diameter"):
            self.diameter = _dict.get("diameter", 1)
        if _dict.get("radius"):
            self.radius = _dict.get("radius", self.diameter / 2.0 or 1)
        if _dict.get("rounding"):
            self.rounding = _dict.get("rounding", None)
        # if _dict.get('x'):
        #    self.x = _dict.get('x', 1)

    def get_center(self) -> tuple:
        """Attempt to get centre (x,y) tuple for a shape."""
        if self.cx and self.cy:
            return (self.cx, self.cy)
        if self.x and self.y and self.width and self.height:
            return (self.x + self.width / 2.0, self.y + self.height / 2.0)
        return ()

    def get_bounds(self) -> Bounds:
        """Attempt to get bounds of Rectangle (or any Shape with height and width)."""
        if self.x and self.y and self.width and self.height:
            bounds = Bounds(self.x, self.x + self.width, self.y, self.y + self.height)
            return bounds
        return None

    def get_shape_in_grid(self, the_shape):
        """Returns shape contained in GridShape class."""
        # if inspect.isclass(the_shape) and the_shape.__class__.__name__ == 'GridShape':
        if isinstance(the_shape, GridShape):
            return the_shape.shape
        else:
            return the_shape

    def get_font_height(self) -> float:
        face = pdfmetrics.getFont(self.font_name).face
        height = (face.ascent - face.descent) / 1000 * self.font_size
        return height

    def textify(self, index: int = None, text: str = "") -> str:
        """Extract text from a list, or create string, based on index & type."""
        _text = text or self.text
        log.debug("text %s %s %s %s", index, text, _text, type(_text))
        if _text is None:
            return
        if hasattr(_text, "lower"):
            return _text
        try:
            return _text[index]
        except TypeError:
            return _text

    def points_to_value(self, value: float) -> float:
        """Convert a point value to a units-based value."""
        try:
            if self.units == cm:
                return float(value) / cm
            if self.units == mm:
                return float(value) / mm
            elif self.units == inch:
                return float(value) / inch
            else:
                return float(value)
        except Exception as err:
            log.exception(err)
            tools.feedback(f'Unable to convert "{value}" to {self.units}!', True)

    def values_to_points(self, items: list) -> list:
        """Convert a list of values to point units."""
        try:
            if self.units == cm:
                return [float(item) * cm for item in items]
            elif self.units == mm:
                return [float(item) * mm for item in items]
            elif self.units == inch:
                return [float(item) * inch for item in items]
            else:
                tools.feedback(f'Unable to convert "{self.units}" to points!', True)
        except Exception as err:
            log.exception(err)
            tools.feedback(f'Unable to convert "{items}" to points!', True)

    def draw_multi_string(
        self, canvas, xm, ym, string, align=None, rotation=0, **kwargs
    ):
        """Low-level text drawing, split string (\n) if needed, with align and rotation.

        Args:
            * canvas (reportlab.pdfgen.canvas.Canvas): usually the calling
              function should access cnv.canvas i.e. an attribute of BaseCanvas
            * x (float) and y (float): must be in native units (i.e. points)!
            * string (str): the text to draw/write
            * align (str): one of [centre|right|left|None] alignment of text
            * rotation (float): an angle in degrees; anti-clockwise from East

        Kwargs:
            * locale - dict created from Locale namedtuple
        """
        if not string:
            return
        # ---- deprecated
        if kwargs.get("text_sequence", None):
            raise NotImplementedError("No text_sequence please!")
        # ---- process locale data (from Locale namedtuple) via jinja2
        _locale = kwargs.get("locale", None)
        if _locale:
            string = tools.eval_template(string, _locale)
        # ---- align and font
        align = align or self.align
        mvy = copy.copy(ym)
        # tools.feedback(f"*** {string=} {rotation=}")
        if kwargs.get("font_size"):
            fsize = float(kwargs.get("font_size"))
            canvas.setFont(self.font_name, fsize)
        # ---- drawString
        for ln in string.split("\n"):
            if rotation:
                canvas.saveState()
                canvas.translate(xm, mvy)
                canvas.rotate(rotation)
                if align == "centre":
                    canvas.drawCentredString(0, 0, ln)
                elif align == "right":
                    canvas.drawRightString(0, 0, ln)
                else:
                    canvas.drawString(0, 0, ln)
                canvas.restoreState()
            else:
                if align == "centre":
                    canvas.drawCentredString(xm, mvy, ln)
                elif align == "right":
                    canvas.drawRightString(xm, mvy, ln)
                else:
                    canvas.drawString(xm, mvy, ln)
            mvy -= canvas._leading

    def draw_string(self, canvas, xs, ys, string, align=None, rotation=0, **kwargs):
        """Draw a multi-string on the canvas."""
        self.draw_multi_string(
            canvas=canvas,
            x=xs,
            y=ys,
            string=string,
            align=align,
            rotation=rotation,
            **kwargs,
        )

    def draw_heading(
        self, canvas, ID, xh, yh, y_offset=0, align=None, rotation=0, **kwargs
    ):
        """Draw the heading for a shape (normally above the shape).

        Requires native units (i.e. points)!
        """
        ttext = self.textify(index=ID, text=self.heading)
        _rotation = rotation or self.heading_rotation
        if ttext:
            _ttext = str(ttext)
            y_off = y_offset or self.title_size / 2.0
            y = yh + self.unit(self.heading_my)
            x = xh + self.unit(self.heading_mx)
            canvas.setFont(self.font_name, self.heading_size)
            canvas.setFillColor(self.heading_stroke)
            self.draw_multi_string(
                canvas, x, y + y_off, _ttext, align=align, rotation=_rotation, **kwargs
            )

    def draw_label(
        self, canvas, ID, xl, yl, align=None, rotation=0, centred=True, **kwargs
    ):
        """Draw the label for a shape (usually at the centre).

        Requires native units (i.e. points)!
        """
        ttext = self.textify(index=ID, text=self.label)
        _rotation = rotation or self.label_rotation
        if ttext:
            _ttext = str(ttext)
            yl = yl - (self.label_size / 3.0) if centred else yl
            y = yl + self.unit(self.label_my)
            x = xl + self.unit(self.label_mx)
            canvas.setFont(self.font_name, self.label_size)
            canvas.setFillColor(self.label_stroke)
            self.draw_multi_string(
                canvas, x, y, _ttext, align=align, rotation=_rotation, **kwargs
            )

    def draw_title(
        self, canvas, ID, xt, yt, y_offset=0, align=None, rotation=0, **kwargs
    ):
        """Draw the title for a shape (normally below the shape).

        Requires native units (i.e. points)!
        """
        ttext = self.textify(index=ID, text=self.title)
        _rotation = rotation or self.title_rotation
        if ttext:
            _ttext = str(ttext)
            y_off = y_offset or self.title_size
            y = yt + self.unit(self.title_my)
            x = xt + self.unit(self.title_mx)
            canvas.setFont(self.font_name, self.title_size)
            canvas.setFillColor(self.title_stroke)
            self.draw_multi_string(
                canvas, x, y - y_off, _ttext, align=align, rotation=_rotation, **kwargs
            )

    def draw_radii_label(
        self, canvas, ID, xl, yl, align=None, rotation=0, centred=True, **kwargs
    ):
        """Draw the label for a radius (usually at the centre).

        Requires native units (i.e. points)!
        """
        if not self.radii_label:
            return
        ttext = self.textify(index=ID, text=self.radii_label)
        _rotation = rotation or self.radii_labels_rotation
        if ttext:
            _ttext = str(ttext)
            yl = yl - (self.radii_labels_size / 3.0) if centred else yl
            y = yl  # + self.unit(self.label_my)
            x = xl  # + self.unit(self.label_mx)
            canvas.setFont(self.radii_labels_face, self.radii_labels_size)
            canvas.setFillColor(self.radii_labels_stroke)
            self.draw_multi_string(
                canvas, x, y, _ttext, align=align, rotation=_rotation, **kwargs
            )

    def draw_dot(self, canvas, x, y):
        """Draw a small dot on a shape (normally the centre)."""
        if self.dot:
            dot_size = self.unit(self.dot)
            canvas.setFillColor(self.dot_stroke)
            canvas.setStrokeColor(self.dot_stroke)
            canvas.circle(x, y, dot_size, stroke=1, fill=1)

    def draw_cross(self, canvas, xd, yd):
        """Draw a cross on a shape (normally the centre)."""
        if self.cross:
            cross_size = self.unit(self.cross)
            canvas.setFillColor(self.cross_stroke)
            canvas.setStrokeColor(self.cross_stroke)
            canvas.setLineWidth(self.cross_stroke_width)
            # horizontal
            pt1 = geoms.Point(xd - cross_size / 2.0, yd)
            pt2 = geoms.Point(xd + cross_size / 2.0, yd)
            self.draw_line_between_points(canvas, pt1, pt2)
            # vertical
            pt1 = geoms.Point(xd, yd - cross_size / 2.0)
            pt2 = geoms.Point(xd, yd + cross_size / 2.0)
            self.draw_line_between_points(canvas, pt1, pt2)

    def draw_line_between_points(self, cnv, p1: geoms.Point, p2: geoms.Point):
        """Draw line between two Points"""
        pth = cnv.beginPath()
        pth.moveTo(p1.x, p1.y)
        pth.lineTo(p2.x, p2.y)
        cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0)

    def make_path_vertices(self, cnv, vertices: list, v1: int, v2: int):
        """Draw line between two vertices"""
        self.draw_line_between_points(cnv, vertices[v1], vertices[v2])

    def draw_lines_between_sides(
        self,
        cnv,
        side: float,
        lines: int,
        vertices: list,
        left_nodes: tuple,
        right_nodes: tuple,
    ):
        """Draw lines between opposing (left and right) sides of a shape

        Args:
            side: length of a side
            lines: number of lines extending from the side
            vertices: list of the Points making up the shape
            left_nodes: ID's of vertices on either end of the left side
            right_nodes: ID's of vertices on either end of the right side

        Note:
            * Vertices normally go clockwise from bottom/lower left
            * Directions of vertex indices in left- and right-nodes must be the same
        """
        delta = side / lines
        # tools.feedback(f'{side=} {lines=} {delta=}')
        for number in range(0, lines + 1):
            left_pt = geoms.point_on_line(
                vertices[left_nodes[0]], vertices[left_nodes[1]], delta * number
            )
            right_pt = geoms.point_on_line(
                vertices[right_nodes[0]], vertices[right_nodes[1]], delta * number
            )
            self.draw_line_between_points(cnv, left_pt, right_pt)

    def _debug(self, canvas, **kwargs):
        """Execute any debug statements."""
        if self.run_debug:
            # display vertex index number next to vertex
            if kwargs.get("vertices", []):
                canvas.setFillColor(self.debug_color)
                canvas.setFont(self.font_name, 4)
                for key, vert in enumerate(kwargs.get("vertices")):
                    x = self.points_to_value(vert.x)
                    y = self.points_to_value(vert.y)
                    self.draw_multi_string(
                        canvas, vert.x, vert.y, f"{key}:{x:.2f},{y:.2f}"
                    )
                    canvas.circle(vert.x, vert.y, 1, stroke=1, fill=1)
            # display labelled point (geoms.Point)
            if kwargs.get("point", []):
                point = kwargs.get("point")
                label = kwargs.get("label", "")
                canvas.setFillColor(kwargs.get("color", self.debug_color))
                canvas.setStrokeColor(kwargs.get("color", self.debug_color))
                canvas.setLineWidth(0.1)
                canvas.setFont(self.font_name, 4)
                x = self.points_to_value(point.x)
                y = self.points_to_value(point.y)
                self.draw_multi_string(
                    canvas, point.x, point.y, f"{label} {point.x:.2f},{point.y:.2f}"
                )
                canvas.circle(point.x, point.y, 2, stroke=1, fill=1)

    def handle_custom_values(self, the_element, ID):
        """Process custom values for a Shape's properties.

        Custom values should be stored in self.deck_data as a list of dicts:
        e.g. [{'SUIT': 'hearts', 'VALUE': 10}, {'SUIT': 'clubs', 'VALUE': 10}]
        which are used for a set of Cards, or similar placeholder items.

        Values can be accessed via a Jinja template using e.g. T("{{ SUIT }}")
        """
        # if not self.deck_data:
        #     return the_element
        new_element = None
        if isinstance(the_element, BaseShape):
            new_element = copy.copy(the_element)
            keys = vars(the_element).keys()
            for key in keys:
                value = getattr(the_element, key)
                if isinstance(value, Template):
                    if not self.deck_data:
                        tools.feedback(
                            "Cannot use T() or S() command without Data already defined!",
                            False,
                        )
                        tools.feedback(
                            "Check that Data command is used before Deck command.",
                            True,
                        )
                    record = self.deck_data[ID]
                    try:
                        custom_value = value.render(record)
                        setattr(new_element, key, custom_value)
                        # print('  +++', f'{ID=} {key=} {custom_value=}', '=>', getattr(new_element, key))
                    except jinja2.exceptions.UndefinedError as err:
                        tools.feedback(
                            f"Unable to process data with this template ({err})", True
                        )
                    except Exception as err:
                        tools.feedback(
                            f"Unable to process data with this template ({err})", True
                        )
                elif isinstance(value, LookupType):
                    record = self.deck_data[ID]
                    lookup_value = record[value.column]
                    custom_value = value.lookups.get(lookup_value, None)
                    setattr(new_element, key, custom_value)
                    # print('+++', f'{ID=} {key=} {custom_value=}', '=>', getattr(new_element, key))
        if new_element:
            return new_element
        return the_element  # no changes needed or made

    def draw_border(self, cnv, border: tuple, ID: int = None):
        """Draw a border line based its settings."""
        if not isinstance(border, tuple):
            tools.feedback(
                'The "borders" property must contain a list of one or more sets'
                f' - not "{border}"',
                True,
            )
        # ---- assign tuple values
        bdirections, bwidth, bcolor, bstyle, dotted, dashed = (
            None,
            None,
            black,
            None,
            False,
            None,
        )
        if len(border) >= 4:
            bstyle = border[3]
        if len(border) >= 3:
            bcolor = border[2]
        if len(border) >= 2:
            bdirections = border[0]
            bwidth = border[1]
        if len(border) <= 1:
            tools.feedback(
                'A "borders" set must contain: direction, width, color'
                f' and an optional style - not "{border}"',
                True,
            )
        # ---- validate
        bwidth = tools.as_float(bwidth, "")
        if bstyle is True:
            dotted = True
        else:
            dashed = bstyle
        # ---- multi-directions
        _bdirections = tools.validated_directions(
            bdirections, tools.DirectionGroup.COMPASS, "border"
        )
        for bdirection in _bdirections:
            if not bdirection:
                continue
            # ---- line start & end
            shape_name = self.__class__.__name__.replace("Shape", "")
            match self.__class__.__name__:

                case "RectangleShape" | "SquareShape" | "TrapezoidShape":
                    match bdirection:
                        case "n":
                            x, y = self.vertices[1][0], self.vertices[1][1]
                            x_1, y_1 = self.vertices[2][0], self.vertices[2][1]
                        case "e":
                            x, y = self.vertices[2][0], self.vertices[2][1]
                            x_1, y_1 = self.vertices[3][0], self.vertices[3][1]
                        case "s":
                            x, y = self.vertices[3][0], self.vertices[3][1]
                            x_1, y_1 = self.vertices[0][0], self.vertices[0][1]
                        case "w":
                            x, y = self.vertices[0][0], self.vertices[0][1]
                            x_1, y_1 = self.vertices[1][0], self.vertices[1][1]
                        case _:
                            raise ValueError(
                                f"Invalid direction for {shape_name} border"
                            )

                case "RhombusShape":
                    match bdirection:
                        case "ne":
                            x, y = self.vertices[1][0], self.vertices[1][1]
                            x_1, y_1 = self.vertices[2][0], self.vertices[2][1]
                        case "se":
                            x, y = self.vertices[2][0], self.vertices[2][1]
                            x_1, y_1 = self.vertices[3][0], self.vertices[3][1]
                        case "sw":
                            x, y = self.vertices[3][0], self.vertices[3][1]
                            x_1, y_1 = self.vertices[0][0], self.vertices[0][1]
                        case "nw":
                            x, y = self.vertices[0][0], self.vertices[0][1]
                            x_1, y_1 = self.vertices[1][0], self.vertices[1][1]
                        case _:
                            raise ValueError(
                                f"Invalid direction for {shape_name} border"
                            )

                case "HexShape":
                    if self.orientation == "pointy":
                        match bdirection:
                            case "ne":
                                x, y = self.vertices[2][0], self.vertices[2][1]
                                x_1, y_1 = self.vertices[3][0], self.vertices[3][1]
                            case "e":
                                x, y = self.vertices[3][0], self.vertices[3][1]
                                x_1, y_1 = self.vertices[4][0], self.vertices[4][1]
                            case "se":
                                x, y = self.vertices[4][0], self.vertices[4][1]
                                x_1, y_1 = self.vertices[5][0], self.vertices[5][1]
                            case "sw":
                                x, y = self.vertices[5][0], self.vertices[5][1]
                                x_1, y_1 = self.vertices[0][0], self.vertices[0][1]
                            case "w":
                                x, y = self.vertices[0][0], self.vertices[0][1]
                                x_1, y_1 = self.vertices[1][0], self.vertices[1][1]
                            case "nw":
                                x, y = self.vertices[1][0], self.vertices[1][1]
                                x_1, y_1 = self.vertices[2][0], self.vertices[2][1]
                            case _:
                                raise ValueError(
                                    f"Invalid direction for {shape_name} border"
                                )
                    elif self.orientation == "flat":
                        match bdirection:
                            case "n":
                                x, y = self.vertices[1][0], self.vertices[1][1]
                                x_1, y_1 = self.vertices[2][0], self.vertices[2][1]
                            case "ne":
                                x, y = self.vertices[2][0], self.vertices[2][1]
                                x_1, y_1 = self.vertices[3][0], self.vertices[3][1]
                            case "se":
                                x, y = self.vertices[3][0], self.vertices[3][1]
                                x_1, y_1 = self.vertices[4][0], self.vertices[4][1]
                            case "s":
                                x, y = self.vertices[4][0], self.vertices[4][1]
                                x_1, y_1 = self.vertices[5][0], self.vertices[5][1]
                            case "sw":
                                x, y = self.vertices[5][0], self.vertices[5][1]
                                x_1, y_1 = self.vertices[0][0], self.vertices[0][1]
                            case "nw":
                                x, y = self.vertices[0][0], self.vertices[0][1]
                                x_1, y_1 = self.vertices[1][0], self.vertices[1][1]
                            case _:
                                raise ValueError(
                                    f"Invalid direction for {shape_name} border"
                                )
                    else:
                        raise ValueError(
                            'Invalid orientation "{self.orientation}" for border'
                        )

                case _:
                    match bdirection:
                        case _:
                            tools.feedback(f"Cannot draw borders for a {shape_name}")

            # ---- set canvas
            self.set_canvas_props(
                index=ID,
                stroke=bcolor,
                stroke_width=bwidth,
                dotted=dotted,
                dashed=dashed,
            )
            # ---- draw line
            pth = cnv.beginPath()
            pth.moveTo(x, y)
            pth.lineTo(x_1, y_1)
            cnv.drawPath(pth, stroke=1 if bcolor else 0, fill=1)


class GroupBase(list):
    """Class for group base."""

    def __init__(self, *args, **kwargs):
        list.__init__(self, *args)
        self.kwargs = kwargs
