# -*- coding: utf-8 -*-
"""
protograf Class for layout of Hexagons on a grid
"""

# lib

# module
from protograf import globals
from protograf.proto import hexagon, Hexagon
from protograf.shapes_hexagon import HexShape
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

# locale
from .proto_grid import ProtografGrid


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
        self.hex_layout = kwargs.get("hex_layout")
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

    def draw_hexagons(
        self, rows: int, cols: int, stop: int, the_cols: list, odd_mid: bool = True
    ):
        """Draw rows of hexagons for each column in `the_cols`"""
        locales = None
        sequence = 0
        top_row = 0
        end_row = rows - 1
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
                    hxgn = hexagon(
                        row=row,
                        col=ccol - 1,
                        hex_rows=rows,
                        hex_cols=cols,
                        **self.kwargs,
                    )
                    hxgn.draw()
                    shape_geo = self.get_geometry(hxgn)
                    _locale = Locale(
                        col=ccol - 1,
                        row=row,
                        x=hxgn.grid.x,
                        y=hxgn.grid.y,
                        cxy=Point(hxgn.grid.x, hxgn.grid.y),
                        geo=shape_geo,
                        id=f"{ccol - 1}:{row}",
                        sequence=sequence,
                        label=hxgn.grid.label,
                        page=globals.page_count + 1,
                    )
                    # print(f'$$$ locale {ccol=} {_row=} / {hxgn.grid.x=} {hxgn.grid.y=}')
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
        sequence = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if self.hidden and (row + 1, col + 1) in self.hidden:
                    pass
                else:
                    hxgn = Hexagon(
                        row=row,
                        col=col,
                        hex_rows=self.rows,
                        hex_cols=self.cols,
                        **self.kwargs,
                    )
                    shape_geo = self.get_geometry(hxgn)
                    _locale = Locale(
                        col=col,
                        row=row,
                        x=hxgn.grid.x,
                        y=hxgn.grid.y,
                        cxy=Point(hxgn.grid.x, hxgn.grid.y),
                        geo=shape_geo,
                        id=f"{col}:{row}",
                        sequence=sequence,
                        label=hxgn.grid.label,
                        page=globals.page_count + 1,
                    )
                    # print(
                    #     f"$$$ Locale {id=} {col=} {row=} {hxgn.grid.x=} {hxgn.grid.y=}"
                    # )
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
        match self.hex_layout:
            case "c", "cir", "circle":
                return self.draw_layout_circle()
            case "d", "dia", "diamond":
                self.draw_layout_diamond()
            case "t", "tri", "triangle":
                self.draw_layout_triangle()
            case "l", "loz", "stadium":
                self.draw_layout_stadium()
            case _:  # default to rectangular layout
                self.draw_layout_rectangle()

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
