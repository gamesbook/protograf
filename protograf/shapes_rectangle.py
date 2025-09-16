# -*- coding: utf-8 -*-
"""
Create custom shapes for protograf
"""
# lib
import codecs
import copy
import logging
import math
import os
from pathlib import Path
from urllib.parse import urlparse

# third party
import pymupdf
from pymupdf import Point as muPoint, Rect as muRect
import segno  # QRCode

# local
from protograf import globals
from protograf.shapes_utils import set_cached_dir, draw_line
from protograf.utils import colrs, geoms, tools, support, fonts
from protograf.utils.tools import _lower
from protograf.utils.constants import (
    BGG_IMAGES,
)
from protograf.utils.messaging import feedback
from protograf.utils.structures import (
    BBox,
    DirectionGroup,
    HexGeometry,
    HexOrientation,
    Link,
    Perbis,
    Point,
    PolyGeometry,
)  # named tuples
from protograf.utils.support import CACHE_DIRECTORY
from protograf.base import (
    BaseShape,
    GridShape,
    get_cache,
)

log = logging.getLogger(__name__)
DEBUG = False


def _sin(degrees: float) -> float:
    return math.sin(math.radians(degrees))


def _cos(degrees: float) -> float:
    return math.cos(math.radians(degrees))


def _tan(degrees: float) -> float:
    return math.tan(math.radians(degrees))


