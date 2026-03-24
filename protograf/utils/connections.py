# -*- coding: utf-8 -*-
"""
Support functions for calculating connections for Lines/Polylines
"""
# lib
import math

# local
from protograf import globals
from protograf.base import BaseShape
from protograf.shapes_hexagon import HexShape
from protograf.shapes_polygon import PolygonShape
from protograf.shapes_utils import draw_line_curve
from protograf.utils.messaging import feedback
from protograf.utils.tools import _lower, validated_directions  # , _vprint
from protograf.utils import geoms, tools
from protograf.utils.structures import (
    DirectionGroup,
    Point,
)


def validate_connection_params(conn: tuple) -> list:
    """Check that a connection tuple contains all required values."""
    from protograf.shapes import StarShape  # avoid circular imports

    dirs = None
    if not isinstance(conn, tuple) or len(conn) < 3:
        feedback(
            "A non-circular connection must contain a shape, a point type,"
            f' and a point location - not "{conn}"',
            True,
        )
    if not isinstance(conn[0], BaseShape):
        feedback(
            "A non-circular connection's first entry must be a shape"
            f' - not "{conn[0]}"',
            True,
        )
    shape_type = conn[0].simple_name()
    if _lower(conn[1]) not in ["v", "vertex", "p", "perbis"]:
        feedback(
            f"A {shape_type} connection's second entry must be"
            f' one of v, vertex, p or point - not "{conn[1]}"',
            True,
        )
    if isinstance(conn[0], PolygonShape):
        dirs = validated_directions(
            value=_lower(conn[2]),
            direction_group=DirectionGroup.POLYGONAL,
            label=f"{shape_type} connection's third (direction)",
        )
    elif isinstance(conn[0], StarShape):
        dirs = validated_directions(
            value=_lower(conn[2]),
            direction_group=DirectionGroup.STAR,
            label=f"{shape_type} connection's third (direction)",
        )
    else:
        dirs = validated_directions(
            value=_lower(conn[2]),
            direction_group=DirectionGroup.COMPASS,
            label=f"{shape_type} connection's third (direction)",
        )
    return dirs, shape_type


def get_connection_point(the_shape: BaseShape, conn_type: str, direction: str) -> Point:
    """Get Point at which connection is to be made."""
    from protograf.shapes import StarShape  # avoid circular imports

    the_point = None
    shape_name = the_shape.simple_name()
    _name = f"{shape_name} ({the_shape.label})" if the_shape.label else shape_name
    if isinstance(the_shape, HexShape):
        shape_name = f"{the_shape.ORIENTATION.name.lower()} {shape_name}"
    if isinstance(the_shape, (PolygonShape, StarShape)):
        direction = tools.as_int(direction, "direction")
    # print(f"*** connections {shape_name=}")
    match _lower(conn_type):
        case "v" | "vertex":
            try:
                vertexes = the_shape._shape_vertexes_named
            except AttributeError:
                feedback(
                    f"{_name} has no vertices available for a connection.",
                    True,
                )
            vtx = vertexes.get(direction)
            if not vtx:
                # print(f"*** Line:connections {vertexes}")
                feedback(
                    f'{_name} cannot use a vertex in the "{direction}" direction.',
                    True,
                )
            else:
                the_point = vtx.point
        case "p" | "perbis":
            the_centre = the_shape.get_center()
            if the_centre is None:
                feedback(
                    f"{_name} centre cannot be calculated; please report this error!",
                    True,
                )
            try:
                perbises = the_shape.calculate_perbii(centre=the_centre)
            except AttributeError:
                feedback(
                    f"{_name} has no perbii available for a connection.",
                    True,
                )
            pbs = perbises.get(direction)
            if not pbs:
                feedback(
                    f'{_name} cannot use a perbis in the "{direction}" direction.',
                    True,
                )
            else:
                the_point = pbs.point
    if the_shape.rotation:
        center_point = the_shape._shape_centre
        the_point = geoms.rotate_point_around_point(
            (the_point.x, the_point.y),
            (center_point.x, center_point.y),
            the_shape.rotation,
        )
    return the_point


def get_rotation(centre_a: Point, centre_b: Point) -> tuple:
    """Get relative rotation between points."""
    # print(f"*** connections {centre_a=}, {centre_b=}")
    _, rotation = geoms.angles_from_points(centre_a, centre_b)
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
    return rotation_a, rotation_b


