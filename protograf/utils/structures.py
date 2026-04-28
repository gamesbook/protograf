# -*- coding: utf-8 -*-
"""
Data structures (enum, dataclasses, namedtuples) for protograf
"""

# lib
from collections import namedtuple
from dataclasses import dataclass
from enum import Enum
import logging
from typing import Any, List, NamedTuple

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
    ORDINAL = 7
    TRIANGULAR = 8
    TRIANGULAR_EDGE = 9
    POLYGONAL = 10
    STAR = 11
    TRIANGULAR_HATCH = 12


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


class TriangleType(Enum):
    EQUILATERAL = 1
    ISOSCELES = 2
    IRREGULAR = 3


# ---- NAMEDTUPLES

# ---- * Bounds
Bounds = namedtuple(
    "Bounds",
    [
        "left",
        "right",
        "bottom",
        "top",
    ],
)

"""
cb_fields = ("fill", "offset_x", "offset_y", "offset_radius")
CardBleed = namedtuple("CardBleed", cb_fields, defaults=(None,) * len(cb_fields))
"""

# ---- * CrossParts
CrossParts = namedtuple(
    "CrossParts",
    ["thickness", "half_thick", "arm", "body", "head"],
)

# track progress of a Deck print (front or back)
DeckPrintState = namedtuple(
    "DeckPrintState",
    [
        "card_count",
        "card_number",
        "copies_done",
        "start_x",  # left-most point of first card
    ],
)

# ---- * GridShape
GridShape = namedtuple(
    "GridShape",
    [
        "label",
        "x",
        "y",
        "shape",
    ],
)

# ---- * GlobalDocument
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

# ---- * HexGeometry
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

# ---- * HexEdgeResult - use for GridLine edge path
HexEdgeResult = namedtuple(
    "HexEdgeResult",
    [
        "edge",  # compass direction / edge
        "end",  # compass direction / vertex
        "row",  # int; -1, 0 or 1
        "col",  # int; -1, 0 or 1
    ],
)
# ---- * LookupType
LookupType = namedtuple("LookupType", ["column", "lookups"])

# ---- * Link
Link = namedtuple("Link", ["a", "b", "style"])

# ---- * OffsetProperties
OffsetProperties = namedtuple(
    "OffsetProperties",
    [
        "off_x",
        "off_y",
        "delta_x",
        "delta_y",
    ],
)

# ----  PAGEMARGINS
# base margins are in user units
PageMarginsBase = namedtuple(
    "PageMarginsBase",
    [
        "margin",  # default
        "left",
        "right",
        "bottom",
        "top",
        "debug",  # show the margin?
        "units",  # point equivalent of single user unit
    ],
)


class PageMargins(PageMarginsBase):

    @property
    def left_u(self):
        """Calculates the margin in point units."""
        return self.units * self.left

    @property
    def right_u(self):
        """Calculates the margin in point units."""
        return self.units * self.right

    @property
    def top_u(self):
        """Calculates the margin in point units."""
        return self.units * self.top

    @property
    def bottom_u(self):
        """Calculates the margin in point units."""
        return self.units * self.bottom


Place = namedtuple("Place", ["shape", "rotation"])

Point = namedtuple("Point", ["x", "y"])

PolyGeometry = namedtuple(
    "PolyGeometry", ["x", "y", "radius", "side", "half_flat", "vertices", "sides"]
)

Ray = namedtuple(
    "Ray", ["x", "y", "angle"]
)  # maths term specifing position & direction

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

# ---- NAMEDTUPLE CLASS


class CardBleed(NamedTuple):
    """Attributes for setting bleed color and extent around a Card"""

    fill: Any | None = None
    offset_x: float | None = None
    offset_y: float | None = None
    offset_radius: float | None = None


class ClockGeometry(NamedTuple):
    """Clock-hour locations on the circumference of a Circle"""

    h1: Point | None = None
    h2: Point | None = None
    h3: Point | None = None
    h4: Point | None = None
    h5: Point | None = None
    h6: Point | None = None
    h7: Point | None = None
    h8: Point | None = None
    h9: Point | None = None
    h10: Point | None = None
    h11: Point | None = None
    h12: Point | None = None


