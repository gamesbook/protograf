# -*- coding: utf-8 -*-
"""
Mathematical utility functions for protograf
"""
# lib
import cmath
import logging
import math
import sys
from typing import Any, List

# local
from protograf.utils.messaging import feedback
from protograf.utils.structures import Point
from protograf.utils.support import numbers, round_tiny_float

log = logging.getLogger(__name__)
DEBUG = False


def polygon_vertices(
    sides: int, radius: float, centre: Point, starting_angle: float = None
) -> list:
    """Calculate array of Points for a polygon's vertices.

    Args:
        sides:  number of sides of polygon
        radius: distance from centre
        centre: the Point of origin
        starting_angle: effectively the "rotation"

    Doc Test:

    >>> P = polygon_vertices(6, 1.0, Point(2,2))
    >>> assert P == [ \
    Point(x=2.5, y=1.1339745962155614), \
    Point(x=3.0, y=2.0), \
    Point(x=2.5, y=2.8660254037844384), \
    Point(x=1.5000000000000002, y=2.866025403784439), \
    Point(x=1.0, y=2.0), \
    Point(x=1.4999999999999996, y=1.1339745962155616)]
    """
    try:
        sides = max(int(sides), 3)
    except ValueError:
        feedback("Polygon's sides must be an integer of 3 or more.")
        return []
    points = []
    # starting_angle is effectively the "rotation"
    interior_angle = ((sides - 2) * 180.0) / sides
    if sides % 2 != 0:
        _start = -90.0  # odd sides
    else:
        _start = -interior_angle / 2.0  # even sides
    starting_angle = _start if starting_angle is None else starting_angle
    try:
        _starting_angle = float(starting_angle)
    except ValueError:
        feedback("Polygon's start angle must be an decimal or integer number.")
        return []
    # print(f'\n+++ poly_vert {sides=} {interior_angle=} {starting_angle=} {_starting_angle=} +++')
    # angles go around a full circle, anti-clockwise, starting from the "top"
    _step = 360.0 / sides
    data_generator = numbers(_starting_angle, 360.0 + _starting_angle, _step)
    try:
        _rotate = next(data_generator)
        while True:
            points.append(degrees_to_xy(_rotate, radius, centre))
            _rotate = next(data_generator)
    except (StopIteration, RuntimeError):
        pass  # ignore StopIteration
    finally:
        del data_generator
    return points


def degrees_to_xy(degrees: float, radius: float, origin: Point) -> Point:
    """Calculates a Point that is at an angle from the origin; 0 is to the right.

    Args:
        degrees: normal angle (NOT radians) in anti-clockwise direction
        radius: length of line originating at origin
        origin: the (x, y) coordinates of the point of origin

    Doc Test:

    >>> R = degrees_to_xy(300, 5, Point(0,0))
    >>> assert round(R.x, 2) == 2.5
    >>> assert round(R.y, 2) == -4.33
    >>> R = degrees_to_xy(210, 5, Point(0,0))
    >>> assert round(R.x, 2) == -4.33
    >>> assert round(R.y, 2) == -2.5
    >>> R = degrees_to_xy(120, 5, Point(0,0))
    >>> assert round(R.x, 2) == -2.5
    >>> assert round(R.y, 2) == 4.33
    >>> R = degrees_to_xy(30, 5, Point(0,0))
    >>> assert round(R.x, 2) == 4.33
    >>> assert round(R.y, 2) == 2.5

    >>> R = degrees_to_xy(120, 19, Point(85,113))
    >>> assert round(R.x, 2) == 75.5
    >>> assert round(R.y, 2) == 129.45
    """
    # print(f'+++ degrees_to_xy :: {degrees=}, {radius=}, {origin=}')
    radians = float(degrees) * math.pi / 180.0
    x_o = math.cos(radians) * radius + origin.x
    y_o = math.sin(radians) * radius + origin.y
    # print('+++ +++', Point(x_o, y_o))
    return Point(x_o, y_o)


def compass_to_angle(direction: str) -> tuple:
    """Convert a 16-point compass bearing abbreviation to angles

    Args:
        direction (str): name of compass bearing

    Returns:
        compass (float): degrees clockwise from North
        rotation (float): degrees anti-clockwise from East

    Doc Test:

    >>> compass_to_angle('ene')
    (67.5, 22.5)
    >>> compass_to_angle('W')
    (270.0, 180.0)
    """
    data = {
        "N": 0.0,
        "NNE": 22.5,
        "NE": 45.0,
        "ENE": 67.5,
        "E": 90.0,
        "ESE": 112.5,
        "SE": 135.0,
        "SSE": 157.5,
        "S": 180.0,
        "SSW": 202.5,
        "SW": 225.0,
        "WSW": 247.5,
        "W": 270.0,
        "WNW": 292.5,
        "NW": 315.0,
        "NNW": 337.5,
    }
    if not isinstance(direction, str):
        feedback(f'The compass bearing "{direction}" must be a string!', True)
    compass = data.get(direction.upper(), None)
    if compass is None:
        feedback(f'The compass bearing "{direction}" is not valid!', True)
    rotation = (450 - compass) % 360.0
    # print(f'compass-angle fn: {compass=}, {rotation=}')
    return round_tiny_float(compass), round_tiny_float(rotation)


