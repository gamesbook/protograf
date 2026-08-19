# -*- coding: utf-8 -*-
"""
Create custom objects for protograf
"""

# lib
import logging
import math
import random

# third party
from pymupdf import Point as muPoint

# local
from protograf import globals
from protograf.shapes_utils import draw_line
from protograf.utils import colrs, geoms, tools

# STANDARD_CARD_SIZES
from protograf.utils.tools import _lower
from protograf.utils.messaging import feedback
from protograf.utils.structures import (
    Point,
    ShapeGeometry,
    Tetris3D,
)  # named tuples
from protograf.base import BaseShape
from protograf.shapes import BandShape
from protograf.shapes_polygon import PolygonShape
from protograf.shapes_circle import CircleShape
from protograf.shapes_rectangle import RectangleShape
from protograf.shapes_hexagon import HexShape

log = logging.getLogger(__name__)
DEBUG = False


class CubeObject(HexShape):
    """
    A pseudo-3D view of a cube as an isometric drawing.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(CubeObject, self).__init__(_object=_object, canvas=canvas, **kwargs)
        # overrides
        self.orientation = "pointy"
        if not self.shades or self.radii_stroke != colrs.get_color(globals.black):
            self.radii = "s ne nw"

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a cube on a given canvas."""
        return super().draw(cnv, off_x, off_y, ID, **kwargs)