class ShapeGeometry(NamedTuple):
    """Key points and spatial attributes of a Shape

    # N = 90, W = 180, S = 270, E = 0
    # NE = 45, NW = 135, SW = 225, SE = 315
    # NNW =
    """

    # points
    centre: Point | None = None
    center: Point | None = None
    c: Point | None = None
    n: Point | None = None
    s: Point | None = None
    e: Point | None = None
    w: Point | None = None
    ne: Point | None = None
    se: Point | None = None
    nw: Point | None = None
    sw: Point | None = None
    nnw: Point | None = None
    nne: Point | None = None
    sse: Point | None = None
    ssw: Point | None = None
    wnw: Point | None = None
    ene: Point | None = None
    ese: Point | None = None
    wsw: Point | None = None
    v: list | None = None
    vertices: list | None = None
    p: Point | None = None
    perbii: list | None = None
    # lengths
    radius: float | None = None
    diameter: float | None = None
    side: float | None = None
    length: float | None = None
    width: float | None = None
    height: float | None = None
    perimeter: float | None = None
    # other
    area: float | None = None
    sides: int | None = None  # e.g. for a regular Polygon
    # meta
    t: str | None = None
    type: str | None = None
    shapetype: str | None = None
    name: str | None = None


class Locale(NamedTuple):
    """Key values and spatial attributes of a Locale

    Note:
        * Typically used for a grid-like or cell location
    """

    col: int | None = None
    row: int | None = None
    x: float | None = None
    y: float | None = None
    xy: Point | None = None
    cxy: Point | None = None
    geo: ShapeGeometry | None = None
    height: float | None = None
    width: float | None = None
    radius: float | None = None
    side: float | None = None
    id: int | None = None
    sequence: int | None = None
    corner: bool = False
    label: str | None = None
    page: int | None = None


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


@dataclass
class Perbis:
    """Perbis is the centre of an edge of a Shape"""

    point: Point
    direction: str
    v1: Point
    v2: Point
    compass: float
    angle: float


@dataclass
class Radius:
    """Radius is the line from centre to circumference enclosing a Shape"""

    point: Point
    direction: str
    compass: float
    angle: float


# wrapper around a jinja Template to support operations on an Template output
@dataclass
class TemplatingType:
    """Support dynamic object creation from a jinja Template"""

    template: Template
    function: object
    members: List


@dataclass
class Vertex:
    """Vertext is a named point corresponding a vertex on a Shape"""

    point: Point
    direction: str


@dataclass
class VirtualHex:
    """VirtualHex is an identified Hex in a HexHexLocations array"""

    centre: Point
    id: int
    ring: int
    counter: int
    spine: int
    zone: str
    orientation: HexOrientation


# ---- "FIXED" DICT

# ---- * Travel outcomes for GridLine edges
HEX_FLAT_EDGE_TRAVEL = {
    # startpoint / direction => result
    ("ne", "w"): HexEdgeResult(edge="n", end="nw", row=0, col=0),
    ("ne", "ne"): HexEdgeResult(edge="se", end="nw", row=-1, col=1),
    ("ne", "se"): HexEdgeResult(edge="ne", end="e", row=0, col=0),
    ("e", "nw"): HexEdgeResult(edge="ne", end="ne", row=0, col=0),
    ("e", "e"): HexEdgeResult(edge="s", end="se", row=0, col=1),
    ("e", "sw"): HexEdgeResult(edge="se", end="se", row=0, col=0),
    ("se", "ne"): HexEdgeResult(edge="se", end="e", row=0, col=0),
    ("se", "se"): HexEdgeResult(edge="sw", end="sw", row=0, col=1),
    ("se", "w"): HexEdgeResult(edge="s", end="sw", row=0, col=0),
    ("sw", "e"): HexEdgeResult(edge="s", end="se", row=0, col=0),
    ("sw", "nw"): HexEdgeResult(edge="sw", end="w", row=0, col=0),
    ("sw", "sw"): HexEdgeResult(edge="se", end="se", row=0, col=-1),
    ("w", "w"): HexEdgeResult(edge="s", end="sw", row=0, col=-1),
    ("w", "ne"): HexEdgeResult(edge="nw", end="nw", row=0, col=0),
    ("w", "se"): HexEdgeResult(edge="sw", end="sw", row=0, col=0),
    ("nw", "e"): HexEdgeResult(edge="n", end="ne", row=0, col=0),
    ("nw", "nw"): HexEdgeResult(edge="sw", end="w", row=-1, col=0),
    ("nw", "sw"): HexEdgeResult(edge="nw", end="w", row=0, col=0),
}
