# -*- coding: utf-8 -*-
"""
Project Enum definitions for protograf
"""
# lib
from enum import Enum
import logging

log = logging.getLogger(__name__)


class CardFrame(Enum):
    RECTANGLE = 1
    HEXAGON = 2
    CIRCLE = 3


class DatasetType(Enum):
    FILE = 1
    DICT = 2
    MATRIX = 3
    IMAGE = 4


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
