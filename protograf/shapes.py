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
from reportlab.platypus import Paragraph
from reportlab.lib.colors import red, green, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import (
    A8,
    A7,
    A6,
    A5,
    A4,
    A3,
    A2,
    A1,
    A0,
    LETTER,
    LEGAL,
    ELEVENSEVENTEEN,
    letter,
    legal,
    elevenSeventeen,
    B6,
    B5,
    B4,
    B3,
    B2,
    B0,
    landscape,
)
from reportlab.lib.utils import ImageReader
import segno  # QRCode

# local
from protograf.utils.geoms import Point, Link, Locale, PolyGeometry  # named tuples
from protograf.utils import geoms, tools, support
from protograf.base import (
    BaseShape,
    BaseCanvas,
    GridShape,
    UNITS,
    COLORS,
    PAGES,
    DEBUG_COLOR,
    CACHE_DIRECTORY,
    BGG_IMAGES,
)

log = logging.getLogger(__name__)

DEBUG = False
GRID_SHAPES_WITH_CENTRE = [
    "CircleShape",
    "CompassShape",
    "DotShape",
    "HexShape",
    "PolygonShape",
    "RectangleShape",
    "RhombusShape",
    "SquareShape",
    "StadiumShape",
    "EllipseShape",
    "StarShape",
]
GRID_SHAPES_NO_CENTRE = [
    "TextShape",
]
# NOT GRID:  ArcShape, BezierShape, PolylineShape, ChordShape

# following shapes must have vertices accessible WITHOUT calling draw()
SHAPES_FOR_TRACK = [
    "LineShape",
    "PolygonShape",
    "PolylineShape",
    "RectangleShape",
    "RhombusShape",
    "SquareShape",
]


def get_cache(**kwargs):
    """Get and/or set a cache directory for to save file images."""
    default_cache = Path(Path.home(), CACHE_DIRECTORY, "images")
    default_cache.mkdir(parents=True, exist_ok=True)
    cache_directory = kwargs.get("cache_directory", str(default_cache))
    if not os.path.exists(cache_directory):
        tools.feedback(
            "Unable to create or find the cache directory:" f" {str(cache_directory)}",
            True,
        )
    return cache_directory


def set_cached_dir(source):
    """Set special cached directory, depending on source being a URL."""
    if not tools.is_url_valid(url=source):
        return None
    loc = urlparse(source)
    # print('@http@',  loc)
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
        cnv = cnv.canvas if cnv else self.canvas.canvas
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        img = None
        # ---- check for Card usage
        cache_directory = str(self.cache_directory)
        _source = self.source
        # tools.feedback(f'*** IMAGE {ID=} {self.source=}')
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
                tools.feedback(
                    "Must supply width and height for use with cx and cy.", stop=True
                )
        else:
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
        # ---- load image
        # tools.feedback(f'*** IMAGE {ID=} {_source=} {x=} {y=} {self.scaling=}')
        img, is_svg, is_dir = self.load_image(  # via BaseShape (in base.py)
            _source,
            scaling=self.scaling,
            sliced=self.sliced,
            width_height=(width, height),
            cache_directory=cache_directory,
        )
        if not img and not is_dir:
            tools.feedback(
                f'Unable to load image "{_source}!" - please check name and location',
                True,
            )
        else:
            try:
                self.image_location = img.fileName
            except AttributeError:
                self.image_location = _source
        rotation = kwargs.get("rotation", self.rotation)
        # assumes 1 pt == 1 pixel ?
        if rotation:
            # ---- rotated image
            # tools.feedback(f'*** IMAGE {ID=} {rotation=} {self._u.x=} {self._u.y=}')
            cnv.saveState()
            # move the canvas origin
            if ID is not None:
                dx, dy = self._u.margin_left, self._u.margin_bottom
                cnv.translate(x + dx, y + dy)
            else:
                cnv.translate(x + self._o.delta_x, y + self._o.delta_y)
            cnv.rotate(rotation)
            # draw the image relative to the origin
            if is_svg:
                from reportlab.graphics import renderPDF

                renderPDF.draw(img, cnv, x=-width / 2.0, y=-height / 2.0)
            else:
                cnv.drawImage(
                    img,
                    x=-width / 2.0,
                    y=-height / 2.0,
                    width=width,
                    height=height,
                    mask="auto",
                )
            cnv.restoreState()
        else:
            # ---- normal image
            if is_svg:
                from reportlab.graphics import renderPDF

                renderPDF.draw(img, cnv, x=x, y=y)
            else:
                # TODO -> use height=10 OR width=12 AND preserveAspectRatio=True
                cnv.drawImage(img, x=x, y=y, width=width, height=height, mask="auto")
        # ---- text
        xc = x + width / 2.0
        yc = y + height / 2.0
        if self.heading:
            cnv.setFont(self.font_name, self.heading_size)
            cnv.setFillColor(self.heading_stroke)
            self.draw_multi_string(cnv, xc, y + height + cnv._leading, self.heading)
        if self.label:
            cnv.setFont(self.font_name, self.label_size)
            cnv.setFillColor(self.label_stroke)
            self.draw_multi_string(cnv, xc, yc, self.label)
        if self.title:
            cnv.setFont(self.font_name, self.title_size)
            cnv.setFillColor(self.title_stroke)
            self.draw_multi_string(cnv, xc, y - cnv._leading, self.title)


class ArcShape(BaseShape):
    """
    Arc on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw arc on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv.canvas if cnv else self.canvas.canvas
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # tools.feedback(f'*** ARC {self.x=} {self.y=} {self.x_1=} {self.y_1=} {self.angle_width=} ')
        # ---- convert to using units
        x_1 = self._u.x + self._o.delta_x
        y_1 = self._u.y + self._o.delta_y
        if not self.x_1:
            self.x_1 = self.x + self.default_length
        if not self.y_1:
            self.y_1 = self.y + self.default_length
        x_2 = self.unit(self.x_1) + self._o.delta_x
        y_2 = self.unit(self.y_1) + self._o.delta_y
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- draw arc
        # tools.feedback(f'*** Arc: {x_1=}, {y_1=}, {x_2=}, {y_2=}')
        cnv.arc(
            x_1, y_1, x_2, y_2, startAng=self.angle, extent=self.angle_width
        )  # anti-clock from flat; 90°


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

    def get_vertices(self, **kwargs):
        """Calculate vertices of arrow."""
        x_c = kwargs.get("x")
        x_s, y_s = x_c - self.tail_width_u / 2.0, kwargs.get("y")
        tail_height = self._u.height
        total_height = self._u.height + self.head_height_u
        if tail_height <= 0:
            tools.feedback(
                "The Arrow head height must be less than overall height", True
            )
        # print(f"***2 {self._u.width=} {self.tail_width_u=}  {self.head_width_u=} {self.fill=} ")
        # print(f"{=} ")
        vertices = []
        vertices.append(Point(x_s, y_s))  # lower-left corner
        vertices.append(Point(x_c - self._u.width / 2.0, y_s + tail_height))
        vertices.append(
            Point(
                x_c - self.head_width_u / 2.0, y_s + tail_height + self.points_offset_u
            )
        )
        vertices.append(Point(x_c, y_s + total_height))  # tip
        vertices.append(
            Point(
                x_c + self.head_width_u / 2.0, y_s + tail_height + self.points_offset_u
            )
        )
        vertices.append(Point(x_c + self._u.width / 2.0, y_s + tail_height))
        vertices.append(Point(x_c + self.tail_width_u / 2.0, y_s))  # bottom corner
        if self.tail_notch_u > 0:
            vertices.append(Point(x_c, y_s + self.tail_notch_u))  # centre notch
        return vertices

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw an arrow shape on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv.canvas if cnv else self.canvas.canvas
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        if self.use_abs:
            x = self._abs_x
            y = self._abs_y
        else:
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
        cx = x
        cy = y + self._u.height
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- handle rotation: START
        rotation = kwargs.get("rotation", self.rotation)
        if rotation:
            # tools.feedback(f'*** Arrow {ID=} {rotation=} {self._u.x=}, {self._u.y=}')
            cnv.saveState()
            # move the canvas origin
            if ID is not None:
                # cnv.translate(cx + self._u.margin_left, cy + self._u.margin_bottom)
                cnv.translate(cx, cy)
            else:
                cnv.translate(cx, cy)
            cnv.rotate(rotation)
            # reset centre and "bottom centre"
            cx, cy = 0, 0
            x = 0
            y = -self._u.height
        # ---- draw arrow
        self.vertices = self.get_vertices(cx=cx, cy=cy, x=x, y=y)
        pth = cnv.beginPath()
        pth.moveTo(*self.vertices[0])
        for vertex in self.vertices:
            pth.lineTo(*vertex)
        pth.close()
        cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0)
        # ---- dot
        self.draw_dot(cnv, cx, cy)
        # ---- cross
        self.draw_cross(cnv, cx, cy)
        # ---- text
        if kwargs and kwargs.get("rotation"):
            kwargs.pop("rotation")  # otherwise labels rotate again!
        self.draw_heading(cnv, ID, x, y + self._u.height + self.head_height_u, **kwargs)
        self.draw_title(cnv, ID, x, y, **kwargs)
        # ---- handle rotation: END
        if rotation:
            cnv.restoreState()


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
        cnv = cnv.canvas if cnv else self.canvas.canvas
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
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- draw bezier
        cnv.bezier(x_1, y_1, x_2, y_2, x_3, y_3, x_4, y_4)


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

    def draw_hatch(self, cnv, ID, num: int, x_c: float, y_c: float):
        """Draw line(s) from one edge to the other.

        Args:
            num: number of lines
            x_c: x-centre of circle
            y_c: y-centre of circle
        """
        self.set_canvas_props(
            index=ID,
            stroke=self.hatch_stroke,
            stroke_width=self.hatch_stroke_width,
            stroke_cap=self.hatch_cap,
        )
        _dirs = tools.validated_directions(
            self.hatch, tools.DirectionGroup.CIRCULAR, "hatch"
        )
        lines = int(num)
        if lines < 0:
            tools.feedback("Cannot draw negative number of lines!", True)
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
                self.draw_line_between_points(
                    cnv,
                    Point(x_c + self._u.radius, y_c),
                    Point(x_c - self._u.radius, y_c),
                )
            if "n" in _dirs or "s" in _dirs or "o" in _dirs:  # vertical
                self.draw_line_between_points(
                    cnv,
                    Point(x_c, y_c + self._u.radius),
                    Point(x_c, y_c - self._u.radius),
                )
            if "se" in _dirs or "nw" in _dirs or "d" in _dirs:  # diagonal  "down"
                poc_top_d = geoms.point_on_circle(Point(x_c, y_c), self._u.radius, 135)
                poc_btm_d = geoms.point_on_circle(Point(x_c, y_c), self._u.radius, 315)
                self.draw_line_between_points(cnv, poc_top_d, poc_btm_d)
            if "ne" in _dirs or "sw" in _dirs or "d" in _dirs:  # diagonal  "up"
                poc_top_u = geoms.point_on_circle(Point(x_c, y_c), self._u.radius, 45)
                poc_btm_u = geoms.point_on_circle(Point(x_c, y_c), self._u.radius, 225)
                self.draw_line_between_points(cnv, poc_top_u, poc_btm_u)

        if num <= 1:
            return

        if "e" in _dirs or "w" in _dirs or "o" in _dirs:  # horizontal
            for dist in horizontal_distances:
                self.draw_line_between_points(  # "above" diameter
                    cnv,
                    Point(x_c - dist[0], y_c + dist[1]),
                    Point(x_c + dist[0], y_c + dist[1]),
                )
                self.draw_line_between_points(  # "below" diameter
                    cnv,
                    Point(x_c - dist[0], y_c - dist[1]),
                    Point(x_c + dist[0], y_c - dist[1]),
                )

        if "n" in _dirs or "s" in _dirs or "o" in _dirs:  # vertical
            for dist in vertical_distances:
                self.draw_line_between_points(  # "right" of diameter
                    cnv,
                    Point(x_c + dist[0], y_c + dist[1]),
                    Point(x_c + dist[0], y_c - dist[1]),
                )
                self.draw_line_between_points(  # "left" of diameter
                    cnv,
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
                self.draw_line_between_points(cnv, dar, dal)
                # "below left" of diameter
                dbl = geoms.point_on_circle(
                    Point(x_c, y_c), self._u.radius, 225.0 - _angle
                )
                dbr = geoms.point_on_circle(
                    Point(x_c, y_c), self._u.radius, 225.0 + _angle
                )
                self.draw_line_between_points(cnv, dbr, dbl)
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
                self.draw_line_between_points(cnv, poc_top, poc_btm)
                # "below right" of diameter
                poc_top = geoms.point_on_circle(
                    Point(x_c, y_c), self._u.radius, 45 - _angle
                )
                poc_btm = geoms.point_on_circle(
                    Point(x_c, y_c), self._u.radius, 180.0 + _angle + 45.0
                )
                self.draw_line_between_points(cnv, poc_top, poc_btm)

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
                tools.feedback(
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
            # print(f'{radius_length=} :: {radius_offset=} :: {outer_radius=}')
            self.set_canvas_props(
                index=ID,
                stroke=self.radii_stroke,
                stroke_width=self.radii_stroke_width,
                dashed=self.radii_dashed,
                dotted=self.radii_dotted,
            )
            _radii_labels = tools.split(self.radii_labels)
            label_key = 0
            for key, rad_angle in enumerate(_radii):
                # points based on length of line, offset and the angle in degrees
                diam_pt = geoms.point_on_circle(
                    Point(x_c, y_c), radius_length, rad_angle
                )
                pth = cnv.beginPath()
                if radius_offset is not None and radius_offset != 0:
                    # print(f'{rad_angle=} {radius_offset=} {diam_pt}, {x_c=}, {y_c=}')
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
                # ---- radii line
                pth.moveTo(x_start, y_start)
                pth.lineTo(x_end, y_end)
                cnv.drawPath(
                    pth,
                    stroke=1 if self.radii_stroke else 0,
                    fill=1 if self.fill else 0,
                )
                # ---- radii text label
                if _radii_labels:
                    self.radii_label = _radii_labels[label_key]
                    self.draw_radii_label(
                        cnv,
                        ID,
                        (x_start + x_end) / 2.0,
                        (y_start + y_end) / 2.0,
                        rotation=rad_angle + self.radii_labels_rotation,
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
                # print(f'  ^^^ {index=} {angle=} ')
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
                    case "curve" | "c":
                        if index == 0:
                            # start point (for first "current" petal location)
                            petals_vertices.append(
                                geoms.point_on_circle(
                                    center, self._u.radius + offset, angle + gap
                                )
                            )
                        else:
                            # 3 points for create arc/bezier 'bounding box':
                            # the curveTo method starts painting a Bezier curve
                            # beginning at the current location, using
                            # (x1,y1), (x2,y2), and (x3,y3) as the other
                            # three control points, leaving brush on (x3,y3)
                            pt1 = geoms.point_on_circle(
                                center, self._u.radius + offset + height, angle
                            )
                            pt2 = geoms.point_on_circle(
                                center, self._u.radius + offset + height, angle + gap
                            )
                            pt3 = geoms.point_on_circle(
                                center, self._u.radius + offset, angle + gap
                            )
                            petals_vertices.append((pt1, pt2, pt3))
                            # print(f'  {pt1=} {pt2=} {pt3=}')
                    case "petal" | "p":
                        if index == 0:
                            # start point (for first "current" curve location)
                            last_pt = geoms.point_on_circle(
                                center, self._u.radius + offset, angle
                            )
                            petals_vertices.append(last_pt)
                            self._debug(cnv, point=last_pt, label="start", color=red)
                        else:
                            # 3 points for create arc/bezier 'bounding box':
                            # the curveTo method starts painting a Bezier curve
                            # beginning at the current location, using
                            # (x1,y1), (x2,y2), and (x3,y3) as the other
                            # three control points, leaving brush on (x3,y3)
                            next_pt = geoms.point_on_circle(
                                center, self._u.radius + offset, angle
                            )
                            self._debug(
                                cnv, point=next_pt, label=f"next:{index}", color=green
                            )
                            chord = abs(geoms.length_of_line(last_pt, next_pt))
                            box_height = chord / 2.0 * 4.0 / 3.0
                            _, _, chord_angle = geoms.circle_angles(
                                self._u.radius, chord
                            )
                            pt0_angle = angles[index - 1] + (90 - chord_angle)
                            pt1_angle = angle - (90 - chord_angle)
                            # print(f' * {chord_angle=} {pt0_angle=} {pt1_angle=}')
                            pt0 = geoms.degrees_to_xy(pt0_angle, box_height, last_pt)
                            pt1 = geoms.degrees_to_xy(pt1_angle, box_height, next_pt)
                            petals_vertices.append((pt0, pt1, next_pt))
                            last_pt = next_pt
                            self._debug(
                                cnv, point=next_pt, label=f"last:{index}", color=red
                            )
                            # print(f'  {pt0=} {pt1=} {next_pt=} ')
            # ---- draw and fill
            self.set_canvas_props(
                index=ID,
                fill=self.petals_fill,
                stroke=self.petals_stroke,
                stroke_width=self.petals_stroke_width,
                dashed=self.petals_dashed,
                dotted=self.petals_dotted,
            )
            pth = cnv.beginPath()
            pth.moveTo(*petals_vertices[0])
            match self.petals_style:
                case "triangle" | "t":
                    for vertex in petals_vertices:
                        pth.lineTo(*vertex)
                case "curve" | "c" | "petal" | "p":
                    for index, vertex in enumerate(petals_vertices):
                        if index == 0:
                            continue  # already have a "start" location on path
                        pth.curveTo(
                            vertex[0].x,
                            vertex[0].y,
                            vertex[1].x,
                            vertex[1].y,
                            vertex[2].x,
                            vertex[2].y,
                        )
                        if index in [1, 1]:
                            self._debug(cnv, vertices=[vertex[0], vertex[1], vertex[2]])
            pth.close()
            cnv.drawPath(
                pth,
                stroke=1 if self.petals_stroke else 0,
                fill=1 if self.petals_fill else 0,
            )

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw circle on a given canvas."""
        kwargs = self.kwargs | kwargs
        _ = kwargs.pop("ID", None)
        # tools.feedback(f' @@@ Circ.draw {kwargs=}')
        cnv = cnv.canvas if cnv else self.canvas.canvas
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
        # ---- handle rotation: START
        is_rotated = False
        rotation = kwargs.get("rotation", self.rotation)
        if rotation:
            is_rotated = True
            # tools.feedback(f'*** Rect {ID=} {rotation=} {self._u.x=}, {self._u.y=}')
            cnv.saveState()
            # move the canvas origin
            if ID is not None:
                cnv.translate(x + self._u.margin_left, y + self._u.margin_bottom)
            else:
                cnv.translate(x, y)
            cnv.rotate(rotation)
            x, y = 0, 0
            self.x_c, self.y_c = 0, 0
        # ---- draw petals
        if self.petals:
            if self.rotation:
                # tools.feedback(f'*** Rect {self.petals=}, {self.rotation=}, {type(cnv)}')
                cnv.saveState()
                cnv.translate(self.x_c, self.y_c)
                self.draw_petals(cnv, ID, 0, 0)
                cnv.rotate(self.rotation)
                cnv.restoreState()
            else:
                self.draw_petals(cnv, ID, self.x_c, self.y_c)
        # tools.feedback(f'*** Circle: {x=} {y=}')
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- draw circle
        cnv.circle(
            x,
            y,
            self._u.radius,
            stroke=1 if self.stroke else 0,
            fill=1 if self.fill else 0,
        )
        # ---- grid marks
        self.set_canvas_props(
            index=ID, stroke=self.grid_stroke, stroke_width=self.grid_stroke_width
        )
        if self.grid_marks:
            # print(f'{self._u.radius=} {self._u.diameter=}')
            deltag = self.unit(self.grid_length)
            pth = cnv.beginPath()
            gx, gy = 0, y - self._u.radius  # left-side
            pth.moveTo(gx, gy)
            pth.lineTo(deltag, gy)
            pth.moveTo(0, gy + self._u.radius * 2.0)
            pth.lineTo(deltag, gy + self._u.radius * 2.0)
            gx, gy = x - self._u.radius, self.paper[1]  # top-side
            pth.moveTo(gx, gy)
            pth.lineTo(gx, gy - deltag)
            pth.moveTo(gx + self._u.radius * 2.0, gy)
            pth.lineTo(gx + self._u.radius * 2.0, gy - deltag)
            gx, gy = self.paper[0], y - self._u.radius  # right-side
            pth.moveTo(gx, gy)
            pth.lineTo(gx - deltag, gy)
            pth.moveTo(gx, gy + self._u.radius * 2.0)
            pth.lineTo(gx - deltag, gy + self._u.radius * 2)
            gx, gy = x - self._u.radius, 0  # bottom-side
            pth.moveTo(gx, gy)
            pth.lineTo(gx, gy + deltag)
            pth.moveTo(gx + self._u.radius * 2.0, gy)
            pth.lineTo(gx + self._u.radius * 2.0, gy + deltag)
            # done
            cnv.drawPath(pth, stroke=1, fill=1)
        # ---- draw hatch
        if self.hatch_count:
            if self.rotation:
                # tools.feedback(f'*** Circle {self.hatch_count=}, {self.rotation=}, {type(cnv)}')
                cnv.saveState()
                cnv.translate(self.x_c, self.y_c)
                self.draw_hatch(cnv, ID, self.hatch_count, 0, 0)
                cnv.rotate(self.rotation)
                cnv.restoreState()
            else:
                self.draw_hatch(cnv, ID, self.hatch_count, self.x_c, self.y_c)
        # ---- draw radii
        if self.radii:
            if self.rotation:
                # tools.feedback(f'*** Circle {self.hatch_count=}, {self.rotation=}, {type(cnv)}')
                cnv.saveState()
                cnv.translate(self.x_c, self.y_c)
                self.draw_radii(cnv, ID, 0, 0)
                cnv.rotate(self.rotation)
                cnv.restoreState()
            else:
                self.draw_radii(cnv, ID, self.x_c, self.y_c)
        # ---- centred shape (with offset)
        if self.centre_shape:
            cshape_name = self.centre_shape.__class__.__name__
            if cshape_name in GRID_SHAPES_WITH_CENTRE:
                self.centre_shape.draw(
                    _abs_cx=x + self.unit(self.centre_shape_mx),
                    _abs_cy=y + self.unit(self.centre_shape_my),
                )
            elif cshape_name not in GRID_SHAPES_WITH_CENTRE:
                tools.feedback(f"Cannot draw a centered {cshape_name}!")
        # ---- cross
        self.draw_cross(cnv, self.x_c, self.y_c)
        # ---- dot
        self.draw_dot(cnv, self.x_c, self.y_c)
        # ---- text
        if kwargs and kwargs.get("rotation"):
            kwargs.pop("rotation")  # otherwise labels rotate again!
        self.draw_heading(cnv, ID, self.x_c, self.y_c + self._u.radius, **kwargs)
        self.draw_label(cnv, ID, self.x_c, self.y_c, **kwargs)
        self.draw_title(cnv, ID, self.x_c, self.y_c - self._u.radius, **kwargs)
        # ---- handle rotation: END
        if rotation:
            cnv.restoreState()


