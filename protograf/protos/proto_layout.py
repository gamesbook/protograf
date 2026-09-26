# -*- coding: utf-8 -*-
"""
Primary interface for protograf (imported at top-level)

Note:
    Some imports here are for sake of reuse by the top-level import
"""

# lib
from contextlib import suppress
from copy import copy
import logging

# third party

# project
from protograf import globals
from protograf.base import BaseShape, WIDTH
from protograf.utils import colrs, tools
from protograf.utils.messaging import feedback
from protograf.utils.structures import (
    DirectionGroup,
    Locale,
    Point,
    Place,
)
from protograf.utils.tools import (  # used in scripts
    _lower,
)

# local
from .proto_shapes import (
    Dot,
    Rectangle,
    Rhombus,
    Triangle,
)

# local
from . import utils  # globals_set, validate_globals, margins

log = logging.getLogger(__name__)


class LayoutGrid:
    """Draw shape(s) or lines in locations, cols, & rows in a virtual layout"""

    def __init__(self, grid, **kwargs):
        utils.validate_globals()
        self.grid = grid

        self.grid_classname = self.grid.__class__.__name__ if grid else ""
        kwargs = kwargs
        shapes = kwargs.get("shapes", [])  # shapes or Places
        corners = kwargs.get("corners", [])  # shapes or Places for corners only!
        # set this property if location centres should be joined with lines
        self.lines = tools.as_bool(kwargs.get("draw_lines", False))
        rotations = kwargs.get("rotations", [])  # rotations for an edge
        if kwargs.get("masked") and isinstance(kwargs.get("masked"), str):
            self.masked = tools.sequence_split(kwargs.get("masked"), "masked")
        else:
            self.masked = kwargs.get("masked", [])
        if kwargs.get("visible") and isinstance(kwargs.get("visible"), str):
            self.visible = tools.integer_pairs(kwargs.get("visible"), "visible")
        else:
            self.visible = kwargs.get("visible", [])
        # ---- internal control
        self._draw_grid = tools.as_bool(
            kwargs.get("_draw_grid", True), allow_none=False
        )
        self.do_debug = kwargs.get("debug", None)
        # ---- grid setup
        self.locations = kwargs.get("locations", [])
        self.location_rows = kwargs.get("rows", [])
        self.location_cols = kwargs.get("cols", [])
        self.layout_grid = kwargs.get("gridlines", None)  # directions ...
        _grid_stroke = kwargs.get("gridlines_stroke", globals.black)
        self.layout_grid_ends = kwargs.get("gridlines_ends", None)
        self.layout_grid_fill = kwargs.get("gridlines_fill", None)
        self.layout_grid_stroke = colrs.get_color(_grid_stroke)
        self.layout_grid_stroke_width = kwargs.get("gridlines_stroke_width", WIDTH)
        self.layout_grid_dotted = kwargs.get("gridlines_dotted", False)
        self.layout_grid_dashed = kwargs.get("gridlines_dashed", None)
        self.layout_grid_transparency = kwargs.get("gridlines_transparency", None)
        # ---- process grid
        corners_dict = self.validate_inputs(shapes, corners)
        if self._draw_grid:
            self.draw_the_grid()
        _locations = self.process_locations()
        rotation_sequence = self.process_rotations(rotations)
        if self.lines and self._draw_grid:
            self.draw_lines(_locations)
        # NOTE!  test for valid shapes and/or debug reside INSIDE the function!
        self.draw_shapes(shapes, _locations, rotation_sequence, corners_dict)

    def validate_inputs(self, shapes, corners):
        from protograf.shapes.virtuals import VirtualLocations

        # ---- validate inputs
        if not shapes:
            feedback(
                f"There is no list of {self.grid_classname} shapes to draw!",
                False,
                True,
            )
        if shapes and not isinstance(shapes, list):
            feedback(
                f"The values for {self.grid_classname} 'shapes' must be in a list!",
                True,
            )
        if not isinstance(self.grid, VirtualLocations):
            feedback(f"The grid type '{self.grid_classname} ' is not valid!", True)
        corners_dict = {}
        if corners:
            if not isinstance(corners, list):
                feedback(
                    f"The {self.grid_classname} corners value '{corners}' is not a valid list!",
                    True,
                )
            for corner in corners:
                try:
                    value = corner[0]
                    shape = corner[1]
                    if _lower(value) not in ["nw", "ne", "sw", "se", "*"]:
                        feedback(
                            f'The {self.grid_classname} corner must be one of nw, ne, sw, se (not "{value}")!',
                            True,
                        )
                    if not isinstance(shape, BaseShape):
                        feedback(
                            f'The {self.grid_classname} corner item must be a shape (not "{shape}") !',
                            True,
                        )
                    if value == "*":
                        corners_dict["nw"] = shape
                        corners_dict["ne"] = shape
                        corners_dict["sw"] = shape
                        corners_dict["se"] = shape
                    else:
                        corners_dict[value] = shape
                except Exception:
                    feedback(
                        f'The {self.grid_classname} corners setting "{corner}" is not a valid list',
                        True,
                    )
        return corners_dict

    def max_cols_max_rows(self, locations: list) -> tuple:
        """Get the maximum column and row values from a list of locations"""
        """
            Locale(
                col=loc[1].col,
                row=loc[1].row,
                x=loc[1].x,
                y=loc[1].y,
                xy=Point(loc[1].x, loc[1].y),
                id=f"{loc[1].col}:{loc[1].row}",  # ,loc[1].id,
                sequence=key,
                corner=loc[1].corner,
                page=globals.page_count + 1,
            ),
        """
        row, col = 0, 0
        for loc in locations:
            _loc = loc[1]
            col = _loc.col if _loc.col > col else col
            row = _loc.row if _loc.row > row else row
        return col, row

    def locale_by_col_and_row(self, locations: list, col: int, row: int) -> Locale:
        """Get a Locale by its column and row value from a list of locations"""
        for loc in locations:
            _loc = loc[1]
            if _loc.col == col and _loc.row == row:
                return _loc
        return None

    def draw_lines(self, _locations: list):
        """Draw gridlines between location centres"""
        if self.lines:
            match self.grid_classname:
                case "DiamondLocations":
                    raise NotImplementedError(
                        "DiamondLocations cannot be connected with lines"
                    )
                case "TriangularLocations":
                    raise NotImplementedError(
                        "TriangularLocations cannot be connected with lines"
                    )
                case "RectangularLocations":
                    max_cols, max_rows = self.max_cols_max_rows(_locations)
                    for row in range(1, max_rows):
                        for col in range(1, max_cols):
                            loc = self.locale_by_col_and_row(_locations, col, row)
                            if loc.col == max_cols:
                                continue  # skip locations in the end column
                            if loc.row == max_rows:
                                continue  # skip locations in the end row
                            next_col_loc = self.locale_by_col_and_row(
                                _locations, col + 1, row
                            )
                            next_row_loc = self.locale_by_col_and_row(
                                _locations, col, row + 1
                            )
                            height = next_row_loc.y - loc.y
                            width = next_col_loc.x - loc.x
                            cxy = Point(loc.x + width / 2.0, loc.y + height / 2.0)
                            Rectangle(
                                x=loc.x,
                                y=loc.y,
                                # cxy=cxy,
                                height=height,
                                width=width,
                                stroke=self.layout_grid_stroke,
                                stroke_width=self.layout_grid_stroke_width,
                                stroke_ends=self.layout_grid_ends,
                                dotted=self.layout_grid_dotted,
                                dashed=self.layout_grid_dashed,
                                fill=self.layout_grid_fill,
                            )
                case _:
                    feedback(
                        f"The grid type '{self.grid_classname}' does not support gridlines!",
                        True,
                    )

    def draw_the_grid(self):
        """Draw the grid (using a regular Shape)"""
        if self.layout_grid:
            self.layout_grid_centroid = self.grid.grid_centroid  # calculated in layouts
            match self.grid_classname:
                case "DiamondLocations":
                    # ---- get gridlines params
                    self.layout_grid_dirs = tools.validated_gridlines(
                        self.layout_grid, DirectionGroup.COMPASS, "gridlines"
                    )
                    self.layout_grid_hatches = (
                        self.grid.cols // 2 - 1
                    )  # for Diamond, rows == cols
                    # ---- setup gridlines configuration # eg.  [('d', 10), ('ne', 10)]
                    gridlines_count = {
                        "n": self.grid.cols // 2,
                        "s": self.grid.cols // 2,
                        "e": self.grid.rows // 2,
                        "w": self.grid.rows // 2,
                        "ne": self.grid.cols // 2 - 1,
                        "nw": self.grid.cols // 2 - 1,
                        "se": self.grid.rows // 2 - 1,
                        "sw": self.grid.rows // 2 - 1,
                    }
                    gridlines_config = [
                        (_dir, gridlines_count[_dir]) for _dir in self.layout_grid_dirs
                    ]
                    # ---- draw lines
                    if self._draw_grid:
                        Rhombus(
                            cx=self.layout_grid_centroid.x,
                            cy=self.layout_grid_centroid.y,
                            height=self.grid.total_height,
                            width=self.grid.total_width,
                            stroke=self.layout_grid_stroke,
                            stroke_width=self.layout_grid_stroke_width,
                            stroke_ends=self.layout_grid_ends,
                            dotted=self.layout_grid_dotted,
                            dashed=self.layout_grid_dashed,
                            fill=self.layout_grid_fill,
                            transparency=self.layout_grid_transparency,
                            hatches_count=self.layout_grid_hatches,
                            hatches=gridlines_config,
                            hatches_stroke=self.layout_grid_stroke,
                            hatches_stroke_width=self.layout_grid_stroke_width,
                            hatches_ends=self.layout_grid_ends,
                            hatches_dotted=self.layout_grid_dotted,
                            hatches_dashed=self.layout_grid_dashed,
                            # rotation=0,
                        )
                case "RectangularLocations":
                    # ---- get gridlines params
                    self.layout_grid_dirs = tools.validated_gridlines(
                        self.layout_grid, DirectionGroup.COMPASS, "gridlines"
                    )
                    # ---- NO diags for unequal rows & cols:
                    if self.grid.cols != self.grid.rows:
                        with suppress(ValueError):
                            self.layout_grid_dirs.remove("ne")
                        with suppress(ValueError):
                            self.layout_grid_dirs.remove("nw")
                        with suppress(ValueError):
                            self.layout_grid_dirs.remove("se")
                        with suppress(ValueError):
                            self.layout_grid_dirs.remove("sw")
                        with suppress(ValueError):
                            self.layout_grid_dirs.remove("d")
                    self.layout_grid_hatches = self.grid.cols
                    # ---- setup gridlines configuration
                    gridlines_config = (
                        self.layout_grid
                    )  # eg. '*', 'd', 'ne' etc. or [('d', 10)]
                    gridlines_count = {
                        "n": self.grid.cols // 2,
                        "s": self.grid.cols // 2,
                        "e": self.grid.rows // 2 + 1,
                        "w": self.grid.rows // 2 + 1,
                        "ne": self.grid.cols + 1,
                        "nw": self.grid.cols + 1,
                        "se": self.grid.rows + 1,
                        "sw": self.grid.rows + 1,
                    }
                    gridlines_config = [
                        (_dir, gridlines_count[_dir]) for _dir in self.layout_grid_dirs
                    ]
                    # ---- draw lines
                    if self._draw_grid:
                        Rectangle(
                            cx=self.layout_grid_centroid.x,
                            cy=self.layout_grid_centroid.y,
                            height=self.grid.total_height,
                            width=self.grid.total_width,
                            stroke=self.layout_grid_stroke,
                            stroke_width=self.layout_grid_stroke_width,
                            stroke_ends=self.layout_grid_ends,
                            dotted=self.layout_grid_dotted,
                            dashed=self.layout_grid_dashed,
                            fill=self.layout_grid_fill,
                            transparency=self.layout_grid_transparency,
                            hatches_count=self.layout_grid_hatches,
                            hatches=gridlines_config,
                            hatches_stroke=self.layout_grid_stroke,
                            hatches_stroke_width=self.layout_grid_stroke_width,
                            hatches_ends=self.layout_grid_ends,
                            hatches_dotted=self.layout_grid_dotted,
                            hatches_dashed=self.layout_grid_dashed,
                            # rotation=rotation,
                        )
                case "TriangularLocations":
                    # ---- get gridlines params
                    self.layout_grid_dirs = tools.validated_gridlines(
                        self.layout_grid, DirectionGroup.TRIANGULAR_HATCH, "gridlines"
                    )
                    self.layout_grid_hatches = (
                        self.grid.cols // 2 - 1
                    )  # for Diamond, rows == cols
                    # ---- setup gridlines configuration # eg.  [('d', 10), ('ne', 10)]
                    match self.grid.facing:
                        case "north" | "south":
                            gridlines_count = {
                                "e": self.grid.rows * 2,
                                "w": self.grid.rows * 2,
                                "ne": self.grid.cols // 2 + 1,
                                "nw": self.grid.cols // 2 + 1,
                                "se": self.grid.cols // 2 + 1,
                                "sw": self.grid.cols // 2 + 1,
                            }
                        case "east" | "west":
                            gridlines_count = {
                                "e": self.grid.cols * 2,
                                "w": self.grid.cols * 2,
                                "ne": self.grid.rows // 2 + 1,
                                "nw": self.grid.rows // 2 + 1,
                                "se": self.grid.rows // 2 + 1,
                                "sw": self.grid.rows // 2 + 1,
                            }
                    gridlines_config = [
                        (_dir, gridlines_count[_dir]) for _dir in self.layout_grid_dirs
                    ]
                    match self.grid.facing:
                        case "south":
                            rotation = 180
                        case "east":
                            rotation = 30
                        case "west":
                            rotation = -30
                        case _:
                            rotation = 0
                    # ---- draw lines

                    if self._draw_grid:
                        Triangle(
                            cx=self.layout_grid_centroid.x,
                            cy=self.layout_grid_centroid.y,
                            # height=self.grid.total_height,
                            side=self.grid.total_width,
                            stroke=self.layout_grid_stroke,
                            stroke_width=self.layout_grid_stroke_width,
                            stroke_ends=self.layout_grid_ends,
                            dotted=self.layout_grid_dotted,
                            dashed=self.layout_grid_dashed,
                            fill=self.layout_grid_fill,
                            transparency=self.layout_grid_transparency,
                            hatches_count=self.layout_grid_hatches,
                            hatches=gridlines_config,
                            hatches_stroke=self.layout_grid_stroke,
                            hatches_stroke_width=self.layout_grid_stroke_width,
                            hatches_ends=self.layout_grid_ends,
                            hatches_dotted=self.layout_grid_dotted,
                            hatches_dashed=self.layout_grid_dashed,
                            rotation=rotation,
                        )
                case _:
                    feedback(
                        f"The grid type '{self.grid_classname}' does not support gridlines!",
                        True,
                    )

    def process_locations(self) -> list:
        """setup locations; automatically or via user-specification"""
        _default_locations = enumerate(self.grid.next_locale())
        default_locations = [*_default_locations]
        if not self.locations and not self.location_rows and not self.location_cols:
            _locations = default_locations
        else:
            _locations = []
            user_locations = tools.integer_pairs(self.locations, label="locations")
            user_location_rows = tools.sequence_split(
                self.location_rows, to_int=True, unique=True, msg="rows"
            )
            user_location_cols = tools.sequence_split(
                self.location_cols, to_int=True, unique=True, msg="col"
            )

            # ---- pick locations according to user input
            for key, user_loc in enumerate(user_locations):
                for loc in default_locations:
                    if user_loc[0] == loc[1].col and user_loc[1] == loc[1].row:
                        new_loc = (
                            key,
                            Locale(
                                col=loc[1].col,
                                row=loc[1].row,
                                x=loc[1].x,
                                y=loc[1].y,
                                xy=Point(loc[1].x, loc[1].y),
                                id=f"{loc[1].col}:{loc[1].row}",  # ,loc[1].id,
                                sequence=key,
                                corner=loc[1].corner,
                                page=globals.page_count + 1,
                            ),
                        )
                        _locations.append(new_loc)
                default_locations = enumerate(self.grid.next_locale())  # regenerate !

            # ---- pick locations by row according to user input
            for key, user_loc in enumerate(user_location_rows):
                for loc in default_locations:
                    if user_loc == loc[1].row:
                        new_loc = (
                            key,
                            Locale(
                                col=loc[1].col,
                                row=loc[1].row,
                                x=loc[1].x,
                                y=loc[1].y,
                                xy=Point(loc[1].x, loc[1].y),
                                id=f"{loc[1].col}:{loc[1].row}",  # ,loc[1].id,
                                sequence=key,
                                corner=loc[1].corner,
                                page=globals.page_count + 1,
                            ),
                        )
                        if new_loc not in _locations:
                            _locations.append(new_loc)
                default_locations = enumerate(self.grid.next_locale())  # regenerate !

            # ---- pick locations by col according to user input
            for key, user_loc in enumerate(user_location_cols):
                for loc in default_locations:
                    if user_loc == loc[1].col:
                        new_loc = (
                            key,
                            Locale(
                                col=loc[1].col,
                                row=loc[1].row,
                                x=loc[1].x,
                                y=loc[1].y,
                                xy=Point(loc[1].x, loc[1].y),
                                id=f"{loc[1].col}:{loc[1].row}",  # ,loc[1].id,
                                sequence=key,
                                corner=loc[1].corner,
                                page=globals.page_count + 1,
                            ),
                        )
                        if new_loc not in _locations:
                            _locations.append(new_loc)
                default_locations = enumerate(self.grid.next_locale())  # regenerate !
        return _locations

    def process_rotations(self, rotations: list):
        """generate rotations - keyed per sequence number"""
        rotation_sequence = {}
        if rotations:
            for rotation in rotations:
                if not isinstance(rotation, tuple):
                    feedback("The 'rotations' must each contain a set!", True)
                if len(rotation) != 2:
                    feedback(
                        "The 'rotations' must each contain a set of two items!", True
                    )
                _key = rotation[0]
                if not isinstance(_key, str):
                    feedback(
                        "The first value for each 'rotations' entry must be a string!",
                        True,
                    )
                rotate = tools.as_float(
                    rotation[1], " second value for the 'rotations' entry"
                )
                try:
                    _keys = list(tools.sequence_split(_key))
                except Exception:
                    feedback(f'Unable to convert "{_key}" into a range of values.')
                for the_key in _keys:
                    rotation_sequence[the_key] = rotate
        return rotation_sequence

    def draw_shapes(
        self,
        shapes: list,
        _locations: list,
        rotation_sequence: dict,
        corners_dict: dict,
    ):
        """Iterate through locations & draw shape(s) and debug IDs"""
        shape_id = 0
        for count, loc in _locations:
            # print("395: time to draw locs:", count, loc)
            if self.masked and count + 1 in self.masked:  # ignore if IN masked
                continue
            if (
                self.visible and count + 1 not in self.visible
            ):  # ignore if NOT in visible
                continue
            if self.grid.stop and count + 1 >= self.grid.stop:
                break
            if self.grid.pattern in ["o", "outer"]:  # Rectangle only?
                if count + 1 > self.grid.rows * 2 + (self.grid.cols - 2) * 2:
                    break
            # ---- draw shapes
            if shapes:
                # ---- * extract shape data
                rotation = rotation_sequence.get(count + 1, 0)  # default rotation
                if isinstance(shapes[shape_id], BaseShape):
                    _shape = shapes[shape_id]
                elif isinstance(shapes[shape_id], tuple):
                    _shape = shapes[shape_id][0]
                    if not isinstance(_shape, BaseShape):
                        feedback(
                            f'The first item in "{shapes[shape_id]}" must be a shape!',
                            True,
                        )
                    if len(shapes[shape_id]) > 1:
                        rotation = tools.as_float(shapes[shape_id][1], "rotation")
                elif isinstance(shapes[shape_id], Place):
                    _shape = shapes[shape_id].shape
                    if not isinstance(_shape, BaseShape):
                        feedback(
                            f'The value for "{shapes[shape_id].name}" must be a shape!',
                            True,
                        )
                    if shapes[shape_id].rotation:
                        rotation = tools.as_float(shapes[shape_id].rotation, "rotation")
                else:
                    feedback(
                        f'Use a shape, or set, or Place - not "{shapes[shape_id]}"!',
                        True,
                    )
                # ---- * overwrite shape to use for corner
                if corners_dict:
                    if loc.corner in corners_dict.keys():
                        _shape = corners_dict[loc.corner]

                # ---- * set shape to enable overwrite/change of properties
                shape = copy(_shape)

                # ---- * execute shape.draw()
                cx = loc.x * shape.units + shape._o.delta_x
                cy = loc.y * shape.units + shape._o.delta_y
                locale = Locale(
                    col=loc.col,
                    row=loc.row,
                    x=loc.x,
                    y=loc.y,
                    xy=Point(loc.x, loc.y),
                    id=f"{loc.col}:{loc.row}",
                    label=f"{loc.col}:{loc.row}",
                    sequence=loc.sequence or count,
                    page=globals.page_count + 1,
                )
                _locale = locale._asdict()
                if self._draw_grid:
                    shape.draw(
                        _abs_cx=cx, _abs_cy=cy, rotation=rotation, locale=_locale
                    )
                shape_id += 1
            if shape_id > len(shapes) - 1:
                shape_id = 0  # reset and start again
            # ---- display debug
            if self.do_debug and self._draw_grid:
                match _lower(self.do_debug):
                    case "normal" | "none" | "null" | "n":
                        Dot(
                            x=loc.x,
                            y=loc.y,
                            stroke=globals.debug_color,
                            fill=globals.debug_color,
                        )
                    case "id" | "i":
                        Dot(
                            x=loc.x,
                            y=loc.y,
                            label=loc.id,
                            stroke=globals.debug_color,
                            fill=globals.debug_color,
                        )
                    case "sequence" | "s":
                        Dot(
                            x=loc.x,
                            y=loc.y,
                            label=f"{loc.sequence or count}",
                            stroke=globals.debug_color,
                            fill=globals.debug_color,
                        )
                    case "xy" | "xy":
                        Dot(
                            x=loc.x,
                            y=loc.y,
                            label=f"{round(loc.x, 2)},{round(loc.y, 2)}",
                            stroke=globals.debug_color,
                            fill=globals.debug_color,
                        )
                    case "yx" | "yx":
                        Dot(
                            x=loc.x,
                            y=loc.y,
                            label=f"{loc.y},{loc.x}",
                            stroke=globals.debug_color,
                            fill=globals.debug_color,
                        )
                    case "colrow" | "cr":
                        Dot(
                            x=loc.x,
                            y=loc.y,
                            label=f"{loc.col},{loc.row}",
                            stroke=globals.debug_color,
                            fill=globals.debug_color,
                        )
                    case "col" | "c":
                        Dot(
                            x=loc.x,
                            y=loc.y,
                            label=f"{loc.col}",
                            stroke=globals.debug_color,
                            fill=globals.debug_color,
                        )
                    case "row" | "r":
                        Dot(
                            x=loc.x,
                            y=loc.y,
                            label=f"{loc.row}",
                            stroke=globals.debug_color,
                            fill=globals.debug_color,
                        )
                    case "rowcol" | "rc":
                        Dot(
                            x=loc.x,
                            y=loc.y,
                            label=f"{loc.row},{loc.col}",
                            stroke=globals.debug_color,
                            fill=globals.debug_color,
                        )
                    case _:
                        feedback(f'Unknown debug style "{self.do_debug}"', True)


def Layout(grid, **kwargs):
    l_g = LayoutGrid(grid=grid, **kwargs)
    return l_g


def layout(grid, **kwargs):
    kwargs["_draw_grid"] = False
    l_g = LayoutGrid(grid=grid, **kwargs)
    return l_g
