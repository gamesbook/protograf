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
import random
from urllib.parse import urlparse

# third party
import pymupdf
from pymupdf import Point as muPoint, Rect as muRect
import segno  # QRCode

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

log = logging.getLogger(__name__)
DEBUG = False


def get_cache(**kwargs):
    """Get and/or set a cache directory for to save file images."""
    default_cache = Path(Path.home(), CACHE_DIRECTORY, "images")
    default_cache.mkdir(parents=True, exist_ok=True)
    cache_directory = kwargs.get("cache_directory", str(default_cache))
    if not os.path.exists(cache_directory):
        feedback(
            "Unable to create or find the cache directory:" f" {str(cache_directory)}",
            True,
        )
    return cache_directory


def set_cached_dir(source):
    """Set special cached directory, depending on source being a URL."""
    if not tools.is_url_valid(url=source):
        return None
    loc = urlparse(source)
    # print('*** @http@',  loc)
    # handle special case of BGG images
    # ... BGG gives thumb and original images the EXACT SAME filename :(
    if loc.netloc == BGG_IMAGES:
        subfolder = "images"
        if "thumb" in loc.path:
            subfolder = "thumbs"
        the_cache = Path(Path.home() / CACHE_DIRECTORY / "bgg" / subfolder)
        the_cache.mkdir(parents=True, exist_ok=True)
        return str(the_cache)
    return None


