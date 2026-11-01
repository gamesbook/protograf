# -*- coding: utf-8 -*-
"""
protograf 18XX games

Credits:
    * All symbols are sources from the  Noun Project (https://thenounproject.com)
      and are licensed under CC BY 3.0; see resources/xx18/symbols/CREDITS.md

Notes:
    * all arrays, such the cells of a board, are (col,row) with 1-based values

Summary of functions:

The 18xx map "blueprint" feature covers:

* depiction of towns as filled-in circles
* depiction of cities (single, double) as open circles; may include
  the railroad logo or a custom shape or text inset into it
* depiction of revenue (single, double) as circle with an amount
* depiction of track, curved or straight; by itself or extending from a city
* depiction of terminal spikes running off the board (short, medium and long)
* depiction of blocked hex-sides (as lines)
* depiction of private railways (in-hex; across hexes)
* depiction of icons for various in-hex features; including mountains (two sizes),
  hills, swamp, river, port, desert, mine, coal and oilrig
* setting of a single piece of text
* display of hex coordinates along the edges of the map
* depiction of a custom shape in a hex
* depiction of a circle on a hex-side (at a perbii position)
* depiction of a river running along a hex-side
* coloring ("fill") of a whole hex
* setting of a shaded rectangular area (typically red and at the edge of the map)
* creation of a small multi-line table to appear in a hex
  (typically income per stage of the game)

The blueprint will also provide:
* standard, named 18xx colors
* ability to set the map fonts (of different sizes) to use
* ability to put labels next to icons, towns or cities (above, below, left of, right of)

In-hex features, for example, cities, towns, icons, or lettering, will by default
appear at the centre of a hex. These can be repositioned using a combination of
direction (in degrees clockwise from east) and distance of the feature's center
from the hex center (as a fraction of the hex radius).

Positioning of features, such as lines or numbered circles, on hex edges will
be done using standard compass directions; "ne" for northeast, "s" for south, etc.,
and will be centred on that edge.

Drawing will be done following the order in which features are provided.
"""

# lib
from importlib.resources import files
import re
import math

# third party

# module
from protograf import globals
from protograf.base import BaseShape
from protograf.shapes import (
    RectangularLocations,
)
from protograf.utils import tools, colrs, geoms
from protograf.utils.constants import GRID_SHAPES_WITH_CENTRE, COLORS_18XX
from protograf.utils.messaging import feedback
from protograf.utils.structures import (  # named tuples; enums
    AbstractBoardType,
    Corner,
    HexOrientationName,
    Point,
    ShapeGeometry,
)
from protograf.utils.tools import _lower

# local
from .core_game import CoreGameObject

# ---- constants
XX18_HEX_HEIGHT = 4.399  # cm
XX18_HEX_SIDE = XX18_HEX_HEIGHT / math.sqrt(3)  # cm
XX18_HEX_DIAMETER = 2 * XX18_HEX_SIDE
XX18_CITY_DIAMETER = 1.45  # cm
XX18_TOWN_DIAMETER = 0.45  # cm
XX18_PRIVATE_DIAMETER = 0.4  # cm
XX18_REVENUE_DIAMETER = 0.8  # cm
XX18_MTN_SIDE = 0.6  # cm; equilateral triangle
XX18_SYMBOL_SET = [
    "coal",
    "hills",
    "desert",
    "mine",
    "mountains",
    "oil",
    "port",
    "river",
    "swamp",
]
XX18_FEATURE_SET = XX18_SYMBOL_SET + [
    "town",
    "city",
    "mountain",
    "private",
    "revenue",
    "fill",
]
XX18_LABEL_POSITION = ["above", "below", "left", "right"]
XX18_STROKE_WIDTH = 1
XX18_TEXT_SMALL = 12
XX18_TEXT_MEDIUM = 14
XX18_TEXT_LARGE = 16
XX18_TEXT_FONT = "Times New Roman"
XX18_RESOURCES = "resources/xx18/symbols/"


