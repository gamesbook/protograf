# -*- coding: utf-8 -*-
"""
Data structures (enum, dataclasses, namedtuples) for protograf
"""
# lib
from collections import namedtuple
from dataclasses import dataclass
from enum import Enum
import logging
from typing import Any, List, Tuple

# third-party
from jinja2 import Template

log = logging.getLogger(__name__)

# ---- ENUM


class CardFrame(Enum):
    RECTANGLE = 1
    HEXAGON = 2
    CIRCLE = 3


class DatasetType(Enum):
    FILE = 1
    DICT = 2
    MATRIX = 3
    IMAGE = 4
    GSHEET = 5


class DirectionGroup(Enum):
    CARDINAL = 1
    COMPASS = 2
    HEX_FLAT = 3  # vertex
    HEX_POINTY = 4
    HEX_FLAT_EDGE = 4  # edge
    HEX_POINTY_EDGE = 5
    CIRCULAR = 6


class ExportFormat(Enum):
    GIF = 1
    PNG = 2
    SVG = 3


class FontStyleType(Enum):
    REGULAR = 1
    BOLD = 2
    ITALIC = 3
    BOLDITALIC = 4


class HexOrientation(Enum):
    FLAT = 1
    POINTY = 2


# ---- NAMEDTUPLE

Bounds = namedtuple(
    "Bounds",
    [
        "left",
        "right",
        "bottom",
        "top",
    ],
)

# track progress of a Deck print (front or back)
DeckPrintState = namedtuple(
    "DeckPrintState",
    [
        "card_count",
        "card_number",
        "copies_to_do",
        "start_x",  # left-most point of first card
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

GlobalDocument = namedtuple(
    "GlobalDocument",
    [
        "base",
        "deck",
        "card_frames",
        "filename",
        "directory",
        "document",
        "doc_page",
        "canvas",
        "margins",
        "page",
        "page_fill",
        "page_width",
        "page_height",
        "page_count",
        "page_grid",
    ],
)

HexGeometry = namedtuple(
    "HexGeometry",
    [
        "radius",
        "diameter",
        "side",
        "half_side",
        "half_flat",
        "height_flat",
        "z_fraction",
    ],
)
LookupType = namedtuple("LookupType", ["column", "lookups"])
Link = namedtuple("Link", ["a", "b", "style"])

fields = ("col", "row", "x", "y", "id", "sequence", "corner", "label")
Locale = namedtuple("Locale", fields, defaults=(None,) * len(fields))

OffsetProperties = namedtuple(
    "OffsetProperties",
    [
        "off_x",
        "off_y",
        "delta_x",
        "delta_y",
    ],
)

# margins are in user units
PageMargins = namedtuple(
    "PageMargins",
    [
        "margin",  # default
        "left",
        "right",
        "bottom",
        "top",
        "debug",  # show the margin?
    ],
)

Place = namedtuple("Place", ["shape", "rotation"])

Point = namedtuple("Point", ["x", "y"])  # maths term specifing position & direction

PolyGeometry = namedtuple(
    "PolyGeometry", ["x", "y", "radius", "side", "half_flat", "vertices"]
)

Ray = namedtuple("Ray", ["x", "y", "angle"])

ShapeProperties = namedtuple(
    "ShapeProperties",
    [
        "width",
        "color",
        "fill",
        "lineCap",
        "lineJoin",
        "dashes",
        "fill_opacity",
        "morph",
        "closePath",
    ],
)

Tetris3D = namedtuple(
    "Tetris3D",
    [
        "inner",
        "outer_tl",
        "outer_br",
        "tribtm",
        "tritop",
    ],
)

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

# ---- DATACLASS


@dataclass
class BBox:
    """Spatial bounding box.

    Properties:

    - `tl` is minimum x,y point
    - `br` is maximum x,y point
    """

    tl: Point
    br: Point


# wrapper around a jinja Template to support operations on an Template output
@dataclass
class TemplatingType:
    """Support dynamic object creation from a jinja Template"""

    template: Template
    function: object
    members: List