class ImageShape(BaseShape):
    """
    Image (bitmap or SVG) on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(ImageShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        # overrides / extra args
        self.sliced = kwargs.get("sliced", None)
        self.cache_directory = get_cache(**kwargs)
        self.image_location = None

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Show an image on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        img = None
        # ---- check for Card usage
        cache_directory = str(self.cache_directory)
        _source = self.source
        # feedback(f'*** IMAGE {ID=} {self.source=}')
        if ID is not None and isinstance(self.source, list):
            _source = self.source[ID]
            cache_directory = set_cached_dir(_source) or cache_directory
        elif ID is not None and isinstance(self.source, str):
            _source = self.source
            cache_directory = set_cached_dir(self.source) or cache_directory
        else:
            pass
        # ---- convert to using units
        height = self._u.height
        width = self._u.width
        if self.cx is not None and self.cy is not None:
            if width and height:
                x = self._u.cx - width / 2.0 + self._o.delta_x
                y = self._u.cy - height / 2.0 + self._o.delta_y
            else:
                feedback(
                    "Must supply width and height for use with cx and cy.", stop=True
                )
        else:
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
        rotation = kwargs.get("rotation", self.rotation)
        # ---- load image
        # feedback(f'*** IMAGE {ID=} {_source=} {x=} {y=} {self.rotation=}')
        img, is_dir = self.load_image(  # via base.BaseShape
            globals.doc_page,
            _source,
            origin=(x, y),
            sliced=self.sliced,
            width_height=(width, height),
            cache_directory=cache_directory,
            rotation=rotation,
        )
        if not img and not is_dir:
            if _source:
                feedback(
                    f'Unable to load image "{_source}" - please check name and location',
                    True,
                )
            else:
                feedback(
                    f"Unable to load image - no name provided",
                    True,
                )
        # ---- text
        xc = x + width / 2.0
        yc = y + height / 2.0
        _off = self.heading_size / 2.0
        self.draw_heading(cnv, ID, xc, yc - height / 2.0 - _off, **kwargs)
        self.draw_label(cnv, ID, xc, yc + _off, **kwargs)
        self.draw_title(cnv, ID, xc, yc + height / 2.0 + _off * 3.5, **kwargs)


class ArcShape(BaseShape):
    """
    Arc on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(ArcShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        self.kwargs = kwargs
        # ---- perform overrides
        self.radius = self.radius or self.diameter / 2.0
        if self.cx is None and self.x is None:
            feedback("Either provide x or cx for Arc", True)
        if self.cy is None and self.y is None:
            feedback("Either provide y or cy for Arc", True)
        if self.cx is not None and self.cy is not None:
            self.x = self.cx - self.radius
            self.y = self.cy - self.radius
        # feedback(f'***Arc {self.cx=} {self.cy=} {self.x=} {self.y=}')
        # ---- calculate centre
        radius = self._u.radius
        if self.row is not None and self.col is not None:
            self.x_c = self.col * 2.0 * radius + radius
            self.y_c = self.row * 2.0 * radius + radius
            # log.debug(f"{self.col=}, {self.row=}, {self.x_c=}, {self.y_c=}")
        elif self.cx is not None and self.cy is not None:
            self.x_c = self._u.cx
            self.y_c = self._u.cy
        else:
            self.x_c = self._u.x + radius
            self.y_c = self._u.y + radius
        # feedback(f'***Arc {self.x_c=} {self.y_c=} {self.radius=}')

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw arc on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        if self.use_abs_c:
            self.x_c = self._abs_cx
            self.y_c = self._abs_cy
        # ---- centre point in units
        p_C = Point(self.x_c + self._o.delta_x, self.y_c + self._o.delta_y)
        # ---- circumference point in units
        p_P = geoms.point_on_circle(p_C, self._u.radius, self.angle_start)
        # ---- draw sector
        # feedback(
        #     f'***Arc: {p_P=} {p_C=} {self.angle_start=} {self.angle_width=}')
        cnv.draw_sector(  # anti-clockwise from p_P; 90° default
            (p_C.x, p_C.y), (p_P.x, p_P.y), self.angle_width, fullSector=False
        )
        kwargs["closed"] = False
        kwargs["fill"] = None
        self.set_canvas_props(cnv=cnv, index=ID, **kwargs)


class ArrowShape(BaseShape):
    """
    Arrow on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(ArrowShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        self.kwargs = kwargs
        # ---- unit calcs
        self.points_offset_u = (
            self.unit(self.points_offset) if self.points_offset else 0
        )
        self.head_height_u = (
            self.unit(self.head_height) if self.head_height else self._u.height
        )
        self.head_width_u = (
            self.unit(self.head_width) if self.head_width else self._u.width * 2.0
        )
        # print(f"***1 {self._u.width=} {self.tail_width=}")
        self.tail_width_u = (
            self.unit(self.tail_width) if self.tail_width else self._u.width
        )
        self.tail_notch_u = self.unit(self.tail_notch) if self.tail_notch else 0

    def get_vertexes(self, **kwargs):
        """Calculate vertices of arrow."""
        x_c = kwargs.get("x")
        x_s, y_s = x_c - self.tail_width_u / 2.0, kwargs.get("y")
        tail_height = self._u.height
        total_height = self._u.height + self.head_height_u
        if tail_height <= 0:
            feedback("The Arrow head height must be less than overall height", True)
        # print(f"***2 {self._u.width=} {self.tail_width_u=}  {self.head_width_u=} {self.fill=} ")
        vertices = []
        vertices.append(Point(x_s, y_s))  # lower-left corner
        vertices.append(Point(x_c - self._u.width / 2.0, y_s - tail_height))
        vertices.append(
            Point(
                x_c - self.head_width_u / 2.0, y_s - tail_height - self.points_offset_u
            )
        )
        vertices.append(Point(x_c, y_s - total_height))  # tip
        vertices.append(
            Point(
                x_c + self.head_width_u / 2.0, y_s - tail_height - self.points_offset_u
            )
        )
        vertices.append(Point(x_c + self._u.width / 2.0, y_s - tail_height))
        vertices.append(Point(x_c + self.tail_width_u / 2.0, y_s))  # bottom corner
        if self.tail_notch_u > 0:
            vertices.append(Point(x_c, y_s - self.tail_notch_u))  # centre notch
        return vertices

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw an arrow shape on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        if self.use_abs:
            x = self._abs_x
            y = self._abs_y
        else:
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
        cx = x
        cy = y - self._u.height
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- handle rotation
        rotation = kwargs.get("rotation", self.rotation)
        if rotation:
            self.centroid = muPoint(cx, cy)
            kwargs["rotation"] = rotation
            kwargs["rotation_point"] = self.centroid
        # ---- draw arrow
        self.vertexes = self.get_vertexes(cx=cx, cy=cy, x=x, y=y)
        # feedback(f'***Arrow {x=} {y=} {self.vertexes=}')
        cnv.draw_polyline(self.vertexes)
        kwargs["closed"] = True
        self.set_canvas_props(cnv=cnv, index=ID, **kwargs)
        # ---- dot
        self.draw_dot(cnv, cx, cy)
        # ---- cross
        self.draw_cross(cnv, cx, cy, rotation=kwargs.get("rotation"))
        # ---- text
        self.draw_label(cnv, ID, cx, cy, **kwargs)
        self.draw_heading(cnv, ID, x, y - self._u.height - self.head_height_u, **kwargs)
        self.draw_title(cnv, ID, x, y, **kwargs)


class BezierShape(BaseShape):
    """
    Bezier curve on a given canvas.

    A Bezier curve is specified by four control points:
        (x1,y1), (x2,y2), (x3,y3), (x4,y4).
    The curve starts at (x1,y1) and ends at (x4,y4) with a line segment
    from (x1,y1) to (x2,y2) and a line segment from (x3,y3) to (x4,y4)
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw Bezier curve on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- convert to using units
        x_1 = self._u.x + self._o.delta_x
        y_1 = self._u.y + self._o.delta_y
        if not self.x_1:
            self.x_1 = self.x + self.default_length
        if not self.y_1:
            self.y1 = self.y + self.default_length
        x_2 = self.unit(self.x_1) + self._o.delta_x
        y_2 = self.unit(self.y_1) + self._o.delta_y
        x_3 = self.unit(self.x_2) + self._o.delta_x
        y_3 = self.unit(self.y_2) + self._o.delta_y
        x_4 = self.unit(self.x_3) + self._o.delta_x
        y_4 = self.unit(self.y_3) + self._o.delta_y
        # ---- draw bezier
        cnv.draw_bezier((x_1, y_1), (x_2, y_2), (x_3, y_3), (x_4, y_4))
        kwargs["closed"] = False
        kwargs["fill"] = None
        self.set_canvas_props(cnv=cnv, index=ID, **kwargs)


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

    def calculate_centre(self):
        # ---- calculated centre
        if self.use_abs_c:
            self.x_c = self._abs_cx
            self.y_c = self._abs_cy
        else:
            self.x_c = self._u.cx + self._o.delta_x
            self.y_c = self._u.cy + self._o.delta_y
        return self.x_c, self.y_c

    def calculate_area(self):
        return math.pi * self._u.radius * self._u.radius

    def calculate_perimeter(self, units: bool = False) -> float:
        """Total length of bounding line (circumference)."""
        length = math.pi * 2.0 * self._u.radius
        if units:
            return self.points_to_value(length)
        else:
            return length

    def draw_hatch(
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
            self.hatch, DirectionGroup.CIRCULAR, "circle hatch"
        )
        lines = tools.as_int(num, "hatch_count")
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
            stroke=self.hatch_stroke,
            stroke_width=self.hatch_stroke_width,
            stroke_cap=self.hatch_cap,
            dashed=self.hatch_dashed,
            dotted=self.hatch_dots,
            rotation=rotation,
            rotation_point=muPoint(x_c, y_c),
        )

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
            except:
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
                # ---- draw radii line
                cnv.draw_line((x_start, y_start), (x_end, y_end))
                # ---- style radii lines
                _radii_stroke = _radii_strokes[stroke_key]
                self.set_canvas_props(
                    index=ID,
                    stroke=_radii_stroke,
                    stroke_width=self.radii_stroke_width,
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
                petals_style = self.petals_style.lower()
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

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw circle on a given canvas."""
        kwargs = self.kwargs | kwargs
        _ = kwargs.pop("ID", None)
        # feedback(f' @@@ Circ.draw {kwargs=}')
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        is_cards = kwargs.get("is_cards", False)
        # ---- set centre & area
        x, y = self.calculate_centre()  # self.x_c, self.y_c
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
        is_rotated = False
        rotation = kwargs.get("rotation", self.rotation)
        if rotation:
            self.centroid = muPoint(x, y)
            kwargs["rotation"] = rotation
            kwargs["rotation_point"] = self.centroid
        # ---- draw petals
        if self.petals:
            self.draw_petals(cnv, ID, self.x_c, self.y_c)
        # feedback(f'*** Circle: {x=} {y=}')
        # ---- draw circle
        cnv.draw_circle((x, y), self._u.radius)
        self.set_canvas_props(cnv=cnv, index=ID, **kwargs)
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
            self.set_canvas_props(cnv=None, index=ID, **gargs)

        # ---- draw hatch
        if self.hatch_count:
            self.draw_hatch(
                cnv, ID, self.hatch_count, self.x_c, self.y_c, rotation=rotation
            )
        # ---- draw radii
        if self.radii:
            self.draw_radii(cnv, ID, self.x_c, self.y_c)
        # ---- centred shape (with offset)
        if self.centre_shape:
            if self.can_draw_centred_shape(self.centre_shape):
                self.centre_shape.draw(
                    _abs_cx=x + self.unit(self.centre_shape_mx),
                    _abs_cy=y + self.unit(self.centre_shape_my),
                )
        # ---- cross
        self.draw_cross(cnv, self.x_c, self.y_c, rotation=kwargs.get("rotation"))
        # ---- dot
        self.draw_dot(cnv, self.x_c, self.y_c)
        # ---- text
        self.draw_heading(cnv, ID, self.x_c, self.y_c - self._u.radius, **kwargs)
        self.draw_label(cnv, ID, self.x_c, self.y_c, **kwargs)
        self.draw_title(cnv, ID, self.x_c, self.y_c + self._u.radius, **kwargs)
        # ---- set calculated top-left in user units
        self.calculated_left = (self.x_c - self._u.radius) / self.units
        self.calculated_top = (self.y_c - self._u.radius) / self.units


class ChordShape(BaseShape):
    """
    Chord line on a Circle on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a chord on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        if not isinstance(self.shape, CircleShape):
            feedback("Shape must be a circle!", True)
        circle = self.shape
        x_c, y_c = circle.calculate_centre()
        centre = Point(circle.cx, circle.cy)
        pt0 = geoms.point_on_circle(centre, circle.radius, self.angle)
        pt1 = geoms.point_on_circle(centre, circle.radius, self.angle_1)
        # feedback(f"*** {circle.radius=} {pt0=} {pt1=}")
        x = self.unit(pt0.x) + self._o.delta_x
        y = self.unit(pt0.y) + self._o.delta_y
        x_1 = self.unit(pt1.x) + self._o.delta_x
        y_1 = self.unit(pt1.y) + self._o.delta_y
        # ---- draw chord
        # feedback(f"*** Chord {x=} {y=}, {x_1=} {y_1=}")
        mid_point = geoms.fraction_along_line(Point(x, y), Point(x_1, y_1), 0.5)
        cnv.draw_line(Point(x, y), Point(x_1, y_1))
        kwargs["rotation"] = self.rotation
        kwargs["rotation_point"] = mid_point
        self.set_canvas_props(cnv=cnv, index=ID, **kwargs)  # shape.finish()
        # ---- calculate line rotation
        compass, rotation = geoms.angles_from_points(Point(x, y), Point(x_1, y_1))
        # feedback(f"*** Chord {compass=} {rotation=}")
        # ---- dot
        self.draw_dot(cnv, (x_1 + x) / 2.0, (y_1 + y) / 2.0)
        # ---- text
        kwargs["rotation"] = rotation
        kwargs["rotation_point"] = mid_point
        self.draw_label(
            cnv,
            ID,
            (x_1 + x) / 2.0,
            (y_1 + y) / 2.0,
            centred=False,
            **kwargs,
        )


class CompassShape(BaseShape):
    """
    Compass on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(CompassShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        # overrides
        self.radius = self.radius or self.diameter / 2.0
        if self.cx is not None and self.cy is not None:
            self.x = self.cx - self.radius
            self.y = self.cy - self.radius
            self.width = 2.0 * self.radius
            self.height = 2.0 * self.radius
        self.x_c = None
        self.y_c = None
        self.directions = self.directions or "*"  # compass should always have!

    def draw_radius(self, cnv, ID, x, y, absolute=False):
        # feedback(
        #    f'*** Compass Radius {self.x_c=:.2f} {self.y_c=:.2f}; {x=:.2f} {y=:.2f}')
        if absolute:
            cnv.draw_line((self.x_c, self.y_c), (x, y))
        else:
            cnv.draw_line((self.x_c, self.y_c), (x + self.x_c, y + self.y_c))
        keys = {}
        keys["stroke"] = self.radii_stroke
        keys["stroke_width"] = self.radii_stroke_width
        keys["dashed"] = self.radii_dashed
        keys["dotted"] = self.radii_dotted
        self.set_canvas_props(cnv=cnv, index=ID, **keys)

    def circle_radius(self, cnv, ID, angle):
        """Calc x,y on circle and draw line from centre to it."""
        x = self._u.radius * math.sin(math.radians(angle))
        y = self._u.radius * math.cos(math.radians(angle))
        self.draw_radius(cnv, ID, x, y)

    def rectangle_radius(self, cnv, ID, vertices, angle, height, width):
        """Calc x,y on rectangle and draw line from centre to it."""

        def get_xy(radians, radius):
            x = radius * math.sin(radians)
            y = radius * math.cos(radians)
            return x, y

        # feedback(f'*** Compass {angle=}', False)
        radians = math.radians(angle)
        match angle:
            # ---- primary directions
            case 0:
                x, y = get_xy(radians, 0.5 * height)
                self.draw_radius(cnv, ID, x, y)
            case 90:
                x, y = get_xy(radians, 0.5 * width)
                self.draw_radius(cnv, ID, x, y)
            case 180:
                x, y = get_xy(radians, 0.5 * height)
                self.draw_radius(cnv, ID, x, y)
            case 270:
                x, y = get_xy(radians, 0.5 * width)
                self.draw_radius(cnv, ID, x, y)
            # ---- secondary directions
            case 45:
                x, y = vertices[2].x, vertices[2].y
                self.draw_radius(cnv, ID, x, y, True)
            case 135:
                x, y = vertices[1].x, vertices[1].y
                self.draw_radius(cnv, ID, x, y, True)
            case 225:
                x, y = vertices[0].x, vertices[0].y
                self.draw_radius(cnv, ID, x, y, True)
            case 315:
                x, y = vertices[3].x, vertices[3].y
                self.draw_radius(cnv, ID, x, y, True)
            case _:
                feedback(f"{angle} not in range", True)

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw compass on a given canvas."""
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        # convert to using units
        height = self._u.height
        width = self._u.width
        radius = self._u.radius
        # ---- overrides to centre the shape
        if self.use_abs_c:
            self.x_c = self._abs_cx
            self.y_c = self._abs_cy
        elif self.row is not None and self.col is not None:
            self.x_c = self.col * 2.0 * radius + radius + self._o.delta_x
            self.y_c = self.row * 2.0 * radius + radius + self._o.delta_y
            log.debug("row:%s col:%s x:%s y:%s", self.col, self.row, self.x_c, self.y_c)
        elif self.cx is not None and self.cy is not None:
            self.x_c = self._u.cx + self._o.delta_x
            self.y_c = self._u.cy + self._o.delta_y
        else:
            if self.perimeter == "rectangle":
                self.x_c = self._u.x + width / 2.0 + self._o.delta_x
                self.y_c = self._u.y + height / 2.0 + self._o.delta_x
            else:
                self.x_c = self._u.x + self._o.delta_x + radius
                self.y_c = self._u.y + self._o.delta_y + radius
        # ---- draw perimeter
        if self.perimeter == "circle":
            cnv.draw_circle((self.x_c, self.y_c), radius)
            self.set_canvas_props(cnv=cnv, index=ID, **kwargs)
        # ---- draw compass in circle
        _directions = tools.validated_directions(
            self.directions, DirectionGroup.COMPASS, "compass directions"
        )
        if self.perimeter == "circle":
            for direction in _directions:
                match direction:
                    case "n":
                        self.circle_radius(cnv, ID, 0)
                    case "ne":
                        self.circle_radius(cnv, ID, 45)
                    case "e":
                        self.circle_radius(cnv, ID, 90)
                    case "se":
                        self.circle_radius(cnv, ID, 135)
                    case "s":
                        self.circle_radius(cnv, ID, 180)
                    case "sw":
                        self.circle_radius(cnv, ID, 225)
                    case "w":
                        self.circle_radius(cnv, ID, 270)
                    case "nw":
                        self.circle_radius(cnv, ID, 315)
                    case _:
                        pass
        # ---- draw compass in rect
        if self.perimeter == "rectangle":
            if self.radii_length is not None:
                feedback(
                    "radii_length cannot be used for a rectangle-perimeter Compass",
                    False,
                    True,
                )
            rect = RectangleShape(**self.kwargs)
            rotation = 0
            vertices = rect.get_vertexes(**kwargs)

            for direction in _directions:
                match direction:
                    case "n":
                        self.rectangle_radius(cnv, ID, vertices, 0, height, width)
                    case "ne":
                        self.rectangle_radius(cnv, ID, vertices, 45, height, width)
                    case "e":
                        self.rectangle_radius(cnv, ID, vertices, 90, height, width)
                    case "se":
                        self.rectangle_radius(cnv, ID, vertices, 315, height, width)
                    case "s":
                        self.rectangle_radius(cnv, ID, vertices, 180, height, width)
                    case "sw":
                        self.rectangle_radius(cnv, ID, vertices, 225, height, width)
                    case "w":
                        self.rectangle_radius(cnv, ID, vertices, 270, height, width)
                    case "nw":
                        self.rectangle_radius(cnv, ID, vertices, 135, height, width)
                    case _:
                        pass
        # ---- draw compass in hex
        if self.perimeter == "hexagon":
            for direction in _directions:
                match direction:
                    case "n":
                        self.circle_radius(cnv, ID, 0)
                    case "ne":
                        self.circle_radius(cnv, ID, 60)
                    case "e":
                        pass
                    case "se":
                        self.circle_radius(cnv, ID, 120)
                    case "s":
                        self.circle_radius(cnv, ID, 180)
                    case "sw":
                        self.circle_radius(cnv, ID, 240)
                    case "w":
                        pass
                    case "nw":
                        self.circle_radius(cnv, ID, 300)
                    case _:
                        pass

        # ---- cross
        self.draw_cross(cnv, self.x_c, self.y_c, rotation=kwargs.get("rotation"))
        # ---- dot
        self.draw_dot(cnv, self.x_c, self.y_c)
        # ---- text
        self.draw_heading(cnv, ID, self.x_c, self.y_c - radius, **kwargs)
        self.draw_label(cnv, ID, self.x_c, self.y_c, **kwargs)
        self.draw_title(cnv, ID, self.x_c, self.y_c + radius, **kwargs)


class DotShape(BaseShape):
    """
    Dot of fixed radius on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a dot on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # feedback(f"*** Dot {self._o.delta_x=} {self._o.delta_y=}")
        if self.use_abs_c:
            x = self._abs_cx
            y = self._abs_cy
        else:
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
        size = self.dot_point / 2.0  # diameter is 3 points ~ 1mm or 1/32"
        self.fill = self.stroke
        center = muPoint(x, y)
        # ---- draw dot
        # feedback(f'*** Dot {size=} {x=} {y=}')
        cnv.draw_circle(center=center, radius=size)
        kwargs["rotation"] = self.rotation
        kwargs["rotation_point"] = center
        self.set_canvas_props(cnv=cnv, index=ID, **kwargs)  # shape.finish()
        # ---- text
        self.draw_heading(cnv, ID, x, y, **kwargs)
        self.draw_label(cnv, ID, x, y, **kwargs)
        self.draw_title(cnv, ID, x, y, **kwargs)


class EllipseShape(BaseShape):
    """
    Ellipse on a given canvas.
    """

    def calculate_area(self):
        return math.pi * self._u.height * self._u.width

    def calculate_xy(self, **kwargs):
        # ---- adjust start
        if self.row is not None and self.col is not None:
            x = self.col * self._u.width + self._o.delta_x
            y = self.row * self._u.height + self._o.delta_y
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
        # ---- overrides for centering
        rotation = kwargs.get("rotation", None)
        if rotation:
            x = -self._u.width / 2.0
            y = -self._u.height / 2.0
        return x, y

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw ellipse on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- calculate properties
        x, y = self.calculate_xy()
        # ---- overrides for grid layout
        if self.use_abs_c:
            x = self._abs_cx - self._u.width / 2.0
            y = self._abs_cy - self._u.height / 2.0
        x_d = x + self._u.width / 2.0  # centre
        y_d = y + self._u.height / 2.0  # centre
        self.area = self.calculate_area()
        delta_m_up, delta_m_down = 0.0, 0.0  # potential text offset from chevron
        # ---- handle rotation
        rotation = kwargs.get("rotation", self.rotation)
        if rotation:
            self.centroid = muPoint(x_d, y_d)
            kwargs["rotation"] = rotation
            kwargs["rotation_point"] = self.centroid
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- draw ellipse
        cnv.draw_oval((x, y, x + self._u.width, y + self._u.height))
        self.set_canvas_props(cnv=cnv, index=ID, **kwargs)  # shape.finish()
        # ---- cross
        self.draw_cross(cnv, x_d, y_d, rotation=kwargs.get("rotation"))
        # ---- dot
        self.draw_dot(cnv, x_d, y_d)
        # ---- text
        self.draw_heading(
            cnv, ID, x_d, y_d - 0.5 * self._u.height - delta_m_up, **kwargs
        )
        self.draw_label(cnv, ID, x_d, y_d, **kwargs)
        self.draw_title(
            cnv, ID, x_d, y_d + 0.5 * self._u.height + delta_m_down, **kwargs
        )


class EquilateralTriangleShape(BaseShape):
    """
    Equilateral Triangle on a given canvas.
    """

    def draw_hatch(
        self, cnv, ID, side: float, vertices: list, num: int, rotation: float = 0.0
    ):
        _dirs = tools.validated_directions(
            self.hatch, DirectionGroup.HEX_POINTY_EDGE, "triangle hatch"
        )
        lines = tools.as_int(num, "hatch_count")
        if lines >= 1:
            # v_tl, v_tr, v_bl, v_br
            if "ne" in _dirs or "sw" in _dirs:  # slope UP to the right
                self.draw_lines_between_sides(
                    cnv, side, lines, vertices, (0, 1), (2, 1), True
                )
            if "se" in _dirs or "nw" in _dirs:  # slope DOWN to the right
                self.draw_lines_between_sides(
                    cnv, side, lines, vertices, (0, 2), (0, 1), True
                )
            if "e" in _dirs or "w" in _dirs:  # horizontal
                self.draw_lines_between_sides(
                    cnv, side, lines, vertices, (0, 2), (1, 2), True
                )
        # ---- set canvas
        centre = self.get_centroid(vertices)
        self.set_canvas_props(
            index=ID,
            stroke=self.hatch_stroke,
            stroke_width=self.hatch_stroke_width,
            stroke_cap=self.hatch_cap,
            dashed=self.hatch_dashed,
            dotted=self.hatch_dots,
            rotation=rotation,
            rotation_point=centre,
        )

    def calculate_area(self) -> float:
        _side = self._u.side if self._u.side else self._u.width
        return math.sqrt(3) / 4.0 * _side**2

    def calculate_perimeter(self, units: bool = False) -> float:
        """Total length of bounding line."""
        _side = self._u.side if self._u.side else self._u.width
        length = 3 * _side
        if units:
            return self.points_to_value(length)
        else:
            return length

    def get_vertexes(
        self, x: float, y: float, side: float, hand: str, flip: str
    ) -> list:
        height = 0.5 * math.sqrt(3) * side  # ½√3(a)
        vertices = []
        pt0 = Point(x + self._o.delta_x, y + self._o.delta_y)
        vertices.append(pt0)
        hand = hand or "east"
        flip = flip or "north"
        # print(f"*** {hand=} {flip=}")
        if hand == "west" or hand == "w":
            x2 = pt0.x - side
            y2 = pt0.y
            x3 = pt0.x - 0.5 * side
        elif hand == "east" or hand == "e":
            x2 = pt0.x + side
            y2 = pt0.y
            x3 = x2 - 0.5 * side
        else:
            raise ValueError(f"The value {hand} is not allowed for hand")
        if flip == "north" or flip == "n":
            y3 = pt0.y - height
        elif flip == "south" or flip == "s":
            y3 = pt0.y + height
        else:
            raise ValueError(f"The value {flip} is not allowed for flip")
        vertices.append(Point(x2, y2))
        vertices.append(Point(x3, y3))
        return vertices

    def get_centroid(self, vertices: list) -> Point:
        x_c = (vertices[0].x + vertices[1].x + vertices[2].x) / 3.0
        y_c = (vertices[0].y + vertices[1].y + vertices[2].y) / 3.0
        return Point(x_c, y_c)

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw an equilateraltriangle on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- calculate points
        x, y = self._u.x, self._u.y
        # angle = self.angle
        side = self._u.side if self._u.side else self._u.width
        height = 0.5 * math.sqrt(3) * side  # ½√3(a)
        if self.cx and self.cy:
            self.centroid = Point(self._u.cx, self._u.cy)
            centroid_to_vertex = side / math.sqrt(3)
            y_off = height + centroid_to_vertex
            x = self._u.cx - side / 2.0
            y = self._u.cy + (height - centroid_to_vertex)
            # print(f'** {side=} {height=} {centroid_to_vertex=} {y_off=}')
        # feedback(f'*** EQT {side=} {height=} {self.fill=} {self.stroke=}')
        self.vertexes = self.get_vertexes(x, y, side, self.hand, self.flip)
        self.centroid = self.get_centroid(self.vertexes)
        # ---- handle rotation
        rotation = kwargs.get("rotation", self.rotation)
        if rotation:
            kwargs["rotation"] = rotation
            kwargs["rotation_point"] = self.centroid
        # ---- draw equilateral triangle
        # feedback(f'*** EqiTri {x=} {y=} {self.vertexes=} {kwargs=}')
        cnv.draw_polyline(self.vertexes)
        kwargs["closed"] = True
        self.set_canvas_props(cnv=cnv, index=ID, **kwargs)

        # ---- debug
        self._debug(cnv, vertices=self.vertexes)
        # ---- draw hatch
        if self.hatch_count:
            self.draw_hatch(cnv, ID, side, self.vertexes, self.hatch_count, rotation)
        # ---- centred shape (with offset)
        if self.centre_shape:
            if self.can_draw_centred_shape(self.centre_shape):
                self.centre_shape.draw(
                    _abs_cx=self.centroid.x + self.unit(self.centre_shape_mx),
                    _abs_cy=self.centroid.y + self.unit(self.centre_shape_my),
                )
        # ---- dot
        self.draw_dot(cnv, self.centroid.x, self.centroid.y)
        # ---- text
        self.draw_heading(
            cnv, ID, self.centroid.x, self.centroid.y - height * 2.0 / 3.0, **kwargs
        )
        self.draw_label(cnv, ID, self.centroid.x, self.centroid.y, **kwargs)
        self.draw_title(
            cnv, ID, self.centroid.x, self.centroid.y + height / 3.0, **kwargs
        )


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
                "No value for side or height or diameter or radius supplied for hexagon.",
                True,
            )
        # ---- diameter and radius
        diameter = 2.0 * side
        radius = side
        if self.orientation.lower() in ["p", "pointy"]:
            self.width = 2 * half_flat / self.units
            self.height = 2 * radius / self.units
        elif self.orientation.lower() in ["f", "flat"]:
            self.height = 2 * half_flat / self.units
            self.width = 2 * radius / self.units
        else:
            feedback(
                'Invalid orientation "{self.orientation}" supplied for hexagon.', True
            )
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
            if str(self.coord_style).lower() in ["d", "diagonal"]:
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

    def draw_links(self, cnv, ID, side: float, vertices: list, links: list):
        """Draw arcs or lines to link two sides of a hexagon."""
        self.set_canvas_props(
            index=ID,
            stroke=self.link_stroke,
            stroke_width=self.link_width,
            stroke_cap=self.link_cap,
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
            feedback(f"a:{va_start}-{va_end} b:{vb_start}-{vb_end}")

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

    def draw_radii(self, cnv, ID, centre: Point, vertices: list):
        """Draw line(s) connecting the Hexagon centre to a vertex."""
        # _dirs = self.radii.lower().split()
        dir_group = (
            DirectionGroup.HEX_POINTY
            if self.orientation == "pointy"
            else DirectionGroup.HEX_FLAT
        )
        _dirs = tools.validated_directions(self.radii, dir_group, "hex radii")
        if "ne" in _dirs:  # slope UP to the right
            cnv.draw_line(centre, vertices[4])
        if "sw" in _dirs:  # slope DOWN to the left
            cnv.draw_line(centre, vertices[1])
        if "se" in _dirs:  # slope DOWN to the right
            if self.orientation in ["p", "pointy"]:
                cnv.draw_line(centre, vertices[3])
            else:
                cnv.draw_line(centre, vertices[2])
        if "nw" in _dirs:  # slope UP to the left
            if self.orientation in ["p", "pointy"]:
                cnv.draw_line(centre, vertices[0])
            else:
                cnv.draw_line(centre, vertices[5])
        if "n" in _dirs and self.orientation in ["p", "pointy"]:  # vertical UP
            cnv.draw_line(centre, vertices[5])
        if "s" in _dirs and self.orientation in ["p", "pointy"]:  # vertical DOWN
            cnv.draw_line(centre, vertices[2])
        if "e" in _dirs and self.orientation in ["f", "flat"]:  # horizontal RIGHT
            cnv.draw_line(centre, vertices[3])
        if "w" in _dirs and self.orientation in ["f", "flat"]:  # horizontal LEFT
            cnv.draw_line(centre, vertices[0])
        # color, thickness etc.
        self.set_canvas_props(
            index=ID,
            stroke=self.radii_stroke or self.stroke,
            stroke_width=self.radii_stroke_width or self.stroke_width,
            stroke_cap=self.radii_cap or self.line_cap,
        )

    def draw_perbis(
        self, cnv, ID, centre: Point, vertices: list, rotation: float = None
    ):
        """Draw lines connecting the Hexagon centre to the centre of each edge.

        Def:
        A perpendicular bisector ("perbis") of a chord is:
            A line passing through the center of circle such that it divides the
            chord into two equal parts and meets the chord at a right angle;
            for a polygon, each edge is effectively a chord.
        """
        _perbis = []  # store angles to centre of edges (the "chords")
        _perbis_pts = []  # store centre Point of edges
        vcount = len(vertices) - 1
        for key, vertex in enumerate(vertices):
            if key == 0:
                p1 = Point(vertex.x, vertex.y)
                p2 = Point(vertices[vcount].x, vertices[vcount].y)
            else:
                p1 = Point(vertex.x, vertex.y)
                p2 = Point(vertices[key - 1].x, vertices[key - 1].y)
            pc = geoms.fraction_along_line(p1, p2, 0.5)  # centre pt of edge
            _perbis_pts.append(pc)
            _, angle = geoms.angles_from_points(centre, pc)
            _perbis.append(angle)
        pb_offset = self.unit(self.perbis_offset, label="perbis offset") or 0
        pb_length = (
            self.unit(self.perbis_length, label="perbis length")
            if self.perbis_length
            else self.radius
        )
        if self.perbis:
            dir_group = (
                DirectionGroup.HEX_POINTY_EDGE
                if self.orientation == "pointy"
                else DirectionGroup.HEX_FLAT_EDGE
            )
            perbis_dirs = tools.validated_directions(
                self.perbis, dir_group, "hex perbis"
            )
            _dirs = []
            # feedback(f'*** HEX {self.perbis=} {self.orientation=} {perbis_dirs=}')
            if self.orientation in ["p", "pointy"]:
                if "e" in perbis_dirs:
                    _dirs.append(4)
                if "ne" in perbis_dirs:
                    _dirs.append(5)
                if "nw" in perbis_dirs:
                    _dirs.append(0)
                if "w" in perbis_dirs:
                    _dirs.append(1)
                if "sw" in perbis_dirs:
                    _dirs.append(2)
                if "se" in perbis_dirs:
                    _dirs.append(3)
            if self.orientation in ["f", "flat"]:
                if "ne" in perbis_dirs:
                    _dirs.append(4)
                if "n" in perbis_dirs:
                    _dirs.append(5)
                if "nw" in perbis_dirs:
                    _dirs.append(0)
                if "sw" in perbis_dirs:
                    _dirs.append(1)
                if "s" in perbis_dirs:
                    _dirs.append(2)
                if "se" in perbis_dirs:
                    _dirs.append(3)

        for key, pb_angle in enumerate(_perbis):
            if self.perbis and key not in _dirs:
                continue
            # points based on length of line, offset and the angle in degrees
            edge_pt = _perbis_pts[key]
            if pb_offset is not None and pb_offset != 0:
                offset_pt = geoms.point_on_circle(centre, pb_offset, pb_angle)
                end_pt = geoms.point_on_line(offset_pt, edge_pt, pb_length)
                # print(f'{pb_angle=} {offset_pt=} {x_c=}, {y_c=}')
                cnv.draw_line((offset_pt.x, offset_pt.y), (end_pt.x, end_pt.y))
            else:
                cnv.draw_line((centre.x, centre.y), (edge_pt.x, edge_pt.y))

        self.set_canvas_props(
            index=ID,
            stroke=self.perbis_stroke,
            stroke_width=self.perbis_stroke_width,
            dashed=self.perbis_dashed,
            dotted=self.perbis_dotted,
        )

    def draw_hatch(
        self, cnv, ID, side: float, vertices: list, num: int, rotation: float = 0.0
    ):
        """Draw lines connecting two opposite sides and parallel to adjacent Hex side.

        Args:
            ID: unique ID
            side: length of a hexagon side
            vertices: the hexagons's nodes
            num: number of lines
            rotation: degrees anti-clockwise from horizontal "east"
        """
        dir_group = (
            DirectionGroup.HEX_POINTY
            if self.orientation == "pointy"
            else DirectionGroup.HEX_FLAT
        )
        _dirs = tools.validated_directions(self.hatch, dir_group, "hexagon hatch")
        _num = tools.as_int(num, "hatch_count")
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
            if self.orientation in ["p", "pointy"]:
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
            if self.orientation in ["f", "flat"]:
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
            stroke=self.hatch_stroke,
            stroke_width=self.hatch_stroke_width,
            stroke_cap=self.hatch_cap,
            dashed=self.hatch_dashed,
            dotted=self.hatch_dots,
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
                "No value for side or height or diameter or radius supplied for hexagon.",
                True,
            )
        half_side = side / 2.0
        height_flat = 2 * half_flat
        diameter = 2.0 * side
        radius = side
        z_fraction = (diameter - side) / 2.0
        return HexGeometry(
            radius, diameter, side, half_side, half_flat, height_flat, z_fraction
        )

    def get_vertexes(self, is_cards=False):
        """Calculate vertices of hexagon."""
        geo = self.get_geometry()
        # ---- POINTY^
        if self.orientation.lower() in ["p", "pointy"]:
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
        else:
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
                # y = self.row * 2.0 * geo.half_flat + self._o.delta_y  # do NOT add half_flat
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
        if self.orientation.lower() in ["p", "pointy"]:
            self.vertexes = [  # clockwise from bottom-left; relative to centre
                muPoint(x, y + geo.z_fraction),
                muPoint(x, y + geo.z_fraction + geo.side),
                muPoint(x + geo.half_flat, y + geo.diameter),
                muPoint(x + geo.height_flat, y + geo.z_fraction + geo.side),
                muPoint(x + geo.height_flat, y + geo.z_fraction),
                muPoint(x + geo.half_flat, y),
            ]
        # ---- ~ flat hexagon vertices (clockwise)
        else:  # self.orientation.lower() in ['f',  'flat']:
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
        # feedback(f'***Hex {x=} {y=} {self.vertexes=} {self.kwargs=')

        # ---- draw hexagon with caltrops
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
                        vertex0, vertex1, self.side, self.caltrops, self.caltrops_invert
                    )
                    if self.caltrops_invert:
                        cnv.draw_line(caltrop_points[0], caltrop_points[1])
                    else:
                        for caltrop_point in caltrop_points:
                            cnv.draw_line(caltrop_point[0], caltrop_point[1])
            self.set_canvas_props(cnv=cnv, index=ID, **kwargs)
        # ---- draw normal hexagon
        else:
            kwargs["fill"] = kwargs.get("fill", self.fill)
            kwargs["stroke"] = kwargs.get("stroke", self.stroke)
            if self.draw_polyline_props(cnv, self.vertexes, **kwargs):
                kwargs["closed"] = True
                self.set_canvas_props(cnv=cnv, index=ID, **kwargs)

        # ---- * borders (override)
        if self.borders:
            if isinstance(self.borders, tuple):
                self.borders = [
                    self.borders,
                ]
            if not isinstance(self.borders, list):
                feedback('The "borders" property must be a list of sets or a set')
            for border in self.borders:
                self.draw_border(cnv, border, ID)  # BaseShape

        # ---- debug
        # self._debug(cnv, Point(x, y), 'start')
        # self._debug(cnv, Point(self.x_d, self.y_d), 'centre')
        self._debug(cnv, vertices=self.vertexes)
        # ---- draw hatch
        if self.hatch_count:
            if not self.hatch_count & 1:
                feedback("Hatch count must be an odd number for a Hexagon", True)
            self.draw_hatch(cnv, ID, geo.side, self.vertexes, self.hatch_count)
        # ---- draw links
        if self.links:
            self.draw_links(cnv, ID, geo.side, self.vertexes, self.links)
        # ---- draw radii
        if self.radii:
            self.draw_radii(cnv, ID, Point(self.x_d, self.y_d), self.vertexes)
        # ---- draw perbis
        if self.perbis:
            self.draw_perbis(cnv, ID, Point(self.x_d, self.y_d), self.vertexes)
        # ---- centred shape (with offset)
        if self.centre_shape:
            if self.can_draw_centred_shape(self.centre_shape):
                self.centre_shape.draw(
                    _abs_cx=self.x_d + self.unit(self.centre_shape_mx),
                    _abs_cy=self.y_d + self.unit(self.centre_shape_my),
                )
        # ---- cross
        self.draw_cross(cnv, self.x_d, self.y_d, rotation=kwargs.get("rotation"))
        # ---- dot
        self.draw_dot(cnv, self.x_d, self.y_d)
        # ---- text
        if self.orientation.lower() in ["p", "pointy"]:
            offset = geo.side  # == radius
        else:
            offset = geo.half_flat
        self.draw_heading(cnv, ID, self.x_d, self.y_d - offset, **kwargs)
        self.draw_label(cnv, ID, self.x_d, self.y_d, **kwargs)
        self.draw_title(cnv, ID, self.x_d, self.y_d + offset, **kwargs)
        # ----  numbering
        self.set_coord(cnv, self.x_d, self.y_d, geo.half_flat)
        # ---- set grid property
        self.grid = GridShape(label=self.coord_text, x=self.x_d, y=self.y_d, shape=self)
        # ---- set calculated top-left in user units
        self.calculated_left = (self.x_d - offset) / self.units
        self.calculated_top = (self.y_d - offset) / self.units


class LineShape(BaseShape):
    """
    Line on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a line on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        if self.use_abs:
            x = self._abs_x
            y = self._abs_y
        else:
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
        if self.use_abs_1:
            x_1 = self._abs_x1
            y_1 = self._abs_y1
        elif self.x_1 or self.y_1:
            x_1 = self.unit(self.x_1) + self._o.delta_x
            y_1 = self.unit(self.y_1) + self._o.delta_y
        elif self.angle != 0 and self.cx and self.cy and self.length:
            # calc points for line "sticking out" both sides of a centre points
            _len = self.unit(self.length) / 2.0
            _cx = self.unit(self.cx) + self._o.delta_x
            _cy = self.unit(self.cy) + self._o.delta_y
            angle1 = max(self.angle + 180.0, self.angle - 180.0)
            delta_pt_2 = geoms.point_from_angle(Point(0, 0), _len, self.angle)
            delta_pt_1 = geoms.point_from_angle(Point(0, 0), _len, angle1)
            # use delta point as offset because function works in Euclidian space
            x, y = _cx + delta_pt_1.x, _cy - delta_pt_1.y
            x_1, y_1 = _cx + delta_pt_2.x, _cy - delta_pt_2.y
        else:
            if self.angle != 0:
                angle = math.radians(self.angle)
                x_1 = x + (self._u.length * math.cos(angle))
                y_1 = y - (self._u.length * math.sin(angle))
            else:
                x_1 = x + self._u.length
                y_1 = y

        if self.row is not None and self.row >= 0:
            y = y + self.row * self._u.height
            y_1 = y_1 + self.row * self._u.height  # - self._u.margin_bottom
        if self.col is not None and self.col >= 0:
            x = x + self.col * self._u.width
            x_1 = x_1 + self.col * self._u.width  # - self._u.margin_left
        # feedback(f"*** Line {x=} {x_1=} {y=} {y_1=}")
        # ---- calculate line rotation
        match self.rotation_point:
            case "centre" | "center" | "c" | None:  # default
                mid_point = geoms.fraction_along_line(Point(x, y), Point(x_1, y_1), 0.5)
                the_point = muPoint(mid_point[0], mid_point[1])
            case "start" | "s":
                the_point = muPoint(x, y)
            case "end" | "e":
                the_point = muPoint(x_1, y_1)
            case _:
                raise ValueError(
                    f'Cannot calculate rotation point "{self.rotation_point}"', True
                )
        # ---- draw line
        cnv.draw_line(Point(x, y), Point(x_1, y_1))
        self.set_canvas_props(cnv=cnv, index=ID, **kwargs)  # shape.finish()
        # ---- dot
        self.draw_dot(cnv, (x_1 + x) / 2.0, (y_1 + y) / 2.0)
        # ---- text
        _, _rotation = geoms.angles_from_points(Point(x, y), Point(x_1, y_1))
        kwargs["rotation"] = -1 * _rotation
        kwargs["rotation_point"] = the_point
        self.draw_label(
            cnv,
            ID,
            (x_1 + x) / 2.0,
            (y_1 + y) / 2.0 + self.font_size / 4.0,
            centred=False,
            **kwargs,
        )
        # ---- arrowhead
        if (
            self.arrow
            or self.arrow_style
            or self.arrow_position
            or self.arrow_height
            or self.arrow_width
            or self.arrow_double
        ):
            self.draw_arrowhead(cnv, Point(x, y), Point(x_1, y_1), **kwargs)
            if self.arrow_double:
                self.draw_arrowhead(cnv, Point(x_1, y_1), Point(x, y), **kwargs)


class PolygonShape(BaseShape):
    """
    Regular polygon on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(PolygonShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        self.use_diameter = True if self.is_kwarg("diameter") else False
        self.use_height = True if self.is_kwarg("height") else False
        self.use_width = True if self.is_kwarg("width") else False
        self.use_radius = True if self.is_kwarg("radius") else False
        # ---- perform overrides
        if self.perbis:
            if isinstance(self.perbis, str):
                if self.perbis.strip().lower() in ["all", "*"]:
                    sides = tools.as_int(self.sides, "sides")
                    self.perbis = list(range(1, sides + 1))
                else:
                    self.perbis = tools.sequence_split(self.perbis)
            if not isinstance(self.perbis, list):
                feedback("The perbis value must be a list of numbers!", True)
        if self.cx is not None and self.cy is not None:
            self.x, self.y = self.cx, self.cy
        # ---- class variables
        self.flatten_angle = 0
        if (self.orientation.lower() == "flat" and not (self.sides - 2) % 4 == 0) or (
            self.orientation.lower() == "pointy" and (self.sides - 2) % 4 == 0
        ):
            interior = ((self.sides - 2) * 180.0) / self.sides
            self.flatten_angle = (180 - interior) / 2.0
        # ---- RESET UNIT PROPS (last!)
        self.set_unit_properties()

    def get_radius(self) -> float:
        if self.radius and self.use_radius:
            radius = self._u.radius
        elif self.diameter and self.use_diameter:
            radius = self._u.diameter / 2.0
        elif self.height and self.use_height:
            radius = self._u.height / 2.0
        elif self.width and self.use_width:
            radius = self._u.width / 2.0
        else:
            side = self._u.side
            sides = int(self.sides)
            # 180 degrees is math.pi radians
            radius = side / (2.0 * math.sin(math.pi / sides))
        return radius

    def calculate_area(self) -> float:
        sides = tools.as_int(self.sides, "sides")
        radius = self.get_radius()
        area = (sides * radius * radius / 2.0) * math.sin(2.0 * math.pi / sides)
        return area

    def draw_mesh(self, cnv, ID, vertices: list):
        """Lines connecting each vertex to mid-points of opposing sides."""
        feedback("Mesh for Polygon is not yet implemented.", True)
        """ TODO - autodraw (without dirs)
        self.set_canvas_props(
            index=ID,
            stroke=self.mesh_stroke or self.stroke,
            stroke_width=self.mesh_stroke_width or self.stroke_width,
            stroke_cap=self.mesh_cap or self.line_cap)
        """

    def get_centre(self) -> Point:
        """Calculate the centre as a Point (in units)"""
        if self.cx is not None and self.cy is not None:
            x = self._u.cx + self._o.delta_x
            y = self._u.cy + self._o.delta_y
        else:
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
        # ---- recalculate centre if preset
        if self.use_abs_c:
            if self._abs_cx is not None and self._abs_cy is not None:
                x = self._abs_cx
                y = self._abs_cy
        return Point(x, y)

    def get_angles(self, rotation: float = 0, is_rotated: bool = False) -> list:
        """Angles of lines connecting the Polygon centre to each of the vertices."""
        centre = self.get_centre()
        vertices = self.get_vertexes(rotation, is_rotated)
        angles = []
        for vertex in vertices:
            _, angle = geoms.angles_from_points(centre, vertex)
            angles.append(angle)
        return angles

    def draw_perbis(
        self,
        cnv,
        ID,
        centre: Point = None,
        vertices: list = None,
        rotation: float = None,
    ):
        """Draw lines connecting the Polygon centre to the centre of each edge.

        Def:
            A perpendicular bisector ("perbis") of a chord is:
            A line passing through the center of circle such that it divides the
            chord into two equal parts and meets the chord at a right angle;
            for a polygon, each edge is effectively a chord.
        """
        if not centre:
            centre = self.get_center()
        if not vertices:
            vertices = self.get_vertexes(rotation=rotation)
        _perbis = []  # store angles to centre of edges (the "chords")
        _perbis_pts = []  # store centre Point of edges
        vcount = len(vertices) - 1
        vertices.reverse()
        for key, vertex in enumerate(vertices):
            if key == 0:
                p1 = Point(vertex.x, vertex.y)
                p2 = Point(vertices[vcount].x, vertices[vcount].y)
            else:
                p1 = Point(vertex.x, vertex.y)
                p2 = Point(vertices[key - 1].x, vertices[key - 1].y)
            pc = geoms.fraction_along_line(p1, p2, 0.5)  # centre pt of edge
            _perbis_pts.append(pc)
            _, angle = geoms.angles_from_points(centre, pc)
            angle = 360.0 - angle if angle > 0.0 else angle
            _perbis.append(angle)
        pb_offset = self.unit(self.perbis_offset, label="perbis offset") or 0
        pb_length = (
            self.unit(self.perbis_length, label="perbis length")
            if self.perbis_length
            else self.get_radius()
        )
        for key, pb_angle in enumerate(_perbis):
            if self.perbis and key + 1 not in self.perbis:
                continue
            # points based on length of line, offset and the angle in degrees
            edge_pt = _perbis_pts[key]
            # print(f'*** {pb_angle=} {edge_pt=} {centre=}')
            if pb_offset is not None and pb_offset != 0:
                offset_pt = geoms.point_on_circle(centre, pb_offset, pb_angle)
                end_pt = geoms.point_on_line(offset_pt, edge_pt, pb_length)
                # print(f'*** {end_pt=} {offset_pt=}')
                cnv.draw_line((offset_pt.x, offset_pt.y), (end_pt.x, end_pt.y))
            else:
                cnv.draw_line((centre.x, centre.y), (edge_pt.x, edge_pt.y))
        self.set_canvas_props(
            index=ID,
            stroke=self.perbis_stroke,
            stroke_width=self.perbis_stroke_width,
            dashed=self.perbis_dashed,
            dotted=self.perbis_dotted,
        )

    def draw_radii(
        self,
        cnv,
        ID,
        centre: Point = None,
        vertices: list = None,
        rotation: float = None,
    ):
        """Draw lines connecting the Polygon centre to each of the vertices."""
        if not centre:
            centre = self.get_center()
        if not vertices:
            vertices = self.get_vertexes(rotation=rotation)
        _radii = []
        for vertex in vertices:
            _, angle = geoms.angles_from_points(centre, vertex)
            _radii.append(angle)
        rad_offset = self.unit(self.radii_offset, label="radii offset") or 0
        rad_length = (
            self.unit(self.radii_length, label="radii length")
            if self.radii_length
            else self.get_radius()
        )
        for rad_angle in _radii:
            # points based on length of line, offset and the angle in degrees
            diam_pt = geoms.point_on_circle(centre, rad_length, rad_angle)
            if rad_offset is not None and rad_offset != 0:
                offset_pt = geoms.point_on_circle(centre, rad_offset, rad_angle)
                end_pt = geoms.point_on_line(offset_pt, diam_pt, rad_length)
                # print('***', rad_angle, offset_pt, f'{x_c=}, {y_c=}')
                cnv.draw_line((offset_pt.x, offset_pt.y), (end_pt.x, end_pt.y))
            else:
                cnv.draw_line((centre.x, centre.y), (diam_pt.x, diam_pt.y))
        self.set_canvas_props(
            cnv=cnv,
            index=ID,
            stroke=self.radii_stroke,
            stroke_width=self.radii_stroke_width,
            dashed=self.radii_dashed,
            dotted=self.radii_dotted,
        )

    def get_geometry(self, rotation: float = None, is_rotated: bool = False):
        """Calculate centre, radius, side and vertices of Polygon."""
        # convert to using units
        if is_rotated:
            x, y = 0.0, 0.0  # centre for now-rotated canvas
        else:
            centre = self.get_centre()
            x, y = centre.x, centre.y
        # calculate side
        if self.height:
            side = self._u.height / math.sqrt(3)
            half_flat = self._u.height / 2.0
        elif self.diameter:
            side = self._u.diameter / 2.0
            self._u.side = side
            half_flat = self._u.side * math.sqrt(3) / 2.0
        elif self.radius:
            side = self.u_radius
        # radius
        radius = self.get_radius()
        # calculate vertices - assumes x,y marks the centre point
        _rotation = self.flatten_angle
        vertices = geoms.polygon_vertices(self.sides, radius, Point(x, y), _rotation)
        # for p in vertices: print(f'*G* {p.x / 28.3465}, {p.y / 28.3465}')
        return PolyGeometry(x, y, radius, side, half_flat, vertices)

    def get_vertexes(self, rotation: float = None, is_rotated: bool = False):
        """Calculate vertices of polygon."""
        # convert to using units
        if is_rotated:
            x, y = 0.0, 0.0  # centre for now-rotated canvas
        else:
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
        radius = self.get_radius()
        # calculate vertices - assumes x,y marks the centre point
        _rotation = self.flatten_angle
        vertices = geoms.polygon_vertices(self.sides, radius, Point(x, y), _rotation)
        # for p in vertices: print(f'*V* {p.x / 28.3465}, {p.y / 28.3465}')
        return vertices

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a regular polygon on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- calc centre (in units)
        centre = self.get_centre()
        x, y = centre.x, centre.y
        # ---- calculate vertices
        pre_geom = self.get_geometry()
        x, y, radius, vertices = (
            pre_geom.x,
            pre_geom.y,
            pre_geom.radius,
            pre_geom.vertices,
        )
        # ---- new x/y per col/row
        is_cards = kwargs.get("is_cards", False)
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
                bl=Point(self.x_c - self._u.radius, self.y_c + self._u.radius),
                tr=Point(self.x_c + self._u.radius, self.y_c - self._u.radius),
            )
        # ---- handle rotation
        is_rotated = False
        rotation = kwargs.get("rotation", self.rotation)
        if rotation:
            self.centroid = muPoint(x, y)
            kwargs["rotation"] = rotation
            kwargs["rotation_point"] = self.centroid
            is_rotated = True
        # ---- updated geom
        # _rotation = rotation or self.flatten_angle
        # vertices = geoms.polygon_vertices(self.sides, radius, Point(x, y), _rotation)
        # ---- invalid polygon?
        if not vertices or len(vertices) == 0:
            return
        # ---- draw polygon
        # feedback(f"***Polygon {self.col=} {self.row=} {x=} {y=} {vertices=}")
        cnv.draw_polyline(vertices)
        kwargs["closed"] = True
        self.set_canvas_props(cnv=cnv, index=ID, **kwargs)
        # ---- draw radii
        if self.radii:
            self.draw_radii(cnv, ID, Point(x, y), vertices)
        # ---- draw perbis
        if self.perbis:
            self.draw_perbis(cnv, ID, Point(x, y), vertices)
        # ---- draw mesh
        if self.mesh:
            self.draw_mesh(cnv, ID, vertices)
        # ---- centred shape (with offset)
        if self.centre_shape:
            if self.can_draw_centred_shape(self.centre_shape):
                self.centre_shape.draw(
                    _abs_cx=x + self.unit(self.centre_shape_mx),
                    _abs_cy=y + self.unit(self.centre_shape_my),
                )
        # ---- debug
        self._debug(cnv, vertices=vertices)  # needs: self.run_debug = True
        # ---- dot
        self.draw_dot(cnv, x, y)
        # ---- cross
        self.draw_cross(cnv, x, y, rotation=kwargs.get("rotation"))
        # ---- text
        self.draw_heading(cnv, ID, x, y, radius, **kwargs)
        self.draw_label(cnv, ID, x, y, **kwargs)
        self.draw_title(cnv, ID, x, y, radius + 0.5 * self.title_size, **kwargs)
        # ---- set calculated top-left in user units
        self.calculated_left = (x - self._u.radius) / self.units
        self.calculated_top = (x - self._u.radius) / self.units


class PolylineShape(BaseShape):
    """
    Multi-part line on a given canvas.
    """

    def get_points(self) -> list:
        points = tools.tuple_split(self.points)
        if not points:
            points = self.points
        if not points or len(points) == 0:
            feedback("There are no points to draw the Polyline", False, True)
        return points

    def get_vertexes(self):
        """Return polyline vertices in canvas units"""
        points = self.get_points()
        vertices = [
            Point(
                self.unit(pt[0]) + self._o.delta_x, self.unit(pt[1]) + self._o.delta_y
            )
            for pt in points
        ]
        return vertices

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a polyline on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        points = self.get_points()
        # ---- set vertices
        x_sum, y_sum = 0, 0
        self.vertexes = []
        for key, vertex in enumerate(points):
            x, y = vertex
            # convert to using units
            x = self.unit(x) + self._o.delta_x
            y = self.unit(y) + self._o.delta_y
            self.vertexes.append((x, y))
        # ---- draw polyline
        # feedback(f'***PolyLineShp{x=} {y=} {self.vertexes=}')
        if points:
            cnv.draw_polyline(self.vertexes)
            kwargs["closed"] = False
            kwargs["fill"] = None
            if kwargs.get("rounded"):
                kwargs["lineJoin"] = 1
            self.set_canvas_props(cnv=cnv, index=ID, **kwargs)
        # ---- arrowhead
        if (
            self.arrow
            or self.arrow_style
            or self.arrow_position
            or self.arrow_height
            or self.arrow_width
            or self.arrow_double
        ) and points:
            _vertexes = tools.as_point(self.vertexes)
            start, end = _vertexes[-2], _vertexes[-1]
            self.draw_arrowhead(cnv, start, end, **kwargs)
            if self.arrow_double:
                start, end = _vertexes[1], _vertexes[0]
                self.draw_arrowhead(cnv, start, end, **kwargs)


class QRCodeShape(BaseShape):
    """
    QRCode drawn on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(QRCodeShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        # overrides / extra args
        _cache_directory = get_cache(**kwargs)
        self.cache_directory = Path(_cache_directory, "qrcodes")
        self.cache_directory.mkdir(parents=True, exist_ok=True)

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a QRCode on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        img = None
        # ---- check for Card usage
        cache_directory = str(self.cache_directory)
        _source = self.source
        # feedback(f'*** QRCode {ID=} {self.source=}')
        if ID is not None and isinstance(self.source, list):
            _source = self.source[ID]
        elif ID is not None and isinstance(self.source, str):
            _source = self.source
        else:
            pass
        if not _source:
            _source = Path(globals.filename).stem + ".png"
        # if no directory in _source, use qrcodes cache directory!
        if Path(_source).name:
            _source = os.path.join(cache_directory, _source)
        # feedback(f"*** QRC {self._o.delta_x=} {self._o.delta_y=}")
        if self.use_abs_c:
            x = self._abs_cx
            y = self._abs_cy
        else:
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
        self.set_canvas_props(index=ID)
        # ---- convert to using units
        height = self._u.height
        width = self._u.width
        if self.cx is not None and self.cy is not None:
            if width and height:
                x = self._u.cx - width / 2.0 + self._o.delta_x
                y = self._u.cy - height / 2.0 + self._o.delta_y
            else:
                feedback(
                    "Must supply width and height for use with cx and cy.", stop=True
                )
        else:
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- overrides for self.text / text value
        _locale = kwargs.get("locale", None)
        if _locale:
            self.text = tools.eval_template(self.text, _locale)
        _text = self.textify(ID)
        # feedback(f'*** QRC {_locale=} {self.text=} {_text=}', False)
        if _text is None or _text == "":
            feedback("No text supplied for the QRCode shape!", False, True)
            return
        _text = str(_text)  # card data could be numeric
        if "\\u" in _text:
            _text = codecs.decode(_text, "unicode_escape")
        # ---- create QR code
        qrcode = segno.make_qr(_text)
        qrcode.save(
            _source,
            scale=self.scaling or 1,
            light=tools.rgb_to_hex(tools.get_color(self.fill)),
            dark=tools.rgb_to_hex(tools.get_color(self.stroke)),
        )
        rotation = kwargs.get("rotation", self.rotation)
        # ---- load QR image
        # feedback(f'*** IMAGE {ID=} {_source=} {x=} {y=} {self.rotation=}')
        img, is_dir = self.load_image(  # via base.BaseShape
            globals.doc_page,
            _source,
            origin=(x, y),
            sliced=self.sliced,
            width_height=(width, height),
            cache_directory=cache_directory,
            rotation=rotation,
        )
        if not img and not is_dir:
            feedback(
                f'Unable to load image "{_source}!" - please check name and location',
                True,
            )
        # ---- QR shape other text
        if kwargs and kwargs.get("text"):
            kwargs.pop("text")  # otherwise labels use text!
        xc = x + width / 2.0
        yc = y + height / 2.0
        _off = self.heading_size / 2.0
        self.draw_heading(cnv, ID, xc, yc - height / 2.0 - _off, **kwargs)
        self.draw_label(cnv, ID, xc, yc + _off, **kwargs)
        self.draw_title(cnv, ID, xc, yc + height / 2.0 + _off * 3.5, **kwargs)


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
        self._u_roof_line = self.unit(self.roof_line) if self.roof_line else None
        self._u_roof_line_mx = self.unit(self.roof_line_mx) if self.roof_line_mx else 0
        self._u_roof_line_my = self.unit(self.roof_line_mx) if self.roof_line_my else 0
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

    def calculate_xy(self, **kwargs):
        # ---- adjust start
        # feedback(f'*** Rect.calc {self.col=} {self.row=} {self._u.offset_x=} {self._o.off_x=}')
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

    def draw_roof(self, cnv, ID, vertexes, rotation=0):
        """Draw triangles and trapezoids inside the Rectangle

        Args:
            ID: unique ID
            vertexes: the rectangle's nodes
            rotation: degrees anti-clockwise from horizontal "east"
        """
        # ---- get roof color list from string
        if isinstance(self.roof, str):
            _roof = tools.split(self.roof.strip())
        else:
            _roof = self.roof
        # ---- validate roof color settings
        err = ("Roof must be a list of colors - either 2 or 4",)
        if not isinstance(_roof, list):
            feedback(err, True)
        else:
            if len(_roof) not in [2, 4]:
                feedback(err, True)
        roof_colors = [tools.get_color(rcolor) for rcolor in _roof]
        # ---- draw 2 triangles
        if len(roof_colors) == 2:
            # top-left
            vertexes_tl = [vertexes[0], vertexes[1], vertexes[3]]
            cnv.draw_polyline(vertexes_tl)
            self.set_canvas_props(
                index=ID,
                stroke=self.roof_stroke or roof_colors[0],
                fill=roof_colors[0],
                closed=True,
                rotation=rotation,
                rotation_point=self.centroid,
            )
            # bottom-right
            vertexes_br = [vertexes[1], vertexes[2], vertexes[3]]
            cnv.draw_polyline(vertexes_br)
            self.set_canvas_props(
                index=ID,
                stroke=self.roof_stroke or roof_colors[1],
                fill=roof_colors[1],
                closed=True,
                rotation=rotation,
                rotation_point=self.centroid,
            )
        # ---- draw 2 triangles and (maybe) 2 trapezoids
        elif len(roof_colors) == 4:
            dx = (vertexes[3].x - vertexes[0].x) / 2.0
            dy = (vertexes[1].y - vertexes[0].y) / 2.0
            midpt = Point(vertexes[0].x + dx, vertexes[0].y + dy)
            if self.roof_line:
                _line = self._u_roof_line / 2.0
                midleft = Point(
                    midpt.x - _line + self._u_roof_line_mx,
                    midpt.y + self._u_roof_line_my,
                )
                midrite = Point(
                    midpt.x + _line + self._u_roof_line_mx,
                    midpt.y + self._u_roof_line_my,
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
                    stroke=self.roof_stroke or roof_colors[key],
                    fill=roof_colors[key],
                    closed=True,
                    rotation=rotation,
                    rotation_point=self.centroid,
                )

    def draw_hatch(self, cnv, ID, vertices: list, num: int, rotation: float = 0.0):
        """Draw line(s) from one side of Rectangle to the parallel opposite.

        Args:
            ID: unique ID
            vertices: the rectangle's nodes
            num: number of lines
            rotation: degrees anti-clockwise from horizontal "east"
        """
        _dirs = tools.validated_directions(self.hatch, DirectionGroup.CIRCULAR, "hatch")
        lines = tools.as_int(num, "hatch_count")
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
                    "No diagonal hatching permissible with rounding in the rectangle",
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
                    "No hatching permissible with this size of rounding in a rectangle",
                    True,
                )
        if self.notch and self.hatch_count > 1 or self.notch_x or self.notch_y:
            if (
                "ne" in _dirs
                or "sw" in _dirs
                or "se" in _dirs
                or "nw" in _dirs
                or "d" in _dirs
            ):
                feedback(
                    "Multi- diagonal hatching not permissible in a notched Rectangle",
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
            stroke=self.hatch_stroke,
            stroke_width=self.hatch_stroke_width,
            stroke_cap=self.hatch_cap,
            dashed=self.hatch_dashed,
            dotted=self.hatch_dots,
            rotation=rotation,
            rotation_point=muPoint(cx, cy),
        )

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
        is_borders = True if self.borders else False
        is_round = True if (self.rounding or self.rounded) else False
        if self.roof and (is_round or is_notched or is_peaks or is_chevron):
            feedback("Cannot use roof with other styles.", True)
        if is_round and is_borders:
            feedback("Cannot use rounding or rounded with borders.", True)
        if is_round and is_notched:
            feedback("Cannot use rounding or rounded with notch.", True)
        if is_round and is_chevron:
            feedback("Cannot use rounding or rounded with chevron.", True)
        if is_round and is_peaks:
            feedback("Cannot use rounding or rounded with peaks.", True)
        if self.hatch_count and is_notched and self.hatch_count > 1:
            feedback("Cannot use multiple hatches with notch.", True)
        if self.hatch_count and is_chevron:
            feedback("Cannot use hatch_count with chevron.", True)
        if is_notched and is_chevron:
            feedback("Cannot use notch and chevron together.", True)
        if is_notched and is_peaks:
            feedback("Cannot use notch and peaks together.", True)
        if is_chevron and is_peaks:
            feedback("Cannot use chevron and peaks together.", True)
        if self.hatch_count and is_peaks:
            feedback("Cannot use hatch_count and peaks together.", True)
        if is_borders and (is_chevron or is_peaks or is_notched):
            feedback("Cannot use borders with any of: hatch, peaks or chevron.", True)
        # ---- calculate properties
        x, y = self.calculate_xy()
        # feedback(f'*** RECT      {self.col=} {self.row=} {x=} {y=}')
        # ---- overrides for grid layout
        if self.use_abs_c:
            x = self._abs_cx - self._u.width / 2.0
            y = self._abs_cy - self._u.height / 2.0
        x_d = x + self._u.width / 2.0  # centre
        y_d = y + self._u.height / 2.0  # centre
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
            _notch_style = self.notch_style.lower()
            if _notch_style in ["b", "bite"]:
                feedback('The "bite" setting is not implemented yet', False)
            if self.notch_corners:
                _ntches = self.notch_corners.split()
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
                    case "bite" | "b":
                        # TODO - write code ...
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
                    case "bite" | "b":
                        # TODO - write code ...
                        pass
            else:
                self.vertexes.append(Point(x, y + self._u.height))

            if "SE" in _notches:  ##
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
                        self.vertexes.append(
                            Point(x + self._u.width, y + self._u.height)
                        )
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
                    case "bite" | "b":
                        # TODO - write code ...
                        pass
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
                    case "bite" | "b":
                        # TODO - write code ...
                        pass
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
                    case "bite" | "b":
                        # TODO - write code ...
                        pass
            else:
                self.vertexes.append(Point(x, y))

            # ---- debug
            self._debug(cnv, vertices=self.vertexes)
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
            except:
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
                f"The rounding radius cannot exceed 50% of the smallest side.", True
            )

        # ---- draw rectangle
        # feedback(f'*** RECT {self.col=} {self.row=} {x=} {y=} {radius=}')
        if is_notched or is_chevron or is_peaks:
            # feedback(f'*** RECT  vertices')
            cnv.draw_polyline(self.vertexes)
            kwargs["closed"] = True
            self.set_canvas_props(cnv=cnv, index=ID, **kwargs)
            self._debug(cnv, vertices=self.vertexes)
        else:
            # feedback(f'*** RECT  normal')   )
            cnv.draw_rect((x, y, x + self._u.width, y + self._u.height), radius=radius)
            self.set_canvas_props(cnv=cnv, index=ID, **kwargs)
            self._debug(cnv, vertices=self.vertexes)
            # ---- * borders (override)
            if self.borders:
                if isinstance(self.borders, tuple):
                    self.borders = [
                        self.borders,
                    ]
                if not isinstance(self.borders, list):
                    feedback('The "borders" property must be a list of sets or a set')
                for border in self.borders:
                    self.draw_border(cnv, border, ID)  # BaseShape

        # ---- fill pattern?
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

        # ---- draw roof after base
        if self.roof:
            self.draw_roof(cnv, ID, self.vertexes, rotation)

        # ---- draw hatch
        if self.hatch_count:
            # if 'rotation' in kwargs.keys():
            #     kwargs.pop('rotation')
            vertices = self.get_vertexes(**kwargs)
            self.draw_hatch(cnv, ID, vertices, self.hatch_count, rotation=rotation)

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
            self.set_canvas_props(cnv=None, index=ID, **gargs)

        # ---- centred shape (with offset)
        if self.centre_shape:
            if self.can_draw_centred_shape(self.centre_shape):
                self.centre_shape.draw(
                    _abs_cx=x_d + self.unit(self.centre_shape_mx),
                    _abs_cy=y_d + self.unit(self.centre_shape_my),
                )
        # ---- cross
        self.draw_cross(cnv, x_d, y_d, rotation=kwargs.get("rotation"))
        # ---- dot
        self.draw_dot(cnv, x_d, y_d)
        # ---- text
        self.draw_heading(
            cnv, ID, x_d, y_d - 0.5 * self._u.height - delta_m_up, **kwargs
        )
        self.draw_label(cnv, ID, x_d, y_d, **kwargs)
        self.draw_title(
            cnv, ID, x_d, y_d + 0.5 * self._u.height + delta_m_down, **kwargs
        )
        # ----  numbering
        self.set_coord(cnv, x_d, y_d)
        # ---- set grid property
        self.grid = GridShape(label=self.coord_text, x=x_d, y=y_d, shape=self)
        # ---- set calculated top-left in user units
        self.calculated_left, self.calculated_top = x / self.units, y / self.units