class ChordShape(BaseShape):
    """
    Chord line on a Circle on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a chord on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv.canvas if cnv else self.canvas.canvas
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        if not isinstance(self.shape, CircleShape):
            tools.feedback("Shape must be a circle!", True)
        circle = self.shape
        x_c, y_c = circle.calculate_centre()
        centre = Point(circle.cx, circle.cy)
        pt0 = geoms.point_on_circle(centre, circle.radius, self.angle)
        pt1 = geoms.point_on_circle(centre, circle.radius, self.angle_1)
        # tools.feedback(f"*** {circle.radius=} {pt0=} {pt1=}")
        x = self.unit(pt0.x) + self._o.delta_x
        y = self.unit(pt0.y) + self._o.delta_y
        x_1 = self.unit(pt1.x) + self._o.delta_x
        y_1 = self.unit(pt1.y) + self._o.delta_y
        # tools.feedback(f"*** {x=} {x_1=} {y=} {y_1=}")
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- draw line
        pth = cnv.beginPath()
        pth.moveTo(x, y)
        pth.lineTo(x_1, y_1)
        cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0)
        # ---- calculate line rotation
        compass, rotation = geoms.angles_from_points(x, y, x_1, y_1)
        # tools.feedback(f"*** {compass=} {rotation=}")
        # ---- dot
        self.draw_dot(cnv, (x_1 + x) / 2.0, (y_1 + y) / 2.0)
        # ---- text
        self.draw_label(
            cnv,
            ID,
            (x_1 + x) / 2.0,
            (y_1 + y) / 2.0,
            rotation=rotation,
            centred=False,
            **kwargs,
        )


class DotShape(BaseShape):
    """
    Dot of fixed radius on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a dot on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv.canvas if cnv else self.canvas.canvas
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # tools.feedback(f"Dot {self._o.delta_x=} {self._o.delta_y=}")
        if self.use_abs_c:
            x = self._abs_cx
            y = self._abs_cy
        else:
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
        size = self.dot_point / 2.0  # diameter is 3 points ~ 1mm or 1/32"
        self.fill = self.stroke
        self.set_canvas_props(index=ID)
        # ---- draw dot
        # tools.feedback(f'*** Dot {size=} {x=} {y=}')
        cnv.circle(x, y, size, stroke=0, fill=1 if self.fill else 0)
        # ---- text
        self.draw_heading(cnv, ID, x, y, **kwargs)
        self.draw_label(cnv, ID, x, y, **kwargs)
        self.draw_title(cnv, ID, x, y, **kwargs)


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
        self.set_canvas_props(
            index=ID,
            stroke=self.radii_stroke,
            stroke_width=self.radii_stroke_width,
            dashed=self.radii_dashed,
            dotted=self.radii_dotted,
        )
        pth = cnv.beginPath()
        # tools.feedback(
        #    f'*** Compass {self.x_c=:.2f} {self.y_c=:.2f}; {x=:.2f} {y=:.2f}')
        pth.moveTo(self.x_c, self.y_c)
        if absolute:
            pth.lineTo(x, y)
        else:
            pth.lineTo(x + self.x_c, y + self.y_c)
        cnv.drawPath(
            pth, stroke=1 if self.radii_stroke else 0, fill=1 if self.fill else 0
        )

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

        # tools.feedback(f'*** Compass {angle=}', False)
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
                tools.feedback(f"{angle} not in range", True)

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw compass on a given canvas."""
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        cnv = cnv.canvas if cnv else self.canvas.canvas
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
        # ---- set canvas
        self.set_canvas_props(index=ID)
        if self.perimeter == "circle":
            cnv.circle(self.x_c, self.y_c, radius, stroke=1, fill=1 if self.fill else 0)
        # ---- draw compass in circle
        _directions = tools.validated_directions(
            self.directions, tools.DirectionGroup.COMPASS, "directions"
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
                tools.feedback(
                    "radii_length cannot be used for a rectangle-perimeter Compass",
                    False,
                    True,
                )
            rect = RectangleShape(**self.kwargs)
            rotation = 0
            vertices = rect.get_vertices(rotation, **kwargs)

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
        self.draw_cross(cnv, self.x_c, self.y_c)
        # ---- dot
        self.draw_dot(cnv, self.x_c, self.y_c)
        # ---- text
        self.draw_heading(cnv, ID, self.x_c, self.y_c + radius, **kwargs)
        self.draw_label(cnv, ID, self.x_c, self.y_c, **kwargs)
        self.draw_title(cnv, ID, self.x_c, self.y_c - radius, **kwargs)


class ChordShape(BaseShape):
    """
    Chord line on a Circle on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a chord on a given canvas."""
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        cnv = cnv.canvas if cnv else self.canvas.canvas
        if not isinstance(self.shape, CircleShape):
            tools.feedback("Shape must be a circle!", True)
        circle = self.shape
        x_c, y_c = circle.calculate_centre()
        centre = Point(circle.cx, circle.cy)
        pt0 = geoms.point_on_circle(centre, circle.radius, self.angle)
        pt1 = geoms.point_on_circle(centre, circle.radius, self.angle_1)
        # tools.feedback(f"*** {circle.radius=} {pt0=} {pt1=}")
        x = self.unit(pt0.x) + self._o.delta_x
        y = self.unit(pt0.y) + self._o.delta_y
        x_1 = self.unit(pt1.x) + self._o.delta_x
        y_1 = self.unit(pt1.y) + self._o.delta_y
        # tools.feedback(f"*** {x=} {x_1=} {y=} {y_1=}")
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- draw line
        pth = cnv.beginPath()
        pth.moveTo(x, y)
        pth.lineTo(x_1, y_1)
        cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0)
        # ---- calculate line rotation
        compass, rotation = geoms.angles_from_points(x, y, x_1, y_1)
        # tools.feedback(f"*** {compass=} {rotation=}")
        # ---- dot
        self.draw_dot(cnv, (x_1 + x) / 2.0, (y_1 + y) / 2.0)
        # ---- text
        self.draw_label(
            cnv,
            ID,
            (x_1 + x) / 2.0,
            (y_1 + y) / 2.0,
            rotation=rotation,
            centred=False,
            **kwargs,
        )


class DotShape(BaseShape):
    """
    Dot of fixed radius on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a dot on a given canvas."""
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # tools.feedback(f"Dot {self._o.delta_x=} {self._o.delta_y=}")
        cnv = cnv.canvas if cnv else self.canvas.canvas
        if self.use_abs_c:
            x = self._abs_cx
            y = self._abs_cy
        else:
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
        size = self.dot_point / 2.0  # diameter is 3 points ~ 1mm or 1/32"
        self.fill = self.stroke
        self.set_canvas_props(index=ID)
        # ---- draw dot
        # tools.feedback(f'*** Dot {size=} {x=} {y=}')
        cnv.circle(x, y, size, stroke=0, fill=1 if self.fill else 0)
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
        cnv = cnv.canvas if cnv else self.canvas.canvas
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
        # ---- handle rotation: START
        rotation = kwargs.get("rotation", self.rotation)
        if rotation:
            # tools.feedback(f'***Ellp {ID=} {rotation=} {self._u.x=}, {self._u.y=}')
            cnv.saveState()
            # move the canvas origin
            if ID is not None:
                cnv.translate(x + self._u.margin_left, y + self._u.margin_bottom)
            else:
                cnv.translate(x + self._u.width / 2.0, y + self._u.height / 2.0)
            cnv.rotate(rotation)
            # reset centre and "bottom left"
            x_d, y_d = 0, 0
            x = -self._u.width / 2.0
            y = -self._u.height / 2.0
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- draw ellipse
        pth = cnv.beginPath()
        pth.ellipse(x, y, self._u.width, self._u.height)
        cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0)
        # ---- cross
        self.draw_cross(cnv, x_d, y_d)
        # ---- dot
        self.draw_dot(cnv, x_d, y_d)
        # ---- text
        if kwargs and kwargs.get("rotation"):
            kwargs.pop("rotation")  # otherwise labels rotate again!
        self.draw_heading(
            cnv, ID, x_d, y_d + 0.5 * self._u.height + delta_m_up, **kwargs
        )
        self.draw_label(cnv, ID, x_d, y_d, **kwargs)
        self.draw_title(
            cnv, ID, x_d, y_d - 0.5 * self._u.height - delta_m_down, **kwargs
        )
        # ---- handle rotation: END
        if rotation:
            cnv.restoreState()


class EquilateralTriangleShape(BaseShape):
    """
    Equilateral Triangle on a given canvas.
    """

    def draw_hatch(self, cnv, ID, side: float, vertices: list, num: int):
        self.set_canvas_props(
            index=ID,
            stroke=self.hatch_stroke,
            stroke_width=self.hatch_stroke_width,
            stroke_cap=self.hatch_cap,
        )
        _dirs = tools.validated_directions(
            self.hatch, tools.DirectionGroup.HEX_POINTY, "hatch"
        )
        lines = int(num) + 1

        if num >= 1:
            # v_tl, v_tr, v_bl, v_br
            if "ne" in _dirs or "sw" in _dirs:  # slope UP to the right
                self.draw_lines_between_sides(
                    cnv, side, lines, vertices, (0, 1), (2, 1)
                )
            if "se" in _dirs or "nw" in _dirs:  # slope down to the right
                self.draw_lines_between_sides(
                    cnv, side, lines, vertices, (0, 2), (0, 1)
                )
            if "e" in _dirs or "w" in _dirs:  # horizontal
                self.draw_lines_between_sides(
                    cnv, side, lines, vertices, (0, 2), (1, 2)
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

    def get_vertices(
        self, x: float, y: float, side: float, hand: str, flip: str
    ) -> list:
        height = 0.5 * math.sqrt(3) * side  # ½√3(a)
        vertices = []
        pt0 = Point(x + self._o.delta_x, y + self._o.delta_y)
        vertices.append(pt0)
        if hand == "west" or hand == "w":
            x2 = pt0.x - side
            y2 = pt0.y
            x3 = pt0.x - 0.5 * side
        elif hand == "east" or hand == "e":
            x2 = pt0.x + side
            y2 = pt0.y
            x3 = x2 - 0.5 * side
        if flip == "north" or flip == "n":
            y3 = pt0.y + height
        elif flip == "south" or flip == "s":
            y3 = pt0.y - height
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
        cnv = cnv.canvas if cnv else self.canvas.canvas
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- calculate points
        x, y = self._u.x, self._u.y
        # angle = self.angle
        side = self._u.side if self._u.side else self._u.width
        height = 0.5 * math.sqrt(3) * side  # ½√3(a)
        if self.cx and self.cy:
            self.centroid = Point(self._u.cx, self._u.cy)
            centroid_to_vertex = side / math.sqrt(3)
            y_off = height - centroid_to_vertex
            x = self._u.cx - side / 2.0
            y = self._u.cy - (height - centroid_to_vertex)
            # print(f'** {side=} {height=} {centroid_to_vertex=} {y_off=}')
        # tools.feedback(f'*** EQT {side=} {height=} {self.fill=} {self.stroke=}')
        self.vertices = self.get_vertices(x, y, side, self.hand, self.flip)
        self.centroid = self.get_centroid(self.vertices)
        # ---- handle rotation: START
        rotation = kwargs.get("rotation", self.rotation)
        if rotation:
            # tools.feedback(f'*** EQT {ID=} {rotation=} {x=}, {y=}')
            cnv.saveState()
            # move the canvas origin
            if ID is not None:
                cnv.translate(self.centroid.x, self.centroid.y)
            else:
                cnv.translate(self.centroid.x, self.centroid.y)
            cnv.rotate(rotation)
            # reset centre and "bottom left"
            self.centroid = Point(0, 0)
            centroid_to_vertex = side / math.sqrt(3)
            y_off = height - centroid_to_vertex
            x = 0.0 - side / 2.0
            y = 0.0 - y_off
            # print(f'*** EQT {side=} {height=} {centroid_to_vertex=} {y_off=}')
            # print(f'*** EQT {x=}, {y=}')
            self.vertices = self.get_vertices(x, y, side, self.hand, self.flip)
        # tools.feedback(f'*** EQT {self.centroid=}')
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- draw equilateral triangle
        pth = cnv.beginPath()
        pth.moveTo(self.vertices[0].x, self.vertices[0].y)
        for key, vertex in enumerate(self.vertices):
            pth.lineTo(vertex.x, vertex.y)
        pth.close()
        cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0)
        # ---- debug
        self._debug(cnv, vertices=self.vertices)
        # ---- draw hatch
        if self.hatch_count:
            self.draw_hatch(cnv, ID, side, self.vertices, self.hatch_count)
        # ---- centred shape (with offset)
        if self.centre_shape:
            cshape_name = self.centre_shape.__class__.__name__
            if cshape_name in GRID_SHAPES_WITH_CENTRE:
                self.centre_shape.draw(
                    _abs_cx=self.centroid.x + self.unit(self.centre_shape_mx),
                    _abs_cy=self.centroid.y + self.unit(self.centre_shape_my),
                )
            elif cshape_name not in GRID_SHAPES_WITH_CENTRE:
                tools.feedback(f"Cannot draw a centered {cshape_name}!")
        # ---- dot
        self.draw_dot(cnv, self.centroid.x, self.centroid.y)
        # ---- text
        self.draw_heading(
            cnv, ID, self.centroid.x, self.centroid.y + height * 2.0 / 3.0, **kwargs
        )
        self.draw_label(cnv, ID, self.centroid.x, self.centroid.y, **kwargs)
        self.draw_title(
            cnv, ID, self.centroid.x, self.centroid.y - height / 3.0, **kwargs
        )
        # ---- handle rotation: END
        if rotation:
            cnv.restoreState()


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
            tools.feedback(
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
            tools.feedback(
                'Invalid orientation "{self.orientation}" supplied for hexagon.', True
            )
        return radius, diameter, side, half_flat

    def calculate_caltrops(self, side, size=None, fraction=None, invert=False):
        """Calculate settings for caltrops (the hex "corner").

        Note: `side` must be in unconverted (user) form e.g. cm or inches
        """
        # tools.feedback(f'*** HEX {side=} {size=} {fraction=}')
        array = []
        match size:
            case "large" | "l":
                part = side / 3.0
                array = [part, part, part]
            case "medium" | "m":
                part = side / 5.0
                array = [part, part * 3.0, part]
            case "small" | "s":
                part = side / 7.0
                array = [part, part * 5.0, part]
            case _:
                pass
        if fraction:
            try:
                float(fraction)
            except Exception:
                tools.feedback(f'Cannot use "{fraction}" for a caltrops fraction', True)
            fraction = min(fraction, 0.5)  # caltrops might meet in the middle
            if fraction < 1.0:
                part = fraction * side
                middle = (1.0 - 2.0 * fraction) * side
                array = [part, middle, part]
        array.insert(0, 0) if invert else array.append(0)
        # convert to points!
        points = self.values_to_points(array)
        return points

    def set_coord(self, cnv, x_d, y_d, half_flat):
        """Set and draw the coords of the hexagon."""
        the_row = self.row or 0
        the_col = self.col or 0
        _row = self.hex_rows - the_row + self.coord_start_y
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
            cnv.setFont(self.coord_font_name, self.coord_font_size)
            cnv.setFillColor(self.coord_stroke)
            coord_offset = self.unit(self.coord_offset)
            if self.coord_elevation in ["t", "top"]:
                self.draw_multi_string(
                    cnv, x_d, y_d + half_flat * 0.7 + coord_offset, self.coord_text
                )
            elif self.coord_elevation in ["m", "middle", "mid"]:
                self.draw_multi_string(
                    cnv,
                    x_d,
                    y_d + coord_offset - self.coord_font_size / 2.0,
                    self.coord_text,
                )
            elif self.coord_elevation in ["b", "bottom", "bot"]:
                self.draw_multi_string(
                    cnv, x_d, y_d - half_flat * 0.9 + coord_offset, self.coord_text
                )
            else:
                tools.feedback(
                    f'Cannot handle a coord_elevation of "{self.coord_elevation}"'
                )

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
                # tools.feedback(f'*** HEX LINK {the_link=}')
            except TypeError:
                tools.feedback(
                    f"Cannot use {parts[0]} and/or {parts[1]} as hex side numbers.",
                    True,
                )

            va_start = the_link.a - 1
            va_end = the_link.a % 6
            vb_start = the_link.b - 1
            vb_end = the_link.b % 6
            tools.feedback(f"a:{va_start}-{va_end} b:{vb_start}-{vb_end}")

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

                    # tools.feedback(
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
        self.set_canvas_props(
            index=ID,
            stroke=self.radii_stroke or self.stroke,
            stroke_width=self.radii_stroke_width or self.stroke_width,
            stroke_cap=self.radii_cap or self.line_cap,
        )
        # _dirs = self.radii.lower().split()
        dir_group = (
            tools.DirectionGroup.HEX_POINTY
            if self.orientation == "pointy"
            else tools.DirectionGroup.HEX_FLAT
        )
        _dirs = tools.validated_directions(self.radii, dir_group, "radii")
        if "ne" in _dirs:  # slope UP to the right
            self.draw_line_between_points(cnv, centre, vertices[2])
        if "sw" in _dirs:  # slope DOWN to the left
            if self.orientation in ["p", "pointy"]:
                self.draw_line_between_points(cnv, centre, vertices[0])
            else:
                self.draw_line_between_points(cnv, centre, vertices[5])
        if "se" in _dirs:  # slope DOWN to the right
            self.draw_line_between_points(cnv, centre, vertices[4])
        if "nw" in _dirs:  # slope UP to the left
            self.draw_line_between_points(cnv, centre, vertices[1])
        if "n" in _dirs and self.orientation in ["p", "pointy"]:  # vertical UP
            self.draw_line_between_points(cnv, centre, vertices[2])
        if "s" in _dirs and self.orientation in ["p", "pointy"]:  # vertical DOWN
            self.draw_line_between_points(cnv, centre, vertices[5])
        if "e" in _dirs and self.orientation in ["f", "flat"]:  # horizontal RIGHT
            self.draw_line_between_points(cnv, centre, vertices[3])
        if "w" in _dirs and self.orientation in ["f", "flat"]:  # horizontal LEFT
            self.draw_line_between_points(cnv, centre, vertices[0])

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
            _, angle = geoms.angles_from_points(centre.x, centre.y, pc.x, pc.y)
            _perbis.append(angle)
        pb_offset = self.unit(self.perbis_offset, label="perbis offset") or 0
        pb_length = (
            self.unit(self.perbis_length, label="perbis length")
            if self.perbis_length
            else self.radius
        )
        self.set_canvas_props(
            index=ID,
            stroke=self.perbis_stroke,
            stroke_width=self.perbis_stroke_width,
            dashed=self.perbis_dashed,
            dotted=self.perbis_dotted,
        )

        if self.perbis:
            dir_group = (
                tools.DirectionGroup.HEX_POINTY_EDGE
                if self.orientation == "pointy"
                else tools.DirectionGroup.HEX_FLAT_EDGE
            )
            perbis_dirs = tools.validated_directions(self.perbis, dir_group, "perbis")
            _dirs = []
            # tools.feedback(f'*** HEX {self.perbis=} {self.orientation=} {perbis_dirs=}')
            if self.orientation in ["p", "pointy"]:
                if "e" in perbis_dirs:
                    _dirs.append(4)
                if "ne" in perbis_dirs:
                    _dirs.append(3)
                if "nw" in perbis_dirs:
                    _dirs.append(2)
                if "w" in perbis_dirs:
                    _dirs.append(1)
                if "sw" in perbis_dirs:
                    _dirs.append(0)
                if "se" in perbis_dirs:
                    _dirs.append(5)
            if self.orientation in ["f", "flat"]:
                if "ne" in perbis_dirs:
                    _dirs.append(3)
                if "n" in perbis_dirs:
                    _dirs.append(2)
                if "nw" in perbis_dirs:
                    _dirs.append(1)
                if "sw" in perbis_dirs:
                    _dirs.append(0)
                if "s" in perbis_dirs:
                    _dirs.append(5)
                if "se" in perbis_dirs:
                    _dirs.append(4)

        for key, pb_angle in enumerate(_perbis):
            if self.perbis and key not in _dirs:
                continue
            # points based on length of line, offset and the angle in degrees
            edge_pt = _perbis_pts[key]
            pth = cnv.beginPath()
            if pb_offset is not None and pb_offset != 0:
                offset_pt = geoms.point_on_circle(centre, pb_offset, pb_angle)
                end_pt = geoms.point_on_line(offset_pt, edge_pt, pb_length)
                # print(f'{pb_angle=} {offset_pt=} {x_c=}, {y_c=}')
                pth.moveTo(offset_pt.x, offset_pt.y)
                pth.lineTo(end_pt.x, end_pt.y)
            else:
                pth.moveTo(centre.x, centre.y)
                pth.lineTo(edge_pt.x, edge_pt.y)
            cnv.drawPath(
                pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0
            )
            # cnv.drawCentredString(edge_pt.x, edge_pt.y, f"{key}")  # test

    def draw_hatch(self, cnv, ID, side: float, vertices: list, num: int):
        """Draw lines connecting two opposite sides and parallel to adjacent side."""
        self.set_canvas_props(
            index=ID,
            stroke=self.hatch_stroke,
            stroke_width=self.hatch_stroke_width,
            stroke_cap=self.hatch_cap,
        )
        dir_group = (
            tools.DirectionGroup.HEX_POINTY
            if self.orientation == "pointy"
            else tools.DirectionGroup.HEX_FLAT
        )
        _dirs = tools.validated_directions(self.hatch, dir_group, "hatch")
        lines = int((num - 1) / 2 + 1)

        if num >= 1:
            # tools.feedback(f'*** HEX {vertices=} {num=} {_dirs=}')
            if self.orientation in ["p", "pointy"]:
                if "ne" in _dirs or "sw" in _dirs:  # slope UP to the right
                    self.make_path_vertices(cnv, vertices, 0, 3)
                if "se" in _dirs or "nw" in _dirs:  # slope down to the right
                    self.make_path_vertices(cnv, vertices, 1, 4)
                if "n" in _dirs or "s" in _dirs:  # vertical
                    self.make_path_vertices(cnv, vertices, 2, 5)
            if self.orientation in ["f", "flat"]:
                if "ne" in _dirs or "sw" in _dirs:  # slope UP to the right
                    self.make_path_vertices(cnv, vertices, 2, 5)
                if "se" in _dirs or "nw" in _dirs:  # slope down to the right
                    self.make_path_vertices(cnv, vertices, 1, 4)
                if "e" in _dirs or "w" in _dirs:  # horizontal
                    self.make_path_vertices(cnv, vertices, 0, 3)
        if num >= 3:
            if self.orientation in ["p", "pointy"]:
                if "ne" in _dirs or "sw" in _dirs:  # slope UP to the right
                    self.draw_lines_between_sides(
                        cnv, side, lines, vertices, (2, 3), (1, 0)
                    )
                    self.draw_lines_between_sides(
                        cnv, side, lines, vertices, (3, 4), (0, 5)
                    )
                if "se" in _dirs or "nw" in _dirs:  # slope down to the right
                    self.draw_lines_between_sides(
                        cnv, side, lines, vertices, (0, 1), (5, 4)
                    )
                    self.draw_lines_between_sides(
                        cnv, side, lines, vertices, (1, 2), (4, 3)
                    )
                if "n" in _dirs or "s" in _dirs:  # vertical
                    self.draw_lines_between_sides(
                        cnv, side, lines, vertices, (1, 2), (0, 5)
                    )
                    self.draw_lines_between_sides(
                        cnv, side, lines, vertices, (2, 3), (5, 4)
                    )
            if self.orientation in ["f", "flat"]:
                if "ne" in _dirs or "sw" in _dirs:  # slope UP to the right
                    self.draw_lines_between_sides(
                        cnv, side, lines, vertices, (2, 1), (5, 0)
                    )
                    self.draw_lines_between_sides(
                        cnv, side, lines, vertices, (2, 3), (5, 4)
                    )
                if "se" in _dirs or "nw" in _dirs:  # slope down to the right
                    self.draw_lines_between_sides(
                        cnv, side, lines, vertices, (4, 5), (1, 0)
                    )
                    self.draw_lines_between_sides(
                        cnv, side, lines, vertices, (1, 2), (4, 3)
                    )
                if "e" in _dirs or "w" in _dirs:  # horizontal
                    self.draw_lines_between_sides(
                        cnv, side, lines, vertices, (0, 1), (3, 2)
                    )
                    self.draw_lines_between_sides(
                        cnv, side, lines, vertices, (0, 5), (3, 4)
                    )

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a hexagon on a given canvas."""
        kwargs = self.kwargs | kwargs
        # tools.feedback(f'*** draw hex: {off_x=} {off_y=} {ID=}')
        # tools.feedback(f'*** draw hex: {self.x=} {self.y=} {self.cx=} {self.cy=}')
        # tools.feedback(f'*** draw hex: {self.row=} {self.col=}')
        # tools.feedback(f' @@@ Hexg.draw {kwargs=}')
        cnv = cnv.canvas if cnv else self.canvas.canvas
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        is_cards = kwargs.get("is_cards", False)
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
            tools.feedback(
                "No value for side or height or diameter or radius supplied for hexagon.",
                True,
            )

        half_side = side / 2.0
        height_flat = 2 * half_flat
        diameter = 2.0 * side
        radius = side
        z_fraction = (diameter - side) / 2.0

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
                    self.col * (height_flat + self._u.spacing_x)
                    + self._o.delta_x
                    + self._u.offset_x
                )
                y = (
                    self.row * (diameter + self._u.spacing_y)
                    + self._o.delta_y
                    + self._u.offset_y
                )  # do NOT add half_flat
            elif self.row is not None and self.col is not None:
                if self.hex_offset in ["o", "O", "odd"]:
                    # TODO => calculate!
                    # downshift applies from first even row - NOT the very first one!
                    downshift = diameter - z_fraction if self.row >= 1 else 0
                    downshift = downshift * self.row if self.row >= 2 else downshift
                    y = (
                        self.row * (diameter + side)
                        - downshift
                        + self._u.y
                        + self._o.delta_y
                    )
                    if (self.row + 1) & 1:  # is odd row; row are 0-base numbered!
                        x = (
                            self.col * height_flat
                            + half_flat
                            + self._u.x
                            + self._o.delta_x
                        )
                    else:  # even row
                        x = self.col * height_flat + self._u.x + self._o.delta_x
                else:  # self.hex_offset in ['e', 'E', 'even']
                    # downshift applies from first even row - NOT the very first one!
                    downshift = diameter - z_fraction if self.row >= 1 else 0
                    downshift = downshift * self.row if self.row >= 2 else downshift
                    y = (
                        self.row * (diameter + side)
                        - downshift
                        + self._u.y
                        + self._o.delta_y
                    )
                    if (self.row + 1) & 1:  # is odd row; row are 0-base numbered!
                        x = self.col * height_flat + self._u.x + self._o.delta_x
                    else:  # even row
                        x = (
                            self.col * height_flat
                            + half_flat
                            + self._u.x
                            + self._o.delta_x
                        )
            # ----  ^ set hex centre relative to x,y
            self.x_d = x + half_flat
            self.y_d = y + side
            # ---- ^ recalculate hex centre
            if self.use_abs_c:
                # create x_d, y_d as the unit-formatted hex centre
                self.x_d = self._abs_cx
                self.y_d = self._abs_cy
                # recalculate start x,y
                x = self.x_d - half_flat
                y = self.y_d - half_side - side / 2.0
            elif self.cx is not None and self.cy is not None:
                # cx,cy are centre; create x_d, y_d as the unit-formatted hex centre
                self.x_d = self._u.cx + self._o.delta_y
                self.y_d = self._u.cy + self._o.delta_x
                # recalculate start x,y
                x = self.x_d - half_flat
                y = self.y_d - half_side - side / 2.0
            # tools.feedback(f"*** P^: {x=} {y=} {self.x_d=} {self.y_d=} {half_flat=} {side=}")

        # ---- FLAT~
        else:
            #         __
            # x,y .. /  \
            #        \__/
            #
            # x and y are at the bottom-left corner of the box around the hex
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
            # tools.feedback(f"{x=} {y=} {half_flat=} {side=} {self.row=} {self.col=}")
            # ---- ~ draw flat by row/col
            if self.row is not None and self.col is not None and is_cards:
                # x = self.col * 2.0 * side + self._o.delta_x
                # if self.row & 1:
                #     x = x + side
                # y = self.row * 2.0 * half_flat + self._o.delta_y  # do NOT add half_flat
                x = (
                    self.col * 2.0 * (side + self._u.spacing_x)
                    + self._o.delta_x
                    + self._u.offset_x
                )
                if self.row & 1:
                    x = x + side + self._u.spacing_x
                y = (
                    self.row * 2.0 * (half_flat + self._u.spacing_y)
                    + self._o.delta_y
                    + self._u.offset_y
                )  # do NOT add half_flat
            elif self.row is not None and self.col is not None:
                if self.hex_offset in ["o", "O", "odd"]:
                    x = self.col * (half_side + side) + self._u.x + self._o.delta_x
                    y = self.row * half_flat * 2.0 + self._u.y + self._o.delta_y
                    if (self.col + 1) & 1:  # is odd
                        y = y + half_flat
                else:  # self.hex_offset in ['e', 'E', 'even']
                    x = self.col * (half_side + side) + self._u.x + self._o.delta_x
                    y = self.row * half_flat * 2.0 + self._u.y + self._o.delta_y
                    if (self.col + 1) & 1:  # is odd
                        pass
                    else:
                        y = y + half_flat
            # ----  ~ set hex centre relative to x,y
            self.x_d = x + side
            self.y_d = y + half_flat
            # ----  ~ recalculate centre if preset
            if self.use_abs_c:
                # create x_d, y_d as the unit-formatted hex centre
                self.x_d = self._abs_cx
                self.y_d = self._abs_cy
                # recalculate start x,y
                x = self.x_d - half_side - side / 2.0
                y = self.y_d - half_flat
            elif self.cx is not None and self.cy is not None:
                # cx,cy are centre; create x_d, y_d as the unit-formatted hex centre
                self.x_d = self._u.cx + self._o.delta_x
                self.y_d = self._u.cy + self._o.delta_y
                # recalculate start x,y
                x = self.x_d - half_side - side / 2.0
                y = self.y_d - half_flat
            # tools.feedback(f"*** F~: {x=} {y=} {self.x_d=} {self.y_d=} {half_flat=} {side=}")

        # ---- calculate area
        self.area = self.calculate_area()
        # ---- canvas
        self.set_canvas_props(index=ID)
        if self.caltrops or self.caltrops_fraction:
            line_dashed = self.calculate_caltrops(
                self.side, self.caltrops, self.caltrops_fraction, self.caltrops_invert
            )
            cnv.setDash(array=line_dashed)
        # ---- calculate vertical hexagon (clockwise)
        if self.orientation.lower() in ["p", "pointy"]:
            self.vertices = [  # clockwise from bottom-left; relative to centre
                Point(x, y + z_fraction),
                Point(x, y + z_fraction + side),
                Point(x + half_flat, y + diameter),
                Point(x + height_flat, y + z_fraction + side),
                Point(x + height_flat, y + z_fraction),
                Point(x + half_flat, y),
            ]
        # ---- calculate horizontal hexagon (clockwise)
        else:  # self.orientation.lower() in ['f',  'flat']:
            self.vertices = [  # clockwise from left; relative to centre
                Point(x, y + half_flat),
                Point(x + z_fraction, y + height_flat),
                Point(x + z_fraction + side, y + height_flat),
                Point(x + diameter, y + half_flat),
                Point(x + z_fraction + side, y),
                Point(x + z_fraction, y),
            ]

        # ---- draw hexagon
        # tools.feedback(f'***Hex {x=} {y=} {self.vertices=}')
        pth = cnv.beginPath()
        pth.moveTo(*self.vertices[0])
        for vertex in self.vertices:
            # TODO - set side-specific line color/style here
            pth.lineTo(*vertex)
        pth.close()
        cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0)

        # ---- * borders (override)
        if self.borders:
            if isinstance(self.borders, tuple):
                self.borders = [
                    self.borders,
                ]
            if not isinstance(self.borders, list):
                tools.feedback('The "borders" property must be a list of sets or a set')
            for border in self.borders:
                self.draw_border(cnv, border, ID)

        # ---- debug
        # self._debug(cnv, Point(x, y), 'start')
        # self._debug(cnv, Point(self.x_d, self.y_d), 'centre')
        self._debug(cnv, vertices=self.vertices)
        # ---- draw hatch
        if self.hatch_count:
            if not self.hatch_count & 1:
                tools.feedback("Hatch must be an odd number for a Hexagon", True)
            self.draw_hatch(cnv, ID, side, self.vertices, self.hatch_count)
        # ---- draw links
        if self.links:
            self.draw_links(cnv, ID, side, self.vertices, self.links)
        # ---- draw radii
        if self.radii:
            self.draw_radii(cnv, ID, Point(self.x_d, self.y_d), self.vertices)
        # ---- draw perbis
        if self.perbis:
            self.draw_perbis(cnv, ID, Point(self.x_d, self.y_d), self.vertices)
        # ---- centred shape (with offset)
        if self.centre_shape:
            cshape_name = self.centre_shape.__class__.__name__
            if cshape_name in GRID_SHAPES_WITH_CENTRE:
                # tools.feedback(f'*** IN-HEX {cshape_name} at ({self.x_d=},{self.y_d=}, '
                #               f'{self.centre_shape_x}, {self.centre_shape_y})')
                self.centre_shape.draw(
                    _abs_cx=self.x_d + self.unit(self.centre_shape_mx),
                    _abs_cy=self.y_d + self.unit(self.centre_shape_my),
                )
            elif cshape_name not in GRID_SHAPES_WITH_CENTRE:
                tools.feedback(f"Cannot draw a centered {cshape_name}!")
        # ---- cross
        self.draw_cross(cnv, self.x_d, self.y_d)
        # ---- dot
        self.draw_dot(cnv, self.x_d, self.y_d)
        # ---- text
        if self.orientation.lower() in ["p", "pointy"]:
            offset = side  # == radius
        else:
            offset = half_flat
        self.draw_heading(cnv, ID, self.x_d, self.y_d + offset, **kwargs)
        self.draw_label(cnv, ID, self.x_d, self.y_d, **kwargs)
        self.draw_title(cnv, ID, self.x_d, self.y_d - offset, **kwargs)
        # ----  numbering
        self.set_coord(cnv, self.x_d, self.y_d, half_flat)
        # ---- set grid property
        self.grid = GridShape(label=self.coord_text, x=self.x_d, y=self.y_d, shape=self)


