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

Place = namedtuple("Place", ["shape", "rotation"])

Point = namedtuple("Point", ["x", "y"])  # maths term specifing position & direction

PolyGeometry = namedtuple(
    "PolyGeometry", ["x", "y", "radius", "side", "half_flat", "vertices"]
)

Ray = namedtuple("Ray", ["x", "y", "angle"])

UnitPoints = namedtuple(
    "UnitPoints",
    [
        "cm",
        "mm",
        "inch",
        "pt",
    ],
)

# ---- units point equivalents
unit = UnitPoints(
    cm=28.3465,
    mm=2.83465,
    inch=72.0,
    pt=1.0,
)

# ---- DATACLASS


@dataclass
class BBox:
    """A spatial bounding box - BL is SouthWest x,y point and TR is NorthEast x,y point"""

    bl: Tuple[Point, Point]
    tr: Tuple[Point, Point]


# wrapper around a jinja Template to support operations on an Template output
@dataclass
class TemplatingType:
    """Support dynamic object creation from a jinga Template"""

    template: Template
    function: object
    members: List
