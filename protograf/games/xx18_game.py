# -*- coding: utf-8 -*-
"""
protograf 18XX games

Notes:
    * all arrays, such the cells of a board, are (col,row) with 1-based values

Outline:

The 18xx map "blueprint" feature covers:

* depiction of towns as filled-in circles
* depiction of cities (single, double) as open circles
* depiction of track, curved and straight; by itself or extending from a city
* depiction of terminal spikes running off the board (short, medium and long)
* depiction of blocked hex-sides (as lines)
* depiction of private railways (in-hex; across hexes)
* depiction of icons for various in-hex features; including mountains (two sizes),
  hills, swamp, river, port, desert, mine, coal and oilrig
* setting of a single letter
* display of hex coordinates along the edges of the map
* depiction of a custom shape in a hex
* depiction of a circle on a hex-side (at a perbii position)
* depiction of a river running along a hex-side
* coloring of a whole hex
* setting of a shaded rectangular area (typically red and at the edge of the map)
* creation of a small multi-line table to appear in a hex
  (typically income per stage of the game)

The blueprint will also provide:
* standard, named 18xx colors
* ability to set the map font to use
* ability to put labels next to icons, towns or cities (above, below, left of, right of)
* ability to put text inside a city circle

In-hex features, for example, cities, towns, icons, or letter, will by default appear
at the centre of a hex. These can be repositioned using a combination of direction
(in compass degrees) and distance of the feature's center from the hex center (as a percentage of the hex radius).

Positioning of features on hex edges will be done using standard compass directions;
"ne" for northeast, "s" for south, etc., and distance as a fraction from the centre.

Drawing will be done following the order in which features are provided.
"""

# lib
import re

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

# constants
XX18_HEX_HEIGHT = 4.399  # cm
XX18_HEX_SIDE = 2.54  # cm
XX18_CITY_DIAMETER = 0.5  # cm
XX18_TOWN_DIAMETER = 0.35  # cm
XX18_MTN_SIDE = 0.5  # cm; equilateral triangle


class XX18GameObject(CoreGameObject):
    """Create a XX18GameObject for a given canvas."""

    def __init__(self, _object=None, canvas=None, **kwargs):
        super().__init__(_object=_object, canvas=canvas, **kwargs)
        # ---- 18xx game
        self.game_class = "XX18Game"
        self.board_type = AbstractBoardType.HEXAGONAL
        self.board_pattern = "hexagonal"
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
        # ---- add in defaults from games
        if not self.rows:
            self.rows = 9
        if not self.cols:
            self.cols = 11
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
            stroke_width=self.stroke_width,
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
                    print(f"&&& HEX {row=} {col=} name={cell_id}")
                    setattr(self, cell_id, cell_geo_label)
                except Exception as err:
                    feedback(
                        f"Unable to process hex cell: {col=} {row=} ({err})",
                        True,
                        True,
                    )

    def process_locations(self, feature, location: str = None) -> list:
        """Draw Town shape at hex location(s).

        Args:
            location (str): grid reference or references for one or more cells
        """
        if not location:
            return []
        if location is not None and not isinstance(location, str):
            feedback(
                f"The {feature} 'location' property must be a string; not '{location}'.",
                True,
                True,
            )
        _locations = location.split(location)
        # TODO - check locs exist and convert each to a col/row tuple
        return _locations

    def town(
        self, location: str = None, offset: str = None, label: str = None, **kwargs
    ):
        """Draw Town shape at hex location(s).

        Args:
            location (str): grid reference or references for one or more cells
            offset (str): direction (degrees) and distance from hex centre
            label (str): the name of the town
        """
        _locations = self.process_locations("town", location)

    def city(
        self,
        location: str = None,
        offset: str = None,
        label: str = None,
        shape: str = None,
        **kwargs,
    ):
        """Draw City shape at hex location(s).

        Args:
            location (str): grid reference or references for one or more cells
            offset (str): direction (degrees) and distance from hex centre
            label (str): the name of the city
            shape (Shape): the shape to be drawn inside the city
        """
        _locations = self.process_locations("city", location)

    def mountain(self, location: str = None, offset: str = None, **kwargs):
        """Draw Mountain shape at hex location(s).

        Args:
            location (str): grid reference or references for one or more cells
            offset (str): direction (degrees) and distance from hex centre
        """
        _locations = self.process_locations("mountain", location)

    def feature(
        self, location: str = None, offset: str = None, name: str = None, **kwargs
    ):
        """Draw a Feature shape at hex location(s).

        Args:
            location (str): grid reference or references for one or more cells
            name (str): name of the feature
            offset (str): direction (degrees) and distance from hex centre
        """
        feature_set = [
            "coal",
            "hill",
            "desert",
            "mine",
            "oil",
            "port",
            "river",
            "swamp",
        ]
        if name not in feature_set:
            feedback(
                f"The feature 'name' property cannot be '{name}';",
                f" choose from: {feature_set}.",
                True,
                True,
            )
        _locations = self.process_locations(f"{name} feature", location)
