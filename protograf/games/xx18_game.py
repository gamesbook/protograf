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
* depiction of cities (different sizes) as open circles; may include
  the railroad logo or a custom shape or text inset into it
* depiction of revenue as circle with an amount
* depiction of track, curved or straight
* depiction of track extending from a city
* depiction of terminal spikes running off-board (short, medium and long)
* depiction of blocked hex-sides as thick lines
* depiction of highlighted hex as a yellow band inside of all hex edges
* depiction of private railways; either in-hex or across hexes
* depiction of icons for common in-hex features; including mountains
  (two sizes), hills, and rivers
* depiction of symbols for special features such as: coal, desert, factory,
  fish, flag, forest, hills, lock, mine, noentry, oil, pennant, port,
  swamp, train, tree, tunnel
* depiction of a river; as "wavy line"; running through a hex
* depiction of a custom shape in a hex
* display of a single piece of text
* display of hex coordinates along the edges of the map (above, below,
  left-of, and right-of)
* coloring ("fill") of a whole hex
* creation of a small, multi-line, colored table to appear in an off-board
  hexagon or area (showing revenue per phase of the game)

The blueprint will also provide:

* standard, named 18xx colors
* ability to set the map font names & sizes; or colors to use
* ability to put labels next to icons, symbols, towns or cities
  (above, below, left-of, right-of)

In-hex features, for example, cities, towns, icons, symbols or lettering will,
by default, appear at the centre of a hex. These can be repositioned using a
combination of direction (in degrees clockwise from east) and distance (as a
fraction of the hex radius).

Positioning of features, such as lines, spikes, bumps or numbered circles, on
hex edges will be done using standard compass directions; "ne" for northeast,
"s" for south, etc., and will be centred on that edge.

Drawing will be done following the order in which features are provided.

Setting of an off-board, colored, rectangular, or polyshape area - typically
red and extending from the edge of the board hexagons - is not handled
directly by XX18Game.  There is too much variation in how such areas are
drawn to use a common formulae.  What is possible is to use the cell grid
references and hexagon geometry to set the vertices of such shapes relative
to the board.

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
Map Background     #EAEAEA  Neutral light gray to offset active hexes
Plain Hex (Base)   #FFFFFF  Stark white or a pale off-white (#F9F9F9)
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
import math

# third party

# module
from protograf import globals
from protograf.base import BaseShape
from protograf.utils import tools, colrs, geoms

# from protograf.utils.constants import GRID_SHAPES_WITH_CENTRE
from protograf.utils.messaging import feedback
from protograf.utils.structures import (  # named tuples; enums
    AbstractBoardType,
    RelativeLocation,
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
XX18_PHASE_REVENUE_BOX = 0.7  # cm
XX18_STROKE_WIDTH = 1
XX18_STROKE_WIDTH_HIGHLIGHT = 8
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
XX18_TILE_GREY = "#7F8C8D"
XX18_TILE_YELLOW_MF = "#F1C40F"
XX18_TILE_GREEN_MF = "#27AE60"
XX18_TILE_BROWN_MF = "#7E5109"
XX18_TILE_GRAY_MF = "#95A5A6"
XX18_TILE_GREY_MF = "#95A5A6"
XX18_HEX_BACK = "#EAEAEA"
XX18_HEX_PLAIN = "#FFFFFF"
XX18_HEX_PLAIN_OFF = "#F9f9f9"
XX18_HEX_YELLOW = "#F1E351"
XX18_HEX_GREEN = "#4CAF50"
XX18_HEX_BROWN = "#8D6E63"
XX18_HEX_GRAY = "#B0BEC5"
XX18_HEX_GREY = "#B0BEC5"
XX18_HEX_BARRIER = "#757575"
XX18_HEX_OFFBOARD = "#EF5350"
XX18_HEX_WATER = "#4A7F9D"
XX18_HEX_RIVER = "#01A0D6"
XX18_HEX_SEA = "#C1E6FD"

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
    "phase_revenue",
    "tile_letter",
    "tile-letter",
    "fill",
    "highlight",
    "block",
    "spike",
    "track",
    "track_town",
    "river_line",
]


