# -*- coding: utf-8 -*-
"""
protograf CoreGameObject for games

Notes:
    * all arrays, such the cells of a board, are (col,row) with 1-based values
"""

# lib
import re

# third party

# module
from protograf import globals
from protograf.base import BaseShape
from protograf.utils import tools, geoms
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


class CoreGameObject(BaseShape):
    """Create a GameObject for a given canvas."""

    def __init__(self, _object=None, canvas=None, **kwargs):

        super().__init__(_object=_object, canvas=canvas, **kwargs)
        # self.kwargs = kwargs
        # self.set_unit_properties()
        # self.cnv = (
        #     canvas if canvas else globals.canvas
        # )  # a new Page/Shape may now exist
        # ---- unique properties
        self.name = self._commons("name") or kwargs.get("name") or "grid"
        self.cell_shape = (
            self._commons("cell_shape") or kwargs.get("cell_shape") or None
        )
        self.cell_size = self._commons("height") or kwargs.get("height") or 1
        self.cell_size = tools.as_float(self.cell_size, "height")
        self.areas = (
            self._commons("areas") or kwargs.get("areas") or None
        )  # MUST be none; set by user
        self.fills = (
            self._commons("fills") or kwargs.get("fills") or None
        )  # MUST be none; set by user OR game
        self.frame = self._commons("frame") or kwargs.get("frame") or False
        self.pattern = self._commons("pattern") or kwargs.get("pattern") or None
        self.intersections = (
            self._commons("intersections") or kwargs.get("intersections") or False
        )
        # if not self.label
        self.label = self._commons("label") or kwargs.get("label") or None
        self.label_start = (
            self._commons("label_start") or kwargs.get("label_start") or None
        )
        self.label_type = (
            self._commons("label_type") or kwargs.get("label_type") or None
        )
        self.label_uppercase = (
            self._commons("label_uppercase") or kwargs.get("label_uppercase") or False
        )
        self.label_lower = not self.label_uppercase
        self.label_offset = tools.as_float(
            kwargs.get("label_offset", 0), "label_offset"
        )
        self.label_offset_col = tools.as_float(
            kwargs.get("label_offset_col", self.label_offset), "label_offset_col"
        )
        self.label_offset_row = tools.as_float(
            kwargs.get("label_offset_row", self.label_offset), "label_offset_row"
        )

        self.pieces = self._commons("pieces") or kwargs.get("pieces") or []
        self.pieces_type = (
            self._commons("pieces_type") or kwargs.get("pieces_type") or None
        )  # Shogi can change!
        self.hexes = (
            self._commons("hexes") or kwargs.get("hexes") or 2
        )  # override default in base.py
        self.hexes = tools.as_int(self.hexes, "hexes", minimum=2, allow_none=True)
        # ---- custom / internal properties
        self.grid_kwargs = {}  # used when drawing intersections lines
        # ---- calculated properties
        # ---- cell dimensions: side of square; hexagon/triangle height; circle diameter
        if self._commons("height") or kwargs.get("height"):
            self.auto_size = False
            self.page_width = None
            self.page_height = None
        else:
            self.auto_size = True
            self.page_width = (
                globals.page.width - globals.margins.left - globals.margins.right
            )
            self.page_height = (
                globals.page.height - globals.margins.top - globals.margins.bottom
            )
        self.cells_non_blank = []  # (col,row) pairs of non-blank cells PER ROW
        self.hexgrid_diagonals = None  # hexes in a diagonal
        self.hexgrid_alpha_coords = None  # grid coordinates dict, keyed on (col,row)
        # ---- NULL defaults; set in Child class
        self.game_class = None
        self.board_pattern = None
        self.board_type = None
        self.orientation = None

    def hexhex_size(self, text) -> int:
        """Find one or more digits at the end of the string."""
        match = re.search(r"\d+$", text)
        if match:
            number = match.group()
            return int(number)

    def hexhex_pattern(self, side: int = 2) -> str:
        """Create a O-and-. pattern layout for a hexhex board.

        Args:
            side (int): number of hexagons along an edge
        """

        def _split_gap(number: int):
            if number % 2 != 0:  # odd
                return number // 2, number // 2 + 1
            return number // 2, number // 2  # even

        width = side * 2 - 1
        row_size = side
        add = True
        hexes = ""
        even = 0
        while True:
            gap = width - row_size
            small, big = _split_gap(gap)
            prefix = " " if even else ""
            if side % 2 != 0:  # odd side
                hexes += prefix + ". " * small + "O " * row_size + ". " * big + "\n"
            else:  # even side
                hexes += prefix + ". " * big + "O " * row_size + ". " * small + "\n"
            even = 1 if even != 1 else 0
            if add:
                row_size += 1
            else:
                row_size -= 1
            if row_size == width:
                add = False
            if row_size < side:
                break
        # print(f'&&& {hexes=}')
        return hexes

    def game_name_error(self):
        """Generate feedback if incorrect game name used."""
        pass

    def set_options_by_game(self, **kwargs):
        """Set properties according to preset, known, game."""
        pass

    def _validate_choices(self) -> bool:
        """Check and reset user choices for valid selections."""
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
                    user="AbstractGame",
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

    def setup_pieces(self, pieces_type: str = None, pieces_list: list = None) -> dict:
        """Return pieces mapped as character:shape(s)."""
        pass
