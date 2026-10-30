# -*- coding: utf-8 -*-
"""
protograf XX1StateObject class

Notes:
    * all arrays, such the cells of a board, are (col,row) with 1-based values
"""

# lib
import math
import re

# third party

# module
from protograf import globals
from protograf.base import BaseShape
from protograf.shapes import ImageShape
from protograf.utils import tools
from protograf.utils.messaging import feedback
from protograf.utils.structures import (  # named tuples; enums
    AbstractBoardType,
    Point,
    ShapeGeometry,
)
from protograf.utils.tools import _lower

# local
from .abstracts_game import AbstractGameObject


class XX18StateObject(BaseShape):
    """Draw XX18State composite shape on a given canvas."""

    def __init__(self, _object=None, canvas=None, **kwargs):
        super().__init__(_object=_object, canvas=canvas, **kwargs)

        self.game_class = "XX18State"
