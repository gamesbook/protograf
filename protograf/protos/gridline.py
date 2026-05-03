# -*- coding: utf-8 -*-
"""
protograf function for drawing lines on a grid
"""

# lib

# third party
from typing import Union

# module
from protograf import globals
from protograf.proto import base_shape, line, arc
from protograf.utils import tools, geoms  # , support
from protograf.utils.messaging import feedback
from protograf.utils.tools import _lower
from protograf.utils.structures import (
    DirectionGroup,
    HEX_FLAT_EDGE_TRAVEL,
    HexOrientation,
    Locale,
    Point,
)

# local
from .hexagons import Hexagons


def GridLine(
    grid: list,
    start: str = "",
    point: str = "",
    locations: Union[list, str] | None = None,
    edges: Union[list, str] | None = None,
    paths: Union[list, str] | None = None,
    **kwargs,
):
    """Enable drawing Line or Lines between one or more points in a grid.

    Args:
        grid: list of Locales (from Hexagons)
        start: the ID for a hexagon in the list of Locales
        point: a named compass point for a Locale (valid for a Hexagon)
        locations: one or more hexagon IDs to join with lines (centre-to-centre)
        edges: one or more directions in which to draw lines (vertex-to-vertex)
        paths: one or more directions in which to draw curved lines (perbis-to-perbis)
    """

    def draw_linked_locations(grid, locations, **kwargs):
        """Draw lines between points inside hexagons in grid."""
        dummy = base_shape()  # a BaseShape - not drawable!
        for index, location in enumerate(locations):
            # precheck
            if isinstance(location, str):
                location = (location, 0, 0)  # reformat into standard notation
            if not isinstance(location, tuple) or len(location) != 3:
                feedback(
                    f"The location '{location}' is not valid -- please check its syntax!",
                    True,
                )
            # get location centre from grid via the label
            loc = None
            try:
                iter(grid)
            except TypeError:
                feedback(f"The grid '{grid}' is not valid - please check it!", True)
            for position in grid:
                if not isinstance(position, Locale):
                    feedback(f"The grid '{grid}' is not valid - please check it!", True)
                if location[0] == position.label:
                    loc = Point(position.x, position.y)
                    break
            if loc is None:
                feedback(f"The location '{location[0]}' is not in the grid!", True)
            # new line?
            if index + 1 < len(locations):
                # location #2
                location_2 = locations[index + 1]
                if isinstance(location_2, str):
                    location_2 = (location_2, 0, 0)  # reformat into standard notation
                if not isinstance(location_2, tuple) or len(location_2) != 3:
                    feedback(
                        f"The location '{location_2}' is not valid - please check its syntax!",
                        True,
                    )
                loc_2 = None
                for position in grid:
                    if location_2[0] == position.label:
                        loc_2 = Point(position.x, position.y)
                        break
                if loc_2 is None:
                    feedback(
                        f"The location '{location_2[0]}' is not in the grid!", True
                    )
                if location == location_2:
                    feedback(
                        "Locations must differ from each other - "
                        f"({location} matches {location_2})!",
                        True,
                    )
                # line start/end
                x = dummy.points_to_value(loc.x) + location[1]
                y = dummy.points_to_value(loc.y) + location[2]
                x1 = dummy.points_to_value(loc_2.x) + location_2[1]
                y1 = dummy.points_to_value(loc_2.y) + location_2[2]

                _line = line(x=x, y=y, x1=x1, y1=y1, **kwargs)
                # feedback(f"$$$ {x=}, {y=}, {x1=}, {y1=}")
                delta_x = globals.margins.left
                delta_y = globals.margins.top
                # feedback(f"$$$ {delta_x=}, {delta_y=}")
                _line.draw(
                    off_x=-delta_x,
                    off_y=-delta_y,
                )

    def draw_edges(start: str, vertex: str, edges: list, **kwargs):
        """Draw lines along edges of hexagons in grid."""
        starts = (
            [
                start,
            ]
            if isinstance(start, str)
            else start
        )  # must be a list!
        for start in starts:
            loc = grid.cell(start)
            current_vertex = vertex
            _line = None
            for edge_direction in edges:
                direction = _lower(edge_direction)
                # print('>>>', loc.label, loc.col, loc.row, current_vertex, direction)
                outcome = HEX_FLAT_EDGE_TRAVEL.get((current_vertex, direction))
                if not outcome:
                    feedback(
                        f'It is not possible to travel "{edge_direction}" from'
                        f' a "{current_vertex}" vertex on this hexgrid.',
                        True,
                    )

                # calculate col/row changes for FLAT
                col, row = 0, 0

                if (
                    direction == "e"
                    and current_vertex == "e"
                    or direction == "ne"
                    and current_vertex == "ne"
                    or direction == "se"
                    and current_vertex == "se"
                ):
                    col = 1
                if (
                    direction == "w"
                    and current_vertex == "w"
                    or direction == "nw"
                    and current_vertex == "nw"
                    or direction == "sw"
                    and current_vertex == "sw"
                ):
                    col = -1
                if (
                    direction == "ne"
                    and current_vertex == "ne"
                    or direction == "nw"
                    and current_vertex == "nw"
                    or direction == "w"
                    and current_vertex == "w"
                ):
                    row = -1 if loc.col % 2 == 0 else 0  # even column 0,2,4
                if (
                    direction == "se"
                    and current_vertex == "se"
                    or direction == "sw"
                    and current_vertex == "sw"
                    or direction == "e"
                    and current_vertex == "e"
                ):
                    row = 1 if loc.col % 2 == 1 else 0  # odd column 1,3,5

                col = loc.col + col
                row = loc.row + row
                next_loc = grid.cell(
                    (col, row)
                )  # get_starting_location("", col=col, row=row)
                next_vertex = outcome.end
                # print(f'>>> next edge col/row >>> {col=} {row=} {next_loc=}')

                # line settings
                _line = line(
                    xy=getattr(loc.geo, current_vertex),
                    xy1=getattr(next_loc.geo, next_vertex),
                    **kwargs,
                )
                _line.draw()
                # prep for next iteration
                loc = next_loc
                current_vertex = next_vertex

    def draw_arc(centre: Point, start: Point, angle_width: float, **kwargs):
        radius = geoms.length_of_line(start, centre)
        _, rotate = geoms.angles_from_points(centre, start)
        angle_start = rotate
        if kwargs.get("invert"):
            angle_start = 360 - angle_start
        # print(f'$$$ GridLine arc {centre=} {radius=} {angle_start=} {angle_width=}')
        aarc = arc(
            cxy=centre,
            radius=radius,
            angle_start=angle_start,
            angle_width=angle_width,
            fullSector=False,
            **kwargs,
        )
        aarc.draw()

    def draw_path_lines(
        pair: str,
        perbii: dict,
        vertices: dict,
        centre: Point,
        offset: dict,
        orientation: HexOrientation = HexOrientation.FLAT,
        **kwargs,
    ):
        """Draw arc or line between centre of edges, or centre, of a hexagon."""
        if orientation == HexOrientation.FLAT:
            match pair:
                # 120 degrees / short arc
                case ["n", "ne"] | ["ne", "n"]:
                    draw_arc(vertices["ne"], perbii["n"], 120.0, **kwargs)  # p5 OK
                case ["se", "ne"] | ["ne", "se"]:
                    draw_arc(vertices["e"], perbii["ne"], -120.0, **kwargs)  # p4 OK
                case ["se", "s"] | ["s", "se"]:
                    draw_arc(vertices["se"], perbii["s"], -120.0, **kwargs)  # p3 OK
                case ["sw", "s"] | ["s", "sw"]:
                    draw_arc(vertices["sw"], perbii["s"], 120.0, **kwargs)  # p2 OK
                case ["sw", "nw"] | ["nw", "sw"]:
                    draw_arc(vertices["w"], perbii["sw"], -120.0, **kwargs)  # p1 OK
                case ["n", "nw"] | ["nw", "n"]:
                    draw_arc(vertices["nw"], perbii["n"], -120.0, **kwargs)  # p0 OK
                # 60 degrees / long arc
                case ["n", "se"] | ["se", "n"]:
                    draw_arc(offset["NE"], perbii["n"], 60.0, **kwargs)  # p5
                case ["ne", "s"] | ["s", "ne"]:
                    draw_arc(
                        offset["SE"], perbii["ne"], 60.0, invert=True, **kwargs
                    )  # p4
                case ["se", "sw"] | ["sw", "se"]:
                    draw_arc(
                        offset["S"], perbii["se"], 60.0, invert=True, **kwargs
                    )  # p3
                case ["s", "nw"] | ["nw", "s"]:
                    draw_arc(offset["SW"], perbii["s"], 60.0, **kwargs)  # p2
                case ["sw", "n"] | ["n", "sw"]:
                    draw_arc(
                        offset["NW"], perbii["sw"], 60.0, invert=True, **kwargs
                    )  # p1
                case ["nw", "ne"] | ["ne", "nw"]:
                    draw_arc(
                        offset["N"], perbii["nw"], 60.0, invert=True, **kwargs
                    )  # p0
                # 90 degrees / straight line
                case (
                    ["nw", "se"]
                    | ["se", "nw"]
                    | ["ne", "sw"]
                    | ["sw", "ne"]
                    | ["n", "s"]
                    | ["s", "n"]
                ):
                    _line = line(
                        xy=perbii[pair[0]],
                        xy1=perbii[pair[1]],
                        **kwargs,
                    )
                    _line.draw()
                # straight line TO centre
                case (
                    ["nw", "c"]
                    | ["se", "c"]
                    | ["ne", "c"]
                    | ["sw", "c"]
                    | ["n", "c"]
                    | ["s", "c"]
                ):
                    _line = line(
                        xy=perbii[pair[0]],
                        xy1=centre,
                        **kwargs,
                    )
                    _line.draw()
                # straight line FROM centre
                case (
                    ["c", "nw"]
                    | ["c", "se"]
                    | ["c", "ne"]
                    | ["c", "sw"]
                    | ["c", "n"]
                    | ["c", "s"]
                ):
                    _line = line(
                        xy=centre,
                        xy1=perbii[pair[1]],
                        **kwargs,
                    )
                    _line.draw()
                case ["c", "c"]:
                    feedback(
                        "Unable to draw lines between two centres of hexagons grid.",
                        True,
                    )
                case _:
                    pass

        elif orientation == HexOrientation.POINTY:
            feedback(
                f'Unable to calculate lines for "{orientation}" orientation for hexagons grid.',
                True,
            )
        else:
            feedback(f'Invalid orientation "{orientation}" supplied for hexagon.', True)

    def draw_paths(start: str, perbis: str, directions: list, **kwargs):
        """Draw curved/straight lines between edges of hexagons in grid."""
        # print(f'~~~ GridLine draw_paths() {start=} {directions=}')
        loc = grid.cell(start)  # get_starting_location(start)
        from_edge = perbis
        to_edge = directions[0]
        for index in range(0, len(directions)):
            # ---- perbii // FLAT hex
            perbii = {
                "n": loc.geo.n,
                "ne": loc.geo.ene,
                "se": loc.geo.ese,
                "s": loc.geo.s,
                "sw": loc.geo.wsw,
                "nw": loc.geo.wnw,
            }
            # ---- vertices // FLAT hex
            #     nw 0__5 ne
            #     w 1/  \4 e
            #        \__/
            #     sw 2  3 se
            vertices = {
                "nw": loc.geo.nw,
                "w": loc.geo.w,
                "sw": loc.geo.sw,
                "se": loc.geo.se,
                "e": loc.geo.e,
                "ne": loc.geo.ne,
            }
            # ---- calculate offset centres  // FLAT hex
            side_plus = loc.geo.side * 1.5
            h_flat = loc.geo.height / 2.0
            height_flat = loc.geo.height
            centre = loc.geo.centre
            #      A
            #     ___
            #  F / . \ B
            #  E \___/ C
            #      D
            offsets = {
                "N": Point(centre.x, centre.y - height_flat),
                "NE": Point(centre.x + side_plus, centre.y - h_flat),
                "SE": Point(centre.x + side_plus, centre.y + h_flat),
                "S": Point(centre.x, centre.y + height_flat),
                "SW": Point(centre.x - side_plus, centre.y + h_flat),
                "NW": Point(centre.x - side_plus, centre.y - h_flat),
            }
            # ---- draw lines
            draw_path_lines(
                [from_edge, to_edge], perbii, vertices, centre, offsets, **kwargs
            )
            # ---- set next location
            if index + 1 == len(directions):
                continue
            col, row = 0, 0
            if to_edge in ["se", "ne"]:
                col = 1
            if to_edge in ["nw", "sw"]:
                col = -1
            if to_edge in ["nw", "ne"]:
                row = -1 if loc.col % 2 == 0 else 0  # even column 0,2,4
            if to_edge in ["sw", "se"]:
                row = 1 if loc.col % 2 == 1 else 0  # odd column 1,3,5
            if to_edge in ["n"]:
                row = -1
            if to_edge in ["s"]:
                row = 1
            col = loc.col + col
            row = loc.row + row
            loc = grid.cell((col, row))  # get_starting_location("", col=col, row=row)
            # ---- set next pair of directions
            match directions[index]:
                case "ne":
                    from_edge = "sw"
                case "se":
                    from_edge = "nw"
                case "n":
                    from_edge = "s"
                case "s":
                    from_edge = "n"
                case "nw":
                    from_edge = "se"
                case "sw":
                    from_edge = "ne"
            to_edge = directions[index + 1] if index < (len(directions) - 1) else None

    # ---- validation
    if locations is not None:
        if isinstance(locations, str):  # should be a comma-delimited string
            locations = tools.sequence_split(locations, to_int=False, unique=False)
        if not isinstance(locations, list):
            feedback(
                f"GridLine locations '{locations}' is not a list - please check!", True
            )
        if locations and len(locations) < 2:
            feedback("There should be at least 2 locations to create links!", True)
        if isinstance(grid, Hexagons):
            grid = grid.locales
        draw_linked_locations(grid, locations, **kwargs)

    if edges is not None:
        if edges and not point:
            feedback("There must be an initial point (vertex) to draw edges!", True)
        if not _lower(point) in tools.valid_directions(DirectionGroup.HEX_FLAT):
            feedback(f'The point "{point}" is not valid for this hexagons grid.', True)
        if isinstance(edges, str):  # comma-delimited string for multi-edge
            if edges == "*" or _lower(edges) == "all":
                loop = {
                    "ne": ["se", "sw", "w", "nw", "ne", "e"],
                    "e": ["sw", "w", "nw", "ne", "e", "se"],
                    "se": ["w", "nw", "ne", "e", "se", "sw"],
                    "sw": ["nw", "ne", "e", "se", "sw", "w"],
                    "w": ["ne", "e", "se", "sw", "w", "nw"],
                    "nw": ["e", "se", "sw", "w", "nw", "ne"],
                }
                edges = loop.get(_lower(point))
            else:
                edges = tools.sequence_split(
                    edges, to_int=False, unique=False, no_blanks=True
                )
        if not isinstance(edges, list):
            feedback(f"GridLine edges '{edges}' is not a list - please check!", True)
        if edges and not start:
            feedback("There must be a start (hexagon location) to draw edges!", True)
        draw_edges(start, _lower(point), edges, **kwargs)

    if paths is not None:
        if paths and not point:
            feedback("There must be an initial point (on an edge) to draw paths!", True)
        if (
            not _lower(point) in tools.valid_directions(DirectionGroup.HEX_POINTY)
            and _lower(point) != "c"
        ):
            feedback(f'The point "{point}" is not valid for this hexagons grid.', True)
        if isinstance(paths, str):  # should be a comma-delimited string
            paths = tools.sequence_split(paths, to_int=False, unique=False)
        if not isinstance(paths, list):
            feedback(f"GridLine paths '{paths}' is not a list - please check!", True)
        if paths and not start:
            feedback("There must be a start (hexagon location) to draw paths!", True)
        draw_paths(start, point, paths, **kwargs)

    if locations is None and edges is None and paths is None:
        feedback(
            "Set a value for location, or edges, or paths to draw a GridLine!", True
        )
