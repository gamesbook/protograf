# -*- coding: utf-8 -*-
"""
protograf function for background blueprint-like grid
"""

# lib
from copy import copy
import math

# project
from protograf.utils import colrs, tools
from protograf.utils.messaging import feedback
from protograf.protos.proto_shapes import Common, Text
from protograf.layouts import (
    GridShape,
)
from protograf.utils.structures import (
    DirectionGroup,
)
from protograf.utils.constants import (
    # RGB_BLACK,
    RGB_WHITE,
    # CMYK_BLACK,
    CMYK_WHITE,
)

# local
from .utils import globals_set, validate_globals, margins


def Blueprint(**kwargs):
    """Draw a grid extending between page margins.

    Kwargs:

    - subdivisions (int): a number indicating how many lines should be drawn
      within each square; these are evenly spaces; use *subdivisions_dashed*
      to enhance these lines
    - style (str): set to one of: *blue*, *green* or *grey*
    - decimals (float): set to to an integer number for the decimal points
      which are used for the grid numbers (default is ``0``)
    - edges (str): can be set to any combination of *n*, *s*, *e*, or *w* in a
      single comma-delimited string; grid numbers will then be drawn on
      any of the edges specified
    - edges_y (float): the number set for this determines where a horizontal
      line of grid numbers will be drawn
    - edges_x (float): the number set for this determines where a vertical
      line of grid numbers will be drawn
    - numbering (bool): if True (default), will draw grid numbers on edges

    """

    def set_style(style_name):
        """Set Blueprint color and fill.

        Note:
            RGB to CMYK was done via https://colordesigner.io/convert/hextocmyk
        """
        match style_name:
            case "green":
                if globals.color_model == "CMYK":
                    color, fill = "0,0,78.6,19.2", "52.7,0,16.1,56.1"
                else:
                    color, fill = "#CECE2C", "#35705E"
            case "grey" | "gray":
                if globals.color_model == "CMYK":
                    color, fill = CMYK_WHITE, "0,6.8,3.1.38.9"
                else:
                    color, fill = RGB_WHITE, "#A1969C"
            case "blue" | "invert" | "inverted":
                if globals.color_model == "CMYK":
                    color, fill = "5.9,0,5.9,0", "72.1,22.7,0,32.6"
                else:
                    color, fill = "#F0FFF0", "#3085AC"
            case _:
                if globals.color_model == "CMYK":
                    color, fill = "72.1,22.7,0,32.6", None
                else:
                    color, fill = "#3085AC", None
                if style_name is not None:
                    feedback(
                        f'The Blueprint style "{style_name}" is unknown', False, True
                    )
        return color, fill

    def set_format(num, side):
        return f"{num*side:{1}.{decimals}f}"

    kwargs = margins(**kwargs)
    if kwargs.get("common"):
        feedback('The "common" property cannot be used with a Blueprint.', True)
    kwargs["units"] = kwargs.get("units", globals.units)
    side = 1.0
    decimals = tools.as_int(kwargs.get("decimals", 0), "Blueprint decimals")
    # override defaults ... otherwise grid not "next" to margins
    numbering = kwargs.get("numbering", True)
    kwargs["side"] = kwargs.get("side", side)
    number_edges = kwargs.get("edges", "S,W")
    kwargs["x"] = kwargs.get("x", 0)
    kwargs["y"] = kwargs.get("y", 0)
    m_x = kwargs["units"] * (globals.margins.left + globals.margins.right)
    m_y = kwargs["units"] * (globals.margins.top + globals.margins.bottom)
    _cols = (globals.page.size[0] - m_x) / (kwargs["units"] * float(kwargs["side"]))
    _rows = (globals.page.size[1] - m_y) / (kwargs["units"] * float(kwargs["side"]))
    rows = int(_rows)
    cols = int(_cols)
    kwargs["rows"] = kwargs.get("rows", rows)
    kwargs["cols"] = kwargs.get("cols", cols)
    kwargs["stroke_width"] = kwargs.get("stroke_width", 0.2)  # fine line
    default_font_size = (
        10 * math.sqrt(globals.page.size[0]) / math.sqrt(globals.page.size[1])
    )
    dotted = kwargs.get("dotted", False)
    kwargs["font_size"] = kwargs.get("font_size", default_font_size)
    line_stroke, page_fill = set_style(kwargs.get("style", None))
    kwargs["stroke"] = kwargs.get("stroke", line_stroke)
    kwargs["fill"] = kwargs.get("fill", page_fill)
    # ---- page color (optional)
    if kwargs["fill"] is not None:
        fill = colrs.get_color(kwargs.get("fill", RGB_WHITE))
        globals.canvas.draw_rect((0, 0, globals.page.size[0], globals.page.size[1]))
        globals.canvas.finish(fill=fill, lineJoin=0)
    kwargs["fill"] = kwargs.get("fill", line_stroke)  # revert back for font
    # ---- number edges
    if number_edges:
        edges = tools.validated_directions(
            number_edges, DirectionGroup.CARDINAL, "blueprint edges"
        )
    else:
        edges = []
    # ---- numbering
    if numbering:
        _common = Common(
            font_size=kwargs["font_size"],
            stroke=kwargs["stroke"],
            fill=kwargs["stroke"],
            units=kwargs["units"],
        )
        offset = _common.points_to_value(kwargs["font_size"]) / 2.0
        offset_edge = _common.points_to_value(kwargs["font_size"]) * 1.25
        # ---- * absolute?
        fixed_y, fixed_x = None, None
        edges_x = kwargs.get("edges_x", None)
        if edges_x:
            fixed_x = tools.as_float(edges_x, "edges_x")
        edges_y = kwargs.get("edges_y", None)
        if edges_y:
            fixed_y = tools.as_float(edges_y, "edges_y")
        if fixed_x:
            for y in range(1, kwargs["rows"] + 1):
                Text(
                    x=fixed_x,
                    y=y * side + offset,
                    text=set_format(y, side),
                    common=_common,
                )
        if fixed_y:
            for x in range(1, kwargs["cols"] + 1):
                Text(
                    x=x * side,
                    y=fixed_y + offset,
                    text=set_format(x, side),
                    common=_common,
                )

        # ---- * relative
        if "n" in edges:
            for x in range(1, kwargs["cols"] + 1):
                Text(
                    x=x * side,
                    y=kwargs["y"] - offset,
                    text=set_format(x, side),
                    common=_common,
                )
        if "s" in edges:
            for x in range(1, kwargs["cols"] + 1):
                Text(
                    x=x * side,
                    y=kwargs["y"] + kwargs["rows"] * side + offset_edge,
                    text=set_format(x, side),
                    common=_common,
                )
        if "e" in edges:
            for y in range(1, kwargs["rows"] + 1):
                Text(
                    x=kwargs["x"] + kwargs["cols"] * side + globals.margins.left / 2.0,
                    y=y * side + offset,
                    text=set_format(y, side),
                    common=_common,
                )
        if "w" in edges:
            for y in range(1, kwargs["rows"] + 1):
                Text(
                    x=kwargs["x"] - globals.margins.left / 2.0,
                    y=y * side + offset,
                    text=set_format(y, side),
                    common=_common,
                )
        # ---- draw "zero" number
        # z_x = kwargs["units"] * globals.margins.left
        # z_y = kwargs["units"] * globals.margins.bottom
        # crner_dist = geoms.length_of_line(Point(0, 0), Point(z_x, z_y))
        # crner_frac = crner_dist * 0.66 / kwargs["units"]
        # # feedback(f'$$$  {z_x=} {z_y=} {crner_dist=}')
        # zero_pt = geoms.point_on_line(Point(0, 0), Point(z_x, z_y), crner_frac)
        # Text(
        #     x=zero_pt.x / kwargs["units"] - kwargs["side"] / 4.0,
        #     y=zero_pt.y / kwargs["units"] - kwargs["side"] / 4.0,
        #     text="0",
        #     common=_common,
        # )

    # ---- draw subgrid
    if kwargs.get("subdivisions"):
        local_kwargs = copy(kwargs)
        sub_count = int(kwargs.get("subdivisions"))
        local_kwargs["side"] = float(side / sub_count)
        local_kwargs["rows"] = sub_count * kwargs["rows"]
        local_kwargs["cols"] = sub_count * kwargs["cols"]
        local_kwargs["stroke_width"] = kwargs.get("stroke_width") / 2.0
        local_kwargs["stroke"] = kwargs.get("subdivisions_stroke", kwargs["stroke"])
        local_kwargs["dashed"] = kwargs.get("subdivisions_dashed", None)
        local_kwargs["dotted"] = kwargs.get("subdivisions_dotted", True)
        if local_kwargs["dashed"]:
            local_kwargs["dotted"] = False
        subgrid = GridShape(canvas=globals.canvas, **local_kwargs)
        subgrid.draw(cnv=globals.canvas)

    # ---- draw Blueprint grid
    grid = GridShape(
        canvas=globals.canvas, dotted=dotted, **kwargs
    )  # don't add canvas as arg here!
    grid.draw(cnv=globals.canvas)
    return grid
