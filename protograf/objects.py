# -*- coding: utf-8 -*-
"""
Create custom objects for protograf
"""
# lib
import codecs
import copy
import logging
import math
import os
from pathlib import Path
import random
from urllib.parse import urlparse

# third party
import pymupdf
from pymupdf import Point as muPoint, Rect as muRect

# local
from protograf import globals
from protograf.utils import geoms, tools, support
from protograf.utils.constants import (
    GRID_SHAPES_WITH_CENTRE,
    COLOR_NAMES,
    DEBUG_COLOR,
    BGG_IMAGES,
)
from protograf.utils.messaging import feedback
from protograf.utils.structures import (
    BBox,
    DirectionGroup,
    HexGeometry,
    Link,
    Locale,
    Point,
    PolyGeometry,
)  # named tuples
from protograf.utils.support import CACHE_DIRECTORY
from protograf.base import (
    BaseShape,
    BaseCanvas,
    GridShape,
)
from protograf.shapes import RectangleShape

log = logging.getLogger(__name__)
DEBUG = False


class PolyominoObject(RectangleShape):
    """
    A plane geometric figure formed by joining one or more equal squares edge to edge.
    It is a polyform whose cells are squares.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(PolyominoObject, self).__init__(_object=_object, canvas=canvas, **kwargs)
        # overrides to make a "square rectangle"
        if self.width and not self.side:
            self.side = self.width
        if self.height and not self.side:
            self.side = self.height
        self.height, self.width = self.side, self.side
        self.set_unit_properties()
        self.kwargs = kwargs
        # custom/unique properties
        self.gap = tools.as_float(kwargs.get("gap", 0), "gap")
        self.rotation = tools.as_int(kwargs.get("rotation", 0), "rotation")
        self.pattern = kwargs.get("pattern", ["1"])
        self.invert = kwargs.get("invert", None)
        self.fills = kwargs.get("fills", [])
        self.strokes = kwargs.get("strokes", [])
        self.shapes = kwargs.get("shapes", [])
        # defaults
        self._fill, self._shape, self._stroke = self.fill, self.shape, self.stroke
        # validate
        correct, issue = self.validate_properties()
        if not correct:
            feedback("Problem with polyomino settings: %s." % "; ".join(issue), True)
        # set props
        self.int_pattern = self.numeric_pattern()  # numeric version of string pattern
        if self.rotation or self.invert:
            self.int_pattern = tools.transpose_lists(
                self.int_pattern, direction=self.rotation, flip=self.invert
            )

    def numeric_pattern(self):
        """Generate numeric-equivalent of pattern matrix."""
        numbers = []
        for item in self.pattern:
            values = [int(item[i]) for i in range(0, len(item))]
            numbers.append(values)
        return numbers

    def validate_properties(self):
        correct = True
        issue = []
        if self.invert:
            if str(self.invert).lower() not in [
                "lr",
                "leftright",
                "rl",
                "rightleft",
                "tb",
                "topbottom",
                "bt",
                "bottomtop",
            ]:
                issue.append(f'"{self.invert}" is an invalid reverse value!')
                correct = False
        if self.rotation and self.rotation not in [0, 90, -90]:
            issue.append(f'rotation must be 90 or -90 (not "{self.rotation}")!')
            correct = False
        if not isinstance(self.pattern, list):
            issue.append(f'pattern must be a list of strings (not "{self.pattern}")!')
            correct = False
        else:
            for key, item in enumerate(self.pattern):
                if key == 0:
                    length = len(item)
                else:
                    if not isinstance(item, str) or len(item) != length:
                        correct = False
                        issue.append(
                            f'pattern must be a list of equal-length strings (not "{self.pattern})"!'
                        )
                        break
                values = [item[i] for i in range(0, len(item))]
                for val in values:
                    # print(val, type(val))
                    try:
                        int(val)
                    except ValueError:
                        correct = False
                        issue.append(
                            f'pattern must contain a list of strings with integers (not "{item})"!'
                        )
                        break

        return correct, issue

    def calculate_area(self) -> float:
        return self._u.width * self._u.height

    def calculate_perimeter(self, units: bool = False) -> float:
        """Total length of bounding line."""
        length = 2.0 * (self._u.width + self._u.height)
        if units:
            return self.peaks_to_value(length)
        else:
            return length

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw squares for the Polyomino on a given canvas."""
        # feedback(f'@ Polyomino@ {self.label=} // {off_x=}, {off_y=} {kwargs=}')
        # print(f"{self.int_pattern=}")
        for row, item in enumerate(self.int_pattern):
            off_y = row * self.side  # TODO - add gap
            for col, number in enumerate(item):
                off_x = col * self.side  # TODO - add gap
                if number != 0:
                    # set props based on square's numbers
                    try:
                        kwargs['fill'] = self.fills[number - 1]
                    except:
                        kwargs['fill'] = self.fill
                    try:
                        kwargs['shape'] = self.shapes[number - 1]
                    except:
                        kwargs['shape'] = self.shape
                    try:
                        kwargs['stroke'] = self.strokes[number - 1]
                    except:
                        kwargs['stroke'] = self.stroke
                    # print(f"{row=} {col=} {number=} {kwargs=}")
                    super().draw(cnv, off_x, off_y, ID, **kwargs)


