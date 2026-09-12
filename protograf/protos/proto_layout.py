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


def Layout(grid, **kwargs):
    """Draw shape(s) in locations, cols, & rows in a virtual layout"""
    from protograf.shapes.virtuals import VirtualLocations

    utils.validate_globals()

    grid_classname = grid.__class__.__name__ if grid else ""
    kwargs = kwargs
    shapes = kwargs.get("shapes", [])  # shapes or Places
    locations = kwargs.get("locations", [])
    location_rows = kwargs.get("rows", [])
    location_cols = kwargs.get("cols", [])
    corners = kwargs.get("corners", [])  # shapes or Places for corners only!
    rotations = kwargs.get("rotations", [])  # rotations for an edge
    if kwargs.get("masked") and isinstance(kwargs.get("masked"), str):
        masked = tools.sequence_split(kwargs.get("masked"), "masked")
    else:
        masked = kwargs.get("masked", [])
    if kwargs.get("visible") and isinstance(kwargs.get("visible"), str):
        visible = tools.integer_pairs(kwargs.get("visible"), "visible")
    else:
        visible = kwargs.get("visible", [])
    # ---- grid
    layout_grid = kwargs.get("gridlines", None)  # directions ...
    _grid_stroke = kwargs.get("gridlines_stroke", globals.black)
    layout_grid_ends = kwargs.get("gridlines_ends", None)
    layout_grid_fill = kwargs.get("gridlines_fill", None)
    layout_grid_stroke = colrs.get_color(_grid_stroke)
    layout_grid_stroke_width = kwargs.get("gridlines_stroke_width", WIDTH)
    layout_grid_dotted = kwargs.get("gridlines_dotted", False)
    layout_grid_dashed = kwargs.get("gridlines_dashed", None)
    layout_grid_transparency = kwargs.get("gridlines_transparency", None)

    # ---- validate inputs
    if not shapes:
        feedback(f"There is no list of {grid_classname} shapes to draw!", False, True)
    if shapes and not isinstance(shapes, list):
        feedback(f"The values for {grid_classname} 'shapes' must be in a list!", True)
    if not isinstance(grid, VirtualLocations):
        feedback(f"The grid type '{grid_classname} ' is not valid!", True)
    corners_dict = {}
    if corners:
        if not isinstance(corners, list):
            feedback(
                f"The {grid_classname} corners value '{corners}' is not a valid list!",
                True,
            )
        for corner in corners:
            try:
                value = corner[0]
                shape = corner[1]
                if _lower(value) not in ["nw", "ne", "sw", "se", "*"]:
                    feedback(
                        f'The {grid_classname} corner must be one of nw, ne, sw, se (not "{
                            value}")!',
                        True,
                    )
                if not isinstance(shape, BaseShape):
                    feedback(
                        f'The {grid_classname} corner item must be a shape (not "{
                            shape}") !',
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
                    f'The {grid_classname} corners setting "{
                        corner}" is not a valid list',
                    True,
                )

    # ---- draw grid (using a Shape)
    if layout_grid:
        layout_grid_centroid = grid.grid_centroid  # calculated in layouts
        match grid_classname:
            case "DiamondLocations":
                # ---- get gridlines params
                layout_grid_dirs = tools.validated_gridlines(
                    layout_grid, DirectionGroup.COMPASS, "gridlines"
                )
                layout_grid_hatches = grid.cols // 2 - 1  # for Diamond, rows == cols
                # ---- setup gridlines configuration # eg.  [('d', 10), ('ne', 10)]
                gridlines_count = {
                    "n": grid.cols // 2,
                    "s": grid.cols // 2,
                    "e": grid.rows // 2,
                    "w": grid.rows // 2,
                    "ne": grid.cols // 2 - 1,
                    "nw": grid.cols // 2 - 1,
                    "se": grid.rows // 2 - 1,
                    "sw": grid.rows // 2 - 1,
                }
                gridlines_config = [
                    (_dir, gridlines_count[_dir]) for _dir in layout_grid_dirs
                ]
                # ---- draw lines
                Rhombus(
                    cx=layout_grid_centroid.x,
                    cy=layout_grid_centroid.y,
                    height=grid.total_height,
                    width=grid.total_width,
                    stroke=layout_grid_stroke,
                    stroke_width=layout_grid_stroke_width,
                    stroke_ends=layout_grid_ends,
                    dotted=layout_grid_dotted,
                    dashed=layout_grid_dashed,
                    fill=layout_grid_fill,
                    transparency=layout_grid_transparency,
                    hatches_count=layout_grid_hatches,
                    hatches=gridlines_config,
                    hatches_stroke=layout_grid_stroke,
                    hatches_stroke_width=layout_grid_stroke_width,
                    hatches_ends=layout_grid_ends,
                    hatches_dotted=layout_grid_dotted,
                    hatches_dashed=layout_grid_dashed,
                    # rotation=0,
                )
            case "RectangularLocations":
                # ---- get gridlines params
                layout_grid_dirs = tools.validated_gridlines(
                    layout_grid, DirectionGroup.COMPASS, "gridlines"
                )
                # ---- NO diags for unequal rows & cols:
                if grid.cols != grid.rows:
                    with suppress(ValueError):
                        layout_grid_dirs.remove("ne")
                    with suppress(ValueError):
                        layout_grid_dirs.remove("nw")
                    with suppress(ValueError):
                        layout_grid_dirs.remove("se")
                    with suppress(ValueError):
                        layout_grid_dirs.remove("sw")
                    with suppress(ValueError):
                        layout_grid_dirs.remove("d")
                layout_grid_hatches = grid.cols
                # ---- setup gridlines configuration
                gridlines_config = layout_grid  # eg. '*', 'd', 'ne' etc. or [('d', 10)]
                gridlines_count = {
                    "n": grid.cols // 2,
                    "s": grid.cols // 2,
                    "e": grid.rows // 2 + 1,
                    "w": grid.rows // 2 + 1,
                    "ne": grid.cols + 1,
                    "nw": grid.cols + 1,
                    "se": grid.rows + 1,
                    "sw": grid.rows + 1,
                }
                gridlines_config = [
                    (_dir, gridlines_count[_dir]) for _dir in layout_grid_dirs
                ]
                # ---- draw lines
                Rectangle(
                    cx=layout_grid_centroid.x,
                    cy=layout_grid_centroid.y,
                    height=grid.total_height,
                    width=grid.total_width,
                    stroke=layout_grid_stroke,
                    stroke_width=layout_grid_stroke_width,
                    stroke_ends=layout_grid_ends,
                    dotted=layout_grid_dotted,
                    dashed=layout_grid_dashed,
                    fill=layout_grid_fill,
                    transparency=layout_grid_transparency,
                    hatches_count=layout_grid_hatches,
                    hatches=gridlines_config,
                    hatches_stroke=layout_grid_stroke,
                    hatches_stroke_width=layout_grid_stroke_width,
                    hatches_ends=layout_grid_ends,
                    hatches_dotted=layout_grid_dotted,
                    hatches_dashed=layout_grid_dashed,
                    # rotation=rotation,
                )
            case "TriangularLocations":
                # ---- get gridlines params
                layout_grid_dirs = tools.validated_gridlines(
                    layout_grid, DirectionGroup.TRIANGULAR_HATCH, "gridlines"
                )
                layout_grid_hatches = grid.cols // 2 - 1  # for Diamond, rows == cols
                # ---- setup gridlines configuration # eg.  [('d', 10), ('ne', 10)]
                match grid.facing:
                    case "north" | "south":
                        gridlines_count = {
                            "e": grid.rows * 2,
                            "w": grid.rows * 2,
                            "ne": grid.cols // 2 + 1,
                            "nw": grid.cols // 2 + 1,
                            "se": grid.cols // 2 + 1,
                            "sw": grid.cols // 2 + 1,
                        }
                    case "east" | "west":
                        gridlines_count = {
                            "e": grid.cols * 2,
                            "w": grid.cols * 2,
                            "ne": grid.rows // 2 + 1,
                            "nw": grid.rows // 2 + 1,
                            "se": grid.rows // 2 + 1,
                            "sw": grid.rows // 2 + 1,
                        }
                gridlines_config = [
                    (_dir, gridlines_count[_dir]) for _dir in layout_grid_dirs
                ]
                match grid.facing:
                    case "south":
                        rotation = 180
                    case "east":
                        rotation = 30
                    case "west":
                        rotation = -30
                    case _:
                        rotation = 0
                # ---- draw lines
                Triangle(
                    cx=layout_grid_centroid.x,
                    cy=layout_grid_centroid.y,
                    # height=grid.total_height,
                    side=grid.total_width,
                    stroke=layout_grid_stroke,
                    stroke_width=layout_grid_stroke_width,
                    stroke_ends=layout_grid_ends,
                    dotted=layout_grid_dotted,
                    dashed=layout_grid_dashed,
                    fill=layout_grid_fill,
                    transparency=layout_grid_transparency,
                    hatches_count=layout_grid_hatches,
                    hatches=gridlines_config,
                    hatches_stroke=layout_grid_stroke,
                    hatches_stroke_width=layout_grid_stroke_width,
                    hatches_ends=layout_grid_ends,
                    hatches_dotted=layout_grid_dotted,
                    hatches_dashed=layout_grid_dashed,
                    rotation=rotation,
                )
            case _:
                feedback(
                    f"The grid type '{grid_classname}' does not support gridlines!",
                    True,
                )

    # ---- setup locations; automatically or via user-specification
    shape_id = 0
    _default_locations = enumerate(grid.next_locale())
    default_locations = [*_default_locations]
    if not locations and not location_rows and not location_cols:
        _locations = default_locations
    else:
        _locations = []
        user_locations = tools.integer_pairs(locations, label="locations")
        user_location_rows = tools.sequence_split(
            location_rows, to_int=True, unique=True, msg="rows"
        )
        user_location_cols = tools.sequence_split(
            location_cols, to_int=True, unique=True, msg="col"
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
            default_locations = enumerate(grid.next_locale())  # regenerate !

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
            default_locations = enumerate(grid.next_locale())  # regenerate !

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
            default_locations = enumerate(grid.next_locale())  # regenerate !

    # ---- generate rotations - keyed per sequence number
    rotation_sequence = {}
    if rotations:
        for rotation in rotations:
            if not isinstance(rotation, tuple):
                feedback("The 'rotations' must each contain a set!", True)
            if len(rotation) != 2:
                feedback("The 'rotations' must each contain a set of two items!", True)
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

    # ---- iterate through locations & draw shape(s)
    for count, loc in _locations:
        # print("395: time to draw locs:", count, loc)
        if masked and count + 1 in masked:  # ignore if IN masked
            continue
        if visible and count + 1 not in visible:  # ignore if NOT in visible
            continue
        if grid.stop and count + 1 >= grid.stop:
            break
        if grid.pattern in ["o", "outer"]:  # Rectangle only?
            if count + 1 > grid.rows * 2 + (grid.cols - 2) * 2:
                break
        if shapes:
            # ---- * extract shape data
            rotation = rotation_sequence.get(count + 1, 0)  # default rotation
            if isinstance(shapes[shape_id], BaseShape):
                _shape = shapes[shape_id]
            elif isinstance(shapes[shape_id], tuple):
                _shape = shapes[shape_id][0]
                if not isinstance(_shape, BaseShape):
                    feedback(
                        f'The first item in "{shapes[shape_id]}" must be a shape!', True
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
                    f'Use a shape, or set, or Place - not "{shapes[shape_id]}"!', True
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
            shape.draw(_abs_cx=cx, _abs_cy=cy, rotation=rotation, locale=_locale)
            shape_id += 1
        if shape_id > len(shapes) - 1:
            shape_id = 0  # reset and start again
        # ---- display debug
        do_debug = kwargs.get("debug", None)
        if do_debug:
            match _lower(do_debug):
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
                    feedback(f'Unknown debug style "{do_debug}"', True)
