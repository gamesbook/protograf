# -*- coding: utf-8 -*-
"""
Base shape - extended classes for protograf
"""
from protograf.base import BaseShape
from protograf.shapes_utils import draw_line
from protograf.utils.structures import Point
from protograf.utils import colrs, geoms, tools, support
from protograf.utils.messaging import feedback


class BasePolyShape(BaseShape):
    """
    Extension for common functions for Poly-shapes
    """

    def get_name(self) -> str:
        """Assign a user-friendly name based on class."""
        match self.__class__.__name__:
            case "PolylineShape":
                return "Polyline"
            case "ShapeShape":
                return "Polyshape"
            case _:
                raise NotImplementedError("Unknown BasePolyShape class!")

    def get_points(self) -> list:
        """Get a list of point tuples."""
        points = tools.tuple_split(self.points)
        if not points:
            points = self.points
        if not points or len(points) == 0:
            return None
        return points

    def get_steps(self) -> list:
        """Get a list of step tuples."""
        steps = tools.tuple_split(self.steps)
        if not steps:
            steps = self.steps
        if not steps or len(steps) == 0:
            return None
        return steps

    def draw_snail(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a Poly-shape line (multi-part line) on a given canvas via snail."""

        def is_float(value: str) -> bool:
            try:
                the_value = float(value)
                return True
            except (ValueError, Exception):
                return False

        def draw_or_jump(current_point: Point, distance: float, jump: bool) -> Point:
            """Draw a line or move to a new Point."""
            u_distance = self.unit(distance) * self.scaling  # convert distance to units
            # print('snail', current_dir, distance, u_distance)
            # ---- new point based on current_dir, u_distance
            new_point = geoms.point_from_angle(
                current_point, u_distance, 360 - current_dir
            )
            # ---- draw line from current_point to new_point
            if not jump:
                draw_line(
                    cnv,
                    current_point,
                    new_point,
                    shape=self,
                    **kwargs,
                )
            # ---- save new_point as current_point
            return new_point

        polytype = self.get_name()
        if not isinstance(self.snail, str):
            feedback("The {polytype} snail must be a space-separated string!", True)
        items = self.snail.split(" ")
        # print(f'*** snail {items=}')
        current_dir = 0  # face E by default
        start_point = Point(self._u.x + self._o.delta_x, self._u.y + self._o.delta_y)
        current_point = start_point
        # ---- iterate over all snail items
        for item in items:
            if not item:
                continue
            _item = str(item).lower()
            if _item in ["n", "e", "w", "s", "ne", "se", "sw", "nw"]:
                current_dir = tools.compass_to_rotation(_item)
            elif _item == "*":
                if self.__class__.__name__ == "ShapeShape":
                    tools.feedback(
                        f'The {polytype} snail cannot use move home ("{_item}").',
                        True,
                        True,
                    )
                current_point = start_point
            elif _item == "**":
                draw_line(
                    cnv,
                    current_point,
                    start_point,
                    shape=self,
                    **kwargs,
                )
                current_point = start_point
            elif _item[0] == "a":
                a_item = _item.strip("a")
                if not is_float(a_item):
                    tools.feedback(
                        f'The {polytype} snail angle "{_item}" is not valid.',
                        True,
                        True,
                    )
                else:
                    current_dir = float(a_item)
                    if current_dir < 0 or current_dir > 360:
                        tools.feedback(
                            f'The {polytype} snail angle "{a_item}" must be in the range 0 to 360.',
                            True,
                            True,
                        )
            elif _item[0] == "+" or _item[0] == "l":  # anti-clockwise
                a_item = _item.strip("+").strip("l")
                if not is_float(a_item):
                    tools.feedback(
                        f'The {polytype} snail angle "{_item}" is not valid.',
                        True,
                        True,
                    )
                else:
                    current_dir = current_dir + float(a_item)
                    if current_dir > 360:
                        current_dir = 360 - current_dir
                    if current_dir < 0 or current_dir > 360:
                        tools.feedback(
                            f'The {polytype} snail angle change "{_item}" must result in 0 to 360.',
                            True,
                            True,
                        )
            elif _item[0] == "-" or _item[0] == "r":  # clockwise
                a_item = _item.strip("-").strip("r")
                if not is_float(a_item):
                    tools.feedback(
                        f'The {polytype} snail angle "{_item}" is not valid.',
                        True,
                        True,
                    )
                else:
                    current_dir = current_dir - float(a_item)
                    if current_dir < 0:
                        current_dir = 360 + current_dir
                    if current_dir < 0 or current_dir > 360:
                        tools.feedback(
                            f'The {polytype} snail angle change "{_item}" must result in 0 to 360.',
                            True,
                            True,
                        )
            elif _item[0] == "j":
                if self.__class__.__name__ == "ShapeShape":
                    tools.feedback(
                        f'The {polytype} snail cannot use a jump ("{_item}").',
                        True,
                        True,
                    )
                a_item = _item.strip("j")
                if not is_float(a_item):
                    tools.feedback(
                        f'The {polytype} snail jump "{_item}" is not valid.', True, True
                    )
                else:
                    current_point = draw_or_jump(current_point, float(a_item), True)
            elif is_float(_item):
                current_point = draw_or_jump(current_point, float(_item), False)
            else:
                tools.feedback(
                    f'The {polytype} snail cannot contain "{_item}".', True, True
                )

    def get_vertexes(self):
        """Return Poly-shape line vertices in canvas units"""
        polytype = self.get_name()
        points = self.get_points()
        steps = self.get_steps()
        _snail = self.snail
        if points and _snail:
            feedback(
                f"Snail values will supercede points to draw the {polytype}",
                False,
                True,
            )
            return None
        if steps and _snail:
            feedback(
                f"Snail values will supercede steps to draw the {polytype}", False, True
            )
            return None
        if points and steps:
            feedback(
                f"Point values will supercede steps to draw the {polytype}", False, True
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
        if not self.snail:
            feedback(
                f"There are no points or steps or snail to draw the {polytype}.",
                False,
                True,
            )
        return None