class LineShape(BaseShape):
    """
    Line on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a line on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv.canvas if cnv else self.canvas.canvas
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
        else:
            if self.angle > 0:
                angle = math.radians(self.angle)
                x_1 = x + (self._u.length * math.cos(angle))
                y_1 = y + (self._u.length * math.sin(angle))
            else:
                x_1 = x + self._u.length
                y_1 = y
        if self.row is not None and self.row >= 0:
            y = y + self.row * self._u.height
            y_1 = y_1 + self.row * self._u.height  # - self._u.margin_bottom
        if self.col is not None and self.col >= 0:
            x = x + self.col * self._u.width
            x_1 = x_1 + self.col * self._u.width  # - self._u.margin_left
        # tools.feedback(f"{x=} {x_1=} {y=} {y_1=}")
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- draw line
        pth = cnv.beginPath()
        pth.moveTo(x, y)
        pth.lineTo(x_1, y_1)
        cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0)
        # ---- calculate line rotation
        compass, rotation = geoms.angles_from_points(x, y, x_1, y_1)
        # ---- dot
        self.draw_dot(cnv, (x_1 + x) / 2.0, (y_1 + y) / 2.0)
        # ---- text
        self.draw_label(
            cnv,
            ID,
            (x_1 + x) / 2.0,
            (y_1 + y) / 2.0 + self.font_size / 4.0,
            rotation=rotation,
            centred=False,
            **kwargs,
        )


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
                tools.feedback("The perbis value must be a list of numbers!", True)
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
        tools.feedback("Sorry, the mesh for Polygon is not yet implemented.", True)
        """ TODO - autodraw (without dirs)
        self.set_canvas_props(
            index=ID,
            stroke=self.mesh_stroke or self.stroke,
            stroke_width=self.mesh_stroke_width or self.stroke_width,
            stroke_cap=self.mesh_cap or self.line_cap)
        _dirs = self.hatch.lower().split()
        lines = int(num)
        if num >= 1:
            if 'ne' in _dirs or 'sw' in _dirs:  # slope UP to the right
                self.draw_lines_between_sides(cnv, side, lines, vertices, (0, 1), (5, 4))
            if 'se' in _dirs or 'nw' in _dirs:  # slope down to the right
                self.draw_lines_between_sides(cnv, side, lines, vertices, (2, 3), (7, 6))
            if 'n' in _dirs or 's' in _dirs:  # vertical
                self.draw_lines_between_sides(cnv, side, lines, vertices, (3, 4), (0, 7))
            if 'e' in _dirs or 'w' in _dirs:  # horizontal
                self.draw_lines_between_sides(cnv, side, lines, vertices, (1, 2), (6, 5))
        """

    def get_centre(self) -> Point:
        """Calculate the centre as a Point (in units)"""
        if self.cx is not None and self.cy is not None:
            x = self._u.cx + self._o.delta_x
            y = self._u.cy + self._o.delta_y
        else:
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
        return Point(x, y)

    def get_angles(self, rotation: float = 0, is_rotated: bool = False) -> list:
        """Angles of lines connecting the Polygon centre to each of the vertices."""
        centre = self.get_centre()
        vertices = self.get_vertices(rotation, is_rotated)
        angles = []
        for vertex in vertices:
            _, angle = geoms.angles_from_points(centre.x, centre.y, vertex.x, vertex.y)
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
            vertices = self.get_vertices(rotation=rotation)
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
            _, angle = geoms.angles_from_points(centre.x, centre.y, pc.x, pc.y)
            _perbis.append(angle)
        pb_offset = self.unit(self.perbis_offset, label="perbis offset") or 0
        pb_length = (
            self.unit(self.perbis_length, label="perbis length")
            if self.perbis_length
            else self.get_radius()
        )
        self.set_canvas_props(
            index=ID,
            stroke=self.perbis_stroke,
            stroke_width=self.perbis_stroke_width,
            dashed=self.perbis_dashed,
            dotted=self.perbis_dotted,
        )
        for key, pb_angle in enumerate(_perbis):
            if self.perbis and key + 1 not in self.perbis:
                continue
            # points based on length of line, offset and the angle in degrees
            edge_pt = _perbis_pts[key]
            pth = cnv.beginPath()
            if pb_offset is not None and pb_offset != 0:
                offset_pt = geoms.point_on_circle(centre, pb_offset, pb_angle)
                end_pt = geoms.point_on_line(offset_pt, edge_pt, pb_length)
                # print(pb_angle, offset_pt, f'{x_c=}, {y_c=}')
                pth.moveTo(offset_pt.x, offset_pt.y)
                pth.lineTo(end_pt.x, end_pt.y)
            else:
                pth.moveTo(centre.x, centre.y)
                pth.lineTo(edge_pt.x, edge_pt.y)
            cnv.drawPath(
                pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0
            )
            # cnv.drawCentredString(edge_pt.x, edge_pt.y, f"{key}")  # test

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
            vertices = self.get_vertices(rotation=rotation)
        _radii = []
        for vertex in vertices:
            _, angle = geoms.angles_from_points(centre.x, centre.y, vertex.x, vertex.y)
            _radii.append(angle)
        rad_offset = self.unit(self.radii_offset, label="radii offset") or 0
        rad_length = (
            self.unit(self.radii_length, label="radii length")
            if self.radii_length
            else self.get_radius()
        )
        self.set_canvas_props(
            index=ID,
            stroke=self.radii_stroke,
            stroke_width=self.radii_stroke_width,
            dashed=self.radii_dashed,
            dotted=self.radii_dotted,
        )
        for rad_angle in _radii:
            # points based on length of line, offset and the angle in degrees
            diam_pt = geoms.point_on_circle(centre, rad_length, rad_angle)
            pth = cnv.beginPath()
            if rad_offset is not None and rad_offset != 0:
                offset_pt = geoms.point_on_circle(centre, rad_offset, rad_angle)
                end_pt = geoms.point_on_line(offset_pt, diam_pt, rad_length)
                # print(rad_angle, offset_pt, f'{x_c=}, {y_c=}')
                pth.moveTo(offset_pt.x, offset_pt.y)
                pth.lineTo(end_pt.x, end_pt.y)
            else:
                pth.moveTo(centre.x, centre.y)
                pth.lineTo(diam_pt.x, diam_pt.y)
            cnv.drawPath(
                pth, stroke=1 if self.radii_stroke else 0, fill=1 if self.fill else 0
            )

    def get_vertices(self, rotation: float = None, is_rotated: bool = False):
        """Calculate vertices of polygon."""
        # convert to using units
        if is_rotated:
            x, y = 0.0, 0.0  # centre for now-rotated canvas
        else:
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
        radius = self.get_radius()
        # calculate vertices - assumes x,y marks the centre point
        _rotation = rotation or self.flatten_angle
        vertices = geoms.polygon_vertices(self.sides, radius, Point(x, y), _rotation)
        # for p in vertices: print(f'*V* {p.x / 28.3465}, {p.y / 28.3465}')
        return vertices

    def get_geometry(self, rotation: float = None, is_rotated: bool = False):
        """Calculate centre, radius, side and vertices of Polygon."""
        # convert to using units
        if is_rotated:
            x, y = 0.0, 0.0  # centre for now-rotated canvas
        else:
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
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
        _rotation = rotation or self.flatten_angle
        vertices = geoms.polygon_vertices(self.sides, radius, Point(x, y), _rotation)
        # for p in vertices: print(f'*G* {p.x / 28.3465}, {p.y / 28.3465}')
        return PolyGeometry(x, y, radius, side, half_flat, vertices)

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a regular polygon on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv.canvas if cnv else self.canvas.canvas
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- calc centre (in units)
        centre = self.get_centre()
        x, y = centre.x, centre.y
        # ---- handle rotation: START
        is_rotated = False
        rotation = kwargs.get("rotation", self.rotation)
        if rotation:
            is_rotated = True
            # tools.feedback(f'*** POLY {ID=} {rotation=} {self._u.x=}, {self._u.y=}')
            cnv.saveState()
            # move the canvas origin
            if ID is not None:
                cnv.translate(x + self._u.margin_left, y + self._u.margin_bottom)
            else:
                cnv.translate(x, y)
            cnv.rotate(rotation)
        # --- handle 'orientation' (flat vs pointy)
        _geom = self.get_geometry(rotation=rotation, is_rotated=is_rotated)
        x, y, radius, vertices = _geom.x, _geom.y, _geom.radius, _geom.vertices
        # ---- invalid polygon?
        if not vertices or len(vertices) == 0:
            if rotation:
                cnv.restoreState()
            return
        # ---- draw polygon
        pth = cnv.beginPath()
        pth.moveTo(*vertices[0])
        for vertex in vertices:
            pth.lineTo(vertex.x, vertex.y)
        pth.close()
        cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0)
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
            cshape_name = self.centre_shape.__class__.__name__
            if cshape_name in GRID_SHAPES_WITH_CENTRE:
                self.centre_shape.draw(
                    _abs_cx=x + self.unit(self.centre_shape_mx),
                    _abs_cy=y + self.unit(self.centre_shape_my),
                )
            elif cshape_name not in GRID_SHAPES_WITH_CENTRE:
                tools.feedback(f"Cannot draw a centered {cshape_name}!")
        # ---- debug
        self._debug(cnv, vertices=vertices)  # needs: self.run_debug = True
        # ---- dot
        self.draw_dot(cnv, x, y)
        # ---- cross
        self.draw_cross(cnv, x, y)
        # ---- text
        if kwargs and kwargs.get("rotation"):
            kwargs.pop("rotation")  # otherwise labels rotate again!
        self.draw_heading(cnv, ID, x, y, 1.3 * radius, **kwargs)
        self.draw_label(cnv, ID, x, y, **kwargs)
        self.draw_title(cnv, ID, x, y, 1.4 * radius, **kwargs)
        # ---- handle rotation: END
        if rotation:
            cnv.restoreState()


class PolylineShape(BaseShape):
    """
    Multi-part line on a given canvas.
    """

    def get_points(self) -> list:
        points = tools.tuple_split(self.points)
        if not points:
            points = self.points
        if not points or len(points) == 0:
            tools.feedback("There are no points to draw the Polyline", False, True)
        return points

    def get_vertices(self):
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
        cnv = cnv.canvas if cnv else self.canvas.canvas
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        points = self.get_points()
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- draw polyline
        if points:
            pth = cnv.beginPath()
            for key, vertex in enumerate(points):
                x, y = vertex
                # convert to using units
                x = self.unit(x) + self._o.delta_x
                y = self.unit(y) + self._o.delta_y
                if key == 0:
                    pth.moveTo(x, y)
                pth.lineTo(x, y)
            cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=0)


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
        cnv = cnv.canvas if cnv else self.canvas.canvas
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        img = None
        # ---- check for Card usage
        cache_directory = str(self.cache_directory)
        _source = self.source
        # tools.feedback(f'*** QRCode {ID=} {self.source=}')
        if ID is not None and isinstance(self.source, list):
            _source = self.source[ID]
        elif ID is not None and isinstance(self.source, str):
            _source = self.source
        else:
            pass
        # if no directory in _source, use qrcodes cache directory!
        if Path(_source).name:
            _source = os.path.join(cache_directory, _source)
        # tools.feedback(f"QRC {self._o.delta_x=} {self._o.delta_y=}")
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
                tools.feedback(
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
        # tools.feedback(f'*** QRC {_locale=} {self.text=} {_text=}', False)
        if _text is None or _text == "":
            tools.feedback("No text supplied for the Text shape!", False, True)
            return
        _text = str(_text)  # card data could be numeric
        if "\\u" in _text:
            _text = codecs.decode(_text, "unicode_escape")
        # ---- create QR code
        qrcode = segno.make_qr(_text)
        qrcode.save(
            _source,
            scale=self.scaling or 1,
            light=tools.color_to_hex(self.fill),
            dark=tools.color_to_hex(self.stroke),
        )
        img = ImageReader(_source)
        # ---- draw code as image
        cnv.drawImage(img, x=x, y=y, width=width, height=height, mask="auto")
        # ---- shape's text
        xc = x + width / 2.0
        yc = y + height / 2.0
        if self.heading:
            cnv.setFont(self.font_name, self.heading_size)
            cnv.setFillColor(self.heading_stroke)
            self.draw_multi_string(cnv, xc, y + height + cnv._leading, self.heading)
        if self.label:
            cnv.setFont(self.font_name, self.label_size)
            cnv.setFillColor(self.label_stroke)
            self.draw_multi_string(cnv, xc, yc, self.label)
        if self.title:
            cnv.setFont(self.font_name, self.title_size)
            cnv.setFillColor(self.title_stroke)
            self.draw_multi_string(cnv, xc, y - cnv._leading, self.title)


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
            # tools.feedback(f"INIT {self.cx=} {self.cy=} {self.x=} {self.y=}")
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
        vertices = self.get_vertices(rotation=rotation, **kwargs)
        centre = Point(x + self._u.height / 2.0, y + self._u.height / 2.0)
        angles = []
        for vtx in vertices:
            _, angle = geoms.angles_from_points(centre.x, centre.y, vtx.x, vtx.y)
            angles.append(angle)
        return angles

    def get_vertices(self, rotation=0, **kwargs):
        """Get vertices for rectangle without notches."""
        if rotation:
            kwargs["rotation"] = rotation
        x, y = self.calculate_xy(**kwargs)
        vertices = [  # clockwise from bottom-left; relative to centre
            Point(x, y),
            Point(x, y + self._u.height),
            Point(x + self._u.width, y + self._u.height),
            Point(x + self._u.width, y),
        ]
        # tools.feedback(
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
        # tools.feedback(f'*** Rect # ---- {_row=},{_col=}')
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
                tools.feedback(
                    f'Cannot handle a coord_elevation of "{self.coord_elevation}"'
                )

    def calculate_xy(self, **kwargs):
        # ---- adjust start
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
        # ---- overrides for centering
        rotation = kwargs.get("rotation", None)
        if rotation:
            x = -self._u.width / 2.0
            y = -self._u.height / 2.0
        return x, y

    def draw_hatch(self, cnv, ID, vertices: list, num: int):
        _dirs = tools.validated_directions(
            self.hatch, tools.DirectionGroup.CIRCULAR, "hatch"
        )
        # ---- check dirs
        if self.rounding or self.rounded:
            if (
                "ne" in _dirs
                or "sw" in _dirs
                or "se" in _dirs
                or "nw" in _dirs
                or "d" in _dirs
            ):
                tools.feedback(
                    "No diagonal hatching permissible with rounding in the rectangle",
                    True,
                )
        # ---- check spaces
        if self.rounding or self.rounded:
            spaces = max(self._u.width / (num + 1), self._u.height / (num + 1))
            if self.rounding:
                _rounding = self.unit(self.rounding)
            elif self.rounded:
                _rounding = self._u.width * 0.08
            if spaces < _rounding:
                tools.feedback(
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
                tools.feedback(
                    "Multi- diagonal hatching not permissible in a notched Rectangle",
                    True,
                )
        # ---- set canvas
        self.set_canvas_props(
            index=ID,
            stroke=self.hatch_stroke,
            stroke_width=self.hatch_stroke_width,
            stroke_cap=self.hatch_cap,
        )
        # ---- draw items
        if num >= 1:
            if "ne" in _dirs or "sw" in _dirs or "d" in _dirs:  # UP to the right
                pth = cnv.beginPath()
                pth.moveTo(vertices[0].x, vertices[0].y)
                pth.lineTo(vertices[2].x, vertices[2].y)
                cnv.drawPath(
                    pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0
                )
            if "se" in _dirs or "nw" in _dirs or "d" in _dirs:  # DOWN to the right
                pth = cnv.beginPath()
                pth.moveTo(vertices[1].x, vertices[1].y)
                pth.lineTo(vertices[3].x, vertices[3].y)
                cnv.drawPath(
                    pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0
                )
            if "n" in _dirs or "s" in _dirs or "o" in _dirs:  # vertical
                x_dist = self._u.width / (num + 1)
                for i in range(1, num + 1):
                    pth = cnv.beginPath()
                    pth.moveTo(vertices[0].x + i * x_dist, vertices[1].y)
                    pth.lineTo(vertices[0].x + i * x_dist, vertices[0].y)
                    cnv.drawPath(
                        pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0
                    )
            if "e" in _dirs or "w" in _dirs or "o" in _dirs:  # horizontal
                y_dist = self._u.height / (num + 1)
                for i in range(1, num + 1):
                    pth = cnv.beginPath()
                    pth.moveTo(vertices[0].x, vertices[0].y + i * y_dist)
                    pth.lineTo(
                        vertices[0].x + self._u.width, vertices[0].y + i * y_dist
                    )
                    cnv.drawPath(
                        pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0
                    )
        if num >= 1:
            diag_num = int((num - 1) / 2 + 1)
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

        if "ne" in _dirs or "sw" in _dirs or "d" in _dirs:  # slope UP to the right
            for i in range(1, diag_num):  # top-left side
                j = diag_num - i
                pth = cnv.beginPath()
                pth.moveTo(left_pt[i].x, left_pt[i].y)
                pth.lineTo(top_pt[j].x, top_pt[j].y)
                cnv.drawPath(
                    pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0
                )
            for i in range(1, diag_num):  # bottom-right side
                j = diag_num - i
                pth = cnv.beginPath()
                pth.moveTo(btm_pt[i].x, btm_pt[i].y)
                pth.lineTo(rite_pt[j].x, rite_pt[j].y)
                cnv.drawPath(
                    pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0
                )
        if "se" in _dirs or "nw" in _dirs or "d" in _dirs:  # slope down to the right
            for i in range(1, diag_num):  # bottom-left side
                pth = cnv.beginPath()
                pth.moveTo(left_pt[i].x, left_pt[i].y)
                pth.lineTo(btm_pt[i].x, btm_pt[i].y)
                cnv.drawPath(
                    pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0
                )
            for i in range(1, diag_num):  # top-right side
                pth = cnv.beginPath()
                pth.moveTo(top_pt[i].x, top_pt[i].y)
                pth.lineTo(rite_pt[i].x, rite_pt[i].y)
                cnv.drawPath(
                    pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0
                )

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a rectangle on a given canvas."""
        kwargs = self.kwargs | kwargs
        # tools.feedback(f' @@@ Rect.draw {kwargs=}')
        cnv = cnv.canvas if cnv else self.canvas.canvas
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- updated based on kwargs
        self.rounding = kwargs.get("rounding", self.rounding)
        self.grid_marks = kwargs.get("grid_marks", self.grid_marks)
        # ---- validate properties
        is_notched = True if (self.notch or self.notch_x or self.notch_y) else False
        is_chevron = True if (self.chevron or self.chevron_height) else False
        is_peaks = True if self.peaks else False
        is_borders = True if self.borders else False
        if (self.rounding or self.rounded) and is_borders:
            tools.feedback("Cannot use rounding or rounded with borders.", True)
        if (self.rounding or self.rounded) and is_notched:
            tools.feedback("Cannot use rounding or rounded with notch.", True)
        if (self.rounding or self.rounded) and is_chevron:
            tools.feedback("Cannot use rounding or rounded with chevron.", True)
        if (self.rounding or self.rounded) and is_peaks:
            tools.feedback("Cannot use rounding or rounded with peaks.", True)
        if self.hatch_count and is_notched and self.hatch_count > 1:
            tools.feedback("Cannot use multiple hatches with notch.", True)
        if self.hatch_count and is_chevron:
            tools.feedback("Cannot use hatch_count with chevron.", True)
        if is_notched and is_chevron:
            tools.feedback("Cannot use notch and chevron together.", True)
        if is_notched and is_peaks:
            tools.feedback("Cannot use notch and peaks together.", True)
        if is_chevron and is_peaks:
            tools.feedback("Cannot use chevron and peaks together.", True)
        if self.hatch_count and is_peaks:
            tools.feedback("Cannot use hatch_count and peaks together.", True)
        if is_borders and (is_chevron or is_peaks or is_notched):
            tools.feedback(
                "Cannot use borders with any of: hatch, peaks or chevron.", True
            )
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
        # ---- handle rotation: START
        rotation = kwargs.get("rotation", self.rotation)
        # print(self.label, rotation)
        if rotation:
            # tools.feedback(f'*** Rect {ID=} {rotation=} {self._u.x=}, {self._u.y=}')
            cnv.saveState()
            # move the canvas origin
            if ID is not None:
                cnv.translate(x + self._u.margin_left, y + self._u.margin_bottom)
            else:
                cnv.translate(x + self._u.width / 2.0, y + self._u.height / 2.0)
            cnv.rotate(rotation)
            # reset centre and "bottom left"
            x_d, y_d = 0, 0
            x = -self._u.width / 2.0
            y = -self._u.height / 2.0
        # ---- * notch vertices
        if is_notched:
            _notch_style = self.notch_style.lower()
            if _notch_style in ["b", "bite"]:
                tools.feedback('The "bite" setting is not implemented yet', False)
            if self.notch_corners:
                _ntches = self.notch_corners.split()
                _notches = [str(ntc).upper() for ntc in _ntches]
            # tools.feedback(f'*** Rect {self.notch_x=} {self.notch_y=} {_notches=} ')
            n_x = self.unit(self.notch_x) if self.notch_x else self.unit(self.notch)
            n_y = self.unit(self.notch_y) if self.notch_y else self.unit(self.notch)
            self.vertices = []
            if "SW" in _notches:
                self.vertices.append(Point(x, y + n_y))
                match _notch_style:
                    case "snip" | "s":
                        pass
                    case "fold" | "d":
                        self.vertices.append(Point(x, y))
                        self.vertices.append(Point(x + n_x, y))
                        self.vertices.append(Point(x, y + n_y))
                    case "flap" | "p":
                        self.vertices.append(Point(x + n_x, y + n_y))
                        self.vertices.append(Point(x + n_x, y))
                        self.vertices.append(Point(x, y + n_y))
                    case "step" | "t":
                        pass
                    case "bite" | "b":
                        # TODO - write code ...
                        pass
            else:
                self.vertices.append(Point(x, y))
            if "NW" in _notches:
                self.vertices.append(Point(x, y + self._u.height - n_y))
                match _notch_style:
                    case "snip" | "s":
                        self.vertices.append(Point(x + n_x, y + self._u.height))
                    case "fold" | "d":
                        self.vertices.append(Point(x + n_x, y + self._u.height))
                        self.vertices.append(Point(x, y + self._u.height))
                        self.vertices.append(Point(x, y + self._u.height - n_y))
                        self.vertices.append(Point(x + n_x, y + self._u.height))
                    case "flap" | "p":
                        self.vertices.append(Point(x + n_x, y + self._u.height))
                        self.vertices.append(Point(x + n_x, y + self._u.height - n_y))
                        self.vertices.append(Point(x, y + self._u.height - n_y))
                        self.vertices.append(Point(x + n_x, y + self._u.height))
                    case "step" | "t":
                        self.vertices.append(Point(x + n_x, y + self._u.height - n_y))
                        self.vertices.append(Point(x + n_x, y + self._u.height))
                    case "bite" | "b":
                        # TODO - write code ...
                        pass
            else:
                self.vertices.append(Point(x, y + self._u.height))
            if "NE" in _notches:
                self.vertices.append(Point(x + self._u.width - n_x, y + self._u.height))
                match _notch_style:
                    case "snip" | "s":
                        self.vertices.append(
                            Point(x + self._u.width, y + self._u.height - n_y)
                        )
                    case "fold" | "d":
                        self.vertices.append(
                            Point(x + self._u.width, y + self._u.height - n_y)
                        )
                        self.vertices.append(
                            Point(x + self._u.width, y + self._u.height)
                        )
                        self.vertices.append(
                            Point(x + self._u.width - n_x, y + self._u.height)
                        )
                        self.vertices.append(
                            Point(x + self._u.width, y + self._u.height - n_y)
                        )
                    case "flap" | "p":
                        self.vertices.append(
                            Point(x + self._u.width, y + self._u.height - n_y)
                        )
                        self.vertices.append(
                            Point(x + self._u.width - n_x, y + self._u.height - n_y)
                        )
                        self.vertices.append(
                            Point(x + self._u.width - n_x, y + self._u.height)
                        )
                        self.vertices.append(
                            Point(x + self._u.width, y + self._u.height - n_y)
                        )
                    case "step" | "t":
                        self.vertices.append(
                            Point(x + self._u.width - n_x, y + self._u.height - n_y)
                        )
                        self.vertices.append(
                            Point(x + self._u.width, y + self._u.height - n_y)
                        )
                    case "bite" | "b":
                        # TODO - write code ...
                        pass
            else:
                self.vertices.append(Point(x + self._u.width, y + self._u.height))
            if "SE" in _notches:
                self.vertices.append(Point(x + self._u.width, y + n_y))
                match _notch_style:
                    case "snip" | "s":
                        self.vertices.append(Point(x + self._u.width - n_x, y))
                    case "fold" | "d":
                        self.vertices.append(Point(x + self._u.width - n_x, y))
                        self.vertices.append(Point(x + self._u.width, y))
                        self.vertices.append(Point(x + self._u.width, y + n_y))
                        self.vertices.append(Point(x + self._u.width - n_x, y))
                    case "flap" | "p":
                        self.vertices.append(Point(x + self._u.width - n_x, y))
                        self.vertices.append(Point(x + self._u.width - n_x, y + n_y))
                        self.vertices.append(Point(x + self._u.width, y + n_y))
                        self.vertices.append(Point(x + self._u.width - n_x, y))
                    case "step" | "t":
                        self.vertices.append(Point(x + self._u.width - n_x, y + n_y))
                        self.vertices.append(Point(x + self._u.width - n_x, y))
                    case "bite" | "b":
                        # TODO - write code ...
                        pass
            else:
                self.vertices.append(Point(x + self._u.width, y))
            if "SW" in _notches:
                match _notch_style:
                    case "snip" | "s":
                        self.vertices.append(Point(x + n_x, y))
                    case "fold" | "o":
                        self.vertices.append(Point(x + n_x, y))
                    case "flap" | "l":
                        self.vertices.append(Point(x + n_x, y))
                    case "step" | "t":
                        self.vertices.append(Point(x + n_x, y))
                        self.vertices.append(Point(x + n_x, y + n_y))
                        self.vertices.append(Point(x, y + n_y))
                    case "bite" | "b":
                        # TODO - write code ...
                        tools.feedback(
                            'The "bite" setting is not implemented yet', False
                        )
            else:
                self.vertices.append(Point(x, y))
        # ---- * peaks vertices
        elif is_peaks:
            half_height = self._u.height / 2.0
            half_width = self._u.width / 2.0
            self.vertices = []
            self.vertices.append(Point(x, y))  # start here!
            if "w" in self.peaks_dict.keys():
                _pt = self.unit(self.peaks_dict["w"])
                self.vertices.append(Point(x - _pt, y + half_height))
                self.vertices.append(Point(x, y + self._u.height))
            else:
                self.vertices.append(Point(x, y + self._u.height))
            if "n" in self.peaks_dict.keys():
                _pt = self.unit(self.peaks_dict["n"])
                self.vertices.append(Point(x + half_width, y + self._u.height + _pt))
                self.vertices.append(Point(x + self._u.width, y + self._u.height))
            else:
                self.vertices.append(Point(x + self._u.width, y + self._u.height))
            if "e" in self.peaks_dict.keys():
                _pt = self.unit(self.peaks_dict["e"])
                self.vertices.append(Point(x + +self._u.width + _pt, y + half_height))
                self.vertices.append(Point(x + self._u.width, y))
            else:
                self.vertices.append(Point(x + self._u.width, y))
            if "s" in self.peaks_dict.keys():
                _pt = self.unit(self.peaks_dict["s"])
                self.vertices.append(Point(x + half_width, y - _pt))
            else:
                self.vertices.append(Point(x, y))  # close() draws line back to start
        # ---- * chevron vertices
        elif is_chevron:
            try:
                _chevron_height = float(self.chevron_height)
            except:
                tools.feedback(
                    f"A chevron_height of {self.chevron_height} is not valid!", True
                )
            if _chevron_height <= 0:
                tools.feedback(
                    "The chevron_height must be greater than zero; "
                    f"not {self.chevron_height}.",
                    True,
                )
            delta_m = self.unit(_chevron_height)
            if not self.chevron:
                self.chevron = "N"
            self.vertices = []
            if self.chevron.upper() == "N":
                delta_m_up = delta_m
                self.vertices.append(Point(x, y))
                self.vertices.append(Point(x, y + self._u.height))
                self.vertices.append(
                    Point(x + self._u.width / 2.0, y + self._u.height + delta_m)
                )
                self.vertices.append(Point(x + self._u.width, y + self._u.height))
                self.vertices.append(Point(x + self._u.width, y))
                self.vertices.append(Point(x + self._u.width / 2.0, y + delta_m))
            elif self.chevron.upper() == "S":
                delta_m_down = delta_m
                self.vertices.append(Point(x, y))
                self.vertices.append(Point(x, y + self._u.height))
                self.vertices.append(
                    Point(x + self._u.width / 2.0, y + self._u.height - delta_m)
                )
                self.vertices.append(Point(x + self._u.width, y + self._u.height))
                self.vertices.append(Point(x + self._u.width, y))
                self.vertices.append(Point(x + self._u.width / 2.0, y - delta_m))
            elif self.chevron.upper() == "W":
                self.vertices.append(Point(x, y))
                self.vertices.append(Point(x - delta_m, y + self._u.height / 2.0))
                self.vertices.append(Point(x, y + self._u.height))
                self.vertices.append(Point(x + self._u.width, y + self._u.height))
                self.vertices.append(
                    Point(x + self._u.width - delta_m, y + self._u.height / 2.0)
                )
                self.vertices.append(Point(x + self._u.width, y))
            elif self.chevron.upper() == "E":
                self.vertices.append(Point(x, y))
                self.vertices.append(Point(x + delta_m, y + self._u.height / 2.0))
                self.vertices.append(Point(x, y + self._u.height))
                self.vertices.append(Point(x + self._u.width, y + self._u.height))
                self.vertices.append(
                    Point(x + self._u.width + delta_m, y + self._u.height / 2.0)
                )
                self.vertices.append(Point(x + self._u.width, y))
            else:
                self.vertices = self.get_vertices(**kwargs)
        else:
            self.vertices = self.get_vertices(**kwargs)
        # tools.feedback(f'*** Rect {len(self.vertices)=}')
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- draw rectangle
        if is_notched or is_chevron or is_peaks:
            pth = cnv.beginPath()
            pth.moveTo(*self.vertices[0])
            for vertex in self.vertices:
                pth.lineTo(*vertex)
            pth.close()
            cnv.drawPath(
                pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0
            )
        elif self.rounding:
            rounding = self.unit(self.rounding)
            cnv.roundRect(
                x,
                y,
                self._u.width,
                self._u.height,
                rounding,
                stroke=1 if self.stroke else 0,
                fill=1 if self.fill else 0,
            )
        elif self.rounded:
            _rounding = self._u.width * 0.08
            cnv.roundRect(
                x,
                y,
                self._u.width,
                self._u.height,
                _rounding,
                stroke=1 if self.stroke else 0,
                fill=1 if self.fill else 0,
            )
        else:
            cnv.rect(
                x,
                y,
                self._u.width,
                self._u.height,
                stroke=1 if self.stroke else 0,
                fill=1 if self.fill else 0,
            )
            # ---- * borders (override)
            if self.borders:
                if isinstance(self.borders, tuple):
                    self.borders = [
                        self.borders,
                    ]
                if not isinstance(self.borders, list):
                    tools.feedback(
                        'The "borders" property must be a list of sets or a set'
                    )
                for border in self.borders:
                    self.draw_border(cnv, border, ID)

        # ---- draw hatch
        if self.hatch_count:
            vertices = self.get_vertices(rotation=rotation, **kwargs)
            self.draw_hatch(cnv, ID, vertices, self.hatch_count)
        # ---- grid marks
        self.set_canvas_props(
            index=ID, stroke=self.grid_stroke, stroke_width=self.grid_stroke_width
        )
        if self.grid_marks:
            deltag = self.unit(self.grid_length)
            pth = cnv.beginPath()
            gx, gy = 0, y  # left-side
            pth.moveTo(gx, gy)
            pth.lineTo(deltag, gy)
            pth.moveTo(0, gy + self._u.height)
            pth.lineTo(deltag, gy + self._u.height)
            gx, gy = x, self.paper[1]  # top-side
            pth.moveTo(gx, gy)
            pth.lineTo(gx, gy - deltag)
            pth.moveTo(gx + self._u.width, gy)
            pth.lineTo(gx + self._u.width, gy - deltag)
            gx, gy = self.paper[0], y  # right-side
            pth.moveTo(gx, gy)
            pth.lineTo(gx - deltag, gy)
            pth.moveTo(gx, gy + self._u.height)
            pth.lineTo(gx - deltag, gy + self._u.height)
            gx, gy = x, 0  # bottom-side
            pth.moveTo(gx, gy)
            pth.lineTo(gx, gy + deltag)
            pth.moveTo(gx + self._u.width, gy)
            pth.lineTo(gx + self._u.width, gy + deltag)
            # done
            cnv.drawPath(pth, stroke=1, fill=1)
        # ---- fill pattern?
        if self.pattern:
            img, is_svg, is_dir = self.load_image(self.pattern)
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
                    # TODO - work out how to (a) fill and (b) cut off -- mask?
                    # assume DPI = 300?  72pt = 1" = 300px -see
                    # http://two.pairlist.net/pipermail/reportlab-users/2006-January/004670.html
                    # w, h = yourImage.size
                    # yourImage.crop((0, 30, w, h-30)).save(...)
                    cnv.drawImage(
                        img,
                        x=x,
                        y=y,
                        width=self._u.width,
                        height=self._u.height,
                        mask="auto",
                    )
        # ---- centred shape (with offset)
        if self.centre_shape:
            cshape_name = self.centre_shape.__class__.__name__
            if cshape_name in GRID_SHAPES_WITH_CENTRE:
                self.centre_shape.draw(
                    _abs_cx=x_d + self.unit(self.centre_shape_mx),
                    _abs_cy=y_d + self.unit(self.centre_shape_my),
                )
            elif cshape_name not in GRID_SHAPES_WITH_CENTRE:
                tools.feedback(f"Cannot draw a centered {cshape_name}!")
        # ---- cross
        self.draw_cross(cnv, x_d, y_d)
        # ---- dot
        self.draw_dot(cnv, x_d, y_d)
        # ---- text
        if kwargs and kwargs.get("rotation"):
            kwargs.pop("rotation")  # otherwise labels rotate again!
        self.draw_heading(
            cnv, ID, x_d, y_d + 0.5 * self._u.height + delta_m_up, **kwargs
        )
        self.draw_label(cnv, ID, x_d, y_d, **kwargs)
        self.draw_title(
            cnv, ID, x_d, y_d - 0.5 * self._u.height - delta_m_down, **kwargs
        )
        # ----  numbering
        self.set_coord(cnv, x_d, y_d)
        # ---- handle rotation: END
        if rotation:
            cnv.restoreState()
        # ---- set grid property
        self.grid = GridShape(label=self.coord_text, x=x_d, y=y_d, shape=self)