class PolyominoObject(RectangleShape):
    """
    A plane geometric figure formed by joining one or more equal squares edge to edge.
    It is a polyform whose cells are squares.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(PolyominoObject, self).__init__(_object=_object, canvas=canvas, **kwargs)
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
        self.gap = tools.as_float(kwargs.get("gap", 0), "gap")
        self.pattern = kwargs.get("pattern", ["1"])
        self.invert = kwargs.get("invert", None)
        self.fills = kwargs.get("fills", [])
        self.labels = kwargs.get("labels", [])
        self.strokes = kwargs.get("strokes", [])
        self.centre_shapes = kwargs.get("centre_shapes", [])
        # defaults
        self._fill, self._centre_shape, self._stroke = (
            self.fill,
            self.centre_shape,
            self.stroke,
        )
        self.is_outline = True if (self.outline_stroke or self.outline_width) else False
        # validate
        correct, issue = self.validate_properties()
        if not correct:
            feedback("Problem with polyomino settings: %s." % "; ".join(issue), True)
        # tetris
        self.letter = kwargs.get("letter", None)
        self.tetris = kwargs.get("tetris", False)
        self.is_tetronimo = False  # see draw()

    def numeric_pattern(self):
        """Generate numeric-equivalent of pattern matrix."""
        numbers = []
        for item in self.pattern:
            values = [int(item[i]) for i in range(0, len(item))]
            numbers.append(values)
        return numbers

    def validate_properties(self):
        correct = True
        issue = []
        if self.gap > 0 and self.is_outline:
            issue.append("Both gap and outline cannot be set at the same time!")
            correct = False
        if self.invert:
            if _lower(self.invert) not in [
                "lr",
                "leftright",
                "rl",
                "rightleft",
                "tb",
                "topbottom",
                "bt",
                "bottomtop",
            ]:
                issue.append(f'"{self.invert}" is an invalid reverse value!')
                correct = False
        if not isinstance(self.pattern, list):
            issue.append(f'pattern must be a list of strings (not "{self.pattern}")!')
            correct = False
        else:
            for key, item in enumerate(self.pattern):
                if key == 0:
                    length = len(item)
                else:
                    if not isinstance(item, str) or len(item) != length:
                        correct = False
                        issue.append(
                            f'pattern must be a list of equal-length strings (not "{
                                                                              self.pattern})"!'
                        )
                        break
                values = [item[i] for i in range(0, len(item))]
                for val in values:
                    try:
                        int(val)
                    except ValueError:
                        correct = False
                        issue.append(
                            f'pattern must contain a list of strings with integers (not "{
                                                                                    item})"!'
                        )
                        break

        return correct, issue

    def calculate_area(self) -> float:
        return self._u.width * self._u.height

    def calculate_perimeter(self, units: bool = False) -> float:
        """Total length of bounding line."""
        length = 2.0 * (self._u.width + self._u.height)
        if units:
            return self.peaks_to_value(length)
        else:
            return length

    def get_perimeter_lines(self, cnv=None, ID=None, **kwargs) -> list:
        """Calculate set of lines that form perimeter of Polyonimo"""
        perimeter_lines = []
        max_row = len(self.int_pattern)
        max_col = len(self.int_pattern[0])
        for row, item in enumerate(self.int_pattern):
            off_y = row * self.side  # NB - no gap
            for col, number in enumerate(item):
                if number == 0:
                    continue
                off_x = col * self.side
                super().set_abs_and_offset(
                    cnv=cnv, off_x=off_x, off_y=off_y, ID=ID, **kwargs
                )
                vtx = super()._shape_vertexes  # clockwise from top-right
                # handle edges
                if col == 0:  # left edge
                    perimeter_lines.append((vtx[2], vtx[3]))
                if row == 0:  # top edge
                    perimeter_lines.append((vtx[3], vtx[0]))
                if col == max_col - 1:  # right edge
                    perimeter_lines.append((vtx[0], vtx[1]))
                if row == max_row - 1:  # bottom edge
                    perimeter_lines.append((vtx[1], vtx[2]))
                # left
                try:
                    number = self.int_pattern[row][col - 1]
                    if number == 0:
                        perimeter_lines.append((vtx[2], vtx[3]))
                except:
                    pass
                # right
                try:
                    number = self.int_pattern[row][col + 1]
                    if number == 0:
                        perimeter_lines.append((vtx[0], vtx[1]))
                except:
                    pass
                # above
                try:
                    number = self.int_pattern[row - 1][col]
                    if number == 0:
                        perimeter_lines.append((vtx[3], vtx[0]))
                except:
                    pass
                # below
                try:
                    number = self.int_pattern[row + 1][col]
                    if number == 0:
                        perimeter_lines.append((vtx[1], vtx[2]))
                except:
                    pass
        return perimeter_lines

    def set_tetris_style(self, **kwargs):
        """Get colors and set centre-shape for Tetris Tetronimo"""
        match self.letter:
            case "i" | "I":  # aqua
                t3dcolors = Tetris3D(
                    inner="#00CDCD",
                    outer_tl="#00C3C3",
                    outer_br="#008989",
                    tritop="#00FFFF",
                    tribtm="#009898",
                )
            case "l":  # dark blue
                t3dcolors = Tetris3D(
                    inner="#0000CD",
                    outer_tl="#0000B5",
                    outer_br="#00008D",
                    tritop="#0000FF",
                    tribtm="#020198",
                )
            case "L":  # orange
                t3dcolors = Tetris3D(
                    inner="#CD6600",
                    outer_tl="#B55D00",
                    outer_br="#7F3700",
                    tritop="#FF8900",
                    tribtm="#9A4200",
                )
            case "o" | "O":  # yellow
                t3dcolors = Tetris3D(
                    inner="#CDCD00",
                    outer_tl="#BBBB00",
                    outer_br="#8D8D00",
                    tritop="#FFFF00",
                    tribtm="#9A9A00",
                )
            case "S":  # light green
                t3dcolors = Tetris3D(
                    inner="#00CD00",
                    outer_tl="#00CD00",
                    outer_br="#008F00",
                    tritop="#00FF00",
                    tribtm="#009A00",
                )
            case "s":  # red
                t3dcolors = Tetris3D(
                    inner="#CD0000",
                    outer_tl="#C20000",
                    outer_br="#8A0000",
                    tritop="#F60000",
                    tribtm="#990700",
                )
            case "t" | "T":  # purple
                t3dcolors = Tetris3D(
                    inner="#9A00CD",
                    outer_tl="#9100C1",
                    outer_br="#660199",
                    tritop="#CB00FC",
                    tribtm="#66009A",
                )
            case "*" | ".":  # grey
                t3dcolors = Tetris3D(
                    inner="#787878",
                    outer_tl="#969696",
                    outer_br="#515151",
                    tritop="#9A9A9A",
                    tribtm="#313131",
                )
            case _:
                feedback(f"The Tetronimo letter {self.letter} is unknown", True)

        swidth = 0.0247 * self.unit(self.width)
        # breakpoint()
        self.centre_shape = RectangleShape(
            width=0.8 * self.width,
            height=0.8 * self.height,
            fill=t3dcolors.inner,
            stroke=None,
            borders=[
                ("n w", swidth, t3dcolors.outer_tl),
                ("s e", swidth, t3dcolors.outer_br),
            ],
        )
        return t3dcolors.tritop, t3dcolors.tribtm

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw squares for the Polyomino on a given canvas."""
        # feedback(f'~~~ Polyomino {self.label=} // {off_x=}, {off_y=} {kwargs=}')
        # set props
        self.int_pattern = self.numeric_pattern()  # numeric version of string pattern
        if self.flip or self.invert:
            self.int_pattern = tools.transpose_lists(
                self.int_pattern, direction=self.flip, invert=self.invert
            )
        self.is_tetronimo = kwargs.get("is_tetromino", False)
        # print(f"~~~ {self.int_pattern=}")
        base_x, base_y = off_x, off_y
        # ---- squares
        for row, item in enumerate(self.int_pattern):
            off_y = base_y + row * self.side + row * self.gap
            for col, number in enumerate(item):
                off_x = base_x + col * self.side + col * self.gap
                if number != 0:
                    # set props based on the square's number
                    try:
                        kwargs["fill"] = self.fills[number - 1]
                    except:
                        kwargs["fill"] = self.fill
                    try:
                        self.centre_shape = self.centre_shapes[number - 1]
                    except:
                        self.centre_shape = self._centre_shape
                    try:
                        kwargs["stroke"] = self.strokes[number - 1]
                    except:
                        kwargs["stroke"] = self.stroke
                    try:
                        self.label = self.labels[number - 1]
                    except:
                        self.label = self._label
                    # ---- Tetris: overide colors and shape centre
                    # print(f"~~~ Polyomino {self.tetris=}  {self.is_tetronimo=}")
                    if self.tetris and self.is_tetronimo:
                        color_top, color_btm = self.set_tetris_style(**kwargs)
                        if color_top and color_btm:
                            self.slices = [color_top, color_btm]
                            # print(f"~~~ Polyomino {self.letter=} {self.slices=}")

                    kwargs["row"] = row
                    kwargs["col"] = col
                    # print(f"~~~ Polyomino {row=} {col=} {number=} {self.label=}")
                    super().draw(cnv, off_x=off_x, off_y=off_y, ID=ID, **kwargs)
                else:
                    if self.blank_fill:
                        kwargs["fill"] = self.blank_fill
                        kwargs["stroke"] = self.blank_stroke or self.stroke
                        kwargs["row"] = row
                        kwargs["col"] = col
                        super().draw(cnv, off_x=off_x, off_y=off_y, ID=ID, **kwargs)

        # ---- optional perimeter
        if self.outline_stroke or self.outline_width:
            cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
            perimeter_lines = self.get_perimeter_lines(cnv=cnv, ID=ID, **kwargs)
            for line in perimeter_lines:
                cnv.draw_line(Point(line[0].x, line[0].y), Point(line[1].x, line[1].y))
            kwargs["stroke"] = self.outline_stroke or self.stroke
            kwargs["stroke_width"] = self.outline_width or self.stroke_width
            kwargs["closed"] = False
            kwargs["fill"] = None
            self.set_canvas_props(cnv=cnv, index=ID, **kwargs)  # shape.finish()


