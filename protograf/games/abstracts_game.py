# -*- coding: utf-8 -*-
"""
protograf Abstract game shapes

Notes:
    * all arrays, such the cells of a board, are (col,row) with 1-based values
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
from protograf.utils.constants import (
    GRID_SHAPES_WITH_CENTRE,
)
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
from .abstracts_pieces import (
    piece_shape,
    NAMED_CHESS_BLACK,
    NAMED_CHESS_WHITE,
    NAMED_SHOGI_BLACK,
    NAMED_SHOGI_WHITE,
    NAMED_SHOGI_INT_WHITE,
    NAMED_SHOGI_INT_BLACK,
    SHOGI_NAMES,
)


class AbstractGameObject(CoreGameObject):
    """Create an AbstractGame for a given canvas."""

    def __init__(self, _object=None, canvas=None, **kwargs):
        super().__init__(_object=_object, canvas=canvas, **kwargs)
        # ---- abstract game
        self.game_class = "AbstractGame"
        self.board_pattern = "default"
        self.board_type = AbstractBoardType.GRID
        self.label_lower = not self.label_uppercase
        self.orientation = HexOrientationName.POINTY.value  # set for HexHex & Hex Grid
        # ---- add in defaults from games
        self.set_options_by_game(**kwargs)  # MUST be before call to validate!
        self._validate_choices()
        # ---- setup pieces
        # _pieces = kwargs.get("pieces", [])  # custom, define by user
        self.pieces = self.setup_pieces(self.pieces_type, self.pieces)
        # ---- setup board
        self.setup_board()

    def game_name_error(self):
        """Generate feedback if incorrect game name used."""
        feedback(
            "The AbstractGame 'name' property must be one of the following: "
            f" Chess, Go, Checkers, Shogi, Hex, HexHex, or grid (not '{self.name}').",
            True,
            True,
        )

    def set_options_by_game(self, **kwargs):
        """Set properties according to preset, known, game."""
        _max_cells = None
        match _lower(self.name):
            case "grid":  # default
                self.pieces_type = (
                    self._commons("pieces_type")
                    or kwargs.get("pieces_type")
                    or "checkers"
                )
                if self.fills is None:
                    self.fills = ("white",)
                if self.stroke is None:
                    self.stroke = "black"
                if not self.rows:
                    self.rows = 8
                if not self.cols:
                    self.cols = 8
                if self.label_start is None:
                    self.label_start = Corner.BOTTOM_LEFT
                if self.label_type is None:
                    self.label_type = "AN"
            case "chess":
                self.pieces_type = (
                    self._commons("pieces_type") or kwargs.get("pieces_type") or "chess"
                )
                self.intersections = False
                if self.fills is None:
                    self.fills = ("white", "silver")
                if self.stroke is None:
                    self.stroke = None
                if not self.rows:
                    self.rows = 8
                if not self.cols:
                    self.cols = 8
                self.board_pattern = "snake"
                self.label_start = Corner.BOTTOM_LEFT
                self.label_type = "AN"
            case "checkers" | "draughts":
                self.pieces_type = (
                    self._commons("pieces_type")
                    or kwargs.get("pieces_type")
                    or "checkers"
                )
                self.intersections = False
                if self.fills is None:
                    self.fills = ("firebrick", "black")
                if self.stroke is None:
                    self.stroke = None
                if not self.rows:
                    self.rows = 8
                if not self.cols:
                    self.cols = 8
                self.board_pattern = "snake"
                self.label_start = Corner.BOTTOM_LEFT
                self.label_type = "AN"
            case "go":
                self.pieces_type = (
                    self._commons("pieces_type") or kwargs.get("pieces_type") or "go"
                )
                self.intersections = True
                if self.fills is None:
                    self.fills = ("#D9A359",)
                if self.stroke is None:
                    self.stroke = "black"
                if not self.rows:
                    self.rows = 18
                if not self.cols:
                    self.cols = 18
                self.label_start = Corner.BOTTOM_LEFT
                self.label_type = "AN"
            case "shogi":
                self.pieces_type = (
                    self._commons("pieces_type") or kwargs.get("pieces_type") or "shogi"
                )
                self.intersections = False
                if self.fills is None:
                    self.fills = ("white",)
                if self.stroke is None:
                    self.stroke = "black"
                if not self.rows:
                    self.rows = 9
                if not self.cols:
                    self.cols = 9
                self.label_start = Corner.TOP_RIGHT
                self.label_type = "NN"
            case "hex":
                self._commons("pieces_type") or kwargs.get("pieces_type") or "default"
                if self.fills is None:
                    self.fills = ("white",)
                if self.stroke is None:
                    self.stroke = "black"
                self.rows = 11
                self.cols = 16
                if self.label_start is None:
                    self.label_start = Corner.BOTTOM_LEFT
                if self.label_type is None:
                    self.label_type = "AN"
                self.board_type = AbstractBoardType.HEXAGONAL
                self.pattern = """
                O O O O O O O O O O O . . . . .
                 O O O O O O O O O O O . . . . .
                . O O O O O O O O O O O . . . .
                 . O O O O O O O O O O O . . . .
                . . O O O O O O O O O O O . . .
                 . . O O O O O O O O O O O . . .
                . . . O O O O O O O O O O O . .
                 . . . O O O O O O O O O O O . .
                . . . . O O O O O O O O O O O .
                 . . . . O O O O O O O O O O O .
                . . . . . O O O O O O O O O O O
                """
            case "hexhex":
                if self.fills is None:
                    self.fills = ("white",)
                if self.stroke is None:
                    self.stroke = "black"
                if self.auto_size:
                    _available = min(self.page_height, self.page_width)
                    _max_cells = self.hexes * 2 - 1
                    self.cell_size = _available / _max_cells  # / 0.866
                self.board_type = AbstractBoardType.HEXAGONAL
                if self.label_start is None:
                    self.label_start = Corner.BOTTOM_LEFT
                if self.label_type is None:
                    self.label_type = "AN"
                self.rows = self.hexes * 2 - 1
                self.cols = self.hexes * 2 - 1
                self.pattern = self.hexhex_pattern(side=self.hexes)
            case "hexagons" | "hexagonal":
                if self.fills is None:
                    self.fills = ("white",)
                if self.stroke is None:
                    self.stroke = "black"
                if not self.rows:
                    self.rows = 8
                if not self.cols:
                    self.cols = 8
                self.board_type = AbstractBoardType.HEXAGONAL
                if self.label_start is None:
                    self.label_start = Corner.BOTTOM_LEFT
                if self.label_type is None:
                    self.label_type = "AN"
            case "tri" | "triangle" | "triangular":
                self.board_type = AbstractBoardType.TRIANGULAR
                if self.fills is None:
                    self.fills = ("white",)
                if self.stroke is None:
                    self.stroke = "black"
                raise NotImplementedError(
                    "Sorry, a triangular board is not available yet."
                )
            case None:
                # can ignore the name for this AB
                if self.fills is None:
                    self.fills = ("white",)
                if self.stroke is None:
                    self.stroke = "black"
                if self.label_start is None:
                    self.label_start = Corner.BOTTOM_LEFT
                if self.label_type is None:
                    self.label_type = "AN"
            case _:
                self.game_name_error()
        # ---- calculate "auto" cell_size
        # do for gridded boards NOT already calculated
        if self.auto_size and not _max_cells:
            _available = min(self.page_height, self.page_width)
            match self.board_type:
                case AbstractBoardType.GRID:
                    _max_cells = max(self.rows, self.cols)
                    self.cell_size = _available / _max_cells
                case AbstractBoardType.HEXAGONAL:
                    _max_cells = max(self.rows, self.cols)
                    self.cell_size = _available / _max_cells
                case AbstractBoardType.TRIANGULAR:
                    raise NotImplementedError(
                        "Sorry, a triangular board is not available yet to calculate cell size."
                    )
                case _:
                    feedback(
                        f"Cannot auto-calculate cell size for a '{self.name}' {self.game_class}.",
                        alert=True,
                    )

    def _validate_choices(self) -> bool:
        """Check and reset user choices for valid selections."""
        if self.label and self.label_type is None:
            self.label_type = "AN"
        if self.label_type is not None and self.label_type not in ["AN", "NN"]:
            feedback(
                f"The {self.game_class} 'label_type' property must be 'AN' or 'NN'; "
                f" not '{self.label_type}'.",
                True,
                True,
            )
        if self.label_start is not None:
            match self.label_start:
                case "TL" | Corner.TOP_LEFT:
                    self.label_start = Corner.TOP_LEFT
                case "TR" | Corner.TOP_RIGHT:
                    self.label_start = Corner.TOP_RIGHT
                case "BL" | Corner.BOTTOM_LEFT:
                    self.label_start = Corner.BOTTOM_LEFT
                case "BR" | Corner.BOTTOM_RIGHT:
                    self.label_start = Corner.BOTTOM_RIGHT
                case _:
                    feedback(
                        "The AbstractGame 'label_start' property must be one of: "
                        f"'TL', 'TR', 'BL', or 'BR'; not '{self.label_start}'.",
                        True,
                        True,
                    )
        if self.pieces is not None:
            if not isinstance(self.pieces, (list, tuple)):
                feedback(
                    f"The {self.game_class} 'pieces' property must be a list of pieces, "
                    f" not a '{type(self.pieces).__name__}'.",
                    True,
                    True,
                )
        if not isinstance(self.name, (type(None), str)):
            feedback(
                f"The {self.game_class} 'name' property must be a string, "
                f" not a '{type(self.name).__name__}'.",
                True,
                True,
            )
        if self.cell_shape:
            _type = type(self.cell_shape).__name__
            if not isinstance(self.cell_shape, BaseShape):
                feedback(
                    f"A shape is required for the cell_shape '{self.cell_shape}',"
                    f" not a {_type}.",
                    True,
                    True,
                )
            cshape_name = self.cell_shape.__class__.__name__
            if cshape_name not in GRID_SHAPES_WITH_CENTRE:
                feedback(
                    "A shape with a defined centre is required for the cell_shape"
                    f" - this cannot be a {cshape_name}.",
                    True,
                    True,
                )
        if self.fills:
            if isinstance(self.fills, str):
                self.fills = [self.fills]  # "auto-correct" for user
            if not isinstance(self.fills, (list, tuple)):
                feedback(
                    "The AbstractGame 'fills' property must be a list of colors, "
                    f" not a '{type(self.fills).__name__}'.",
                    True,
                    True,
                )
            for col in self.fills:
                colrs.get_color(col)  # validate each color
        if self.areas:
            if not isinstance(self.areas, (list, tuple)):
                feedback(
                    f"The {self.game_class} 'areas' property must be a list of shapes, "
                    f" not a '{type(self.areas).__name__}'.",
                    True,
                    True,
                )
            for area in self.areas:
                if not isinstance(area, BaseShape):
                    feedback(
                        f"The {self.game_class} 'areas' property must contain a list of shapes, "
                        f" it cannot contain a '{type(area).__name__}'.",
                        True,
                        True,
                    )
        match _lower(self.name):
            case "hexagons" | "hexagonal":
                if not self.cols:
                    feedback(
                        'Missing number of cols for AbstractBoard of type "hexagons."',
                        True,
                        True,
                    )
                if not self.rows:
                    feedback(
                        'Missing number of rows for AbstractBoard of type "hexagons."',
                        True,
                        True,
                    )
            case "hexhex":
                if not self.hexes:
                    feedback(
                        "Missing 'hexes' value (hexagons along an edge)"
                        " for AbstractBoard of type 'hexhex'.",
                        True,
                        True,
                    )
                else:
                    if not self.hexes.is_integer():
                        feedback(
                            "The 'hexes' value (hexagons along an edge) must be an"
                            " integer for an AbstractBoard of type 'hexhex'.",
                            True,
                            True,
                        )
                    self.hexes = int(self.hexes)
                    if self.hexes < 2:
                        feedback(
                            "The 'hexes' value (hexagons along an edge) must be more"
                            " than 2 for an AbstractBoard of type 'hexhex'.",
                            True,
                            True,
                        )
            case _:
                pass
        if self.board_type == AbstractBoardType.HEXAGONAL and self.intersections:
            feedback(
                "Use of intersections is not supported for hexagonal type boards.",
                True,
                True,
            )

        return True

    def draw_frame(self):
        """Draw the board's frame on a given canvas."""
        match _lower(self.name):
            case "grid" | "chess" | "checkers" | "go" | "shogi":  # default name is grid
                total_width = self.cols * self.cell_size
                total_height = self.rows * self.cell_size
                top_left = self.board_layout.cells[(1, 1)].bbox.tl
                x_left = tools.unit(top_left.x + globals.margins.left)
                y_top = tools.unit(top_left.y + globals.margins.top)
                # ---- offset frame as a rectangle
                rect = (
                    x_left - self.frame_width / 2.0,
                    y_top - self.frame_width / 2.0,
                    x_left + tools.unit(total_width) + self.frame_width / 2.0,
                    y_top + tools.unit(total_height) + self.frame_width / 2.0,
                )
                rkwargs = {}  # copy.copy(kwargs)
                rkwargs["fill"] = self.frame_fill
                rkwargs["stroke"] = self.frame_stroke
                rkwargs["stroke_width"] = self.frame_width
                rkwargs["stroke_transparency"] = self.frame_stroke_transparency
                rkwargs["dashed"] = self.frame_dashed
                rkwargs["dotted"] = self.frame_dotted
                pymu_props = tools.get_pymupdf_props(**rkwargs)
                globals.doc_page.draw_rect(
                    rect,
                    width=pymu_props.width,
                    color=pymu_props.color,
                    fill=pymu_props.fill,
                    lineCap=pymu_props.lineCap,
                    dashes=pymu_props.dashes,
                    fill_opacity=pymu_props.fill_opacity,
                    stroke_opacity=pymu_props.stroke_opacity,
                    # radius=None,
                )
            case _:
                feedback(
                    f"No available logic to draw a frame for AbstractBoard '{self.name}'",
                    True,
                    True,
                )

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

            # ---- grid column labels
            if self.board_type == AbstractBoardType.GRID:
                col_num = 1
                for col_no in range(start_col, end_col, delta_col):
                    # skip blank columns at start OR end of row
                    active_cells = self.cells_non_blank[label_row - 1]
                    col_exists = any(
                        len(tup) > 1 and tup[0] == col_no for tup in active_cells
                    )
                    if not col_exists:
                        continue
                    col_value = str(col_num)
                    if self.label_type in ["AN", "AA"]:
                        col_value = tools.alpha_column(col_num, lower=self.label_lower)
                    else:
                        col_value = str(col_num)
                    # get cell geo to use for label position
                    adjacent_cell = self.board_layout.cells[(col_no, label_row)]
                    x, y = 0, 0
                    if self.label_start in [Corner.BOTTOM_RIGHT, Corner.BOTTOM_LEFT]:
                        x = adjacent_cell.s.x
                        y = (
                            adjacent_cell.s.y
                            + shift * lbl_offset_col * 1.5
                            - lbl_intersect
                        )
                    elif self.label_start in [Corner.TOP_RIGHT, Corner.TOP_LEFT]:
                        x = adjacent_cell.n.x
                        y = adjacent_cell.n.y + shift * lbl_offset_col + lbl_intersect
                    else:
                        raise NotImplementedError(
                            "Cannot process label_start of {self.label_start}"
                        )
                    Text(col_value, x=x, y=y, **lkeys)
                    col_num += 1
            # ---- hex column labels
            elif self.board_type == AbstractBoardType.HEXAGONAL:
                non_blank_col_no = 1  # do NOT label blank diagonals
                for _, dcells in self.hexgrid_diagonals.items():
                    # print(f'&&& {dcells=} {non_blank_col_no=}')
                    for value in dcells:
                        col_no, row_no = value[0], value[1]
                        col_value = tools.as_excel(non_blank_col_no, self.label_lower)
                        adjacent_cell = self.board_layout.cells[(col_no, row_no)]
                        if not adjacent_cell.blank:
                            x, y = hex_col_label()
                            Text(col_value, x=x, y=y, **lkeys)
                            # print(f'&&& {col_value=} {col_no=} {row_no=}')
                            non_blank_col_no += 1
                            break  # label done; next diagonal, please!
            # ---- tri column labels
            elif self.board_type == AbstractBoardType.TRIANGULAR:
                raise NotImplementedError(f"No labels for {self.board_type} grid!")
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
                    row_value = tools.alpha_column(row_num, lower=self.label_lower)
                else:
                    row_value = str(row_num)
                col_no = label_col  # label col can be at start or end
                # print(f"{row_no=} {col_no=}") ; #breakpoint()
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
        match self.board_type:
            # ---- setup Grid boards
            case AbstractBoardType.GRID:
                top_x = self.x if self.kwargs.get("x") else self.cell_size / 2.0
                top_y = self.y if self.kwargs.get("y") else self.cell_size / 2.0
                self.board_layout = RectangularLocations(  # VirtualLocations
                    cols=self.cols,
                    rows=self.rows,
                    x=top_x,
                    y=top_y,
                    interval=self.cell_size,
                    start=board_start,
                    direction=board_direction,
                    pattern=self.board_pattern,
                )
                # print(f'&&& GRID BOARD {self.board_layout.cells.keys()=}')
                if self.intersections:
                    self.grid_kwargs["gridlines_ends"] = self.stroke_ends
                    self.grid_kwargs["gridlines_fill"] = self.fill
                    self.grid_kwargs["gridlines_stroke"] = self.stroke
                    self.grid_kwargs["gridlines_stroke_width"] = self.stroke_width
                    self.grid_kwargs["gridlines_dotted"] = self.dotted
                    self.grid_kwargs["gridlines_dashed"] = self.dashed
                    self.grid_kwargs["gridlines_transparency"] = self.transparency
                    Layout(
                        self.board_layout,
                        draw_lines=True,
                        _draw_grid=False,
                        **self.grid_kwargs,
                    )
                else:
                    if self.areas:
                        pass
                    else:
                        self.areas = []
                        for colr in self.fills:
                            self.areas.append(
                                rectangle(
                                    height=self.cell_size,
                                    width=self.cell_size,
                                    stroke=self.stroke,
                                    stroke_width=self.stroke_width,
                                    fill=colr,
                                )
                            )
                    Layout(self.board_layout, shapes=self.areas, _draw_grid=False)

                # ---- * default cell attributes (plus label); track non-blank cells

                # ---- * label direction
                for row in range(1, self.rows + 1, 1):
                    non_blank = []
                    for col in range(1, self.cols + 1, 1):
                        # alter ID according to direction
                        match self.label_start:
                            case Corner.TOP_LEFT:
                                col_no = col
                                row_no = row
                            case Corner.BOTTOM_RIGHT:
                                col_no = self.cols - col + 1
                                row_no = self.rows - row + 1
                            case Corner.TOP_RIGHT:
                                col_no = self.cols - col + 1
                                row_no = row
                            case Corner.BOTTOM_LEFT:
                                col_no = col
                                row_no = self.rows - row + 1
                        if self.label_type == "AN":  # alpha-numeric
                            col_id = tools.sheet_column(col_no, lower=self.label_lower)
                            row_id = str(row_no)
                            id_prefix = ""
                        elif self.label_type == "NN":  # numeric-numeric
                            col_id = str(col_no)
                            row_id = str(row_no)
                            id_prefix = "_"
                        else:
                            raise NotImplementedError(
                                f"Cannot process label_type {self.label_type}"
                            )
                        cell_id = f"{id_prefix}{col_id}{row_id}"
                        cell_geo = self.board_layout.cells[(col, row)]
                        if not cell_geo.blank:
                            non_blank.append((col, row))
                        # print(f"&&& GRID {col=} {row=}",  cell_id)
                        cell_geo_label = cell_geo._replace(name=cell_id)
                        setattr(self, cell_id, cell_geo_label)
                    self.cells_non_blank.append(non_blank)  # per-row list of non-blank

            # ---- setup Hexagonal boards
            case AbstractBoardType.HEXAGONAL:
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
                    orientation=HexOrientationName.POINTY.value,  # hard-coded: HexGrid
                    _draw_grid=False,
                    pattern=self.pattern,
                    user=f"{self.game_class}",
                    # single hexagon properties:-
                    height=self.cell_size,
                    stroke=self.stroke,
                    stroke_width=self.stroke_width,
                    fill=colr,
                    hex_shape=self.cell_shape,  # insert centre_image into hex
                )
                # print(f'&&& HEXES BOARD {self.board_layout.cells.keys()=}')

                # ---- * get hexgrid in alpha-numeric form
                self.hexgrid_diagonals = geoms.hexgrid_diagonal_cells(
                    cols=self.cols, rows=self.rows, start_cell=self.label_start
                )
                self.hexgrid_alpha_coords = geoms.hexgrid_alphanumeric(
                    diagonal_dict=self.hexgrid_diagonals,
                    start_cell=self.label_start,
                    lower=self.label_lower,
                )

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
                non_blank_col_no = 0  # do NOT label **fully blank** diagonal
                for _, dcells in self.hexgrid_diagonals.items():
                    # print(f'\n&&& {diagonal=} {dcells=}')
                    use_diagonal = False
                    for value in dcells:
                        target_cell = self.board_layout.cells[(value[0], value[1])]
                        if not target_cell.blank:
                            use_diagonal = True
                            break
                    if use_diagonal:
                        non_blank_col_no += 1
                        for value in dcells:
                            # print(f'&&& {diagonal=} {non_blank_col_no=} {value=}')
                            try:
                                col, row = value[0], value[1]
                                if self.label_start in [
                                    Corner.BOTTOM_LEFT,
                                    Corner.BOTTOM_RIGHT,
                                ]:
                                    row_num = self.rows - row + 1
                                else:
                                    row_num = row
                                cell_geo = self.board_layout.cells[(col, row)]
                                col_alpha = tools.as_excel(
                                    non_blank_col_no, self.label_lower
                                )
                                cell_id = f"{col_alpha}{row_num}"
                                cell_geo_label = cell_geo._replace(name=cell_id)
                                # print(f"&&& HEX {value=} name={cell_id}")
                                setattr(self, cell_id, cell_geo_label)
                            except Exception as err:
                                feedback(
                                    f"Unable to process hex cell: col={value[0]}, "
                                    f"row={value[1]} ({err})",
                                    True,
                                    True,
                                )

            # ---- setup Triangular boards
            case AbstractBoardType.TRIANGULAR:
                raise NotImplementedError(
                    "Sorry, a triangular board is not available yet."
                )
            case _:
                self.game_name_error()

    def setup_pieces(self, pieces_type: str = None, pieces_list: list = None) -> dict:
        """Return pieces mapped as character:shape(s)."""
        if pieces_type is None and not pieces_list:
            pieces_type = None  # Default!
        pg_pieces = {}
        kwargs = {}
        kwargs["height"] = self.cell_size
        kwargs["width"] = self.cell_size
        kwargs["radius"] = self.cell_size / 2.0 * 0.8
        # ---- pre-defined piece types
        match pieces_type:
            case "checkers" | "draughts":
                pg_pieces = {
                    "R": piece_shape("kR", "Red", **kwargs),
                    "W": piece_shape("kW", "White", **kwargs),
                }
            case "chess":
                pg_pieces = {
                    "B": piece_shape("cB", "White Bishop", **kwargs),
                    "b": piece_shape("cb", "Black Bishop", **kwargs),
                    "K": piece_shape("cK", "White King", **kwargs),
                    "k": piece_shape("ck", "Black King", **kwargs),
                    "N": piece_shape("cN", "White Knight", **kwargs),
                    "n": piece_shape("cn", "Black Knight", **kwargs),
                    "P": piece_shape("cP", "White Pawn", **kwargs),
                    "p": piece_shape("cp", "Black Pawn", **kwargs),
                    "Q": piece_shape("cQ", "White Queen", **kwargs),
                    "q": piece_shape("cq", "Black Queen", **kwargs),
                    "R": piece_shape("cR", "White Rook", **kwargs),
                    "r": piece_shape("cr", "Black Rook", **kwargs),
                }
            case "go":
                pg_pieces = {
                    "B": piece_shape("gB", "Black Stone", **kwargs),
                    "W": piece_shape("gW", "White Stone", **kwargs),
                }
            case "shogi":
                pg_pieces = {
                    "A": piece_shape("sA", "White Lance: Promoted", **kwargs),
                    "a": piece_shape("sa", "Black Lance: Promoted", **kwargs),
                    "B": piece_shape("sB", "White Bishop", **kwargs),
                    "b": piece_shape("sb", "Black Bishop", **kwargs),
                    "D": piece_shape("sD", "White Rook: Promoted (Dragon)", **kwargs),
                    "d": piece_shape("sd", "Black Rook: Promoted (Dragon)", **kwargs),
                    "G": piece_shape("sG", "White Gold General", **kwargs),
                    "g": piece_shape("sg", "Black Gold General", **kwargs),
                    "H": piece_shape("sH", "White Bishop: Promoted (Horse)", **kwargs),
                    "h": piece_shape("sh", "Black Bishop: Promoted (Horse)", **kwargs),
                    "J": piece_shape("sJ", "White King (challenger)", **kwargs),
                    "j": piece_shape("sj", "Black King (challenger)", **kwargs),
                    "K": piece_shape("sK", "White King (champion)", **kwargs),
                    "k": piece_shape("sk", "Black King (champion)", **kwargs),
                    "l": piece_shape("sl", "Black Lance", **kwargs),
                    "L": piece_shape("sL", "White Lance", **kwargs),
                    "N": piece_shape("sN", "White Knight", **kwargs),
                    "n": piece_shape("sn", "Black Knight", **kwargs),
                    "P": piece_shape("sP", "White Pawn", **kwargs),
                    "p": piece_shape("sp", "Black Pawn", **kwargs),
                    "R": piece_shape("sR", "White Rook", **kwargs),
                    "r": piece_shape("sr", "Black Rook", **kwargs),
                    "S": piece_shape("sS", "White Silver General", **kwargs),
                    "s": piece_shape("ss", "Black Silver General", **kwargs),
                    "T": piece_shape("sT", "White Knight: Promoted", **kwargs),
                    "t": piece_shape("st", "Black Knight: Promoted", **kwargs),
                    "W": piece_shape("sV", "White Pawn: Promoted", **kwargs),
                    "w": piece_shape("sv", "Black Pawn: Promoted", **kwargs),
                    "V": piece_shape("sW", "White Silver General: Promoted", **kwargs),
                    "v": piece_shape("sw", "Black Silver General: Promoted", **kwargs),
                }
            case "shogi_int" | "shogi-int":
                pg_pieces = {
                    "A": piece_shape("iA", "White Lance: Promoted", **kwargs),
                    "a": piece_shape("ia", "Black Lance: Promoted", **kwargs),
                    "B": piece_shape("iB", "White Bishop", **kwargs),
                    "b": piece_shape("ib", "Black Bishop", **kwargs),
                    "D": piece_shape("iD", "White Rook: Promoted (Dragon)", **kwargs),
                    "d": piece_shape("id", "Black Rook: Promoted (Dragon)", **kwargs),
                    "G": piece_shape("iG", "White Gold General", **kwargs),
                    "g": piece_shape("ig", "Black Gold General", **kwargs),
                    "H": piece_shape("iH", "White Bishop: Promoted (Horse)", **kwargs),
                    "h": piece_shape("ih", "Black Bishop: Promoted (Horse)", **kwargs),
                    "J": piece_shape("iJ", "White King (challenger)", **kwargs),
                    "j": piece_shape("ij", "Black King (challenger)", **kwargs),
                    "K": piece_shape("iK", "White King (champion)", **kwargs),
                    "k": piece_shape("ik", "Black King (champion)", **kwargs),
                    "l": piece_shape("il", "Black Lance", **kwargs),
                    "L": piece_shape("iL", "White Lance", **kwargs),
                    "N": piece_shape("iN", "White Knight", **kwargs),
                    "n": piece_shape("in", "Black Knight", **kwargs),
                    "P": piece_shape("iP", "White Pawn", **kwargs),
                    "p": piece_shape("ip", "Black Pawn", **kwargs),
                    "R": piece_shape("iR", "White Rook", **kwargs),
                    "r": piece_shape("ir", "Black Rook", **kwargs),
                    "S": piece_shape("iS", "White Silver General", **kwargs),
                    "s": piece_shape("is", "Black Silver General", **kwargs),
                    "T": piece_shape("iT", "White Knight: Promoted", **kwargs),
                    "t": piece_shape("it", "Black Knight: Promoted", **kwargs),
                    "W": piece_shape("iV", "White Pawn: Promoted", **kwargs),
                    "w": piece_shape("iv", "Black Pawn: Promoted", **kwargs),
                    "V": piece_shape("iW", "White Silver General: Promoted", **kwargs),
                    "v": piece_shape("iw", "Black Silver General: Promoted", **kwargs),
                }
            case None:
                pg_pieces = {
                    "B": piece_shape("B", "Black", **kwargs),  # plain circle
                    "W": piece_shape("W", "White", **kwargs),  # plain circle
                }
            case _:
                raise NotImplementedError(
                    f'Pieces Type "{pieces_type}" is not available.'
                )
        # ---- convert PG and User lists to dict
        if not pieces_list:
            pieces_list = []
        for _piece in pieces_list:
            if not isinstance(_piece, (list, tuple)):
                feedback(
                    f"The {self.game_class} 'pieces' property must contain a list of lists,"
                    f" not a '{type(self.name).__name__}'.",
                    True,
                    True,
                )
            if len(_piece) < 2:
                feedback(
                    f"Each item in the {self.game_class} 'pieces' property must"
                    " contain a piece identity and its pattern,"
                    f" so not '{_piece}'.",
                    True,
                    True,
                )
            piece_id = _piece[0]
            if not isinstance(piece_id, str) or _piece == ".":
                feedback(
                    f"Each item in the {self.game_class} 'pieces' property must"
                    " have a single character piece identity,"
                    f" not '{piece_id}'.",
                    True,
                    True,
                )
            if len(piece_id) != 1:
                feedback(
                    f"Each item in the {self.game_class} 'pieces' property must"
                    " have a single character piece identity,"
                    f" not '{piece_id}'.",
                    True,
                    True,
                )
            if isinstance(_piece[1], str):
                # try to use existing, defined piece
                # e.g. checkers_black, or chess_white_rook
                # NOTE use of kwargs to, for example, scale the piece size
                parts = _piece[1].split("_")
                game = _lower(parts[0])
                if game not in ("go", "checkers", "chess"):
                    feedback(
                        "A named piece type must start with a matching game, "
                        f" not '{parts[0]}'.",
                        True,
                        True,
                    )
                if len(parts) < 2:
                    feedback(
                        "A named piece type must start with a matching game, followed by a color, "
                        f" not '{parts}'.",
                        True,
                        True,
                    )
                pcolor = _lower(parts[1])
                if pcolor not in ("black", "white"):
                    feedback(
                        "A named piece type color must be either black or white, "
                        f" not '{parts[1]}'.",
                        True,
                        True,
                    )
                if len(parts) > 2:
                    pname = _lower(parts[2])

                    match game:
                        case "checkers":
                            match pcolor:
                                case "black":
                                    pg_pieces[piece_id] = piece_shape(
                                        "kR", "checkers", **kwargs
                                    )
                                case "white":
                                    pg_pieces[piece_id] = piece_shape(
                                        "kW", "checkers", **kwargs
                                    )
                        case "chess":
                            if pname not in (
                                "pawn",
                                "queen",
                                "king",
                                "rook",
                                "bishop",
                                "knight",
                            ):
                                feedback(
                                    f"A piece's Chess name cannot be '{parts[2]}'.",
                                    True,
                                    True,
                                )
                            match pcolor:
                                case "black":
                                    pcode = NAMED_CHESS_BLACK[pname]
                                    pg_pieces[piece_id] = piece_shape(
                                        pcode, "chess", **kwargs
                                    )
                                case "white":
                                    pcode = NAMED_CHESS_WHITE[pname]
                                    pg_pieces[piece_id] = piece_shape(
                                        pcode, "chess", **kwargs
                                    )
                        case "go":
                            match pcolor:
                                case "black":
                                    pg_pieces[piece_id] = piece_shape(
                                        "gB", "go", **kwargs
                                    )
                                case "white":
                                    pg_pieces[piece_id] = piece_shape(
                                        "gW", "go", **kwargs
                                    )
                        case "shogi":
                            if pname not in SHOGI_NAMES:
                                feedback(
                                    f"A piece's Shogi name cannot be '{parts[2]}'.",
                                    True,
                                    True,
                                )
                            match pcolor:
                                case "black":
                                    pcode = NAMED_SHOGI_BLACK[pname]
                                    pg_pieces[piece_id] = piece_shape(
                                        pcode, "shogi", **kwargs
                                    )
                                case "white":
                                    pcode = NAMED_SHOGI_WHITE[pname]
                                    pg_pieces[piece_id] = piece_shape(
                                        pcode, "shogi", **kwargs
                                    )
                        case "shogi_int":
                            if pname not in SHOGI_NAMES:
                                feedback(
                                    f"A piece's Shogi International name cannot be '{parts[2]}'.",
                                    True,
                                    True,
                                )
                            match pcolor:
                                case "black":
                                    pcode = NAMED_SHOGI_INT_BLACK[pname]
                                    pg_pieces[piece_id] = piece_shape(
                                        pcode, "shogi", **kwargs
                                    )
                                case "white":
                                    pcode = NAMED_SHOGI_INT_WHITE[pname]
                                    pg_pieces[piece_id] = piece_shape(
                                        pcode, "shogi", **kwargs
                                    )
                        case _:
                            feedback(
                                f"The {self.game_class} name for the piece must be chosen"
                                " from one of the following games: "
                                f" Chess, Go, Shogi, or Checkers (not '{self.name}').",
                                True,
                                True,
                            )

            else:
                # user-defined piece; could be single shape or list of shapes
                pg_pieces[piece_id] = _piece[1]

        return pg_pieces
