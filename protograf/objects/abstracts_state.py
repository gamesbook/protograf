# -*- coding: utf-8 -*-
"""
protograf AbstractState class

Notes:
    * all arrays, such the cells of a board, are (col,row) with 1-based values
"""

# lib
import math
import re

# third party

# module
from protograf import globals
from protograf.base import BaseShape
from protograf.shapes import ImageShape
from protograf.utils import tools
from protograf.utils.messaging import feedback
from protograf.utils.structures import (  # named tuples; enums
    AbstractBoardType,
    Point,
    ShapeGeometry,
)
from protograf.utils.tools import _lower

# local
from .abstracts_game import AbstractGameObject


class AbstractStateObject(BaseShape):
    """Draw AbstractState composite shape on a given canvas."""

    def __init__(self, _object=None, canvas=None, **kwargs):
        super().__init__(_object=_object, canvas=canvas, **kwargs)
        # self.kwargs = kwargs
        # self.set_unit_properties()
        # self.cnv = (
        #     canvas if canvas else globals.canvas
        # )  # a new Page/Shape may now exist
        # ---- unique properties
        self.board = self._commons("board") or kwargs.get("board") or None
        self.positions = self._commons("positions") or kwargs.get("positions") or "."
        self.setup = self._commons("setup") or kwargs.get("setup") or False
        self.setup = tools.as_bool(self.setup, False)
        self.moves = self._commons("moves") or kwargs.get("moves") or None
        self.markers = self._commons("markers") or kwargs.get("markers") or None
        self.markers_stroke = (
            self._commons("markers_stroke") or kwargs.get("markers_stroke") or "yellow"
        )
        self.markers_fraction = (
            self._commons("markers_fraction") or kwargs.get("markers_fraction") or 0.1
        )
        self.markers_fraction = tools.as_float(
            self.markers_fraction, "markers_fraction", minimum=0
        )
        self.markers_transparency = (
            self._commons("markers_transparency")
            or kwargs.get("markers_transparency")
            or 1
        )
        self.markers_transparency = tools.as_float(
            self.markers_transparency, "markers_transparency", minimum=0
        )
        self.markers_shapes = (
            self._commons("markers_shapes") or kwargs.get("markers_shapes") or None
        )
        self.annotations = (
            self._commons("annotations") or kwargs.get("annotations") or None
        )
        # --- internal properties
        self.position_shapes = []
        self._validate_choices()
        # ---- set positions
        self.positions = self.initialise_pieces()
        self.position_matrix = self.process_positions()

    def game_name_error(self):
        """Generate feedback if incorrect game name used."""
        feedback(
            "The AbstractGame 'name' property must be one of the following: "
            f" Chess, Go, Checkers, Shogi, Hex, HexHex, or grid (not '{self.board.name}').",
            True,
            True,
        )

    def initialise_pieces(self) -> str:
        """Create initial positions."""
        if self.setup:
            match _lower(self.board.name):
                case "chess":  # white at the bottom
                    return "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
                case "checkers" | "draughts":  # white at the bottom
                    return "1R1R1R1R/R1R1R1R1/1R1R1R1R/8/8/W1W1W1W1/1W1W1W1W/W1W1W1W1"
                case "go":
                    return ""
                case "shogi" | "shogi-int":  # white at the top
                    return "LNSGKGSNL/1R5B1/PPPPPPPPP/9/9/9/ppppppppp/1b5r1/lnsgkgsnl"
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
        if self.markers is not None:
            if not isinstance(self.markers, (list, tuple)):
                feedback(
                    "The AbstractState 'markers' property must be a list of elements, "
                    f" not a '{type(self.markers).__name__}'.",
                    True,
                    True,
                )
        if self.markers_shapes is not None:
            if not isinstance(self.markers_shapes, (list, tuple)):
                feedback(
                    "The AbstractState 'markers_shapes' property must be a list of elements, "
                    f" not a '{type(self.markers_shapes).__name__}'.",
                    True,
                    True,
                )
        if self.annotations is not None:
            if not isinstance(self.annotations, (list, tuple)):
                feedback(
                    "The AbstractState 'annotations' property must be a list of elements, "
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

    def process_positions(self) -> list:
        """Convert positions into a list of AbstractPiece objects."""
        if self.positions is None or self.positions == "":
            return []
        if "/" in self.positions and "\n" in self.positions:
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
        elif "\n" in self.positions:
            _position_list = self.positions.split("\n")
        else:
            if self.positions != ".":  # the default - used internally
                feedback(
                    "Neither '/' or line-break were specified for AbstractState 'positions',"
                    " so only a single row will be processed.",
                    False,
                )
            _position_list = self.positions
        # ---- clean list
        position_list = [row.strip() for row in _position_list if row]
        position_list = [row for row in position_list if row]
        # ---- validate list of item positions
        # TODO - improve these checks for hexhex board as well as irregular hexagonal
        if position_list and len(position_list) != self.board.rows:
            if self.positions != ".":  # the default - internal use
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
                non_blanks = len(self.board.cells_non_blank[key])
                if len(row) < non_blanks:
                    feedback(
                        "Not all columns have been set for available cells"
                        f" in row#{key + 1} of the"
                        f" AbstractState 'positions' ({len(row)} vs {non_blanks}).",
                        False,
                    )
                if len(row) > non_blanks:
                    feedback(
                        "There are too many columns for available cells"
                        f" in row#{key + 1} of the AbstractState"
                        f" 'positions' ({len(row)} vs {non_blanks}).",
                        True,
                        True,
                    )
        return position_list

    def draw_single_element(self, mark: str, grid_refs: list):
        """Draw one element on the board."""
        from protograf.protos import Circle, Dot, Hexagon, Line, Square

        def check_grid(grid_refs: list, name: str = "line", points: float = 2):
            """Ensure enough grid points to draw the shape."""
            if len(grid_refs) < points:
                feedback(
                    f'The AbstractGame "markers" shortcut for a {name}'
                    f" needs {points} grid references.",
                    True,
                    True,
                )

        cntr0 = grid_refs[0].centre
        ht = grid_refs[0].height
        rd = ht / 2.0
        ht_pts = float(ht) * self.units

        # default props
        stroke = self.markers_stroke
        stroke_width = ht_pts * self.markers_fraction
        stroke_transparency = self.markers_transparency
        offset = tools.points(stroke_width) / 2.0
        def_kwargs = {
            "stroke": stroke,
            "stroke_width": stroke_width,
            "stroke_transparency": stroke_transparency,
        }
        # user props
        usr_kwargs = {}
        # If duplicate keys, the last dictionary unpacked overwrites previous values.

        # multiple grid_refs => used for line or arrow
        grid_locs = [loc.centre for loc in grid_refs]

        # ---- color-in-a-cell
        if mark[0] == "#":  # color-in a cell
            match self.board.board_type:
                case AbstractBoardType.GRID:
                    skwargs = {
                        "x": None,
                        "y": None,
                        "fill": mark,
                        "stroke": mark,
                        "height": ht - 2 * offset,
                        "width": ht - 2 * offset,
                    }
                    for loc in grid_locs:
                        kwargs = {**def_kwargs, **usr_kwargs, **skwargs, "cxy": loc}
                        Square(**kwargs)
                case AbstractBoardType.HEXAGONAL:
                    hkwargs = {
                        "x": None,
                        "y": None,
                        "fill": mark,
                        "stroke": mark,
                        "height": ht - 2 * offset,
                        "orientation": "pointy",
                    }
                    for loc in grid_locs:
                        kwargs = {**def_kwargs, **usr_kwargs, **hkwargs, "cxy": loc}
                        Hexagon(**kwargs)
                case AbstractBoardType.TRIANGULAR:
                    raise NotImplementedError(
                        "Sorry, a triangular board is not available yet."
                    )
                case _:
                    self.game_name_error()
            return

        # ---- draw a shape
        match mark.lower():
            case "a" | "ac":  # arrow / curved
                check_grid(grid_refs, "arrow (a)", 2)
                if grid_locs:
                    akwargs = {"links": grid_locs, "stroke_ends": "rounded"}
                else:
                    cntr1 = grid_refs[1].centre
                    akwargs = {
                        "x": cntr0.x,
                        "y": cntr0.y,
                        "x1": cntr1.x,
                        "y1": cntr1.y,
                        "arrow": True,
                        "stroke_ends": "rounded",
                    }
                    if mark.lower() == "ac":
                        curve_height = (
                            math.dist((cntr0.x, cntr0.y), (cntr1.x, cntr1.y)) * 0.2
                        )
                        akwargs["curve"] = curve_height

                kwargs = {**def_kwargs, **usr_kwargs, **akwargs}
                Line(**kwargs)
            case "c":  # circle
                ckwargs = {
                    "x": cntr0.x,
                    "y": cntr0.y,
                    "radius": rd - offset,
                    "orientation": "pointy",
                }
                for loc in grid_locs:
                    kwargs = {**def_kwargs, **usr_kwargs, **ckwargs, "cxy": loc}
                    Circle(**kwargs)
            case "d":  # dot
                dkwargs = {
                    "x": cntr0.x,
                    "y": cntr0.y,
                    "dot_width": stroke_width,
                }
                for loc in grid_locs:
                    kwargs = {**def_kwargs, **usr_kwargs, **dkwargs, "cxy": loc}
                    Dot(**kwargs)
            case "h":  # hexagon
                hkwargs = {
                    "x": None,
                    "y": None,
                    "height": ht - 2 * offset,
                    "orientation": "pointy",
                }
                for loc in grid_locs:
                    kwargs = {**def_kwargs, **usr_kwargs, **hkwargs, "cxy": loc}
                    Hexagon(**kwargs)
            case "s":  # square
                skwargs = {
                    "x": None,
                    "y": None,
                    "height": ht - 2 * offset,
                    "width": ht - 2 * offset,
                }
                for loc in grid_locs:
                    kwargs = {**def_kwargs, **usr_kwargs, **skwargs, "cxy": loc}
                    Square(**kwargs)
            case "l" | "lc":  # line / curve
                check_grid(grid_refs, "line (l)", 2)
                if grid_locs:
                    lkwargs = {"links": grid_locs, "stroke_ends": "rounded"}
                else:
                    cntr1 = grid_refs[1].centre
                    lkwargs = {
                        "x": cntr0.x,
                        "y": cntr0.y,
                        "x1": cntr1.x,
                        "y1": cntr1.y,
                        "stroke_ends": "rounded",
                    }
                    if mark.lower() == "lc":
                        curve_height = (
                            math.dist((cntr0.x, cntr0.y), (cntr1.x, cntr1.y)) * 0.2
                        )
                        lkwargs["curve"] = curve_height

                kwargs = {**def_kwargs, **usr_kwargs, **lkwargs}
                Line(**kwargs)
            case "x":  # cross "X"
                match self.board.board_type:
                    case AbstractBoardType.GRID:
                        for loc in grid_refs:
                            xkwargs = {
                                "x": loc.sw.x + offset,
                                "y": loc.sw.y - offset,
                                "x1": loc.ne.x - offset,
                                "y1": loc.ne.y + offset,
                                "stroke_ends": "rounded",
                            }
                            kwargs = {**def_kwargs, **usr_kwargs, **xkwargs}
                            Line(**kwargs)
                            zkwargs = {
                                "x": loc.nw.x + offset,
                                "y": loc.nw.y + offset,
                                "x1": loc.se.x - offset,
                                "y1": loc.se.y - offset,
                                "stroke_ends": "rounded",
                            }
                            kwargs = {**def_kwargs, **usr_kwargs, **zkwargs}
                            Line(**kwargs)
                    case AbstractBoardType.HEXAGONAL:
                        for loc in grid_refs:
                            xkwargs = {
                                "x": loc.sw.x + offset,
                                "y": loc.sw.y - offset,
                                "x1": loc.ne.x - offset,
                                "y1": loc.ne.y + offset,
                                "stroke_ends": "rounded",
                            }
                            kwargs = {**def_kwargs, **usr_kwargs, **xkwargs}
                            Line(**kwargs)
                            zkwargs = {
                                "x": loc.nw.x + offset,
                                "y": loc.nw.y + offset,
                                "x1": loc.se.x - offset,
                                "y1": loc.se.y - offset,
                                "stroke_ends": "rounded",
                            }
                            kwargs = {**def_kwargs, **usr_kwargs, **zkwargs}
                            Line(**kwargs)
                    case AbstractBoardType.TRIANGULAR:
                        raise NotImplementedError(
                            "Sorry, a triangular board is not available yet."
                        )
                    case _:
                        self.game_name_error()

    def process_multiple_elements(self, mark: str, elements_group: str):
        """."""
        allowed_marks = ["a", "ac", "c", "d", "h", "x", "s", "l", "lc"]
        marks = tools.sequence_split(
            mark, sep=" ", to_int=False, unique=False, clean=True
        )
        if marks[0].lower() not in allowed_marks and marks[0][0] != "#":
            feedback(
                f'The AbstractGame "{elements_group}" shortcut must start with one of'
                f' "{allowed_marks}", or be a color, not "{marks[0]}".',
                True,
                True,
            )
        if len(marks) < 2:
            feedback(
                f'The AbstractGame "{elements_group}" shortcut must contain a key, or color'
                f' followed by one or more grid references, not "{mark}".',
                True,
                True,
            )
        grid_refs = []
        for _grid_mark in marks[1:]:
            if _grid_mark == "":
                continue
            try:
                _grid = getattr(self.board, _grid_mark.lower())
                grid_refs.append(_grid)
            except AttributeError:
                try:
                    _grid = getattr(self.board, _grid_mark.upper())
                    grid_refs.append(_grid)
                except AttributeError:
                    feedback(
                        f'The AbstractGame "{elements_group}" shortcut grid reference'
                        f' "{_grid_mark}" is a not valid for this game.',
                        True,
                        True,
                    )
        if grid_refs:
            self.draw_single_element(marks[0], grid_refs)

    def draw_annotations(self):
        """Draw annotation elements on the board."""
        if self.annotations:
            for anno in self.annotations:
                if isinstance(anno, str):
                    self.process_multiple_elements(
                        mark=anno, elements_group="annotations"
                    )
                elif isinstance(anno, BaseShape):
                    anno.draw()
                else:
                    feedback(
                        "The AbstractState 'annotations' property must be a list of shapes, "
                        f" or a string, not a '{type(anno).__name__}'.",
                        True,
                        True,
                    )

    def draw_markers(self):
        """Draw marker elements on the board."""
        for mark in self.markers:
            if isinstance(mark, str):
                self.process_multiple_elements(mark=mark, elements_group="markers")
            elif isinstance(mark, BaseShape):
                mark.draw()
            else:
                feedback(
                    "The AbstractGame 'markers' property must be a list of shapes, "
                    f" or shortcut strings, not a '{type(mark).__name__}'.",
                    True,
                    True,
                )

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
                if col == ".":
                    # print(f'&&& AbstractState {row_no=},{col_no=} : BLANK')
                    continue  # no piece here; move along, move along
                kwargs = {}
                piece_shp = self.board.pieces.get(col, None)
                # print(f'&&& AbstractState {row_no=},{col_no=} :', piece_shp)
                # ---- NULL shape
                if piece_shp is None:
                    feedback(
                        item=f"Unable to find the piece named '{col}'; "
                        f" please check the 'positions' for '{self.board.name}'.",
                        warn=False,
                        alert=True,
                        stop=True,
                    )
                else:
                    # ---- get cell location
                    # cell = self.board.board_layout.cells.get((col_no + 1, row_no + 1))
                    the_cell = self.board.cells_non_blank[row_no][col_no]  # 0-based!
                    cell_col, cell_row = the_cell[0], the_cell[1]
                    cell = self.board.board_layout.cells.get((cell_col, cell_row))
                    # ---- set Image shape props
                    if isinstance(piece_shp, ImageShape):
                        bbox = cell.bbox  # geo ~ user units ~ relative to margin
                        if bbox:
                            # define absolute position on page
                            kwargs = {
                                "_abs_x": tools.unit(bbox.tl.x + globals.margins.left),
                                "_abs_y": tools.unit(bbox.tl.y + globals.margins.top),
                            }
                        else:
                            feedback(
                                "Unable to properly draw Images on the board;"
                                " no BoundingBox is provided!",
                                True,
                                True,
                            )
                    # ---- set Other shape props
                    elif isinstance(piece_shp, BaseShape):
                        cntr = cell.centre  # geo ~ user units ~ relative to margin
                        kwargs = {
                            "_abs_cx": tools.unit(cntr.x + globals.margins.left),
                            "_abs_cy": tools.unit(cntr.y + globals.margins.top),
                        }
                    else:
                        raise NotImplementedError(
                            f'Unable to draw a piece of type "{type(piece_shp)}"'
                        )
                    # print(f'&&& AbstractState {row_no=},{col_no=} P:', type(piece_shp))
                    # ---- draw shape
                    piece_shp.draw(**kwargs)

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw the AbstractStateObject on a given canvas."""
        from protograf.protos import Layout

        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- draw the board frame
        if self.board.frame is True:
            self.board.draw_frame()
        # ---- draw the board
        match _lower(self.board.name):
            case "grid" | "chess" | "checkers" | "go" | "shogi":  # default name is grid
                if self.board.intersections:
                    Layout(
                        self.board.board_layout,
                        shapes=None,
                        # debug="colrow",  (for testing only!)
                        draw_lines=True,
                        **self.board.grid_kwargs,
                    )
                else:
                    Layout(
                        self.board.board_layout,
                        shapes=self.board.areas,
                        # debug="colrow",  (for testing only!)
                        **kwargs,
                    )
            case "hexagons" | "hex" | "hexhex" | "hexagonal" | "hexes" | "hex":
                self.board.board_layout._draw_grid = True
                self.board.board_layout.draw_layout()
            case _:
                feedback(
                    f"No available logic to draw AbstractState board '{self.board.name}'",
                    True,
                    True,
                )
        # ---- draw the board labels
        if self.board.label is True:
            self.board.draw_labels()
        # ---- draw the annotations on the board
        if self.annotations:
            self.draw_annotations()
        # ---- draw the pieces
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
        # ---- draw the state markers
        if self.markers:
            self.draw_markers()
