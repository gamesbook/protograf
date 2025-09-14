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


class HexShape(BaseShape):
    """
    Hexagon on a given canvas.

    See: http://powerfield-software.com/?p=851
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(HexShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        self.kwargs = kwargs
        self.use_diameter = True if self.is_kwarg("diameter") else False
        self.use_height = True if self.is_kwarg("height") else False
        self.use_radius = True if self.is_kwarg("radius") else False
        self.use_side = False
        if "side" in kwargs:
            self.use_side = True
            if "radius" in kwargs or "height" in kwargs or "diameter" in kwargs:
                self.use_side = False
        # fallback / default
        if not self.use_diameter and not self.use_radius and not self.use_side:
            self.use_height = True
        self.ORIENTATION = self.get_orientation()

    def get_orientation(self):
        if _lower(self.orientation) in ["p", "pointy"]:
            orientation = HexOrientation.POINTY
        elif _lower(self.orientation) in ["f", "flat"]:
            orientation = HexOrientation.FLAT
        else:
            feedback(
                'Invalid orientation "{self.orientation}" supplied for hexagon.', True
            )
        return orientation

    def hex_height_width(self) -> tuple:
        """Calculate vertical and horizontal point dimensions of a hexagon

        Returns:
            tuple: radius, diameter, side, half_flat

        Notes:
            * Useful for a row/col layout
            * Units are in points!
        """
        # ---- half_flat, side & half_side
        if self.height and self.use_height:
            side = self._u.height / math.sqrt(3)
            half_flat = self._u.height / 2.0
        elif self.diameter and self.use_diameter:
            side = self._u.diameter / 2.0
            half_flat = side * math.sqrt(3) / 2.0
        elif self.radius and self.use_radius:
            side = self._u.radius
            half_flat = side * math.sqrt(3) / 2.0
        else:
            pass
        if self.side and self.use_side:
            side = self._u.side
            half_flat = side * math.sqrt(3) / 2.0
        if not self.radius and not self.height and not self.diameter and not self.side:
            feedback(
                "No value for side or height or diameter or radius"
                " supplied for hexagon.",
                True,
            )
        # ---- diameter and radius
        diameter = 2.0 * side
        radius = side
        self.ORIENTATION = self.get_orientation()
        if self.ORIENTATION == HexOrientation.POINTY:
            self.width = 2 * half_flat / self.units
            self.height = 2 * radius / self.units
        elif self.ORIENTATION == HexOrientation.FLAT:
            self.height = 2 * half_flat / self.units
            self.width = 2 * radius / self.units
        return radius, diameter, side, half_flat

    def calculate_caltrop_lines(
        self,
        p0: Point,
        p1: Point,
        side: float,
        size: float = None,
        invert: bool = False,
    ) -> Point:
        """Calculate points for caltrops lines (extend from the hex "corner").

        Note: `side` must be in unconverted (user) form e.g. cm or inches

        Returns:
            tuple:
                if not invert; two sets of Point tuples (start/end for the two caltrops)
                if invert; one set of Point tuples (start/end for the mid-caltrops)
        """
        # feedback(f'*** HEX-CC {p0=} {p1=} {size=} {invert=}')
        if invert:
            size = (side - size) / 2
        fraction = size / side
        if fraction > 0.5:
            feedback(f'Cannot use "{fraction}" for a caltrops fraction', True)
        else:
            # first caltrop end pt
            p0a = geoms.fraction_along_line(p0, p1, fraction)
            # second caltrop end pt
            p1a = geoms.fraction_along_line(p1, p0, fraction)
            if not invert:
                return ((p0, p0a), (p1, p1a))
            else:
                return (p0a, p1a)

    def set_coord(self, cnv, x_d, y_d, half_flat):
        """Set and draw the coords of the hexagon."""
        the_row = self.row or 0
        the_col = self.col or 0
        _row = the_row + 1 if not self.coord_start_y else the_row + self.coord_start_y
        _col = the_col + 1 if not self.coord_start_x else the_col + self.coord_start_x
        # ---- set coord label value
        if self.coord_style:
            if _lower(self.coord_style) in ["d", "diagonal"]:
                col_group = (_col - 1) // 2
                _row += col_group
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
            keys = {}
            keys["font_name"] = self.coord_font_name
            keys["font_size"] = self.coord_font_size
            keys["stroke"] = self.coord_stroke
            coord_offset = self.unit(self.coord_offset)
            if self.coord_elevation in ["t", "top"]:
                self.draw_multi_string(
                    cnv,
                    x_d,
                    y_d - half_flat * 0.7 + coord_offset,
                    self.coord_text,
                    **keys,
                )
            elif self.coord_elevation in ["m", "middle", "mid"]:
                self.draw_multi_string(
                    cnv,
                    x_d,
                    y_d + coord_offset + self.coord_font_size / 2.0,
                    self.coord_text,
                    **keys,
                )
            elif self.coord_elevation in ["b", "bottom", "bot"]:
                self.draw_multi_string(
                    cnv,
                    x_d,
                    y_d + half_flat * 0.9 + coord_offset,
                    self.coord_text,
                    **keys,
                )
            else:
                feedback(f'Cannot handle a coord_elevation of "{self.coord_elevation}"')

    def calculate_area(self):
        if self.side:
            side = self._u.side
        elif self.height:
            side = self._u.height / math.sqrt(3)
        return (3.0 * math.sqrt(3.0) * side * side) / 2.0

    def draw_hatches(
        self, cnv, ID, side: float, vertices: list, num: int, rotation: float = 0.0
    ):
        """Draw lines connecting two opposite sides and parallel to adjacent Hex side.

        Args:
            ID: unique ID
            side: length of a Hex side
            vertices: list of Hex'es nodes as Points
            num: number of lines
            rotation: degrees anti-clockwise from horizontal "east"
        """
        dir_group = (
            DirectionGroup.HEX_POINTY
            if self.orientation == "pointy"
            else DirectionGroup.HEX_FLAT
        )
        _dirs = tools.validated_directions(self.hatches, dir_group, "hexagon hatches")
        _num = tools.as_int(num, "hatches_count")
        lines = int((_num - 1) / 2 + 1)
        # feedback(f'*** HEX {num=} {lines=} {vertices=} {_dirs=}')
        if num >= 1:
            if self.orientation in ["p", "pointy"]:
                if "ne" in _dirs or "sw" in _dirs:  # slope UP to the right
                    self.make_path_vertices(cnv, vertices, 1, 4)
                if "se" in _dirs or "nw" in _dirs:  # slope down to the right
                    self.make_path_vertices(cnv, vertices, 0, 3)
                if "n" in _dirs or "s" in _dirs:  # vertical
                    self.make_path_vertices(cnv, vertices, 2, 5)
            if self.orientation in ["f", "flat"]:
                if "ne" in _dirs or "sw" in _dirs:  # slope UP to the right
                    self.make_path_vertices(cnv, vertices, 1, 4)
                if "se" in _dirs or "nw" in _dirs:  # slope down to the right
                    self.make_path_vertices(cnv, vertices, 2, 5)
                if "e" in _dirs or "w" in _dirs:  # horizontal
                    self.make_path_vertices(cnv, vertices, 0, 3)
        if num >= 3:
            _lines = lines - 1
            self.ORIENTATION = self.get_orientation()
            if self.ORIENTATION == HexOrientation.POINTY:
                if "ne" in _dirs or "sw" in _dirs:  # slope UP to the right
                    self.draw_lines_between_sides(
                        cnv, side, _lines, vertices, (4, 5), (1, 0)
                    )
                    self.draw_lines_between_sides(
                        cnv, side, _lines, vertices, (4, 3), (1, 2)
                    )
                if "se" in _dirs or "nw" in _dirs:  # slope down to the right
                    self.draw_lines_between_sides(
                        cnv, side, _lines, vertices, (0, 5), (3, 4)
                    )
                    self.draw_lines_between_sides(
                        cnv, side, _lines, vertices, (3, 2), (0, 1)
                    )
                if "n" in _dirs or "s" in _dirs:  # vertical
                    self.draw_lines_between_sides(
                        cnv, side, _lines, vertices, (1, 2), (0, 5)
                    )
                    self.draw_lines_between_sides(
                        cnv, side, _lines, vertices, (2, 3), (5, 4)
                    )
            elif self.ORIENTATION == HexOrientation.FLAT:
                if "ne" in _dirs or "sw" in _dirs:  # slope UP to the right
                    self.draw_lines_between_sides(
                        cnv, side, _lines, vertices, (0, 1), (5, 4)
                    )
                    self.draw_lines_between_sides(
                        cnv, side, _lines, vertices, (3, 4), (2, 1)
                    )
                if "se" in _dirs or "nw" in _dirs:  # slope down to the right
                    self.draw_lines_between_sides(
                        cnv, side, _lines, vertices, (4, 5), (3, 2)
                    )
                    self.draw_lines_between_sides(
                        cnv, side, _lines, vertices, (2, 1), (5, 0)
                    )
                if "e" in _dirs or "w" in _dirs:  # horizontal
                    self.draw_lines_between_sides(
                        cnv, side, _lines, vertices, (0, 1), (3, 2)
                    )
                    self.draw_lines_between_sides(
                        cnv, side, _lines, vertices, (0, 5), (3, 4)
                    )
        # ---- set canvas
        self.set_canvas_props(
            index=ID,
            stroke=self.hatches_stroke,
            stroke_width=self.hatches_stroke_width,
            stroke_ends=self.hatches_ends,
            dashed=self.hatches_dashed,
            dotted=self.hatches_dots,
        )

    def draw_links(self, cnv, ID, side: float, vertices: list, links: list):
        """Draw arcs or lines to link two sides of a hexagon.

        Args:
            ID: unique ID
            side: length of Hex side
            vertices: list of Hex'es nodes as Points
        """
        self.set_canvas_props(
            index=ID,
            stroke=self.link_stroke,
            stroke_width=self.link_width,
            stroke_ends=self.link_ends,
        )
        _links = links.split(",")
        for _link in _links:
            parts = _link.split()
            try:
                the_link = Link(
                    a=int(parts[0]),
                    b=int(parts[1]),
                    style=parts[2] if len(parts) > 2 else None,
                )
                # feedback(f'*** HEX LINK {the_link=}')
            except TypeError:
                feedback(
                    f"Cannot use {parts[0]} and/or {parts[1]} as hex side numbers.",
                    True,
                )

            va_start = the_link.a - 1
            va_end = the_link.a % 6
            vb_start = the_link.b - 1
            vb_end = the_link.b % 6
            # feedback(f"*** a:{va_start}-{va_end} b:{vb_start}-{vb_end}")

            separation = geoms.separation_between_hexsides(the_link.a, the_link.b)
            match separation:
                case 0:
                    pass  # no line
                case 1:  # adjacent; small arc
                    if va_start in [5, 0] and vb_start in [4, 5]:
                        lower_corner = Point(
                            vertices[vb_end].x - side / 2.0,
                            vertices[vb_end].y - side / 2.0,
                        )
                        top_corner = Point(
                            vertices[vb_end].x + side / 2.0,
                            vertices[vb_end].y + side / 2.0,
                        )
                        cnv.arc(
                            lower_corner.x,
                            lower_corner.y,
                            top_corner.x,
                            top_corner.y,
                            startAng=0,
                            extent=120,
                        )  # anti-clockwise from "east"

                    if va_start in [0, 5] and vb_start in [0, 1]:
                        lower_corner = Point(
                            vertices[vb_end].x - side / 2.0,
                            vertices[vb_end].y - side / 2.0,
                        )
                        top_corner = Point(
                            vertices[vb_end].x + side / 2.0,
                            vertices[vb_end].y + side / 2.0,
                        )
                        cnv.arc(
                            lower_corner.x,
                            lower_corner.y,
                            top_corner.x,
                            top_corner.y,
                            startAng=-60,
                            extent=120,
                        )  # anti-clockwise from "east"

                    # feedback(
                    #     f'arc *** x_1={lower_corner.x}, y_1={lower_corner.y}'
                    #     f' x_2={top_corner.x}, y_2={top_corner.y}')

                case 2:  # non-adjacent; large arc
                    pass
                case 3:  # opposite sides; straight line
                    a_mid = geoms.point_on_line(
                        vertices[va_start], vertices[va_end], side / 2.0
                    )
                    b_mid = geoms.point_on_line(
                        vertices[vb_start], vertices[vb_end], side / 2.0
                    )
                    pth = cnv.beginPath()
                    pth.moveTo(*a_mid)
                    pth.lineTo(*b_mid)
                    cnv.drawPath(pth, stroke=1, fill=1 if self.fill else 0)
                case _:
                    raise NotImplementedError(f'Unable to handle hex "{separation=}"')

    def draw_paths(self, cnv, ID, centre: Point, vertices: list):
        """Draw arc(s) connecting Hexagon edge-to-edge.

        Args:
            ID: unique ID
            vertices: list of Hex'es nodes as Points
            centre: the centre Point of the Hex
        """

        def arc(centre: Point, start: Point, angle: float):
            cnv.draw_sector(centre, start, angle, fullSector=False)

        # validation
        dir_group = (
            DirectionGroup.HEX_POINTY_EDGE
            if self.orientation == "pointy"
            else DirectionGroup.HEX_FLAT_EDGE
        )
        if self.paths is not None and not isinstance(self.paths, list):
            feedback("A Hexagon's paths must be in the form of a list!", True)
        if self.paths == []:
            feedback("A Hexagon's path list cannot be empty!", False, True)

        # --- calculate offset centres
        hex_geom = self.get_geometry()
        side_plus = hex_geom.side * 1.5
        h_flat = hex_geom.half_flat
        self.ORIENTATION = self.get_orientation()
        if self.ORIENTATION == HexOrientation.POINTY:
            #          .
            #    F/ \`A
            #   E|  |B
            #   D\ /C
            #
            ptA = Point(centre.x + h_flat, centre.y - side_plus)
            ptB = Point(centre.x + 2 * h_flat, centre.y)
            ptC = Point(centre.x + h_flat, centre.y + side_plus)
            ptD = Point(centre.x - h_flat, centre.y + side_plus)
            ptE = Point(centre.x - 2 * h_flat, centre.y)
            ptF = Point(centre.x - h_flat, centre.y - side_plus)
        elif self.ORIENTATION == HexOrientation.FLAT:
            #     _A_
            #  .F/  \B
            #   E\__/C
            #     D
            ptA = Point(centre.x, centre.y - hex_geom.height_flat)
            ptB = Point(centre.x + side_plus, centre.y - h_flat)
            ptC = Point(centre.x + side_plus, centre.y + h_flat)
            ptD = Point(centre.x, centre.y + hex_geom.height_flat)
            ptE = Point(centre.x - side_plus, centre.y + h_flat)
            ptF = Point(centre.x - side_plus, centre.y - h_flat)

        # ---- calculate centres of sides
        perbii_dict = self.calculate_perbii(cnv=cnv, centre=centre, vertices=vertices)

        for item in self.paths:
            dir_pair = tools.validated_directions(item, dir_group, "hexagon paths")
            if len(dir_pair) != 2:
                feedback(
                    f"A Hexagon's paths must be in the form of a list of direction pairs!",
                    True,
                )
            # ---- set line styles
            lkwargs = {}
            lkwargs["wave_style"] = self.kwargs.get("paths_wave_style", None)
            lkwargs["wave_height"] = self.kwargs.get("paths_wave_height", 0)
            # ---- draw line/arc
            if self.ORIENTATION == HexOrientation.FLAT:
                match dir_pair:
                    # 120 degrees / short arc
                    case ["n", "ne"] | ["ne", "n"]:
                        arc(vertices[4], perbii_dict["n"].point, 120.0)  # p5
                    case ["se", "ne"] | ["ne", "se"]:
                        arc(vertices[3], perbii_dict["ne"].point, 120.0)  # p4
                    case ["se", "s"] | ["s", "se"]:
                        arc(vertices[2], perbii_dict["se"].point, 120.0)  # p3
                    case ["sw", "s"] | ["s", "sw"]:
                        arc(vertices[1], perbii_dict["s"].point, 120.0)  # p2
                    case ["sw", "nw"] | ["nw", "sw"]:
                        arc(vertices[0], perbii_dict["sw"].point, 120.0)  # p1
                    case ["n", "nw"] | ["nw", "n"]:
                        arc(vertices[5], perbii_dict["nw"].point, 120.0)  # p5
                    # 60 degrees / long arc
                    case ["n", "se"] | ["se", "n"]:
                        arc(ptB, perbii_dict["n"].point, 60.0)  # p5
                    case ["ne", "s"] | ["s", "ne"]:
                        arc(ptC, perbii_dict["ne"].point, 60.0)  # p4
                    case ["se", "sw"] | ["sw", "se"]:
                        arc(ptD, perbii_dict["se"].point, 60.0)  # p3
                    case ["s", "nw"] | ["nw", "s"]:
                        arc(ptE, perbii_dict["s"].point, 60.0)  # p2
                    case ["sw", "n"] | ["n", "sw"]:
                        arc(ptF, perbii_dict["sw"].point, 60.0)  # p1
                    case ["nw", "ne"] | ["ne", "nw"]:
                        arc(ptA, perbii_dict["nw"].point, 60.0)  # p0
                    # 90 degrees
                    case ["nw", "se"] | ["se", "nw"]:
                        klargs = draw_line(
                            cnv,
                            perbii_dict["se"].point,
                            perbii_dict["nw"].point,
                            shape=self,
                            **lkwargs,
                        )
                    case ["ne", "sw"] | ["sw", "ne"]:
                        klargs = draw_line(
                            cnv,
                            perbii_dict["ne"].point,
                            perbii_dict["sw"].point,
                            shape=self,
                            **lkwargs,
                        )
                    case ["n", "s"] | ["s", "n"]:
                        klargs = draw_line(
                            cnv,
                            perbii_dict["n"].point,
                            perbii_dict["s"].point,
                            shape=self,
                            **lkwargs,
                        )
            if self.ORIENTATION == HexOrientation.POINTY:
                match dir_pair:
                    # 120 degrees / short arc
                    case ["e", "ne"] | ["ne", "e"]:
                        arc(vertices[4], perbii_dict["ne"].point, 120.0)  # p5
                    case ["e", "se"] | ["se", "e"]:
                        arc(vertices[3], perbii_dict["e"].point, 120.0)  # p4
                    case ["sw", "se"] | ["se", "sw"]:
                        arc(vertices[2], perbii_dict["se"].point, 120.0)  # p3
                    case ["w", "sw"] | ["sw", "w"]:
                        arc(vertices[1], perbii_dict["sw"].point, 120.0)  # p2
                    case ["w", "nw"] | ["nw", "w"]:
                        arc(vertices[0], perbii_dict["w"].point, 120.0)  # p1
                    case ["nw", "ne"] | ["nw", "ne"]:
                        arc(vertices[5], perbii_dict["nw"].point, 120.0)  # p0
                    # 60 degrees / long arc
                    case ["ne", "se"] | ["se", "ne"]:
                        arc(ptB, perbii_dict["ne"].point, 60.0)  # p5
                    case ["e", "sw"] | ["sw", "e"]:
                        arc(ptC, perbii_dict["e"].point, 60.0)  # p4
                    case ["w", "se"] | ["se", "w"]:
                        arc(ptD, perbii_dict["se"].point, 60.0)  # p3
                    case ["nw", "sw"] | ["sw", "nw"]:
                        arc(ptE, perbii_dict["sw"].point, 60.0)  # p2
                    case ["ne", "w"] | ["w", "ne"]:
                        arc(ptF, perbii_dict["w"].point, 60.0)  # p1
                    case ["e", "nw"] | ["nw", "e"]:
                        arc(ptA, perbii_dict["nw"].point, 60.0)  # p0
                    # 90 degrees
                    case ["ne", "sw"] | ["sw", "ne"]:
                        klargs = draw_line(
                            cnv,
                            perbii_dict["ne"].point,
                            perbii_dict["sw"].point,
                            shape=self,
                            **lkwargs,
                        )
                    case ["e", "w"] | ["w", "e"]:
                        klargs = draw_line(
                            cnv,
                            perbii_dict["e"].point,
                            perbii_dict["w"].point,
                            shape=self,
                            **lkwargs,
                        )
                    case ["nw", "se"] | ["se", "nw"]:
                        klargs = draw_line(
                            cnv,
                            perbii_dict["se"].point,
                            perbii_dict["nw"].point,
                            shape=self,
                            **lkwargs,
                        )
        # ---- set color, thickness etc.
        self.set_canvas_props(
            index=ID,
            fill=None,
            stroke=self.paths_stroke or self.stroke,
            stroke_width=self.paths_stroke_width or self.stroke_width,
            stroke_ends=self.paths_ends,
            dashed=self.paths_dashed,
            dotted=self.paths_dotted,
        )

    def calculate_perbii(
        self, cnv, centre: Point, vertices: list, debug: bool = False
    ) -> list:
        """Calculate centre points for each Hex edge and angles from centre.

        Args:
            vertices: list of Hex'es nodes as Points
            centre: the centre Point of the Hex

        Returns:
            dict of Perbis objects keyed on direction
        """
        if self.ORIENTATION == HexOrientation.POINTY:
            directions = ["nw", "w", "sw", "se", "e", "ne"]
        if self.ORIENTATION == HexOrientation.FLAT:
            directions = ["nw", "sw", "s", "se", "ne", "n"]
        perbii_dict = {}
        vcount = len(vertices) - 1
        _perbii_pts = []
        # print(f"*** HEX perbii {centre=} {vertices=}")
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
            # print(f"*** HEX *** perbii {key=} {pc=} {compass=} {angle=}")
            _perbii = Perbis(
                point=pc,
                direction=directions[key],
                v1=p1,
                v2=p2,
                compass=compass,
                angle=angle,
            )
            perbii_dict[directions[key]] = _perbii
        # if debug:
        #     self.run_debug = True
        #     self._debug(cnv, vertices=_perbii_pts)
        return perbii_dict

    def draw_perbii(
        self, cnv, ID, centre: Point, vertices: list, rotation: float = None
    ):
        """Draw lines connecting the Hexagon centre to the centre of each edge.

        Args:
            ID: unique ID
            vertices: list of Hex'es nodes as Points
            centre: the centre Point of the Hex
            rotation: degrees anti-clockwise from horizontal "east"

        Notes:
            A perpendicular bisector ("perbis") of a chord is:
                A line passing through the center of circle such that it divides
                the chord into two equal parts and meets the chord at a right angle;
                for a polygon, each edge is effectively a chord.
        """
        perbii_dict = self.calculate_perbii(cnv=cnv, centre=centre, vertices=vertices)
        pb_offset = self.unit(self.perbii_offset, label="perbii offset") or 0
        pb_length = (
            self.unit(self.perbii_length, label="perbii length")
            if self.perbii_length
            else self.radius
        )
        if self.perbii:
            dir_group = (
                DirectionGroup.HEX_POINTY_EDGE
                if self.orientation == "pointy"
                else DirectionGroup.HEX_FLAT_EDGE
            )
            perbii_dirs = tools.validated_directions(
                self.perbii, dir_group, "hex perbii"
            )

        # ---- set perbii styles
        lkwargs = {}
        lkwargs["wave_style"] = self.kwargs.get("perbii_wave_style", None)
        lkwargs["wave_height"] = self.kwargs.get("perbii_wave_height", 0)
        for key, a_perbii in perbii_dict.items():
            if self.perbii and key not in perbii_dirs:
                continue
            # points based on length of line, offset and the angle in degrees
            edge_pt = a_perbii.point
            if pb_offset is not None and pb_offset != 0:
                offset_pt = geoms.point_on_circle(centre, pb_offset, a_perbii.angle)
                end_pt = geoms.point_on_line(offset_pt, edge_pt, pb_length)
                # print(f'{pb_angle=} {offset_pt=} {x_c=}, {y_c=}')
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
        """Draw line(s) connecting the Hexagon centre to a vertex.

        Args:
            ID: unique ID
            vertices: list of Hex'es nodes as Points
            centre: the centre Point of the Hex
        """
        # _dirs = _lower(self.radii).split()
        dir_group = (
            DirectionGroup.HEX_POINTY
            if self.orientation == "pointy"
            else DirectionGroup.HEX_FLAT
        )
        _dirs = tools.validated_directions(self.radii, dir_group, "hex radii")
        # ---- set radii styles
        lkwargs = {}
        lkwargs["wave_style"] = self.kwargs.get("radii_wave_style", None)
        lkwargs["wave_height"] = self.kwargs.get("radii_wave_height", 0)
        if "ne" in _dirs:  # slope UP to the right
            draw_line(cnv, centre, vertices[4], shape=self, **lkwargs)
        if "sw" in _dirs:  # slope DOWN to the left
            draw_line(cnv, centre, vertices[1], shape=self, **lkwargs)
        if "se" in _dirs:  # slope DOWN to the right
            if self.orientation in ["p", "pointy"]:
                draw_line(cnv, centre, vertices[3], shape=self, **lkwargs)
            else:
                draw_line(cnv, centre, vertices[2], shape=self, **lkwargs)
        if "nw" in _dirs:  # slope UP to the left
            if self.orientation in ["p", "pointy"]:
                draw_line(cnv, centre, vertices[0], shape=self, **lkwargs)
            else:
                draw_line(cnv, centre, vertices[5], shape=self, **lkwargs)
        if "n" in _dirs and self.orientation in ["p", "pointy"]:  # vertical UP
            draw_line(cnv, centre, vertices[5], shape=self, **lkwargs)
        if "s" in _dirs and self.orientation in ["p", "pointy"]:  # vertical DOWN
            draw_line(cnv, centre, vertices[2], shape=self, **lkwargs)
        if "e" in _dirs and self.orientation in ["f", "flat"]:  # horizontal RIGHT
            draw_line(cnv, centre, vertices[3], shape=self, **lkwargs)
        if "w" in _dirs and self.orientation in ["f", "flat"]:  # horizontal LEFT
            draw_line(cnv, centre, vertices[0], shape=self, **lkwargs)
        # color, thickness etc.
        self.set_canvas_props(
            index=ID,
            stroke=self.radii_stroke or self.stroke,
            stroke_width=self.radii_stroke_width or self.stroke_width,
            stroke_ends=self.radii_ends,
        )

    def draw_slices(self, cnv, ID, centre: Point, vertexes: list, rotation=0):
        """Draw triangles inside the Hexagon

        Args:
            ID: unique ID
            vertexes: list of Hex'es nodes as Points
            centre: the centre Point of the Hex
            rotation: degrees anti-clockwise from horizontal "east"
        """
        # ---- get slices color list from string
        if isinstance(self.slices, str):
            _slices = tools.split(self.slices.strip())
        else:
            _slices = self.slices
        # ---- validate slices color settings
        slices_colors = [
            colrs.get_color(slcolor)
            for slcolor in _slices
            if not isinstance(slcolor, bool)
        ]
        # ---- draw triangle per slice; repeat as needed!
        sid = 0
        nodes = [4, 3, 2, 1, 0, 5]
        if _lower(self.orientation) in ["p", "pointy"]:
            nodes = [5, 4, 3, 2, 1, 0]
        for vid in nodes:
            if sid > len(slices_colors) - 1:
                sid = 0
            vnext = vid - 1 if vid > 0 else 5
            vertexes_slice = [vertexes[vid], centre, vertexes[vnext]]
            cnv.draw_polyline(vertexes_slice)
            self.set_canvas_props(
                index=ID,
                stroke=self.slices_stroke or slices_colors[sid],
                stroke_ends=self.slices_ends,
                fill=slices_colors[sid],
                transparency=self.slices_transparency,
                closed=True,
                rotation=rotation,
                rotation_point=muPoint(centre[0], centre[1]),
            )
            sid += 1
            vid += 1

    def draw_shades(self, cnv, ID, centre: Point, vertexes: list, rotation=0):
        """Draw rhombuses inside the Hexagon

        Args:

            ID: unique ID
            vertexes: list of Hex'es nodes as Points
            centre: the centre Point of the Hex
            rotation: degrees anti-clockwise from horizontal "east"
        """
        # ---- get shades color list from string
        if isinstance(self.shades, str):
            _shades = tools.split(self.shades.strip())
        else:
            _shades = self.shades
        # ---- validate shades color settings
        shades_colors = [
            colrs.get_color(slcolor)
            for slcolor in _shades
            if not isinstance(slcolor, bool)
        ]
        # ---- add shades (if not provided)
        if len(shades_colors) == 1:
            shades_colors = [
                colrs.lighten_pymu(shades_colors[0], factor=0.2),
                colrs.darken_pymu(shades_colors[0], factor=0.2),
                shades_colors[0],
            ]
        elif len(shades_colors) != 3:
            feedback(
                "There must be exactly 1 or 3 shades provided.",
                True,
            )
        # ---- draw a rhombus per shade
        vertexes.append(centre)  # becomes vertex no. 6
        nodes = ([5, 4, 6, 0], [4, 3, 2, 6], [2, 1, 0, 6])
        for sid, rhombus in enumerate(nodes):
            pl_points = [vertexes[vid] for vid in rhombus]
            cnv.draw_polyline(pl_points)
            self.set_canvas_props(
                index=ID,
                stroke=self.shades_stroke or shades_colors[sid],
                fill=shades_colors[sid],
                closed=True,
                rotation=rotation,
                rotation_point=muPoint(centre[0], centre[1]),
            )

    def draw_spikes(
        self, cnv, ID, centre: Point, vertices: list, rotation: float = None
    ):
        """Draw triangles extending from the centre of each edge.

        Args:

            ID: unique ID
            vertices: list of Hex'es nodes as Points
            centre: the centre Point of the Hex
            rotation: degrees anti-clockwise from horizontal "east"
        """
        if not self.spikes:
            return
        dir_group = (
            DirectionGroup.HEX_POINTY_EDGE
            if self.orientation == "pointy"
            else DirectionGroup.HEX_FLAT_EDGE
        )
        spikes_dirs = tools.validated_directions(self.spikes, dir_group, "hex perbii")
        if not spikes_dirs:
            return

        spikes_fill = colrs.get_color(self.spikes_fill)
        geo = self.get_geometry()
        perbii_dict = self.calculate_perbii(
            cnv=cnv, centre=centre, vertices=vertices, debug=True
        )
        spk_length = (
            self.unit(self.spikes_height, label="spikes height")
            if self.spikes_height
            else geo.half_flat
        )
        spk_width = (
            self.unit(self.spikes_width, label="spikes width")
            if self.spikes_width
            else geo.side * 0.1
        )
        # feedback(f"*** HEX {self.spikes=} {self.orientation=} {spikes_dirs=}")

        for key, a_perbii in perbii_dict.items():
            if self.spikes and key not in spikes_dirs:
                continue
            # points based on spike height, width and inverted perbii angle (degrees)
            spk_angle = 360.0 - a_perbii.angle
            edge_pt = a_perbii.point

            if spk_length < 0:
                top_pt = geoms.point_on_circle(
                    centre, geo.half_flat - abs(spk_length), spk_angle
                )
            else:
                # print(f'***HEX{spk_length=} {geo.half_flat=} {spk_width=} {edge_pt=}')
                top_pt = geoms.point_on_circle(
                    centre, spk_length + geo.half_flat, spk_angle
                )
            left_pt = geoms.point_on_line(edge_pt, a_perbii.v1, spk_width / 2.0)
            right_pt = geoms.point_on_line(edge_pt, a_perbii.v2, spk_width / 2.0)
            # print(f"*** HEX {spk_angle=} {top_pt=} {left_pt=}, {right_pt=}")
            cnv.draw_polyline([left_pt, top_pt, right_pt])

        self.set_canvas_props(
            index=ID,
            closed=True,  # for triangle
            stroke=self.spikes_stroke,
            fill=spikes_fill,
            stroke_width=self.spikes_stroke_width,
            stroke_ends=self.spikes_ends,
            dashed=self.spikes_dashed,
            dotted=self.spikes_dotted,
        )

    def get_geometry(self):
        """Calculate geometric settings of a Hexagon."""
        # ---- calculate half_flat & half_side
        if self.height and self.use_height:
            side = self._u.height / math.sqrt(3)
            half_flat = self._u.height / 2.0
        elif self.diameter and self.use_diameter:
            side = self._u.diameter / 2.0
            half_flat = side * math.sqrt(3) / 2.0
        elif self.radius and self.use_radius:
            side = self._u.radius
            half_flat = side * math.sqrt(3) / 2.0
        else:
            pass
        if self.side and self.use_side:
            side = self._u.side
            half_flat = side * math.sqrt(3) / 2.0
        if not self.radius and not self.height and not self.diameter and not self.side:
            feedback(
                "No value for side or height or diameter or radius"
                " supplied for hexagon.",
                True,
            )
        half_side = side / 2.0
        height_flat = 2 * half_flat
        diameter = 2.0 * side
        radius = side
        z_fraction = (diameter - side) / 2.0
        self.ORIENTATION = self.get_orientation()
        return HexGeometry(
            radius, diameter, side, half_side, half_flat, height_flat, z_fraction
        )

    def get_vertexes(self, is_cards=False) -> list:
        """Calculate vertices of the Hexagon.

        Returns:
            list of Hex'es nodes as Points
        """
        geo = self.get_geometry()
        # ---- POINTY^
        self.ORIENTATION = self.get_orientation()
        if self.ORIENTATION == HexOrientation.POINTY:
            #          .
            #         / \`
            # x,y .. |  |
            #        \ /
            #         .
            # x and y are at the bottom-left corner of the box around the hex
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
            # ---- ^ draw pointy by row/col
            if self.row is not None and self.col is not None and is_cards:
                x = (
                    self.col * (geo.height_flat + self._u.spacing_x)
                    + self._o.delta_x
                    + self._u.offset_x
                )
                y = (
                    self.row * (geo.diameter + self._u.spacing_y)
                    + self._o.delta_y
                    + self._u.offset_y
                )  # do NOT add half_flat
            elif self.row is not None and self.col is not None:
                if self.hex_offset in ["o", "O", "odd"]:
                    # TODO => calculate!
                    # downshift applies from first odd row - NOT the very first one!
                    downshift = geo.diameter - geo.z_fraction if self.row >= 1 else 0
                    downshift = downshift * self.row if self.row >= 2 else downshift
                    y = (
                        self.row * (geo.diameter + geo.side)
                        - downshift
                        + self._u.y
                        + self._o.delta_y
                    )
                    if (self.row + 1) & 1:  # is odd row; row are 0-base numbered!
                        x = (
                            self.col * geo.height_flat
                            + geo.half_flat
                            + self._u.x
                            + self._o.delta_x
                        )
                    else:  # even row
                        x = self.col * geo.height_flat + self._u.x + self._o.delta_x
                elif self.hex_offset in ["e", "E", "even"]:  #
                    # downshift applies from first even row - NOT the very first one!
                    downshift = geo.diameter - geo.z_fraction if self.row >= 1 else 0
                    downshift = downshift * self.row if self.row >= 2 else downshift
                    y = (
                        self.row * (geo.diameter + geo.side)
                        - downshift
                        + self._u.y
                        + self._o.delta_y
                    )
                    if (self.row + 1) & 1:  # is odd row; row are 0-base numbered!
                        x = self.col * geo.height_flat + self._u.x + self._o.delta_x
                    else:  # even row
                        x = (
                            self.col * geo.height_flat
                            + geo.half_flat
                            + self._u.x
                            + self._o.delta_x
                        )
                else:
                    feedback(f"Unknown hex_offset value {self.hex_offset}", True)
            # ----  ^ set hex centre relative to x,y
            self.x_d = x + geo.half_flat
            self.y_d = y + geo.side
            # ---- ^ recalculate hex centre
            if self.use_abs_c:
                # create x_d, y_d as the unit-formatted hex centre
                self.x_d = self._abs_cx
                self.y_d = self._abs_cy
                # recalculate start x,y
                x = self.x_d - geo.half_flat
                y = self.y_d - geo.half_side - geo.side / 2.0
            elif self.cx is not None and self.cy is not None:
                # cx,cy are centre; create x_d, y_d as the unit-formatted hex centre
                self.x_d = self._u.cx + self._o.delta_y
                self.y_d = self._u.cy + self._o.delta_x
                # recalculate start x,y
                x = self.x_d - geo.half_flat
                y = self.y_d - geo.half_side - geo.side / 2.0
            # feedback(f"*** P^: {x=} {y=}{self.x_d=} {self.y_d=} {geo=} ")

        # ---- FLAT~
        elif self.ORIENTATION == HexOrientation.FLAT:
            #         __
            # x,y .. /  \
            #        \__/
            #
            # x and y are at the bottom-left corner of the box around the hex
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
            # feedback(f""*** P~: {x=} {y=} {self.row=} {self.col=} {geo=} ")
            # ---- ~ draw flat by row/col
            if self.row is not None and self.col is not None and is_cards:
                # x = self.col * 2.0 * geo.side + self._o.delta_x
                # if self.row & 1:
                #     x = x + geo.side
                # y = self.row * 2.0 * geo.half_flat + self._o.delta_y  # NO half_flat
                x = (
                    self.col * 2.0 * (geo.side + self._u.spacing_x)
                    + self._o.delta_x
                    + self._u.offset_x
                )
                if self.row & 1:
                    x = x + geo.side + self._u.spacing_x
                y = (
                    self.row * 2.0 * (geo.half_flat + self._u.spacing_y)
                    + self._o.delta_y
                    + self._u.offset_y
                )  # do NOT add half_flat
            elif self.row is not None and self.col is not None:
                if self.hex_offset in ["o", "O", "odd"]:
                    x = (
                        self.col * (geo.half_side + geo.side)
                        + self._u.x
                        + self._o.delta_x
                    )
                    y = self.row * geo.half_flat * 2.0 + self._u.y + self._o.delta_y
                    if (self.col + 1) & 1:  # is odd
                        y = y + geo.half_flat
                elif self.hex_offset in ["e", "E", "even"]:
                    x = (
                        self.col * (geo.half_side + geo.side)
                        + self._u.x
                        + self._o.delta_x
                    )
                    y = self.row * geo.half_flat * 2.0 + self._u.y + self._o.delta_y
                    if (self.col + 1) & 1:  # is odd
                        pass
                    else:
                        y = y + geo.half_flat
                else:
                    feedback(f"Unknown hex_offset value {self.hex_offset}", True)

            # ----  ~ set hex centre relative to x,y
            self.x_d = x + geo.side
            self.y_d = y + geo.half_flat
            # ----  ~ recalculate centre if preset
            if self.use_abs_c:
                # create x_d, y_d as the unit-formatted hex centre
                self.x_d = self._abs_cx
                self.y_d = self._abs_cy
                # recalculate start x,y
                x = self.x_d - geo.half_side - geo.side / 2.0
                y = self.y_d - geo.half_flat
            elif self.cx is not None and self.cy is not None:
                # cx,cy are centre; create x_d, y_d as the unit-formatted hex centre
                self.x_d = self._u.cx + self._o.delta_x
                self.y_d = self._u.cy + self._o.delta_y
                # recalculate start x,y
                x = self.x_d - geo.half_side - geo.side / 2.0
                y = self.y_d - geo.half_flat
            # feedback(f"*** F~: {x=} {y=} {self.x_d=} {self.y_d=} {geo=}")

        # ---- ^ pointy hexagon vertices (clockwise)
        if self.ORIENTATION == HexOrientation.POINTY:
            self.vertexes = [  # clockwise from bottom-left; relative to centre
                muPoint(x, y + geo.z_fraction),
                muPoint(x, y + geo.z_fraction + geo.side),
                muPoint(x + geo.half_flat, y + geo.diameter),
                muPoint(x + geo.height_flat, y + geo.z_fraction + geo.side),
                muPoint(x + geo.height_flat, y + geo.z_fraction),
                muPoint(x + geo.half_flat, y),
            ]
        # ---- ~ flat hexagon vertices (clockwise)
        elif self.ORIENTATION == HexOrientation.FLAT:
            self.vertexes = [  # clockwise from left; relative to centre
                muPoint(x, y + geo.half_flat),
                muPoint(x + geo.z_fraction, y + geo.height_flat),
                muPoint(x + geo.z_fraction + geo.side, y + geo.height_flat),
                muPoint(x + geo.diameter, y + geo.half_flat),
                muPoint(x + geo.z_fraction + geo.side, y),
                muPoint(x + geo.z_fraction, y),
            ]
        return self.vertexes

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a hexagon on a given canvas."""
        kwargs = self.kwargs | kwargs
        # feedback(f'*** draw hex: {off_x=} {off_y=} {ID=}')
        # feedback(f'*** draw hex: {self.x=} {self.y=} {self.cx=} {self.cy=}')
        # feedback(f'*** draw hex: {self.row=} {self.col=}')
        # feedback(f' @@@ Hexg.draw {kwargs=}')
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- calculate vertexes
        geo = self.get_geometry()
        is_cards = kwargs.get("is_cards", False)
        self.get_vertexes(is_cards)
        # ---- calculate area
        self.area = self.calculate_area()
        # ---- remove rotation
        if kwargs and kwargs.get("rotation"):
            kwargs.pop("rotation")
        # ---- calculate offset
        if _lower(self.orientation) in ["p", "pointy"]:
            offset = geo.side  # == radius
        else:
            offset = geo.half_flat
        # feedback(f'***Hex {x=} {y=} {self.vertexes=} {self.kwargs=')

        # ---- determine ordering
        base_ordering = [
            "base",
            "borders",
            "shades",
            "slices",
            "spikes",
            "hatches",
            "links",
            "perbii",
            "paths",
            "radii",
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
        # feedback(f'*** Hexagon: {ordering=}')

        # ---- draw in ORDER
        for item in ordering:
            if item == "base":
                # ---- * hexagon with caltrops
                if self.caltrops:
                    # draw fill
                    _stroke = kwargs.get("stroke", self.stroke)
                    if self.fill:
                        cnv.draw_polyline(self.vertexes)
                        kwargs["stroke"] = None
                        kwargs["closed"] = True
                        self.set_canvas_props(cnv=cnv, index=ID, **kwargs)
                    # draw lines
                    kwargs["stroke"] = _stroke
                    self.vertexes.append(self.vertexes[0])
                    for key, vertex0 in enumerate(self.vertexes):
                        if key + 1 != len(self.vertexes):
                            vertex1 = self.vertexes[key + 1]
                            caltrop_points = self.calculate_caltrop_lines(
                                vertex0,
                                vertex1,
                                self.side,
                                self.caltrops,
                                self.caltrops_invert,
                            )
                            if self.caltrops_invert:
                                cnv.draw_line(caltrop_points[0], caltrop_points[1])
                            else:
                                for caltrop_point in caltrop_points:
                                    cnv.draw_line(caltrop_point[0], caltrop_point[1])
                    self.set_canvas_props(cnv=cnv, index=ID, **kwargs)
                # ---- * normal hexagon
                else:
                    kwargs["fill"] = kwargs.get("fill", self.fill)
                    kwargs["stroke"] = kwargs.get("stroke", self.stroke)
                    kwargs["stroke_ends"] = kwargs.get("stroke_ends", self.stroke_ends)
                    if self.draw_polyline_props(cnv, self.vertexes, **kwargs):
                        kwargs["closed"] = True
                        self.set_canvas_props(cnv=cnv, index=ID, **kwargs)
            if item == "borders":
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
            if item == "shades":
                # ---- * draw shades
                if self.shades:
                    self.draw_shades(
                        cnv,
                        ID,
                        Point(self.x_d, self.y_d),
                        self.vertexes,
                        rotation=kwargs.get("rotation"),
                    )
            if item == "slices":
                # ---- * draw slices
                if self.slices:
                    self.draw_slices(
                        cnv,
                        ID,
                        Point(self.x_d, self.y_d),
                        self.vertexes,
                        rotation=kwargs.get("rotation"),
                    )
            if item == "spikes":
                # ---- * draw spikes
                if self.spikes:
                    self.draw_spikes(
                        cnv,
                        ID,
                        Point(self.x_d, self.y_d),
                        self.vertexes,
                        rotation=kwargs.get("rotation"),
                    )
            if item == "hatches":
                # ---- * draw hatches
                if self.hatches_count:
                    if not self.hatches_count & 1:
                        feedback(
                            "hatches count must be an odd number for a Hexagon", True
                        )
                    self.draw_hatches(
                        cnv, ID, geo.side, self.vertexes, self.hatches_count
                    )
            if item == "links":
                # ---- * draw links
                if self.links:
                    self.draw_links(cnv, ID, geo.side, self.vertexes, self.links)
            if item == "radii":
                # ---- * draw radii
                if self.radii:
                    self.draw_radii(cnv, ID, Point(self.x_d, self.y_d), self.vertexes)
            if item == "perbii":
                # ---- * draw perbii
                if self.perbii:
                    self.draw_perbii(cnv, ID, Point(self.x_d, self.y_d), self.vertexes)
            if item == "paths":
                # ---- * draw paths
                if self.paths is not None and self.paths != []:
                    self.draw_paths(cnv, ID, Point(self.x_d, self.y_d), self.vertexes)
            if item == "centre_shape" or item == "center_shape":
                # ---- * centred shape (with offset)
                if self.centre_shape:
                    if self.can_draw_centred_shape(self.centre_shape):
                        self.centre_shape.draw(
                            _abs_cx=self.x_d + self.unit(self.centre_shape_mx),
                            _abs_cy=self.y_d + self.unit(self.centre_shape_my),
                        )
            if item == "centre_shapes" or item == "center_shapes":
                # ---- * centred shapes (with offsets)
                if self.centre_shapes:
                    self.draw_centred_shapes(self.centre_shapes, self.x_d, self.y_d)
            if item == "cross":
                # ---- * cross
                self.draw_cross(
                    cnv, self.x_d, self.y_d, rotation=kwargs.get("rotation")
                )
            if item == "dot":
                # ---- * dot
                self.draw_dot(cnv, self.x_d, self.y_d)
            if item == "text":
                # ---- * text
                self.draw_heading(cnv, ID, self.x_d, self.y_d - offset, **kwargs)
                self.draw_label(cnv, ID, self.x_d, self.y_d, **kwargs)
                self.draw_title(cnv, ID, self.x_d, self.y_d + offset, **kwargs)
            if item == "numbering":
                # ---- * numbering
                self.set_coord(cnv, self.x_d, self.y_d, geo.half_flat)
                # ---- * set grid property
                self.grid = GridShape(
                    label=self.coord_text, x=self.x_d, y=self.y_d, shape=self
                )

        # ---- debug
        # self._debug(cnv, Point(x, y), 'start')
        # self._debug(cnv, Point(self.x_d, self.y_d), 'centre')
        self._debug(cnv, vertices=self.vertexes)
        # ---- set calculated top-left in user units
        self.calculated_left = (self.x_d - offset) / self.units
        self.calculated_top = (self.y_d - offset) / self.units