class PentominoObject(PolyominoObject):
    """
    A plane geometric figure formed by joining five equal squares edge to edge.

    Notes:
        * The lettering convention follows that of Golomb - not the
          Games & Puzzles Issue 9 (1973)
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw squares for the Pentomino on a given canvas."""
        # feedback(f'~~~ Pentomino {self.label=} // {off_x=}, {off_y=} {kwargs=}')
        if not self.letter:
            self.letter = kwargs.get("letter", "I")
        # ---- overrides for self.letter (via a card value)
        _locale = kwargs.get("locale", None)
        if _locale:
            self.letter = tools.eval_template(self.letter, _locale)
        match self.letter:
            case "T":
                pattern = ["111", "010", "010"]
            case "U":
                pattern = ["101", "111"]
            case "V":
                pattern = ["001", "001", "111"]
            case "W":
                pattern = ["001", "011", "110"]
            case "X":
                pattern = ["010", "111", "010"]
            case "Y":
                pattern = ["01", "11", "01", "01"]
            case "Z":
                pattern = ["110", "010", "011"]
            case "F":
                pattern = ["011", "110", "010"]
            case "I":
                pattern = ["1", "1", "1", "1", "1"]
            case "L":
                pattern = ["10", "10", "10", "11"]
            case "N":
                pattern = ["01", "11", "10", "10"]
            case "P":
                pattern = ["11", "11", "10"]
            # LOWER - flipped LR
            case "t":
                pattern = ["111", "010", "010"]
            case "u":
                pattern = ["101", "111"]
            case "v":
                pattern = ["100", "100", "111"]
            case "w":
                pattern = ["001", "011", "110"]
            case "x":
                pattern = ["010", "111", "010"]
            case "y":
                pattern = ["10", "11", "10", "10"]
            case "z":
                pattern = ["011", "010", "110"]
            case "f":
                pattern = ["110", "011", "010"]
            case "i":
                pattern = ["1", "1", "1", "1", "1"]
            case "l":
                pattern = ["01", "01", "01", "11"]
            case "n":
                pattern = ["10", "11", "01", "01"]
            case "p":
                pattern = ["11", "11", "01"]
            case _:
                feedback("Pentomino letter must be selected from predefined set!", True)

        self.pattern = pattern
        super(PentominoObject, self).draw(
            cnv=cnv, off_x=off_x, off_y=off_y, ID=ID, **kwargs
        )