class RhombusShape(BaseShape):
    """
    Rhombus on a given canvas.
    """

    def get_vertices(self, **kwargs):
        """Calculate vertices of rhombus."""
        x_s, y_s = kwargs.get("x"), kwargs.get("y") + self._u.height / 2.0
        vertices = []
        vertices.append(Point(x_s, y_s))
        vertices.append(Point(x_s + self._u.width / 2.0, y_s + self._u.height / 2.0))
        vertices.append(Point(x_s + self._u.width, y_s))
        vertices.append(Point(x_s + self._u.width / 2.0, y_s - self._u.height / 2.0))
        return vertices

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a rhombus (diamond) on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv.canvas if cnv else self.canvas.canvas
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
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- calculated properties
        self.area = (self._u.width * self._u.height) / 2.0
        # ---- handle rotation: START
        rotation = kwargs.get("rotation", self.rotation)
        if rotation:
            # tools.feedback(f'*** RHOMB {ID=} {rotation=} {self._u.x=}, {self._u.y=}')
            cnv.saveState()
            # move the canvas origin
            if ID is not None:
                # cnv.translate(cx + self._u.margin_left, cy + self._u.margin_bottom)
                cnv.translate(cx, cy)
            else:
                cnv.translate(cx, cy)
            cnv.rotate(rotation)
            # reset centre and "bottom left"
            cx, cy = 0, 0
            x = -self._u.width / 2.0
            y = -self._u.height / 2.0
        # ---- draw rhombus
        self.vertices = self.get_vertices(cx=cx, cy=cy, x=x, y=y)
        pth = cnv.beginPath()
        pth.moveTo(*self.vertices[0])
        for vertex in self.vertices:
            pth.lineTo(*vertex)
        pth.close()
        cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0)
        # ---- borders (override)
        if self.borders:
            if isinstance(self.borders, tuple):
                self.borders = [
                    self.borders,
                ]
            if not isinstance(self.borders, list):
                tools.feedback('The "borders" property must be a list of sets or a set')
            for border in self.borders:
                self.draw_border(cnv, border, ID)
        # ---- dot
        self.draw_dot(cnv, x + self._u.width / 2.0, y + self._u.height / 2.0)
        # ---- cross
        self.draw_cross(cnv, x + self._u.width / 2.0, y + self._u.height / 2.0)
        # ---- text
        if kwargs and kwargs.get("rotation"):
            kwargs.pop("rotation")  # otherwise labels rotate again!
        self.draw_heading(
            cnv, ID, x + self._u.width / 2.0, y + self._u.height, **kwargs
        )
        self.draw_label(
            cnv, ID, x + self._u.width / 2.0, y + self._u.height / 2.0, **kwargs
        )
        self.draw_title(cnv, ID, x + self._u.width / 2.0, y, **kwargs)
        # ---- handle rotation: END
        if rotation:
            cnv.restoreState()


