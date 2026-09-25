# -*- coding: utf-8 -*-
"""
protograf Abstract game shapes
"""

# lib
# import os
import re

# third party

# module
from protograf import globals
from protograf.base import BaseShape
from protograf.shapes import (
    CircleShape,
    # PolygonShape,
    # RectangleShape,
    RectangularLocations,
    HexHexLocations,
    HexHexShape,
)
from protograf.utils import tools, colrs, geoms
from protograf.utils.messaging import feedback
from protograf.utils.structures import (  # named tuples
    Point,
    ShapeGeometry,
)
from protograf.utils.tools import _lower

# local
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


class AbstractGameObject(BaseShape):
    """Create an AbstractGame for a given canvas.

    Ref:

    """

    def __init__(self, _object=None, canvas=None, **kwargs):

        super().__init__(_object=_object, canvas=canvas, **kwargs)
        self.kwargs = kwargs
        self.set_unit_properties()
        # ---- user properties
        self.name = kwargs.get("name", "grid")
        self.fills = kwargs.get("fills", ["white"])
        self.strokes = kwargs.get("strokes", ["black"])
        self.hairs = tools.as_bool(kwargs.get("hairs", False))
        self.intersections = tools.as_bool(kwargs.get("intersections", False))
        self.hex_pattern = kwargs.get("hex_pattern", None)  # TODO - process this!
        self.label_start = kwargs.get("label_start", None)
        self.label_type = kwargs.get("label_type", None)
        self.pieces = None
        user_pieces = kwargs.get("pieces", [])
        self.pieces_resize = kwargs.get("pieces_resize", 0.8)
        self._validate_choices()
        # ---- custom properties
        self.orientation = "pointy"  # current, hard-coded for HexHex
        self.pieces_type = None
        self.cell_size = 1  # typically a "square" area or a hexagon diameter
        # ---- calculated properties
        if not kwargs.get("width"):
            self.width = (
                globals.page.width - globals.margins.left - globals.margins.right
            )
        if not kwargs.get("height"):
            self.height = (
                globals.page.height - globals.margins.top - globals.margins.bottom
            )
        if not kwargs.get("cx"):
            self.cx = self.width / 2.0
        if not kwargs.get("cy"):
            self.cy = self.height / 2.0
        self.set_options_by_game()
        # ---- check fills and colors
        if len(self.fills) != len(self.strokes):
            feedback(
                "The AbstractGame 'fills' and 'strokes' properties must be of equal length",
                True,
                True,
            )
        # ---- setup pieces
        self.pieces = self.setup_pieces(self.pieces_type, user_pieces)
        # ---- setup board
        self.setup_board()

    def game_name_error(self):
        """Generate feedback if incorrect game name used."""
        feedback(
            "The AbstractGame 'name' property must be one of the following: "
            f" Chess, Go, Checkers, Shogi, or grid (not '{self.name}').",
            True,
            True,
        )

    def set_options_by_game(self):
        """Set properties according to preset, known, game."""
        _available = min(self.height, self.width)
        match _lower(self.name):
            case "grid":  # default
                self.pieces_type = "checkers"
                if not self.fills:
                    self.fills = ("white",)
                if not self.strokes:
                    self.strokes = ("black",)
                if not self.cols:
                    self.rows = 8
                if not self.cols:
                    self.cols = 8
                _max_cells = max(self.rows, self.cols)
                self.cell_size = _available / _max_cells
            case "chess":
                self.pieces_type = "chess"
                if not self.fills:
                    self.fills = ("black", "silver")
                if not self.strokes:
                    self.strokes = (None, None)
                if not self.cols:
                    self.rows = 8
                if not self.cols:
                    self.cols = 8
                self.board_pattern = "snake"
            case "checkers" | "draughts":
                self.pieces_type = "checkers"
                if not self.fills:
                    self.fills = ("white",)
                if not self.strokes:
                    self.strokes = ("black",)
                if not self.cols:
                    self.rows = 8
                if not self.cols:
                    self.cols = 8
            case "go":
                self.pieces_type = "go"
                self.intersections = True
                if not self.fills:
                    self.fills = ("#D9A359",)
                if not self.strokes:
                    self.strokes = ("black",)
                if not self.cols:
                    self.rows = 18
                if not self.cols:
                    self.cols = 18
            case "shogi":
                self.pieces_type = "shogi"
                if not self.fills:
                    self.fills = ("white",)
                if not self.strokes:
                    self.strokes = ("black",)
                if not self.cols:
                    self.rows = 9
                if not self.cols:
                    self.cols = 9
            case "hexagons":
                if not self.cols:
                    feedback(
                        'Missing number of cols for AbstractBoard of type "hexagons"',
                        True,
                        True,
                    )
                if not self.rows:
                    feedback(
                        'Missing number of rows for AbstractBoard of type "hexagons"',
                        True,
                        True,
                    )
                _max_cells = max(self.rows, self.cols)
                self.cell_size = _available / _max_cells
            case "hex":
                raise NotImplementedError("Sorry, a hex board is not available yet.")
            case "hexhex":
                if not self.side:
                    feedback(
                        "Missing 'side' value (hexes along an edge)"
                        " for AbstractBoard of type 'hexhex'",
                        True,
                        True,
                    )
                _max_cells = self.side * 2 - 1
                self.cell_size = _available / _max_cells / 0.866
            case "tri" | "triangle" | "triangular":
                raise NotImplementedError(
                    "Sorry, a triangular board is not available yet."
                )
            case None:
                pass  # can ignore the name for this AB
            case _:
                self.game_name_error()
        # ---- calculate cell_size for gridded boards
        match _lower(self.name):
            case "grid" | "chess" | "checkers" | "go" | "shogi":
                _max_cells = max(self.rows, self.cols)
                self.cell_size = _available / _max_cells
            case _:
                pass

    def _validate_choices(self) -> bool:
        """Check user choices for valid selections."""
        # TODO - validate self.label_start and self.label_type
        if self.pieces is not None:
            if not isinstance(self.pieces, (list, tuple)):
                feedback(
                    "The AbstractGame 'pieces' property must be a list of pieces, "
                    f" not a '{type(self.pieces).__name__}'.",
                    True,
                    True,
                )
        if not isinstance(self.pieces_resize, (type(None), float, int)):
            feedback(
                "The AbstractGame 'pieces_resize' property must be a number, "
                f" not a '{type(self.name).__name__}'.",
                True,
                True,
            )
        if not isinstance(self.name, (type(None), str)):
            feedback(
                "The AbstractGame 'name' property must be a string, "
                f" not a '{type(self.name).__name__}'.",
                True,
                True,
            )
        if self.fills:
            if not isinstance(self.fills, (list, tuple)):
                feedback(
                    "The AbstractGame 'fills' property must be a list of colors, "
                    f" not a '{type(self.name).__name__}'.",
                    True,
                    True,
                )
            for col in self.fills:
                colrs.get_color(col)

        return True

    @property
    def shape_centre(self) -> Point:
        """Centre of AbstractGameObject."""
        return None

    @property
    def geo(self) -> ShapeGeometry:
        """Geometry of AbstractGameObject in user units."""
        return ShapeGeometry()

    @property
    def geometry(self) -> ShapeGeometry:
        """Geometry of AbstractGameObject - alias for geo."""
        return self.geo

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw the AbstractGameObject on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props

    def setup_board(self):
        """Create board_layout for the required grid"""
        from protograf.protos import Layout, square, Hexagons, hexagon

        # ---- game-based defaults
        board_pattern = "default"
        board_start = "NW"
        board_direction = "east"
        # TODO - calculate board labels
        top_x = self.x if self.kwargs.get("x") else self.cell_size / 2.0
        top_y = self.y if self.kwargs.get("y") else self.cell_size / 2.0
        match _lower(self.name):
            case "grid" | "chess" | "checkers" | "go" | "shogi":  # default
                self.board_layout = RectangularLocations(
                    cols=self.cols,
                    rows=self.rows,
                    x=top_x,
                    y=top_y,
                    interval=self.cell_size,
                    start=board_start,
                    direction=board_direction,
                    pattern=board_pattern,
                )
                _shapes = []
                for key, colr in enumerate(self.fills):
                    if self.intersections:
                        Layout(self.board_layout, draw_lines=True, _draw_grid=False)
                    else:
                        _shapes.append(
                            square(
                                side=self.cell_size,
                                stroke=self.strokes[key],
                                fill=colr,
                            )
                        )
                        Layout(self.board_layout, shapes=_shapes, _draw_grid=False)
                # ---- set default cell attributes (plus label)
                # TODO  - change this for shogi !! (numbers only; start at TR)
                for row in range(self.rows, 0, -1):
                    for col in range(1, self.cols + 1):
                        col_id = tools.sheet_column(col, lower=True)
                        cell_id = f"{col_id}{row}"
                        cell_geo = self.board_layout.cells[(col, row)]
                        cell_geo_label = cell_geo._replace(name=cell_id)
                        setattr(self, cell_id, cell_geo_label)
            case "hex":
                self.game_name_error()
            case "hexhex":
                rings = int(self.side) - 1
                self.board_layout = HexHexLocations(
                    cx=self.cx or self.x,  # no default value for cx
                    cy=self.cy or self.y,  # no default value for cy
                    diameter=self.cell_size,
                    # height=,  # NB self.height is the whole grid height
                    rings=rings,
                    orientation=self.orientation,
                )
                self.rows = (int(self.side) - 1) * 2 + 1
                self.cols = self.rows  # maximum at centre row!
                for key in self.board_layout.cells.keys():
                    ring, position = key[0], key[1] - 1  # 0-based position
                    col_row = geoms.hexhex_label(
                        ring=ring, position=position, num_rings=rings
                    )
                    cell_id = f"{col_row[0]}{col_row[1]}"
                    cell_geo = self.board_layout.cells[(ring, position + 1)]
                    # print(f"{ring=} {position=} => {cell_id} -> {cell_geo.centre}")
                    cell_geo_label = cell_geo._replace(name=cell_id)
                    setattr(self, cell_id, cell_geo_label)
            case "hexagons":
                self.board_layout = Hexagons(
                    cols=self.cols,
                    rows=self.rows,
                    x=top_x,
                    y=top_y,
                    orientation="pointy",
                    _draw_grid=False,
                )
                # ---- set default cell attributes (plus label)
                for row in range(1, self.rows + 1):
                    for col in range(1, self.cols + 1):
                        try:
                            # TODO - pass in settings to this function!
                            col_row = geoms.hexgrid_diagonal_coords(
                                col=col, row=row, total_rows=self.rows
                            )
                            cell_id = f"{col_row[0]}{col_row[1]}"
                            cell_geo = self.board_layout.cells[(col, row)]
                            # print(f"{col=} {row=}", col_row, cell_geo)
                            cell_geo_label = cell_geo._replace(name=cell_id)
                            setattr(self, cell_id, cell_geo_label)
                        except Exception as err:
                            feedback(
                                f"Unable to set properties for {col=}/{row=} ({err})",
                                True,
                                True,
                            )
            case _:
                self.game_name_error()

    def setup_pieces(self, pieces_type: str = None, pieces_list: list = None) -> dict:
        """Return pieces mapped as character:shape(s)."""
        if pieces_type is None and not pieces_list:
            pieces_type = "checkers"  # Default!
        pg_pieces = {}
        kwargs = {}
        breakpoint()
        kwargs["height"] = self.cell_size
        kwargs["width"] = self.cell_size
        kwargs["radius"] = self.cell_size / 2.0 * 0.9
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
            case "shogi_int":
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
                pass  # no defauls
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
                    "The AbstractGame 'pieces' property must contain a list of lists,"
                    f" not a '{type(self.name).__name__}'.",
                    True,
                    True,
                )
            if len(_piece) < 2:
                feedback(
                    "Each item in the AbstractGame 'pieces' property must"
                    " contain a piece identity and its pattern,"
                    f" so not '{_piece}'.",
                    True,
                    True,
                )
            piece_id = _piece[0]
            if not isinstance(piece_id, str) or _piece == ".":
                feedback(
                    "Each item in the AbstractGame 'pieces' property must"
                    " have a single character piece identity,"
                    f" not '{piece_id}'.",
                    True,
                    True,
                )
            if len(piece_id) != 1:
                feedback(
                    "Each item in the AbstractGame 'pieces' property must"
                    " have a single character piece identity,"
                    f" not '{piece_id}'.",
                    True,
                    True,
                )
            if isinstance(_piece[1], str):
                # try to use existing, defined piece
                # e.g. checkers_black, or chess_white_rook
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
                                    pg_pieces[piece_id] = piece_shape("kR", "checkers")
                                case "white":
                                    pg_pieces[piece_id] = piece_shape("kW", "checkers")
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
                                    f"A named piece's Chess name cannot be '{parts[2]}'.",
                                    True,
                                    True,
                                )
                            match pcolor:
                                case "black":
                                    pcode = NAMED_CHESS_BLACK[pname]
                                    pg_pieces[piece_id] = piece_shape(pcode, "chess")
                                case "white":
                                    pcode = NAMED_CHESS_WHITE[pname]
                                    pg_pieces[piece_id] = piece_shape(pcode, "chess")
                        case "go":
                            match pcolor:
                                case "black":
                                    pg_pieces[piece_id] = piece_shape("gB", "go")
                                case "white":
                                    pg_pieces[piece_id] = piece_shape("gW", "go")
                        case "shogi":
                            if pname not in SHOGI_NAMES:
                                feedback(
                                    f"A named piece's Shogi name cannot be '{parts[2]}'.",
                                    True,
                                    True,
                                )
                            match pcolor:
                                case "black":
                                    pcode = NAMED_SHOGI_BLACK[pname]
                                    pg_pieces[piece_id] = piece_shape(pcode, "shogi")
                                case "white":
                                    pcode = NAMED_SHOGI_WHITE[pname]
                                    pg_pieces[piece_id] = piece_shape(pcode, "shogi")
                        case "shogi_int":
                            if pname not in SHOGI_NAMES:
                                feedback(
                                    f"A named piece's Shogi International name cannot be '{parts[2]}'.",
                                    True,
                                    True,
                                )
                            match pcolor:
                                case "black":
                                    pcode = NAMED_SHOGI_INT_BLACK[pname]
                                    pg_pieces[piece_id] = piece_shape(pcode, "shogi")
                                case "white":
                                    pcode = NAMED_SHOGI_INT_WHITE[pname]
                                    pg_pieces[piece_id] = piece_shape(pcode, "shogi")
                        case _:
                            feedback(
                                "The AbstractGame name for the piece must be chosen"
                                " from one of the following games: "
                                f" Chess, Go, Shogi, or Checkers (not '{self.name}').",
                                True,
                                True,
                            )

            else:
                # user-defined piece; could be single shape or list of shapes
                pg_pieces[piece_id] = _piece[1]

        return pg_pieces