def point_in_polygon(point: Point, vertices: List[Point], valid_border=False) -> bool:
    """Wrapper for is_inside_polygon() function.

    Args:
        point: the (x, y) coordinates of the Point to check
        vertices: a list of (x, y) Point coordinates of the enclosing shape

    Doc Test:

    >>> point_in_polygon(Point(1,1), [Point(1, 1), Point(2, 2), Point(3, 3)])
    False
    >>> point_in_polygon(Point(1,1), [Point(0, 0), Point(1, 2), Point(2, 0)])
    True
    """
    _point = (point.x, point.y)
    _vertices = [(pnt.x, pnt.y) for pnt in vertices]
    return is_inside_polygon(_point, _vertices, valid_border)


def is_point_on_line(
    point_a: Point, point_b: Point, point_c: Point, tolerance: float = 1e-6
):
    """Check if point C is on the finite line defined by points A and B.

    Doc Test:
    >>> point_a = Point(1, 2)
    >>> point_b = Point(4, 8)
    >>> point_c = Point(2, 4)
    >>> point_d = Point(2, 5)
    >>> is_point_on_line(point_a, point_b, point_c)
    True
    >>> is_point_on_line(point_a, point_b, point_d)
    False
    >>> point_a = Point(0, 0)
    >>> point_b = Point(10, 10)
    >>> point_P1 = Point(5, 5)     # On the segment
    >>> point_P2 = Point(15, 15)   # Collinear, but outside the segment's end
    >>> is_point_on_line(point_a, point_b, point_P1)
    True
    >>> is_point_on_line(point_a, point_b, point_P2)
    False
    """
    # Vector AB: (b.x - a.x, b.y - a.y)
    ab_x = point_b.x - point_a.x
    ab_y = point_b.y - point_a.y
    # Vector AC: (c.x - a.x, c.y - a.y)
    ac_x = point_c.x - point_a.x
    ac_y = point_c.y - point_a.y
    # Cross product (magnitude for 2D vectors): AB_x * AC_y - AB_y * AC_x
    cross_product = ab_x * ac_y - ab_y * ac_x
    # 1. Check if the cross product is close to zero (using math.isclose for floats)
    if not math.isclose(cross_product, 0.0, abs_tol=tolerance):
        return False  # point is NOT collinear
    # 2. Bound Check (point is between endpoints)
    # Check if C's coordinates are within the range of A and B's coordinates
    # use max and min to handle segments defined in any order
    if (
        min(point_a.x, point_b.x) - tolerance
        <= point_c.x
        <= max(point_a.x, point_b.x) + tolerance
        and min(point_a.y, point_b.y) - tolerance
        <= point_c.y
        <= max(point_a.y, point_b.y) + tolerance
    ):
        # point is collinear AND within the bounds
        return True
    # point is collinear BUT outside the segment endpoints
    return False


def is_inside_polygon(point: tuple, vertices: list, valid_border=False) -> bool:
    """Check if point inside a polygon defined by set of vertices.

    Ref:
        https://www.linkedin.com/pulse/~
        short-formula-check-given-point-lies-inside-outside-polygon-ziemecki/

    Doc Test:

    >>> is_inside_polygon(Point(1,1), [ Point(1, 1), Point(2, 2), Point(3, 3)])
    False
    >>> is_inside_polygon(Point(1,1), [ Point(0, 0), Point(1, 2), Point(2, 0)])
    True
    """

    def _is_point_in_segment(point, point_0, point_1):
        p_0 = point_0[0] - point[0], point_0[1] - point[1]
        p_1 = point_1[0] - point[0], point_1[1] - point[1]
        det = p_0[0] * p_1[1] - p_1[0] * p_0[1]
        prod = p_0[0] * p_1[0] + p_0[1] * p_1[1]
        return (
            (det == 0 and prod < 0)
            or (p_0[0] == 0 and p_0[1] == 0)
            or (p_1[0] == 0 and p_1[1] == 0)
        )

    sum_ = complex(0, 0)
    for vertex in range(1, len(vertices) + 1):
        v0, v1 = vertices[vertex - 1], vertices[vertex % len(vertices)]
        if _is_point_in_segment(point, v0, v1):
            return valid_border
        sum_ += cmath.log(
            (complex(*v1) - complex(*point)) / (complex(*v0) - complex(*point))
        )
    return abs(sum_) > 1


def length_of_line(start: Point, end: Point) -> float:
    """Calculate length of line between two Points.

    Doc Test:

    >>> length_of_line(Point(0, 0), Point(0, 1))
    1.0
    >>> length_of_line(Point(0, 0), Point(3, 4))
    5.0
    """
    # √[(x₂ - x₁)² + (y₂ - y₁)²]
    return math.sqrt((end.x - start.x) ** 2 + (end.y - start.y) ** 2)