class RightAngledTriangleShape(BaseShape):
    """
    Right-angled Triangle on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        kwargs = self.kwargs | kwargs
        cnv = cnv.canvas if cnv else self.canvas.canvas
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # set sizes
        if self.height and not self.width:
            self._u.width = self._u.height
        if self.width and not self.height:
            self._u.height = self._u.width
        # calculate points
        x, y = self._u.x, self._u.y
        self.vertices = []
        self.vertices.append(Point(x, y))
        if not self.hand or not self.flip:
            tools.feedback(
                'Need to supply both "flip" and "hand" options! for triangle.',
                stop=True,
            )
        hand = self.hand.lower()
        flip = self.flip.lower()
        if hand == "west":
            x2 = x - self._u.width
        elif hand == "east":
            x2 = x + self._u.width
        if flip == "north":
            y2 = y + self._u.height
        elif flip == "south":
            y2 = y - self._u.height
        self.vertices.append(Point(x2, y2))
        self.vertices.append(Point(x2, y))
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- draw RA triangle
        x_sum, y_sum = 0, 0
        pth = cnv.beginPath()
        for key, vertex in enumerate(self.vertices):
            # shift to relative position
            x = vertex.x + self._o.delta_x
            y = vertex.y + self._o.delta_y
            x_sum += x
            y_sum += y
            if key == 0:
                pth.moveTo(x, y)
            pth.lineTo(x, y)
        pth.close()
        cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0)
        x_c, y_c = x_sum / 3.0, y_sum / 3.0  # centroid
        # ---- dot
        self.draw_dot(cnv, x_c, y_c)
        # ---- text
        self.draw_label(cnv, ID, x_c, y_c, **kwargs)


class SectorShape(BaseShape):
    """
    Sector on a given canvas. Aka "wedge". Aka "slice" or "pie slice".

    Note:
        * User supplies a "compass" angle i.e. degrees clockwise from North -
          but this must be converted to a "ReportLab" angle i.e. degrees
          anti-clockwise from East
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(SectorShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        self.kwargs = kwargs
        # ---- perform overrides
        self.radius = self.radius or self.diameter / 2.0
        if self.cx is None and self.x is None:
            tools.feedback("Either provide x or cx for Sector", True)
        if self.cy is None and self.y is None:
            tools.feedback("Either provide y or cy for Sector", True)
        if self.cx is not None and self.cy is not None:
            self.x = self.cx - self.radius
            self.y = self.cy - self.radius
            self.x_1 = self.cx + self.radius
            self.y_1 = self.cy + self.radius
            # tools.feedback(f'*** Sect {self.x=} {self.y=} {self.x1=} {self.y1=}')
        else:
            self.x_1 = self.x + 2.0 * self.radius
            self.y_1 = self.y + 2.0 * self.radius
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

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw sector on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv.canvas if cnv else self.canvas.canvas
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        if self.use_abs_c:
            self.x_c = self._abs_cx
            self.y_c = self._abs_cy
        # convert to using units
        x_1 = self.unit(self.x) + self._o.delta_x
        y_1 = self.unit(self.y) + self._o.delta_y
        x_2 = self.unit(self.x_1) + self._o.delta_x
        y_2 = self.unit(self.y_1) + self._o.delta_y
        # angles
        start = (450 - self.angle) % 360.0 - self.angle_width
        width = self.angle_width
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- draw sector
        cnv.wedge(
            x_1, y_1, x_2, y_2, start, width, stroke=1, fill=1 if self.fill else 0
        )


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
        cnv = cnv.canvas if cnv else self.canvas.canvas
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
            pth = cnv.beginPath()
            for key, vertex in enumerate(points):
                _x0, _y0 = float(vertex[0]), float(vertex[1])
                # convert to using units
                x = self.unit(_x0) + self._o.delta_x + x_offset
                y = self.unit(_y0) + self._o.delta_y + y_offset
                if key == 0:
                    pth.moveTo(x, y)
                pth.lineTo(x, y)
            pth.close()
            cnv.drawPath(
                pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0
            )
            # ---- centre?
            if self.cx and self.cy:
                x = self._u.cx + self._o.delta_x + x_offset
                y = self._u.cy + self._o.delta_y + y_offset
                # ---- * dot
                self.draw_dot(cnv, x, y)
                # ---- * cross
                self.draw_cross(cnv, x, y)
                # ---- * text
                self.draw_label(cnv, ID, x, y, **kwargs)
        else:
            tools.feedback("There are no points to draw the Polyshape", False, True)


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
        # tools.feedback(f'@Square@ {self.label=} // {off_x=}, {off_y=} {kwargs=}')
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
            # tools.feedback(f"INIT Old x:{x} Old y:{y} New X:{self.x} New Y:{self.y}")
        self.kwargs = kwargs

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a stadium on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv.canvas if cnv else self.canvas.canvas
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
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
        cx = x + self._u.width / 2.0
        cy = y + self._u.height / 2.0
        # ---- handle rotation: START
        rotation = kwargs.get("rotation", self.rotation)
        if rotation:
            # tools.feedback(f'*** Stad {ID=} {rotation=} {self._u.x=}, {self._u.y=}')
            cnv.saveState()
            # move the canvas origin
            if ID is not None:
                # cnv.translate(cx + self._u.margin_left, cy + self._u.margin_bottom)
                cnv.translate(cx, cy)
            else:
                cnv.translate(cx, cy)
            cnv.rotate(rotation)
            # reset centre and "bottom left"
            cx, cy = 0, 0
            x = -self._u.width / 2.0
            y = -self._u.height / 2.0
        # ---- vertices
        self.vertices = [  # clockwise from bottom-left; relative to centre
            Point(x, y),
            Point(x, y + self._u.height),
            Point(x + self._u.width, y + self._u.height),
            Point(x + self._u.width, y),
        ]
        # tools.feedback(f'*** Stad{len(self.vertices)=}')
        # ---- edges
        _edges = []
        if self.edges:
            if not isinstance(self.edges, list):
                __edges = self.edges.split()
            else:
                __edges = self.edges
            _edges = [edge.lower() for edge in __edges]
            # reverse order of vertices because curves are drawn anti-clockwise
            self.vertices = list(reversed(self.vertices))
            self.vertices.append(self.vertices[0])
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- draw rect fill only
        pth = cnv.beginPath()
        pth.moveTo(*self.vertices[0])
        for vertex in self.vertices:
            pth.lineTo(*vertex)
        pth.close()
        cnv.drawPath(pth, stroke=0, fill=1 if self.fill else 0)
        # ---- draw stadium
        pth = cnv.beginPath()
        pth.moveTo(*self.vertices[0])
        radius_lr = self._u.height / 2.0
        radius_tb = self._u.width / 2.0
        for count, vertex in enumerate(self.vertices):
            # draw half-circle at chosen stadium self.edges;
            # using Bezier, cannot get half-circle - need to use two quarter circles

            # vx, vy = self.points_to_value(vertex.x) - 1, self.points_to_value(vertex.y) - 1
            # tools.feedback(f'*** Stad {count=} vx={vx:.2f} vy={vy:.2f}')
            if count == 2 and ("w" in _edges or "west" in _edges):
                cx, cy = vertex.x, vertex.y - 0.5 * self._u.height
                # _cx, _cy = self.points_to_value(cx) - 1, self.points_to_value(cy) - 1
                # tools.feedback(f'*** Stad cx={_cx:.2f} cy={_cy:.2f}')
                top_curve = geoms.bezier_arc_segment(
                    cx, cy, radius_lr, radius_lr, 90, 180
                )
                bottom_curve = geoms.bezier_arc_segment(
                    cx, cy, radius_lr, radius_lr, 180, 270
                )
                pth.moveTo(*vertex)
                pth.curveTo(*top_curve[1])
                pth.curveTo(*bottom_curve[1])
            elif count == 1 and ("n" in _edges or "north" in _edges):
                cx, cy = vertex.x - 0.5 * self._u.width, vertex.y
                right_curve = geoms.bezier_arc_segment(
                    cx, cy, radius_tb, radius_tb, 0, 90
                )
                left_curve = geoms.bezier_arc_segment(
                    cx, cy, radius_tb, radius_tb, 90, 180
                )
                pth.moveTo(*vertex)
                pth.curveTo(*right_curve[1])
                pth.curveTo(*left_curve[1])
            elif count == 3 and ("s" in _edges or "south" in _edges):
                cx, cy = vertex.x + 0.5 * self._u.width, vertex.y
                left_curve = geoms.bezier_arc_segment(
                    cx, cy, radius_tb, radius_tb, 180, 270
                )
                right_curve = geoms.bezier_arc_segment(
                    cx, cy, radius_tb, radius_tb, 270, 360
                )
                pth.moveTo(*vertex)
                pth.curveTo(*left_curve[1])
                pth.curveTo(*right_curve[1])
                pth.moveTo(*self.vertices[3])
            elif count == 0 and ("e" in _edges or "east" in _edges):
                cx, cy = vertex.x, vertex.y + 0.5 * self._u.height
                bottom_curve = geoms.bezier_arc_segment(
                    cx, cy, radius_lr, radius_lr, 270, 360
                )
                top_curve = geoms.bezier_arc_segment(
                    cx, cy, radius_lr, radius_lr, 0, 90
                )
                pth.moveTo(*vertex)
                pth.curveTo(*bottom_curve[1])
                pth.curveTo(*top_curve[1])
            # no curve; use a regular line
            else:
                if count + 1 < len(self.vertices):
                    pth.lineTo(*self.vertices[count + 1])
        # pth.close()
        cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0)
        # ---- cross
        self.draw_cross(cnv, x + self._u.width / 2.0, y + self._u.height / 2.0)
        # ---- dot
        self.draw_dot(cnv, x + self._u.width / 2.0, y + self._u.height / 2.0)
        # ---- text
        if kwargs and kwargs.get("rotation"):
            kwargs.pop("rotation")  # otherwise labels rotate again!
        delta = radius_tb if "n" in _edges or "north" in _edges else 0.0
        self.draw_heading(
            cnv, ID, x + self._u.width / 2.0, y + self._u.height + delta, **kwargs
        )
        self.draw_label(
            cnv, ID, x + self._u.width / 2.0, y + self._u.height / 2.0, **kwargs
        )
        self.draw_title(cnv, ID, x + self._u.width / 2.0, y - delta, **kwargs)
        # ---- handle rotation: END
        if rotation:
            cnv.restoreState()