class RhombusShape(BaseShape):
    """
    Rhombus on a given canvas.
    """

    def get_vertexes(self, **kwargs):
        """Calculate vertices of rhombus."""
        x, y = kwargs.get("x"), kwargs.get("y")
        # ---- overrides for grid layout
        if self.use_abs_c:
            x = self._abs_cx - self._u.width / 2.0
            y = self._abs_cy - self._u.height / 2.0
        x_s, y_s = x, y + self._u.height / 2.0
        vertices = []
        vertices.append(Point(x_s, y_s))
        vertices.append(Point(x_s + self._u.width / 2.0, y_s + self._u.height / 2.0))
        vertices.append(Point(x_s + self._u.width, y_s))
        vertices.append(Point(x_s + self._u.width / 2.0, y_s - self._u.height / 2.0))
        return vertices

    def draw_hatch(
        self,
        cnv,
        ID,
        x_c: float,
        y_c: float,
        side: float,
        vertices: list,
        num: int,
        rotation: float = 0.0,
    ):
        """Draw lines connecting two opposite sides and parallel to adjacent sides.

        Args:
            ID: unique ID
            x_c, yc: centre of rhombus
            side: length of rhombus edge
            vertices: the rhombus's nodes
            num: number of lines
            rotation: degrees anti-clockwise from horizontal "east"
        """
        _dirs = tools.validated_directions(
            self.hatch, DirectionGroup.CIRCULAR, "rhombus hatch"
        )
        _num = tools.as_int(num, "hatch_count")
        lines = int((_num - 1) / 2 + 1)
        # feedback(f'*** RHOMB {num=} {lines=} {vertices=} {_dirs=} {side=}')
        if num >= 1:
            if any(item in _dirs for item in ["e", "w", "o"]):
                cnv.draw_line(vertices[0], vertices[2])
            if any(item in _dirs for item in ["n", "s", "o"]):  # vertical
                cnv.draw_line(vertices[1], vertices[3])
        if num >= 3:
            _lines = lines - 1
            if any(item in _dirs for item in ["ne", "sw", "d"]):
                self.draw_lines_between_sides(cnv, side, _num, vertices, (1, 0), (2, 3))
            if any(item in _dirs for item in ["se", "nw", "d"]):
                self.draw_lines_between_sides(cnv, side, _num, vertices, (0, 3), (1, 2))
            if any(item in _dirs for item in ["s", "n", "o"]):
                self.draw_lines_between_sides(
                    cnv, side, _lines, vertices, (0, 3), (0, 1)
                )
                self.draw_lines_between_sides(
                    cnv, side, _lines, vertices, (3, 2), (1, 2)
                )
            if any(item in _dirs for item in ["e", "w", "o"]):
                self.draw_lines_between_sides(
                    cnv, side, _lines, vertices, (0, 3), (2, 3)
                )
                self.draw_lines_between_sides(
                    cnv, side, _lines, vertices, (1, 0), (1, 2)
                )

        # ---- set canvas
        self.set_canvas_props(
            index=ID,
            stroke=self.hatch_stroke,
            stroke_width=self.hatch_stroke_width,
            stroke_cap=self.hatch_cap,
            dashed=self.hatch_dashed,
            dotted=self.hatch_dots,
            rotation=rotation,
            rotation_point=muPoint(x_c, y_c),
        )

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a rhombus (diamond) on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        if self.use_abs_c:
            x = self._abs_cx
            y = self._abs_cy
        elif self.cx is not None and self.cy is not None:
            x = self._u.cx - self._u.width / 2.0 + self._o.delta_x
            y = self._u.cy - self._u.height / 2.0 + self._o.delta_y
        elif self.use_abs:
            x = self._abs_x
            y = self._abs_y
        else:
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
        cx = x + self._u.width / 2.0
        cy = y + self._u.height / 2.0
        # ---- calculated properties
        self.area = (self._u.width * self._u.height) / 2.0
        # ---- handle rotation
        rotation = kwargs.get("rotation", self.rotation)
        if rotation:
            self.centroid = muPoint(cx, cy)
            kwargs["rotation"] = rotation
            kwargs["rotation_point"] = self.centroid
        # ---- draw rhombus
        self.vertexes = self.get_vertexes(cx=cx, cy=cy, x=x, y=y)
        # feedback(f'***Rhombus {x=} {y=} {self.vertexes=}')
        cnv.draw_polyline(self.vertexes)
        kwargs["closed"] = True
        self.set_canvas_props(cnv=cnv, index=ID, **kwargs)
        # ---- draw hatch
        if self.hatch_count:
            self.side = math.sqrt(
                (self._u.width / 2.0) ** 2 + (self._u.height / 2.0) ** 2
            )
            self.draw_hatch(
                cnv, ID, cx, cy, self.side, self.vertexes, self.hatch_count, rotation
            )
        # ---- borders (override)
        if self.borders:
            if isinstance(self.borders, tuple):
                self.borders = [
                    self.borders,
                ]
            if not isinstance(self.borders, list):
                feedback('The "borders" property must be a list of sets or a set')
            for border in self.borders:
                self.draw_border(cnv, border, ID)  # BaseShape
        # ---- dot
        self.draw_dot(cnv, x + self._u.width / 2.0, y + self._u.height / 2.0)
        # ---- cross
        self.draw_cross(
            cnv,
            x + self._u.width / 2.0,
            y + self._u.height / 2.0,
            rotation=kwargs.get("rotation"),
        )
        # ---- text
        y_off = self._u.height / 2.0
        self.draw_heading(cnv, ID, x + self._u.width / 2.0, cy - y_off, **kwargs)
        self.draw_label(cnv, ID, x + self._u.width / 2.0, cy, **kwargs)
        self.draw_title(cnv, ID, x + self._u.width / 2.0, cy + y_off, **kwargs)


