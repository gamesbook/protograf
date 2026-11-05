# -*- coding: utf-8 -*-
"""
protograf 18XX games

Credits:
    * All symbols are sourced from the Noun Project (https://thenounproject.com)
      and are licensed under CC BY 3.0; see resources/xx18/symbols/CREDITS.md

Notes:
    * all arrays, such the cells of a board, are (col,row) with 1-based values

Summary of functions:

The 18xx map "blueprint" feature covers:

* depiction of towns as filled-in circles (may include a border)
* depiction of cities (single, double) as open circles; may include
  the railroad logo or a custom shape or text inset into it
* depiction of revenue as circle with an amount
* depiction of track, curved or straight; by itself or extending from a city
* depiction of terminal spikes running off-board (short, medium and long)
* depiction of blocked hex-sides as thick lines
* depiction of private railways; either in-hex or across hexes
* depiction of icons for common in-hex features; including mountains
  (two sizes), hills, and rivers
* depiction of symbols for special features such coal, desert, factory,
  fish, flag, forest, hills, lock, mine, noentry, oil, pennant, port,
  swamp, train, tree, tunnel
* depiction of a river; as "wavy line"; running through a hex
* depiction of a custom shape in a hex
* display of a single piece of text
* display of hex coordinates along the edges of the map
* coloring ("fill") of a whole hex
* setting of a shaded rectangular area (typically red and at the map edge)
* creation of a small multi-line table to appear in an off-board hex
  (typically income per stage of the game)

The blueprint will also provide:
* standard, named 18xx colors
* ability to set the map fonts (of different sizes) to use
* ability to put labels next to icons, towns or cities
  (above, below, left of, right of)

In-hex features, for example, cities, towns, icons, or lettering, will by default
appear at the centre of a hex. These can be repositioned using a combination of
direction (in degrees clockwise from east) and distance of the feature's center
from the hex center (as a fraction of the hex radius).

Positioning of features, such as lines, spikes, bumps or numbered circles, on hex
edges will be done using standard compass directions; "ne" for northeast,
"s" for south, etc., and will be centred on that edge.

Drawing will be done following the order in which features are provided.

Standard, named 18xx colors
===========================

Tile Phase        Classic (Avalon Hill) HEX Code  Modern (Lookout/Mayfair) HEX Code
----------------- ------------------------------- ---------------------------------
Yellow (Phase 2)  #FFD200 (Bright Golden Yellow)  #F1C40F (Muted/Warm Yellow)
Green (Phase 3)   #00A651 (Rich Kelly Green)      #27AE60 (Mid-tone Emerald)
Brown (Phase 5)   #7A4B1B (Deep Chocolate Brown)  #7E5109 (Clay/Dark Ochre)
Gray (Phase 7)    #7F8C8D (Medium Neutral Gray)   #95A5A6 (Light Slate Gray)
----------------- ------------------------------- ---------------------------------

Hex Type / Phase   HEX Code UI Design Purpose
------------------ -------- ----------------------------------------------------
Map Background     #EAEAEA  Neutral light gray to make active hexes pop.
Plain Hex (Base)   #FFFFFF  Stark white or a pale off-white (#F9F9F9).
Yellow Phase Hex   #F1E351  Warm digital yellow
Green Phase Hex    #4CAF50  Vibrant emerald green for clear route tracking
Brown Phase Hex    #8D6E63  Balanced medium brown
Gray Phase Hex     #B0BEC5  Cool, light slate gray
Barrier            #757575  Dark neutral gray for mountain edges or grid borders
Off-Board Red Hex  #EF5350  Soft digital crimson for red-zone revenue endpoints

Coastal Water      #5A8CAF  Often used near the coastline; water for artwork & land
Avalon Hill Water  #4A7F9D  Slightly green-tinted teal-blue
Modern 18xx Water  #A9CBE2  Very pale sky-blue. Desaturated, pastel light-blue

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
from protograf.utils.constants import GRID_SHAPES_WITH_CENTRE
from protograf.utils.messaging import feedback
from protograf.utils.structures import (  # named tuples; enums
    AbstractBoardType,
    Corner,
    HexOrientation,
    HexOrientationName,
    Point,
    ShapeGeometry,
)
from protograf.utils.tools import _lower

# local
from .core_game import CoreGameObject

# ---- "variable" constants
# TODO => enable overwrite by loading via JSON
XX18_HEX_SIDE = 2.3864  # cm
XX18_CITY_DIAMETER = 1.45  # cm
XX18_TOWN_DIAMETER = 0.45  # cm
XX18_TOWN_HEIGHT = 0.45  # cm
XX18_TOWN_HEIGHT = 0.7  # cm
XX18_TOWN_HEIGHT_OUTER = 0.8  # cm
XX18_TOWN_WIDTH = 0.4  # cm
XX18_TOWN_WIDTH_OUTER = 0.5  # cm
XX18_TOWN_DIAMETER_BORDER = 0.55  # cm; outer-circle
XX18_PRIVATE_DIAMETER = 0.4  # cm
XX18_REVENUE_DIAMETER = 0.8  # cm
XX18_TRACK_WIDTH_INNER = 0.4  # cm
XX18_TRACK_WIDTH_OUTER = 0.5  # cm
XX18_MOUNTAIN_SIDE = 0.6  # cm; equilateral triangle
XX18_STROKE_WIDTH = 1
XX18_TEXT_SMALL = 11
XX18_TEXT_MEDIUM = 13
XX18_TEXT_LARGE = 16
XX18_TEXT_EXTRA = 20
XX18_TEXT_FONT = "Times-Roman"
XX18_TEXT_FONT_BOLD = "Times-Bold"
XX18_RESOURCES = "resources/xx18/symbols/"

# ---- color constants
XX18_TILE_YELLOW = "#FFD200"
XX18_TILE_GREEN = "#00A651"
XX18_TILE_BROWN = "#7A4B1B"
XX18_TILE_GRAY = "#7F8C8D"
XX18_TILE_YELLOW_MF = "#F1C40F"
XX18_TILE_GREEN_MF = "#27AE60"
XX18_TILE_BROWN_MF = "#7E5109"
XX18_TILE_GRAY_MF = "#95A5A6"
XX18_HEX_BACK = "#EAEAEA"
XX18_HEX_PLAIN = "#FFFFFF"
XX18_HEX_PLAIN_OFF = "#F9f9f9"
XX18_HEX_YELLOW = "#F1E351"
XX18_HEX_GREEN = "#4CAF50"
XX18_HEX_BROWN = "#8D6E63 "
XX18_HEX_GRAY = "#B0BEC5"
XX18_HEX_BARRIER = "#757575"
XX18_HEX_OFFBOARD = "#EF5350"
XX18_HEX_WATER = "#4A7F9D"

# ---- fixed/derived constants
XX18_HEX_HEIGHT = XX18_HEX_SIDE * math.sqrt(3)  # cm
XX18_HEX_DIAMETER = 2 * XX18_HEX_SIDE
XX18_SYMBOL_SET = [
    "coal",
    "desert",
    "factory",
    "fish",
    "flag",
    "forest",
    "hills",
    "lock",
    "mine",
    "mountains",
    "noentry",
    "oil",
    "pennant",
    "port",
    "river",
    "swamp",
    "train",
    "tree",
    "tunnel",
]
XX18_FEATURE_SET = XX18_SYMBOL_SET + [
    "town",
    "town_border",
    "city",
    "cityx1",
    "cityx2",
    "cityx3",
    "cityx4",
    "mountain",
    "private",
    "revenue",
    "tile_letter",
    "tile-letter",
    "fill",
    "block",
    "spike",
    "track",
    "track_town",
]
XX18_LABEL_POSITION = ["above", "below", "left", "right"]


class XX18GameObject(CoreGameObject):
    """Create a XX18GameObject for a given canvas."""

    def __init__(self, _object=None, canvas=None, **kwargs):
        super().__init__(_object=_object, canvas=canvas, **kwargs)
        # ---- class props
        self.features = self._commons("features") or kwargs.get("features") or []
        # print(f"&&& {self.features=}")
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
        self.plain_hex = XX18_HEX_PLAIN
        self.ground_hex = XX18_HEX_PLAIN_OFF
        self.yellow_hex = XX18_HEX_YELLOW
        self.green_hex = XX18_HEX_GREEN
        self.brown_hex = XX18_HEX_BROWN
        self.gray_hex = XX18_HEX_GRAY
        self.grey_hex = XX18_HEX_GRAY
        self.barrier_hex = XX18_HEX_BARRIER
        self.offboard_hex = XX18_HEX_OFFBOARD
        self.background = XX18_HEX_BACK
        self.water_hex = XX18_HEX_WATER
        # self. = self._commons("") or kwargs.get("") or COLORS_18XX['']
        if kwargs.get("greys"):
            self.yellow_hex = "#D4D4D4"
            self.green_hex = "#B4B4B4"
            self.grey_hex = "#909090"
            self.gray_hex = "#909090"
            self.brown_hex = "#636363"
            self.offboard_hex = "#494848"
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
        hex_color = self.fill if self.fill else self.plain_hex
        x_offset = 0
        # x_offset = -0.5 * self.cell_size
        if self.name == "hexhex" and self.auto_size and self.hexes % 2 == 0:
            x_offset = -self.cell_size * 0.5
        self.board_layout = Hexagons(
            cols=self.cols,
            rows=self.rows,
            x=top_x + x_offset,
            y=top_y,
            # offset= odd/even TODO
            orientation=self.orientation,  # default: pointy
            _draw_grid=False,
            pattern=self.pattern,
            user=f"{self.game_class}",
            # single hexagon properties:-
            height=self.cell_size,
            stroke=self.stroke,
            stroke_width=XX18_STROKE_WIDTH,
            fill=hex_color,
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
                    else:
                        cell_id = ""
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

    def feature_position(self, position: tuple | str = None) -> tuple:
        """Extract either (direction, distance) tuple or string from a string."""
        if not position:
            return None, None
        if isinstance(position, (list, tuple)):
            if len(position) < 2:
                feedback(
                    f"Position must contain at least two values; not '{position}'.",
                    True,
                    True,
                )
            direction, distance = 0, 0
            _fdir = position[0]
            direction = tools.as_float(_fdir, "direction")
            if len(position) >= 1:
                _fdist = position[1]
                distance = tools.as_float(_fdist, "distance")
            return direction, distance
        elif isinstance(position, str):
            # TODO - validate hexside position !
            # print(f"hexside: {position}")
            return position, None
        else:
            feedback(
                f'The position must be a set of two numbers or a hex side, not "{position}"',
                True,
                True,
            )
            return None, None

    def process_feature(self, feature: tuple = None) -> list:
        """Process a feature from its tuple

        Args:
            location (str): grid reference or references for one or more cells

        Notes:
            * The feature (tuple) should contain in this order:
                  cellID (str): the alphanumeric grid coordinate of the hex
                  position (tuple | str): either a tuple of
                      direction (float): optional, degrees
                      distance (float): optional, fraction
                    or a string of:
                      hex-side directions
                    or None
                  label (str): a label for the feature or symbol (default "")
                  label_position (str): the position for label (above, below, L, R)

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
                f"The feature '{ftype}' is not available; choose from: \n{XX18_FEATURE_SET}.",
                True,
                True,
            )
        flabel, flabel_pos, fdirection, fdistance = "", None, None, None
        if len(feature) >= 3:
            fdirection, fdistance = self.feature_position(feature[2])
        if len(feature) >= 4:
            flabel = str(feature[3])
        if len(feature) >= 5 and ftype != "private":  # see below; private overloads
            flabel_pos = feature[4]
            if flabel_pos not in XX18_LABEL_POSITION:
                feedback(
                    f"The label positions '{feature[5]}' is not available;",
                    f" choose from: {XX18_LABEL_POSITION}.",
                    True,
                    True,
                )
            kwargs["label_position"] = flabel_pos
        # print(f"&&& {feature[0]=} {ftype=} {fdirection=} {fdistance=} {flabel=} ")
        # ---- feature to function
        match ftype:
            case "fill":
                self.fill_hex(
                    location=feature[0],
                    color=flabel,
                    **kwargs,
                )
            case "city" | "cityx1" | "cityx2" | "cityx3" | "cityx4":
                if "x" in ftype:
                    _, count = ftype.split("x")
                else:
                    count = 1
                self.city(
                    location=feature[0],
                    label=flabel,
                    direction=fdirection,
                    distance=fdistance,
                    count=count,
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
            case "town_border":
                self.town(
                    location=feature[0],
                    label=flabel,
                    direction=fdirection,
                    distance=fdistance,
                    border=True,
                    **kwargs,
                )
            case "track":
                self.track(
                    location=feature[0],
                    label=flabel,
                    position=fdirection,
                    color=None,  # TODO => how to set
                    **kwargs,
                )
            case "track_town":
                self.track(
                    location=feature[0],
                    label=flabel,
                    position=fdirection,
                    color=None,  # TODO => how to set
                    town="middle",  # ALL POSITIONS NOT OPERATIONAL
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
                # print(f"&&& private {flocation1=} {fdirection1=} {fdistance1=}")
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
            case "tile_letter" | "tile-letter" | "tileletter":
                self.tile_letter(
                    location=feature[0],
                    label=flabel,
                    direction=fdirection,
                    distance=fdistance,
                    **kwargs,
                )
            case "block":
                self.block(
                    location=feature[0],
                    label=flabel,
                    position=fdirection,
                    color=None,  # TODO => how to set
                    **kwargs,
                )
            case "spike":
                self.spike(
                    location=feature[0],
                    size=flabel,
                    position=fdirection,
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

    def process_label(
        self,
        label: str,
        position: str = "below",
        base_shift: float = 0.0,
        text_size: str = "medium",
    ) -> dict:
        """Create label properties for a feature or symbol."""
        kwargs = {}
        label_mx = 0.0
        heading, title, _label = "", "", ""
        label_align = "centre"
        match text_size:
            case "small":
                font_size = XX18_TEXT_SMALL
            case "medium":
                font_size = XX18_TEXT_MEDIUM
            case "large":
                font_size = XX18_TEXT_LARGE
            case _:
                raise ValueError(
                    f'Text size "{text_size}" is not available for label processing'
                )
        if label:
            shift = base_shift + self.label_size / self.units / 3.0
            match position:
                case "above":
                    heading = label
                case "below":
                    title = label
                case "left":
                    _label = label
                    label_mx = -shift
                    label_align = "right"
                case "right":
                    _label = label
                    label_mx = shift
                    label_align = "left"
        else:
            label = ""

        kwargs["heading"] = heading
        kwargs["heading_size"] = font_size
        kwargs["heading_font"] = XX18_TEXT_FONT
        kwargs["heading_stroke"] = "black"

        kwargs["title"] = title
        kwargs["title_size"] = font_size
        kwargs["title_font"] = XX18_TEXT_FONT
        kwargs["title_stroke"] = "black"

        kwargs["label"] = _label
        kwargs["label_mx"] = label_mx
        kwargs["label_align"] = label_align
        kwargs["label_size"] = font_size
        kwargs["label_font"] = XX18_TEXT_FONT
        kwargs["label_stroke"] = "black"
        return kwargs

    def process_track_town_position(
        self, hexagon: object, path_pair: list, offset: str = "middle"
    ) -> tuple:
        """Determine where on a hexagon path a shape should be located.

        Args:
            hexagon (Hexagon): a pre-drawn Hexagon shape
            path_pair (list): list of two strings (start and end compass directions)
            offset: where on the path to draw the shape

        Returns:
            tuple: direction (float), distance (float), rotation (float)
        """
        direction, distance, rotation = 0, 0, 0
        if hexagon.ORIENTATION == HexOrientation.FLAT:
            match path_pair:
                # 120 degrees / short arc
                case ["n", "ne"] | ["ne", "n"]:
                    direction = 60
                    distance = 0.4
                    rotation = 60
                case ["se", "ne"] | ["ne", "se"]:
                    direction = 60
                    distance = 0.4
                    rotation = 60
                case ["se", "s"] | ["s", "se"]:
                    direction = 60
                    distance = 0.4
                    rotation = 60
                case ["sw", "s"] | ["s", "sw"]:
                    direction = 60
                    distance = 0.4
                    rotation = 60
                case ["sw", "nw"] | ["nw", "sw"]:
                    direction = 60
                    distance = 0.4
                    rotation = 60
                case ["n", "nw"] | ["nw", "n"]:
                    direction = 60
                    distance = 0.4
                    rotation = 60
                # 60 degrees / long arc
                case ["n", "se"] | ["se", "n"]:
                    direction = 60
                    distance = 0.5
                    rotation = 60
                case ["ne", "s"] | ["s", "ne"]:
                    direction = 60
                    distance = 0.5
                    rotation = 60
                case ["se", "sw"] | ["sw", "se"]:
                    direction = 60
                    distance = 0.5
                    rotation = 60
                case ["s", "nw"] | ["nw", "s"]:
                    direction = 60
                    distance = 0.5
                    rotation = 60
                case ["sw", "n"] | ["n", "sw"]:
                    direction = 60
                    distance = 0.5
                    rotation = 60
                case ["nw", "ne"] | ["ne", "nw"]:
                    direction = 60
                    distance = 0.5
                    rotation = 60
                # 90 degrees
                case ["nw", "se"] | ["se", "nw"]:
                    direction = 0
                    distance = 0
                    rotation = 90
                case ["ne", "sw"] | ["sw", "ne"]:
                    direction = 0
                    distance = 0
                    rotation = 90
                case ["n", "s"] | ["s", "n"]:
                    direction = 0
                    distance = 0
                    rotation = 90
        elif hexagon.ORIENTATION == HexOrientation.POINTY:
            match path_pair:
                # 120 degrees / short arc
                case ["e", "ne"] | ["ne", "e"]:
                    direction = 330
                    distance = 0.5
                    rotation = 120
                case ["e", "se"] | ["se", "e"]:
                    direction = 30
                    distance = 0.5
                    rotation = 60
                case ["sw", "se"] | ["se", "sw"]:
                    direction = 90
                    distance = 0.5
                    rotation = 0
                case ["w", "sw"] | ["sw", "w"]:
                    direction = 150
                    distance = 0.5
                    rotation = 300
                case ["w", "nw"] | ["nw", "w"]:
                    direction = 210
                    distance = 0.5
                    rotation = 240
                case ["nw", "ne"] | ["ne", "nw"]:
                    direction = 270
                    distance = 0.5
                    rotation = 180
                # 60 degrees / long arc
                case ["ne", "se"] | ["se", "ne"]:
                    direction = 0
                    distance = 0.23
                    rotation = 90
                case ["e", "sw"] | ["sw", "e"]:
                    direction = 60
                    distance = 0.23
                    rotation = 30
                case ["w", "se"] | ["se", "w"]:
                    direction = 120
                    distance = 0.23
                    rotation = -30
                case ["nw", "sw"] | ["sw", "nw"]:
                    direction = 180
                    distance = 0.23
                    rotation = 270
                case ["ne", "w"] | ["w", "ne"]:
                    direction = 240
                    distance = 0.23
                    rotation = 210
                case ["e", "nw"] | ["nw", "e"]:
                    direction = 300
                    distance = 0.23
                    rotation = 150
                # 90 degrees
                case ["ne", "sw"] | ["sw", "ne"]:
                    direction = 0
                    distance = 0
                    rotation = 60
                case ["e", "w"] | ["w", "e"]:
                    direction = 0
                    distance = 0
                    rotation = 0
                case ["nw", "se"] | ["se", "nw"]:
                    direction = 0
                    distance = 0
                    rotation = 300
        return direction, distance, rotation

    def track(
        self,
        location: str = None,
        position: str = None,
        stroke: object = None,
        label: str = None,
        town: str = None,
        **kwargs,
    ):
        """Draw track between hexsides at hex location(s).

        Args:
            location (str): grid reference or references for one or more cells
            position (str): hex edge compass reference or references
            stroke: the name of a color (defaults to self.barrier)
            label (str): the text to be drawn above/below the line
            town (str): position of a town "block" on the track; middle, start or end
        """
        from protograf.protos import Hexagon, Rectangle

        _locations = self.process_locations(location, "track")
        if position is None:
            position = []
        _positions = tools.split(position, separator=" ", clean=True, no_blanks=True)
        paths = []
        perbii = ""
        for _loc in _locations:
            geo = self.cells.get(_loc)
            for edges in _positions:
                start, end = None, None
                if "," in edges:
                    start, end = tools.split(edges, separator=",", clean=True)
                else:
                    start, end = edges, ""
                # ---- validate allowed track directions
                if self.orientation == HexOrientationName.POINTY.value:
                    allowed = ["ne", "e", "se", "sw", "w", "nw", ""]
                    if start not in allowed or end not in allowed:
                        feedback(
                            f"The track start and end must be chosen from '{allowed}';",
                            f" the option '{edges}' is not allowed.",
                            True,
                            True,
                        )
                elif self.orientation == HexOrientationName.FLAT.value:
                    allowed = ["n", "ne", "se", "s", "sw", "nw", ""]
                    if start not in allowed or end not in allowed:
                        feedback(
                            f"The track start and end must be chosen from '{allowed}';",
                            f" the option '{edges}' is not allowed.",
                            True,
                            True,
                        )
                if start and end:
                    paths.append(f"{start} {end}")
                elif start:
                    perbii = perbii + " " + start
                if paths:
                    hxw = Hexagon(  # underlying white
                        cxy=geo.centre,
                        height=XX18_HEX_HEIGHT,
                        fill=None,
                        stroke="black",
                        stroke_width=0.1,
                        orientation=self.orientation,
                        paths_stroke="white",
                        paths_stroke_width=XX18_TRACK_WIDTH_OUTER * self.units,
                        paths=paths,
                        perbii=perbii,
                        perbii_stroke="white",
                        perbii_stroke_width=XX18_TRACK_WIDTH_OUTER * self.units,
                        **kwargs,
                    )
                    # ---- town-on-track
                    if town:
                        direction, distance, rotation = (
                            self.process_track_town_position(hxw, [start, end])
                        )
                        ccentre = self.feature_location(geo, direction, distance)
                        label_position = kwargs.get("label_position", "above")
                        lwargs = self.process_label(
                            label, label_position, XX18_TOWN_DIAMETER / 2.0
                        )
                        Rectangle(
                            cxy=ccentre,
                            height=XX18_TOWN_HEIGHT_OUTER,
                            width=XX18_TOWN_WIDTH_OUTER,
                            fill_stroke="white",
                            stroke_width=XX18_STROKE_WIDTH,
                            rotation=rotation,
                            **{**kwargs, **lwargs},
                        )
                    Hexagon(  # overlying black
                        cxy=geo.centre,
                        height=XX18_HEX_HEIGHT,
                        fill=None,
                        stroke="black",
                        stroke_width=0.1,
                        orientation=self.orientation,
                        paths_stroke="black",
                        paths_stroke_width=XX18_TRACK_WIDTH_INNER * self.units,
                        paths=paths,
                        perbii=perbii,
                        perbii_stroke="black",
                        perbii_stroke_width=XX18_TRACK_WIDTH_INNER * self.units,
                        **kwargs,
                    )
                    if town:
                        Rectangle(
                            cxy=ccentre,  # as set for white above
                            height=XX18_TOWN_HEIGHT,
                            width=XX18_TOWN_WIDTH,
                            fill_stroke="black",
                            stroke_width=XX18_STROKE_WIDTH,
                            rotation=rotation,  # as set for white above
                            **kwargs,
                        )
                else:
                    feedback(
                        f"The track '{position}' for '{location}' cannot be drawn;",
                        " please check the directions used.",
                        False,
                        alert=True,
                    )

    def town(
        self,
        location: str = None,
        label: str = None,
        direction: float = None,
        distance: float = None,
        border: bool = False,
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
            label_position = kwargs.get("label_position", "below")
            lwargs = self.process_label(label, label_position, XX18_TOWN_DIAMETER / 2.0)
            # ---- circle
            if border:
                Circle(
                    cxy=ccentre,
                    radius=XX18_TOWN_DIAMETER_BORDER / 2.0,
                    fill_stroke="white",
                    stroke_width=XX18_STROKE_WIDTH,
                )
            Circle(
                cxy=ccentre,
                radius=XX18_TOWN_DIAMETER / 2.0,
                fill_stroke="black",
                stroke_width=XX18_STROKE_WIDTH,
                **{**kwargs, **lwargs},
            )

    def city(
        self,
        location: str = None,
        label: str = None,
        direction: float = None,
        distance: float = None,
        count: str | int = None,
        shape: str = None,
        **kwargs,
    ):
        """Draw City shape at hex location(s).

        Args:
            location (str): grid reference or references for one or more cells
            label (str): the name of the city
            direction (float): degrees clockwise from East
            distance (float): distance from hex centre
            count (str|int): number of circles in the city
            shape (Shape): the shape to be drawn inside the city
        """
        from protograf.protos import Circle, Rectangle, Triangle, Polyshape

        _locations = self.process_locations(location, "city")
        _radius = XX18_CITY_DIAMETER / 2.0
        if count:
            city_count = tools.as_int(count, "city count", maximum=6, minimum=1)
        else:
            city_count = 1
        for _loc in _locations:
            geo = self.cells.get(_loc)
            ccentre = self.feature_location(geo, direction, distance)
            label_position = kwargs.get("label_position", "below")
            if city_count > 1:
                if label_position not in ["above", "below"]:
                    label_position = "below"
            lwargs = self.process_label(label, label_position, _radius, "medium")
            cwargs = {}
            cwargs["radius"] = _radius
            cwargs["fill"] = "white"
            cwargs["stroke"] = "black"
            cwargs["stroke_width"] = XX18_STROKE_WIDTH
            cwargs["centre_shape"] = shape
            match city_count:
                # ---- city 1
                case 1:
                    Circle(
                        cxy=ccentre,
                        **{**kwargs, **lwargs, **cwargs},
                    )
                # ---- city 1
                case 2:
                    ccentre = geo
                    cw = ccentre.centre.x - _radius
                    ce = ccentre.centre.x + _radius
                    Rectangle(
                        height=XX18_CITY_DIAMETER,
                        width=XX18_CITY_DIAMETER,
                        cx=ccentre.centre.x,
                        cy=ccentre.centre.y,
                        fill="white",
                        stroke="black",
                        stroke_width=XX18_STROKE_WIDTH,
                        **{**kwargs, **lwargs},
                    )
                    Circle(
                        cx=cw,
                        cy=geo.centre.y,
                        **{**kwargs, **cwargs},
                    )
                    Circle(
                        cx=ce,
                        cy=geo.centre.y,
                        **{**kwargs, **cwargs},
                    )
                # ---- city 3
                case 3:
                    ccentre = geo
                    rwargs = {}
                    rwargs["fill"] = "white"
                    rwargs["stroke"] = "black"
                    rwargs["stroke_width"] = XX18_STROKE_WIDTH
                    # fill background
                    tri = Triangle(
                        cx=geo.centre.x,
                        cy=geo.centre.y,
                        side=XX18_CITY_DIAMETER,
                        **{**kwargs, **rwargs},
                    )
                    csw = tri.geo.sw
                    cse = tri.geo.se
                    cn = tri.geo.n
                    Polyshape(
                        x=cn.x,
                        y=cn.y,
                        snail=f"a30 {_radius} r90 {XX18_CITY_DIAMETER} r90 {_radius} r90 {XX18_CITY_DIAMETER}",
                        **{**kwargs, **rwargs},
                    )
                    Polyshape(
                        x=cn.x,
                        y=cn.y,
                        snail=f"a150 {_radius} l90 {XX18_CITY_DIAMETER} l90 {_radius} l90 {XX18_CITY_DIAMETER}",
                        **{**kwargs, **rwargs},
                    )
                    # label below csw-cse rectangle
                    Rectangle(
                        height=_radius,
                        width=XX18_CITY_DIAMETER,
                        x=csw.x,
                        y=csw.y,
                        # title=label,
                        **{**kwargs, **lwargs, **rwargs},
                    )
                    # draw city circles
                    Circle(
                        cxy=cn,
                        **{**kwargs, **cwargs},
                    )
                    Circle(
                        cxy=cse,
                        **{**kwargs, **cwargs},
                    )
                    Circle(
                        cxy=csw,
                        **{**kwargs, **cwargs},
                    )
                # ---- city 4
                case 4:
                    ccentre = geo
                    cx1 = ccentre.centre.x - _radius
                    cy1 = ccentre.centre.y - _radius
                    cx2 = ccentre.centre.x + _radius
                    cy2 = ccentre.centre.y - _radius
                    cx3 = ccentre.centre.x + _radius
                    cy3 = ccentre.centre.y + _radius
                    cx4 = ccentre.centre.x - _radius
                    cy4 = ccentre.centre.y + _radius
                    rwargs = {}
                    rwargs["fill"] = "white"
                    rwargs["stroke"] = "black"
                    rwargs["stroke_width"] = XX18_STROKE_WIDTH
                    Rectangle(
                        height=2 * XX18_CITY_DIAMETER,
                        width=XX18_CITY_DIAMETER,
                        cx=ccentre.centre.x,
                        cy=ccentre.centre.y,
                        **{**kwargs, **rwargs, **lwargs},
                    )
                    Rectangle(
                        height=XX18_CITY_DIAMETER,
                        width=2 * XX18_CITY_DIAMETER,
                        cx=ccentre.centre.x,
                        cy=ccentre.centre.y,
                        **{**kwargs, **rwargs},
                    )
                    Circle(
                        cx=cx1,
                        cy=cy1,
                        **{**kwargs, **cwargs},
                    )
                    Circle(
                        cx=cx2,
                        cy=cy2,
                        **{**kwargs, **cwargs},
                    )
                    Circle(
                        cx=cx3,
                        cy=cy3,
                        **{**kwargs, **cwargs},
                    )
                    Circle(
                        cx=cx4,
                        cy=cy4,
                        **{**kwargs, **cwargs},
                    )
                case _:
                    feedback(
                        f"Unable to draw a City of size '{city_count}';",
                        " choose from sizes 1, 2, 3 or 4",
                        True,
                        True,
                    )

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

    def spike(
        self,
        location: str = None,
        position: str = None,
        stroke: object = None,
        size: str = None,
        **kwargs,
    ):
        """Draw thin inset triangle(s) on hexside(s) at hex location(s).

        Args:
            location (str): grid reference or references for one or more cells
            position (str): hex edge compass reference or references
            stroke: the name of a color (defaults to white)
            size (str): short, medium or long (defaults to medium)
        """
        from protograf.protos import Hexagon

        if size:
            if _lower(size) not in [
                "short",
                "medium",
                "long",
                "s",
                "m",
                "l",
            ]:
                feedback(
                    f'"{size}" is an invalid size - choose short, medium or long.',
                    True,
                    True,
                )
        else:
            size = "medium"

        _locations = self.process_locations(location, "spike")
        if position is None:
            if self.orientation == HexOrientationName.POINTY.value:
                position = ["ne", "e", "se", "sw", "w", "nw"]
            elif self.orientation == HexOrientationName.FLAT.value:
                position = ["n", "ne", "se", "s", "sw", "nw"]
        _positions = tools.split(position, separator=" ", clean=True)
        stroke = stroke if stroke else "white"
        stroke_color = colrs.get_color(stroke)
        height_shrink = XX18_TRACK_WIDTH_OUTER - XX18_TRACK_WIDTH_INNER
        match _lower(size):
            case "short" | "s":
                height = XX18_HEX_DIAMETER * 0.1
            case "medium" | "m":
                height = XX18_HEX_DIAMETER * 0.25
            case "long" | "l":
                height = XX18_HEX_DIAMETER * 0.5
        for _loc in _locations:
            geo = self.cells.get(_loc)
            Hexagon(
                cxy=geo.centre,
                height=XX18_HEX_HEIGHT,
                fill=None,
                stroke="black",
                stroke_width=0.1,
                orientation=self.orientation,
                spikes=_positions,
                spikes_stroke="white",
                spikes_fill="white",
                spikes_width=XX18_TRACK_WIDTH_OUTER,
                spikes_height=-height,
            )
            Hexagon(
                cxy=geo.centre,
                height=XX18_HEX_HEIGHT,
                fill=None,
                stroke="black",
                stroke_width=0.1,
                orientation=self.orientation,
                spikes=_positions,
                spikes_stroke="black",
                spikes_fill="black",
                spikes_width=XX18_TRACK_WIDTH_INNER,
                spikes_height=-(height - height_shrink),
            )

    def block(
        self,
        location: str = None,
        position: str = None,
        stroke: object = None,
        label: str = None,
        **kwargs,
    ):
        """Draw thick line on hexside(s) at hex location(s).

        Args:
            location (str): grid reference or references for one or more cells
            position (str): hex edge compass reference or references
            stroke: the name of a color (defaults to self.barrier)
            label (str): the text to be drawn above/below the line
        """
        from protograf.protos import Line

        _locations = self.process_locations(location, "block")
        if position is None:
            if self.orientation == HexOrientationName.POINTY.value:
                position = ["ne", "e", "se", "sw", "w", "nw"]
            elif self.orientation == HexOrientationName.FLAT.value:
                position = ["n", "ne", "se", "s", "sw", "nw"]
        _positions = tools.split(position, separator=" ", clean=True)
        edge_color = colrs.get_color(stroke) if stroke else self.barrier_hex
        for _loc in _locations:
            geo = self.cells.get(_loc)
            for edge in _positions:
                start, end = None, None
                if self.orientation == HexOrientationName.POINTY.value:
                    match _lower(edge):
                        case "ne":
                            start = geo.n
                            end = geo.ne
                        case "e":
                            start = geo.ne
                            end = geo.se
                        case "se":
                            start = geo.se
                            end = geo.s
                        case "sw":
                            start = geo.s
                            end = geo.sw
                        case "w":
                            start = geo.sw
                            end = geo.nw
                        case "nw":
                            start = geo.nw
                            end = geo.n
                        case _:
                            feedback(
                                f'The block line position "{position}" is not a valid one.',
                                True,
                                True,
                            )
                elif self.orientation == HexOrientationName.FLAT.value:
                    match _lower(edge):
                        case "n":
                            start = geo.nw
                            end = geo.ne
                        case "ne":
                            start = geo.ne
                            end = geo.e
                        case "se":
                            start = geo.e
                            end = geo.se
                        case "s":
                            start = geo.se
                            end = geo.sw
                        case "sw":
                            start = geo.sw
                            end = geo.w
                        case "nw":
                            start = geo.w
                            end = geo.nw
                        case _:
                            feedback(
                                f'The block line position "{position}" is not a valid one.',
                                True,
                                True,
                            )
                if start and end:
                    Line(xy=start, xy1=end, stroke=edge_color, stroke_width=7, **kwargs)

    def tile_letter(
        self,
        location: str = None,
        label: str = None,
        direction: float = None,
        distance: float = None,
        **kwargs,
    ):
        """Draw Tile Letter at hex location(s).

        Args:
            location (str): grid reference or references for one or more cells
            label (str): the character for the tile letter
            direction (float): degrees clockwise from East
            distance (float): distance from hex centre
        """
        from protograf.protos import Text

        _locations = self.process_locations(location, "revenue")
        for _loc in _locations:
            geo = self.cells.get(_loc)
            ccentre = self.feature_location(geo, direction, distance)
            letter = label if label else ""
            Text(
                text=letter,
                xy=ccentre,
                stroke="black",
                stroke_width=XX18_STROKE_WIDTH,
                font_size=XX18_TEXT_EXTRA,
                font_name=XX18_TEXT_FONT_BOLD,
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
            label_position = kwargs.get("label_position", "below")
            lwargs = self.process_label(
                label, label_position, XX18_MOUNTAIN_SIDE / 2.0, "small"
            )
            Triangle(
                cx=ccentre.x,
                cy=ccentre.y,
                side=XX18_MOUNTAIN_SIDE,
                stroke_width=XX18_STROKE_WIDTH,
                fill="black",
                **{**kwargs, **lwargs},
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
                # label_size=XX18_TEXT_SMALL,
            )
            pce = Circle(
                cxy=ccentre1,
                radius=XX18_PRIVATE_DIAMETER / 2.0,
                fill=None,
                stroke="black",
                stroke_width=XX18_STROKE_WIDTH,
                # label=label if label else "",
                # label_size=XX18_TEXT_SMALL,
            )
            Line(
                links=[pcs, pce],
                stroke="black",
                stroke_width=XX18_STROKE_WIDTH,
            )

        if label:
            print("TODO - label for Private")

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
            case "factry":
                _file = files("protograf").joinpath(f"{XX18_RESOURCES}/factory.svg")
            case "fish":
                _file = files("protograf").joinpath(f"{XX18_RESOURCES}/fish.svg")
            case "flag":
                _file = files("protograf").joinpath(f"{XX18_RESOURCES}/flag.svg")
            case "forest":
                _file = files("protograf").joinpath(f"{XX18_RESOURCES}/forest.svg")
            case "lock":
                _file = files("protograf").joinpath(f"{XX18_RESOURCES}/lock.svg")
            case "noentry":
                _file = files("protograf").joinpath(f"{XX18_RESOURCES}/noentry.svg")
            case "pennant":
                _file = files("protograf").joinpath(f"{XX18_RESOURCES}/pennant.svg")
            case "train":
                _file = files("protograf").joinpath(f"{XX18_RESOURCES}/train.svg")
            case "tree":
                _file = files("protograf").joinpath(f"{XX18_RESOURCES}/tree.svg")
            case "tunnel":
                _file = files("protograf").joinpath(f"{XX18_RESOURCES}/tunnel.svg")

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
            label_position = kwargs.get("label_position", "below")
            offset = 0.5
            lwargs = self.process_label(label, label_position, offset, "small")
            Image(_file, cxy=ccentre, **{**kwargs, **lwargs})