class TetrominoObject(PolyominoObject):
    """
    A plane geometric figure formed by joining four equal squares edge to edge.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw squares for the Tetromino on a given canvas."""
        # feedback(f'~~~ Tetromino {self.label=} // {off_x=}, {off_y=} {kwargs=}')
        if not self.letter:
            self.letter = kwargs.get("letter", "I")
        # ---- overrides for self.letter (via a card value)
        _locale = kwargs.get("locale", None)
        if _locale:
            self.letter = tools.eval_template(self.letter, _locale)
        match self.letter:
            case "I":
                pattern = [
                    "1",
                    "1",
                    "1",
                    "1",
                ]
            case "L":
                pattern = ["10", "10", "11"]
            case "O":
                pattern = ["11", "11"]
            case "S":
                pattern = ["011", "110"]
            case "T":
                pattern = ["111", "010"]
            # LOWER - flipped LR
            case "i":
                pattern = [
                    "1",
                    "1",
                    "1",
                    "1",
                ]
            case "l":
                pattern = ["01", "01", "11"]
            case "o":
                pattern = ["11", "11"]
            case "s":
                pattern = ["110", "011"]
            case "t":
                pattern = ["111", "010"]
            case "*" | ".":
                pattern = ["1"]
            case _:
                feedback("Tetromino letter must be selected from predefined set!", True)

        kwargs["is_tetromino"] = True
        kwargs["letter"] = self.letter
        self.pattern = pattern
        super(TetrominoObject, self).draw(
            cnv=cnv, off_x=off_x, off_y=off_y, ID=ID, **kwargs
        )


class StarFieldObject(BaseShape):
    """Draw StarField pattern on a given canvas.

    Reference:

        https://codeboje.de/starfields-and-galaxies-python/

    TODO:

        Implement the createElipticStarfield()
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(StarFieldObject, self).__init__(_object=_object, canvas=canvas, **kwargs)
        self.kwargs = kwargs
        # override to set the randomisation sequence
        if self.seeding:
            self.seed = tools.as_float(self.seeding, "seeding")
        else:
            self.seed = None
        # validation
        for size in self.sizes:
            tools.as_float(size, 'the Starfield "size"', minimum=0.000000001)

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
            ccentre = self.enclosure._shape_centre
            x_c, y_c = ccentre.x, ccentre.y
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
        area = math.sqrt(self.enclosure._shape_area)
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


class DiceObject(BaseShape):
    """
    Parent class to handle common routines for all Shapes with a D6 'face'.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(DiceObject, self).__init__(_object=_object, canvas=canvas, **kwargs)

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
        shape_name: str = "shape",
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
            except:
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
        super(D6Object, self).__init__(_object=_object, canvas=canvas, **kwargs)
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
            feedback("Problem with D6 settings: %s." % "; ".join(issue), True)

    def validate_properties(self):
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
                "D6",
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
        super(DominoObject, self).__init__(_object=_object, canvas=canvas, **kwargs)
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
            feedback("Problem with Domino settings: %s." % "; ".join(issue), True)

    def validate_properties(self):
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