class XX18GameObject(CoreGameObject):
    """Create a XX18GameObject for a given canvas."""

    def __init__(self, _object=None, canvas=None, **kwargs):
        super().__init__(_object=_object, canvas=canvas, **kwargs)
        # ---- class props
        self.features = self._commons("features") or kwargs.get("features") or []
        self.debug = self._commons("debug") or kwargs.get("debug") or False
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
            feedback(
                f'Invalid orientation "{self.orientation}" for XX18Game;'
                ' choose from "flat" or "pointy".',
                True,
                True,
            )
        # ---- labels
        self.label_locations = []
        _label_locations = (
            self._commons("label_locations") or kwargs.get("label_locations") or ""
        )
        if not _label_locations:
            _label_locations = ""  # avoid invalid, non-string
        if not _label_locations and self.label is True:
            _label_locations = "AL"  # set default
        try:
            if "A" in _label_locations or "a" in _label_locations:
                self.label_locations.append(RelativeLocation.ABOVE.value)
            if "L" in _label_locations or "l" in _label_locations:
                self.label_locations.append(RelativeLocation.LEFT.value)
            if "B" in _label_locations or "b" in _label_locations:
                self.label_locations.append(RelativeLocation.BELOW.value)
            if "R" in _label_locations or "r" in _label_locations:
                self.label_locations.append(RelativeLocation.RIGHT.value)
        except (TypeError, ValueError):
            feedback(
                f'Invalid label_locations "{_label_locations}" for XX18Game;'
                " this should be a string with any or all of A, L, B, or R.",
                True,
                True,
            )
        # ---- offset
        if self.hex_offset not in ["odd", "even"]:
            feedback(
                f'Invalid hex_offset "{self.hex_offset}" for XX18Game;'
                ' choose from "odd" or "even".',
                True,
                True,
            )
        # ---- fonts
        self.label_font = (
            self._commons("label_font") or kwargs.get("label_font") or XX18_TEXT_FONT
        )
        # ---- add in defaults
        if not self.rows:
            self.rows = 8
        if not self.cols:
            self.cols = 8
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
        self.sea_hex = XX18_HEX_SEA
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

    def _validate_choices(self) -> bool:
        """Check and reset user choices for valid selections."""
        return True

    def draw_debug_labels(self):
        """Draw Hexagon labels overlays"""
        from protograf.protos import Text

        def get_label(row, col):
            for key, locale in enumerate(self.board_layout.locales):
                if locale.col == col and locale.row == row:
                    return self.board_layout.locales[key].label

        if not self.debug:
            return

        lkeys = {}
        LSIZE = XX18_HEX_SIDE * self.units * 0.75
        lkeys["font_name"] = "Helvetica"
        lkeys["font_size"] = LSIZE
        lkeys["stroke"] = self.debug_color
        lkeys["stroke_transparency"] = 50
        lkeys["align"] = "centre"

        end_col, end_row = self.cols + 1, self.rows + 1
        for col_no in range(1, end_col):
            for row_no in range(1, end_row):
                cell = self.board_layout.cells[(col_no, row_no)]
                label = get_label(row_no - 1, col_no - 1)
                Text(label, x=cell.c.x, y=cell.c.y + LSIZE / self.units / 2.5, **lkeys)

    def draw_labels(self):
        """Draw row and column labels at the board edges."""
        from protograf.protos import Text

        if not self.label:
            return

        # ---- label settings
        end_col, end_row = self.cols + 1, self.rows + 1
        _label_col = self._p2v(self.label_size) * 0.5  # user-units
        _label_row = self._p2v(self.label_size) * 0.75  # user-units
        lbl_offset = self.label_offset if self.label_offset else None
        if lbl_offset:
            _label_col, _label_col = lbl_offset, lbl_offset
        else:
            _label_col = self._p2v(self.label_size) * 0.5  # user-units
            _label_row = self._p2v(self.label_size) * 0.75  # user-units
        lbl_offset_col = self.label_offset_col if self.label_offset_col else _label_col
        lbl_offset_row = self.label_offset_row if self.label_offset_row else _label_row
        lkeys = {}
        lkeys["font_name"] = self.label_font
        lkeys["font_size"] = self.label_size
        lkeys["stroke"] = self.label_stroke
        lkeys["align"] = "centre"
        font_offset = self.label_size / self.units / 2.0

        # ---- POINTY grid
        if self.orientation == HexOrientationName.POINTY.value:
            # ---- * column labels
            for col_no in range(1, end_col):
                col_value = 2 * col_no - 1
                if RelativeLocation.ABOVE.value in self.label_locations:
                    cell = self.board_layout.cells[(col_no, 1)]
                    # first label
                    x = cell.n.x if self.hex_offset == "even" else cell.nw.x
                    y = cell.n.y - lbl_offset_col
                    Text(str(col_value), x=x, y=y, **lkeys)
                    # second label
                    x = cell.ne.x if self.hex_offset == "even" else cell.n.x
                    y = cell.n.y - lbl_offset_col
                    Text(str(col_value + 1), x=x, y=y, **lkeys)
                if RelativeLocation.BELOW.value in self.label_locations:
                    cell = self.board_layout.cells[(col_no, self.rows)]
                    # first label
                    x = cell.s.x if self.hex_offset == "even" else cell.sw.x
                    y = cell.s.y + lbl_offset_col + font_offset
                    Text(str(col_value), x=x, y=y, **lkeys)
                    # second label
                    x = cell.se.x if self.hex_offset == "even" else cell.s.x
                    y = cell.s.y + lbl_offset_col + font_offset
                    Text(str(col_value + 1), x=x, y=y, **lkeys)
            # ---- * row labels
            for row_no in range(1, end_row):
                row_value = tools.alpha_column(row_no, lower=False)
                if RelativeLocation.LEFT.value in self.label_locations:
                    cell = self.board_layout.cells[(1, row_no)]
                    if self.even(row_no) and self.hex_offset == "even":
                        x = cell.w.x - lbl_offset_row - self.cell_size / 2.0
                    elif self.odd(row_no) and self.hex_offset == "odd":
                        x = cell.w.x - lbl_offset_row - self.cell_size / 2.0
                    else:
                        x = cell.w.x - lbl_offset_row
                    y = cell.w.y
                    Text(row_value, x=x, y=y, **lkeys)
                if RelativeLocation.RIGHT.value in self.label_locations:
                    cell = self.board_layout.cells[(self.cols, row_no)]
                    if self.odd(row_no) and self.hex_offset == "even":
                        x = cell.e.x + lbl_offset_row + self.cell_size / 2.0
                    elif self.even(row_no) and self.hex_offset == "odd":
                        x = cell.e.x + lbl_offset_row + self.cell_size / 2.0
                    else:
                        x = cell.e.x + lbl_offset_row
                    y = cell.e.y
                    Text(row_value, x=x, y=y, **lkeys)

        # ---- FLAT grid
        elif self.orientation == HexOrientationName.FLAT.value:
            # ---- * column labels
            for col_no in range(1, end_col):
                col_value = tools.alpha_column(col_no, lower=False)
                if RelativeLocation.ABOVE.value in self.label_locations:
                    cell = self.board_layout.cells[(col_no, 1)]
                    x = cell.n.x
                    if self.even(col_no) and self.hex_offset == "even":
                        y = cell.n.y - lbl_offset_col - self.cell_size / 2.0
                    elif self.odd(col_no) and self.hex_offset == "odd":
                        y = cell.n.y - lbl_offset_col - self.cell_size / 2.0
                    else:
                        y = cell.n.y - lbl_offset_col
                    Text(col_value, x=x, y=y, **lkeys)
                if RelativeLocation.BELOW.value in self.label_locations:
                    cell = self.board_layout.cells[(col_no, self.rows)]
                    x = cell.n.x
                    if self.odd(col_no) and self.hex_offset == "even":
                        y = (
                            cell.s.y
                            + lbl_offset_col
                            + self.cell_size / 2.0
                            + font_offset
                        )
                    elif self.even(col_no) and self.hex_offset == "odd":
                        y = (
                            cell.s.y
                            + lbl_offset_col
                            + self.cell_size / 2.0
                            + font_offset
                        )
                    else:
                        y = cell.s.y + lbl_offset_col + font_offset
                    Text(col_value, x=x, y=y, **lkeys)
            # ---- * row labels
            for row_no in range(1, end_row):
                row_value = 2 * row_no - 1
                if RelativeLocation.LEFT.value in self.label_locations:
                    cell = self.board_layout.cells[(1, row_no)]
                    # first label
                    x = cell.w.x
                    y = (
                        cell.w.y + font_offset
                        if self.hex_offset == "even"
                        else cell.nw.y + font_offset
                    )
                    x = x - lbl_offset_row
                    Text(str(row_value), x=x, y=y, **lkeys)
                    # second label
                    x = cell.w.x
                    y = (
                        cell.sw.y + font_offset
                        if self.hex_offset == "even"
                        else cell.w.y + font_offset
                    )
                    x = x - lbl_offset_row
                    Text(str(row_value + 1), x=x, y=y, **lkeys)
                if RelativeLocation.RIGHT.value in self.label_locations:
                    cell = self.board_layout.cells[(self.cols, row_no)]
                    # first label
                    x = cell.e.x
                    y = (
                        cell.ne.y + font_offset
                        if self.hex_offset == "even"
                        else cell.e.y + font_offset
                    )
                    x = x + lbl_offset_row
                    Text(str(row_value), x=x, y=y, **lkeys)
                    # second label
                    x = cell.e.x
                    y = (
                        cell.e.y + font_offset
                        if self.hex_offset == "even"
                        else cell.se.y + font_offset
                    )
                    x = x + lbl_offset_row
                    Text(str(row_value + 1), x=x, y=y, **lkeys)

    def set_locale_label(self, row: int, col: int, label: str):
        """Set a locale label attribute for the board's locales."""
        for key, locale in enumerate(self.board_layout.locales):
            if locale.col == col and locale.row == row:
                self.board_layout.locales[key] = self.board_layout.locales[
                    key
                ]._replace(label=label)
                break

    def setup_board(self):
        """Create board_layout for the required grid"""
        from protograf.protos import Hexagons

        # ---- game-based defaults
        # Point(top_x, top_x) is the top-left point of the VirtualLocations (grid points)
        top_x = self.x if self.kwargs.get("x") else 0
        top_y = self.y if self.kwargs.get("y") else 0
        hex_color = self.fill if (self.fill or self.fill is None) else self.plain_hex
        x_offset = 0
        # x_offset = -0.5 * self.cell_size
        self.board_layout = Hexagons(
            cols=self.cols,
            rows=self.rows,
            x=top_x + x_offset,
            y=top_y,
            hex_offset=self.hex_offset,
            orientation=self.orientation,  # default: pointy
            _draw_grid=False,
            pattern=self.pattern,
            user=f"{self.game_class}",
            # single hexagon properties:-
            height=self.cell_size,
            stroke=self.stroke,
            stroke_width=XX18_STROKE_WIDTH,
            fill=hex_color,
            debug=self.debug,
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
                    self.set_locale_label(row - 1, col - 1, cell_id)
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
            * The feature (tuple) can contain in this order:
                  * cellID (str): the alphanumeric grid coordinate of the hex
                  * position (tuple | str):
                      either a tuple of
                        direction (float): optional, degrees
                        distance (float): optional, fraction
                      or a string of:
                        hex-side directions
                      or None
                  * label (str): a label for the feature or symbol (default "")
                  * label_location (str): the position for label
                    (above, below, left, right)
                  * shapes (BaseShape): a list of one or more shape to be drawn
                    inside the feature; usually inside a city or, if multiple items
                    in the list, one shape per city circle in a compound city -
                    this could be to add color, or text or an Image e.g. a logo

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
        fhexagon = feature[0]
        self.process_locations(fhexagon)  # sanity check
        # ---- feature property values
        kwargs = {}
        ftype = feature[1]
        if ftype not in XX18_FEATURE_SET and not isinstance(ftype, BaseShape):
            feedback(
                f"The feature '{ftype}' is not available; "
                f"choose from: \n{XX18_FEATURE_SET} or supply a shape.",
                True,
                True,
            )
        flabel, flabel_loc, fdirection, fdistance, fshapes = "", None, None, None, []
        if len(feature) >= 3:
            fdirection, fdistance = self.feature_position(feature[2])
        if len(feature) >= 4:
            flabel = str(feature[3])
        if len(feature) >= 5 and ftype != "private":  # see below; private overloads
            kwargs["label_location"] = feature[4]
        if len(feature) >= 6 and ftype != "private":  # see below; private overloads
            fshapes = feature[5]
            if not isinstance(fshapes, (tuple, list)):
                feedback(
                    f"The setting '{fshapes}' for {fhexagon} must be a list.",
                    True,
                    True,
                )
            for fshape in fshapes:
                if fshape is not None and not isinstance(fshape, BaseShape):
                    feedback(
                        f"The item '{fshape}' in the list for {fhexagon} is not a "
                        "protograf shape.",
                        True,
                        True,
                    )

        # print(f"&&& {fhexagon=} {ftype=} {fdirection=} {fdistance=} {flabel=} ")
        # ---- feature to function
        feature_type = ftype
        if ftype in XX18_SYMBOL_SET:
            feature_type = "SYMBOL"
        if isinstance(ftype, BaseShape):
            feature_type = "SHAPE"
        match feature_type:
            case "fill":
                self.fill_hex(
                    location=fhexagon,
                    color=flabel,
                    **kwargs,
                )
            case "highlight":
                self.highlight(
                    location=fhexagon,
                    color=flabel,
                    **kwargs,
                )
            case "city" | "cityx1" | "cityx2" | "cityx3" | "cityx4":
                if "x" in ftype:
                    _, count = ftype.split("x")
                else:
                    count = 1
                self.city(
                    location=fhexagon,
                    label=flabel,
                    direction=fdirection,
                    distance=fdistance,
                    count=count,
                    shapes=fshapes,
                    **kwargs,
                )
            case "town":
                self.town(
                    location=fhexagon,
                    label=flabel,
                    direction=fdirection,
                    distance=fdistance,
                    **kwargs,
                )
            case "town_border":
                self.town(
                    location=fhexagon,
                    label=flabel,
                    direction=fdirection,
                    distance=fdistance,
                    border=True,
                    **kwargs,
                )
            case "track":
                self.track(
                    location=fhexagon,
                    label=flabel,
                    position=fdirection,
                    **kwargs,
                )
            case "track_town":
                self.track(
                    location=fhexagon,
                    label=flabel,
                    position=fdirection,
                    town="middle",  # ALL POSITIONS NOT OPERATIONAL
                    **kwargs,
                )
            case "river_line":
                self.river_line(
                    location=fhexagon,
                    position=fdirection,
                    stroke=None,  # TODO => how to set
                    breadth="medium",  # all thicknesses: medium/m; narrow/n; wide/w
                    **kwargs,
                )
            case "mountain":
                self.mountain(
                    location=fhexagon,
                    label=flabel,
                    direction=fdirection,
                    distance=fdistance,
                    **kwargs,
                )
            case "private":
                flocation1, fdirection1, fdistance1 = "", 0, 0
                if len(feature) >= 5:
                    flocation1 = str(feature[4])
                    if flocation1 in ["", None]:
                        flocation1 = fhexagon
                if len(feature) >= 6:
                    fdirection1, fdistance1 = self.feature_position(feature[5])
                if len(feature) >= 7:
                    kwargs["label_location"] = feature[6]
                # print(f"&&& private {flocation1=} {fdirection1=} {fdistance1=}")
                self.private(
                    label=flabel,
                    location=fhexagon,
                    direction=fdirection,
                    distance=fdistance,
                    location1=flocation1,
                    direction1=fdirection1,
                    distance1=fdistance1,
                    **kwargs,
                )
            case "revenue":
                self.revenue(
                    location=fhexagon,
                    label=flabel,
                    direction=fdirection,
                    distance=fdistance,
                    **kwargs,
                )
            case "phase_revenue":
                self.phase_revenue(
                    location=fhexagon,
                    income=flabel,
                    direction=fdirection,
                    distance=fdistance,
                    **kwargs,
                )
            case "tile_letter" | "tile-letter" | "tileletter":
                self.tile_letter(
                    location=fhexagon,
                    label=flabel,
                    direction=fdirection,
                    distance=fdistance,
                    **kwargs,
                )
            case "block":
                self.block(
                    location=fhexagon,
                    position=fdirection,
                    stroke=None,  # TODO => how to set
                    **kwargs,
                )
            case "spike":
                self.spike(
                    location=fhexagon,
                    size=flabel,
                    position=fdirection,
                    **kwargs,
                )
            case "SYMBOL":
                self.symbol(
                    location=fhexagon,
                    label=flabel,
                    direction=fdirection,
                    distance=fdistance,
                    name=ftype,
                    **kwargs,
                )
            case "SHAPE":
                self.figure(
                    location=fhexagon,
                    label=flabel,
                    direction=fdirection,
                    distance=fdistance,
                    thing=ftype,
                    **kwargs,
                )
            case _:
                feedback(
                    f"The feature '{ftype}' is not available; "
                    f"choose from: \n{XX18_FEATURE_SET} or supply a shape.",
                    True,
                    True,
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

    def relative_location(self, location: str = None) -> int:
        """Convert a string into a RelativeLocation value."""
        if not location:
            return None
        if not isinstance(location, str):
            feedback(
                "The location must be a string;",
                f" the option '{location}' is not allowed.",
                True,
                True,
            )
        match _lower(location):
            case "a" | "above":
                return RelativeLocation.ABOVE.value
            case "b" | "below":
                return RelativeLocation.BELOW.value
            case "l" | "left":
                return RelativeLocation.LEFT.value
            case "r" | "right":
                return RelativeLocation.RIGHT.value
            case _:
                feedback(
                    "The location must be one of A, B, L, R;",
                    f" the option '{location}' is not allowed.",
                    True,
                    True,
                )

    def process_label(
        self,
        label: str,
        location: RelativeLocation = RelativeLocation.BELOW.value,
        base_shift: float = 0.0,
        text_size: str = "medium",
    ) -> dict:
        """Create label properties for a feature or symbol."""
        kwargs = {}
        label_mx = 0.0
        heading, title, _label = "", "", ""
        label_align = "centre"
        match text_size:
            case "small" | "s":
                font_size = XX18_TEXT_SMALL
            case "medium" | "m":
                font_size = XX18_TEXT_MEDIUM
            case "large" | "l":
                font_size = XX18_TEXT_LARGE
            case "extra" | "e" | "x":
                font_size = XX18_TEXT_EXTRA
            case _:
                raise ValueError(
                    f'Text size "{text_size}" is not available for label processing.',
                )
        if label:
            shift = base_shift + self.label_size / self.units / 3.0
            match location:
                case RelativeLocation.ABOVE.value:
                    heading = label
                case RelativeLocation.BELOW.value:
                    title = label
                case RelativeLocation.LEFT.value:
                    _label = label
                    label_mx = -shift
                    label_align = "right"
                case RelativeLocation.RIGHT.value:
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
            offset: where on the path to draw the shape [TO BE DONE]

        Returns:
            tuple: direction (float), distance (float), rotation (float)
        """
        direction, distance, rotation = 0, 0, 0
        if hexagon.ORIENTATION == HexOrientation.FLAT:
            match path_pair:
                # 120 degrees / short arc
                case ["n", "ne"] | ["ne", "n"]:
                    direction = 300
                    distance = 0.5
                    rotation = 150
                case ["se", "ne"] | ["ne", "se"]:
                    direction = 0
                    distance = 0.5
                    rotation = 90
                case ["se", "s"] | ["s", "se"]:
                    direction = 60
                    distance = 0.5
                    rotation = 30
                case ["sw", "s"] | ["s", "sw"]:
                    direction = 120
                    distance = 0.5
                    rotation = 330
                case ["sw", "nw"] | ["nw", "sw"]:
                    direction = 180
                    distance = 0.5
                    rotation = 270
                case ["n", "nw"] | ["nw", "n"]:
                    direction = 240
                    distance = 0.5
                    rotation = 210
                # 60 degrees / long arc
                case ["n", "se"] | ["se", "n"]:
                    direction = 330
                    distance = 0.24
                    rotation = 300
                case ["ne", "s"] | ["s", "ne"]:
                    direction = 30
                    distance = 0.24
                    rotation = 60
                case ["se", "sw"] | ["sw", "se"]:
                    direction = 90
                    distance = 0.24
                    rotation = 0
                case ["s", "nw"] | ["nw", "s"]:
                    direction = 150
                    distance = 0.24
                    rotation = 300
                case ["sw", "n"] | ["n", "sw"]:
                    direction = 210
                    distance = 0.24
                    rotation = 60
                case ["nw", "ne"] | ["ne", "nw"]:
                    direction = 270
                    distance = 0.24
                    rotation = 0
                # 90 degrees
                case ["nw", "se"] | ["se", "nw"]:
                    direction = 0
                    distance = 0
                    rotation = 330
                case ["ne", "sw"] | ["sw", "ne"]:
                    direction = 0
                    distance = 0
                    rotation = 30
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
                if paths or perbii:
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
                        _label_loc = kwargs.get("label_location", "above")
                        relative_location = self.relative_location(_label_loc)
                        lwargs = self.process_label(
                            label, relative_location, XX18_TOWN_DIAMETER / 2.0
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

    def river_line(
        self,
        location: str = None,
        position: str = None,
        stroke: str = None,
        breadth: str = None,
        **kwargs,
    ):
        """Draw river path along/between hexsides starting at hex location(s).

        Args:
            location (str): grid reference or references for one or more cells
            position (str): hex compass reference(s) for the path
            stroke: the name of a color (defaults to self.river)
            breadth (str): thickness of the river line; medium/m; narrow/n; wide/w
        """
        from protograf.protos.proto_gridline import GridLine

        _locations = self.process_locations(location, "river_line")
        if position is None:
            position = []
        river_stroke = stroke or XX18_HEX_RIVER
        _positions = tools.split(position, separator=" ", clean=True, no_blanks=True)
        edges = ", ".join(_positions[1:])
        point = _positions[0]
        match breadth:
            case "narrow" | "n":
                _river_width = 2
            case "medium" | "m":
                _river_width = 4
            case "wide" | "w":
                _river_width = 6
        for _loc in _locations:
            GridLine(
                self.board_layout,
                start=_loc,
                point=point,
                edges=edges,
                stroke=river_stroke,
                stroke_width=_river_width,
                stroke_ends="rounded",
                wave_style="wave",
                wave_height=0.15,
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
            label (str): the name of the town
            direction (float): degrees clockwise from East
            distance (float): distance from hex centre
        """
        from protograf.protos import Circle

        _locations = self.process_locations(location, "town")
        for _loc in _locations:
            geo = self.cells.get(_loc)
            ccentre = self.feature_location(geo, direction, distance)
            label_location = kwargs.get("label_location", "below")
            relative_location = self.relative_location(label_location)
            lwargs = self.process_label(
                label, relative_location, XX18_TOWN_DIAMETER / 2.0
            )
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
        shapes: list = None,  # list of BaseShape
        **kwargs,
    ):
        """Draw City shape at hex location(s).

        Args:
            location (str): grid reference or references for one or more cells
            label (str): the name of the city
            direction (float): degrees clockwise from East
            distance (float): distance from hex centre
            count (str|int): number of circles in the city
            shapes (list): a list of shapes to be drawn inside the city circle(s)
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
            label_location = kwargs.get("label_location", "below")
            if city_count > 1:
                if label_location not in ["above", "below"]:
                    label_location = "below"
            relative_location = self.relative_location(label_location)
            lwargs = self.process_label(label, relative_location, _radius, "medium")
            cwargs = {}
            cwargs["radius"] = _radius
            cwargs["fill"] = "white"
            cwargs["stroke"] = "black"
            cwargs["stroke_width"] = XX18_STROKE_WIDTH
            cwargs["centre_shape"] = shapes
            match city_count:
                # ---- city 1
                case 1:
                    if shapes and len(shapes) > 0:
                        cwargs["centre_shape"] = shapes[0]
                    else:
                        cwargs["centre_shape"] = None
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
                    if shapes and len(shapes) > 0:
                        cwargs["centre_shape"] = shapes[0]
                    else:
                        cwargs["centre_shape"] = None
                    Circle(
                        cx=cw,
                        cy=geo.centre.y,
                        **{**kwargs, **cwargs},
                    )
                    if shapes and len(shapes) > 1:
                        cwargs["centre_shape"] = shapes[1]
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
                    if shapes and len(shapes) > 0:
                        cwargs["centre_shape"] = shapes[0]
                    else:
                        cwargs["centre_shape"] = None
                    Circle(
                        cxy=cn,
                        **{**kwargs, **cwargs},
                    )
                    if shapes and len(shapes) > 1:
                        cwargs["centre_shape"] = shapes[1]
                    else:
                        cwargs["centre_shape"] = None
                    Circle(
                        cxy=cse,
                        **{**kwargs, **cwargs},
                    )
                    if shapes and len(shapes) > 2:
                        cwargs["centre_shape"] = shapes[2]
                    else:
                        cwargs["centre_shape"] = None
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
                    if shapes and len(shapes) > 0:
                        cwargs["centre_shape"] = shapes[0]
                    else:
                        cwargs["centre_shape"] = None
                    Circle(
                        cx=cx1,
                        cy=cy1,
                        **{**kwargs, **cwargs},
                    )
                    if shapes and len(shapes) > 1:
                        cwargs["centre_shape"] = shapes[1]
                    else:
                        cwargs["centre_shape"] = None
                    Circle(
                        cx=cx2,
                        cy=cy2,
                        **{**kwargs, **cwargs},
                    )
                    if shapes and len(shapes) > 2:
                        cwargs["centre_shape"] = shapes[2]
                    else:
                        cwargs["centre_shape"] = None
                    Circle(
                        cx=cx3,
                        cy=cy3,
                        **{**kwargs, **cwargs},
                    )
                    if shapes and len(shapes) > 3:
                        cwargs["centre_shape"] = shapes[3]
                    else:
                        cwargs["centre_shape"] = None
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

        _locations = self.process_locations(location, "spike")
        if size:
            if not isinstance(size, str) or _lower(size) not in [
                "short",
                "medium",
                "long",
                "s",
                "m",
                "l",
            ]:
                feedback(
                    f'"{size}" is an invalid size for {_locations};'
                    " - use short, medium or long.",
                    True,
                    True,
                )
        else:
            size = "medium"

        if position is None:
            if self.orientation == HexOrientationName.POINTY.value:
                position = ["ne", "e", "se", "sw", "w", "nw"]
            elif self.orientation == HexOrientationName.FLAT.value:
                position = ["n", "ne", "se", "s", "sw", "nw"]
        _positions = tools.split(position, separator=" ", clean=True)
        stroke = stroke if stroke else "white"
        # stroke_color = colrs.get_color(stroke)
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
        **kwargs,
    ):
        """Draw thick line on hexside(s) at hex location(s).

        Args:
            location (str): grid reference or references for one or more cells
            position (str): hex edge compass reference or references
            stroke: the name of a color (defaults to self.barrier)
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

        _locations = self.process_locations(location, "tile_letter")
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

        _locations = self.process_locations(location, "fill_hex")
        if color:
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
        else:
            feedback("No color has been set for the hexagon fill!", alert=True)

    def highlight(
        self,
        location: str = None,
        color: object = None,
        **kwargs,
    ):
        """Draw an inner outline hexagon in color at hex location(s).

        Args:
            location (str): grid reference or references for one or more cells
            color (color): a color reference (default to 18XX yellow)
        """
        from protograf.protos import Hexagon

        _locations = self.process_locations(location, "highlight")
        _color = color if color else XX18_HEX_YELLOW
        the_color = colrs.get_color(_color)
        _height = XX18_HEX_HEIGHT - XX18_STROKE_WIDTH_HIGHLIGHT / self.units
        for _loc in _locations:
            geo = self.cells.get(_loc)
            ccentre = geo.centre
            Hexagon(
                cxy=ccentre,
                height=_height,
                fill=None,
                stroke=the_color,
                stroke_width=XX18_STROKE_WIDTH_HIGHLIGHT,
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

        _locations = self.process_locations(location, "mountain")
        for _loc in _locations:
            geo = self.cells.get(_loc)
            ccentre = self.feature_location(geo, direction, distance)
            label_location = kwargs.get("label_location", "below")
            relative_location = self.relative_location(label_location)
            lwargs = self.process_label(
                label, relative_location, XX18_MOUNTAIN_SIDE / 2.0, "small"
            )
            Triangle(
                cx=ccentre.x,
                cy=ccentre.y,
                side=XX18_MOUNTAIN_SIDE,
                stroke_width=XX18_STROKE_WIDTH,
                fill="black",
                **{**kwargs, **lwargs},
            )

    def phase_revenue(
        self,
        location: str = None,
        income: str = None,
        direction: float = None,
        distance: float = None,
        colors: list = None,
        orientation: str = "v",  # None,
        **kwargs,
    ):
        """Draw a Phase Revenue table at hex location(s).

        Args:
            location (str): grid reference or references for one or more cells
            income (str): the phase revenue incomes (two to four values)
            direction (float): degrees clockwise from East
            distance (float): distance from hex centre
            colors (list): the colors to use for the different incomes
            orientation (str):
                the table layout; either vertical (v) or horizontal (h)
        """
        from protograf.protos import Rectangle

        _locations = self.process_locations(location, "phase_revenue")
        if colors:
            _colors = colors
            colors_default = True
        else:
            _colors = [XX18_HEX_YELLOW, XX18_HEX_GREEN, XX18_HEX_BROWN, XX18_HEX_GREY]
            colors_default = True
        orientation = orientation if orientation else "horizontal"
        if not isinstance(orientation, str) or _lower(orientation) not in [
            "v",
            "vertical",
            "h",
            "horizontal",
        ]:
            feedback(
                f'The phase_revenue orientation "{orientation}" is invalid for {_locations};'
                " - use vertical (v) or horizontal (h).",
                True,
                True,
            )
        table_orientation = "V" if _lower(orientation) in ["v", "vertical"] else "H"
        incomes = tools.split(income, separator=" ", clean=True, no_blanks=True)
        if not incomes or len(incomes) < 2:
            feedback(
                f'The phase_revenue income "{income}" is invalid for {_locations};'
                " - at least two, space-separated values are required.",
                True,
                True,
            )
        if len(incomes) > len(_colors):
            feedback(
                f"Each phase_revenue income for {_locations} must have a matching color",
                True,
                True,
            )
        if len(incomes) == 2 and colors_default:
            _colors = [XX18_HEX_YELLOW, XX18_HEX_BROWN]
        box_width = XX18_PHASE_REVENUE_BOX
        box_height = XX18_PHASE_REVENUE_BOX * 0.8
        if table_orientation == "H":
            offset = box_width * len(incomes) / 2.0
        else:
            offset = box_height * len(incomes) / 2.0

        for _loc in _locations:
            geo = self.cells.get(_loc)
            ccentre = self.feature_location(geo, direction, distance)
            x1 = (
                ccentre.x - offset
                if table_orientation == "H"
                else ccentre.x - XX18_PHASE_REVENUE_BOX / 2.0
            )
            y1 = (
                ccentre.y - offset
                if table_orientation == "V"
                else ccentre.y - XX18_PHASE_REVENUE_BOX / 2.0
            )
            x, y = x1, y1
            for key, inc in enumerate(incomes):
                Rectangle(
                    x=x,
                    y=y,
                    height=box_height,
                    width=box_width,
                    fill_stroke=_colors[key],
                    label=inc,
                    label_font=XX18_TEXT_FONT,
                    label_stroke="black",
                    **kwargs,
                )
                x = x + box_width if table_orientation == "H" else x
                y = y + box_height if table_orientation == "V" else y
            if table_orientation == "H":
                Rectangle(
                    x=x1,
                    y=y1,
                    height=box_height,
                    width=box_width * len(incomes),
                    fill=None,
                    stroke="black",
                    stroke_width=XX18_STROKE_WIDTH,
                )
            else:
                Rectangle(
                    x=x1,
                    y=y1,
                    height=box_height * len(incomes),
                    width=box_width,
                    fill=None,
                    stroke="black",
                    stroke_width=XX18_STROKE_WIDTH,
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
            location1 (str): grid reference or references for end cell
            direction1 (float): degrees clockwise from East in end cell
            distance1 (float): distance from hex centre in end cell
        """
        from protograf.protos import Circle, Line, Text

        _locations_s = self.process_locations(location, "private-start")
        _locations_e = self.process_locations(location1, "private-end")
        if _locations_s and _locations_e:
            _loc_s = _locations_s[0]
            _loc_e = _locations_e[0]
            geo = self.cells.get(_loc_s)
            geo1 = self.cells.get(_loc_e)
            c_s = self.feature_location(geo, direction, distance)  # start
            c_e = self.feature_location(geo1, direction1, distance1)  # end
            # ---- private label settings
            # above: heading for upper-circle; above: title for lower-circle;
            # left: above line; right: below line;
            pce_heading, pce_title, pcs_heading, pcs_title = "", "", "", ""
            lheading, ltitle, labove = "", "", False
            if label:
                lwargs = {}
                lwargs["font_name"] = XX18_TEXT_FONT
                lwargs["font_size"] = XX18_TEXT_SMALL
                kwargs["stroke"] = "black"
                lwargs["heading_font"] = XX18_TEXT_FONT
                lwargs["heading_size"] = XX18_TEXT_SMALL
                kwargs["heading_stroke"] = "black"
                lwargs["title_font"] = XX18_TEXT_FONT
                lwargs["title_size"] = XX18_TEXT_SMALL
                kwargs["title_stroke"] = "black"

                label_location = kwargs.get("label_location", "below")
                relative_location = self.relative_location(label_location)

                match relative_location:
                    case RelativeLocation.ABOVE.value:
                        lheading = label
                        labove = True
                    case RelativeLocation.BELOW.value:
                        ltitle = label
                    case RelativeLocation.LEFT.value:
                        if c_s.x <= c_e.x:
                            if c_s.y < c_e.y:
                                pcs_heading = label
                            else:
                                pcs_title = label
                        else:
                            if c_s.y > c_e.y:
                                pce_heading = label
                            else:
                                pce_title = label
                    case RelativeLocation.RIGHT.value:
                        if c_s.x >= c_e.x:
                            if c_s.y < c_e.y:
                                pcs_heading = label
                            else:
                                pcs_title = label
                        else:
                            if c_e.y < c_s.y:
                                pce_heading = label
                            else:
                                pce_title = label

            # ---- private features; circles with title or heading
            pcs = Circle(
                cxy=c_s,
                radius=XX18_PRIVATE_DIAMETER / 2.0,
                fill=None,
                stroke="black",
                stroke_width=XX18_STROKE_WIDTH,
                title=pcs_title,
                heading=pcs_heading,
                **lwargs,
            )
            pce = Circle(
                cxy=c_e,
                radius=XX18_PRIVATE_DIAMETER / 2.0,
                fill=None,
                stroke="black",
                stroke_width=XX18_STROKE_WIDTH,
                title=pce_title,
                heading=pce_heading,
                **lwargs,
            )
            Line(
                links=[pcs, pce],
                **lwargs,
            )
            # ---- label - title or heading - for private line
            # breakpoint()
            if label and (ltitle or lheading):
                lcntr = geoms.fraction_along_line(c_e, c_s, 0.5)
                llabel = lheading or ltitle
                if c_e.y != c_s.y:
                    # align text in/out from line centre
                    if labove:
                        delta_y = -XX18_TEXT_SMALL / self.units / 2.0
                    else:
                        delta_y = XX18_TEXT_SMALL / self.units

                    if c_e.x > c_s.x and c_e.y < c_s.y:
                        talign = "left"
                    if c_e.x < c_s.x and c_e.y > c_s.y:
                        talign = "left"

                    if c_e.x > c_s.x and c_e.y > c_s.y:
                        talign = "right"
                    if c_e.x < c_s.x and c_e.y < c_s.y:
                        talign = "right"

                    Text(llabel, x=lcntr.x, y=lcntr.y + delta_y, align=talign, **lwargs)
                else:
                    # centre text over/above the line
                    if labove:
                        delta_y = -XX18_TEXT_SMALL / self.units / 2.0
                    else:
                        delta_y = XX18_TEXT_SMALL / self.units
                    Text(llabel, x=lcntr.x, y=lcntr.y + delta_y, **lwargs)  # centre

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
            label_location = kwargs.get("label_location", "below")
            offset = 0.5
            relative_location = self.relative_location(label_location)
            lwargs = self.process_label(label, relative_location, offset, "small")
            Image(_file, cxy=ccentre, **{**kwargs, **lwargs})

    def figure(
        self,
        location: str = None,
        direction: float = None,
        distance: float = None,
        thing: object = None,
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
        _locations = self.process_locations(location, "figure")
        for _loc in _locations:
            geo = self.cells.get(_loc)
            ccentre = self.feature_location(geo, direction, distance)
            thing.draw(off_x=ccentre.x, off_y=ccentre.y)
