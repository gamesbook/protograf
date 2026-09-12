# -*- coding: utf-8 -*-
"""
protograf dice- and cubic-like shapes
"""

# lib
import random

# third party
from pymupdf import Point as muPoint

# module
from protograf import globals
from protograf.base import BaseShape
from protograf.shapes import (
    HexShape,
)
from protograf.shapes.utils import draw_line
from protograf.utils import colrs, geoms, tools
from protograf.utils.messaging import feedback
from protograf.utils.structures import (  # named tuples
    Point,
)
from protograf.utils.tools import _lower


class CubeObject(HexShape):
    """
    A pseudo-3D view of a cube as an isometric drawing.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super().__init__(_object=_object, canvas=canvas, **kwargs)
        # overrides
        self.orientation = "pointy"
        if not self.shades or self.radii_stroke != colrs.get_color(globals.black):
            self.radii = "s ne nw"

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a cube on a given canvas."""
        return super().draw(cnv, off_x, off_y, ID, **kwargs)


class DiceObject(BaseShape):
    """
    Parent class to handle common routines for all Shapes with a D6 'face'.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super().__init__(_object=_object, canvas=canvas, **kwargs)

    def draw_diamond(self, cnv, middle: float, radius: float):
        """Draw a Diamond shape based on a centre and radius."""
        centre = Point(middle[0], middle[1])
        pt1 = Point(centre.x, centre.y - radius)
        pt2 = Point(centre.x + radius, centre.y)
        pt3 = Point(centre.x, centre.y + radius)
        pt4 = Point(centre.x - radius, centre.y)
        cnv.draw_polyline((pt1, pt2, pt3, pt4, pt1))

    def draw_knot(
        self,
        cnv,
        position: str,
        offset: float,
        px: float,
        py: float,
        knot_shape: str,
        knot_radius: float,
    ):
        """Draw a knot on a vertex based on a position and the pip style.

        Args:
            position (str):
                an x-y coordinate as a Excel cell ref string;
                values for x runs from A to E, and y runs from 1 to 5
                or
                a single value from A to D representing the 4 inner points
            offset (float):
                distance between each vertex

        Note:
            * A knot is a slightly smaller shape than a pip, drawn on one of
              the vertices of an imaginary 5x5 grid overlaid onto the die face
        """
        pos_x, pos_y = None, None
        if len(position) == 1:
            match position:
                case "a" | "A":
                    pos_y, pos_x = 2, 2
                case "b" | "B":
                    pos_y, pos_x = 2, 4
                case "c" | "C":
                    pos_y, pos_x = 4, 2
                case "d" | "D":
                    pos_y, pos_x = 4, 4
                case _:
                    feedback(
                        "Invalid knot position - a single character must A, B, C or D",
                        True,
                    )
        else:
            try:
                pos_y = int(position[1])
                pos_x = tools.column_from_string(position[0])
            except Exception:
                feedback(
                    "Invalid knot position - must be a string with values A1..E5", True
                )
        if _lower(knot_shape) in ["circle", "c"]:
            offset_y = (pos_y - 3) * offset / 2  # negative for 1  & 2
            offset_x = (pos_x - 3) * offset / 2  # negative for 1  & 2
            cnv.draw_circle((px + offset_x, py + offset_y), knot_radius)
        else:
            raise NotImplementedError('No support for knot shape: "{knot_shape}"')

    def draw_pips(
        self,
        cnv,
        number: int,
        offset: float,
        px: float,
        py: float,
        pip_shape: str | BaseShape,
        pip_radius: float,
        rotation: float = 0,
        shape_name: str = "shape",
    ):
        """Draw pips based on a number (the 'pips') and the pip style."""
        pargs = {}

        if isinstance(pip_shape, BaseShape):
            if rotation:
                m_c = geoms._rotate_point_around_point(
                    Point(px, py), self.centroid, rotation
                )
                t_l = geoms._rotate_point_around_point(
                    Point(px - offset, py - offset), self.centroid, rotation
                )
                t_r = geoms._rotate_point_around_point(
                    Point(px + offset, py - offset), self.centroid, rotation
                )
                b_l = geoms._rotate_point_around_point(
                    Point(px - offset, py + offset), self.centroid, rotation
                )
                b_r = geoms._rotate_point_around_point(
                    Point(px + offset, py + offset), self.centroid, rotation
                )
                m_l = geoms._rotate_point_around_point(
                    Point(px - offset, py), self.centroid, rotation
                )
                m_r = geoms._rotate_point_around_point(
                    Point(px + offset, py), self.centroid, rotation
                )
                t_c = geoms._rotate_point_around_point(
                    Point(px, py - offset), self.centroid, rotation
                )
                b_c = geoms._rotate_point_around_point(
                    Point(px, py + offset), self.centroid, rotation
                )

            else:
                m_c = Point(px, py)
                t_l = Point(px - offset, py - offset)
                t_r = Point(px + offset, py - offset)
                b_l = Point(px - offset, py + offset)
                b_r = Point(px + offset, py + offset)
                m_l = Point(px - offset, py)
                m_r = Point(px + offset, py)
                t_c = Point(px, py - offset)
                b_c = Point(px, py + offset)

            match number:
                case 0:
                    pass  # blank face
                case 1:
                    kwargs = {"_abs_cx": m_c.x, "_abs_cy": m_c.y}
                    pip_shape.draw(**kwargs)
                case 2:
                    kwargs = {"_abs_cx": t_l.x, "_abs_cy": t_l.y}
                    pip_shape.draw(**kwargs)
                    kwargs = {"_abs_cx": b_r.x, "_abs_cy": b_r.y}
                    pip_shape.draw(**kwargs)
                case 3:
                    kwargs = {"_abs_cx": t_l.x, "_abs_cy": t_l.y}
                    pip_shape.draw(**kwargs)
                    kwargs = {"_abs_cx": m_c.x, "_abs_cy": m_c.y}
                    pip_shape.draw(**kwargs)
                    kwargs = {"_abs_cx": b_r.x, "_abs_cy": b_r.y}
                    pip_shape.draw(**kwargs)
                case 4:
                    kwargs = {"_abs_cx": t_l.x, "_abs_cy": t_l.y}
                    pip_shape.draw(**kwargs)
                    kwargs = {"_abs_cx": t_r.x, "_abs_cy": t_r.y}
                    pip_shape.draw(**kwargs)
                    kwargs = {"_abs_cx": b_l.x, "_abs_cy": b_l.y}
                    pip_shape.draw(**kwargs)
                    kwargs = {"_abs_cx": b_r.x, "_abs_cy": b_r.y}
                    pip_shape.draw(**kwargs)
                case 5:
                    kwargs = {"_abs_cx": t_l.x, "_abs_cy": t_l.y}
                    pip_shape.draw(**kwargs)
                    kwargs = {"_abs_cx": t_r.x, "_abs_cy": t_r.y}
                    pip_shape.draw(**kwargs)
                    kwargs = {"_abs_cx": m_c.x, "_abs_cy": m_c.y}
                    pip_shape.draw(**kwargs)
                    kwargs = {"_abs_cx": b_l.x, "_abs_cy": b_l.y}
                    pip_shape.draw(**kwargs)
                    kwargs = {"_abs_cx": b_r.x, "_abs_cy": b_r.y}
                    pip_shape.draw(**kwargs)
                case 6:
                    kwargs = {"_abs_cx": t_l.x, "_abs_cy": t_l.y}
                    pip_shape.draw(**kwargs)
                    kwargs = {"_abs_cx": t_r.x, "_abs_cy": t_r.y}
                    pip_shape.draw(**kwargs)
                    kwargs = {"_abs_cx": m_l.x, "_abs_cy": m_l.y}
                    pip_shape.draw(**kwargs)
                    kwargs = {"_abs_cx": m_r.x, "_abs_cy": m_r.y}
                    pip_shape.draw(**kwargs)
                    kwargs = {"_abs_cx": b_l.x, "_abs_cy": b_l.y}
                    pip_shape.draw(**kwargs)
                    kwargs = {"_abs_cx": b_r.x, "_abs_cy": b_r.y}
                    pip_shape.draw(**kwargs)
                case 7:
                    kwargs = {"_abs_cx": t_l.x, "_abs_cy": t_l.y}
                    pip_shape.draw(**kwargs)
                    kwargs = {"_abs_cx": t_r.x, "_abs_cy": t_r.y}
                    pip_shape.draw(**kwargs)
                    kwargs = {"_abs_cx": m_l.x, "_abs_cy": m_l.y}
                    pip_shape.draw(**kwargs)
                    kwargs = {"_abs_cx": m_c.x, "_abs_cy": m_c.y}
                    pip_shape.draw(**kwargs)
                    kwargs = {"_abs_cx": m_r.x, "_abs_cy": m_r.y}
                    pip_shape.draw(**kwargs)
                    kwargs = {"_abs_cx": b_l.x, "_abs_cy": b_l.y}
                    pip_shape.draw(**kwargs)
                    kwargs = {"_abs_cx": b_r.x, "_abs_cy": b_r.y}
                    pip_shape.draw(**kwargs)
                case 8:
                    kwargs = {"_abs_cx": t_l.x, "_abs_cy": t_l.y}
                    pip_shape.draw(**kwargs)
                    kwargs = {"_abs_cx": t_r.x, "_abs_cy": t_r.y}
                    pip_shape.draw(**kwargs)
                    kwargs = {"_abs_cx": m_l.x, "_abs_cy": m_l.y}
                    pip_shape.draw(**kwargs)
                    kwargs = {"_abs_cx": t_c.x, "_abs_cy": t_c.y}
                    pip_shape.draw(**kwargs)
                    kwargs = {"_abs_cx": b_c.x, "_abs_cy": b_c.y}
                    pip_shape.draw(**kwargs)
                    kwargs = {"_abs_cx": m_r.x, "_abs_cy": m_r.y}
                    pip_shape.draw(**kwargs)
                    kwargs = {"_abs_cx": b_l.x, "_abs_cy": b_l.y}
                    pip_shape.draw(**kwargs)
                    kwargs = {"_abs_cx": b_r.x, "_abs_cy": b_r.y}
                    pip_shape.draw(**kwargs)
                case 9:
                    kwargs = {"_abs_cx": t_l.x, "_abs_cy": t_l.y}
                    pip_shape.draw(**kwargs)
                    kwargs = {"_abs_cx": t_r.x, "_abs_cy": t_r.y}
                    pip_shape.draw(**kwargs)
                    kwargs = {"_abs_cx": m_l.x, "_abs_cy": m_l.y}
                    pip_shape.draw(**kwargs)
                    kwargs = {"_abs_cx": t_c.x, "_abs_cy": t_c.y}
                    pip_shape.draw(**kwargs)
                    kwargs = {"_abs_cx": m_c.x, "_abs_cy": m_c.y}
                    pip_shape.draw(**kwargs)
                    kwargs = {"_abs_cx": b_c.x, "_abs_cy": b_c.y}
                    pip_shape.draw(**kwargs)
                    kwargs = {"_abs_cx": m_r.x, "_abs_cy": m_r.y}
                    pip_shape.draw(**kwargs)
                    kwargs = {"_abs_cx": b_l.x, "_abs_cy": b_l.y}
                    pip_shape.draw(**kwargs)
                    kwargs = {"_abs_cx": b_r.x, "_abs_cy": b_r.y}
                    pip_shape.draw(**kwargs)
                case _:
                    feedback(f"The {shape_name} must use a number from 0 to 9", True)
            self.set_canvas_props(cnv=cnv, index=None, **pargs)
            return

        if _lower(pip_shape) in ["circle", "c"]:
            match number:
                case 0:
                    pass  # blank face
                case 1:
                    cnv.draw_circle((px, py), pip_radius)
                case 2:
                    cnv.draw_circle((px - offset, py - offset), pip_radius)
                    cnv.draw_circle((px + offset, py + offset), pip_radius)
                case 3:
                    cnv.draw_circle((px - offset, py - offset), pip_radius)
                    cnv.draw_circle((px, py), pip_radius)
                    cnv.draw_circle((px + offset, py + offset), pip_radius)
                case 4:
                    cnv.draw_circle((px - offset, py + offset), pip_radius)
                    cnv.draw_circle((px + offset, py - offset), pip_radius)
                    cnv.draw_circle((px - offset, py - offset), pip_radius)
                    cnv.draw_circle((px + offset, py + offset), pip_radius)
                case 5:
                    cnv.draw_circle((px - offset, py + offset), pip_radius)
                    cnv.draw_circle((px + offset, py - offset), pip_radius)
                    cnv.draw_circle((px - offset, py - offset), pip_radius)
                    cnv.draw_circle((px, py), pip_radius)
                    cnv.draw_circle((px + offset, py + offset), pip_radius)
                case 6:
                    cnv.draw_circle((px - offset, py + offset), pip_radius)
                    cnv.draw_circle((px + offset, py - offset), pip_radius)
                    cnv.draw_circle((px - offset, py - offset), pip_radius)
                    cnv.draw_circle((px + offset, py + offset), pip_radius)
                    cnv.draw_circle((px - offset, py), pip_radius)
                    cnv.draw_circle((px + offset, py), pip_radius)
                case 7:
                    cnv.draw_circle((px - offset, py + offset), pip_radius)
                    cnv.draw_circle((px + offset, py - offset), pip_radius)
                    cnv.draw_circle((px - offset, py - offset), pip_radius)
                    cnv.draw_circle((px + offset, py + offset), pip_radius)
                    cnv.draw_circle((px - offset, py), pip_radius)
                    cnv.draw_circle((px + offset, py), pip_radius)
                    cnv.draw_circle((px, py), pip_radius)  # centre
                case 8:
                    cnv.draw_circle((px - offset, py + offset), pip_radius)
                    cnv.draw_circle((px + offset, py - offset), pip_radius)
                    cnv.draw_circle((px - offset, py - offset), pip_radius)
                    cnv.draw_circle((px + offset, py + offset), pip_radius)
                    cnv.draw_circle((px - offset, py), pip_radius)
                    cnv.draw_circle((px + offset, py), pip_radius)
                    cnv.draw_circle((px, py - offset), pip_radius)
                    cnv.draw_circle((px, py + offset), pip_radius)
                case 9:
                    cnv.draw_circle((px - offset, py + offset), pip_radius)
                    cnv.draw_circle((px + offset, py - offset), pip_radius)
                    cnv.draw_circle((px - offset, py - offset), pip_radius)
                    cnv.draw_circle((px + offset, py + offset), pip_radius)
                    cnv.draw_circle((px - offset, py), pip_radius)
                    cnv.draw_circle((px + offset, py), pip_radius)
                    cnv.draw_circle((px, py - offset), pip_radius)
                    cnv.draw_circle((px, py + offset), pip_radius)
                    cnv.draw_circle((px, py), pip_radius)  # centre
                case _:
                    feedback(f"The {shape_name} must use a number from 0 to 9", True)
        elif _lower(pip_shape) in ["diamond", "d"]:
            match number:
                case 0:
                    pass  # blank face
                case 1:
                    self.draw_diamond(cnv, (px, py), pip_radius)
                case 2:
                    self.draw_diamond(cnv, (px - offset, py - offset), pip_radius)
                    self.draw_diamond(cnv, (px + offset, py + offset), pip_radius)
                case 3:
                    self.draw_diamond(cnv, (px - offset, py - offset), pip_radius)
                    self.draw_diamond(cnv, (px, py), pip_radius)
                    self.draw_diamond(cnv, (px + offset, py + offset), pip_radius)
                case 4:
                    self.draw_diamond(cnv, (px - offset, py + offset), pip_radius)
                    self.draw_diamond(cnv, (px + offset, py - offset), pip_radius)
                    self.draw_diamond(cnv, (px - offset, py - offset), pip_radius)
                    self.draw_diamond(cnv, (px + offset, py + offset), pip_radius)
                case 5:
                    self.draw_diamond(cnv, (px - offset, py + offset), pip_radius)
                    self.draw_diamond(cnv, (px + offset, py - offset), pip_radius)
                    self.draw_diamond(cnv, (px - offset, py - offset), pip_radius)
                    self.draw_diamond(cnv, (px, py), pip_radius)
                    self.draw_diamond(cnv, (px + offset, py + offset), pip_radius)
                case 6:
                    self.draw_diamond(cnv, (px - offset, py + offset), pip_radius)
                    self.draw_diamond(cnv, (px + offset, py - offset), pip_radius)
                    self.draw_diamond(cnv, (px - offset, py - offset), pip_radius)
                    self.draw_diamond(cnv, (px + offset, py + offset), pip_radius)
                    self.draw_diamond(cnv, (px - offset, py), pip_radius)
                    self.draw_diamond(cnv, (px + offset, py), pip_radius)
                case _:
                    feedback(f"The {shape_name} must use a number from 0 to 6", True)
        else:
            raise NotImplementedError('No support for pip shape: "{pip_shape}"')


class D6Object(DiceObject):
    """
    A top-down view of a six-sided (cubic) die
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super().__init__(_object=_object, canvas=canvas, **kwargs)
        # overrides to centre shape
        if self.cx is not None and self.cy is not None:
            self.x = self.cx - self.width / 2.0
            self.y = self.cy - self.height / 2.0
            # feedback(f"*** D6 OldX:{x} OldY:{y} NewX:{self.x} NewY:{self.y}")
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
        self.pips = tools.as_int(kwargs.get("pips", 1), "pips")
        self.random = tools.as_bool(kwargs.get("random", False))
        # defaults
        self._fill, self._stroke = (
            self.fill,
            self.stroke,
        )
        if "rounded" not in kwargs and "rounding" not in kwargs:
            self.rounded = True
        # validate
        correct, issue = self.validate_properties()
        if not correct:
            _items = "; ".join(issue)
            feedback(f"Problem with D6 settings: {_items}", True)

    def validate_properties(self):
        """Ensure all D6 settings are correct."""
        correct = True
        issue = []
        if self.random and self.pips is not None:
            issue.append("Both random and pips cannot be set at the same time!")
            correct = False
        if not self.random and self.pips not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
            issue.append("The value for pips must be a number from 0 to 9")
            correct = False
        if self.pip_fraction > 0.33 or self.pip_fraction < 0.1:
            issue.append("The pip_fraction must be between 0.1 and 0.33")
            correct = False
        return correct, issue

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw the D6 on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
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
        else:
            self.centroid = None
        # ---- calculate rounding
        # Specifies the radius of the curvature as percentage of rectangle side length
        # where 0.5 corresponds to 50% of the respective side.
        radius = None
        if self.rounded:
            radius = self.rounded_radius  # hard-coded OR from defaults
        if self.rounding:
            rounding = self.unit(self.rounding)
            radius = rounding / min(self._u.width, self._u.height)
        if radius and radius > 0.5:
            feedback("The rounding radius cannot exceed 50% of the D6 side.", True)
        # ---- draw the outline
        # feedback(f'*** D6 normal {radius=} {kwargs=}')
        cnv.draw_rect((x, y, x + self._u.width, y + self._u.height), radius=radius)
        self.set_canvas_props(cnv=cnv, index=ID, **kwargs)
        # ---- draw the pips
        if self.random:
            number = random.randint(1, 6)
        else:
            number = self.pips
        pip_radius = self.pip_fraction * self._u.width / 2.0
        px = x + self._u.width / 2.0
        py = y + self._u.height / 2.0
        offset = 3 * (0.2 * self._u.width / 2.0)  # fixed regardless of pip size
        self.draw_pips(
            cnv, number, offset, px, py, self.pip_shape, pip_radius, rotation, "D6"
        )
        # add style
        pargs = {}
        pargs["stroke"] = self.pip_stroke
        pargs["fill"] = self.pip_fill
        if rotation:
            pargs["rotation"] = rotation
            pargs["rotation_point"] = self.centroid
        self.set_canvas_props(cnv=None, index=ID, **pargs)
        # ---- draw the knot
        knot_position = kwargs.get("knot")
        if knot_position:
            knot_fill = kwargs.get("knot_fill", self.pip_fill)
            knot_stroke = kwargs.get("knot_stroke", knot_fill)
            knot_offset = 3 * (
                0.2 * self._u.width / 2.0
            )  # fixed regardless of pip size
            # knot_offset = 0.2 * self._u.width  # fixed regardless of pip size
            knot_radius = 0.66 * pip_radius
            self.draw_knot(
                cnv,
                knot_position,
                knot_offset,
                px,
                py,
                self.pip_shape,
                knot_radius,
            )
            # add style
            pargs = {}
            pargs["stroke"] = knot_stroke
            pargs["fill"] = knot_fill
            if rotation:
                pargs["rotation"] = rotation
                pargs["rotation_point"] = self.centroid
            self.set_canvas_props(cnv=None, index=ID, **pargs)
        # ---- cross
        self.draw_cross(cnv, cx, cy, rotation=kwargs.get("rotation"))
        # ---- dot
        self.draw_dot(cnv, cx, cy)
        # ---- text
        self.draw_heading(cnv, ID, cx, cy - 0.5 * self._u.height, **kwargs)
        self.draw_label(cnv, ID, cx, cy, **kwargs)
        self.draw_title(cnv, ID, cx, cy + 0.5 * self._u.height, **kwargs)


