# -*- coding: utf-8 -*-
"""
protograf function for layout of Location on a grid
"""

# lib
from typing import Union, Any

# module
from protograf.shapes import BaseShape

# from protograf.utils import tools, geoms, support
from protograf.utils.messaging import feedback
from protograf.utils.tools import _lower
from protograf.utils.structures import (
    # HEX_FLAT_EDGE_TRAVEL,
    # HexOrientation,
    Locale,
    Point,
)
from protograf.utils.constants import (
    GRID_SHAPES_WITH_CENTRE,
    GRID_SHAPES_NO_CENTRE,
)
from .hexagons import Hexagons


def Location(grid: list, label: str, shapes: list, **kwargs):
    kwargs = kwargs

    def test_foo(x: bool = True, **kwargs):
        print("--- test only ---", kwargs)

    def draw_shape(shape: BaseShape, point: Point, locale: Locale):
        shape_name = shape.__class__.__name__
        shape_abbr = shape_name.replace("Shape", "")
        # shape._debug(cnv.canvas, point=loc)
        dx = shape.kwargs.get("dx", 0)  # user-units
        dy = shape.kwargs.get("dy", 0)  # user-units
        pts = shape.values_to_points([dx, dy])  # absolute units (points)
        try:
            x = point.x + pts[0]
            y = point.y + pts[1]
            kwargs["locale"] = locale
            # feedback(f"$$$ {shape=} :: {loc.x=}, {loc.y=} // {dx=}, {dy=}")
            # feedback(f"$$$ {kwargs=}")
            # feedback(f"$$$ Loc {label} :: {shape_name=}")
            if shape_name in GRID_SHAPES_WITH_CENTRE:
                shape.draw(_abs_cx=x, _abs_cy=y, **kwargs)
            elif shape_name in GRID_SHAPES_NO_CENTRE:
                shape.draw(_abs_x=x, _abs_y=y, **kwargs)
            else:
                feedback(f"Unable to draw {shape_abbr}s in Location!", True)
        except Exception as err:
            feedback(err, False)
            feedback(
                f"Unable to draw the '{shape_abbr}' - please check its settings!", True
            )

    # checks
    if isinstance(grid, Hexagons):
        grid = grid.locales
    if grid is None or not isinstance(grid, list):
        feedback("The grid (as a list) must be supplied!", True)

    # get location centre from grid via the label
    locale, point = None, None
    for _locale in grid:
        if _lower(_locale.label) == _lower(label):
            point = Point(_locale.x, _locale.y)
            locale = _locale
            break
    if point is None:
        msg = ""
        if label and "," in label:
            msg = " (Did you mean to use Locations?)"
        feedback(f"The Location '{label}' is not in the grid!{msg}", True)

    if shapes:
        try:
            iter(shapes)
        except TypeError:
            feedback("The Location shapes property must contain a list!", True)
        for shape in shapes:
            if shape.__class__.__name__ == "GroupBase":
                feedback(f"Group drawing ({shape}) NOT IMPLEMENTED YET", True)
            else:
                draw_shape(shape, point, locale)


def Locations(grid: list, labels: Union[str, list], shapes: list, **kwargs):
    kwargs = kwargs

    if isinstance(grid, Hexagons):
        grid = grid.locales
    if grid is None or not isinstance(grid, list):
        feedback("The grid (as a list) must be supplied!", True)
    if labels is None:
        feedback("No grid location labels supplied!", True)
    if shapes is None:
        feedback("No list of shapes supplied!", True)
    if isinstance(labels, str):
        _labels = [_label.strip() for _label in labels.split(",")]
        if _lower(labels) == "all" or _lower(labels) == "*":
            _labels = []
            for loc in grid:
                if isinstance(loc, Locale):
                    _labels.append(loc.label)
    elif isinstance(labels, list):
        _labels = labels
    else:
        feedback(
            "Grid location labels must be a list or a comma-delimited string!", True
        )

    if not isinstance(shapes, list):
        feedback("Shapes must contain a list of shapes!", True)

    for label in _labels:
        # feedback(f'### Locations {label=} :: {shapes=}')
        Location(grid, label, shapes)