class PentominoObject(PolyominoObject):
    """
    A plane geometric figure formed by joining five equal squares edge to edge.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        self.letter = kwargs.get('letter', 'I')
        match self.letter:
            case 'T':
                pattern = ['111', '010', '010']
            case 'U':
                pattern = ['101', '111']
            case 'V':
                pattern = ['001', '001', '111']
            case 'W':
                pattern = ['001', '011', '110']
            case 'X':
                pattern = ['010', '111', '010']
            case 'Y':
                pattern = ['01', '11', '01', '01']
            case 'Z':
                pattern = ['110', '010', '011']
            case 'F':
                pattern = ['011', '110', '010']
            case 'I':
                pattern = ['1', '1', '1', '1', '1']
            case 'L':
                pattern = ['10', '10', '10', '11']
            case 'N':
                pattern = ['01', '11', '10', '10']
            case 'P':
                pattern = ['11', '11', '10']
            # LOWER - flipped LR
            case 't':
                pattern = ['111', '010', '010']
            case 'u':
                pattern = ['101', '111']
            case 'v':
                pattern = ['100', '100', '111']
            case 'w':
                pattern = ['001', '011', '110']
            case 'x':
                pattern = ['010', '111', '010']
            case 'y':
                pattern = ['10', '11', '10', '10']
            case 'z':
                pattern = ['011', '010', '110']
            case 'f':
                pattern = ['110', '011', '010']
            case 'i':
                pattern = ['1', '1', '1', '1', '1']
            case 'l':
                pattern = ['01', '01', '01', '11']
            case 'n':
                pattern = ['10', '11', '01', '01']
            case 'p':
                pattern = ['11', '11', '01']
            case _:
                feedback("Pentomino letter must be selected from predefined set!", True)

        kwargs['pattern'] = pattern
        super(PentominoObject, self).__init__(_object=_object, canvas=canvas, **kwargs)


class TetrominoObject(PolyominoObject):
    """
    A plane geometric figure formed by joining four equal squares edge to edge.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        self.letter = kwargs.get('letter', 'I')
        match self.letter:
            case 'I':
                pattern = ['1', '1', '1', '1',]
            case 'L':
                pattern = ['10', '10', '11']
            case 'O':
                pattern = ['11', '11']
            case 'S':
                pattern = ['011', '110']
            case 'T':
                pattern = ['111', '010']
            # LOWER - flipped LR
            case 'i':
                pattern = ['1', '1', '1', '1',]
            case 'l':
                pattern = ['01', '01', '11']
            case 'o':
                pattern = ['11', '11']
            case 's':
                pattern = ['110', '011']
            case 't':
                pattern = ['111', '010']
            case _:
                feedback("Tetromino letter must be selected from predefined set!", True)

        kwargs['pattern'] = pattern
        super(TetrominoObject, self).__init__(_object=_object, canvas=canvas, **kwargs)