class DominoObject(DiceObject):
    """
    A top-down view of a domino playing piece
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super().__init__(_object=_object, canvas=canvas, **kwargs)
        # overrides to centre shape
        if self.cx is not None and self.cy is not None:
            self.x = self.cx - self.width / 2.0
            self.y = self.cy - self.height / 2.0
            # feedback(f"*** Domino OldX:{x} OldY:{y} NewX:{self.x} NewY:{self.y}")
        # overrides to make a "double square rectangle"
        if self.width and not self.side:
            self.side = 0.5 * self.width
        if self.height and not self.side:
            self.side = self.height
        self.height, self.width = self.side, 2.0 * self.side
        self.set_unit_properties()
        self.kwargs = kwargs
        self._label = self.label
        # custom/unique properties
        self.pips = kwargs.get("pips", (1, 1))
        self.random = tools.as_bool(kwargs.get("random", False))
        # defaults
        self._fill, self._stroke = (
            self.fill,
            self.stroke,
        )
        if "rounded" not in kwargs and "rounding" not in kwargs:
            self.rounded = True
        # validate
        correct, issue = self.validate_properties()
        if not correct:
            _items = "; ".join(issue)
            feedback(f"Problem with Domino settings: {_items}", True)

    def validate_properties(self):
        """Ensure all Domino settings are correct."""
        correct = True
        issue = []
        if self.random and self.pips is not None:
            issue.append("Both random and pips cannot be set at the same time!")
            correct = False
        if not self.random:
            if self.pips:
                if not isinstance(self.pips, (list, tuple)):
                    issue.append(
                        "The pips setting must be a pair of numbers, each between 0 to 6"
                    )
                    correct = False
                else:
                    allowed = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                    if self.pips[0] not in allowed or self.pips[1] not in allowed:
                        issue.append("Each pips value must be a number between 0 to 9")
                        correct = False
        if self.pip_fraction > 0.33 or self.pip_fraction < 0.1:
            issue.append("The pip_fraction must be between 0.1 and 0.33")
            correct = False
        return correct, issue

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw the Domino on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
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
        else:
            self.centroid = None
        # ---- calculate rounding
        # Specifies the radius of the curvature as percentage of rectangle side length
        # where 0.5 corresponds to 50% of the respective side.
        radius = None
        if self.rounded:
            radius = self.rounded_radius  # hard-coded OR from defaults
        if self.rounding:
            rounding = self.unit(self.rounding)
            radius = rounding / min(self._u.width, self._u.height)
        if radius and radius > 0.5:
            feedback("The rounding radius cannot exceed 50% of the Domino side.", True)
        # ---- draw the outline
        # feedback(f'*** Domino normal {radius=} {kwargs=} {self.pips=} {self.random=}')
        cnv.draw_rect((x, y, x + self._u.width, y + self._u.height), radius=radius)
        self.set_canvas_props(cnv=cnv, index=ID, **kwargs)
        # ---- draw centre line
        if self.centre_line:
            ctop = (cx, cy - 0.5 * self.unit(self.centre_line_length))
            cbtm = (cx, cy + 0.5 * self.unit(self.centre_line_length))
            lkwargs = {}
            lkwargs["wave_style"] = self.kwargs.get("centre_line_wave_style", None)
            lkwargs["wave_height"] = self.kwargs.get("centre_line_wave_height", 0)
            draw_line(cnv, ctop, cbtm, shape=self, **lkwargs)
            self.set_canvas_props(
                index=ID,
                stroke=self.centre_line_stroke or self.stroke,
                stroke_width=self.centre_line_stroke_width or self.stroke_width,
                stroke_ends=self.centre_line_ends,
                dashed=self.centre_line_dashed,
                dotted=self.centre_line_dotted,
                rotation=rotation,
                rotation_point=muPoint(cx, cy),
            )
        # ---- draw centre_shape
        if self.centre_shape:
            if self.can_draw_centred_shape(self.centre_shape):
                self.centre_shape.draw(
                    _abs_cx=cx + self.unit(self.centre_shape_mx),
                    _abs_cy=cy + self.unit(self.centre_shape_my),
                )
        # ---- draw the pips
        for face in [0, 1]:
            if self.random:
                number = random.randint(1, 6)
            else:
                number = self.pips[face]
                # feedback(f'*** Domino normal {face=} {number=}')
            pip_radius = self.pip_fraction * self._u.height / 2.0
            px = x + self._u.height / 2.0 + face * self._u.height
            py = y + self._u.height / 2.0
            offset = 3 * (0.2 * self._u.height / 2.0)  # fixed regardless of pip size
            self.draw_pips(
                cnv,
                number,
                offset,
                px,
                py,
                self.pip_shape,
                pip_radius,
                rotation,
                "Domino",
            )
            # self.set_canvas_props(cnv=None, index=ID, **kwargs)
        # ---- set style
        pargs = {}
        pargs["stroke"] = self.pip_stroke
        pargs["fill"] = self.pip_fill
        if rotation:
            pargs["rotation"] = rotation
            pargs["rotation_point"] = self.centroid
        self.set_canvas_props(cnv=None, index=ID, **pargs)
        # ---- cross
        self.draw_cross(cnv, cx, cy, rotation=kwargs.get("rotation"))
        # ---- dot
        self.draw_dot(cnv, cx, cy)
        # ---- text
        self.draw_heading(cnv, ID, cx, cy - 0.5 * self._u.height, **kwargs)
        self.draw_label(cnv, ID, cx, cy, **kwargs)
        self.draw_title(cnv, ID, cx, cy + 0.5 * self._u.height, **kwargs)