class XX18GameObject(CoreGameObject):
    """Create a XX18GameObject for a given canvas."""

    def __init__(self, _object=None, canvas=None, **kwargs):
        super().__init__(_object=_object, canvas=canvas, **kwargs)
        # ---- class props
        self.features = self._commons("features") or kwargs.get("features") or []
        print(f"&&& {self.features=}")
        # ---- 18xx game
        self.cell_size = XX18_HEX_HEIGHT
        self.game_class = "XX18Game"
        self.board_type = AbstractBoardType.HEXAGONAL
        self.board_pattern = "hexagonal"
        self.cells = {}  # track cell geo by grid-reference key
        if self.frame:
            feedback(
                f"The {self.game_class} 'frame' property cannot be used.",
                True,
                True,
            )
        # ---- orientation
        self.orientation = (
            self._commons("orientation") or kwargs.get("orientation") or "pointy"
        )
        if self.orientation == "pointy":
            self.orientation = HexOrientationName.POINTY.value
        elif self.orientation == "flat":
            self.orientation = HexOrientationName.FLAT.value
        else:
            raise ValueError(
                f'Invalid orientation "{self.orientation}" for {self.game_class}'
            )
        # ---- add in defaults
        if not self.rows:
            self.rows = 8
        if not self.cols:
            self.cols = 8
        self.set_options_by_game(**kwargs)  # MUST be before call to validate!
        self._validate_choices()
        # ---- 18xx default colors
        self.red = self._commons("red") or kwargs.get("red") or COLORS_18XX["red"]
        self.ground = (
            self._commons("ground") or kwargs.get("ground") or COLORS_18XX["ground"]
        )
        self.yellow = (
            self._commons("yellow") or kwargs.get("yellow") or COLORS_18XX["yellow"]
        )
        self.green = (
            self._commons("green") or kwargs.get("green") or COLORS_18XX["green"]
        )
        self.russet = (
            self._commons("russet") or kwargs.get("russet") or COLORS_18XX["russet"]
        )
        self.grey = self._commons("grey") or kwargs.get("grey") or COLORS_18XX["grey"]
        self.brown = (
            self._commons("brown") or kwargs.get("brown") or COLORS_18XX["brown"]
        )
        self.blue = self._commons("blue") or kwargs.get("blue") or COLORS_18XX["blue"]
        self.barrier = (
            self._commons("barrier") or kwargs.get("barrier") or COLORS_18XX["barrier"]
        )
        self.white = (
            self._commons("white") or kwargs.get("white") or COLORS_18XX["white"]
        )
        # self. = self._commons("") or kwargs.get("") or COLORS_18XX['']
        if kwargs.get("greys"):
            self.yellow = "#D4D4D4"
            self.green = "#B4B4B4"
            self.grey = "#909090"
            self.brown = "#636363"
            self.red = "#494848"
        # ---- setup
        self.setup_board()
        self.setup_pieces()  # none as yet

    def game_name_error(self):
        """Generate feedback if incorrect game name used."""
        pass

    def set_options_by_game(self, **kwargs):
        """Set properties according to preset, known, game."""
        pass

    def _validate_choices(self) -> bool:
        """Check and reset user choices for valid selections."""
        return True

    def draw_labels(self):
        """Draw labels around the board."""
        from protograf.protos import Text

        def hex_col_label():
            x, y = 0, 0
            ajc = adjacent_cell
            match self.label_start:
                case Corner.BOTTOM_RIGHT:
                    tr = geoms.fraction_along_line(ajc.ne, ajc.n, 0.5)
                    bl = geoms.fraction_along_line(ajc.s, ajc.sw, 0.5)
                    distance = self.label_size / self.units * 1.0
                    lbc = geoms.point_beyond_line(tr, bl, distance)
                    x, y = lbc.x, lbc.y
                case Corner.BOTTOM_LEFT:
                    tl = geoms.fraction_along_line(ajc.nw, ajc.n, 0.5)
                    br = geoms.fraction_along_line(ajc.s, ajc.se, 0.5)
                    distance = self.label_size / self.units * 1.0
                    lbc = geoms.point_beyond_line(tl, br, distance)
                    x, y = lbc.x, lbc.y
                case Corner.TOP_RIGHT:
                    x = ajc.nw.x + (ajc.n.x - ajc.nw.x) * (1.0 / 3.0)
                    y = ajc.n.y  # + shift * lbl_offset_col
                case Corner.TOP_LEFT:
                    x = ajc.ne.x - (ajc.ne.x - ajc.n.x) * (1.0 / 3.0)
                    y = ajc.n.y  # + shift * lbl_offset_col
                case _:
                    raise NotImplementedError(
                        "Cannot process label_start of {self.label_start}"
                    )
            return x, y

        # ---- label ranges
        if self.label:
            match self.label_start:
                case Corner.TOP_RIGHT:  # eg. Shogi
                    start_col, start_row = self.cols, 1
                    delta_row, delta_col = 1, -1
                    end_col, end_row = 0, self.rows + 1
                case Corner.TOP_LEFT:  # eg. Hex
                    start_col, start_row = 1, 1
                    delta_row, delta_col = 1, 1
                    end_col, end_row = self.cols + 1, self.rows + 1
                case Corner.BOTTOM_RIGHT:  # eg. ???
                    start_col, start_row = self.cols, self.rows
                    delta_row, delta_col = -1, -1
                    end_col, end_row = 0, 0
                case Corner.BOTTOM_LEFT:  # eg. Chess (default)
                    start_col, start_row = 1, self.rows
                    delta_row, delta_col = -1, 1
                    end_col, end_row = self.cols + 1, 0

            # ---- label settings
            _label_col = self._p2v(self.label_size) * 0.5  # user-units
            _label_row = self._p2v(self.label_size) * 0.75  # user-units
            lbl_intersect = 0  # user-units
            lbl_offset = self.label_offset if self.label_offset else None
            if lbl_offset:
                _label_col, _label_col = lbl_offset, lbl_offset
            else:
                _label_col = self._p2v(self.label_size) * 0.5  # user-units
                _label_row = self._p2v(self.label_size) * 0.75  # user-units
                if self.intersections:
                    lbl_intersect = 0.5 * self.cell_size  # user-units
            lbl_offset_col = (
                self.label_offset_col if self.label_offset_col else _label_col
            )
            lbl_offset_row = (
                self.label_offset_row if self.label_offset_row else _label_row
            )
            lkeys = {}
            lkeys["font_name"] = self.label_font
            lkeys["font_size"] = self.label_size
            lkeys["stroke"] = self.label_stroke

            # ---- column label settings
            if self.label_start in [Corner.TOP_RIGHT, Corner.TOP_LEFT]:
                label_row = 1
                shift = -1
            elif self.label_start in [Corner.BOTTOM_RIGHT, Corner.BOTTOM_LEFT]:
                label_row = self.rows
                shift = 1
            else:
                raise NotImplementedError(
                    "Cannot process label_start of {self.label_start}"
                )

            # ---- hex column labels
            if self.board_type == AbstractBoardType.HEXAGONAL:
                non_blank_col_no = 1  # do NOT label blank diagonals
                for _, dcells in self.hexgrid_diagonals.items():
                    # print(f'&&& {dcells=} {non_blank_col_no=}')
                    for value in dcells:
                        col_no, row_no = value[0], value[1]
                        col_value = tools.as_excel(non_blank_col_no, False)
                        adjacent_cell = self.board_layout.cells[(col_no, row_no)]
                        if not adjacent_cell.blank:
                            x, y = hex_col_label()
                            Text(col_value, x=x, y=y, **lkeys)
                            # print(f'&&& {col_value=} {col_no=} {row_no=}')
                            non_blank_col_no += 1
                            break  # label done; next diagonal, please!
            else:
                raise NotImplementedError(
                    "No labels can be drawn for this type of board!"
                )
            # print('&&& col label', ltype, col_value, x, y)

            # ---- row labels
            if self.label_start in [Corner.TOP_LEFT, Corner.BOTTOM_LEFT]:
                label_col = 1
                shift = -1
                col_shift = 1
            elif self.label_start in [Corner.BOTTOM_RIGHT, Corner.TOP_RIGHT]:
                label_col = self.cols
                shift = 1
                col_shift = -1
            else:
                raise NotImplementedError(
                    "Cannot process label_start of {self.label_start}"
                )

            row_num = 1
            for row_no in range(start_row, end_row, delta_row):
                if self.label_type in ["AA", "NA"]:
                    row_value = tools.alpha_column(row_num, lower=False)
                else:
                    row_value = str(row_num)
                col_no = label_col  # label col can be at start or end
                # print(f"{row_no=} {col_no=}") ; breakpoint()
                # skip blank columns at start of a hexagonal grid row
                if self.board_type == AbstractBoardType.HEXAGONAL:
                    active_cells = self.cells_non_blank[row_no - 1]
                    while True:
                        col_exists = any(
                            len(tup) > 1 and tup[0] == col_no for tup in active_cells
                        )
                        if col_exists:
                            break
                        col_no += col_shift
                        if col_no < 1 or col_no > self.cols:
                            col_no = label_col  # give up and use default ...
                            break
                # get cell geo to use for label position
                adjacent_cell = self.board_layout.cells[(col_no, row_no)]
                if self.board_type == AbstractBoardType.GRID:
                    if self.label_start in [Corner.TOP_LEFT, Corner.BOTTOM_LEFT]:
                        x = adjacent_cell.w.x + shift * lbl_offset_row + lbl_intersect
                        y = adjacent_cell.w.y + (self.label_size * 0.5) / globals.units
                    else:
                        x = adjacent_cell.e.x + shift * lbl_offset_row - lbl_intersect
                        y = adjacent_cell.e.y + (self.label_size * 0.5) / globals.units
                elif self.board_type == AbstractBoardType.HEXAGONAL:
                    if self.label_start in [Corner.TOP_LEFT, Corner.BOTTOM_LEFT]:
                        x = adjacent_cell.w.x + shift * lbl_offset_row
                        y = adjacent_cell.w.y + (self.label_size * 0.5) / globals.units
                    else:
                        x = adjacent_cell.e.x + shift * lbl_offset_row
                        y = adjacent_cell.e.y + (self.label_size * 0.5) / globals.units
                elif self.board_type == AbstractBoardType.TRIANGULAR:
                    raise NotImplementedError("No labels for Triangle grids!")
                # print('&&& row label', ltype, row_value, x, y)
                Text(row_value, x=x, y=y, **lkeys)
                row_num += 1

    def setup_board(self):
        """Create board_layout for the required grid"""
        from protograf.protos import Layout, rectangle, Hexagons

        # ---- game-based defaults
        board_start = "NW"
        board_direction = "east"
        # Point(top_x, top_x) is the top-left point of the VirtualLocations (grid points)

        # pointy; non-offset
        top_x = self.x if self.kwargs.get("x") else 0
        top_y = self.y if self.kwargs.get("y") else 0
        colr = self.fills[0] if self.fills else "white"
        x_offset = 0
        # x_offset = -0.5 * self.cell_size
        if self.name == "hexhex" and self.auto_size and self.hexes % 2 == 0:
            x_offset = -self.cell_size * 0.5
        self.board_layout = Hexagons(
            cols=self.cols,
            rows=self.rows,
            x=top_x + x_offset,
            y=top_y,
            orientation=self.orientation,
            _draw_grid=False,
            pattern=self.pattern,
            user=f"{self.game_class}",
            # single hexagon properties:-
            height=self.cell_size,
            stroke=self.stroke,
            stroke_width=XX18_STROKE_WIDTH,
            fill=colr,
            # hex_shape=self.cell_shape,  # insert centre_image into hex?
        )
        # print(f'&&& XX18 BOARD {self.board_layout.cells.keys()=}')

        # ---- * track non-blank cells
        for row in range(1, self.rows + 1):
            non_blank = []
            for col in range(1, self.cols + 1):
                try:
                    cell_geo = self.board_layout.cells[(col, row)]
                    if not cell_geo.blank:
                        non_blank.append((col, row))
                except Exception as err:
                    feedback(
                        f"Unable to set properties for {col=}/{row=} ({err})",
                        True,
                        True,
                    )
            self.cells_non_blank.append(non_blank)  # per-row list of non-blank

        # ---- * set cell attributes (plus label)
        for row in range(1, self.rows + 1):
            for col in range(1, self.cols + 1):
                try:
                    cell_geo = self.board_layout.cells[(col, row)]
                    if self.orientation == HexOrientationName.POINTY.value:
                        row_alpha = tools.as_excel(row, False)
                        if self.odd(row):
                            col_num = col * 2 - 1
                        else:
                            col_num = col * 2
                        cell_id = f"{row_alpha}{col_num}"
                    elif self.orientation == HexOrientationName.FLAT.value:
                        col_alpha = tools.as_excel(col, False)
                        row_num = row * 2 - 1
                        if self.even(col):
                            row_num += 1
                        cell_id = f"{col_alpha}{row_num}"
                    cell_geo_label = cell_geo._replace(name=cell_id)
                    # print(f"&&& HEX {row=} {col=} name={cell_id}")
                    setattr(self, cell_id, cell_geo_label)
                    self.cells[cell_id] = cell_geo
                except Exception as err:
                    feedback(
                        f"Unable to process hex cell: {col=} {row=} ({err})",
                        True,
                        True,
                    )

    def process_locations(self, location: str = None, name: str = None) -> list:
        """Extract one or more location(s) from a string.

        Args:
            location (str): grid reference or references for one or more cells
        """
        if not location:
            return []
        if location is not None and not isinstance(location, str):
            _loc = "Location(s)"
            if name:
                _loc = f"The {name} location(s)"
            feedback(
                f"{_loc} must be a string; not '{location}'.",
                True,
                True,
            )
        if " " in location:
            _locations = tools.split(location, separator=" ", clean=True)
        else:
            _locations = [location]
        # check each location exists in the grid
        for _loc in _locations:
            if _loc not in self.cells.keys():
                feedback(
                    f'The hexagon reference "{_loc}" is not on this board.',
                    True,
                    True,
                )
        return _locations

    def process_feature(self, feature: tuple = None) -> list:
        """Process a feature from its tuple

        Args:
            location (str): grid reference or references for one or more cells

        Notes:
            * The feature (tuple) should contain in this order:
                cellID (str): the alphanumeric grid coordinate of the hex
                feature (str): the name of the feature or symbol to draw
                direction (float): optional, degrees (default zero)
                distance (float): optional, fraction (default zero)
                label (str): a label for the feature or symbol (default "")

            * For a private railroad, which has a start and end hex, the
              start settings are the ones above, and then the following extras
              need to be supplied:
                cellID (str): the alphanumeric grid coordinate of the end hex
                direction (float): optional, degrees (default zero) in end hex
                distance (float): optional, fraction (default zero) in end hex
              It is possible for start end hex to be the same

        """
        # ---- validate input
        if not feature:
            return []
        if feature is not None and not isinstance(feature, (tuple, list)):
            feedback(
                f"Feature must contain a set of values; not '{feature}'.",
                True,
                True,
            )
        if len(feature) < 2:
            feedback(
                f"Feature must contain at least two values; not '{feature}'.",
                True,
                True,
            )
        self.process_locations(feature[0])  # sanity check
        # ---- feature property values
        kwargs = {}
        ftype = feature[1]
        if ftype not in XX18_FEATURE_SET:
            feedback(
                f"The feature '{ftype}' is not available;",
                f" choose from: {XX18_FEATURE_SET}.",
                True,
                True,
            )
        fdirection, fdistance, flabel, flabel_pos = 0, 0, "", None
        if len(feature) >= 3:
            _fdir = feature[2]
            fdirection = tools.as_float(_fdir, "direction")
        if len(feature) >= 4:
            _fdist = feature[3]
            fdistance = tools.as_float(_fdist, "distance")
        if len(feature) >= 5:
            flabel = str(feature[4])
        if len(feature) >= 6 and ftype != "private":  # see below; private overloads
            flabel_pos = feature[5]
            if flabel_pos not in XX18_LABEL_POSITION:
                feedback(
                    f"The label positions '{feature[5]}' is not available;",
                    f" choose from: {XX18_LABEL_POSITION}.",
                    True,
                    True,
                )
            kwargs["label_position"] = flabel_pos
        print(f"&&& {feature[0]=} {ftype=} {fdirection=} {fdistance=} {flabel=} ")
        # ---- feature to function
        match ftype:
            case "city":
                self.city(
                    location=feature[0],
                    label=flabel,
                    direction=fdirection,
                    distance=fdistance,
                    **kwargs,
                )
            case "fill":
                self.fill_hex(
                    location=feature[0],
                    color=flabel,
                    **kwargs,
                )
            case "town":
                self.town(
                    location=feature[0],
                    label=flabel,
                    direction=fdirection,
                    distance=fdistance,
                    **kwargs,
                )
            case "mountain":
                self.mountain(
                    location=feature[0],
                    label=flabel,
                    direction=fdirection,
                    distance=fdistance,
                    **kwargs,
                )
            case "private":
                flocation1, fdirection1, fdistance1 = "", 0, 0
                if len(feature) >= 6:
                    flocation1 = str(feature[5])
                    if flocation1 in ["", None]:
                        flocation1 = feature[0]
                if len(feature) >= 7:
                    _fdir1 = feature[6]
                    fdirection1 = tools.as_float(_fdir1, "direction")
                if len(feature) >= 8:
                    _fdist1 = feature[7]
                    fdistance1 = tools.as_float(_fdist1, "distance")

                if len(feature) >= 9:
                    flabel_pos = feature[8]
                    if flabel_pos not in XX18_LABEL_POSITION:
                        feedback(
                            f"The label position '{feature[8]}' is not available;",
                            f" choose from: {XX18_LABEL_POSITION}.",
                            True,
                            True,
                        )
                    kwargs["label_position"] = flabel_pos
                print(f"&&& private {flocation1=} {fdirection1=} {fdistance1=}")
                self.private(
                    label=flabel,
                    location=feature[0],
                    direction=fdirection,
                    distance=fdistance,
                    location1=flocation1,
                    direction1=fdirection1,
                    distance1=fdistance1,
                    **kwargs,
                )
            case "revenue":
                self.revenue(
                    location=feature[0],
                    label=flabel,
                    direction=fdirection,
                    distance=fdistance,
                    **kwargs,
                )
            case _:
                self.symbol(
                    location=feature[0],
                    label=flabel,
                    direction=fdirection,
                    distance=fdistance,
                    name=ftype,
                    **kwargs,
                )

    def feature_location(
        self, geo: ShapeGeometry, direction: float = None, distance: float = None
    ) -> Point:
        """Get a feature's centre Point."""
        if direction is not None and distance is not None:
            length = distance * XX18_HEX_SIDE  # fraction of radius
            fcentre = geoms.point_from_angle(geo.centre, length, direction)
        else:
            fcentre = geo.centre
        return fcentre

    def town(
        self,
        location: str = None,
        label: str = None,
        direction: float = None,
        distance: float = None,
        **kwargs,
    ):
        """Draw Town shape at hex location(s).

        Args:
            location (str): grid reference or references for one or more cells
            label (str): the name of the Town
            direction (float): degrees clockwise from East
            distance (float): distance from hex centre
        """
        from protograf.protos import Circle

        _locations = self.process_locations(location, "town")
        for _loc in _locations:
            geo = self.cells.get(_loc)
            ccentre = self.feature_location(geo, direction, distance)
            Circle(
                cxy=ccentre,
                radius=XX18_TOWN_DIAMETER / 2.0,
                fill_stroke="black",
                stroke_width=XX18_STROKE_WIDTH,
            )
            if label:
                print("TODO")

    def city(
        self,
        location: str = None,
        label: str = None,
        direction: float = None,
        distance: float = None,
        shape: str = None,
        **kwargs,
    ):
        """Draw City shape at hex location(s).

        Args:
            location (str): grid reference or references for one or more cells
            label (str): the name of the city
            direction (float): degrees clockwise from East
            distance (float): distance from hex centre
            shape (Shape): the shape to be drawn inside the city
        """
        from protograf.protos import Circle

        _locations = self.process_locations(location, "city")
        for _loc in _locations:
            geo = self.cells.get(_loc)
            ccentre = self.feature_location(geo, direction, distance)
            Circle(
                cxy=ccentre,
                radius=XX18_CITY_DIAMETER / 2.0,
                fill="white",
                stroke="black",
                stroke_width=XX18_STROKE_WIDTH,
                centre_shape=shape,
            )
            if label:
                print("TODO")

    def revenue(
        self,
        location: str = None,
        label: str = None,
        direction: float = None,
        distance: float = None,
        **kwargs,
    ):
        """Draw Revenue shape at hex location(s).

        Args:
            location (str): grid reference or references for one or more cells
            label (str): the value of the revenue
            direction (float): degrees clockwise from East
            distance (float): distance from hex centre
        """
        from protograf.protos import Circle

        _locations = self.process_locations(location, "revenue")
        for _loc in _locations:
            geo = self.cells.get(_loc)
            ccentre = self.feature_location(geo, direction, distance)
            Circle(
                cxy=ccentre,
                radius=XX18_REVENUE_DIAMETER / 2.0,
                fill=None,
                stroke="black",
                stroke_width=XX18_STROKE_WIDTH,
                label=label if label else "",
                label_size=XX18_TEXT_MEDIUM,
            )

    def fill_hex(
        self,
        location: str = None,
        color: object = None,
        **kwargs,
    ):
        """Fill in color at hex location(s).

        Args:
            location (str): grid reference or references for one or more cells
            color (color): a color reference
        """
        from protograf.protos import Hexagon

        _locations = self.process_locations(location, "fill")
        the_color = colrs.get_color(color)
        for _loc in _locations:
            geo = self.cells.get(_loc)
            ccentre = geo.centre
            Hexagon(
                cxy=ccentre,
                height=XX18_HEX_HEIGHT,
                fill=the_color,
                stroke="black",
                stroke_width=XX18_STROKE_WIDTH,
                orientation=self.orientation,
            )

    def mountain(
        self,
        location: str = None,
        label: str = None,
        direction: float = None,
        distance: float = None,
        **kwargs,
    ):
        """Draw Mountain shape at hex location(s).

        Args:
            location (str): grid reference or references for one or more cells
            label (str): the cost of the mountain
            direction (float): degrees clockwise from East
            distance (float): distance from hex centre
        """
        from protograf.protos import Triangle

        _locations = self.process_locations(location, "revenue")
        for _loc in _locations:
            geo = self.cells.get(_loc)
            ccentre = self.feature_location(geo, direction, distance)
            Triangle(
                cx=ccentre.x,
                cy=ccentre.y,
                side=XX18_MTN_SIDE,
                stroke_width=XX18_STROKE_WIDTH,
                fill="black",
            )

    def private(
        self,
        label: str = None,
        location: str = None,
        direction: float = None,
        distance: float = None,
        location1: str = None,
        direction1: float = None,
        distance1: float = None,
        **kwargs,
    ):
        """Draw Private Railroad at hex location(s).

        Args:
            label (str): the name of the Private Railroad
            location (str): grid reference or references for start cell
            direction (float): degrees clockwise from East in start cell
            distance (float): distance from hex centre in start cell
            location1 (str): grid reference or references for start cell
            direction1 (float): degrees clockwise from East in end cell
            distance1 (float): distance from hex centre in end cell
        """
        from protograf.protos import Circle, Line

        _locations = self.process_locations(location, "private-start")
        _locations1 = self.process_locations(location1, "private-end")
        if _locations and _locations1:
            _loc = _locations[0]
            _loc1 = _locations1[0]
            geo = self.cells.get(_loc)
            geo1 = self.cells.get(_loc1)
            ccentre = self.feature_location(geo, direction, distance)
            ccentre1 = self.feature_location(geo1, direction1, distance1)
            pcs = Circle(
                cxy=ccentre,
                radius=XX18_PRIVATE_DIAMETER / 2.0,
                fill=None,
                stroke="black",
                stroke_width=XX18_STROKE_WIDTH,
                # label=label if label else "",
                # label_size=XX18_TEXT_MEDIUM,
            )
            pce = Circle(
                cxy=ccentre1,
                radius=XX18_PRIVATE_DIAMETER / 2.0,
                fill=None,
                stroke="black",
                stroke_width=XX18_STROKE_WIDTH,
                # label=label if label else "",
                # label_size=XX18_TEXT_MEDIUM,
            )
            Line(
                links=[pcs, pce],
                stroke="black",
                stroke_width=XX18_STROKE_WIDTH,
            )

        if label:
            print("TODO")

    def symbol(
        self,
        location: str = None,
        label: str = None,
        direction: float = None,
        distance: float = None,
        name: str = None,
        **kwargs,
    ):
        """Draw a symbol/shape at hex location(s).

        Args:
            location (str): grid reference or references for one or more cells
            label (str): the label for the symbol
            direction (float): degrees clockwise from East
            distance (float): distance from hex centre
            name (str): the name the symbol
        """
        from protograf.protos import Image

        match name:
            case "coal":
                _file = files("protograf").joinpath(f"{XX18_RESOURCES}/coal.svg")
            case "hills":
                _file = files("protograf").joinpath(f"{XX18_RESOURCES}/hills.svg")
                kwargs["width"] = 1.5
                kwargs["height"] = 1.5
            case "desert":
                _file = files("protograf").joinpath(f"{XX18_RESOURCES}/desert.svg")
            case "mine":
                _file = files("protograf").joinpath(f"{XX18_RESOURCES}/mine.svg")
            case "mountains":
                _file = files("protograf").joinpath(f"{XX18_RESOURCES}/mountains.svg")
            case "oil":
                _file = files("protograf").joinpath(f"{XX18_RESOURCES}/oil.svg")
            case "port":
                _file = files("protograf").joinpath(f"{XX18_RESOURCES}/port.svg")
            case "river":
                _file = files("protograf").joinpath(f"{XX18_RESOURCES}/river.svg")
            case "swamp":
                _file = files("protograf").joinpath(f"{XX18_RESOURCES}/swamp.svg")
            case _:
                feedback(
                    f"The symbol 'name' property cannot be '{name}';",
                    f" choose from: {XX18_SYMBOL_SET}.",
                    True,
                    True,
                )
        _locations = self.process_locations(location, f"{name} symbol")
        for _loc in _locations:
            geo = self.cells.get(_loc)
            ccentre = self.feature_location(geo, direction, distance)
            Image(_file, cxy=ccentre, **kwargs)