def point_on_line(point_start: Point, point_end: Point, distance: float) -> Point:
    """Calculate new Point at a distance along a line defined by its end Points

    Args:
        point_start: the (x, y) coordinates of the start point
        point_end: the (x, y) coordinates of the end point
        distance: the distance of the line to use (from the point_start)

    Doc Test:

    >>> P = Point(0,2)
    >>> Q = Point(4,4)
    >>> D = 3
    >>> R = point_on_line(P, Q, D)
    >>> assert round(R.x, 4) == 2.6833
    >>> assert round(R.y, 4) == 3.3416
    >>> P = Point(4,4)
    >>> Q = Point(0,2)
    >>> D = 3
    >>> R = point_on_line(P, Q, D)
    >>> assert round(R.x, 4) == 1.3167
    >>> assert round(R.y, 4) == 2.6584
    >>> R = point_on_line(Point(0,5), Point(0,2), 1)  # downwards
    >>> assert round(R.x, 4) == 0
    >>> assert round(R.y, 4) == 4
    >>> R = point_on_line(Point(0,2), Point(0,5), 1)  # upwards
    >>> assert round(R.x, 4) == 0
    >>> assert round(R.y, 4) == 3
    >>> R = point_on_line(Point(2,0), Point(5,0), 1)  # right
    >>> assert round(R.x, 4) == 3
    >>> assert round(R.y, 4) == 0
    >>> R = point_on_line(Point(5,0), Point(2,0), 1)  # left
    >>> assert round(R.x, 4) == 4
    >>> assert round(R.y, 4) == 0
    """
    if point_end.x == point_start.x and point_end.y == point_start.y:
        return point_start
    distance = abs(distance)
    if point_end.x != point_start.x and point_end.y != point_start.y:
        line = math.sqrt(
            (point_end.x - point_start.x) ** 2 + (point_end.y - point_start.y) ** 2
        )
        ratio = distance / line
        x = (1.0 - ratio) * point_start.x + ratio * point_end.x
        y = (1.0 - ratio) * point_start.y + ratio * point_end.y
    elif point_end.y == point_start.y:
        distance = distance * -1.0 if point_start.x > point_end.x else distance
        x = point_start.x + distance
        y = point_end.y
    elif point_end.x == point_start.x:
        distance = distance * -1.0 if point_start.y > point_end.y else distance
        y = point_start.y + distance
        x = point_end.x
    else:
        raise NotImplementedError(
            f"Cannot calculate line on point for: {point_start} and {point_end}"
        )
    return Point(x, y)


def point_on_circle(point_centre: Point, radius: float, angle: float) -> Point:
    """Calculate Point on circumference of a circle at a specific angle in degrees

    Args:
        point_center: the (x, y) coordinates of the circle centre
        angle: the rotation angle in degrees (anti-clockwise from x-axis baseline)
        radius: length of circle radius

    Doc Test:

    >>> P = Point(0,0)
    >>> R = 3.0
    >>> T = 45.0
    >>> R = point_on_circle(P, R, T)
    >>> round(R.x, 4) == 2.1213
    True
    >>> round(R.y, 4) == -2.1213
    True
    """
    if radius == 0.0:
        return point_centre
    try:
        theta = float(angle) * math.pi / 180.0
        x = math.cos(theta) * radius + point_centre.x
        y = point_centre.y - math.sin(theta) * radius  # + point_centre.y
    except Exception as exc:
        raise ValueError(
            f"Cannot calculate point on circle for: {point_centre}, {radius} and {angle}"
        ) from exc
    return Point(x, y)


def point_on_ellipse(
    point_centre: Point, angle: float, height: float, width: float
) -> Point:
    """Calculate Point on circumference of an ellipse at a specific angle in degrees

        Args:
            point_center: the (x, y) coordinates of the ellipse centre
            angle: the rotation angle in degrees (anti-clockwise from x-axis baseline)
            height: length of ellipse vertical axis
            width: length of ellipse horizontal axis
    R,
        Doc Test:

        >>> P = Point(3, 4)
        >>> T = 30.0
        >>> H = 4.0
        >>> W = 10.0
        >>> R = point_on_ellipse(P, T, H, W)
        >>> round(R.x, 4)
        5.8475
        >>> round(R.y, 4)
        5.644
    """
    try:
        h2 = float(height / 2.0)
        w2 = float(width / 2.0)
    except ValueError:
        feedback("Ellipse's height and width must be decimal or integer numbers.")
        return point_centre
    try:
        theta = float(angle) * math.pi / 180.0
        divisor = math.sqrt((h2 * math.cos(theta)) ** 2 + (w2 * math.sin(theta)) ** 2)
        x = point_centre.x + (h2 * w2 * math.cos(theta)) / divisor
        y = point_centre.y + (h2 * w2 * math.sin(theta)) / divisor
    except Exception as exc:
        raise ValueError(
            f"Cannot calculate point on ellipse for: {point_centre} and angle: {angle}"
        ) from exc
    return Point(x, y)