class CardBoxObject(BaseShape):
    """Draw CardBox outline on a given canvas.

    Reference:

    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(CardBoxObject, self).__init__(_object=_object, canvas=canvas, **kwargs)
        self.kwargs = kwargs
        card_size = self.kwargs.get("card_size", "Poker")
        card_hw = tools.card_size(card_size, globals.margins.units_type)
        # ----  overrides to create sensible defaults
        if not kwargs.get("height"):
            self.height = card_hw[1]
        if not kwargs.get("width"):
            self.width = card_hw[0]
        if not kwargs.get("depth"):
            self.depth = 51.0 / globals.units  # ~ 1.8 cm or 0.7"
        # print(f'***  pos: {self.x=} {self.y=}')
        # print(f'*** size: {self.height=} {self.width=} {self.depth=}')
        self.set_unit_properties()
        # ---- user-selections
        _fg = kwargs.get("flap_glue", None)
        self._flap_glue = (
            tools.as_float(_fg, "flap_glue") * globals.units if _fg else None
        )
        _fi = kwargs.get("flap_inner", None)
        self._flap_inner = (
            tools.as_float(_fi, "flap_inner") * globals.units if _fi else None
        )
        _ft = kwargs.get("flap", None)
        self._flap_tuck = tools.as_float(_ft, "flap") * globals.units if _ft else None
        self._flap_size = 0  # NB!! see _shape_vertexes => calculated based on flap_tuck
        _th = kwargs.get("thumb", None)
        self._thumb = tools.as_float(_th, "thumb") * globals.units if _th else None
        self._padding = self.padding * globals.units if self.padding else None
        self._padding_width = (
            self.padding_width * globals.units if self.padding_width else self._padding
        )
        self._padding_height = (
            self.padding_height * globals.units
            if self.padding_height
            else self._padding
        )
        # ---- placeholders for user-defined items to be drawn
        self.shapes_front = kwargs.get("shapes_front", None)
        self.shapes_back = kwargs.get("shapes_back", None)
        self.shapes_left = kwargs.get("shapes_left", None)
        self.shapes_right = kwargs.get("shapes_right", None)
        self.shapes_top = kwargs.get("shapes_top", None)
        self.shapes_bottom = kwargs.get("shapes_bottom", None)
        self.shapes_wrap = kwargs.get("shapes_wrap", None)  # front,left,right,back
        # ---- vertices for panels
        # topleft, topright, bottomright, bottomleft
        self.panel_front = []
        self.panel_back = []
        self.panel_left = []
        self.panel_right = []
        self.panel_wrap = []
        # need placeholders because drawing order does not match
        self.panel_top = [None, None, None, None]
        self.panel_bottom = [None, None, None, None]
        # ---- set vertices and panel_* for point-based draw
        self.vertexes = self._shape_vertexes

    @property
    def shape_centre(self) -> Point:
        """Centre of CardBoxObject."""
        if self.cx and self.cy:
            return Point(self.cx, self.cy)
        return None

    @property
    def geo(self) -> ShapeGeometry:
        """Geometry of CardBoxObject in user units."""
        return ShapeGeometry()

    @property
    def geometry(self) -> ShapeGeometry:
        """Geometry of CardBoxObject - alias for geo."""
        return self.geo

    @property  # must be able to change e.g. for layout
    def _shape_vertexes(self):
        """Vertices and Panels of CardBoxObject in points."""

        def next(ax, ay):
            vertices.append(Point(ax, ay))
            return ax, ay

        default_padding = 2 * 2.83465  # 2mm padding all round
        padding_height = (
            self._padding_height
            if self._padding_height is not None
            else default_padding
        )
        padding_width = (
            self._padding_width if self._padding_width is not None else default_padding
        )
        w_p = self._u.width + padding_width
        h_p = self._u.height + padding_height
        d_p = self._u.depth
        # ---- flaps
        flap = self._flap_inner if self._flap_inner is not None else 0.25 * w_p
        flap_tuck = self._flap_tuck if self._flap_tuck is not None else 0.15 * w_p
        if flap_tuck * 2.0 > w_p:
            feedback("Flap size cannot be greater than half of the box width.", True)
        self._flap_size = flap_tuck
        flap_glue = self._flap_glue if self._flap_glue is not None else 0.66 * d_p
        # print(f'*** size: {h_p=} {w_p=} {d_p=} {flap=} {flap_tuck=} {flap_glue=}')
        FI1 = 0.1
        FI2 = 0.8
        flap_offcut = flap_tuck  # create 45 deg angle OR use for quarter-round
        flap_midcut = w_p - 2 * flap_offcut

        # ---- vertices
        vertices = []
        offset_y = flap_tuck + d_p - flap
        sx, sy = (
            self._u.x + self._u.margin_left,
            self._u.y + self._u.margin_top + offset_y,
        )
        # ... TOP EDGE
        px, py = next(sx, sy)  # 0
        self.panel_front.append(Point(px, py))  # TL
        self.panel_top[3] = Point(px, py)  # BL
        px, py = next(px, py - d_p)  # 1
        self.panel_top[0] = Point(px, py)  # TL
        px, py = next(px + flap_offcut, py - flap_tuck)  # 2
        px, py = next(px + flap_midcut, py)  # 3
        px, py = next(px + flap_offcut, py + flap_tuck)  # 4
        self.panel_top[1] = Point(px, py)  # TR
        px, py = next(px, sy)  # 5
        self.panel_front.append(Point(px, py))  # TR
        self.panel_right.append(Point(px, py))  # TL
        self.panel_top[2] = Point(px, py)  # BR
        px, py = next(px + FI1 * d_p, py - flap)  # 6
        px, py = next(px + FI2 * d_p, py)  # 7
        px, py = next(px + FI1 * d_p, py + flap)  # 8
        self.panel_right.append(Point(px, py))  # TR
        self.panel_back.append(Point(px, py))  # TL
        px, py = next(px + w_p, py)  # 9
        self.panel_left.append(Point(px, py))  # TL
        self.panel_back.append(Point(px, py))  # TR
        px, py = next(px + FI1 * d_p, py - flap)  # 10
        px, py = next(px + FI2 * d_p, py)  # 11
        px, py = next(px + FI1 * d_p, py + flap)  # 12
        self.panel_left.append(Point(px, py))  # TR
        # ... BOTTOM EDGE
        px, py = next(px, py + h_p)  # 13
        self.panel_left.append(Point(px, py))  # BR
        px, py = next(px - FI1 * d_p, py + flap)  # 14
        px, py = next(px - FI2 * d_p, py)  # 15
        px, py = next(px - FI1 * d_p, py - flap)  # 16
        self.panel_left.append(Point(px, py))  # BL
        self.panel_back.append(Point(px, py))  # BR
        self.panel_bottom[1] = Point(px, py)  # TR
        px, py = next(px, py + d_p)  # 17
        self.panel_bottom[2] = Point(px, py)  # BR
        px, py = next(px - flap_offcut, py + flap_tuck)  # 18
        px, py = next(px - flap_midcut, py)  # 19
        px, py = next(px - flap_offcut, py - flap_tuck)  # 20
        self.panel_bottom[3] = Point(px, py)  # BL
        px, py = next(px, py - d_p)  # 21
        self.panel_back.append(Point(px, py))  # BL
        self.panel_bottom[0] = Point(px, py)  # TL
        self.panel_right.append(Point(px, py))  # BR
        px, py = next(px - FI1 * d_p, py + flap)  # 22
        px, py = next(px - FI2 * d_p, py)  # 23
        px, py = next(px - FI1 * d_p, py - flap)  # 24
        self.panel_front.append(Point(px, py))  # BR
        self.panel_right.append(Point(px, py))  # BL
        px, py = next(sx, py)  # 25
        self.panel_front.append(Point(px, py))  # BL
        # ... GLUE FLAP
        px, py = next(px - flap_glue, py - 0.05 * h_p)  # 26
        px, py = next(px, py - 0.9 * h_p)  # 27
        # ... START
        px, py = next(sx, sy)  # 0

        # wrap
        # topleft, topright, bottomright, bottomleft
        self.panel_wrap = [
            self.panel_front[0],
            self.panel_left[1],
            self.panel_left[2],
            self.panel_front[3],
        ]

        return vertices

    def draw_item(self, item, area):
        """Draw one or shapes on an area of the card"""
        if item is None:
            return
        _cx = (area[1].x - area[0].x) / 2.0 + area[0].x
        _cy = (area[3].y - area[0].y) / 2.0 + area[0].y
        if isinstance(item, (list, tuple)):
            for shp in item:
                if shp is not None:
                    shp.draw(_abs_cx=_cx, _abs_cy=_cy)  # used by set_abs_and_offset()
        else:
            if item is not None:
                item.draw(_abs_cx=_cx, _abs_cy=_cy)  # used by set_abs_and_offset()

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw the CardBoxObject on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- draw outline by vertices
        # feedback(f'***CardBoxObject {x=} {y=} {self.vertexes=}')
        if self.vertexes:
            for key, vertex in enumerate(self.vertexes):
                if key < len(self.vertexes) - 1:
                    # ---- * curved flaps
                    if self.rounded and key in [1, 3, 17, 19]:
                        if key in [1, 17]:
                            midpt = Point(vertex.x, self.vertexes[key + 1].y)
                        else:
                            midpt = Point(self.vertexes[key + 1].x, vertex.y)
                        cnv.draw_curve(vertex, midpt, self.vertexes[key + 1])
                    else:
                        draw_line(
                            cnv, vertex, self.vertexes[key + 1], shape=self, **kwargs
                        )
                else:
                    draw_line(cnv, vertex, self.vertexes[0], shape=self, **kwargs)
            kwargs["closed"] = True
            if kwargs.get("rounded"):
                kwargs["lineJoin"] = 1
            self.set_canvas_props(cnv=cnv, index=ID, **kwargs)

        # ---- process folds (OVER any fill for box)
        if self.vertexes and self.fold:
            # ---- * set fold style
            pargs = {}
            pargs["stroke"] = self.fold_stroke
            pargs["stroke_width"] = self.fold_stroke_width
            pargs["dotted"] = self.fold_dotted
            pargs["dashed"] = self.fold_dashed
            pargs["closed"] = False
            pargs["fill"] = None
            # ----- * draw fold lines
            cnv.draw_line(self.panel_left[0], self.panel_left[1])
            cnv.draw_line(self.panel_left[2], self.panel_left[3])
            cnv.draw_line(self.panel_front[0], self.panel_front[3])
            cnv.draw_line(self.panel_front[1], self.panel_front[2])
            cnv.draw_line(self.panel_right[0], self.panel_right[1])
            cnv.draw_line(self.panel_right[2], self.panel_right[3])
            cnv.draw_line(self.panel_back[0], self.panel_back[3])
            cnv.draw_line(self.panel_back[1], self.panel_back[2])
            cnv.draw_line(self.panel_top[0], self.panel_top[1])
            cnv.draw_line(self.panel_top[2], self.panel_top[3])
            cnv.draw_line(self.panel_bottom[0], self.panel_bottom[1])
            cnv.draw_line(self.panel_bottom[2], self.panel_bottom[3])
            self.set_canvas_props(cnv=cnv, index=ID, **pargs)

        # ---- draw wrap-around shape/image
        self.draw_item(self.shapes_wrap, self.panel_wrap)
        # ---- draw front shape/image
        self.draw_item(self.shapes_front, self.panel_front)
        # ---- draw back shape/image
        self.draw_item(self.shapes_back, self.panel_back)
        # ---- draw top shape/image
        self.draw_item(self.shapes_top, self.panel_top)
        # ---- draw bottom shape/image
        self.draw_item(self.shapes_bottom, self.panel_bottom)
        # ---- draw left shape/image
        self.draw_item(self.shapes_left, self.panel_left)
        # ---- right shape/image
        self.draw_item(self.shapes_right, self.panel_right)

        # ---- draw thumb
        if self._thumb:
            midx = (
                self.panel_back[1].x - self.panel_back[0].x
            ) / 2.0 + self.panel_back[0].x
            tcentre = Point(midx, self.panel_back[1].y)
            tstart = Point(midx - (self._thumb / 2.0), self.panel_back[1].y)
            cnv.draw_sector(
                (tcentre.x, tcentre.y),
                (tstart.x, tstart.y),
                180,
                fullSector=False,
            )
            kwargs["closed"] = False
            kwargs["fill"] = None
            self.set_canvas_props(cnv=cnv, index=ID, **kwargs)


class RaceTrackObject(BaseShape):
    """Draw RaceTrack composite shape on a given canvas.

    Reference:

    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(RaceTrackObject, self).__init__(_object=_object, canvas=canvas, **kwargs)
        self.kwargs = kwargs
        self.set_unit_properties()
        # ---- validate user-choices
        self.stages = kwargs.get("stages", None)
        if not self.stages:
            feedback(
                "The RaceTrack 'stages' property must be a list of one or more Rectangles and Bands.",
                True,
            )
        if not isinstance(self.stages, (list, tuple)):
            feedback(
                "The RaceTrack 'stages' property must be in the form of a list,"
                f" not a '{type(self.stages).__name__}'.",
                True,
            )
        for stage in self.stages:
            if not isinstance(stage, (RectangleShape, BandShape)):
                invalid = stage.simple_name()
                feedback(
                    f"Each stage must be either a Rectangle or a Band - not a {invalid}.",
                    True,
                    True,
                )

    @property
    def shape_centre(self) -> Point:
        """Centre of RaceTrackObject."""
        return None

    @property
    def geo(self) -> ShapeGeometry:
        """Geometry of RaceTrackObject in user units."""
        return ShapeGeometry()

    @property
    def geometry(self) -> ShapeGeometry:
        """Geometry of RaceTrackObject - alias for geo."""
        return self.geo

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw the RaceTrackObject on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- draw by stage
        old_stage, track_height = None, 0.0
        for key, stage in enumerate(self.stages):
            if key == 0:
                # print("\nstage:first")
                # FIRST stage ONLY - draw "as is"
                stage.draw()
                old_stage = stage
                # use settings of first stage to determine kwarg overrides
                track_height = stage.geo.height
            if key > 0:
                # print(key, type(stage), f"{old_stage.geo.nw=}", f"{old_stage.geo.sw=}")
                supplied_kwargs = stage.kwargs
                supplied_kwargs["height"] = track_height
                stage_type = type(stage)
                # coordinates of old_stage used to calculate props of this stage
                if getattr(old_stage, "inverted", False):
                    # previous curve was drawn bulging "inwards"
                    old_nw = old_stage.geo.se
                    old_sw = old_stage.geo.ne
                else:
                    old_nw = old_stage.geo.nw
                    old_sw = old_stage.geo.sw
                if isinstance(stage, RectangleShape):
                    # print("\nstage:rect")
                    new_center, new_rotation = geoms.racetrack_rectangle_properties(
                        ur=old_sw, lr=old_nw, width=stage.width
                    )
                    supplied_kwargs.pop("x", None)
                    supplied_kwargs.pop("y", None)
                    supplied_kwargs.pop("cxy", None)
                    supplied_kwargs["x"] = new_center.x - stage.width / 2.0
                    supplied_kwargs["y"] = new_center.y - track_height / 2.0
                    supplied_kwargs["rotation"] = 360.0 - new_rotation
                elif isinstance(stage, BandShape):
                    # print("\nstage:band")
                    if track_height > stage.radius:
                        feedback(
                            f"The RaceTrack's adjusted Band height is greater than its radius",
                            True,
                            True,
                        )
                    corner_to_centre = stage.radius - track_height
                    if stage.inverted:  # draw with curve towards the "inside"
                        new_rotation = (
                            geoms.angle_between_points(first=old_nw, second=old_sw)
                            - stage.angle_width
                        )

                        pid = geoms.point_in_direction(
                            point_start=old_sw,
                            point_end=old_nw,
                            distance_factor=corner_to_centre / track_height,
                        )
                    else:
                        new_rotation = geoms.angle_between_points(
                            first=old_sw, second=old_nw
                        )

                        pid = geoms.point_in_direction(
                            point_start=old_nw,
                            point_end=old_sw,
                            distance_factor=corner_to_centre / track_height,
                        )

                    supplied_kwargs.pop("width", None)
                    supplied_kwargs["angle_start"] = new_rotation
                    supplied_kwargs["cx"] = pid.x
                    supplied_kwargs["cy"] = pid.y
                    # print(f"band {pid=} angle_start={new_rotation}")
                else:
                    raise ValueError(
                        f'A RaceTrack cannot contain shapes of type "{stage_type}"'
                    )
                shadow_stage = stage_type(canvas=globals.canvas, **supplied_kwargs)
                shadow_stage.draw()
                old_stage = shadow_stage
