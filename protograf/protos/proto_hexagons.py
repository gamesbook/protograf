# -*- coding: utf-8 -*-
"""
protograf Class for layout of Hexagons on a grid
"""

# lib
import re

# project
from protograf import globals
from protograf.shapes import HexShape
from protograf.utils import tools  # , geoms, support
from protograf.utils.messaging import feedback
from protograf.utils.tools import _lower
from protograf.utils.structures import (
    # HEX_FLAT_EDGE_TRAVEL,
    # HexOrientation,
    Locale,
    Point,
    ShapeGeometry,
)
from protograf.utils.abstracts import ProtografGrid

# local
from . import utils  # globals_set, validate_globals, margins


class Hexagons(ProtografGrid):
    """Draw multiple copies of a Hexagon across rows and columns."""

    def __init__(self, rows=1, cols=1, **kwargs):
        """
        Kwrgs:

        - sides (int): the number of hexagons along the edge of a HexHex frame
        - hidden: a list of hidden hexagons

        Notes:

        The same kwargs as used for a Hexagon shape can be applied here.

        """
        super().__init__(rows=rows, cols=cols, **kwargs)
        self.sides = kwargs.get("sides", 0)
        self.hidden = None
        if kwargs.get("hidden"):
            self.hidden = tools.integer_pairs(kwargs.get("hidden"), "hidden")
        self._draw_grid = kwargs.get("_draw_grid", False)
        self.hex_layout = kwargs.get("hex_layout", "")  # default to rectangular
        self.pattern = kwargs.get("pattern", None)  # used by AbstractGame
        self.user = kwargs.get("user", "Hexagons")  # the calling Shape
        self.locales = []  # will be created by specific draw_* method
        self.draw_layout()

    def get_geometry(self, hexgn: HexShape) -> ShapeGeometry:
        shape_geometry = ShapeGeometry(  # keep in user units for GridLine
            centre=hexgn.geo.centre,
            center=hexgn.geo.centre,
            c=hexgn.geo.centre,
            height=hexgn.geo.height,
            side=hexgn.geo.side,
            # vertices  // FLAT
            ne=hexgn.geo.ne,
            se=hexgn.geo.se,
            e=hexgn.geo.e,
            w=hexgn.geo.w,
            sw=hexgn.geo.sw,
            nw=hexgn.geo.nw,
            # perbii // FLAT
            n=hexgn.geo.n,
            s=hexgn.geo.s,
            wnw=hexgn.geo.wnw,
            ene=hexgn.geo.ene,
            ese=hexgn.geo.ese,
            wsw=hexgn.geo.wsw,
        )
        return shape_geometry

    def process_pattern(self, hex_rows, hex_cols) -> list:
        """Convert pattern into a list structure."""
        if self.pattern is None or self.pattern == "":
            return []
        if "/" in self.pattern and "\n" in self.pattern:
            feedback(
                "Do not mix '/' and line-breaks for {self.user} 'pattern'.",
                True,
                True,
            )
            return []
        # ---- list of items in pattern
        if "/" in self.pattern:
            position_std = re.sub(r"\d", lambda m: "." * int(m.group()), self.pattern)
            _pattern_list = position_std.split("/")
        elif "\n" in self.pattern:
            _pattern_list = self.pattern.split("\n")
        else:
            feedback(
                f"Neither '/' or line-break were specified for {self.user} 'pattern',"
                " so only a single row will be processed.",
                False,
            )
            _pattern_list = self.pattern
        # ---- clean list
        pattern_list = [row.strip() for row in _pattern_list if row]
        pattern_list = [row.replace(" ", "") for row in pattern_list if row]
        pattern_list = [row.replace("\t", "") for row in pattern_list if row]
        pattern_list = [row for row in pattern_list if row]
        # ---- validate pattern list
        if pattern_list and len(pattern_list) != hex_rows:
            if len(pattern_list) < hex_rows:
                feedback(
                    f"Not all rows have been set for the {self.user} 'pattern'"
                    f" ({len(pattern_list)} vs {hex_rows}).",
                    False,
                )
            if len(pattern_list) > hex_rows:
                feedback(
                    f"There are too many rows for the {self.user} 'pattern'"
                    f" ({len(pattern_list)} vs {hex_rows}).",
                    True,
                    True,
                )
        for key, row in enumerate(pattern_list):
            if row == "O" or row == "o":
                row = "O" * int(hex_cols)
                pattern_list[key] = row
            if len(row) != hex_cols:
                if len(row) < hex_cols:
                    feedback(
                        f"Not all columns have been set for row#{key + 1} of the"
                        f" {self.user} 'pattern' ({len(row)} vs {hex_cols}).",
                        False,
                    )
                if len(row) > hex_cols:
                    feedback(
                        f"There are too many columns for row#{key + 1} of the {self.user}"
                        f" 'pattern' ({len(row)} vs {hex_cols}).",
                        True,
                        True,
                    )
        return pattern_list

    def draw_hexagons(
        self, rows: int, cols: int, stop: int, the_cols: list, odd_mid: bool = True
    ):
        """Create rows of hexagons for each column in `the_cols`"""
        from protograf.protos import hexagon

        locales = []
        sequence = 0
        top_row = 0
        end_row = rows - 1
        hex_pattern = self.process_pattern(hex_rows=rows, hex_cols=cols)

        if not odd_mid:
            end_row = rows
            top_row = 1
        for ccol in the_cols:
            top_row = top_row + 1 if ccol & 1 != 0 else top_row  # odd col
            end_row = end_row - 1 if ccol & 1 == 0 else end_row  # even col
            # print('$$$ ccol, top_row, end_row', ccol, top_row, end_row)
            for row in range(top_row - 1, end_row + 1):
                _row = row + 1
                # feedback(f'$$$ Hexagons {ccol=}, {_row=}')
                if self.hidden and (_row, ccol) in self.hidden:
                    pass
                else:
                    col = ccol - 1
                    hxgn = hexagon(
                        row=row,
                        col=col,
                        hex_rows=rows,
                        hex_cols=cols,
                        **self.kwargs,
                    )
                    is_blank = False
                    if hex_pattern:  # test if current col/row in pattern
                        if hex_pattern[row][col] == ".":
                            is_blank = True
                        # feedback(f'$$$ Hexagons:draw_hexag {col=},{row=} {is_blank=}')
                    # test if blank and if skip drawing
                    if self._draw_grid and not is_blank:
                        hxgn.draw()
                    shape_geo = self.get_geometry(hxgn)
                    _locale = Locale(
                        col=ccol - 1,
                        row=row,
                        x=hxgn.grid.x,
                        y=hxgn.grid.y,
                        cxy=Point(hxgn.grid.x, hxgn.grid.y),
                        geo=shape_geo,
                        is_blank=is_blank,
                        id=f"{ccol - 1}:{row}",
                        sequence=sequence,
                        label=hxgn.grid.label,
                        page=globals.page_count + 1,
                    )
                    # print(f'$$$ locale {ccol=} {_row=} / {hxgn.grid.x=} {hxgn.grid.y=}')
                    self.cells[(col, row)] = hxgn.geometry
                    locales.append(_locale)
                    sequence += 1

                if ccol - 1 == stop:  # reached "leftmost" -> reset counters
                    top_row = 1
                    end_row = rows - 1
        return locales

    def draw_layout_circle(self):
        """Layout of hexagons in a circle."""
        if not self.sides and (
            (self.rows is not None and self.rows < 3)
            and (self.cols is not None and self.cols < 3)
        ):
            feedback("The minimum values for rows/cols is 3!", True)
        if self.rows and self.rows > 1:
            self.cols = self.rows
        if self.cols and self.cols > 1:
            self.rows = self.cols
        if self.rows != self.cols:
            self.rows = self.cols
        if self.sides:
            if self.sides < 2:
                feedback("The minimum value for sides is 2!", True)
            self.rows = 2 * self.sides - 1
            self.cols = self.rows
        else:
            if self.rows & 1 == 0:
                feedback("An odd number is needed for rows!", True)
            if self.cols & 1 == 0:
                feedback("An odd number is needed for cols!", True)
            self.sides = self.rows // 2 + 1
        odd_mid = not self.sides & 1 == 0
        the_cols = list(range(self.sides, 0, -1)) + list(
            range(self.sides + 1, self.rows + 1)
        )
        self.locales = self.draw_hexagons(
            rows=self.rows, cols=self.cols, stop=0, the_cols=the_cols, odd_mid=odd_mid
        )

    def draw_layout_diamond(self):
        """Layout of hexagons in a diamond."""
        cols = self.rows * 2 - 1
        the_cols = list(range(self.rows, 0, -1)) + list(range(self.rows + 1, cols + 1))
        self.locales = self.draw_hexagons(
            rows=self.rows, cols=cols, stop=0, the_cols=the_cols
        )

    def draw_layout_rectangle(self):
        """Layout of hexagons in a rectangle."""
        from protograf.protos import hexagon

        sequence = 0
        hex_pattern = self.process_pattern(hex_rows=self.rows, hex_cols=self.cols)
        for row in range(self.rows):
            for col in range(self.cols):
                if self.hidden and (row + 1, col + 1) in self.hidden:
                    pass
                else:
                    hxgn = hexagon(
                        row=row,
                        col=col,
                        hex_rows=self.rows,
                        hex_cols=self.cols,
                        **self.kwargs,
                    )
                    is_blank = False
                    if hex_pattern:  # test if current col/row in pattern
                        if hex_pattern[row][col] == ".":
                            is_blank = True
                        # feedback(f'$$$ Hexagons:draw_layout_rec {col=},{row=} {is_blank=}')
                    # test if blank and skip drawing
                    if self._draw_grid and not is_blank:
                        hxgn.draw()
                    shape_geo = self.get_geometry(hxgn)
                    if hxgn.grid:
                        _x = hxgn.grid.x
                        _y = hxgn.grid.y
                        _label = hxgn.grid.label
                    else:
                        _x = shape_geo.center.x
                        _y = shape_geo.center.y
                        _label = ""
                    _locale = Locale(
                        col=col,
                        row=row,
                        x=_x,
                        y=_y,
                        cxy=Point(_x, _y),
                        geo=shape_geo,
                        is_blank=is_blank,
                        id=f"{col}:{row}",
                        sequence=sequence,
                        label=_label,
                        page=globals.page_count + 1,
                    )
                    self.cells[(col + 1, row + 1)] = hxgn.geometry  # 1-based for cells
                    self.locales.append(_locale)
                    sequence += 1

    def draw_layout_stadium(self):
        """Layout of hexagons in a stadium (lozenge)."""
        feedback(f"Cannot draw stadium-pattern hexagons: {self.kwargs}", True)
        self.locales = []

    def draw_layout_triangle(self):
        """Layout of hexagons in a triangle."""
        feedback(f"Cannot draw triangle-pattern hexagons: {self.kwargs}", True)
        self.locales = []

    def draw_layout(self):
        """Choose and draw a layout of hexagons."""
        orient = self.kwargs.get("orientation")
        if self.hex_layout and orient:
            if not isinstance(orient, str):
                feedback(
                    'Hexagons `orientation` must be a string, not "{orient}"', True
                )
            if _lower(orient) in ["p", "pointy"] and self.hex_layout not in [
                "r",
                "rec",
                "rect",
                "rectangle",
            ]:
                feedback(
                    "Cannot use this Hexagons `hex_layout` with pointy hexagons!", True
                )
        match _lower(self.hex_layout):
            case "c" | "cir" | "circle":
                return self.draw_layout_circle()
            case "d" | "dia" | "diamond":
                return self.draw_layout_diamond()
            case "t" | "tri" | "triangle":
                return self.draw_layout_triangle()
            case "l" | "loz" | "stadium":
                return self.draw_layout_stadium()
            case _:  # default to rectangular layout
                return self.draw_layout_rectangle()

    def cell(self, reference: str | int | tuple) -> Locale:
        """Return details for a single cell in a Hexagons grid.

        Args:
            reference (str | tuple):
                reference a cell either by label (str), sequence (int)
                or col & row (tuple)
        """
        if isinstance(reference, str):
            for loc in self.locales:
                if loc.label == reference:
                    return loc
        elif isinstance(reference, int):
            for loc in self.locales:
                if loc.sequence == reference:
                    return loc
        elif isinstance(reference, tuple):
            if (
                len(reference) == 2
                and isinstance(reference[0], int)
                and isinstance(reference[1], int)
            ):
                for loc in self.locales:
                    if loc.col == reference[0] and loc.row == reference[1]:
                        return loc
            else:
                feedback(
                    "Cell (col,row) reference for Hexagons must be"
                    f' a pair of integers, not "{reference}"',
                    True,
                )
        else:
            feedback(
                f'Cell reference for Hexagons must be a label or (col,row), not "{reference}".',
                True,
            )
        feedback(
            f'Cell reference "{reference}" cannot be located on the Hexagons grid.',
            True,
        )
        return Locale()

    def cxy(self, reference: str | int | tuple) -> Locale:
        """Return centre point, in user units, of a single cell in a Hexagons grid.

        Args:
            reference (str | tuple):
                reference a cell either by label (str), sequence (int)
                or col & row (tuple)
        """
        cell = self.cell(reference)
        return cell.geo.centre