def get_connections(shapes: list, connections_style: str, curve: float = None) -> tuple:
    """Get connection vertices.

    Returns:
        tuple:
            float: curve height
            list: connection point tuples; start and end
    """
    from protograf.shapes import CircleShape, DotShape  # avoid circular imports

    def get_connection_curve(pt_x, centre_x, shape_x, rotation_x):
        """recalculate curve height as `connection_curve`"""
        straight_pt_x = geoms.point_on_circle(centre_x, shape_x._u.radius, rotation_x)
        theta = geoms.circle_angle_between_points(pt_x, straight_pt_x, centre_x)
        offset_height = shape_x._shape_radius * math.sin(math.radians(theta))
        connection_curve = (globals.units * curve - abs(offset_height)) / globals.units
        # print(f"{shape_x._shape_radius=} {theta=} {offset_height=} {connection_curve=}")
        return connection_curve

    connections = []
    connection_curve = curve

    for idx in range(0, len(shapes) - 1):
        cshape = shapes[idx]
        if connections_style and _lower(connections_style) in [
            "s",
            "spoke",
        ]:
            shape_a, shape_b = shapes[0], shapes[idx + 1]
        else:
            shape_a, shape_b = cshape, shapes[idx + 1]
        if isinstance(shape_a, (CircleShape, DotShape)) and isinstance(
            shape_b, (CircleShape, DotShape)
        ):
            centre_a = shape_a._shape_centre  # circle/dot
            centre_b = shape_b._shape_centre  # circle/dot
            rotation_a, rotation_b = get_rotation(centre_a, centre_b)
            # print(f"*** connections {rotation_a=}, {rotation_b=}")
            # print(f"*** connections {centre_a=} {shape_a._shape_radius=}")
            # print(f"*** connections {centre_b=} {shape_b._shape_radius=}")
            if curve:
                # curve intersects
                klargs, curve_centre, circle_centre, radius = draw_line_curve(
                    None, centre_a, centre_b, curve, draw=False
                )  # NOT drawn here
                # print(f"*** connection curve {circle_centre=} {radius=} {centre_a=} {shape_a._shape_radius=}")
                intersects_a = geoms.circle_intersections(
                    circle_centre, radius, centre_a, shape_a._shape_radius
                )
                # print(f"*** connection curve {circle_centre=} {radius=} {centre_b=} {shape_b._shape_radius=}")
                intersects_b = geoms.circle_intersections(
                    circle_centre, radius, centre_b, shape_b._shape_radius
                )
                pt_a, pt_b = intersects_a[1], intersects_b[0]
                # print(f"*** connection points {pt_a=}, {pt_b=}")
                connection_curve = get_connection_curve(
                    pt_a, centre_a, shape_a, rotation_a
                )
            else:
                pt_a = geoms.point_on_circle(centre_a, shape_a._u.radius, rotation_a)
                pt_b = geoms.point_on_circle(centre_b, shape_b._u.radius, rotation_b)
            connections.append((pt_a, pt_b))

        if isinstance(shape_a, (CircleShape, DotShape)) and not isinstance(
            shape_b, (CircleShape, DotShape)
        ):
            pt_b = get_connection_point(shape_b[0], shape_b[1], shape_b[2])
            centre_a = shape_a._shape_centre  # circle/dot
            rotation_a, rotation_b = get_rotation(centre_a, pt_b)
            # print(f"*** connections {rotation_a=}, {rotation_b=}")
            if curve:
                # print(f"*** connections ca:{tools._p2v(centre_a)} b:{tools._p2v(pt_b)}")
                # curve intersects
                klargs, curve_centre, circle_centre, radius = draw_line_curve(
                    None, centre_a, pt_b, curve, draw=False
                )  # NOT drawn here
                # print(f"*** b-a connection curve {tools._p2v(curve_centre)=}")
                # print(f"*** b-a connection curve c:{tools._p2v(circle_centre)} r:{radius/globals.units}")
                intersects_a = geoms.circle_intersections(
                    circle_centre, radius, centre_a, shape_a._shape_radius
                )
                ia = intersects_a
                # feedback(f"***Intersects: {tools._p2v(ia[0])} {tools._p2v(ia[1])}")
                if curve < 0:
                    pt_a = intersects_a[0]
                else:
                    pt_a = intersects_a[1]
                # print(f"*** connections a:{tools._p2v(pt_a)} b:{tools._p2v(pt_b)}")
                chord = geoms.length_of_line(pt_a, pt_b)
                connection_curve = geoms.circle_to_chord(radius, chord) / globals.units
                connection_curve = (
                    connection_curve * -1 if curve < 0 else connection_curve
                )
                # print(f"*** {connection_curve=}")
            else:
                pt_a = geoms.point_on_circle(centre_a, shape_a._u.radius, rotation_a)
            connections.append((pt_a, pt_b))

        if not isinstance(shape_a, (CircleShape, DotShape)) and isinstance(
            shape_b, (CircleShape, DotShape)
        ):
            pt_a = get_connection_point(shape_a[0], shape_a[1], shape_a[2])
            centre_b = shape_b._shape_centre  # circle/dot
            rotation_a, rotation_b = get_rotation(pt_a, centre_b)
            if curve:
                # print(f"*** connections a:{tools._p2v(pt_a)} cb:{tools._p2v(centre_b)}")
                # curve intersects
                klargs, curve_centre, circle_centre, radius = draw_line_curve(
                    None, pt_a, centre_b, curve, draw=False
                )  # NOT drawn here
                # print(f"*** b-a connection curve {tools._p2v(curve_centre)=}")
                # print(f"*** b-a connection curve c:{tools._p2v(circle_centre)} r:{radius/globals.units}")
                intersects_b = geoms.circle_intersections(
                    circle_centre, radius, centre_b, shape_b._shape_radius
                )
                ib = intersects_b
                feedback(f"***Intersects: {tools._p2v(ib[0])} {tools._p2v(ib[1])}")
                if curve < 0:
                    pt_b = intersects_b[1]
                else:
                    pt_b = intersects_b[0]
                # print(f"*** connections a:{tools._p2v(pt_a)} b:{tools._p2v(pt_b)}")
                chord = geoms.length_of_line(pt_a, pt_b)
                connection_curve = geoms.circle_to_chord(radius, chord) / globals.units
                connection_curve = (
                    connection_curve * -1 if curve < 0 else connection_curve
                )
                # print(f"*** {connection_curve=}")
            else:
                pt_b = geoms.point_on_circle(centre_b, shape_b._u.radius, rotation_b)
            connections.append((pt_a, pt_b))

        if not isinstance(shape_a, (CircleShape, DotShape)) and not isinstance(
            shape_b, (CircleShape, DotShape)
        ):
            pt_a = get_connection_point(shape_a[0], shape_a[1], shape_a[2])
            pt_b = get_connection_point(shape_b[0], shape_b[1], shape_b[2])
            connections.append((pt_a, pt_b))

    return connection_curve, connections
