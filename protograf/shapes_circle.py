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


class CircleShape(BaseShape):
    """
    Circle on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(CircleShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        self.kwargs = kwargs
        # ---- perform overrides
        self.radius = self.radius or self.diameter / 2.0
        if self.cx is not None and self.cy is not None:
            self.x = self.cx - self.radius
            self.y = self.cy - self.radius
        else:
            self.cx = self.x + self.radius
            self.cy = self.y + self.radius
        self.width = 2.0 * self.radius
        self.height = 2.0 * self.radius
        self.bbox = None
        # ---- RESET UNIT PROPS (last!)
        self.set_unit_properties()

    def calculate_centre(self) -> Point:
        """Calculate centre of Circle."""
        if self.use_abs_c:
            self.x_c = self._abs_cx
            self.y_c = self._abs_cy
        else:
            self.x_c = self._u.cx + self._o.delta_x
            self.y_c = self._u.cy + self._o.delta_y
        return Point(self.x_c, self.y_c)

    def calculate_area(self) -> float:
        """Calculate area of Circle."""
        return math.pi * self._u.radius * self._u.radius

    def calculate_perimeter(self, units: bool = False) -> float:
        """Calculate length of circumference of Circle"""
        length = math.pi * 2.0 * self._u.radius
        if units:
            return self.points_to_value(length)
        else:
            return length

    def draw_hatches(
        self, cnv, ID, num: int, x_c: float, y_c: float, rotation: float = 0.0
    ):
        """Draw parallel line(s) across the Circle

        Args:
            num: number of lines
            x_c: x-centre of circle
            y_c: y-centre of circle
            rotation: degrees anti-clockwise from horizontal "east"
        """
        _dirs = tools.validated_directions(
            self.hatches, DirectionGroup.CIRCULAR, "circle hatches"
        )
        lines = tools.as_int(num, "hatches_count")
        if lines < 0:
            feedback("Cannot draw negative number of lines!", True)
        dist = (self._u.radius * 2.0) / (lines + 1)
        partial = lines // 2

        # calculate relative distances for each line - (x, y) tuples
        vertical_distances, horizontal_distances = [], []
        for line_no in range(1, partial + 1):
            if lines & 1:
                dist_h = dist * line_no
            else:
                dist_h = dist * 0.5 if line_no == 1 else dist * line_no - dist * 0.5
            dist_v = math.sqrt(self._u.radius * self._u.radius - dist_h * dist_h)
            vertical_distances.append((dist_h, dist_v))
            horizontal_distances.append((dist_v, dist_h))

        if num >= 1 and lines & 1:  # is odd - draw centre lines
            if "e" in _dirs or "w" in _dirs or "o" in _dirs:  # horizontal
                cnv.draw_line(
                    Point(x_c + self._u.radius, y_c),
                    Point(x_c - self._u.radius, y_c),
                )
            if "n" in _dirs or "s" in _dirs or "o" in _dirs:  # vertical
                cnv.draw_line(
                    Point(x_c, y_c + self._u.radius),
                    Point(x_c, y_c - self._u.radius),
                )
            if "se" in _dirs or "nw" in _dirs or "d" in _dirs:  # diagonal  "down"
                poc_top_d = geoms.point_on_circle(Point(x_c, y_c), self._u.radius, 135)
                poc_btm_d = geoms.point_on_circle(Point(x_c, y_c), self._u.radius, 315)
                cnv.draw_line(poc_top_d, poc_btm_d)
            if "ne" in _dirs or "sw" in _dirs or "d" in _dirs:  # diagonal  "up"
                poc_top_u = geoms.point_on_circle(Point(x_c, y_c), self._u.radius, 45)
                poc_btm_u = geoms.point_on_circle(Point(x_c, y_c), self._u.radius, 225)
                cnv.draw_line(poc_top_u, poc_btm_u)

        if num <= 1:
            return

        if "e" in _dirs or "w" in _dirs or "o" in _dirs:  # horizontal
            for dist in horizontal_distances:
                cnv.draw_line(  # "above" diameter
                    Point(x_c - dist[0], y_c + dist[1]),
                    Point(x_c + dist[0], y_c + dist[1]),
                )
                cnv.draw_line(  # "below" diameter
                    Point(x_c - dist[0], y_c - dist[1]),
                    Point(x_c + dist[0], y_c - dist[1]),
                )

        if "n" in _dirs or "s" in _dirs or "o" in _dirs:  # vertical
            for dist in vertical_distances:
                cnv.draw_line(  # "right" of diameter
                    Point(x_c + dist[0], y_c + dist[1]),
                    Point(x_c + dist[0], y_c - dist[1]),
                )
                cnv.draw_line(  # "left" of diameter
                    Point(x_c - dist[0], y_c + dist[1]),
                    Point(x_c - dist[0], y_c - dist[1]),
                )

        if "se" in _dirs or "nw" in _dirs or "d" in _dirs:  # diagonal  "down"
            for dist in horizontal_distances:
                _angle = math.degrees(math.asin(dist[0] / self._u.radius))
                # "above right" of diameter
                dal = geoms.point_on_circle(
                    Point(x_c, y_c), self._u.radius, 45.0 + _angle
                )
                dar = geoms.point_on_circle(
                    Point(x_c, y_c), self._u.radius, 45.0 - _angle
                )  # + 45.)
                cnv.draw_line(dar, dal)
                # "below left" of diameter
                dbl = geoms.point_on_circle(
                    Point(x_c, y_c), self._u.radius, 225.0 - _angle
                )
                dbr = geoms.point_on_circle(
                    Point(x_c, y_c), self._u.radius, 225.0 + _angle
                )
                cnv.draw_line(dbr, dbl)
                # TEST cnv.circle(dal.x, dal.y, 2, stroke=1, fill=1 if self.fill else 0)

        if "ne" in _dirs or "sw" in _dirs or "d" in _dirs:  # diagonal  "up"
            for dist in vertical_distances:
                _angle = math.degrees(math.asin(dist[0] / self._u.radius))
                # "above left" of diameter
                poc_top = geoms.point_on_circle(
                    Point(x_c, y_c), self._u.radius, _angle + 45.0
                )
                poc_btm = geoms.point_on_circle(
                    Point(x_c, y_c), self._u.radius, 180.0 - _angle + 45.0
                )
                cnv.draw_line(poc_top, poc_btm)
                # "below right" of diameter
                poc_top = geoms.point_on_circle(
                    Point(x_c, y_c), self._u.radius, 45 - _angle
                )
                poc_btm = geoms.point_on_circle(
                    Point(x_c, y_c), self._u.radius, 180.0 + _angle + 45.0
                )
                cnv.draw_line(poc_top, poc_btm)

        # ---- set canvas
        self.set_canvas_props(
            index=ID,
            stroke=self.hatches_stroke,
            stroke_width=self.hatches_stroke_width,
            stroke_ends=self.hatches_ends,
            dashed=self.hatches_dashed,
            dotted=self.hatches_dots,
            rotation=rotation,
            rotation_point=muPoint(x_c, y_c),
        )

    def draw_nested(self, cnv, ID, x_c: float, y_c: float, **kwargs):
        """Draw concentric circles from the circumference inwards."""
        if self.nested:
            intervals = []
            if isinstance(self.nested, int):
                if self.nested <= 0:
                    feedback("The nested value must be greater than zero!", True)
                interval_size = 1.0 / (self.nested + 1.0)
                for item in range(1, self.nested + 1):
                    intervals.append(interval_size * item)
            elif isinstance(self.nested, list):
                intervals = [
                    tools.as_float(item, "a nested fraction") for item in self.nested
                ]
                for inter in intervals:
                    if inter < 0 or inter >= 1:
                        feedback("The nested list values must be fractions!", True)
            else:
                feedback(
                    "The nested value must either be a whole number"
                    " or a list of fractions.",
                    True,
                )
            if intervals:
                intervals.sort(reverse=True)
                # print(f'*** nested {intervals=}')
                for inter in intervals:
                    cnv.draw_circle((x_c, y_c), self._u.radius * inter)
                    self.set_canvas_props(cnv=cnv, index=ID, **kwargs)

    def draw_radii(self, cnv, ID, x_c: float, y_c: float):
        """Draw radius lines from the centre outwards to the circumference.

        The offset will start the line a certain distance away; and the length will
        determine how long the radial line is.  By default it stretches from centre
        to circumference.

        Args:
            x_c: x-centre of circle
            y_c: y-centre of circle
        """
        if self.radii:
            try:
                _radii = [
                    float(angle) for angle in self.radii if angle >= 0 and angle <= 360
                ]
            except Exception:
                feedback(
                    f"The radii {self.radii} are not valid - must be a list of numbers"
                    " from 0 to 360",
                    True,
                )
            if self.radii_length and self.radii_offset:
                outer_radius = self.radii_length + self.radii_offset
            elif self.radii_length:
                outer_radius = self.radii_length
            else:
                outer_radius = self.radius
            radius_offset = self.unit(self.radii_offset) or None
            radius_length = self.unit(outer_radius, label="radius length")
            # print(f'*** {radius_length=} :: {radius_offset=} :: {outer_radius=}')
            _radii_labels = [self.radii_labels]
            if self.radii_labels:
                if isinstance(self.radii_labels, list):
                    _radii_labels = self.radii_labels
                else:
                    _radii_labels = tools.split(self.radii_labels)
            _radii_strokes = [self.radii_stroke]  # could be color tuple (or str?)
            if self.radii_stroke:
                if isinstance(self.radii_stroke, list):
                    _radii_strokes = self.radii_stroke
                else:
                    _radii_strokes = tools.split(self.radii_stroke, tuple_to_list=True)
            # print(f'*** {_radii_labels=} {_radii_strokes=}')
            label_key, stroke_key = 0, 0
            label_points = []

            # ---- set radii styles
            lkwargs = {}
            lkwargs["wave_style"] = self.kwargs.get("radii_wave_style", None)
            lkwargs["wave_height"] = self.kwargs.get("radii_wave_height", 0)
            for key, rad_angle in enumerate(_radii):
                # points based on length of line, offset and the angle in degrees
                diam_pt = geoms.point_on_circle(
                    Point(x_c, y_c), radius_length, rad_angle
                )
                if radius_offset is not None and radius_offset != 0:
                    # print(f'***{rad_angle=} {radius_offset=} {diam_pt} {x_c=} {y_c=}')
                    offset_pt = geoms.point_on_circle(
                        Point(x_c, y_c), radius_offset, rad_angle
                    )
                    end_pt = geoms.point_on_circle(
                        Point(x_c, y_c), radius_length, rad_angle
                    )
                    x_start, y_start = offset_pt.x, offset_pt.y
                    x_end, y_end = end_pt.x, end_pt.y
                else:
                    x_start, y_start = x_c, y_c
                    x_end, y_end = diam_pt.x, diam_pt.y
                # ---- track label points
                label_points.append(
                    (Point((x_start + x_end) / 2.0, (y_start + y_end) / 2.0), rad_angle)
                )
                # ---- draw a radii line
                draw_line(
                    cnv, (x_start, y_start), (x_end, y_end), shape=self, **lkwargs
                )
                # ---- style radii line
                _radii_stroke = _radii_strokes[stroke_key]
                self.set_canvas_props(
                    index=ID,
                    stroke=_radii_stroke,
                    stroke_width=self.radii_stroke_width,
                    stroke_ends=self.radii_ends,
                    dashed=self.radii_dashed,
                    dotted=self.radii_dotted,
                )
                stroke_key += 1
                if stroke_key > len(_radii_strokes) - 1:
                    stroke_key = 0
            # ---- draw radii text labels
            if self.radii_labels:
                for label_point in label_points:
                    self.radii_label = _radii_labels[label_key]
                    # print(f'*** {label_point[1]=}  {self.radii_labels_rotation=}')
                    self.draw_radii_label(
                        cnv,
                        ID,
                        label_point[0].x,
                        label_point[0].y,
                        rotation=label_point[1] + self.radii_labels_rotation,
                        centred=False,
                    )
                    label_key += 1
                    if label_key > len(_radii_labels) - 1:
                        label_key = 0

    def draw_petals(self, cnv, ID, x_c: float, y_c: float):
        """Draw "petals" going outwards from the circumference.

        The offset will start the petals a certain distance away; and the height
        will determine the size of their peaks. Odd number of petals will have
        the first one's point aligned with north direction; an even number will
        have the "valley" aligned with the northern most point of the circle.

        Args:
            x_c: x-centre of circle
            y_c: y-centre of circle
        """
        if self.petals:
            center = Point(x_c, y_c)
            gap = 360.0 / self.petals
            shift = gap / 2.0 if self.petals & 1 else 0
            offset = self.unit(self.petals_offset, label="petals offset")
            height = self.unit(self.petals_height, label="petals height")
            petals_vertices = []
            # ---- calculate points
            angles = support.steps(90 - shift, 450 - shift, gap)
            # print(f' ^ {self.petals=} {angles=}')
            for index, angle in enumerate(angles):
                angle = angle - 360.0 if angle > 360.0 else angle
                petals_style = _lower(self.petals_style)
                if petals_style not in ["triangle", "t"]:
                    if len(angles) < self.petals + 1:
                        angles.append(angles[-1] + gap)
                match petals_style:
                    case "triangle" | "t":
                        petals_vertices.append(
                            geoms.point_on_circle(
                                center,
                                self._u.radius + offset + height,
                                angle - gap / 2.0,
                            )
                        )
                        petals_vertices.append(
                            geoms.point_on_circle(
                                center, self._u.radius + offset, angle
                            )
                        )

                    case "petal" | "p":
                        pt1 = geoms.point_on_circle(
                            center,
                            self._u.radius + offset,
                            angle - gap / 2.0,
                        )
                        pt2 = geoms.point_on_circle(
                            center, self._u.radius + offset + height, angle
                        )
                        pt3 = geoms.point_on_circle(
                            center,
                            self._u.radius + offset,
                            angle + gap / 2.0,
                        )
                        petals_vertices.append((pt1, pt2, pt3))

                    case _:
                        feedback(f'Unknown petals_style "{self.petals_style}"', True)

            # ---- draw and fill
            match self.petals_style:
                case "triangle" | "t":
                    petals_vertices.append(petals_vertices[0])
                    for key, vertex in enumerate(petals_vertices):
                        if key == len(petals_vertices) - 1:
                            continue
                        cnv.draw_line(
                            (vertex.x, vertex.y),
                            (petals_vertices[key + 1].x, petals_vertices[key + 1].y),
                        )
                case "petal" | "p":
                    for key, vertex in enumerate(petals_vertices):
                        # if key == 0:
                        #     continue  # already have a "start" location on path
                        cnv.draw_curve(  # was curveTo
                            (vertex[0].x, vertex[0].y),
                            (vertex[1].x, vertex[1].y),
                            (vertex[2].x, vertex[2].y),
                        )
                case _:
                    feedback(f'Unknown petals_style "{self.petals_style}"', True)

            self.set_canvas_props(
                index=ID,
                fill=self.petals_fill,
                stroke=self.petals_stroke,
                stroke_width=self.petals_stroke_width,
                stroke_ends=self.petals_ends,
                dashed=self.petals_dashed,
                dotted=self.petals_dotted,
            )

            # ---- draw 'fill' circles
            cnv.draw_circle(center, self._u.radius + offset)
            _color = self.petals_fill or self.fill
            self.set_canvas_props(
                index=ID,
                fill=_color,
                stroke=_color,
                stroke_width=0.001,
                dashed=None,
                dotted=None,
            )

    def draw_slices(
        self, cnv, ID: int, centre: Point, radius: float, rotation: float = 0
    ):
        """Draw pie-shaped slices inside the Circle

        Args:
            ID: unique ID
            centre: Point at centre of circle
            radius: length of circle's radius
            rotation: degrees anti-clockwise from horizontal "east"

        """
        # ---- get slices color list from string
        if isinstance(self.slices, str):
            _slices = tools.split(self.slices.strip())
        else:
            _slices = self.slices
        # ---- validate slices color settings
        if not isinstance(_slices, list):
            feedback("Slices must be a list of colors", True)
        # ---- get slices fractions list from string
        if isinstance(self.slices_fractions, str):
            _slices_frac = tools.split(self.slices_fractions.strip())
        else:
            _slices_frac = self.slices_fractions or [1] * len(_slices)
        # ---- validate slices fractions values
        for _frac in _slices_frac:
            _frac = _frac or 1
            if not isinstance(_frac, (float, int)):
                feedback("The slices_fractions must be a list of values.", True)
        if len(_slices_frac) != len(_slices):
            feedback(
                "The number of slices_fractions must match number of colors.", True
            )
        # ---- get slices_angles list from string
        if isinstance(self.slices_angles, str):
            _slices_ang = tools.split(self.slices_angles.strip())
        else:  # degrees "size" of slice
            _slices_ang = self.slices_angles or [360.0 / len(_slices)] * len(_slices)
        # ---- validate slices anfle values
        for _frac in _slices_ang:
            _frac = _frac or 0
            if not isinstance(_frac, (float, int)):
                feedback("The slices_angles must be a list of values.", True)
        if len(_slices_ang) != len(_slices):
            feedback("The number of slices_angles must match number of colors.", True)
        if sum(_slices_ang) > 360.0:
            feedback("The sum of the slices_angles cannot exceed 360 (degrees).", True)
        slices_colors = [colrs.get_color(slcolor) for slcolor in _slices]
        # ---- draw sectors
        angle = 0.0 + rotation
        for idx, _color in enumerate(slices_colors):
            radius_frac = radius * (_slices_frac[idx] or 1)
            slice_angle = _slices_ang[idx]
            start = geoms.point_on_circle(centre, radius_frac, angle)
            if _color:
                cnv.draw_sector(centre, start, slice_angle, fullSector=True)
                self.set_canvas_props(
                    index=ID,
                    fill=_color,
                    transparency=self.slices_transparency,
                    stroke=_color,
                    stroke_width=0.001,
                    dashed=None,
                    dotted=None,
                )
            angle += slice_angle

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw circle on a given canvas."""
        kwargs = self.kwargs | kwargs
        _ = kwargs.pop("ID", None)
        # feedback(f' @@@ Circ.draw {kwargs=}')
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        is_cards = kwargs.get("is_cards", False)
        # ---- set centre & area
        ccentre = self.calculate_centre()  # self.x_c, self.y_c
        x, y = ccentre.x, ccentre.y
        self.area = self.calculate_area()
        # ---- draw by row/col
        if self.row is not None and self.col is not None and is_cards:
            if self.kwargs.get("grouping_cols", 1) == 1:
                x = (
                    self.col * (self._u.radius * 2.0 + self._u.spacing_x)
                    + self._o.delta_x
                    + self._u.radius
                    + self._u.offset_x
                )
            else:
                group_no = self.col // self.kwargs["grouping_cols"]
                x = (
                    self.col * self._u.radius * 2.0
                    + self._u.spacing_x * group_no
                    + self._o.delta_x
                    + self._u.radius
                    + self._u.offset_x
                )
            if self.kwargs.get("grouping_rows", 1) == 1:
                y = (
                    self.row * (self._u.radius * 2.0 + self._u.spacing_y)
                    + self._o.delta_y
                    + self._u.radius
                    + self._u.offset_y
                )
            else:
                group_no = self.row // self.kwargs["grouping_rows"]
                y = (
                    self.row * self._u.radius * 2.0
                    + self._u.spacing_y * group_no
                    + self._o.delta_y
                    + self._u.radius
                    + self._u.offset_y
                )
            self.x_c, self.y_c = x, y
            self.bbox = BBox(
                tl=Point(self.x_c - self._u.radius, self.y_c - self._u.radius),
                br=Point(self.x_c + self._u.radius, self.y_c + self._u.radius),
            )
        # ---- handle rotation
        rotation = kwargs.get("rotation", self.rotation)
        if rotation:
            self.centroid = muPoint(x, y)
            kwargs["rotation"] = tools.as_float(rotation, "rotation")
            kwargs["rotation_point"] = self.centroid
        else:
            kwargs["rotation"] = 0
        # feedback(f'*** Circle: {x=} {y=}')
        # ---- determine ordering
        base_ordering = [
            "petals",
            "base",
            "nested",
            "slices",
            "hatches",
            "radii",
            "centre_shape",
            "centre_shapes",
            "cross",
            "dot",
            "text",
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
        # feedback(f'*** Circle: {ordering=}')

        # ---- draw in ORDER
        for item in ordering:
            if item == "petals":
                # ---- * draw petals
                if self.petals:
                    self.draw_petals(cnv, ID, self.x_c, self.y_c)
            if item == "base":
                # ---- * draw circle
                cnv.draw_circle((x, y), self._u.radius)
                self.set_canvas_props(cnv=cnv, index=ID, **kwargs)
            if item == "nested":
                # ---- * draw nested
                if self.nested:
                    self.draw_nested(cnv, ID, x, y, **kwargs)
            if item == "slices":
                # ---- * draw slices
                if self.slices:
                    self.draw_slices(
                        cnv,
                        ID,
                        Point(self.x_c, self.y_c),
                        self._u.radius,
                        rotation=kwargs["rotation"],
                    )
            if item == "hatches":
                # ---- * draw hatches
                if self.hatches_count:
                    self.draw_hatches(
                        cnv,
                        ID,
                        self.hatches_count,
                        self.x_c,
                        self.y_c,
                        rotation=kwargs["rotation"],
                    )
            if item == "radii":
                # ---- * draw radii
                if self.radii:
                    self.draw_radii(cnv, ID, self.x_c, self.y_c)
            if item == "centre_shape" or item == "center_shape":
                # ---- * centre shape (with offset)
                if self.centre_shape:
                    if self.can_draw_centred_shape(self.centre_shape):
                        self.centre_shape.draw(
                            _abs_cx=x + self.unit(self.centre_shape_mx),
                            _abs_cy=y + self.unit(self.centre_shape_my),
                        )
            if item == "centre_shapes" or item == "center_shapes":
                # ---- * centre shapes (with offsets)
                if self.centre_shapes:
                    self.draw_centred_shapes(self.centre_shapes, x, y)
            if item == "cross":
                # ---- * cross
                self.draw_cross(
                    cnv, self.x_c, self.y_c, rotation=kwargs.get("rotation")
                )
            if item == "dot":
                # ---- * dot
                self.draw_dot(cnv, self.x_c, self.y_c)
            if item == "text":
                # ---- * text
                self.draw_heading(
                    cnv, ID, self.x_c, self.y_c - self._u.radius, **kwargs
                )
                self.draw_label(cnv, ID, self.x_c, self.y_c, **kwargs)
                self.draw_title(cnv, ID, self.x_c, self.y_c + self._u.radius, **kwargs)

        # ---- grid marks
        if self.grid_marks:  # and not kwargs.get("card_back", False):
            # print(f'*** {self._u.radius=} {self._u.diameter=}')
            deltag = self.unit(self.grid_marks_length)
            gx, gy = 0, y - self._u.radius  # left-side
            cnv.draw_line((gx, gy), (deltag, gy))
            cnv.draw_line(
                (0, gy + self._u.radius * 2.0), (deltag, gy + self._u.radius * 2.0)
            )
            gx, gy = x - self._u.radius, globals.page[1]  # top-side
            cnv.draw_line((gx, gy), (gx, gy - deltag))
            cnv.draw_line(
                (gx + self._u.radius * 2.0, gy),
                (gx + self._u.radius * 2.0, gy - deltag),
            )
            gx, gy = globals.page[0], y - self._u.radius  # right-side
            cnv.draw_line((gx, gy), (gx - deltag, gy))
            cnv.draw_line(
                (gx, gy + self._u.radius * 2.0), (gx - deltag, gy + self._u.radius * 2)
            )
            gx, gy = x - self._u.radius, 0  # bottom-side
            cnv.draw_line((gx, gy), (gx, gy + deltag))
            cnv.draw_line(
                (gx + self._u.radius * 2.0, gy),
                (gx + self._u.radius * 2.0, gy + deltag),
            )
            # done
            # gargs = kwargs
            # gargs["stroke"] = self.grid_marks_stroke
            # gargs["stroke_width"] = self.grid_marks_stroke_width
            # self.set_canvas_props(cnv=cnv, index=ID, **gargs)
            gargs = {}
            gargs["stroke"] = self.grid_marks_stroke
            gargs["stroke_width"] = self.grid_marks_stroke_width
            gargs["dotted"] = self.grid_marks_dotted
            self.set_canvas_props(cnv=None, index=ID, **gargs)
        # ---- set calculated top-left in user units
        self.calculated_left = (self.x_c - self._u.radius) / self.units
        self.calculated_top = (self.y_c - self._u.radius) / self.units