class RectangleShape(BaseShape):
    """
    Rectangle on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(RectangleShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        # overrides to centre shape
        if self.cx is not None and self.cy is not None:
            self.x = self.cx - self.width / 2.0
            self.y = self.cy - self.height / 2.0
            # feedback(f"*** RectShp {self.cx=} {self.cy=} {self.x=} {self.y=}")
        self._u_slices_line = self.unit(self.slices_line) if self.slices_line else None
        self._u_slices_line_mx = (
            self.unit(self.slices_line_mx) if self.slices_line_mx else 0
        )
        self._u_slices_line_my = (
            self.unit(self.slices_line_mx) if self.slices_line_my else 0
        )
        self.kwargs = kwargs

    def calculate_area(self) -> float:
        return self._u.width * self._u.height

    def calculate_perimeter(self, units: bool = False) -> float:
        """Total length of bounding perimeter."""
        length = 2.0 * (self._u.width + self._u.height)
        if units:
            return self.points_to_value(length)
        else:
            return length

    def calculate_perbii(
        self, cnv, centre: Point, rotation: float = None, **kwargs
    ) -> list:
        """Calculate centre points for each edge and angles from centre.

        Args:
            vertices: list of Rect nodes as Points
            centre: the centre Point of the Hex

        Returns:
            dict of Perbis objects keyed on direction
        """
        directions = ["n", "w", "s", "e"]
        perbii_dict = {}
        vertices = self.get_vertexes(rotation=rotation, **kwargs)
        vcount = len(vertices) - 1
        _perbii_pts = []
        # print(f"*** RECT perbii {centre=} {vertices=}")
        for key, vertex in enumerate(vertices):
            if key == 0:
                p1 = Point(vertex.x, vertex.y)
                p2 = Point(vertices[vcount].x, vertices[vcount].y)
            else:
                p1 = Point(vertex.x, vertex.y)
                p2 = Point(vertices[key - 1].x, vertices[key - 1].y)
            pc = geoms.fraction_along_line(p1, p2, 0.5)  # centre pt of edge
            _perbii_pts.append(pc)  # debug use
            compass, angle = geoms.angles_from_points(centre, pc)
            # f"*** RECT *** perbii {key=} {directions[key]=} {pc=} {compass=} {angle=}"
            _perbii = Perbis(
                point=pc,
                direction=directions[key],
                v1=p1,
                v2=p2,
                compass=compass,
                angle=angle,
            )
            perbii_dict[directions[key]] = _perbii
        return perbii_dict

    def calculate_xy(self, **kwargs):
        # ---- adjust start
        # feedback(f'***Rect{self.col=}{self.row=} {self._u.offset_x=}{self._o.off_x=}')
        if self.row is not None and self.col is not None:
            if self.kwargs.get("grouping_cols", 1) == 1:
                x = (
                    self.col * (self._u.width + self._u.spacing_x)
                    + self._o.delta_x
                    + self._u.offset_x
                )
            else:
                group_no = self.col // self.kwargs["grouping_cols"]
                x = (
                    self.col * self._u.width
                    + self._u.spacing_x * group_no
                    + self._o.delta_x
                    + self._u.offset_x
                )
            if self.kwargs.get("grouping_rows", 1) == 1:
                y = (
                    self.row * (self._u.height + self._u.spacing_y)
                    + self._o.delta_y
                    + self._u.offset_y
                )
            else:
                group_no = self.row // self.kwargs["grouping_rows"]
                y = (
                    self.row * self._u.height
                    + self._u.spacing_y * group_no
                    + self._o.delta_y
                    + self._u.offset_y
                )
        elif self.cx is not None and self.cy is not None:
            x = self._u.cx - self._u.width / 2.0 + self._o.delta_x
            y = self._u.cy - self._u.height / 2.0 + self._o.delta_y
        else:
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
        # ---- overrides to centre the shape
        if kwargs.get("cx") and kwargs.get("cy"):
            x = kwargs.get("cx") - self._u.width / 2.0
            y = kwargs.get("cy") - self._u.height / 2.0
        return x, y

    def get_angles(self, rotation=0, **kwargs):
        """Get angles from centre to vertices for rectangle without notches."""
        x, y = self.calculate_xy(**kwargs)
        vertices = self.get_vertexes(rotation=rotation, **kwargs)
        centre = Point(x + self._u.height / 2.0, y + self._u.height / 2.0)
        angles = []
        for vtx in vertices:
            _, angle = geoms.angles_from_points(centre, vtx)
            angles.append(angle)
        return angles

    def get_vertexes(self, **kwargs):
        """Get vertices for rectangle without notches."""
        x, y = self.calculate_xy(**kwargs)
        # ---- overrides for grid layout
        if self.use_abs_c:
            x = self._abs_cx - self._u.width / 2.0
            y = self._abs_cy - self._u.height / 2.0
        vertices = [  # anti-clockwise from top-left; relative to centre
            Point(x, y),  # e
            Point(x, y + self._u.height),  # s
            Point(x + self._u.width, y + self._u.height),  # w
            Point(x + self._u.width, y),  # n
        ]
        # feedback(
        #     '*** RECT VERTS '
        #     f' /0: {vertices[0][0]:.2f};{vertices[0][1]:.2f}'
        #     f' /1: {vertices[1][0]:.2f};{vertices[1][1]:.2f}'
        #     f' /2: {vertices[2][0]:.2f};{vertices[2][1]:.2f}'
        #     f' /3: {vertices[3][0]:.2f};{vertices[3][1]:.2f}'
        # )
        return vertices

    def set_coord(self, cnv, x_d, y_d):
        """Set (optionally draw) the coords of the rectangle."""
        the_row = self.row or 0
        the_col = self.col or 0
        # _row = self.rows - the_row + self.coord_start_y
        _row = the_row + 1 if not self.coord_start_y else the_row + self.coord_start_y
        _col = the_col + 1 if not self.coord_start_x else the_col + self.coord_start_x
        # feedback(f'*** Rect # ---- {_row=},{_col=}')
        # ---- set coord x,y values
        if self.coord_type_x in ["l", "lower"]:
            _x = tools.sheet_column(_col, True)
        elif self.coord_type_x in ["l-m", "lower-multiple"]:
            _x = tools.alpha_column(_col, True)
        elif self.coord_type_x in ["u", "upper"]:
            _x = tools.sheet_column(_col)
        elif self.coord_type_x in ["u-m", "upper-multiple"]:
            _x = tools.alpha_column(_col)
        else:
            _x = str(_col).zfill(self.coord_padding)  # numeric
        if self.coord_type_y in ["l", "lower"]:
            _y = tools.sheet_column(_row, True)
        elif self.coord_type_y in ["l-m", "lower-multiple"]:
            _y = tools.alpha_column(_row, True)
        elif self.coord_type_y in ["u", "upper"]:
            _y = tools.sheet_column(_row)
        elif self.coord_type_y in ["u-m", "upper-multiple"]:
            _y = tools.alpha_column(_row)
        else:
            _y = str(_row).zfill(self.coord_padding)  # numeric
        # ---- set coord label
        self.coord_text = (
            str(self.coord_prefix)
            + _x
            + str(self.coord_separator)
            + _y
            + str(self.coord_suffix)
        )
        # ---- draw coord (optional)
        if self.coord_elevation:
            # ---- * set coord props
            cnv.setFont(self.coord_font_name, self.coord_font_size)
            cnv.setFillColor(self.coord_stroke)
            coord_offset = self.unit(self.coord_offset)
            if self.coord_elevation in ["t", "top"]:
                self.draw_multi_string(cnv, x_d, y_d + coord_offset, self.coord_text)
            elif self.coord_elevation in ["m", "middle", "mid"]:
                self.draw_multi_string(
                    cnv,
                    x_d,
                    y_d + coord_offset - self.coord_font_size / 2.0,
                    self.coord_text,
                )
            elif self.coord_elevation in ["b", "bottom", "bot"]:
                self.draw_multi_string(cnv, x_d, y_d + coord_offset, self.coord_text)
            else:
                feedback(f'Cannot handle a coord_elevation of "{self.coord_elevation}"')

    def set_notch_vertexes(self, x, y):
        """Calculate vertices needed to draw a Rectangle."""
        _notch_style = _lower(self.notch_style)
        if self.notch_directions:
            _ntches = self.notch_directions.split()
            _notches = [str(ntc).upper() for ntc in _ntches]
        # feedback(f'*** Rect {self.notch_x=} {self.notch_y=} {_notches=} ')
        n_x = self.unit(self.notch_x) if self.notch_x else self.unit(self.notch)
        n_y = self.unit(self.notch_y) if self.notch_y else self.unit(self.notch)
        self.vertexes = []

        if "NW" in _notches:
            match _notch_style:
                case "snip" | "s":
                    self.vertexes.append(Point(x + n_x, y))
                    self.vertexes.append(Point(x, y + n_y))
                case "fold" | "d":
                    self.vertexes.append(Point(x, y))
                    self.vertexes.append(Point(x + n_x, y))
                    self.vertexes.append(Point(x, y + n_y))
                case "flap" | "p":
                    self.vertexes.append(Point(x + n_x, y))
                    self.vertexes.append(Point(x, y + n_y))
                    self.vertexes.append(Point(x + n_x, y + n_y))
                    self.vertexes.append(Point(x + n_x, y))
                    self.vertexes.append(Point(x, y + n_y))
                case "step" | "t":
                    pass
        else:
            self.vertexes.append(Point(x, y))

        if "SW" in _notches:
            self.vertexes.append(Point(x, y + self._u.height - n_y))
            match _notch_style:
                case "snip" | "s":
                    self.vertexes.append(Point(x + n_x, y + self._u.height))
                case "fold" | "d":
                    self.vertexes.append(Point(x + n_x, y + self._u.height))
                    self.vertexes.append(Point(x, y + self._u.height))
                    self.vertexes.append(Point(x, y + self._u.height - n_y))
                    self.vertexes.append(Point(x + n_x, y + self._u.height))
                case "flap" | "p":
                    self.vertexes.append(Point(x + n_x, y + self._u.height))
                    self.vertexes.append(Point(x + n_x, y + self._u.height - n_y))
                    self.vertexes.append(Point(x, y + self._u.height - n_y))
                    self.vertexes.append(Point(x + n_x, y + self._u.height))
                case "step" | "t":
                    self.vertexes.append(Point(x + n_x, y + self._u.height - n_y))
                    self.vertexes.append(Point(x + n_x, y + self._u.height))
        else:
            self.vertexes.append(Point(x, y + self._u.height))

        if "SE" in _notches:
            self.vertexes.append(Point(x + self._u.width - n_x, y + self._u.height))
            match _notch_style:
                case "snip" | "s":
                    self.vertexes.append(
                        Point(x + self._u.width, y + self._u.height - n_y)
                    )
                case "fold" | "d":
                    self.vertexes.append(
                        Point(x + self._u.width, y + self._u.height - n_y)
                    )
                    self.vertexes.append(Point(x + self._u.width, y + self._u.height))
                    self.vertexes.append(
                        Point(x + self._u.width - n_x, y + self._u.height)
                    )
                    self.vertexes.append(
                        Point(x + self._u.width, y + self._u.height - n_y)
                    )
                case "flap" | "p":
                    self.vertexes.append(
                        Point(x + self._u.width, y + self._u.height - n_y)
                    )
                    self.vertexes.append(
                        Point(x + self._u.width - n_x, y + self._u.height - n_y)
                    )
                    self.vertexes.append(
                        Point(x + self._u.width - n_x, y + self._u.height)
                    )
                    self.vertexes.append(
                        Point(x + self._u.width, y + self._u.height - n_y)
                    )
                case "step" | "t":
                    self.vertexes.append(
                        Point(x + self._u.width - n_x, y + self._u.height - n_y)
                    )
                    self.vertexes.append(
                        Point(x + self._u.width, y + self._u.height - n_y)
                    )
        else:
            self.vertexes.append(Point(x + self._u.width, y + self._u.height))

        if "NE" in _notches:
            self.vertexes.append(Point(x + self._u.width, y + n_y))
            match _notch_style:
                case "snip" | "s":
                    self.vertexes.append(Point(x + self._u.width - n_x, y))
                case "fold" | "d":
                    self.vertexes.append(Point(x + self._u.width - n_x, y))
                    self.vertexes.append(Point(x + self._u.width, y))
                    self.vertexes.append(Point(x + self._u.width, y + n_y))
                    self.vertexes.append(Point(x + self._u.width - n_x, y))
                case "flap" | "p":
                    self.vertexes.append(Point(x + self._u.width - n_x, y))
                    self.vertexes.append(Point(x + self._u.width - n_x, y + n_y))
                    self.vertexes.append(Point(x + self._u.width, y + n_y))
                    self.vertexes.append(Point(x + self._u.width - n_x, y))
                case "step" | "t":
                    self.vertexes.append(Point(x + self._u.width - n_x, y + n_y))
                    self.vertexes.append(Point(x + self._u.width - n_x, y))
        else:
            self.vertexes.append(Point(x + self._u.width, y))

        if "NW" in _notches:
            match _notch_style:
                case "snip" | "s":
                    pass
                case "fold" | "d":
                    self.vertexes.append(Point(x, y))
                    self.vertexes.append(Point(x + n_x, y))
                    self.vertexes.append(Point(x, y + n_y))
                case "flap" | "p":
                    pass
                    # self.vertexes.append(Point(x + n_x, y + n_y))
                    # self.vertexes.append(Point(x + n_x, y))
                    # self.vertexes.append(Point(x, y + n_y))
                case "step" | "t":
                    self.vertexes.append(Point(x + n_x, y))
                    self.vertexes.append(Point(x + n_x, y + n_y))
                    self.vertexes.append(Point(x, y + n_y))
        else:
            self.vertexes.append(Point(x, y))

    def draw_corners(self, cnv, ID, x, y):
        """Add corners (lines/shapes) to a Rectangle."""
        _corners_style = _lower(self.corners_style)
        if self.corners_directions:
            _crnrs = self.corners_directions.split()
            _corners = [str(crn).upper() for crn in _crnrs]
        # feedback(f'*** Rect corners {_corners=} ')
        o_x = self.unit(self.corners_x) if self.corners_x else self.unit(self.corners)
        o_y = self.unit(self.corners_y) if self.corners_y else self.unit(self.corners)
        # feedback(f'*** Rect corners {o_x=} {o_y=} ')
        ox3 = o_x / 3.0
        oy3 = o_y / 3.0
        if "NW" in _corners:
            match _corners_style:
                case "line" | "l":
                    cnv.draw_line(Point(x, y), Point(x, y + o_y))
                    cnv.draw_line(Point(x, y), Point(x + o_x, y))
                case "triangle" | "t":
                    cnv.draw_line(Point(x, y), Point(x, y + o_y))
                    cnv.draw_line(Point(x, y + o_y), Point(x + o_x, y)),
                    cnv.draw_line(Point(x + o_x, y), Point(x, y))
                case "curve" | "c":
                    cnv.draw_line(Point(x, y), Point(x, y + o_y))
                    cnv.draw_curve(
                        Point(x, y + o_y),
                        Point(x, y),
                        Point(x + o_x, y),
                    )
                    cnv.draw_line(Point(x + o_x, y), Point(x, y))
                case "photo" | "p":
                    cnv.draw_line(Point(x, y), Point(x, y + o_y))
                    cnv.draw_line(Point(x, y + o_y), Point(x + ox3, y + o_y - oy3)),
                    cnv.draw_line(
                        Point(x + ox3, y + o_y - oy3), Point(x + ox3, y + oy3)
                    ),
                    cnv.draw_line(Point(x + ox3, y + oy3), Point(x + 2 * ox3, y + oy3)),
                    cnv.draw_line(Point(x + 2 * ox3, y + oy3), Point(x + o_x, y)),
                    cnv.draw_line(Point(x + o_x, y), Point(x, y))
        if "SE" in _corners:
            match _corners_style:
                case "line" | "l":
                    cnv.draw_line(
                        Point(x + self._u.width, y + self._u.height),
                        Point(x + self._u.width, y + self._u.height - o_y),
                    )
                    cnv.draw_line(
                        Point(x + self._u.width, y + self._u.height),
                        Point(x + self._u.width - o_x, y + self._u.height),
                    )
                case "triangle" | "t":
                    cnv.draw_line(
                        Point(x + self._u.width, y + self._u.height),
                        Point(x + self._u.width, y + self._u.height - o_y),
                    )
                    cnv.draw_line(
                        Point(x + self._u.width, y + self._u.height - o_y),
                        Point(x + self._u.width - o_x, y + self._u.height),
                    )
                    cnv.draw_line(
                        Point(x + self._u.width - o_x, y + self._u.height),
                        Point(x + self._u.width, y + self._u.height),
                    )
                case "curve" | "c":
                    cnv.draw_line(
                        Point(x + self._u.width, y + self._u.height),
                        Point(x + self._u.width, y + self._u.height - o_y),
                    )
                    cnv.draw_curve(
                        Point(x + self._u.width, y + self._u.height - o_y),
                        Point(x + self._u.width, y + self._u.height),
                        Point(x + self._u.width - o_x, y + self._u.height),
                    )
                    cnv.draw_line(
                        Point(x + self._u.width - o_x, y + self._u.height),
                        Point(x + self._u.width, y + self._u.height),
                    )
                case "photo" | "p":
                    cnv.draw_line(
                        Point(x + self._u.width, y + self._u.height),
                        Point(x + self._u.width, y + self._u.height - o_y),
                    )
                    cnv.draw_line(
                        Point(x + self._u.width, y + self._u.height - o_y),
                        Point(x + self._u.width - ox3, y + self._u.height - o_y + oy3),
                    )
                    cnv.draw_line(
                        Point(x + self._u.width - ox3, y + self._u.height - o_y + oy3),
                        Point(
                            x + self._u.width - ox3, y + self._u.height - o_y + 2 * oy3
                        ),
                    )
                    cnv.draw_line(
                        Point(
                            x + self._u.width - ox3, y + self._u.height - o_y + 2 * oy3
                        ),
                        Point(
                            x + self._u.width - 2 * ox3,
                            y + self._u.height - o_y + 2 * oy3,
                        ),
                    )
                    cnv.draw_line(
                        Point(
                            x + self._u.width - 2 * ox3,
                            y + self._u.height - o_y + 2 * oy3,
                        ),
                        Point(x + self._u.width - o_x, y + self._u.height),
                    )
                    cnv.draw_line(
                        Point(x + self._u.width - o_x, y + self._u.height),
                        Point(x + self._u.width, y + self._u.height),
                    )
        if "NE" in _corners:
            match _corners_style:
                case "line" | "l":
                    cnv.draw_line(
                        Point(x + self._u.width, y),
                        Point(x + self._u.width, y + o_y),
                    )
                    cnv.draw_line(
                        Point(x + self._u.width, y),
                        Point(x + self._u.width - o_x, y),
                    )
                case "triangle" | "t":
                    cnv.draw_line(
                        Point(x + self._u.width, y),
                        Point(x + self._u.width, y + o_y),
                    )
                    cnv.draw_line(
                        Point(x + self._u.width, y + o_y),
                        Point(x + self._u.width - o_x, y),
                    )
                    cnv.draw_line(
                        Point(x + self._u.width - o_x, y),
                        Point(x + self._u.width, y),
                    )
                case "curve" | "c":
                    cnv.draw_line(
                        Point(x + self._u.width, y),
                        Point(x + self._u.width, y + o_y),
                    )
                    cnv.draw_curve(
                        Point(x + self._u.width, y + o_y),
                        Point(x + self._u.width, y),
                        Point(x + self._u.width - o_x, y),
                    )
                    cnv.draw_line(
                        Point(x + self._u.width - o_x, y),
                        Point(x + self._u.width, y),
                    )
                case "photo" | "p":
                    cnv.draw_line(
                        Point(x + self._u.width, y),
                        Point(x + self._u.width, y + o_y),
                    )
                    cnv.draw_line(
                        Point(x + self._u.width, y + o_y),
                        Point(x + self._u.width - ox3, y + o_y - oy3),
                    )
                    cnv.draw_line(
                        Point(x + self._u.width - ox3, y + o_y - oy3),
                        Point(x + self._u.width - ox3, y + o_y - 2 * oy3),
                    )
                    cnv.draw_line(
                        Point(x + self._u.width - ox3, y + o_y - 2 * oy3),
                        Point(x + self._u.width - 2 * ox3, y + o_y - 2 * oy3),
                    )
                    cnv.draw_line(
                        Point(x + self._u.width - 2 * ox3, y + o_y - 2 * oy3),
                        Point(x + self._u.width - o_x, y),
                    )
                    cnv.draw_line(
                        Point(x + self._u.width - o_x, y),
                        Point(x + self._u.width, y),
                    )
        if "SW" in _corners:
            match _corners_style:
                case "line" | "l":
                    cnv.draw_line(
                        Point(x, y + self._u.height), Point(x, y + self._u.height - o_y)
                    )
                    cnv.draw_line(
                        Point(x, y + self._u.height), Point(x + o_x, y + self._u.height)
                    )
                case "triangle" | "t":
                    cnv.draw_line(
                        Point(x, y + self._u.height), Point(x, y + self._u.height - o_y)
                    )
                    cnv.draw_line(
                        Point(x, y + self._u.height - o_y),
                        Point(x + o_x, y + self._u.height),
                    )
                    cnv.draw_line(
                        Point(x + o_x, y + self._u.height),
                        Point(x, y + self._u.height),
                    )
                case "curve" | "c":
                    cnv.draw_line(
                        Point(x, y + self._u.height), Point(x, y + self._u.height - o_y)
                    )
                    cnv.draw_curve(
                        Point(x, y + self._u.height - o_y),
                        Point(x, y + self._u.height),
                        Point(x + o_x, y + self._u.height),
                    )
                    cnv.draw_line(
                        Point(x + o_x, y + self._u.height),
                        Point(x, y + self._u.height),
                    )
                case "photo" | "p":
                    cnv.draw_line(
                        Point(x, y + self._u.height), Point(x, y + self._u.height - o_y)
                    )
                    cnv.draw_line(
                        Point(x, y + self._u.height - o_y),
                        Point(x + ox3, y + self._u.height - o_y + oy3),
                    )
                    cnv.draw_line(
                        Point(x + ox3, y + self._u.height - o_y + oy3),
                        Point(x + ox3, y + self._u.height - o_y + 2 * oy3),
                    )
                    cnv.draw_line(
                        Point(x + ox3, y + self._u.height - o_y + 2 * oy3),
                        Point(x + 2 * ox3, y + self._u.height - o_y + 2 * oy3),
                    )
                    cnv.draw_line(
                        Point(x + 2 * ox3, y + self._u.height - o_y + 2 * oy3),
                        Point(x + o_x, y + self._u.height),
                    )
                    cnv.draw_line(
                        Point(x + o_x, y + self._u.height),
                        Point(x, y + self._u.height),
                    )
        # apply
        gargs = {}
        gargs["fill"] = self.corners_fill
        gargs["stroke"] = self.corners_stroke
        gargs["stroke_width"] = self.corners_stroke_width
        gargs["stroke_ends"] = self.corners_ends
        gargs["dotted"] = self.corners_dots
        self.set_canvas_props(cnv=None, index=ID, **gargs)

    def draw_bite_rectangle(self, cnv, x, y):
        """Draw a Rectangle with inward curved corners."""
        if self.notch_directions:
            _ntches = self.notch_directions.split()
            _notches = [str(ntc).upper() for ntc in _ntches]
        # feedback(f'*** Rect bite {self.notch_x=} {self.notch_y=} {_notches=} ')
        n_x = self.unit(self.notch_x) if self.notch_x else self.unit(self.notch)
        n_y = self.unit(self.notch_y) if self.notch_y else self.unit(self.notch)
        # feedback(f'*** Rect bite {n_x=} {n_y=} ')
        if "NW" in _notches:
            p1 = Point(x, y + n_y)
        else:
            p1 = Point(x, y)
        if "SW" in _notches:
            p2 = Point(x, y + self._u.height - n_y)
            p3 = Point(x + n_x, y + self._u.height)
            pm = Point(x + n_x, y + self._u.height - n_y)
            cnv.draw_line(p1, p2)
            cnv.draw_curve(p2, pm, p3)
        else:
            p2 = Point(x, y + self._u.height)
            p3 = p2
            cnv.draw_line(p1, p3)
        if "SE" in _notches:
            p4 = Point(x + self._u.width - n_x, y + self._u.height)
            p5 = Point(x + self._u.width, y + self._u.height - n_y)
            pm = Point(x + self._u.width - n_x, y + self._u.height - n_y)
            cnv.draw_line(p3, p4)
            cnv.draw_curve(p4, pm, p5)
        else:
            p4 = Point(x + self._u.width, y + self._u.height)
            p5 = p4
            cnv.draw_line(p3, p5)
        if "NE" in _notches:
            p6 = Point(x + self._u.width, y + n_y)
            p7 = Point(x + self._u.width - n_x, y)
            pm = Point(x + self._u.width - n_x, y + n_y)
            cnv.draw_line(p5, p6)
            cnv.draw_curve(p6, pm, p7)
        else:
            p6 = Point(x + self._u.width, y)
            p7 = p6
            cnv.draw_line(p5, p7)
        if "NW" in _notches:
            p8 = Point(x + n_x, y)
            pm = Point(x + n_x, y + n_y)
            cnv.draw_line(p7, p8)
            cnv.draw_curve(p8, pm, p1)
        else:
            cnv.draw_line(p7, p1)

    def draw_hatches(self, cnv, ID, vertices: list, num: int, rotation: float = 0.0):
        """Draw line(s) from one side of Rectangle to the parallel opposite.

        Args:
            ID: unique ID
            vertices: the rectangle's nodes
            num: number of lines
            rotation: degrees anti-clockwise from horizontal "east"
        """
        _dirs = tools.validated_directions(
            self.hatches, DirectionGroup.CIRCULAR, "hatches"
        )
        lines = tools.as_int(num, "hatches_count")
        # ---- check dirs
        if self.rounding or self.rounded:
            if (
                "ne" in _dirs
                or "sw" in _dirs
                or "se" in _dirs
                or "nw" in _dirs
                or "d" in _dirs
            ):
                feedback(
                    "No diagonal hatches permissible with rounding in the rectangle",
                    True,
                )
        # ---- check spaces
        if self.rounding or self.rounded:
            spaces = max(self._u.width / (lines + 1), self._u.height / (lines + 1))
            if self.rounding:
                _rounding = self.unit(self.rounding)
            elif self.rounded:
                _rounding = self._u.width * 0.08
            if spaces < _rounding:
                feedback(
                    "No hatches permissible with this size of rounding in a rectangle",
                    True,
                )
        if self.notch and self.hatches_count > 1 or self.notch_x or self.notch_y:
            if (
                "ne" in _dirs
                or "sw" in _dirs
                or "se" in _dirs
                or "nw" in _dirs
                or "d" in _dirs
            ):
                feedback(
                    "Multi-diagonal hatches not permissible in a notched Rectangle",
                    True,
                )
        # ---- draw items
        if lines >= 1:
            if "se" in _dirs or "nw" in _dirs or "d" in _dirs:  # UP to the right
                cnv.draw_line(
                    (vertices[0].x, vertices[0].y), (vertices[2].x, vertices[2].y)
                )
            if "sw" in _dirs or "ne" in _dirs or "d" in _dirs:  # DOWN to the right
                cnv.draw_line(
                    (vertices[1].x, vertices[1].y), (vertices[3].x, vertices[3].y)
                )
            if "n" in _dirs or "s" in _dirs or "o" in _dirs:  # vertical
                x_dist = self._u.width / (lines + 1)
                for i in range(1, lines + 1):
                    cnv.draw_line(
                        (vertices[0].x + i * x_dist, vertices[1].y),
                        (vertices[0].x + i * x_dist, vertices[0].y),
                    )
            if "e" in _dirs or "w" in _dirs or "o" in _dirs:  # horizontal
                y_dist = self._u.height / (lines + 1)
                for i in range(1, lines + 1):
                    cnv.draw_line(
                        (vertices[0].x, vertices[0].y + i * y_dist),
                        (vertices[0].x + self._u.width, vertices[0].y + i * y_dist),
                    )

        if lines >= 1:
            diag_num = int((lines - 1) / 2 + 1)
            x_dist = self._u.width / diag_num
            y_dist = self._u.height / diag_num
            top_pt, btm_pt, left_pt, rite_pt = [], [], [], []
            for number in range(0, diag_num + 1):
                left_pt.append(
                    geoms.point_on_line(vertices[0], vertices[1], y_dist * number)
                )
                top_pt.append(
                    geoms.point_on_line(vertices[1], vertices[2], x_dist * number)
                )
                rite_pt.append(
                    geoms.point_on_line(vertices[3], vertices[2], y_dist * number)
                )
                btm_pt.append(
                    geoms.point_on_line(vertices[0], vertices[3], x_dist * number)
                )

        if "se" in _dirs or "nw" in _dirs or "d" in _dirs:  # slope UP to the right
            for i in range(1, diag_num):  # top-left side
                j = diag_num - i
                cnv.draw_line((left_pt[i].x, left_pt[i].y), (top_pt[j].x, top_pt[j].y))
            for i in range(1, diag_num):  # bottom-right side
                j = diag_num - i
                cnv.draw_line((btm_pt[i].x, btm_pt[i].y), (rite_pt[j].x, rite_pt[j].y))
        if "ne" in _dirs or "sw" in _dirs or "d" in _dirs:  # slope down to the right
            for i in range(1, diag_num):  # bottom-left side
                cnv.draw_line((left_pt[i].x, left_pt[i].y), (btm_pt[i].x, btm_pt[i].y))
            for i in range(1, diag_num):  # top-right side
                cnv.draw_line((top_pt[i].x, top_pt[i].y), (rite_pt[i].x, rite_pt[i].y))
        # ---- set canvas
        cx = vertices[0].x + 0.5 * self._u.width
        cy = vertices[0].y + 0.5 * self._u.height
        self.set_canvas_props(
            index=ID,
            stroke=self.hatches_stroke,
            stroke_width=self.hatches_stroke_width,
            stroke_ends=self.hatches_ends,
            dashed=self.hatches_dashed,
            dotted=self.hatches_dots,
            rotation=rotation,
            rotation_point=muPoint(cx, cy),
        )

    def draw_perbii(self, cnv, ID, centre: Point, rotation: float = None, **kwargs):
        """Draw lines connecting the Rectangle centre to the centre of each edge.

        Args:
            ID: unique ID
            centre (Point): the centre Point of the Rectangle
            rotation: degrees anti-clockwise from horizontal "east"

        Notes:
            A perpendicular bisector ("perbis") of a chord is:
                A line passing through the center of circle such that it divides
                the chord into two equal parts and meets the chord at a right angle;
                for a polygon, each edge is effectively a chord.
        """
        vertices = self.get_vertexes(rotation=rotation, **kwargs)
        perbii_dict = self.calculate_perbii(cnv=cnv, centre=centre, vertices=vertices)
        pb_length = (
            self.unit(self.perbii_length, label="perbii length")
            if self.perbii_length
            else None  # see below for default length
        )
        if self.perbii:
            perbii_dirs = tools.validated_directions(
                self.perbii, DirectionGroup.CARDINAL, "rectangle perbii"
            )

        # ---- set perbii styles
        lkwargs = {}
        lkwargs["wave_style"] = self.kwargs.get("perbii_wave_style", None)
        lkwargs["wave_height"] = self.kwargs.get("perbii_wave_height", 0)
        for key, a_perbii in perbii_dict.items():
            if self.perbii and key not in perbii_dirs:
                continue
            # offset based on dir
            if key in ["n", "s"]:
                pb_offset = self.unit(self.perbii_offset, label="perbii offset") or 0
                pb_offset = (
                    self.unit(self.perbii_offset_y, label="perbii offset") or pb_offset
                )
            if key in ["e", "w"]:
                pb_offset = self.unit(self.perbii_offset, label="perbii offset") or 0
                pb_offset = (
                    self.unit(self.perbii_offset_x, label="perbii offset") or pb_offset
                )
            # length based on dir
            if not pb_length:
                if key in ["n", "s"]:
                    pb_length = self._u.height / 2.0
                if key in ["e", "w"]:
                    pb_length = self._u.width / 2.0
            # points based on length of line, offset and the angle in degrees
            edge_pt = a_perbii.point
            if pb_offset is not None and pb_offset != 0:
                offset_pt = geoms.point_on_circle(centre, pb_offset, a_perbii.angle)
                end_pt = geoms.point_on_line(offset_pt, edge_pt, pb_length)
                # print(f"{key=} {centre=} {pb_offset=} {a_perbii.angle=} {offset_pt=}")
                start_point = offset_pt.x, offset_pt.y
                end_point = end_pt.x, end_pt.y
            else:
                start_point = centre.x, centre.y
                end_point = edge_pt.x, edge_pt.y
            # ---- draw a perbii line
            draw_line(
                cnv,
                start_point,
                end_point,
                shape=self,
                **lkwargs,
            )

        self.set_canvas_props(
            index=ID,
            stroke=self.perbii_stroke,
            stroke_width=self.perbii_stroke_width,
            stroke_ends=self.perbii_ends,
            dashed=self.perbii_dashed,
            dotted=self.perbii_dotted,
        )

    def draw_radii(self, cnv, ID, centre: Point, vertices: list):
        """Draw line(s) connecting the Rectangle centre to a vertex.

        Args:
            ID: unique ID
            vertices: list of Rectangle nodes as Points
            centre: the centre Point of the Rectangle

        Note:
            * vertices start top-left and are ordered anti-clockwise
        """
        _dirs = tools.validated_directions(
            self.radii, DirectionGroup.ORDINAL, "rectangle radii"
        )
        if "nw" in _dirs:  # slope UP to the left
            cnv.draw_line(centre, vertices[0])
        if "sw" in _dirs:  # slope DOWN to the left
            cnv.draw_line(centre, vertices[1])
        if "se" in _dirs:  # slope DOWN to the right
            cnv.draw_line(centre, vertices[2])
        if "ne" in _dirs:  # slope UP to the right
            cnv.draw_line(centre, vertices[3])
        # color, thickness etc.
        self.set_canvas_props(
            index=ID,
            stroke=self.radii_stroke or self.stroke,
            stroke_width=self.radii_stroke_width or self.stroke_width,
            stroke_ends=self.radii_ends,
        )

    def draw_slices(self, cnv, ID, vertexes, rotation=0):
        """Draw triangles and trapezoids inside the Rectangle

        Args:
            ID: unique ID
            vertexes: the rectangle's nodes
            rotation: degrees anti-clockwise from horizontal "east"
        """
        # ---- get slices color list from string
        if isinstance(self.slices, str):
            _slices = tools.split(self.slices.strip())
        else:
            _slices = self.slices
        # ---- validate slices color settings
        err = ("Roof must be a list of colors - either 2 or 4",)
        if not isinstance(_slices, list):
            feedback(err, True)
        else:
            if len(_slices) not in [2, 4]:
                feedback(err, True)
        slices_colors = [colrs.get_color(slcolor) for slcolor in _slices]
        # ---- draw 2 triangles
        if len(slices_colors) == 2:
            # top-left
            vertexes_tl = [vertexes[0], vertexes[1], vertexes[3]]
            cnv.draw_polyline(vertexes_tl)
            self.set_canvas_props(
                index=ID,
                stroke=self.slices_stroke or slices_colors[0],
                stroke_ends=self.slices_ends,
                fill=slices_colors[0],
                transparency=self.slices_transparency,
                closed=True,
                rotation=rotation,
                rotation_point=self.centroid,
            )
            # bottom-right
            vertexes_br = [vertexes[1], vertexes[2], vertexes[3]]
            cnv.draw_polyline(vertexes_br)
            self.set_canvas_props(
                index=ID,
                stroke=self.slices_stroke or slices_colors[1],
                stroke_ends=self.slices_ends,
                fill=slices_colors[1],
                transparency=self.slices_transparency,
                closed=True,
                rotation=rotation,
                rotation_point=self.centroid,
            )
        # ---- draw 2 (or 4) triangles and (maybe) 2 trapezoids
        elif len(slices_colors) == 4:
            dx = (vertexes[3].x - vertexes[0].x) / 2.0
            dy = (vertexes[1].y - vertexes[0].y) / 2.0
            midpt = Point(vertexes[0].x + dx, vertexes[0].y + dy)
            if self.slices_line:
                _line = self._u_slices_line / 2.0
                midleft = Point(
                    midpt.x - _line + self._u_slices_line_mx,
                    midpt.y + self._u_slices_line_my,
                )
                midrite = Point(
                    midpt.x + _line + self._u_slices_line_mx,
                    midpt.y + self._u_slices_line_my,
                )
                vert_t = [vertexes[0], midleft, midrite, vertexes[3]]
                vert_r = [vertexes[3], midrite, vertexes[2]]
                vert_b = [vertexes[1], midleft, midrite, vertexes[2]]
                vert_l = [vertexes[0], midleft, vertexes[1]]
            else:
                vert_t = [vertexes[0], midpt, vertexes[3]]
                vert_r = [vertexes[3], midpt, vertexes[2]]
                vert_b = [vertexes[1], midpt, vertexes[2]]
                vert_l = [vertexes[0], midpt, vertexes[1]]

            sections = [vert_l, vert_r, vert_t, vert_b]  # order is important!
            for key, section in enumerate(sections):
                cnv.draw_polyline(section)
                self.set_canvas_props(
                    index=ID,
                    stroke=self.slices_stroke or slices_colors[key],
                    stroke_ends=self.slices_ends,
                    fill=slices_colors[key],
                    transparency=self.slices_transparency,
                    closed=True,
                    rotation=rotation,
                    rotation_point=self.centroid,
                )

    def draw_stripes(self, cnv, ID, vertices: list, rotation: float = 0.0):
        """Draw tetragons between two sides of a Rectangle.

        Args:
            cnv: PyMuPDF Page object
            ID (int): unique ID
            vertices (list): the Rectangle's nodes
            rotation (float): degrees anti-clockwise from horizontal "east"
        """

        def apply_props(cx, cy):
            self.set_canvas_props(
                index=ID,
                fill=self.stripes_fill,
                stroke=self.stripes_stroke,
                stroke_width=self.stripes_stroke_width,
                transparency=self.stripes_transparency,
                dashed=self.stripes_dashed,
                dotted=self.stripes_dotted,
                rotation=rotation,
                rotation_point=muPoint(cx, cy),
                closed=True,
            )

        # ---- set canvas
        cx = vertices[0].x + 0.5 * self._u.width
        cy = vertices[0].y + 0.5 * self._u.height
        # ---- basic checks
        _dirs = tools.validated_directions(
            self.stripes_directions, DirectionGroup.CIRCULAR, "stripes directions"
        )
        if not _dirs:
            _dirs = ["n"]  # default
        if "*" in _dirs or "all" in _dirs:
            is_all = True
        else:
            is_all = False
        lines = tools.as_int(self.stripes, "stripes")
        if lines % 2 == 0 or lines < 1:
            feedback(
                f"Stripes must be an odd number, greater than zero (not {lines}).", True
            )
        # ---- check rounding limits
        if self.rounding or self.rounded:
            if self.stripes_flush:
                feedback(
                    "No flush stripes permissible with rounding in the rectangle",
                    True,
                )
            if (
                "ne" in _dirs
                or "sw" in _dirs
                or "se" in _dirs
                or "nw" in _dirs
                or "d" in _dirs
            ):
                feedback(
                    "No diagonal stripes permissible with rounding in the rectangle",
                    True,
                )
        # ---- check notches
        if self.notch and self.stripes > 0 or self.notch_x or self.notch_y:
            if (
                "ne" in _dirs
                or "sw" in _dirs
                or "se" in _dirs
                or "nw" in _dirs
                or "d" in _dirs
            ):
                feedback(
                    "Stripes not permissible in a notched Rectangle",
                    True,
                )
        # ---- calculate gaps and breadth
        if self.stripes_breadth:
            _ubreadth = tools.as_float(self.stripes_breadth, "stripes_breadth")
            _breadth = self.unit(_ubreadth)
        else:
            _breadth = None
        if lines == 1:
            gaps = 2
        else:
            if self.stripes_flush:
                gaps = lines - 1
            else:
                gaps = lines + 1
        # ---- calculate and check gap size for preset breadth
        over_allocated = False
        allocations = []
        if "n" in _dirs or "s" in _dirs or "o" in _dirs or is_all:
            space_horz = self._u.width
            allocations.append(space_horz)
        if "e" in _dirs or "w" in _dirs or "o" in _dirs or is_all:
            space_vert = self._u.height
            allocations.append(space_vert)
        if "o" in _dirs:
            space_ortho = min(self._u.height, self._u.width)
            allocations.append(space_ortho)
        if (
            "ne" in _dirs
            or "sw" in _dirs
            or "nw" in _dirs
            or "se" in _dirs
            or is_all
            or "d" in _dirs
        ):
            x, y = self.calculate_xy()
            space_diag = geoms.length_of_line(
                Point(x, y), Point(x + self._u.width, y + self._u.height)
            )
            allocations.append(space_diag)
        space_min = min(allocations)
        if _breadth:
            gap_size_min = (space_min - lines * _breadth) / gaps  # also calc per dir
            if lines * _breadth > space_min:
                feedback(
                    f"The number ({lines}) and breadth ({self.stripes_breadth}) of stripes"
                    " together exceeds the available space!",
                    True,
                )
        # ---- check space available vs round corners
        if self.rounding or self.rounded:
            if self.rounding:
                _rounding = self.unit(self.rounding)
            elif self.rounded:
                _rounding = self._u.width * 0.08
            if gap_size_min < _rounding:
                feedback(
                    "No stripes permissible with this size of rounding in a Rectangle",
                    True,
                )
        # ---- draw items
        if lines >= 1:
            # ---- supports
            if (
                "nw" in _dirs
                or "se" in _dirs
                or "sw" in _dirs
                or "ne" in _dirs
                or "d" in _dirs
                or is_all
            ):
                # interior angles
                _, alpha = geoms.angles_from_points(  # diag. angle; interior; upwards
                    Point(vertices[0].x, vertices[0].y),
                    Point(vertices[2].x, vertices[2].y),
                )
                kappa = 180 - alpha  # diag. angle measured from zero east
                zeta = 90 - alpha  # diag. angle; interior; downwards
                beta = kappa - alpha
                # print(f'*** NW angles {kappa=} {alpha=} {zeta=} {beta=}')
                # line spacing
                if not _breadth:
                    _breadth = space_diag / (lines + gaps)  # divide equally
                d_breadth = _breadth / _sin(beta)  # stripe "width" along diag. angle
                gap_size = (space_diag - lines * d_breadth) / gaps  # calc for ne/sw
                # print(f'*** NW lines {_breadth=} {d_breadth=} {gap_size=}')
                off_y = gap_size / _sin(zeta)  # gap length between stripes on V-edge
                off_x = gap_size / _sin(alpha)  # gap length between stripes on H-edge
                stripe_y = _breadth / _sin(zeta)  # stripe length intersecting V-edge
                stripe_x = _breadth / _sin(alpha)  # stripe length intersecting H-edge
                # print(f'*** NW deltas {off_x=} {off_y=} {stripe_x=} {stripe_y=}')

                if self.stripes_flush:
                    x_offset = 0
                    y_offset = 0
                else:
                    x_offset = gap_size
                    y_offset = gap_size

                # primary diagonal (always)
                prime_y = (_breadth / 2.0) / _sin(zeta)
                prime_x = (_breadth / 2.0) / _sin(90 - zeta)
                # secondary diagonals (sometimes)
                diagonals_per_side = int((self.stripes - 1) / 2)
                # print(f'*** NW primary {diagonals_per_side=}')

            # ---- * diagonal UP
            if "sw" in _dirs or "ne" in _dirs or "d" in _dirs or is_all:
                # primary diagonal (always)
                # print(f'*** NW primary {prime_x=} {prime_y=}')
                p1 = Point(vertices[3].x, vertices[3].y)
                pb2 = Point(vertices[3].x, vertices[3].y + prime_y)
                pb3 = Point(vertices[1].x + prime_x, vertices[1].y)
                p4 = Point(vertices[1].x, vertices[1].y)
                pu3 = Point(vertices[1].x, vertices[1].y - prime_y)
                pu4 = Point(vertices[3].x - prime_x, vertices[3].y)
                vertexes = [p1, pb2, pb3, p4, pu3, pu4, p1]
                cnv.draw_polyline(vertexes)
                apply_props(cx, cy)
                # self._debug(cnv, vertices=vertexes)

                # secondary diagonals (sometimes)
                for each_stripe in range(0, diagonals_per_side):
                    # offset line: below
                    p1 = Point(vertices[3].x, pb2.y + off_y)
                    pb2 = Point(vertices[3].x, pb2.y + off_y + stripe_y)
                    p4 = Point(pb3.x + off_x, vertices[1].y)
                    pb3 = Point(pb3.x + off_x + stripe_x, vertices[1].y)
                    vertexes = [p1, pb2, pb3, p4, p1]
                    cnv.draw_polyline(vertexes)
                    # print(f'NE offset below: {vertexes=}')
                    # offset line: above
                    p1 = Point(pu4.x - off_x, vertices[3].y)
                    p2 = Point(vertices[1].x, pu3.y - off_y)
                    pu3 = Point(vertices[1].x, pu3.y - off_y - stripe_y)
                    pu4 = Point(pu4.x - off_x - stripe_x, vertices[3].y)
                    vertexes = [p1, p2, pu3, pu4, p1]
                    cnv.draw_polyline(vertexes)
                    # print(f'NW offset above: {vertexes=}')
                apply_props(cx, cy)

            # ---- * diagonal DOWN
            if "nw" in _dirs or "se" in _dirs or "d" in _dirs or is_all:
                # primary diagonal (always)
                # print(f'*** NW primary {prime_x=} {prime_y=}')
                p1 = Point(vertices[0].x, vertices[0].y)
                pb2 = Point(vertices[0].x, vertices[0].y + prime_y)
                pb3 = Point(vertices[2].x - prime_x, vertices[2].y)
                p4 = Point(vertices[2].x, vertices[2].y)
                pu3 = Point(vertices[2].x, vertices[2].y - prime_y)
                pu4 = Point(vertices[0].x + prime_x, vertices[0].y)
                vertexes = [p1, pb2, pb3, p4, pu3, pu4, p1]
                cnv.draw_polyline(vertexes)
                apply_props(cx, cy)

                # secondary diagonals (sometimes)
                for each_stripe in range(0, diagonals_per_side):
                    # offset line: below
                    p1 = Point(vertices[0].x, pb2.y + off_y)
                    pb2 = Point(vertices[0].x, pb2.y + off_y + stripe_y)
                    p4 = Point(pb3.x - off_x, vertices[2].y)
                    pb3 = Point(pb3.x - off_x - stripe_x, vertices[2].y)
                    vertexes = [p1, pb2, pb3, p4, p1]
                    cnv.draw_polyline(vertexes)
                    apply_props(cx, cy)
                    # print(f'NW offset below: {vertexes=}')
                    # offset line: above
                    p1 = Point(pu4.x + off_x, vertices[0].y)
                    p2 = Point(vertices[2].x, pu3.y - off_y)
                    pu3 = Point(vertices[2].x, pu3.y - off_y - stripe_y)
                    pu4 = Point(pu4.x + off_x + stripe_x, vertices[0].y)
                    vertexes = [p1, p2, pu3, pu4, p1]
                    cnv.draw_polyline(vertexes)
                    # print(f'NW offset above: {vertexes=}')
                apply_props(cx, cy)

            # ---- * vertical
            if "n" in _dirs or "s" in _dirs or "o" in _dirs or is_all:  # vertical
                if not _breadth:
                    _breadth = space_horz / (lines + gaps)  # divide equally
                gap_size = (space_horz - lines * _breadth) / gaps
                if self.stripes_flush:
                    x_offset = 0
                else:
                    x_offset = gap_size
                delta_x = gap_size + _breadth
                # print(f'*** N {lines=} {space_horz=} {_breadth=} {gap_size=} {x_offset=} {delta_x=}')
                for i in range(0, lines):
                    cnv.draw_rect(
                        (
                            vertices[0].x + i * delta_x + x_offset,
                            vertices[0].y,
                            vertices[0].x + i * delta_x + x_offset + _breadth,
                            vertices[1].y,
                        ),
                    )
                apply_props(cx, cy)

            # ---- * horizontal
            if "e" in _dirs or "w" in _dirs or "o" in _dirs or is_all:
                if not _breadth:
                    _breadth = space_vert / (lines + gaps)  # divide equally
                gap_size = (space_vert - lines * _breadth) / gaps  # calc per dir
                if self.stripes_flush:
                    y_offset = 0
                else:
                    y_offset = gap_size
                delta_y = gap_size + _breadth
                # print(f'*** N {lines=} {space_vert=} {_breadth=} {gap_size=} {y_offset=} {delta_y=}')
                for i in range(0, lines):
                    cnv.draw_rect(
                        (
                            vertices[0].x,
                            vertices[0].y + i * delta_y + y_offset,
                            vertices[2].x,
                            vertices[0].y + i * delta_y + y_offset + _breadth,
                        ),
                    )
                apply_props(cx, cy)

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a rectangle on a given canvas."""
        kwargs = self.kwargs | kwargs
        # feedback(f'\n@@@ Rect.draw {kwargs=}')
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- updated based on kwargs
        self.rounding = kwargs.get("rounding", self.rounding)
        self.grid_marks = kwargs.get("grid_marks", self.grid_marks)
        # ---- validate properties
        is_notched = True if (self.notch or self.notch_x or self.notch_y) else False
        is_chevron = True if (self.chevron or self.chevron_height) else False
        is_peaks = True if self.peaks else False
        is_prows = True if self.prows else False
        is_borders = True if self.borders else False
        is_round = True if (self.rounding or self.rounded) else False
        if self.slices and (is_round or is_notched or is_peaks or is_chevron):
            feedback("Cannot use slices with other styles.", True)
        if is_round and is_borders:
            feedback("Cannot use rounding or rounded with borders.", True)
        if is_round and is_notched:
            feedback("Cannot use rounding or rounded with notch.", True)
        if is_round and is_chevron:
            feedback("Cannot use rounding or rounded with chevron.", True)
        if is_round and is_peaks:
            feedback("Cannot use rounding or rounded with peaks.", True)
        if is_round and is_prows:
            feedback("Cannot use rounding or rounded with prows.", True)
        if self.hatches_count and is_notched and self.hatches_count > 1:
            feedback("Cannot use multiple hatches with notch.", True)
        if self.hatches_count and is_chevron:
            feedback("Cannot use hatches_count with chevron.", True)
        if is_notched and is_chevron:
            feedback("Cannot use notch and chevron together.", True)
        if is_notched and is_peaks:
            feedback("Cannot use notch and peaks together.", True)
        if is_chevron and is_peaks:
            feedback("Cannot use chevron and peaks together.", True)
        if self.hatches_count and is_peaks:
            feedback("Cannot use hatches_count and peaks together.", True)
        if is_notched and is_prows:
            feedback("Cannot use notch and prows together.", True)
        if is_chevron and is_prows:
            feedback("Cannot use chevron and prows together.", True)
        if self.hatches_count and is_prows:
            feedback("Cannot use hatches_count and prows together.", True)
        if is_borders and (is_chevron or is_peaks or is_notched or is_prows):
            feedback(
                "Cannot use borders with any of: hatches, peaks or chevron or prows.",
                True,
            )
        # ---- calculate properties
        x, y = self.calculate_xy()
        # feedback(f'*** RECT      {self.col=} {self.row=} {x=} {y=}')
        # ---- overrides for grid layout
        if self.use_abs_c:
            x = self._abs_cx - self._u.width / 2.0
            y = self._abs_cy - self._u.height / 2.0
        # ---- calculate centre
        x_d = x + self._u.width / 2.0
        y_d = y + self._u.height / 2.0
        self.area = self.calculate_area()
        delta_m_up, delta_m_down = 0.0, 0.0  # potential text offset from chevron
        # ---- handle rotation
        rotation = kwargs.get("rotation", self.rotation)
        if rotation:
            self.centroid = muPoint(x_d, y_d)
            kwargs["rotation"] = rotation
            kwargs["rotation_point"] = self.centroid
        else:
            self.centroid = None
        # ---- * notch vertices
        if is_notched:
            if _lower(self.notch_style) not in ["b", "bite"]:
                self.set_notch_vertexes(x, y)
        # ---- * prows - line/arc endpoints
        elif is_prows:
            # NB! cheating here... "point" actually stores the offset from the side!
            for key, data in self.prows_dict.items():
                _prow = {}
                _prow["height"] = self.unit(1, label="prow height")
                if len(data) >= 1:
                    _prow["height"] = self.unit(data[0], label="prow height")
                if len(data) < 2:
                    if key in ["w", "e"]:
                        _prow["point"] = Point(_prow["height"], self._u.height / 2.0)
                    if key in ["n", "s"]:
                        _prow["point"] = Point(self._u.width / 2.0, _prow["height"])
                if len(data) >= 2:
                    _prow["point"] = Point(self.unit(data[1][0]), self.unit(data[1][1]))
                self.prows_dict[key] = _prow

            self.lines = []
            # print(f'*** {self.prows_dict=}')
            if "w" in self.prows_dict.keys():
                prow = self.prows_dict["w"]
                # top curve
                self.lines.append(
                    [
                        Point(x, y),
                        Point(
                            x - prow["point"].x,
                            y + self._u.height / 2.0 - prow["point"].y,
                        ),
                        Point(x - prow["height"], y + self._u.height / 2.0),
                    ]
                )
                # bottom curve
                self.lines.append(
                    [
                        Point(x - prow["height"], y + self._u.height / 2.0),
                        Point(
                            x - prow["point"].x,
                            y + self._u.height / 2.0 + prow["point"].y,
                        ),
                        Point(x, y + self._u.height),
                    ]
                )
            else:
                self.lines.append([Point(x, y), Point(x, y + self._u.height)])
            if "s" in self.prows_dict.keys():
                prow = self.prows_dict["s"]
                # left-hand curve
                self.lines.append(
                    [
                        Point(x, y + self._u.height),
                        Point(
                            x + self._u.width / 2.0 - prow["point"].x,
                            y + self._u.height + prow["point"].y,
                        ),
                        Point(
                            x + self._u.width / 2.0, y + self._u.height + prow["height"]
                        ),
                    ]
                )
                # right-hand curve
                self.lines.append(
                    [
                        Point(
                            x + self._u.width / 2.0, y + self._u.height + prow["height"]
                        ),
                        Point(
                            x + self._u.width / 2.0 + prow["point"].x,
                            y + self._u.height + prow["point"].y,
                        ),
                        Point(x + self._u.width, y + self._u.height),
                    ]
                )
            else:
                self.lines.append(
                    [
                        Point(x, y + self._u.height),
                        Point(x + self._u.width, y + self._u.height),
                    ]
                )
            if "e" in self.prows_dict.keys():
                prow = self.prows_dict["e"]
                # bottom curve
                self.lines.append(
                    [
                        Point(x + self._u.width, y + self._u.height),
                        Point(
                            x + self._u.width + prow["point"].x,
                            y + self._u.height / 2.0 + prow["point"].y,
                        ),
                        Point(
                            x + self._u.width + prow["height"], y + self._u.height / 2.0
                        ),
                    ]
                )
                # top curve
                self.lines.append(
                    [
                        Point(
                            x + self._u.width + prow["height"], y + self._u.height / 2.0
                        ),
                        Point(
                            x + self._u.width + prow["point"].x,
                            y + self._u.height / 2.0 - prow["point"].y,
                        ),
                        Point(x + self._u.width, y),
                    ]
                )
            else:
                self.lines.append(
                    [
                        Point(x + self._u.width, y + self._u.height),
                        Point(x + self._u.width, y),
                    ]
                )
            if "n" in self.prows_dict.keys():
                prow = self.prows_dict["n"]
                # right-hand curve
                self.lines.append(
                    [
                        Point(x + self._u.width, y),
                        Point(
                            x + self._u.width / 2.0 + prow["point"].x,
                            y - prow["point"].y,
                        ),
                        Point(x + self._u.width / 2.0, y - prow["height"]),
                    ]
                )
                # left-hand curve
                self.lines.append(
                    [
                        Point(x + self._u.width / 2.0, y - prow["height"]),
                        Point(
                            x + self._u.width / 2.0 - prow["point"].x,
                            y - prow["point"].y,
                        ),
                        Point(x, y),
                    ]
                )
            else:
                self.lines.append(
                    [Point(x + self._u.width, y), Point(x, y)]
                )  # line back to start

        # ---- * peaks vertices
        elif is_peaks:
            half_height = self._u.height / 2.0
            half_width = self._u.width / 2.0
            self.vertexes = []
            self.vertexes.append(Point(x, y))  # start here!
            if "w" in self.peaks_dict.keys():
                _pt = self.unit(self.peaks_dict["w"])
                self.vertexes.append(Point(x - _pt, y + half_height))
                self.vertexes.append(Point(x, y + self._u.height))
            else:
                self.vertexes.append(Point(x, y + self._u.height))
            if "s" in self.peaks_dict.keys():
                _pt = self.unit(self.peaks_dict["s"])
                self.vertexes.append(Point(x + half_width, y + self._u.height + _pt))
                self.vertexes.append(Point(x + self._u.width, y + self._u.height))
            else:
                self.vertexes.append(Point(x + self._u.width, y + self._u.height))
            if "e" in self.peaks_dict.keys():
                _pt = self.unit(self.peaks_dict["e"])
                self.vertexes.append(Point(x + +self._u.width + _pt, y + half_height))
                self.vertexes.append(Point(x + self._u.width, y))
            else:
                self.vertexes.append(Point(x + self._u.width, y))
            if "n" in self.peaks_dict.keys():
                _pt = self.unit(self.peaks_dict["n"])
                self.vertexes.append(Point(x + half_width, y - _pt))
            else:
                self.vertexes.append(Point(x, y))  # close() draws line back to start
        # ---- * chevron vertices
        elif is_chevron:
            try:
                _chevron_height = float(self.chevron_height)
            except Exception:
                feedback(
                    f"A chevron_height of {self.chevron_height} is not valid!", True
                )
            if _chevron_height <= 0:
                feedback(
                    "The chevron_height must be greater than zero; "
                    f"not {self.chevron_height}.",
                    True,
                )
            delta_m = self.unit(_chevron_height)
            if not self.chevron:
                self.chevron = "N"
            self.vertexes = []
            if self.chevron.upper() == "S":
                delta_m_down = delta_m
                self.vertexes.append(Point(x, y))
                self.vertexes.append(Point(x, y + self._u.height))
                self.vertexes.append(
                    Point(x + self._u.width / 2.0, y + self._u.height + delta_m)
                )
                self.vertexes.append(Point(x + self._u.width, y + self._u.height))
                self.vertexes.append(Point(x + self._u.width, y))
                self.vertexes.append(Point(x + self._u.width / 2.0, y + delta_m))
            elif self.chevron.upper() == "N":
                delta_m_up = delta_m
                self.vertexes.append(Point(x, y))
                self.vertexes.append(Point(x, y + self._u.height))
                self.vertexes.append(
                    Point(x + self._u.width / 2.0, y + self._u.height - delta_m)
                )
                self.vertexes.append(Point(x + self._u.width, y + self._u.height))
                self.vertexes.append(Point(x + self._u.width, y))
                self.vertexes.append(Point(x + self._u.width / 2.0, y - delta_m))
            elif self.chevron.upper() == "W":
                self.vertexes.append(Point(x, y))
                self.vertexes.append(Point(x - delta_m, y + self._u.height / 2.0))
                self.vertexes.append(Point(x, y + self._u.height))
                self.vertexes.append(Point(x + self._u.width, y + self._u.height))
                self.vertexes.append(
                    Point(x + self._u.width - delta_m, y + self._u.height / 2.0)
                )
                self.vertexes.append(Point(x + self._u.width, y))
            elif self.chevron.upper() == "E":
                self.vertexes.append(Point(x, y))
                self.vertexes.append(Point(x + delta_m, y + self._u.height / 2.0))
                self.vertexes.append(Point(x, y + self._u.height))
                self.vertexes.append(Point(x + self._u.width, y + self._u.height))
                self.vertexes.append(
                    Point(x + self._u.width + delta_m, y + self._u.height / 2.0)
                )
                self.vertexes.append(Point(x + self._u.width, y))
            else:
                self.vertexes = self.get_vertexes(**kwargs)
        else:
            self.vertexes = self.get_vertexes(**kwargs)
        # feedback(f'*** Rect {len(self.vertexes)=}')

        # ---- calculate rounding
        # radius (multiple) – draw rounded rectangle corners. S
        # Specifies the radius of the curvature as percentage of rectangle side length
        # where 0.5 corresponds to 50% of the respective side.
        radius = None
        if self.rounding:
            rounding = self.unit(self.rounding)
            radius = rounding / min(self._u.width, self._u.height)
        if self.rounded:
            radius = self.rounded_radius  # hard-coded OR from defaults
        if radius and radius > 0.5:
            feedback(
                "The rounding radius cannot exceed 50% of the smallest side.", True
            )
        # ---- determine ordering
        base_ordering = [
            "base",
            "pattern",
            "slices",
            "stripes",
            "hatches",
            "perbii",
            "radii",
            "corners",
            "centre_shape",
            "centre_shapes",
            "cross",
            "dot",
            "text",
            "numbering",
        ]
        ordering = base_ordering
        if self.order_all:
            ordering = tools.list_ordering(base_ordering, self.order_all, only=True)
        else:
            if self.order_first:
                ordering = tools.list_ordering(
                    base_ordering, self.order_first, start=True
                )
            if self.order_last:
                ordering = tools.list_ordering(base_ordering, self.order_last, end=True)

        # ---- draw in ORDER
        for item in ordering:
            if item == "base":
                # ---- * draw rectangle
                # feedback(f'*** RECT {self.col=} {self.row=} {x=} {y=} {radius=}')
                if is_notched or is_chevron or is_peaks:
                    # feedback(f'*** RECT  vertices')
                    if _lower(self.notch_style) in ["b", "bite"]:
                        self.draw_bite_rectangle(cnv, x, y)
                    else:
                        cnv.draw_polyline(self.vertexes)
                        kwargs["closed"] = True
                    self.set_canvas_props(cnv=cnv, index=ID, **kwargs)
                    self._debug(cnv, vertices=self.vertexes)
                elif is_prows:
                    for line in self.lines:
                        if len(line) == 2:
                            cnv.draw_line(line[0], line[1])
                        if len(line) == 3:
                            cnv.draw_curve(line[0], line[1], line[2])
                    kwargs["closed"] = True
                    self.set_canvas_props(cnv=cnv, index=ID, **kwargs)
                else:
                    # feedback(f'*** RECT  normal {radius=} {kwargs=}')
                    cnv.draw_rect(
                        (x, y, x + self._u.width, y + self._u.height), radius=radius
                    )
                    self.set_canvas_props(cnv=cnv, index=ID, **kwargs)
                    self._debug(cnv, vertices=self.vertexes)
                    # ---- * borders (override)
                    if self.borders:
                        if isinstance(self.borders, tuple):
                            self.borders = [
                                self.borders,
                            ]
                        if not isinstance(self.borders, list):
                            feedback(
                                'The "borders" property must be a list of sets or a set'
                            )
                        for border in self.borders:
                            self.draw_border(cnv, border, ID)  # BaseShape
            if item == "pattern":
                # ---- * fill pattern?
                if self.fill_pattern:
                    raise NotImplementedError("Fill pattern is not yet supported!")
                    # TODO - convert to PyMuPDF
                    img, is_svg, is_dir = self.load_image(self.fill_pattern)
                    if img:
                        log.debug("IMG %s s%s %s", type(img._image), img._image.size)
                        iwidth = img._image.size[0]
                        iheight = img._image.size[1]
                        # repeat?
                        if self.repeat:
                            cnv.drawImage(
                                img, x=x, y=y, width=iwidth, height=iheight, mask="auto"
                            )
                        else:
                            # stretch
                            cnv.drawImage(
                                img,
                                x=x,
                                y=y,
                                width=self._u.width,
                                height=self._u.height,
                                mask="auto",
                            )
            if item == "slices":
                # ---- * draw slices
                if self.slices:
                    self.draw_slices(cnv, ID, self.vertexes, rotation)
            if item == "stripes":
                # ---- * draw slices
                if self.stripes:
                    self.draw_stripes(cnv, ID, self.vertexes, rotation)
            if item == "hatches":
                # ---- * draw hatches
                if self.hatches_count:
                    # if 'rotation' in kwargs.keys():
                    #     kwargs.pop('rotation')
                    vertices = self.get_vertexes(**kwargs)
                    self.draw_hatches(
                        cnv, ID, vertices, self.hatches_count, rotation=rotation
                    )
            if item == "perbii":
                # ---- * draw perbii
                if self.perbii:
                    self.draw_perbii(cnv, ID, Point(x_d, y_d), **kwargs)
            if item == "radii":
                # ---- * draw radii
                if self.radii:
                    self.draw_radii(cnv, ID, Point(x_d, y_d), self.vertexes)
            if item == "corners":
                # ---- * draw corners
                self.draw_corners(cnv, ID, x, y)
            if item == "centre_shape" or item == "center_shape":
                # ---- * centre shape (with offset)
                if self.centre_shape:
                    if self.can_draw_centred_shape(self.centre_shape):
                        self.centre_shape.draw(
                            _abs_cx=x_d + self.unit(self.centre_shape_mx),
                            _abs_cy=y_d + self.unit(self.centre_shape_my),
                        )
            if item == "centre_shapes" or item == "center_shapes":
                # * ---- centre shapes (with offsets)
                if self.centre_shapes:
                    self.draw_centred_shapes(self.centre_shapes, x_d, y_d)
            if item == "cross":
                # ---- * cross
                self.draw_cross(cnv, x_d, y_d, rotation=kwargs.get("rotation"))
            if item == "dot":
                # ---- * dot
                self.draw_dot(cnv, x_d, y_d)
            if item == "text":
                # ---- * text
                self.draw_heading(
                    cnv, ID, x_d, y_d - 0.5 * self._u.height - delta_m_up, **kwargs
                )
                self.draw_label(cnv, ID, x_d, y_d, **kwargs)
                self.draw_title(
                    cnv, ID, x_d, y_d + 0.5 * self._u.height + delta_m_down, **kwargs
                )
            if item == "numbering":
                # ---- * numbering
                self.set_coord(cnv, x_d, y_d)

        # ---- grid marks
        if self.grid_marks:  # and not kwargs.get("card_back", False):
            deltag = self.unit(self.grid_marks_length)
            gx, gy = 0, y  # left-side
            cnv.draw_line((gx, gy), (deltag, gy))
            cnv.draw_line((0, gy + self._u.height), (deltag, gy + self._u.height))
            gx, gy = x, globals.page[1]  # top-side
            cnv.draw_line((gx, gy), (gx, gy - deltag))
            cnv.draw_line((gx + self._u.width, gy), (gx + self._u.width, gy - deltag))
            gx, gy = globals.page[0], y  # right-side
            cnv.draw_line((gx, gy), (gx - deltag, gy))
            cnv.draw_line((gx, gy + self._u.height), (gx - deltag, gy + self._u.height))
            gx, gy = x, 0  # bottom-side
            cnv.draw_line((gx, gy), (gx, gy + deltag))
            cnv.draw_line((gx + self._u.width, gy), (gx + self._u.width, gy + deltag))
            # done
            gargs = {}
            gargs["stroke"] = self.grid_marks_stroke
            gargs["stroke_width"] = self.grid_marks_stroke_width
            gargs["stroke_ends"] = self.grid_marks_ends
            gargs["dotted"] = self.grid_marks_dotted
            self.set_canvas_props(cnv=None, index=ID, **gargs)
        # ---- set grid property
        self.grid = GridShape(label=self.coord_text, x=x_d, y=y_d, shape=self)
        # ---- debug
        self._debug(cnv, vertices=self.vertexes)
        # ---- set calculated top-left in user units
        self.calculated_left, self.calculated_top = x / self.units, y / self.units