def fraction_along_line(point_start: Point, point_end: Point, fraction: float) -> Point:
    """Calculate new Point at a fractional distance along line defined by end Points

    Args:
        point_start: the (x, y) coordinates of the start point
        point_end: the (x, y) coordinates of the end point
        fraction: the fraction of the line to use (from the point_start)

    """
    if fraction > 1.0 or fraction < 0.0:
        raise ValueError("The fraction cannot be greater than 1 or less than 0.")
    line_length = length_of_line(start=point_start, end=point_end)
    fraction_length = fraction * line_length
    fraction_point = point_on_line(
        point_start=point_start, point_end=point_end, distance=fraction_length
    )
    return fraction_point


def point_in_direction(
    point_start: Point, point_end: Point, distance_factor: float = 1.0
) -> Point:
    """
    Calculate new Point in the same direction as a line segment defined by end Points

    Args:
        point_start (Point):
            coordinates of the first point (x1, y1)
        point_end (Point):
            coordinates of the second point (x2, y2)
        distance_factor (float):
             Distance of the third point relative to the line segment.
             If 1.0, then third point is same distance from point_end as
             point_end is from point_start

    Returns:
        Point: coordinates of the third point (x3, y3).

    Doc Test:
    >>> point1 = Point(1, 2)
    >>> point2 = Point(4, 6)
    >>> point_in_direction(point1, point2)
    Point(x=7.0, y=10.0)
    >>> point_in_direction(point1, point2, distance_factor=0.5)
    Point(x=5.5, y=8.0)
    """
    # direction vector from point_start to point_end
    dx = point_end.x - point_start.x
    dy = point_end.y - point_start.y
    # extend the vector from point_end by the distance_factor
    x3 = point_end.x + dx * distance_factor
    y3 = point_end.y + dy * distance_factor
    return Point(x3, y3)  # coordinates of the third point


def point_from_angle(start: Point, length: float, angle: float) -> Point:
    """Given a point, line length, and an angle, calculate the second point.

    Args:
        start: coordinates of first point
        length: length of line
        angle: angle of line in degrees (anti-clockwise from East)

    Returns:
        coordinates of second point

    Notes:
        Operates in the Euclidian plane

    Doc Test:
    >>> # angle anti-clockwise around circle from 0 degrees at East
    >>> point_from_angle(Point(0, 0), 1, 0)
    Point(x=1.0, y=0.0)
    >>> point_from_angle(Point(0, 0), 1, 90)
    Point(x=0.0, y=1.0)
    >>> R = point_from_angle(Point(0, 0), 1, 45)
    >>> # Point(x=0.7071067811865476, y=0.7071067811865475)
    >>> round(R.x, 5) == 0.70711
    True
    >>> round(R.y, 5) == 0.70711
    True
    >>> R = point_from_angle(Point(0, 0), 1, 225)
    >>> # Point(x=-0.7071067811865476, y=-0.7071067811865475)
    >>> round(R.x, 5) == -0.70711
    True
    >>> round(R.y, 5) == -0.70711
    True
    >>> R = point_from_angle(Point(0, 0), 1, -45)
    >>> # Point(x=0.7071067811865476, y=-0.7071067811865475)
    >>> round(R.x, 5) == 0.70711
    True
    >>> round(R.y, 5) == -0.70711
    True
    """
    theta = math.radians(angle)
    x1, y1 = start.x + length * math.cos(theta), start.y + length * math.sin(theta)
    return Point(round_tiny_float(x1), round_tiny_float(y1))


def angles_from_points(first: Point, second: Point) -> tuple:
    """Given two points, calculate the compass and rotation angles between them

    Args:
        first: coordinates of first point
        second: coordinates of second point

    Returns:
        compass (float): degrees clockwise from North
        rotation (float): degrees anti-clockwise from East

    Doc Test:

    >>> # clockwise around circle from 0 degrees at North
    >>> angles_from_points(Point(0, 0), Point(0, 4))
    (0.0, 90.0)
    >>> angles_from_points(Point(0, 0), Point(4, 4))
    (45.0, 45.0)
    >>> angles_from_points(Point(0, 0), Point(4, 0))
    (90.0, 0.0)
    >>> angles_from_points(Point(0, 0), Point(4, -4))
    (135.0, 315.0)
    >>> angles_from_points(Point(0, 0), Point(0, -4))
    (180.0, 270.0)
    >>> angles_from_points(Point(0, 0), Point(-4, -4))
    (225.0, 225.0)
    >>> angles_from_points(Point(0, 0), Point(-4, 0))
    (270.0, 180.0)
    >>> angles_from_points(Point(0, 0), Point(-4, 4))
    (315.0, 135.0)
    >>> angles_from_points(Point(2.5, 3.5), Point(3.25, 2.2))
    (150.01836063115067, 299.9816393688493)
    """
    compass = 0
    a, b = second.x - first.x, second.y - first.y
    if second.x != first.x:
        gradient = (second.y - first.y) / (second.x - first.x)
        theta = math.atan(gradient)
        angle = theta * 180.0 / math.pi
        # print(f'{x1-x1=} {y1-y1=} {a=} {b=} {angle=}')
        if a > 0 and b >= 0:
            compass = 90.0 - angle
        if a > 0 and b < 0:
            compass = 90 - angle
        if a < 0 and b < 0:
            compass = 270.0 - angle
        if a < 0 and b >= 0:
            compass = 270.0 - angle
    else:
        compass = 0.0
        if second.y - first.y < 0:
            compass = 180.0
    rotation = (450 - compass) % 360.0
    # print(f'angle fn: {compass=}, {rotation=}')
    return round_tiny_float(compass), round_tiny_float(rotation)