class AbstractStateObject(BaseShape):
    """Draw AbstractState composite shape on a given canvas.

    Reference:

    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super().__init__(_object=_object, canvas=canvas, **kwargs)
        self.kwargs = kwargs
        self.set_unit_properties()
        # ---- custom properties
        self.board = kwargs.get("board", None)
        self.positions = kwargs.get("positions", ".")
        self.setup = tools.as_bool(kwargs.get("setup", False))
        self.moves = kwargs.get("moves", None)
        self.annotations = kwargs.get("annotations", None)
        self.position_shapes = []
        self._validate_choices()
        # ---- set positions
        self.positions = self.initialise_pieces()
        self.position_matrix = self.process_positions()

    def initialise_pieces(self) -> str:
        """Create initial positions."""
        if self.setup:
            match _lower(self.board.name):
                case "chess":  # white at the bottom
                    return "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
                case "checkers" | "draughts":
                    return "1B1B1B1B/B1B1B1B1/1B1B1B1B/8/8/W1W1W1W1/1W1W1W1w/W1W1W1W1"
                case "go":
                    return ""
                case "shogi" | "shogi-int":  # white at the top
                    return "LNSGKGSNL/1R5B1/PPPPPPPPP/9/9/9/ppppppppp/1b5r1/lnsgkgsnl/123456789"
                case _:
                    if self.board.name:
                        feedback(
                            "The AbstractGame does not have a setup for '{self.board.name}'.",
                            True,
                            True,
                        )
                    else:
                        feedback(
                            "The AbstractGame does not have the 'name' property set;"
                            " so no predefined setup can be used.",
                            True,
                            True,
                        )
                    return ""
        return self.positions  # leave "as set by user" for processing

    def _validate_choices(self) -> bool:
        """Check user choices for valid selections."""
        if self.board is None:
            feedback(
                "The AbstractState 'board' property must be set!",
                True,
                True,
            )
        if not isinstance(self.board, AbstractGameObject):
            feedback(
                "The AbstractGame 'board' property must be an AbstractGame shape, "
                f" not a '{type(self.board.name).__name__}'.",
                True,
                True,
            )
            if self.board.pieces is not None:
                if not isinstance(self.board.pieces, (list, tuple)):
                    feedback(
                        "The AbstractGame 'pieces' property must be a list of pieces, "
                        f" not a '{type(self.board.pieces).__name__}'.",
                        True,
                        True,
                    )
        if self.positions is not None:
            if not isinstance(self.positions, str):
                feedback(
                    "The AbstractState 'positions' property must"
                    " be a string with positions setting or layout, "
                    f" not a '{type(self.positions).__name__}'.",
                    True,
                    True,
                )
        if self.moves is not None:
            if not isinstance(self.moves, (list, tuple)):
                feedback(
                    "The AbstractState 'moves' property must be a list of moves, "
                    f" not a '{type(self.moves).__name__}'.",
                    True,
                    True,
                )
        if self.annotations is not None:
            if not isinstance(self.annotations, (list, tuple)):
                feedback(
                    "The AbstractState 'annotations' property must be a list of annotations, "
                    f" not a '{type(self.annotations).__name__}'.",
                    True,
                    True,
                )
        return True

    @property
    def shape_centre(self) -> Point:
        """Centre of AbstractStateObject."""
        return None

    @property
    def geo(self) -> ShapeGeometry:
        """Geometry of AbstractStateObject in user units."""
        return None

    @property
    def geometry(self) -> ShapeGeometry:
        """Geometry of AbstractStateObject - alias for geo."""
        return self.geo

    def set_shape_positions(self, positions) -> list:
        """Convert positions list into Shapes suitable for drawing on board."""

    def process_positions(self) -> list:
        """Convert positions into a list structure."""
        if self.positions is None or self.positions == "":
            return []
        if "/" in self.positions and "/n" in self.positions:
            feedback(
                "Do not mix '/' and line-breaks for AbstractState 'positions'.",
                True,
                True,
            )
            return []
        # ---- get list of item positions
        if "/" in self.positions:
            position_std = re.sub(r"\d", lambda m: "." * int(m.group()), self.positions)
            _position_list = position_std.split("/")
        elif "/n" in self.positions:
            _position_list = self.positions.split("/")
        else:
            feedback(
                "Neither '/' or line-break were specified for AbstractState 'positions',"
                " so only a single row will be processed.",
                False,
            )
            _position_list = self.positions
        # ---- clean list
        position_list = [row for row in _position_list if row]
        # ---- validate list of item positions
        # TODO - improve these checks for hexhex board as well as irregular hexagonal
        if position_list and len(position_list) != self.board.rows:
            if len(position_list) < self.board.rows:
                feedback(
                    f"Not all rows have been set for the AbstractState 'positions'"
                    f" ({len(position_list)} vs {self.board.rows}).",
                    False,
                )
            if len(position_list) > self.board.rows:
                feedback(
                    f"There are too many rows for the AbstractState 'positions'"
                    f" ({len(position_list)} vs {self.board.rows}).",
                    True,
                    True,
                )
        for key, row in enumerate(position_list):
            if row == ".":
                row = "." * int(self.board.cols)
                position_list[key] = row
            if len(row) != self.board.cols:
                if len(row) < self.board.cols:
                    feedback(
                        f"Not all columns have been set for row#{key + 1} of the"
                        f" AbstractState 'positions' ({len(row)} vs {self.board.cols}).",
                        False,
                    )
                if len(row) > self.board.cols:
                    feedback(
                        f"There are too many columns for row#{key + 1} of the AbstractState"
                        f" 'positions' ({len(row)} vs {self.board.cols}).",
                        True,
                        True,
                    )
        return position_list

    def draw_pieces(self):
        """Draw the piece shapes on a given canvas using their character IDs."""
        if not self.board.pieces or not isinstance(self.board.pieces, dict):
            feedback(
                "The board's pieces have not been setup correctly!",
                True,
                True,
            )
        for row_no, row in enumerate(self.position_matrix):
            for col_no, col in enumerate(row):
                # print(f'&&& AbstractStateObject {row_no=},{col_no=} :', col)
                if col == ".":
                    continue  # no piece here; move along, move along
                piece_shape = self.board.pieces.get(col, None)
                if piece_shape is None:
                    feedback(
                        f"Unable to find the piece named '{col}'; "
                        " please check the set for '{self.board.name}'.",
                        True,
                        True,
                    )
                else:
                    cell = self.board.board_layout.cells.get((col_no + 1, row_no + 1))
                    cntr = cell.centre
                    # print(f'&&& AbstractStateObject {row_no=},{col_no=} :', cntr)
                    kwargs = {
                        "_abs_cx": tools.unit(cntr.x),
                        "_abs_cy": tools.unit(cntr.y),
                    }
                    piece_shape.draw(**kwargs)

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw the AbstractStateObject on a given canvas."""
        from protograf.protos import Layout, square, hexagon

        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- draw board
        _shapes = []
        match _lower(self.board.name):
            case "grid" | "chess" | "checkers" | "go" | "shogi":  # default name is grid
                if self.board.intersections:
                    Layout(
                        self.board.board_layout, shapes=None, draw_lines=True, **kwargs
                    )
                    # draw square to "fill in" board with color
                    # warning if setting colors for board cells?
                else:
                    for key, colr in enumerate(self.board.fills):
                        _shapes.append(
                            square(
                                side=self.board.cell_size,
                                stroke=self.board.strokes[key],
                                fill=colr,
                            )
                        )
                    Layout(self.board.board_layout, shapes=_shapes, **kwargs)
            case "hexagons":
                self.board.board_layout._draw_grid = True
                self.board.board_layout.draw_layout()
            case "hexhex":
                hhs = HexHexShape(
                    hexhex_locations=self.board.board_layout,
                    shape=hexagon(
                        diameter=self.board.cell_size,
                        fill=self.board.fill,
                        orientation=self.board.orientation,
                    ),
                    **kwargs,
                )
                hhs.draw()
            case _:
                feedback(
                    f"No available logic to draw AbstractState board '{self.board.name}'",
                    True,
                    True,
                )
        # ---- draw pieces
        if self.board.pieces and self.position_matrix:
            self.draw_pieces()
        elif self.board.pieces and not self.position_matrix:
            feedback(
                "To draw an AbstractState requires the 'positions' for the pieces",
                True,
                True,
            )
        elif self.position_matrix and not self.board.pieces:
            feedback(
                "To draw an AbstractState requires the board's pieces to be defined.",
                True,
                True,
            )
        elif not self.position_matrix and not self.board.pieces:
            feedback(
                "To draw an AbstractState requires both 'positions' and board pieces.",
                True,
                True,
            )
        else:
            raise ValueError(
                "Unexpected error handling position_matrix and board.pieces!"
            )

        # ---- draw annotations
        if self.annotations:
            for anno in self.annotations:
                if not isinstance(anno, BaseShape):
                    feedback(
                        "The AbstractGame 'annotations' property must be a list of shapes, "
                        f" not a '{type(self.board.pieces).__name__}'.",
                        True,
                        True,
                    )
                anno.draw()
