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
from protograf.base import (
    BaseShape,
    get_cache,
)
from protograf.shapes_circle import CircleShape
from protograf.shapes_rectangle import RectangleShape
from protograf.utils import colrs, geoms, tools, fonts
from protograf.utils.tools import _lower
from protograf.utils.constants import (
    BGG_IMAGES,
)
from protograf.utils.messaging import feedback
from protograf.utils.structures import (
    BBox,
    DirectionGroup,
    Point,
    PolyGeometry,
)  # named tuples
from protograf.utils.support import CACHE_DIRECTORY

log = logging.getLogger(__name__)
DEBUG = False


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
                    f'Unable to load image "{_source}"; please check name and location',
                    True,
                )
            else:
                feedback(
                    "Unable to load image - no name provided",
                    True,
                )
        # ---- centre
        x_c = x + width / 2.0
        y_c = y + height / 2.0
        # ---- cross
        self.draw_cross(cnv, x_c, y_c, rotation=kwargs.get("rotation"))
        # ---- dot
        self.draw_dot(cnv, x_c, y_c)
        # ---- text
        self.draw_heading(cnv, ID, x_c, y_c - height / 2.0, **kwargs)
        self.draw_label(cnv, ID, x_c, y_c, **kwargs)
        self.draw_title(cnv, ID, x_c, y_c + height / 2.0, **kwargs)


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

    def draw_nested(self, cnv, ID, centre: Point, **kwargs):
        """Draw concentric Arcs from the outer Arc inwards."""
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
                    "The nested value must either be a whole number "
                    "or a list of fractions.",
                    True,
                )
            if intervals:
                intervals.sort(reverse=True)
                # print(f'*** nested {intervals=}')
                for inter in intervals:
                    # ---- circumference point in units
                    p_P = geoms.point_on_circle(
                        centre, self._u.radius * inter, self.angle_start
                    )
                    # ---- draw sector
                    # feedback(
                    #     f'***Arc: {centre=} {self.angle_start=} {self.angle_width=}')
                    cnv.draw_sector(  # anti-clockwise from p_P; 90° default
                        (centre.x, centre.y),
                        (p_P.x, p_P.y),
                        self.angle_width,
                        fullSector=False,
                    )
                    kwargs["closed"] = False
                    kwargs["fill"] = None
                    self.set_canvas_props(cnv=cnv, index=ID, **kwargs)

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
        # ---- draw nested
        if self.nested:
            self.draw_nested(cnv, ID, p_C, **kwargs)


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
        # print(f"***2 {self._u.width=} {self.tail_width_u=}  {self.head_width_u=}  ")
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
        """Draw an arrow on a given canvas."""
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
        centre = circle.calculate_centre()
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
        keys["stroke_ends"] = self.radii_ends
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

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(DotShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        self.kwargs = kwargs
        # ---- perform overrides
        self.point_size = self.dot_width / 2.0  # diameter is 3 points ~ 1mm or 1/32"
        self.radius = self.points_to_value(self.point_size, globals.units)
        if self.cx is not None and self.cy is not None:
            self.x = self.cx - self.radius
            self.y = self.cy - self.radius
        else:
            self.cx = self.x + self.radius
            self.cy = self.y + self.radius
        # ---- RESET UNIT PROPS (last!)
        self.set_unit_properties()

    def calculate_centre(self) -> Point:
        """Calculate centre of Dot."""
        if self.use_abs_c:
            self.x_c = self._abs_cx
            self.y_c = self._abs_cy
        else:
            self.x_c = self._u.cx + self._o.delta_x
            self.y_c = self._u.cy + self._o.delta_y
        return Point(self.x_c, self.y_c)

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a dot on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # feedback(f"*** Dot {self._o.delta_x=} {self._o.delta_y=}")
        # ---- set centre
        ccentre = self.calculate_centre()  # self.x_c, self.y_c
        x, y = ccentre.x, ccentre.y
        self.fill = self.stroke
        center = muPoint(x, y)
        # ---- draw dot
        # feedback(f'*** Dot {size=} {x=} {y=}')
        cnv.draw_circle(center=center, radius=self._u.radius)
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
        # ---- centred shape (with offset)
        if self.centre_shape:
            if self.can_draw_centred_shape(self.centre_shape):
                self.centre_shape.draw(
                    _abs_cx=x + self.unit(self.centre_shape_mx),
                    _abs_cy=y + self.unit(self.centre_shape_my),
                )
        # ---- centred shapes (with offsets)
        if self.centre_shapes:
            self.draw_centred_shapes(self.centre_shapes, x, y)
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

    def draw_hatches(
        self, cnv, ID, side: float, vertices: list, num: int, rotation: float = 0.0
    ):
        _dirs = tools.validated_directions(
            self.hatches, DirectionGroup.HEX_POINTY_EDGE, "triangle hatch"
        )
        lines = tools.as_int(num, "hatcheses_count")
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
            stroke=self.hatches_stroke,
            stroke_width=self.hatches_stroke_width,
            stroke_ends=self.hatches_ends,
            dashed=self.hatches_dashed,
            dotted=self.hatches_dots,
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
        """Draw an equilateral triangle on a given canvas."""
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
            # y_off = height + centroid_to_vertex
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
        # ---- draw hatches
        if self.hatches_count:
            self.draw_hatches(
                cnv, ID, side, self.vertexes, self.hatches_count, rotation
            )
        # ---- centred shape (with offset)
        if self.centre_shape:
            if self.can_draw_centred_shape(self.centre_shape):
                self.centre_shape.draw(
                    _abs_cx=self.centroid.x + self.unit(self.centre_shape_mx),
                    _abs_cy=self.centroid.y + self.unit(self.centre_shape_my),
                )
        # ---- centred shapes (with offsets)
        if self.centre_shapes:
            self.draw_centred_shapes(
                self.centre_shapes, self.centroid.x, self.centroid.y
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


class LineShape(BaseShape):
    """
    Line on a given canvas.
    """

    def draw_connections(
        self, cnv=None, off_x=0, off_y=0, ID=None, shapes: list = None, **kwargs
    ):
        """Draw a line between two or more shapes."""
        if not isinstance(shapes, (list, tuple)) or len(shapes) < 2:
            feedback(
                "Connections can only be made using a list of two or more shapes!",
                False,
                True,
            )
            return False
        connections = []
        for idx, cshape in enumerate(shapes):
            if not isinstance(cshape, (CircleShape, DotShape)):
                feedback("Can only connect Circles or Dots!", True)
            if idx == len(shapes) - 1:
                continue
            if self.connections_style and _lower(self.connections_style) in [
                "s",
                "spoke",
            ]:
                shape_a, shape_b = shapes[0], shapes[idx + 1]
            else:
                shape_a, shape_b = cshape, shapes[idx + 1]
            centre_a = shape_a.calculate_centre()
            centre_b = shape_b.calculate_centre()
            # print(f"{centre_a=}, {centre_b=}")
            if isinstance(shape_a, (CircleShape, DotShape)) and isinstance(
                shape_b, (CircleShape, DotShape)
            ):
                compass, rotation = geoms.angles_from_points(centre_a, centre_b)
                if centre_b.x < centre_a.x and centre_b.y < centre_a.y:
                    rotation_a = 360.0 - rotation
                    rotation_b = 180 + rotation_a
                elif centre_b.x < centre_a.x and centre_b.y > centre_a.y:
                    rotation_b = 180 - rotation
                    rotation_a = 180 + rotation_b
                elif centre_b.x > centre_a.x and centre_b.y < centre_a.y:
                    rotation_a = 360 - rotation
                    rotation_b = 180 + rotation_a
                elif centre_b.x > centre_a.x and centre_b.y > centre_a.y:
                    rotation_b = 180 - rotation
                    rotation_a = 180 + rotation_b
                elif centre_b.y == centre_a.y:
                    rotation_a = rotation
                    rotation_b = 180 - rotation
                elif centre_b.x == centre_a.x:
                    rotation_a = 360 - rotation
                    rotation_b = rotation
                else:
                    rotation_a = rotation - 90
                    rotation_b = rotation + 90
                # print(f"{rotation_a=}, {rotation_b=}")
                pt_a = geoms.point_on_circle(centre_a, shape_a._u.radius, rotation_a)
                pt_b = geoms.point_on_circle(centre_b, shape_b._u.radius, rotation_b)
                connections.append((pt_a, pt_b))
        for conn in connections:
            klargs = draw_line(cnv, conn[0], conn[1], shape=self, **kwargs)
            self.set_canvas_props(cnv=cnv, index=ID, **klargs)  # shape.finish()
            self.draw_arrow(cnv, conn[0], conn[1], **kwargs)
        return True

    def draw_arrow(self, cnv, point_a, point_b, **kwargs):
        if (
            self.arrow
            or self.arrow_style
            or self.arrow_position
            or self.arrow_height
            or self.arrow_width
            or self.arrow_double
        ):
            self.draw_arrowhead(cnv, point_a, point_b, **kwargs)
            if self.arrow_double:
                self.draw_arrowhead(cnv, point_a, point_b, **kwargs)

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a line on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- connections draw
        if self.connections:
            if self.draw_connections(cnv, off_x, off_y, ID, self.connections, **kwargs):
                return
        # "normal" draw
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
        klargs = draw_line(cnv, Point(x, y), Point(x_1, y_1), shape=self, **kwargs)
        self.set_canvas_props(cnv=cnv, index=ID, **klargs)  # shape.finish()
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
        self.draw_arrow(cnv, Point(x, y), Point(x_1, y_1), **kwargs)


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
        if self.perbii:
            if isinstance(self.perbii, str):
                if _lower(self.perbii) in ["all", "*"]:
                    sides = tools.as_int(self.sides, "sides")
                    self.perbii = list(range(1, sides + 1))
                else:
                    self.perbii = tools.sequence_split(self.perbii)
            if not isinstance(self.perbii, list):
                feedback("The perbii value must be a list of numbers!", True)
        if self.cx is not None and self.cy is not None:
            self.x, self.y = self.cx, self.cy
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
            stroke_ends=self.mesh_ends,
        )
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

    def draw_perbii(
        self,
        cnv,
        ID,
        centre: Point = None,
        vertices: list = None,
        rotation: float = None,
    ):
        """Draw lines connecting the Polygon centre to the centre of each edge.

        Def:
            A perpendicular bisector ("perbii") of a chord is:
            A line passing through the center of circle such that it divides the
            chord into two equal parts and meets the chord at a right angle;
            for a polygon, each edge is effectively a chord.
        """
        if not centre:
            centre = self.get_center()
        if not vertices:
            vertices = self.get_vertexes(rotation=rotation)
        _perbii = []  # store angles to centre of edges (the "chords")
        _perbii_pts = []  # store centre Point of edges
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
            _perbii_pts.append(pc)
            _, angle = geoms.angles_from_points(centre, pc)
            angle = 360.0 - angle if angle > 0.0 else angle
            _perbii.append(angle)
        pb_offset = self.unit(self.perbii_offset, label="perbii offset") or 0
        pb_length = (
            self.unit(self.perbii_length, label="perbii length")
            if self.perbii_length
            else self.get_radius()
        )

        # ---- set perbii styles
        lkwargs = {}
        lkwargs["wave_style"] = self.kwargs.get("perbii_wave_style", None)
        lkwargs["wave_height"] = self.kwargs.get("perbii_wave_height", 0)
        for key, pb_angle in enumerate(_perbii):
            if self.perbii and key + 1 not in self.perbii:
                continue
            # points based on length of line, offset and the angle in degrees
            edge_pt = _perbii_pts[key]
            # print(f'*** {pb_angle=} {edge_pt=} {centre=}')
            if pb_offset is not None and pb_offset != 0:
                offset_pt = geoms.point_on_circle(centre, pb_offset, pb_angle)
                end_pt = geoms.point_on_line(offset_pt, edge_pt, pb_length)
                # print(f'*** {end_pt=} {offset_pt=}')
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
        # ---- set radii styles
        lkwargs = {}
        lkwargs["wave_style"] = self.kwargs.get("radii_wave_style", None)
        lkwargs["wave_height"] = self.kwargs.get("radii_wave_height", 0)
        for rad_angle in _radii:
            # points based on length of line, offset and the angle in degrees
            diam_pt = geoms.point_on_circle(centre, rad_length, rad_angle)
            if rad_offset is not None and rad_offset != 0:
                offset_pt = geoms.point_on_circle(centre, rad_offset, rad_angle)
                end_pt = geoms.point_on_line(offset_pt, diam_pt, rad_length)
                # print('***', rad_angle, offset_pt, f'{x_c=}, {y_c=}')
                start_point = offset_pt.x, offset_pt.y
                end_point = end_pt.x, end_pt.y
            else:
                start_point = centre.x, centre.y
                end_point = diam_pt.x, diam_pt.y
            # ---- draw a radii line
            draw_line(
                cnv,
                start_point,
                end_point,
                shape=self,
                **lkwargs,
            )

        self.set_canvas_props(
            cnv=cnv,
            index=ID,
            stroke=self.radii_stroke,
            stroke_width=self.radii_stroke_width,
            dashed=self.radii_dashed,
            dotted=self.radii_dotted,
        )

    def draw_slices(self, cnv, ID, centre: Point, vertexes: list, rotation=0):
        """Draw triangles inside the Polygon

        Args:
            ID: unique ID
            vertexes: list of Polygon's nodes as Points
            centre: the centre Point of the Polygon
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
        # ---- draw triangle per slice; iterate through colors as needed!
        # print(f'*** PS {slices_colors=} {vertexes=}')
        cid = 0
        for vid in range(0, len(vertexes)):
            scolor = slices_colors[cid]
            vnext = vid + 1 if vid < len(vertexes) - 1 else 0
            vertexes_slice = [vertexes[vid], centre, vertexes[vnext]]
            cnv.draw_polyline(vertexes_slice)
            self.set_canvas_props(
                index=ID,
                stroke=self.slices_stroke or scolor,
                stroke_ends=self.slices_ends,
                fill=scolor,
                transparency=self.slices_transparency,
                closed=True,
                rotation=rotation,
                rotation_point=muPoint(centre[0], centre[1]),
            )
            cid += 1
            if cid > len(slices_colors) - 1:
                cid = 0

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
        vertices = geoms.polygon_vertices(self.sides, radius, Point(x, y), None)
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
        vertices = geoms.polygon_vertices(self.sides, radius, Point(x, y), None)
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
        # vertices = geoms.polygon_vertices(self.sides, radius, Point(x, y), None)
        # ---- invalid polygon?
        if not vertices or len(vertices) == 0:
            return
        # ---- draw polygon
        # feedback(f"***Polygon {self.col=} {self.row=} {x=} {y=} {vertices=}")
        cnv.draw_polyline(vertices)
        kwargs["closed"] = True
        self.set_canvas_props(cnv=cnv, index=ID, **kwargs)
        # ---- draw slices
        if self.slices:
            self.draw_slices(
                cnv,
                ID,
                Point(x, y),
                vertices,
                rotation=kwargs.get("rotation"),
            )
        # ---- draw radii
        if self.radii:
            self.draw_radii(cnv, ID, Point(x, y), vertices)
        # ---- draw perbii
        if self.perbii:
            self.draw_perbii(cnv, ID, Point(x, y), vertices)
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
        # ---- centred shapes (with offsets)
        if self.centre_shapes:
            self.draw_centred_shapes(self.centre_shapes, x, y)
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

    def get_steps(self) -> list:
        """Get a list of step tuples."""
        steps = tools.tuple_split(self.steps)
        if not steps:
            steps = self.steps
        if not steps or len(steps) == 0:
            return None
        return steps

    def get_points(self) -> list:
        """Get a list of point tuples."""
        points = tools.tuple_split(self.points)
        if not points:
            points = self.points
        if not points or len(points) == 0:
            return None
        return points

    def get_vertexes(self):
        """Return polyline vertices in canvas units"""
        points = self.get_points()
        steps = self.get_steps()
        if points and steps:
            feedback(
                "Point values will supercede steps to draw the Polyline", False, True
            )
        if points:
            vertices = [
                Point(
                    self.unit(pt[0]) + self._o.delta_x,
                    self.unit(pt[1]) + self._o.delta_y,
                )
                for pt in points
            ]
            return vertices
        # print('***', f'{steps=}')
        if steps:
            vertices = []
            # start here...
            vertices.append(
                Point(
                    self.unit(self.x) + self._o.delta_x,
                    self.unit(self.y) + self._o.delta_y,
                )
            )
            if len(steps) > 0:
                for index, stp in enumerate(steps):
                    vertices.append(
                        Point(
                            vertices[index].x + self.unit(stp[0]),
                            vertices[index].y + self.unit(stp[1]),
                        )
                    )
                return vertices
        feedback("There are no points or steps to draw the Polyline", False, True)
        return None

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a polyline (multi-part line) on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- set vertices
        self.vertexes = self.get_vertexes()
        # ---- set line style
        lkwargs = {}
        lkwargs["wave_style"] = self.kwargs.get("wave_style", None)
        lkwargs["wave_height"] = self.kwargs.get("wave_height", 0)
        # ---- draw polyline
        # feedback(f'***PolyLineShp{x=} {y=} {self.vertexes=}')
        if self.vertexes:
            for key, vertex in enumerate(self.vertexes):
                if key < len(self.vertexes) - 1:
                    draw_line(
                        cnv, vertex, self.vertexes[key + 1], shape=self, **lkwargs
                    )
            kwargs["closed"] = False
            kwargs["fill"] = None
            self.set_canvas_props(cnv=cnv, index=ID, **kwargs)
        # ---- arrowhead
        if (
            self.arrow
            or self.arrow_style
            or self.arrow_position
            or self.arrow_height
            or self.arrow_width
            or self.arrow_double
        ) and self.vertexes:
            _vertexes = tools.as_point(self.vertexes)
            start, end = _vertexes[-2], _vertexes[-1]
            self.draw_arrowhead(cnv, start, end, **kwargs)
            if self.arrow_double:
                start, end = _vertexes[1], _vertexes[0]
                self.draw_arrowhead(cnv, start, end, **kwargs)


class QRCodeShape(BaseShape):
    """
    QRCode on a given canvas.
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
            light=colrs.rgb_to_hex(colrs.get_color(self.fill)),
            dark=colrs.rgb_to_hex(colrs.get_color(self.stroke)),
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

    def draw_hatches(
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
            self.hatches, DirectionGroup.CIRCULAR, "rhombus hatches"
        )
        _num = tools.as_int(num, "hatches_count")
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
            stroke=self.hatches_stroke,
            stroke_width=self.hatches_stroke_width,
            stroke_ends=self.hatches_ends,
            dashed=self.hatches_dashed,
            dotted=self.hatches_dots,
            rotation=rotation,
            rotation_point=muPoint(x_c, y_c),
        )

    def draw_slices(self, cnv, ID, vertexes, centre: tuple, rotation=0):
        """Draw triangles inside the Rhombus

        Args:
            ID: unique ID
            vertexes: the Rhombus's nodes
            centre: the centre Point of the Rhombus
            rotation: degrees anti-clockwise from horizontal "east"
        """
        # ---- get slices color list from string
        if isinstance(self.slices, str):
            _slices = tools.split(self.slices.strip())
        else:
            _slices = self.slices
        # ---- validate slices color settings
        err = ("slices must be a list of colors - either 2 or 4",)
        if not isinstance(_slices, list):
            feedback(err, True)
        else:
            if len(_slices) not in [2, 3, 4]:
                feedback(err, True)
        slices_colors = [
            colrs.get_color(slcolor)
            for slcolor in _slices
            if not isinstance(slcolor, bool)
        ]
        # ---- draw 2 triangles
        if len(_slices) == 2:
            # left
            vertexes_left = [vertexes[1], vertexes[2], vertexes[3]]
            cnv.draw_polyline(vertexes_left)
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
            # right
            vertexes_right = [vertexes[0], vertexes[1], vertexes[3]]
            cnv.draw_polyline(vertexes_right)
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

        elif len(_slices) == 3 and _slices[2]:
            # top
            vertexes_top = [vertexes[0], vertexes[3], vertexes[2]]
            cnv.draw_polyline(vertexes_top)
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
            # bottom
            vertexes_btm = [vertexes[0], vertexes[1], vertexes[2]]
            cnv.draw_polyline(vertexes_btm)
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

        # ---- draw 4 triangles
        elif len(_slices) == 4:
            midpt = Point(centre[0], centre[1])
            vert_bl = [vertexes[0], midpt, vertexes[1]]
            vert_br = [vertexes[1], midpt, vertexes[2]]
            vert_tr = [vertexes[2], midpt, vertexes[3]]
            vert_tl = [vertexes[3], midpt, vertexes[0]]
            # sections = [vert_l, vert_r, vert_t, vert_b]  # order is important!
            sections = [vert_tr, vert_br, vert_bl, vert_tl]  # order is important!
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
        centre = (cx, cy)
        # ---- calculated properties
        self.area = (self._u.width * self._u.height) / 2.0
        # ---- handle rotation
        rotation = kwargs.get("rotation", self.rotation)
        if rotation:
            self.centroid = muPoint(cx, cy)
            kwargs["rotation"] = rotation
            kwargs["rotation_point"] = self.centroid
        else:
            self.centroid = None
        # ---- draw rhombus
        self.vertexes = self.get_vertexes(cx=cx, cy=cy, x=x, y=y)
        # feedback(f'***Rhombus {x=} {y=} {self.vertexes=}')
        cnv.draw_polyline(self.vertexes)
        kwargs["closed"] = True
        self.set_canvas_props(cnv=cnv, index=ID, **kwargs)
        # ---- draw slices after base
        if self.slices:
            self.draw_slices(cnv, ID, self.vertexes, centre, rotation)
        # ---- draw hatches
        if self.hatches_count:
            self.side = math.sqrt(
                (self._u.width / 2.0) ** 2 + (self._u.height / 2.0) ** 2
            )
            self.draw_hatches(
                cnv, ID, cx, cy, self.side, self.vertexes, self.hatches_count, rotation
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

        # ---- centred shape (with offset)
        if self.centre_shape:
            if self.can_draw_centred_shape(self.centre_shape):
                self.centre_shape.draw(
                    _abs_cx=cx + self.unit(self.centre_shape_mx),
                    _abs_cy=cy + self.unit(self.centre_shape_my),
                )
        # ---- centred shapes (with offsets)
        if self.centre_shapes:
            self.draw_centred_shapes(self.centre_shapes, cx, cy)
        # ---- dot
        self.draw_dot(cnv, cx, y + self._u.height / 2.0)
        # ---- cross
        self.draw_cross(
            cnv,
            cx,
            y + self._u.height / 2.0,
            rotation=kwargs.get("rotation"),
        )
        # ---- text
        y_off = self._u.height / 2.0
        self.draw_heading(cnv, ID, cx, cy - y_off, **kwargs)
        self.draw_label(cnv, ID, cx, cy, **kwargs)
        self.draw_title(cnv, ID, cx, cy + y_off, **kwargs)


class RightAngledTriangleShape(BaseShape):
    """
    Right-angled Triangle on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a right-angled triangle on a given canvas."""
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
        hand = _lower(self.hand)
        flip = _lower(self.flip)
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
    Sector on a given canvas.

    Note:
        * Sector can be referred to as a "wedge", "slice" or "pie slice".
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

    def get_steps(self) -> list:
        """Get a list of step tuples."""
        steps = tools.tuple_split(self.steps)
        if not steps:
            steps = self.steps
        if not steps or len(steps) == 0:
            return None
        return steps

    def get_points(self) -> list:
        """Get a list of point tuples."""
        points = tools.tuple_split(self.points)
        if not points:
            points = self.points
        if not points or len(points) == 0:
            return None
        return points

    def get_vertexes(self):
        """Return polyline vertices in canvas units"""
        points = self.get_points()
        steps = self.get_steps()
        if points and steps:
            feedback(
                "Point values will supercede steps to draw the Polyshape", False, True
            )
        if points:
            vertices = [
                Point(
                    self.unit(pt[0]) + self.unit(self.x) + self._o.delta_x,
                    self.unit(pt[1]) + self.unit(self.y) + self._o.delta_y,
                )
                for pt in points
            ]
            return vertices
        # print('***', f'{steps=}')
        if steps:
            vertices = []
            # start here...
            vertices.append(
                Point(
                    self.unit(self.x) + self._o.delta_x,
                    self.unit(self.y) + self._o.delta_y,
                )
            )
            if len(steps) > 0:
                for index, stp in enumerate(steps):
                    vertices.append(
                        Point(
                            vertices[index].x + self.unit(stp[0]),
                            vertices[index].y + self.unit(stp[1]),
                        )
                    )
                return vertices
        feedback("There are no points or steps to draw the Polyshape", False, True)
        return None

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw an irregular polygon on a given canvas."""
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        # ---- set canvas
        self.set_canvas_props(index=ID)
        x_offset, y_offset = self.unit(self.x or 0), self.unit(self.y or 0)
        # ---- set vertices
        self.vertexes = self.get_vertexes()
        # ---- set line style
        lkwargs = {}
        lkwargs["wave_style"] = self.kwargs.get("wave_style", None)
        lkwargs["wave_height"] = self.kwargs.get("wave_height", 0)
        # ---- draw polyshape
        # feedback(f'***PolyShape{x=} {y=} {self.vertexes=}')
        if self.vertexes:
            for key, vertex in enumerate(self.vertexes):
                if key < len(self.vertexes) - 1:
                    draw_line(
                        cnv, vertex, self.vertexes[key + 1], shape=self, **lkwargs
                    )
                else:
                    draw_line(cnv, vertex, self.vertexes[0], shape=self, **lkwargs)
            # cnv.draw_polyline(self.vertexes)
            kwargs["closed"] = True
            if kwargs.get("rounded"):
                kwargs["lineJoin"] = 1
            self.set_canvas_props(cnv=cnv, index=ID, **kwargs)
            # ---- is there a centre?
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
            feedback("There are no points or steps to draw the Polyshape", False, True)


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
            # feedback(f"*** STADIUM OldX:{x} OldY:{y} NewX:{self.x} NewY:{self.y}")
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
        # radius_lr = self._u.height / 2.0
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

        # ---- centred shape (with offset)
        if self.centre_shape:
            if self.can_draw_centred_shape(self.centre_shape):
                self.centre_shape.draw(
                    _abs_cx=cx + self.unit(self.centre_shape_mx),
                    _abs_cy=cy + self.unit(self.centre_shape_my),
                )
        # ---- centred shapes (with offsets)
        if self.centre_shapes:
            self.draw_centred_shapes(self.centre_shapes, cx, cy)
        # ---- cross
        self.draw_cross(
            cnv,
            cx,
            cy,
            rotation=kwargs.get("rotation"),
        )
        # ---- dot
        self.draw_dot(cnv, cx, cy)
        # ---- text
        delta = radius_tb if "n" in _edges or "north" in _edges else 0.0
        self.draw_heading(
            cnv,
            ID,
            cx,
            cy - delta,
            **kwargs,
        )
        self.draw_label(cnv, ID, cx, cy, **kwargs)
        self.draw_title(
            cnv,
            ID,
            cx,
            cy + delta,
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
        # TODO => text rotation
        # rotation = kwargs.get("rotation", self.rotation)
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
            _trans = _lower(self.transform)
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
        if self.box_stroke or self.box_fill or self.box_dashed or self.box_dotted:
            rkwargs = copy.copy(kwargs)
            rkwargs["fill"] = self.box_fill
            rkwargs["stroke"] = self.box_stroke
            rkwargs["stroke_width"] = self.box_stroke_width or self.stroke_width
            rkwargs["dashed"] = self.box_dashed
            rkwargs["dotted"] = self.box_dotted
            rkwargs["transparency"] = self.box_transparency
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
                # feedback(f'*** Text WRAP {kwargs=}=> \n{keys=} \n{rect=} \n{_text=}')
                if self.run_debug:
                    globals.doc_page.draw_rect(
                        rect, color=self.debug_color, dashes="[1 2] 0"
                    )
                keys["fontname"] = keys["mu_font"]
                keys.pop("mu_font")
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
        elif self.html or self.style:
            # insert_htmlbox(rect, text, *, css=None, scale_low=0,
            #   archive=None, rotate=0, oc=0, opacity=1, overlay=True)
            keys = {}
            try:
                keys["opacity"] = colrs.get_opacity(self.transparency)
                _font_name = self.font_name.replace(" ", "-")
                if not fonts.builtin_font(self.font_name):  # local check
                    _, _path, font_file = tools.get_font_file(self.font_name)
                    # if font_file:
                    #   keys["css"] = '@font-face {font-family: %s; src: url(%s);}' % (
                    #     _font_name, font_file)
                keys["css"] = globals.css
                if self.style:
                    _text = f'<div style="{self.style}">{_text}</div>'
                else:
                    # create a wrapper for the text
                    css_style = []
                    if self.font_name:
                        css_style.append(f"font-family: {_font_name};")
                    if self.font_size:
                        css_style.append(f"font-size: {self.font_size}px;")
                    if self.stroke:
                        if isinstance(self.stroke, tuple):
                            _stroke = colrs.rgb_to_hex(self.stroke)
                        else:
                            _stroke = self.stroke
                        css_style.append(f"color: {_stroke};")
                    if self.align:
                        if _lower(self.align) == "centre":
                            self.align = "center"
                        css_style.append(f"text-align: {self.align};")
                    styling = " ".join(css_style)
                    _text = f'<div style="{styling}">{_text}</div>'
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
            if _lower(self.flip) in ["s", "south"]:
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
        # cx = kwargs.get("cx", _cx)
        # cy = kwargs.get("cy", _cy)
        x = kwargs.get("x", _x)
        y = kwargs.get("y", _y)
        # build array
        sign = 1
        if self.flip and _lower(self.flip) in ["s", "south"]:
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
        if self.flip and _lower(self.flip) in ["s", "south"]:
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