def centre_radius_from_points(pt_a: Point, pt_b: Point, pt_c: Point) -> tuple:
    """Return (center, radius) of the circle passing through three Points.

    Args:
        pt_a (Point)
        pt_b (Point)
        pt_c (Point)

    Returns:
        tuple:
            centre (Point), radius (float)

    Notes:
        If points are colinear, feedback "colinear error" and return empty tuple.

    Source:
        https://math.stackexchange.com/questions/213658/

    Doc Test:

    >>> centre_radius_from_points(Point(1, 1), Point(2, 4), Point(5, 3))
    (Point(x=3.0, y=2.0), 2.23606797749979)
    >>> R = centre_radius_from_points(Point(10, 10), Point(3, 7), Point(6, 10))
    >>> round(R[0].x, 5)
    8.0
    >>> round(R[0].y, 5)
    5.0
    >>> round(R[1], 5)
    5.38516
    """
    z_1 = complex(pt_a.x, pt_a.y)
    z_2 = complex(pt_b.x, pt_b.y)
    z_3 = complex(pt_c.x, pt_c.y)

    if z_1 == z_2:
        feedback("Points are colinear and no circle can be determined", True)
        return (None, None)

    w_3 = (z_3 - z_1) / (z_2 - z_1)
    if abs(w_3.imag) < sys.float_info.epsilon:
        feedback("Points are colinear and no circle can be determined", True)
        return (None, None)

    d_1 = (w_3 - w_3 * w_3.conjugate()) / (w_3 - w_3.conjugate())
    c_1 = z_1 + (z_2 - z_1) * d_1
    radius = abs(z_1 - c_1)
    centre = Point(c_1.real, c_1.imag)
    return (centre, radius)


def separation_between_hexsides(side_a: int, side_b: int) -> int:
    """Levels of separation between two sides of a hexagon.

    Args:
        side_a: the ID number of the first side
        side_b: the ID number of the second side

    Notes:
        Sides are numbered from 1 to 6 (by convention starting at furthest left).

    Doc Test:

    >>> separation_between_hexsides(1, 1)
    0
    >>> separation_between_hexsides(1, 2)
    1
    >>> separation_between_hexsides(1, 3)
    2
    >>> separation_between_hexsides(1, 4)
    3
    >>> separation_between_hexsides(1, 5)
    2
    >>> separation_between_hexsides(1, 6)
    1
    >>> separation_between_hexsides(6, 1)
    1
    >>> separation_between_hexsides('a', 1)
    """
    try:
        _side_a = 6 if (side_a % 6 == 0) else side_a % 6
        _side_b = 6 if (side_b % 6 == 0) else side_b % 6
    except TypeError:
        # print(f'Cannot use {side_a} and/or {side_b} as side numbers.', True)
        return None
    if _side_a - _side_b > 3:
        result = (_side_b, _side_a)
    else:
        result = (_side_b, _side_a) if _side_b > _side_a else (_side_a, _side_b)
    dist = (result[0] - result[1]) % 6
    if _side_a == 2 and _side_b == 6:
        dist = 2
    if _side_a == 1 and _side_b == 5:
        dist = 2
    if _side_a == 1 and _side_b == 6:
        dist = 1
    return dist


def lines_intersect(a_start: Point, a_end: Point, c_start: Point, c_end: Point) -> bool:
    """Return True if line segments AB and CD intersect

    Args:
        a_start: (x, y) coordinates of start point of line AB
        a_end: (x, y) coordinates of end point of line AB
        c_start: (x, y) coordinates of start point of line CD
        c_end: (x, y) coordinates of end point of line CD

    Ref:
        https://stackoverflow.com/questions/3838329

    Doc Test:

    >>> lines_intersect(Point(0, 0), Point(1, 1), Point(2, 2), Point(3, 3))
    False
    >>> lines_intersect(Point(0, 0), Point(2, 2), Point(2, 0), Point(0, 2))
    True
    """

    def ccw(a_start: Point, a_end: Point, c_start: Point):
        return (c_start.y - a_start.y) * (a_end.x - a_start.x) > (
            a_end.y - a_start.y
        ) * (c_start.x - a_start.x)

    return ccw(a_start, c_start, c_end) != ccw(a_end, c_start, c_end) and ccw(
        a_start, a_end, c_start
    ) != ccw(a_start, a_end, c_end)


