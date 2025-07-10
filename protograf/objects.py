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
    Tetris3D,
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
        self._label = self.label
        # custom/unique properties
        self.gap = tools.as_float(kwargs.get("gap", 0), "gap")
        self.pattern = kwargs.get("pattern", ["1"])
        self.invert = kwargs.get("invert", None)
        self.fills = kwargs.get("fills", [])
        self.labels = kwargs.get("labels", [])
        self.strokes = kwargs.get("strokes", [])
        self.centre_shapes = kwargs.get("centre_shapes", [])
        # defaults
        self._fill, self._centre_shape, self._stroke = (
            self.fill,
            self.centre_shape,
            self.stroke,
        )
        self.is_outline = True if (self.outline_stroke or self.outline_width) else False
        # validate
        correct, issue = self.validate_properties()
        if not correct:
            feedback("Problem with polyomino settings: %s." % "; ".join(issue), True)
        # set props
        self.int_pattern = self.numeric_pattern()  # numeric version of string pattern
        if self.flip or self.invert:
            self.int_pattern = tools.transpose_lists(
                self.int_pattern, direction=self.flip, invert=self.invert
            )
        # tetris
        self.letter = kwargs.get("letter", None)
        self.tetris = kwargs.get("tetris", False)
        self.is_tetronimo = kwargs.get("is_tetromino", False)

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
        if self.gap > 0 and self.is_outline:
            issue.append("Both gap and outline cannot be set at the same time!")
            correct = False
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

    def get_perimeter_lines(self, cnv=None, ID=None, **kwargs) -> list:
        """Calculate set of lines that form perimeter of polyonimo"""
        perimeter_lines = []
        max_row = len(self.int_pattern)
        max_col = len(self.int_pattern[0])
        for row, item in enumerate(self.int_pattern):
            off_y = row * self.side  # NB - no gap
            for col, number in enumerate(item):
                if number == 0:
                    continue
                off_x = col * self.side
                super().set_abs_and_offset(
                    cnv=cnv, off_x=off_x, off_y=off_y, ID=ID, **kwargs
                )
                vtx = super().get_vertexes()  # anti-clockwise from top-left
                # handle edges
                if col == 0:  # left edge
                    perimeter_lines.append((vtx[1], vtx[0]))
                if row == 0:  # top edge
                    perimeter_lines.append((vtx[0], vtx[3]))
                if col == max_col - 1:  # right edge
                    perimeter_lines.append((vtx[2], vtx[3]))
                if row == max_row - 1:  # bottom edge
                    perimeter_lines.append((vtx[1], vtx[2]))
                # left
                try:
                    number = self.int_pattern[row][col - 1]
                    if number == 0:
                        perimeter_lines.append((vtx[0], vtx[1]))
                except:
                    pass
                # right
                try:
                    number = self.int_pattern[row][col + 1]
                    if number == 0:
                        perimeter_lines.append((vtx[3], vtx[2]))
                except:
                    pass
                # above
                try:
                    number = self.int_pattern[row - 1][col]
                    if number == 0:
                        perimeter_lines.append((vtx[0], vtx[3]))
                except:
                    pass
                # below
                try:
                    number = self.int_pattern[row + 1][col]
                    if number == 0:
                        perimeter_lines.append((vtx[1], vtx[2]))
                except:
                    pass
        return perimeter_lines

    def set_tetris_style(self, **kwargs):
        """Get colors and set centre-shape for Tetris Tetronimo"""
        match self.letter:
            case "i" | "I":  # aqua
                t3dcolors = Tetris3D(
                    inner="#00CDCD",
                    outer_tl="#00C3C3",
                    outer_br="#008989",
                    tritop="#00FFFF",
                    tribtm="#009898",
                )
            case "l":  # dark blue
                t3dcolors = Tetris3D(
                    inner="#0000CD",
                    outer_tl="#0000B5",
                    outer_br="#00008D",
                    tritop="#0000FF",
                    tribtm="#020198",
                )
            case "L":  # orange
                t3dcolors = Tetris3D(
                    inner="#CD6600",
                    outer_tl="#B55D00",
                    outer_br="#7F3700",
                    tritop="#FF8900",
                    tribtm="#9A4200",
                )
            case "o" | "O":  # yellow
                t3dcolors = Tetris3D(
                    inner="#CDCD00",
                    outer_tl="#BBBB00",
                    outer_br="#8D8D00",
                    tritop="#FFFF00",
                    tribtm="#9A9A00",
                )
            case "S":  # light green
                t3dcolors = Tetris3D(
                    inner="#00CD00",
                    outer_tl="#00CD00",
                    outer_br="#008F00",
                    tritop="#00FF00",
                    tribtm="#009A00",
                )
            case "s":  # red
                t3dcolors = Tetris3D(
                    inner="#CD0000",
                    outer_tl="#C20000",
                    outer_br="#8A0000",
                    tritop="#F60000",
                    tribtm="#990700",
                )
            case "t" | "T":  # purple
                t3dcolors = Tetris3D(
                    inner="#9A00CD",
                    outer_tl="#9100C1",
                    outer_br="#660199",
                    tritop="#CB00FC",
                    tribtm="#66009A",
                )
            case "*" | ".":  # grey
                t3dcolors = Tetris3D(
                    inner="#787878",
                    outer_tl="#969696",
                    outer_br="#515151",
                    tritop="#9A9A9A",
                    tribtm="#313131",
                )
            case _:
                feedback(f"The Tetronimo letter {self.letter} is unknown", True)

        swidth = 0.0247 * self.unit(self.width)
        # breakpoint()
        self.centre_shape = RectangleShape(
            width=0.8 * self.width,
            height=0.8 * self.height,
            fill=t3dcolors.inner,
            stroke=None,
            borders=[
                ("n w", swidth, t3dcolors.outer_tl),
                ("s e", swidth, t3dcolors.outer_br),
            ],
        )
        return t3dcolors.tritop, t3dcolors.tribtm

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw squares for the Polyomino on a given canvas."""
        # feedback(f'~~~ Polyomino {self.label=} // {off_x=}, {off_y=} {kwargs=}')
        # print(f"~~~ {self.int_pattern=}")
        # ---- squares
        for row, item in enumerate(self.int_pattern):
            off_y = row * self.side + row * self.gap
            for col, number in enumerate(item):
                off_x = col * self.side + col * self.gap
                if number != 0:
                    # set props based on the square's number
                    try:
                        kwargs["fill"] = self.fills[number - 1]
                    except:
                        kwargs["fill"] = self.fill
                    try:
                        self.centre_shape = self.centre_shapes[number - 1]
                    except:
                        self.centre_shape = self._centre_shape
                    try:
                        kwargs["stroke"] = self.strokes[number - 1]
                    except:
                        kwargs["stroke"] = self.stroke
                    try:
                        self.label = self.labels[number - 1]
                    except:
                        self.label = self._label
                    # ---- Tetris: overide colors and shape centre
                    if self.tetris and self.is_tetronimo:
                        color_top, color_btm = self.set_tetris_style(**kwargs)
                        if color_top and color_btm:
                            self.roof = [color_top, color_btm]
                            # print(f"{self.letter=} {self.roof=}")

                    kwargs["row"] = row
                    kwargs["col"] = col
                    # print(f"~~~ Polyomino {row=} {col=} {number=} {self.label=}")
                    super().draw(cnv, off_x, off_y, ID, **kwargs)
        # ---- optional perimeter
        if self.outline_stroke or self.outline_width:
            cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
            perimeter_lines = self.get_perimeter_lines(cnv=cnv, ID=ID, **kwargs)
            for line in perimeter_lines:
                cnv.draw_line(Point(line[0].x, line[0].y), Point(line[1].x, line[1].y))
            kwargs["stroke"] = self.outline_stroke or self.stroke
            kwargs["stroke_width"] = self.outline_width or self.stroke_width
            kwargs["closed"] = False
            kwargs["fill"] = None
            self.set_canvas_props(cnv=cnv, index=ID, **kwargs)  # shape.finish()


class PentominoObject(PolyominoObject):
    """
    A plane geometric figure formed by joining five equal squares edge to edge.

    Notes:
        * The lettering convention follows that of Golomb - not the
          Games & Puzzles Issue 9 (1973)
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        self.letter = kwargs.get("letter", "I")
        match self.letter:
            case "T":
                pattern = ["111", "010", "010"]
            case "U":
                pattern = ["101", "111"]
            case "V":
                pattern = ["001", "001", "111"]
            case "W":
                pattern = ["001", "011", "110"]
            case "X":
                pattern = ["010", "111", "010"]
            case "Y":
                pattern = ["01", "11", "01", "01"]
            case "Z":
                pattern = ["110", "010", "011"]
            case "F":
                pattern = ["011", "110", "010"]
            case "I":
                pattern = ["1", "1", "1", "1", "1"]
            case "L":
                pattern = ["10", "10", "10", "11"]
            case "N":
                pattern = ["01", "11", "10", "10"]
            case "P":
                pattern = ["11", "11", "10"]
            # LOWER - flipped LR
            case "t":
                pattern = ["111", "010", "010"]
            case "u":
                pattern = ["101", "111"]
            case "v":
                pattern = ["100", "100", "111"]
            case "w":
                pattern = ["001", "011", "110"]
            case "x":
                pattern = ["010", "111", "010"]
            case "y":
                pattern = ["10", "11", "10", "10"]
            case "z":
                pattern = ["011", "010", "110"]
            case "f":
                pattern = ["110", "011", "010"]
            case "i":
                pattern = ["1", "1", "1", "1", "1"]
            case "l":
                pattern = ["01", "01", "01", "11"]
            case "n":
                pattern = ["10", "11", "01", "01"]
            case "p":
                pattern = ["11", "11", "01"]
            case _:
                feedback("Pentomino letter must be selected from predefined set!", True)

        kwargs["pattern"] = pattern
        super(PentominoObject, self).__init__(_object=_object, canvas=canvas, **kwargs)


class TetrominoObject(PolyominoObject):
    """
    A plane geometric figure formed by joining four equal squares edge to edge.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        self.letter = kwargs.get("letter", "I")
        match self.letter:
            case "I":
                pattern = [
                    "1",
                    "1",
                    "1",
                    "1",
                ]
            case "L":
                pattern = ["10", "10", "11"]
            case "O":
                pattern = ["11", "11"]
            case "S":
                pattern = ["011", "110"]
            case "T":
                pattern = ["111", "010"]
            # LOWER - flipped LR
            case "i":
                pattern = [
                    "1",
                    "1",
                    "1",
                    "1",
                ]
            case "l":
                pattern = ["01", "01", "11"]
            case "o":
                pattern = ["11", "11"]
            case "s":
                pattern = ["110", "011"]
            case "t":
                pattern = ["111", "010"]
            case "*" | ".":
                pattern = ["1"]
            case _:
                feedback("Tetromino letter must be selected from predefined set!", True)

        kwargs["pattern"] = pattern
        kwargs["is_tetromino"] = True
        kwargs["letter"] = self.letter
        super(TetrominoObject, self).__init__(_object=_object, canvas=canvas, **kwargs)
