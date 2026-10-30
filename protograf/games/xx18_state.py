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
# local
from .core_state import CoreStateObject


class XX18StateObject(CoreStateObject):
    """Draw XX18State composite shape on a given canvas."""

    def __init__(self, _object=None, canvas=None, **kwargs):
        super().__init__(_object=_object, canvas=canvas, **kwargs)
        # ---- unique properties
        self.game_class = "XX18State"
        # ---- unique properties
        self.board = self._commons("board") or kwargs.get("board") or None
        self.features = self._commons("features") or kwargs.get("features") or []

    def draw_features(self):
        """Draw feature elements on the board."""
        from protograf.base import BaseShape

        for feature in self.features:
            pass

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw the XX18StateObject on a given canvas."""
        # from protograf.protos import Layout

        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- draw the board frame
        if self.board.frame is True:
            self.board.draw_frame()
        # ---- draw the board
        self.board.board_layout._draw_grid = True
        self.board.board_layout.draw_layout()
        # ---- draw the board labels
        if self.board.label is True:
            self.board.draw_labels()
        # ---- draw the features on the board
        if self.features:
            self.draw_features()