def line_intersection_point(
    p1: Point, p2: Point, p3: Point, p4: Point, intersects_primary: bool = False
) -> Point:
    """Calculate intersection of two extended lines (p1-p2) and (p3-p4).

    Args:
        p1 (Point): start of primary line
        p2 (Point): end of primary line
        p3 (Point): start of secondary line
        p4 (Point): end of secondary line
        intersects_primary (bool): only return point if it is on primary line

    Doc Test:

    >>> line_intersection_point(Point(0, 0), Point(10, 10), Point(0, 10), Point(10, 0))
    Point(x=5.0, y=5.0)
    >>> line_intersection_point(Point(0, 0), Point(10, 10), Point(0, 10), Point(2.5, 7.5))
    Point(x=5.0, y=5.0)
    >>> line_intersection_point(Point(0, 10), Point(0, 0), Point(10, 10), Point(10, 0))
    """
    x1, y1 = p1.x, p1.y
    x2, y2 = p2.x, p2.y
    x3, y3 = p3.x, p3.y
    x4, y4 = p4.x, p4.y
    denom = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
    if denom == 0:
        return None  # parallel or coincident
    ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denom
    # intersection point
    x = x1 + ua * (x2 - x1)
    y = y1 + ua * (y2 - y1)
    if intersects_primary:
        if not is_point_on_line(p1, p2, Point(x, y)):
            return None
    return Point(x, y)


def bezier_arc_segment(
    cx: float, cy: float, rx: float, ry: float, theta0: float, theta1: float
) -> tuple:
    """Compute the control points for a Bezier arc with angles theta1-theta0 <= 90.

    Points are computed for an arc with angle theta increasing in the
    anti-clockwise direction. Zero degrees is at the "East" position.

    Returns:
        tuple: starting point and 3 control points of a cubic Bezier curve

    Source:
        https://github.com/makinacorpus/reportlab-ecomobile/blob/master/src/reportlab/graphics/renderPM.py

    Doc Test:

    >>> bezier_arc_segment(cx=1, cy=2.5, rx=0.5, ry=0.5, theta0=90, theta1=180)
    ((1.0, 3.0), (0.7238576250846034, 3.0, 0.5, 2.7761423749153966, 0.5, 2.5))
    >>> bezier_arc_segment(cx=1, cy=2.5, rx=0.5, ry=0.5, theta0=90, theta1=270)
    FEEDBACK:: Angles must have a difference less than, or equal to, 90
    """

    # Requires theta1 - theta0 <= 90 for a good approximation
    if abs(theta1 - theta0) > 90:
        feedback("Angles must have a difference less than, or equal to, 90")
        return None
    cos0 = math.cos(math.pi * theta0 / 180.0)
    sin0 = math.sin(math.pi * theta0 / 180.0)
    x0 = cx + rx * cos0
    y0 = cy + ry * sin0

    cos1 = math.cos(math.pi * theta1 / 180.0)
    sin1 = math.sin(math.pi * theta1 / 180.0)

    x3 = cx + rx * cos1
    y3 = cy + ry * sin1

    dx1 = -rx * sin0
    dy1 = ry * cos0

    half_angle = math.pi * (theta1 - theta0) / (2.0 * 180.0)
    k = abs(4.0 / 3.0 * (1.0 - math.cos(half_angle)) / (math.sin(half_angle)))
    x1 = x0 + dx1 * k
    y1 = y0 + dy1 * k

    dx2 = -rx * sin1
    dy2 = ry * cos1

    x2 = x3 - dx2 * k
    y2 = y3 - dy2 * k
    return (x0, y0), (x1, y1, x2, y2, x3, y3)


def circle_angles(radius: float, chord: float) -> float:
    """Calculate interior angles of isosceles triangle formed inside a circle.

    Args:
        radius (float): radius of circle
        chord (float): length of line between two points on circle

    Source:
        https://www.quora.com/How-do-you-find-the-angles-of-an-isosceles-triangle-given-three-sides

    Doc Test:

    >>> R = circle_angles(5., 6.)
    >>> assert round(R[0], 2) == 73.74
    >>> assert round(R[1], 2) == 53.13
    """
    top = math.acos((2.0 * radius**2 - chord**2) / (2.0 * radius**2))
    base = (180.0 - math.degrees(top)) / 2.0
    return math.degrees(top), base, base