class RightAngledTriangleShape(BaseShape):
    """
    Right-angled Triangle on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # set sizes
        if self.height and not self.width:
            self._u.width = self._u.height
        if self.width and not self.height:
            self._u.height = self._u.width
        # calc directions
        x, y = self._u.x, self._u.y
        self.flip = kwargs.get("flip", "north") or "north"
        self.hand = kwargs.get("hand", "east") or "east"
        if not self.hand or not self.flip:
            feedback(
                'Need to supply both "flip" and "hand" options! for triangle.',
                stop=True,
            )
        hand = str(self.hand).lower()
        flip = str(self.flip).lower()
        if hand == "west" or hand == "w":
            x2 = x - self._u.width
        elif hand == "east" or hand == "e":
            x2 = x + self._u.width
        else:
            feedback(f'The value "{hand}" for hand is invalid (use east or west)', True)
        if flip == "north":
            y2 = y + self._u.height
        elif flip == "south":
            y2 = y - self._u.height
        else:
            feedback(
                f'The value "{flip}" for flip is invalid (use north or south)', True
            )
        # calculate points
        self._vertexes = []
        self._vertexes.append(Point(x, y))
        self._vertexes.append(Point(x2, y2))
        self._vertexes.append(Point(x2, y))
        # ---- set vertices
        self.vertexes = []
        x_sum, y_sum = 0, 0
        for key, vertex in enumerate(self._vertexes):
            # shift to relative position
            x = vertex.x + self._o.delta_x
            y = vertex.y + self._o.delta_y
            x_sum += x
            y_sum += y
            self.vertexes.append((x, y))
        # ---- draw RightAngledTriangle
        # feedback(f'***RAT {x=} {y=} {self.vertexes=}')
        cnv.draw_polyline(self.vertexes)
        kwargs["closed"] = True
        self.set_canvas_props(cnv=cnv, index=ID, **kwargs)
        # ---- centre
        x_c, y_c = x_sum / 3.0, y_sum / 3.0  # centroid
        # ---- dot
        self.draw_dot(cnv, x_c, y_c)
        # ---- text
        self.draw_label(cnv, ID, x_c, y_c, **kwargs)


class SectorShape(BaseShape):
    """
    Sector on a given canvas. Aka "wedge". Aka "slice" or "pie slice".

    Note:
        * User supplies a "compass" angle i.e. degrees anti-clockwise from East;
          which determines the "width" of the sector at the circumference;
          default is 90°
        * User also supplies a start angle; where 0 corresponds to East,
          which determines the second point on the circumference;
          default is 0°
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(SectorShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        self.kwargs = kwargs
        # ---- perform overrides
        self.radius = self.radius or self.diameter / 2.0
        if self.cx is None and self.x is None:
            feedback("Either provide x or cx for Sector", True)
        if self.cy is None and self.y is None:
            feedback("Either provide y or cy for Sector", True)
        if self.cx is not None and self.cy is not None:
            self.x = self.cx - self.radius
            self.y = self.cy - self.radius
        # feedback(f'***Sector {self.cx=} {self.cy=} {self.x=} {self.y=}')
        # ---- calculate centre
        radius = self._u.radius
        if self.row is not None and self.col is not None:
            self.x_c = self.col * 2.0 * radius + radius
            self.y_c = self.row * 2.0 * radius + radius
            # log.debug(f"{self.col=}, {self.row=}, {self.x_c=}, {self.y_c=}")
        elif self.cx is not None and self.cy is not None:
            self.x_c = self._u.cx
            self.y_c = self._u.cy
        else:
            self.x_c = self._u.x + radius
            self.y_c = self._u.y + radius
        # feedback(f'***Sector {self.x_c=} {self.y_c=} {self.radius=}')

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw sector on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        if self.use_abs_c:
            self.x_c = self._abs_cx
            self.y_c = self._abs_cy
        # ---- centre point in units
        p_C = Point(self.x_c + self._o.delta_x, self.y_c + self._o.delta_y)
        # ---- circumference point in units
        p_P = geoms.point_on_circle(p_C, self._u.radius, self.angle_start)
        # ---- draw sector
        # feedback(
        #     f'***Sector: {p_P=} {p_C=} {self.angle_start=} {self.angle_width=}')
        cnv.draw_sector(  # anti-clockwise from p_P; 90° default
            (p_C.x, p_C.y), (p_P.x, p_P.y), self.angle_width, fullSector=True
        )
        kwargs["closed"] = False
        self.set_canvas_props(cnv=cnv, index=ID, **kwargs)


class ShapeShape(BaseShape):
    """
    Irregular polygon, based on a set of points, on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(ShapeShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        # overrides
        self.x = kwargs.get("x", kwargs.get("left", 0))
        self.y = kwargs.get("y", kwargs.get("bottom", 0))

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw an irregular polygon on a given canvas."""
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- draw Shape
        if isinstance(self.points, str):
            # SPLIT STRING e.g. "1,2  3,4  4.5,8.8"
            _points = self.points.split(" ")
            points = [_point.split(",") for _point in _points]
        else:
            points = self.points
        if points and len(points) > 0:
            x_offset, y_offset = self.unit(self.x or 0), self.unit(self.y or 0)
            # ---- set vertices
            x_sum, y_sum = 0, 0
            self.vertexes = []
            for key, vertex in enumerate(points):
                _x0, _y0 = float(vertex[0]), float(vertex[1])
                # convert to using units
                x = self.unit(_x0) + self._o.delta_x + x_offset
                y = self.unit(_y0) + self._o.delta_y + y_offset
                self.vertexes.append((x, y))
            # feedback(f'***RAT {x=} {y=} {self.vertexes=}')
            cnv.draw_polyline(self.vertexes)
            kwargs["closed"] = True
            self.set_canvas_props(cnv=cnv, index=ID, **kwargs)
            # ---- centre?
            if self.cx and self.cy:
                x = self._u.cx + self._o.delta_x + x_offset
                y = self._u.cy + self._o.delta_y + y_offset
                # ---- * dot
                self.draw_dot(cnv, x, y)
                # ---- * cross
                self.draw_cross(cnv, x, y, rotation=kwargs.get("rotation"))
                # ---- * text
                self.draw_label(cnv, ID, x, y, **kwargs)
        else:
            feedback("There are no points to draw the Polyshape", False, True)


class SquareShape(RectangleShape):
    """
    Square on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(SquareShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        # overrides to make a "square rectangle"
        if self.width and not self.side:
            self.side = self.width
        if self.height and not self.side:
            self.side = self.height
        self.height, self.width = self.side, self.side
        self.set_unit_properties()
        self.kwargs = kwargs

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
        """Draw a square on a given canvas."""
        # feedback(f'@Square@ {self.label=} // {off_x=}, {off_y=} {kwargs=}')
        return super().draw(cnv, off_x, off_y, ID, **kwargs)


class StadiumShape(BaseShape):
    """
    Stadium ("pill") on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(StadiumShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        self.kwargs = kwargs
        # overrides to centre shape
        if self.cx is not None and self.cy is not None:
            self.x = self.cx - self.width / 2.0
            self.y = self.cy - self.height / 2.0
            # feedback(f"*** INIT OldX:{x} OldY:{y} NewX:{self.x} NewY:{self.y}")
        self.kwargs = kwargs

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a stadium on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        if "fill" in kwargs.keys():
            if kwargs.get("fill") is None:
                feedback("Cannot have no fill for a Stadium!", True)
        # ---- adjust start
        if self.row is not None and self.col is not None:
            x = self.col * self._u.width + self._o.delta_x
            y = self.row * self._u.height + self._o.delta_y
        elif self.cx is not None and self.cy is not None:
            x = self._u.cx - self._u.width / 2.0 + self._o.delta_x
            y = self._u.cy - self._u.height / 2.0 + self._o.delta_y
        else:
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
        # ---- calculate centre of the shape
        cx = x + self._u.width / 2.0
        cy = y + self._u.height / 2.0
        # ---- overrides for grid layout
        if self._abs_cx is not None and self._abs_cy is not None:
            cx = self._abs_cx
            cy = self._abs_cy
            x = cx - self._u.width / 2.0
            y = cy - self._u.height / 2.0
        # ---- handle rotation
        rotation = kwargs.get("rotation", self.rotation)
        if rotation:
            self.centroid = muPoint(cx, cy)
            kwargs["rotation"] = rotation
            kwargs["rotation_point"] = self.centroid
        # ---- vertices
        self.vertexes = [  # clockwise from top-left; relative to centre
            Point(x, y),
            Point(x, y + self._u.height),
            Point(x + self._u.width, y + self._u.height),
            Point(x + self._u.width, y),
        ]
        # feedback(f'*** Stad{len(self.vertexes)=}')
        # ---- edges
        _edges = tools.validated_directions(
            self.edges, DirectionGroup.CARDINAL, "stadium edges"
        )  # need curves on these edges
        self.vertexes.append(self.vertexes[0])

        # ---- draw rect fill only
        # feedback(f'***Stadium:Rect {x=} {y=} {self.vertexes=}')
        keys = copy.copy(kwargs)
        keys["stroke"] = None
        cnv.draw_polyline(self.vertexes)
        self.set_canvas_props(cnv=cnv, index=ID, **keys)

        # ---- draw stadium - lines or curves
        radius_lr = self._u.height / 2.0
        radius_tb = self._u.width / 2.0

        for key, vertex in enumerate(self.vertexes):
            if key + 1 == len(self.vertexes):
                continue
            if key == 0 and "w" in _edges:
                midpt = geoms.fraction_along_line(vertex, self.vertexes[1], 0.5)
                cnv.draw_sector(
                    (midpt.x, midpt.y),
                    (self.vertexes[1].x, self.vertexes[1].y),
                    -180.0,
                    fullSector=False,
                )
            elif key == 2 and "e" in _edges:
                midpt = geoms.fraction_along_line(vertex, self.vertexes[3], 0.5)
                cnv.draw_sector(
                    (midpt.x, midpt.y),
                    (self.vertexes[3].x, self.vertexes[3].y),
                    -180.0,
                    fullSector=False,
                )
            elif key == 1 and "s" in _edges:
                midpt = geoms.fraction_along_line(vertex, self.vertexes[2], 0.5)
                cnv.draw_sector(
                    (midpt.x, midpt.y),
                    (self.vertexes[2].x, self.vertexes[2].y),
                    -180.0,
                    fullSector=False,
                )
            elif key == 3 and "n" in _edges:
                midpt = geoms.fraction_along_line(vertex, self.vertexes[0], 0.5)
                # TEST ONLY cnv.draw_circle((midpt.x, midpt.y), 1)
                cnv.draw_sector(
                    (midpt.x, midpt.y),
                    (self.vertexes[3].x, self.vertexes[3].y),
                    180.0,
                    fullSector=False,
                )
            else:
                vertex1 = self.vertexes[key + 1]
                cnv.draw_line((vertex.x, vertex.y), (vertex1.x, vertex1.y))

        kwargs["closed"] = False
        self.set_canvas_props(cnv=cnv, index=ID, **kwargs)

        # ---- cross
        self.draw_cross(
            cnv,
            x + self._u.width / 2.0,
            y + self._u.height / 2.0,
            rotation=kwargs.get("rotation"),
        )
        # ---- dot
        self.draw_dot(cnv, x + self._u.width / 2.0, y + self._u.height / 2.0)
        # ---- text
        delta = radius_tb if "n" in _edges or "north" in _edges else 0.0
        self.draw_heading(
            cnv,
            ID,
            x + self._u.width / 2.0,
            cy - self._u.height / 2.0 - delta,
            **kwargs,
        )
        self.draw_label(
            cnv, ID, x + self._u.width / 2.0, y + self._u.height / 2.0, **kwargs
        )
        self.draw_title(
            cnv,
            ID,
            x + self._u.width / 2.0,
            cy + self._u.height / 2.0 + delta,
            **kwargs,
        )


class StarShape(BaseShape):
    """
    Star on a given canvas.
    """

    def get_vertexes(self, x, y, **kwargs):
        """Calculate vertices of star"""
        vertices = []
        radius = self._u.radius
        vertices.append(muPoint(x, y + radius))
        angle = (2 * math.pi) * 2.0 / 5.0
        start_angle = math.pi / 2.0
        log.debug("Start # self.vertices:%s", self.vertices)
        for vertex in range(self.vertices - 1):
            next_angle = angle * (vertex + 1) + start_angle
            x_1 = x + radius * math.cos(next_angle)
            y_1 = y + radius * math.sin(next_angle)
            vertices.append(muPoint(x_1, y_1))
        return vertices

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a star on a given canvas."""
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        # convert to using units
        x = self._u.x + self._o.delta_x
        y = self._u.y + self._o.delta_y
        # ---- overrides to centre the shape
        if self.use_abs_c:
            x = self._abs_cx
            y = self._abs_cy
        elif self.cx is not None and self.cy is not None:
            x = self._u.cx + self._o.delta_x
            y = self._u.cy + self._o.delta_y
        # calc - assumes x and y are the centre!
        radius = self._u.radius
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- handle rotation
        rotation = kwargs.get("rotation", self.rotation)
        if rotation:
            self.centroid = muPoint(x, y)
            kwargs["rotation"] = rotation
            kwargs["rotation_point"] = self.centroid
        # ---- draw star
        # feedback(f'***Star {x=} {y=} {self.vertexes_list=}')
        self.vertexes_list = self.get_vertexes(x, y)
        cnv.draw_polyline(self.vertexes_list)
        kwargs["closed"] = True
        self.set_canvas_props(cnv=cnv, index=ID, **kwargs)
        # ---- dot
        self.draw_dot(cnv, x, y)
        # ---- cross
        self.draw_cross(cnv, x, y, rotation=kwargs.get("rotation"))
        # ---- text
        self.draw_heading(cnv, ID, x, y - radius, **kwargs)
        self.draw_label(cnv, ID, x, y, **kwargs)
        self.draw_title(cnv, ID, x, y + radius, **kwargs)


class StarFieldShape(BaseShape):
    """
    StarField pattern on a given canvas.

    A StarField is specified by the following properties:

     * density (average number of stars per square unit; default is 10)
     * colors (list of individual star colors; default is [white])
     * enclosure (regular shape inside which its drawn; default is a rectangle)
     * sizes (list of individual star sizes; default is [0.1])
     * star_pattern (random | cluster) - NOT YET IMPLEMENTED
     * seeding (float, that if set, predetermines the randomisation sequence)

    Ref:
        https://codeboje.de/starfields-and-galaxies-python/

    TODO:
        Implement : createElipticStarfield()
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(StarFieldShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        self.kwargs = kwargs
        # override to set the randomisation sequence
        if self.seeding:
            self.seed = tools.as_float(self.seeding, "seeding")
        else:
            self.seed = None

    def draw_star(self, cnv, position: Point):
        """Draw a single star at a Point (x,y)."""
        color = self.colors[random.randint(0, len(self.colors) - 1)]
        size = self.sizes[random.randint(0, len(self.sizes) - 1)]
        # feedback(f'*** StarFld {color=} {size=} {position=}')
        cnv.draw_circle((position.x, position.y), size)
        self.set_canvas_props(cnv=cnv, index=None, stroke=color, fill=color)

    def cluster_stars(self, cnv):
        feedback("CLUSTER NOT IMPLEMENTED", True)
        for star in range(0, self.star_count):
            pass

    def random_stars(self, cnv):
        # feedback(f'*** StarFld {self.enclosure=}')
        if isinstance(self.enclosure, CircleShape):
            x_c, y_c = self.enclosure.calculate_centre()
        if isinstance(self.enclosure, PolygonShape):
            _geom = self.enclosure.get_geometry()
            x_c, y_c, radius, vertices = _geom.x, _geom.y, _geom.radius, _geom.vertices
        stars = 0
        if self.seed:
            random.seed(self.seed)
        while stars < self.star_count:
            if isinstance(self.enclosure, RectangleShape):
                x_y = Point(
                    random.random() * self.enclosure._u.width + self._o.delta_x,
                    random.random() * self.enclosure._u.height + self._o.delta_y,
                )
            elif isinstance(self.enclosure, CircleShape):
                r_fraction = random.random() * self.enclosure._u.radius
                angle = math.radians(random.random() * 360.0)
                x = r_fraction * math.cos(angle) + x_c
                y = r_fraction * math.sin(angle) + y_c
                x_y = Point(x, y)
            elif isinstance(self.enclosure, PolygonShape):
                r_fraction = random.random() * radius
                angle = math.radians(random.random() * 360.0)
                x = r_fraction * math.cos(angle) + x_c
                y = r_fraction * math.sin(angle) + y_c
                x_y = Point(x, y)
                if not geoms.point_in_polygon(x_y, vertices):
                    continue
            else:
                feedback(f"{self.enclosure} IS NOT AN IMPLEMENTED SHAPE!", True)
            self.draw_star(cnv, x_y)
            stars += 1

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw StarField pattern on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- settings
        if self.enclosure is None:
            self.enclosure = RectangleShape()
        # ---- calculations
        random.seed()
        area = math.sqrt(self.enclosure.calculate_area())
        self.star_count = round(self.density * self.points_to_value(area))
        # feedback(f'*** StarFld {self.star_pattern =} {self.enclosure}')
        # feedback(f'*** StarFld {area=} {self.density=} {self.star_count=}')
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- draw starfield
        if self.star_pattern in ["r", "random"]:
            self.random_stars(cnv)
        if self.star_pattern in ["c", "cluster"]:
            self.cluster_stars(cnv)


class TextShape(BaseShape):
    """
    Text on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(TextShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        """do something when I'm called"""
        log.debug("calling TextShape...")

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw text on a given canvas.

        Note:
            Any text in a Template should already have been rendered by
            base.handle_custom_values()
        """
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- convert to using units
        x_t = self._u.x + self._o.delta_x
        y_t = self._u.y + self._o.delta_y
        # ---- position the shape
        if self.use_abs:
            x_t = self._abs_x
            y_t = self._abs_y
        if self.height:
            height = self._u.height
        if self.width:
            width = self._u.width
        rotation = kwargs.get("rotation", self.rotation)
        # TODO => text rotation
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- overrides for self.text / text value
        _locale = kwargs.get("locale", None)
        if _locale:
            self.text = tools.eval_template(self.text, _locale)
        _text = self.textify(ID)
        # feedback(f'*** Text {ID=} {_locale=} {self.text=} {_text=}', False)
        if _text is None or _text == "":
            feedback("No text supplied for the Text shape!", False, True)
            return
        _text = str(_text)  # card data could be numeric
        if "\\u" in _text:
            _text = codecs.decode(_text, "unicode_escape")
        # ---- validations
        if self.transform is not None:
            _trans = str(self.transform).lower()
            if _trans in ["u", "up", "upper", "uppercase"]:
                _text = _text.upper()
            elif _trans in ["l", "low", "lower", "lowercase"]:
                _text = _text.lower()
            elif _trans in [
                "c",
                "capitalise",
                "capitalize",
                "t",
                "title",
                "titlecase",
                "titlelise",
                "titlelize",
            ]:
                _text = _text.title()
            else:
                feedback(f"The transform {self.transform} is unknown.", False, True)
        # ---- rectangle for text
        current_page = globals.doc_page
        rect = muRect(x_t, y_t, x_t + width, y_t + height)
        if (
            self.block_stroke
            or self.block_fill
            or self.block_dashed
            or self.block_dotted
        ):
            rkwargs = copy.copy(kwargs)
            rkwargs["fill"] = self.block_fill
            rkwargs["stroke"] = self.block_stroke
            rkwargs["stroke_width"] = self.block_stroke_width or self.stroke_width
            rkwargs["dashed"] = self.block_dashed
            rkwargs["dotted"] = self.block_dotted
            rkwargs["transparency"] = self.block_transparency
            pymu_props = tools.get_pymupdf_props(**rkwargs)
            globals.doc_page.draw_rect(
                rect,
                width=pymu_props.width,
                color=pymu_props.color,
                fill=pymu_props.fill,
                lineCap=pymu_props.lineCap,
                lineJoin=pymu_props.lineJoin,
                dashes=pymu_props.dashes,
                fill_opacity=pymu_props.fill_opacity,
            )
            # self.set_canvas_props(cnv=cnv, index=ID, **rkwargs)
        # ---- BOX text
        if self.wrap:
            # insert_textbox(
            #     rect, buffer, *, fontsize=11, fontname='helv', fontfile=None,
            #     set_simple=False, encoding=TEXT_ENCODING_LATIN, color=None, fill=None,
            #     render_mode=0, miter_limit=1, border_width=1, expandtabs=8,
            #     align=TEXT_ALIGN_LEFT, rotate=0, lineheight=None, morph=None,
            #     stroke_opacity=1, fill_opacity=1, oc=0)
            # ---- rotation
            if self.rotation is None or self.rotation == 0:
                text_rotation = 0
            else:
                text_rotation = self.rotation // 90 * 90  # multiple of 90 for HTML/Box
            # ---- text styles - htmlbox & textbox
            # https://pymupdf.readthedocs.io/en/latest/page.html#Page.insert_htmlbox
            # https://pymupdf.readthedocs.io/en/latest/shape.html#Shape.insert_textbox
            try:
                keys = self.text_properties(string=_text, **kwargs)
                keys["rotate"] = text_rotation
                # feedback(f'*** Text WRAP {kwargs=} \n=> {keys=} \n=> {rect=} \n=>{_text=}')
                if self.run_debug:
                    globals.doc_page.draw_rect(
                        rect, color=self.debug_color, dashes="[1 2] 0"
                    )
                current_page.insert_textbox(rect, _text, **keys)
            except ValueError as err:
                feedback(f"Cannot create Text! - {err}", True)
            except IOError as err:
                _err = str(err)
                cause, thefile = "", ""
                if "caused exception" in _err:
                    cause = _err.split("caused exception")[0].strip("\n").strip(" ")
                    cause = f" in {cause}"
                if "Cannot open resource" in _err:
                    thefile = _err.split("Cannot open resource")[1].strip("\n")
                    thefile = f" - unable to open or find {thefile}"
                msg = f"Cannot create Text{thefile}{cause}"
                feedback(msg, True, True)
        # ---- HTML text
        elif self.html or self.css:
            # insert_htmlbox(rect, text, *, css=None, scale_low=0,
            #   archive=None, rotate=0, oc=0, opacity=1, overlay=True)
            keys = {}
            try:
                keys["opacity"] = tools.get_opacity(self.transparency)
                if self.css:
                    keys["css"] = globals.css + " * {%s}" % self.css
                else:
                    if globals.css:
                        keys["css"] = globals.css
                keys["archive"] = globals.archive
                # feedback(f'*** Text HTML {keys=} {rect=} {_text=} {keys=}')
                if self.run_debug:
                    globals.doc_page.draw_rect(
                        rect, color=self.debug_color, dashes="[1 2] 0"
                    )
                current_page.insert_htmlbox(rect, _text, **keys)
            except ValueError as err:
                feedback(f"Cannot create Text - {err}", True)
        # ---- text string
        else:
            keys = {}
            keys["rotation"] = self.rotation
            # feedback(f"*** Text PLAIN {x_t=} {y_t=} {_text=} {keys=}")
            self.draw_multi_string(cnv, x_t, y_t, _text, **keys)  # use morph to rotate


class TrapezoidShape(BaseShape):
    """
    Trapezoid on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        """."""
        super(TrapezoidShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        self.kwargs = kwargs
        if self.top >= self.width:
            feedback("The top cannot be longer than the width!", True)
        self.delta_width = self._u.width - self._u.top
        # overrides to centre shape
        if self.cx is not None and self.cy is not None:
            self.x = self.cx - self.width / 2.0
            self.y = self.cy - self.height / 2.0
        self.kwargs = kwargs

    def calculate_area(self):
        """Calculate area of trapezoid."""
        return self._u.top * self._u.height + 2.0 * self.delta_width * self._u.height

    def calculate_perimeter(self, units: bool = False) -> float:
        """Total length of bounding perimeter."""
        length = (
            2.0 * math.sqrt(self.delta_width + self._u.height)
            + self._u.top
            + self._u.width
        )
        if units:
            return self.points_to_value(length)
        else:
            return length

    def calculate_xy(self):
        # ---- adjust start
        if self.cx is not None and self.cy is not None:
            x = self._u.cx - self._u.width / 2.0 + self._o.delta_x
            y = self._u.cy - self._u.height / 2.0 + self._o.delta_y
        elif self.use_abs:
            x = self._abs_x
            y = self._abs_y
        else:
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
        # ---- overrides for grid layout
        if self.use_abs_c:
            cx = self._abs_cx
            cy = self._abs_cy
            x = cx - self._u.width / 2.0
            y = cy - self._u.height / 2.0
        else:
            cx = x + self._u.width / 2.0
            cy = y + self._u.height / 2.0
        if self.flip:
            if str(self.flip).lower() in ["s", "south"]:
                y = y + self._u.height
                cy = y - self._u.height / 2.0
        if self.cx is not None and self.cy is not None:
            return self._u.cx, self._u.cy, x, y
        else:
            return cx, cy, x, y

    def get_vertexes(self, **kwargs):
        """Calculate vertices of trapezoid."""
        # set start
        _cx, _cy, _x, _y = self.calculate_xy()  # for direct call without draw()
        cx = kwargs.get("cx", _cx)
        cy = kwargs.get("cy", _cy)
        x = kwargs.get("x", _x)
        y = kwargs.get("y", _y)
        # build array
        sign = 1
        if self.flip and str(self.flip).lower() in ["s", "south"]:
            sign = -1
        self.delta_width = self._u.width - self._u.top
        vertices = []
        vertices.append(Point(x, y))
        vertices.append(Point(x + 0.5 * self.delta_width, y + sign * self._u.height))
        vertices.append(
            Point(x + 0.5 * self.delta_width + self._u.top, y + sign * self._u.height)
        )
        vertices.append(Point(x + self._u.width, y))
        return vertices

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a trapezoid on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- set canvas
        self.set_canvas_props(index=ID)
        cx, cy, x, y = self.calculate_xy()
        # ---- handle rotation
        rotation = kwargs.get("rotation", self.rotation)
        if rotation:
            self.centroid = muPoint(cx, cy)
            kwargs["rotation"] = rotation
            kwargs["rotation_point"] = self.centroid
        # ---- draw trapezoid
        self.vertexes = self.get_vertexes(cx=cx, cy=cy, x=x, y=y)
        # feedback(f'***Trap {x=} {y=} {self.vertexes=}')
        cnv.draw_polyline(self.vertexes)
        kwargs["closed"] = True
        self.set_canvas_props(cnv=cnv, index=ID, **kwargs)
        sign = 1
        if self.flip and str(self.flip).lower() in ["s", "south"]:
            sign = -1
        # ---- borders (override)
        if self.borders:
            if isinstance(self.borders, tuple):
                self.borders = [
                    self.borders,
                ]
            if not isinstance(self.borders, list):
                feedback('The "borders" property must be a list of sets or a set')
            for border in self.borders:
                self.draw_border(cnv, border, ID)  # BaseShape
        # ---- dot
        self.draw_dot(cnv, x + self._u.width / 2.0, y + sign * self._u.height / 2.0)
        # ---- cross
        self.draw_cross(
            cnv,
            x + self._u.width / 2.0,
            y + sign * self._u.height / 2.0,
            rotation=kwargs.get("rotation"),
        )
        # ---- text
        self.draw_heading(cnv, ID, x + self._u.width / 2.0, y, **kwargs)
        self.draw_label(
            cnv, ID, x + self._u.width / 2.0, y + sign * self._u.height / 2.0, **kwargs
        )
        self.draw_title(
            cnv, ID, x + self._u.width / 2.0, y + sign * self._u.height, **kwargs
        )


# ---- Other


class CommonShape(BaseShape):
    """
    Attributes common to, or used by, multiple shapes
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(CommonShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        self._kwargs = kwargs

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Not applicable."""
        feedback("The Common shape cannot be drawn.", True)


class FooterShape(BaseShape):
    """
    Footer for a page.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(FooterShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        self.kwargs = kwargs
        # self.page_width = kwargs.get('paper', (canvas.width, canvas.height))[0]

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw footer on a given canvas page."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        # super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        font_size = kwargs.get("font_size", self.font_size)
        # ---- set location and text
        x = self.kwargs.get("x", self._u.page_width / 2.0)  # centre across page
        y = self.unit(self.margin_bottom) / 2.0  # centre in margin
        text = kwargs.get("text") or "Page %s" % ID
        # feedback(f'*** FooterShape {ID=} {text=} {x=} {y=} {font_size=}')
        # ---- draw footer
        self.draw_multi_string(cnv, x, y, text, align="centre", font_size=font_size)
