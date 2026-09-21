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
)
from protograf.utils import tools, colrs, geoms
from protograf.utils.messaging import feedback
from protograf.utils.structures import (  # named tuples
    Point,
    ShapeGeometry,
)
from protograf.utils.tools import _lower


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
        self.labels_start = kwargs.get("labels_start", None)
        self.labels_type = kwargs.get("labels_type", None)
        self.grid_align = tools.as_bool(kwargs.get("grid_align", False))
        self.pieces = None
        user_pieces = kwargs.get("pieces", [])
        self.pieces_resize = kwargs.get("pieces_resize", 0.8)
        self._validate_choices()
        # ---- custom properties
        self.pieces_type = None
        self.cell_size = 1  # typically a "square" area
        # ---- calculated properties
        if not kwargs.get("width"):
            self.width = (
                globals.page.width - globals.margins.left - globals.margins.right
            )
        if not kwargs.get("height"):
            self.height = (
                globals.page.height - globals.margins.top - globals.margins.bottom
            )
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
                self.grid_align = True
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
                raise NotImplementedError("Sorry, a hexhex board is not available yet.")
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
        # TODO - validate self.labels_start and self.labels_type
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

    def character_map(self, piece_name: str) -> object:
        """Return predefined shape or Image associated with a known piece character."""

        def chess_piece(name):
            # lookup image and return Image
            print(f"Chess {name}")
            return None

        def go_stone(name):
            # lookup image and return Image
            print(f"Go {name}")
            return None

        match piece_name:
            case "cB":
                return CircleShape(canvas=self.canvas, fill="black", stroke="black")
            case "cW":
                return CircleShape(canvas=self.canvas, fill="white", stroke="black")
            case "gB":
                return go_stone("black")
            case "gW":
                return go_stone("white")
            case "b":
                return chess_piece("bishop_black")
            case "B":
                return chess_piece("bishop_white")
            case _:
                raise NotImplementedError(f"Piece type {piece_name} is not pre-defined")

    def setup_board(self):
        """Create board_layout for the required grid"""
        from protograf.protos import Layout, square, Hexagons

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
                    _shapes.append(
                        square(
                            side=self.cell_size,
                            stroke=self.strokes[key],
                            fill=colr,
                        )
                    )
                Layout(self.board_layout, shapes=_shapes, _draw_grid=False)
                # ---- set default label ID attributes
                for row in range(self.rows, 0, -1):
                    for col in range(1, self.cols + 1):
                        col_id = tools.sheet_column(col, lower=True)
                        setattr(
                            self, f"{col_id}{row}", self.board_layout.cells[(col, row)]
                        )
            case "hex":
                self.game_name_error()
            case "hexhex":
                self.game_name_error()
            case "hexagons":
                self.board_layout = Hexagons(
                    cols=self.cols,
                    rows=self.rows,
                    x=top_x,
                    y=top_y,
                    orientation="pointy",
                    _draw_grid=False,
                )
                # ---- set default label ID attributes
                for row in range(1, self.rows + 1):
                    for col in range(1, self.cols + 1):
                        # assuming start at bottom row as 1
                        col_row = geoms.hexgrid_diagonal_coords(
                            col=col, row=row, total_rows=self.rows
                        )
                        print(f"{col=} {row=}", col_row)
                        try:
                            setattr(
                                self,
                                f"{col_row[0]}{col_row[1]}",
                                self.board_layout.cells[(col, row)],
                            )
                        except:
                            print(col, row)
            case _:
                self.game_name_error()

    def setup_pieces(self, pieces_type: str = None, pieces_list: list = None) -> dict:
        """Return pieces mapped as character:shape(s)."""
        if pieces_type is None and not pieces_list:
            pieces_type = "checkers"  # Default!
        pg_pieces = {}
        match pieces_type:
            case "checkers" | "draughts":
                pg_pieces = {
                    "B": self.character_map("cB"),
                    "W": self.character_map("cW"),
                }
            case "chess":
                pg_pieces = {  # TODO - load ALL images from resources
                    "B": self.character_map("B"),
                    "b": self.character_map("b"),
                    "K": self.character_map("K"),
                    "k": self.character_map("k"),
                    "N": self.character_map("N"),
                    "n": self.character_map("n"),
                    "P": self.character_map("P"),
                    "p": self.character_map("p"),
                    "Q": self.character_map("Q"),
                    "q": self.character_map("q"),
                    "R": self.character_map("R"),
                    "r": self.character_map("r"),
                }
            case "go":
                pg_pieces = {  # TODO - load images from resources
                    "B": self.character_map("gB"),
                    "W": self.character_map("gW"),
                }
            case "shogi":
                pg_pieces = {  # TODO - load images from resources
                    "A": self.character_map("sA"),
                    "a": self.character_map("sa"),
                    "B": self.character_map("sB"),
                    "b": self.character_map("sb"),
                    "D": self.character_map("sD"),
                    "d": self.character_map("sd"),
                    "G": self.character_map("sG"),
                    "g": self.character_map("sg"),
                    "H": self.character_map("sH"),
                    "h": self.character_map("sh"),
                    "J": self.character_map("sJ"),
                    "j": self.character_map("sj"),
                    "K": self.character_map("sK"),
                    "k": self.character_map("sk"),
                    "l": self.character_map("sl"),
                    "L": self.character_map("sL"),
                    "N": self.character_map("sN"),
                    "n": self.character_map("sn"),
                    "P": self.character_map("sP"),
                    "p": self.character_map("sp"),
                    "R": self.character_map("sR"),
                    "r": self.character_map("sr"),
                    "S": self.character_map("sS"),
                    "s": self.character_map("ss"),
                    "T": self.character_map("sT"),
                    "t": self.character_map("st"),
                    "V": self.character_map("sV"),
                    "v": self.character_map("sv"),
                    "W": self.character_map("sW"),
                    "w": self.character_map("sw"),
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
                    match game:
                        case "checkers":
                            match pcolor:
                                case "black":
                                    pg_pieces[piece_id] = self.character_map("cB")
                                case "white":
                                    pg_pieces[piece_id] = self.character_map("cW")
                        case "chess":
                            match pcolor:
                                case "black":
                                    pg_pieces[piece_id] = self.character_map(pname)
                                case "white":
                                    pg_pieces[piece_id] = self.character_map(
                                        pname.upper()
                                    )
                        case "go":
                            match pcolor:
                                case "black":
                                    pg_pieces[piece_id] = self.character_map("gB")
                                case "white":
                                    pg_pieces[piece_id] = self.character_map("bW")
                        case _:
                            feedback(
                                "The AbstractGame named for piece must be"
                                " from one of the following games: "
                                f" Chess, Go, or Checkers (not '{self.name}').",
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
        self.moves = kwargs.get("moves", None)
        self.annotations = kwargs.get("annotations", None)
        self.position_shapes = []
        self._validate_choices()
        # ---- set positions
        self.position_matrix = self.process_positions()

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
        # ---- handle special positions
        match _lower(self.positions):
            case "setup":
                match _lower(self.board.name):
                    case "chess":
                        self.positions = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
                    case "checkers":
                        self.positions = (
                            "1B1B1B1B/B1B1B1B1/1B1B1B1B/8/8/W1W1W1W1/1W1W1W1w/W1W1W1W1"
                        )
                    case "go":
                        self.positions = ""
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
                                " so no predefined setup can be determined.",
                                True,
                                True,
                            )
            case "clear":
                self.positions = ""
            case _:
                pass  # leave "as is" for processing
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
                row = "." * self.board.cols
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

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw the AbstractStateObject on a given canvas."""
        from protograf.protos import Layout, square

        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- draw board
        _shapes = []
        match _lower(self.board.name):
            case "grid" | "chess" | "checkers" | "go" | "shogi":  # default is grid
                for key, colr in enumerate(self.board.fills):
                    _shapes.append(
                        square(
                            side=self.board.cell_size,
                            stroke=self.board.strokes[key],
                            fill=colr,
                        )
                    )
                Layout(self.board.board_layout, shapes=_shapes)
            case "hexagons":
                self.board.board_layout._draw_grid = True
                self.board.board_layout.draw_layout()
            case _:
                feedback(
                    f"The AbstractState 'board' property '{self.board.name}' cannot be drawn.",
                    True,
                    True,
                )
        # ---- link board cell geometry to a label ID
        # board.board_layout.cells should contain indexed cell geometry, after drawing!
        # print('abstracts 734 cells', self.board.board_layout.cells)
        for row in range(self.board.rows, 0, -1):
            for col in range(1, self.board.cols + 1):
                col_id = tools.sheet_column(col, lower=True)
                setattr(
                    self.board,
                    f"{col_id}{row}",
                    self.board.board_layout.cells[(col, row)],
                )
        # ---- draw pieces
        if self.board.pieces and self.position_matrix:
            pass
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
            pass
        # TOOD - use the board.cells property - {{col,row}}=centre_point to draw piece
        print("TODO: draw pieces")

        # ---- draw annotations
        for anno in self.annotations:
            if not isinstance(anno, BaseShape):
                feedback(
                    "The AbstractGame 'annotations' property must be a list of shapes, "
                    f" not a '{type(self.board.pieces).__name__}'.",
                    True,
                    True,
                )
            anno.draw()