def circle_angle_between_points(start: Point, end: Point, centre: Point) -> float:
    """Calculate angles between two points lying on a circle of known centre.

    Args:
        start: coordinates of first point
        end: coordinates of second point
        centre: coordinates of circle's centre

    Returns:
        angle (degrees)

    Source:
        Google AI!

    Doc Test:

    >>> P1 = Point(15, 10)
    >>> P2 = Point(10, 15)
    >>> C0 = Point(10, 10)
    >>> circle_angle_between_points(P1, P2, C0)
    90.0
    """
    # subtract center from each point
    angle1 = math.atan2(start.y - centre.y, start.x - centre.x)
    angle2 = math.atan2(end.y - centre.y, end.x - centre.x)
    # calculate difference and normalize
    diff = math.degrees(angle2 - angle1)
    angle_between = diff % 360
    return angle_between


def circle_tangent_angle(centre: Point, point: Point) -> float:
    """
    Calculates the angle of the tangent line at a given point on a circle.

    Args:
        centre: coordinates of circle's centre
        point: coordinates of point

    Returns:
        angle (float): tangent line in degrees (0 to 360).

    Source:
        Google AI!

    Doc Test:

    >>> P1 = Point(15, 10)
    >>> C0 = Point(10, 10)
    >>> circle_tangent_angle(C0, P1)
    90.0
    >>> C0 = Point(5, 5)
    >>> P1 = Point(7.5, 7.5)
    >>> circle_tangent_angle(C0, P1)
    135.0
    """
    # change in coordinates (vector from centre to point)
    dx = point.x - centre.x
    dy = point.y - centre.y
    # angle of the radius
    radius_angle_rad = math.atan2(dy, dx)
    # tangent is perpendicular, so add 90 degrees (pi/2 radians)
    tangent_angle_rad = radius_angle_rad + math.pi / 2
    tangent_angle_deg = math.degrees(tangent_angle_rad)
    # convert angle to range [0, 360]
    if tangent_angle_deg < 0:
        tangent_angle_deg += 360
    elif tangent_angle_deg >= 360:
        tangent_angle_deg -= 360
    return tangent_angle_deg


def circle_intersections(
    centre1: Point, radius1: float, centre2: Point, radius2: float
) -> list:
    """Calculate the intersection points of two circles.

    Args:
        centre1: coordinates of first circle's centre
        radius1: radius of first circle
        centre2: coordinates of second circle's centre
        radius2: radius of second circle

    Returns:
        list: any intersection points (0, 1 or 2)

    Source:
        Google AI!

    Doc Test:

    >>> circle_intersections(Point(0, 0), 5, Point(6, 0), 4)
    [Point(x=3.75, y=-3.307189138830738), Point(x=3.75, y=3.307189138830738)]
    >>> circle_intersections(Point(0, 0),1, Point(5, 0), 1)  # separate
    []
    >>> circle_intersections(Point(0, 0),10, Point(0, 0), 5)  # 2 inside 1
    []
    >>> circle_intersections(Point(0, 0),5, Point(9, 0), 4) # tangent
    [Point(x=5.0, y=0.0)]

    """
    # distance between centers
    c2c = math.sqrt((centre2.x - centre1.x) ** 2 + (centre2.y - centre1.y) ** 2)
    # non-intersecting cases?
    if c2c > radius1 + radius2:
        return []  # separate
    if c2c < abs(radius1 - radius2):
        return []  # circle is contained within the other
    if c2c == 0 and radius1 == radius2:
        return None  # coincident (infinite intersection points!)
    # intermediate values
    a = (radius1**2 - radius2**2 + c2c**2) / (2 * c2c)
    h = math.sqrt(radius1**2 - a**2)
    # point where common chord intersects line connecting centers
    x2 = centre1.x + a * (centre2.x - centre1.x) / c2c
    y2 = centre1.y + a * (centre2.y - centre1.y) / c2c
    # calculate the intersection points
    x3 = x2 + h * (centre2.y - centre1.y) / c2c
    y3 = y2 - h * (centre2.x - centre1.x) / c2c
    x4 = x2 - h * (centre2.y - centre1.y) / c2c
    y4 = y2 + h * (centre2.x - centre1.x) / c2c
    # return point(s)
    if h == 0:
        return [Point(x3, y3)]  # tangent circles (one point)
    return [Point(x3, y3), Point(x4, y4)]