class StarShape(BaseShape):
    """
    Star on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a star on a given canvas."""
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        cnv = cnv.canvas if cnv else self.canvas.canvas
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
        # ---- handle rotation: START
        is_rotated = False
        rotation = kwargs.get("rotation", self.rotation)
        if rotation:
            is_rotated = True
            # tools.feedback(f'*** Star {ID=} {rotation=} {x=}, {y=}')
            cnv.saveState()
            # move the canvas origin
            if ID is not None:
                cnv.translate(x + self._u.margin_left, y + self._u.margin_bottom)
            else:
                cnv.translate(x, y)
            cnv.rotate(rotation)
            x, y = 0, 0
        # ---- draw star
        pth = cnv.beginPath()
        pth.moveTo(x, y + radius)
        angle = (2 * math.pi) * 2.0 / 5.0
        start_angle = math.pi / 2.0
        log.debug("Start self.vertices:%s", self.vertices)
        for vertex in range(self.vertices - 1):
            next_angle = angle * (vertex + 1) + start_angle
            x_1 = x + radius * math.cos(next_angle)
            y_1 = y + radius * math.sin(next_angle)
            pth.lineTo(x_1, y_1)
        pth.close()
        cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0)
        # ---- dot
        self.draw_dot(cnv, x, y)
        # ---- cross
        self.draw_cross(cnv, x, y)
        # ---- text
        if kwargs and kwargs.get("rotation"):
            kwargs.pop("rotation")  # otherwise labels rotate again!
        self.draw_heading(cnv, ID, x, y + radius, **kwargs)
        self.draw_label(cnv, ID, x, y, **kwargs)
        self.draw_title(cnv, ID, x, y - radius, **kwargs)
        # ---- handle rotation: END
        if rotation:
            cnv.restoreState()


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
        # tools.feedback(f'*** StarFld {color=} {size=} {position=}')
        cnv.setFillColor(color)
        cnv.setStrokeColor(color)
        cnv.circle(position.x, position.y, size, stroke=1, fill=1)

    def cluster_stars(self, cnv):
        tools.feedback("CLUSTER NOT IMPLEMENTED", True)
        for star in range(0, self.star_count):
            pass

    def random_stars(self, cnv):
        # tools.feedback(f'*** StarFld {self.enclosure=}')
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
                tools.feedback(f"{self.enclosure} IS NOT AN IMPLEMENTED SHAPE!", True)
            self.draw_star(cnv, x_y)
            stars += 1

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw StarField pattern on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv.canvas if cnv else self.canvas.canvas
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- settings
        if self.enclosure is None:
            self.enclosure = RectangleShape()
        # ---- calculations
        random.seed()
        area = math.sqrt(self.enclosure.calculate_area())
        self.star_count = round(self.density * self.points_to_value(area))
        # tools.feedback(f'*** StarFld {self.star_pattern =} {self.enclosure}')
        # tools.feedback(f'*** StarFld {area=} {self.density=} {self.star_count=}')
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
        """Draw text on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv.canvas if cnv else self.canvas.canvas
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
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- overrides for self.text / text value
        _locale = kwargs.get("locale", None)
        if _locale:
            self.text = tools.eval_template(self.text, _locale)
        _text = self.textify(ID)
        # tools.feedback(f'*** Text {_locale=} {self.text=} {_text=}', False)
        if _text is None or _text == "":
            tools.feedback("No text supplied for the Text shape!", False, True)
            return
        _text = str(_text)  # card data could be numeric
        if "\\u" in _text:
            _text = codecs.decode(_text, "unicode_escape")
        # ---- validations
        if self.transform is not None:
            _trans = str(self.transform).lower()
            if _trans in ["u", "upper", "uppercase"]:
                self.transform = "uppercase"
            elif _trans in ["l", "lower", "lowercase"]:
                self.transform = "lowercase"
            elif _trans in ["c", "caps", "capitals", "capitalise", "capitalize"]:
                self.transform = "capitalize"
            else:
                self.transform = None
        # ---- text style
        if self.wrap:
            _style = ParagraphStyle(name="sc")
            _style.textColor = self.stroke
            _style.backColor = self.fill
            _style.borderColor = self.outline_stroke
            _style.borderWidth = self.outline_width
            _style.alignment = self.to_alignment()
            _style.fontSize = self.font_size
            _style.fontName = self.font_name
            _style.leading = self.leading
            _style.textTransform = self.transform
            """
            # potential other properties
            leftIndent=0,
            rightIndent=0,
            firstLineIndent=0,
            spaceBefore=0,
            spaceAfter=0,
            bulletFontName='Times-Roman',
            bulletFontSize=10,
            bulletIndent=0,
            borderPadding= 0,
            borderRadius= None,
            allowWidows= 1,
            allowOrphans= 0,
            endDots=None,
            splitLongWords=1,
            """
            # tools.feedback(f'*** Text LONG-{ID} => _text:{_text}')
            try:
                para = Paragraph(_text, style=_style)
            except ValueError as err:
                if "name=sc" in str(err):
                    parts = str(err).split("name=sc")
                    _err = parts[1]
                else:
                    _err = err
                tools.feedback(f"Cannot create Text - {_err}", True)
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
                tools.feedback(msg, True, True)
            w, h = para.wrap(width, height)
            para.drawOn(cnv, x_t, y_t - h)  # start text from top of 'box'
        else:
            # tools.feedback(f"*** {x_t=} {y_t=} {_text=} {sequence=} {rotation=}")
            cnv.setFillColor(self.stroke)
            self.draw_multi_string(cnv, x_t, y_t, _text, rotation=rotation)


class TrapezoidShape(BaseShape):
    """
    Trapezoid on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        """."""
        super(TrapezoidShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        self.kwargs = kwargs
        if self.top >= self.width:
            tools.feedback("The top cannot be longer than the width!", True)
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
        if self.flip.lower() in ["s", "south"]:
            y = y + self._u.height
            cy = y - self._u.height / 2.0
        if self.cx is not None and self.cy is not None:
            return self._u.cx, self._u.cy, x, y
        else:
            return cx, cy, x, y

    def get_vertices(self, **kwargs):
        """Calculate vertices of trapezoid."""
        # set start
        _cx, _cy, _x, _y = self.calculate_xy()  # for direct call without draw()
        cx = kwargs.get("cx", _cx)
        cy = kwargs.get("cy", _cy)
        x = kwargs.get("x", _x)
        y = kwargs.get("y", _y)
        # build array
        sign = -1 if self.flip.lower() in ["s", "south"] else 1
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
        cnv = cnv.canvas if cnv else self.canvas.canvas
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- set canvas
        self.set_canvas_props(index=ID)
        cx, cy, x, y = self.calculate_xy()
        # ---- handle rotation: START
        rotation = kwargs.get("rotation", self.rotation)
        if rotation:
            # tools.feedback(f'*** TRAP {ID=} {rotation=} {self._u.x=}, {self._u.y=}')
            cnv.saveState()
            # reset centre and "bottom left"
            cx, cy = 0, 0
            x = -self._u.width / 2.0
            y = -self._u.height / 2.0
            # move the canvas origin
            if ID is not None:
                # cnv.translate(cx + self._u.margin_left, cy + self._u.margin_bottom)
                cnv.translate(cx, cy)
            else:
                cnv.translate(cx, cy)
            cnv.rotate(rotation)
        # ---- draw trapezoid
        self.vertices = self.get_vertices(cx=cx, cy=cy, x=x, y=y)
        pth = cnv.beginPath()
        pth.moveTo(*self.vertices[0])
        for vertex in self.vertices:
            pth.lineTo(*vertex)
        pth.close()
        cnv.drawPath(pth, stroke=1 if self.stroke else 0, fill=1 if self.fill else 0)
        sign = -1 if self.flip.lower() in ["s", "south"] else 1
        # ---- borders (override)
        if self.borders:
            if isinstance(self.borders, tuple):
                self.borders = [
                    self.borders,
                ]
            if not isinstance(self.borders, list):
                tools.feedback('The "borders" property must be a list of sets or a set')
            for border in self.borders:
                self.draw_border(cnv, border, ID)
        # ---- dot
        self.draw_dot(cnv, x + self._u.width / 2.0, y + sign * self._u.height / 2.0)
        # ---- cross
        self.draw_cross(cnv, x + self._u.width / 2.0, y + sign * self._u.height / 2.0)
        # ---- text
        if kwargs and kwargs.get("rotation"):
            kwargs.pop("rotation")  # otherwise labels rotate again!
        self.draw_heading(
            cnv, ID, x + self._u.width / 2.0, y + sign * self._u.height, **kwargs
        )
        self.draw_label(
            cnv, ID, x + self._u.width / 2.0, y + sign * self._u.height / 2.0, **kwargs
        )
        self.draw_title(cnv, ID, x + self._u.width / 2.0, y, **kwargs)
        # ---- handle rotation: END
        if rotation:
            cnv.restoreState()


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
        tools.feedback("The Common shape cannot be drawn.", True)


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
        cnv = cnv if cnv else self.canvas
        # super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        font_size = kwargs.get("font_size", self.font_size)
        # ---- set location and text
        x = self.kwargs.get("x", self._u.page_width / 2.0)  # centre across page
        y = self.unit(self.margin_bottom) / 2.0  # centre in margin
        text = kwargs.get("text") or "Page %s" % ID
        # tools.feedback(f'*** FooterShape {ID=} {text=} {x=} {y=} {font_size=}')
        # ---- draw footer
        self.draw_multi_string(
            cnv.canvas, x, y, text, align="centre", font_size=font_size
        )