def circle_chord_endpoints(
    centre: Point, radius: float, start: Point, chord: float
) -> tuple:
    """Calculate the two possible endpoints of a chord.

    Args:
        centre (Point): coordinates of circle's centre
        radius (float): radius of circle
        chord (float): length of line between two points on circle
        start (Point): coordinates of point on circle

    Returns:
        tuple (Point, Point):
            coordinates of two possible endpoints

    Source:
        Google AI!

    Doc Test:

    >>> center = Point(0, 0)
    >>> radius = 5
    >>> start = Point(5, 0) # A point on the circle
    >>> chord = 8
    >>> circle_chord_endpoints(center, radius, start, chord)
    (Point(x=-1.4000000000000008, y=4.8), Point(x=-1.4000000000000008, y=-4.8))
    >>> chord = 80
    >>> # circle_chord_endpoints(center, radius, start, chord)
    >>> # "Chord length cannot be greater than the diameter."
    >>> chord = 8
    >>> start = Point(50, 50)
    >>> # circle_chord_endpoints(center, radius, start, chord)
    >>> # "Starting point is not on the circle."
    """
    # starting point is on the circle?
    distance_to_center = math.sqrt(
        (start.x - centre.x) ** 2 + (start.y - centre.y) ** 2
    )
    if not math.isclose(distance_to_center, radius):
        feedback("Starting point is not on the circle.", stop=True, warn=True)
    # chord length is valid?
    if chord > 2 * radius:
        feedback(
            "Chord length cannot be greater than the diameter.", stop=True, warn=True
        )
    # angle subtended by the chord at the center using Law of Cosines
    # L^2 = R^2 + R^2 - 2*R*R*cos(theta)
    # cos(theta) = (2*R^2 - L^2) / (2*R^2)
    # theta = acos(...)
    cos_theta = (2 * radius**2 - chord**2) / (2 * radius**2)
    # clamp the value to [-1, 1] to avoid math domain errors due to floating point inaccuracies
    cos_theta = max(-1, min(1, cos_theta))
    theta = math.acos(cos_theta)  # radians
    # initial angle of starting point relative to center
    alpha = math.atan2(start.y - centre.y, start.x - centre.x)
    # two possible angles for second endpoint: alpha + theta & alpha - theta
    angle1 = alpha + theta
    angle2 = alpha - theta
    # convert polar to Cartesian coordinates
    end_x1 = centre.x + radius * math.cos(angle1)
    end_y1 = centre.y + radius * math.sin(angle1)
    end_x2 = centre.x + radius * math.cos(angle2)
    end_y2 = centre.y + radius * math.sin(angle2)
    return Point(end_x1, end_y1), Point(end_x2, end_y2)


def equilateral_height(side: Any) -> float:
    """Calculate height of equilateral triangle from a side.

    Doc Test:

    >>> equilateral_height(5)
    4.330127018922194
    """
    try:
        _side = float(side)
        return math.sqrt(_side**2 - (0.5 * _side) ** 2)
    except ValueError:
        feedback("Equilateral height must be an decimal or integer number.", True)
        return None


def rotate_point_around_point(
    point_to_rotate: tuple, center_point: tuple, angle: float
) -> Point:
    """
    Rotates a point around another point by a specified angle.

    Args:
        point_to_rotate: the (x, y) coordinates of the point to rotate
        center_point: the (x, y) coordinates of the point to rotate around
        angle (float): the rotation angle in degrees (anti-clockwise)

    Returns:
        Point: The (x, y) coordinates of the rotated point (rounded to 8 decimals)

    Doc Test:

    >>> rotate_point_around_point((2,2), (1,1), 90)
    Point(x=2.0, y=0.0)
    >>> rotate_point_around_point((2,2), (1,3), 45)
    Point(x=1.0, y=1.58578644)
    >>> rotate_point_around_point((10,0), (0,0), 90)
    Point(x=0.0, y=-10.0)
    """
    x, y = point_to_rotate
    cx, cy = center_point
    angle_radians = math.radians(-angle)
    # Translate the point so that the center of rotation is the origin
    translated_x = x - cx
    translated_y = y - cy
    # Perform the rotation
    rotated_x = translated_x * math.cos(angle_radians) - translated_y * math.sin(
        angle_radians
    )
    rotated_y = translated_x * math.sin(angle_radians) + translated_y * math.cos(
        angle_radians
    )
    # Translate the rotated point back to the original center
    final_x = rotated_x + cx
    final_y = rotated_y + cy
    return Point(round(final_x, 8), round(final_y, 8))


def rectangles_overlap(rect1: tuple, rect2: tuple) -> bool:
    """Check if rectangles overlap, given top-left and bottom-right coordinates

    Args:
        rect1 (tuple): (x1, y1, x2, y2) for the first rectangle.
        rect2 (tuple): (x1, y1, x2, y2) for the second rectangle.

    Returns:
        bool: True if rectangles overlap, else False

    Doc Test:

    >>> rect_a = (0, 0, 10, 10)  # Top-left (0,0), Bottom-right (10,10)
    >>> rect_b = (5, 5, 15, 15)  # Top-left (5,5), Bottom-right (15,15)
    >>> rect_c = (20, 20, 30, 30) # Top-left (20,20), Bottom-right (30,30)
    >>> rectangles_overlap(rect_a, rect_b)
    True
    >>> rectangles_overlap(rect_a, rect_c)
    False
    """
    x1_a, y1_a, x2_a, y2_a = rect1
    x1_b, y1_b, x2_b, y2_b = rect2
    # Check for horizontal separation
    if x2_a < x1_b or x1_a > x2_b:
        return False
    # Check for vertical separation (y-coordinates increase downwards)
    if y2_a < y1_b or y1_a > y2_b:
        return False
    # Overlap found
    return True


if __name__ == "__main__":
    import doctest

    doctest.testmod()
