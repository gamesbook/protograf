# -*- coding: utf-8 -*-
"""
protograf XX18MarketObject class

Notes:

An 18xx Stock Market chart has adjacent rows of rectangular, outlined cells,
of variable length, some offset from the left, and each containing a number
greater than zero.  There is no specific pattern of numbers.

The grid is defined such that:

* the stock value is at a specific location inside each cell
* some cells are colored-in, with different colors in different areas
* some cells are outlined with a thicker line of a different color
* some cells contain an arrow; either up (on the bottom right) or down (on the left)

Markets in different 18xx games have different:

* fonts
* arrow styles
* set of colors

Cells in the grid can sometimes be annotated with a marker or text.
"""

# lib

# third party

# module
from protograf import globals
from protograf.base import BaseShape
from protograf.utils import tools, colrs, geoms
from protograf.utils.messaging import feedback
from protograf.utils.structures import (  # named tuples; enums
    Point,
)
from protograf.utils.tools import _lower

# local
from .core_state import CoreStateObject


class XX18MarketObject(CoreStateObject):
    """Draw XX18Market composite shape on a given canvas."""

    def __init__(self, _object=None, canvas=None, **kwargs):
        super().__init__(_object=_object, canvas=canvas, **kwargs)
        # height and width for cell size:  derived from BaseShape properties
        # x and y for market top-left: derived from BaseShape properties
        # stroke_width and fill for cell: derived from BaseShape properties
        # outline_stroke, outline_width for cell: derived from BaseShape properties
        # font_size, font_name for text: derived from BaseShape properties
        # ---- unique properties
        self.values = (
            self._commons("values") or kwargs.get("values") or []
        )  # 20,1,u,b => value:20; color:1 in market_colors; u:arrow; b:has border/outline
        if not isinstance(self.values, (list, tuple)):
            feedback
        self.game_class = "XX18Market"
        self.value_direction = (
            self._commons("value_direction") or kwargs.get("value_direction") or "c"
        )  # where label is drawn
        self.font_stroke = (
            self._commons("font_stroke") or kwargs.get("font_stroke") or "black"
        )  # used to draw cell values
        self.market_colors = (
            self._commons("market_colors") or kwargs.get("market_colors") or []
        )
        self.arrow = (
            self._commons("arrow") or kwargs.get("arrow") or None
        )  # internal arrow - referenced as 'a'
        self.arrow_down = (
            self._commons("arrow_down") or kwargs.get("arrow_down") or None
        )  # edge arrow - referenced as 'd'
        self.arrow_up = (
            self._commons("arrow_up") or kwargs.get("arrow_up") or None
        )  # edge arrow - referenced as 'u'
        # ---- final check
        self.validate_settings()

    def validate_settings(self):
        """Ensure correct values are set for properties."""
        if self.value_direction:
            if not isinstance(self.value_direction, str):
                feedback(
                    f'The value_direction "{self.value_direction}" is invalid',
                    " for the XX18Market; a string is required.",
                    True,
                    True,
                )
            if _lower(self.value_direction) not in [
                "c",
                "n",
                "ne",
                "nw",
                "s",
                "se",
                "sw",
                "e",
                "w",
            ]:
                feedback(
                    f'The value_direction "{self.value_direction}" is invalid',
                    True,
                    True,
                )

        if self.market_colors:
            for acolor in self.market_colors:
                if not isinstance(acolor, (tuple, list)):
                    feedback(
                        f'The color setting "{acolor}" is invalid for the XX18Market colors;'
                        " at least two, comma-separated values - number,color -"
                        " in a list are required.",
                        True,
                        True,
                    )
                if len(acolor) != 2:
                    feedback(
                        f'The color setting "{acolor}" is invalid for the XX18Market colors;'
                        " exactly two, comma-separated values - number,color - are required.",
                        True,
                        True,
                    )
                if not isinstance(acolor[0], int):
                    feedback(
                        f'The color setting "{acolor}" is invalid for the XX18Market colors;'
                        " the first value must be a number.",
                        True,
                        True,
                    )
                colrs.get_color(acolor[1])  # raises error if color is invalid

        if self.arrow and not isinstance(self.arrow, BaseShape):
            feedback(
                "The arrow property is invalid for the XX18Market;"
                " it must be a protograf shape.",
                True,
                True,
            )
        if self.arrow_down and not isinstance(self.arrow_down, BaseShape):
            feedback(
                "The arrow_down property is invalid for the XX18Market;"
                " it must be a protograf shape.",
                True,
                True,
            )
        if self.arrow_up and not isinstance(self.arrow_up, BaseShape):
            feedback(
                "The arrow_up property is invalid for the XX18Market;"
                " it must be a protograf shape.",
                True,
                True,
            )

    def get_color(self, color_number: str = None) -> object:
        """Return a valid color from list supplied to object."""
        if color_number is not None:
            _color_number = tools.as_int(color_number, "color number")
            for acolor in self.market_colors:
                if acolor[0] == _color_number:
                    return acolor[1]
        return "white"

    def get_label_xy(self, cell: object) -> tuple:
        """Determine Point position to draw label inside Rectangle.

        Args:
            cell (Rectangle): cell into which the label must be drawn

        Returns
            tuple (str, Point):
                text alignment
                Point for text position
        """
        align, point = None, None
        x_g = self.font_size / globals.units / 2.0
        y_g_t = self.font_size / globals.units * 1
        y_g_b = self.font_size / globals.units / 2.0
        y_g_o = self.font_size / globals.units / 4.0
        location = self.value_direction if self.value_direction else "c"
        _value = _lower(location)
        match _value:
            case "c":
                align = "centre"
                point = Point(cell.geo.c.x, cell.geo.c.y + y_g_o)
            case "n":
                align = "centre"
                point = Point(cell.geo.n.x, cell.geo.n.y + y_g_t)
            case "e":
                align = "right"
                point = Point(cell.geo.e.x - x_g, cell.geo.e.y + y_g_o)
            case "w":
                align = "left"
                point = Point(cell.geo.w.x + x_g, cell.geo.w.y + y_g_o)
            case "s":
                align = "centre"
                point = Point(cell.geo.s.x, cell.geo.s.y - y_g_b)
            case "ne":
                align = "right"
                point = Point(cell.geo.ne.x - x_g, cell.geo.ne.y + y_g_t)
            case "nw":
                align = "left"
                point = Point(cell.geo.nw.x + x_g, cell.geo.nw.y + y_g_t)
            case "sw":
                align = "left"
                point = Point(cell.geo.sw.x + x_g, cell.geo.sw.y - y_g_b)
            case "se":
                align = "right"
                point = Point(cell.geo.se.x - x_g, cell.geo.se.y - y_g_b)
            case _:
                feedback(
                    f'Label location "{location}" is not valid;',
                    " use a compass directon.",
                    True,
                    True,
                )
        return align, point

    def draw_cell(
        self,
        row: int,
        col: int,
        value: str = None,
        location: str = None,
        color: str = None,
        arrow: str = None,
        border: bool = False,
        **kwargs,
    ):
        """Draw a single cell of the Market grid.

        Args:
            row (int): the row number in which the cell appears
            col (int): the column number in which the cell appears
            value (str) : the value to draw as text in the cell
            location (str) : the place within the cell to draw text
            color (str): the color number for a color set
            arrow (str): an arrow setting: u (up), d (down), a (arrow)
            border (bool): whether or not a border/outline must be drawn
        """
        from protograf.protos import Rectangle, Text, Line

        def track_geo(rect: Rectangle):
            """Store the cell's geometry as a named attribute of XX18Market."""
            cell_geo = rect.geo
            col_alpha = tools.as_excel(col + 1, False)
            cell_id = f"{col_alpha}{row + 1}"  # Excel-like reference
            setattr(self, cell_id, cell_geo)

        cell_x = col * self.width + self.x
        cell_y = row * self.height + self.y
        if color:
            cell_color = self.get_color(color)
        else:
            cell_color = self.fill
        # print(f"&&& CELL {row=} {col=} {value=} {color=} {arrow=} {border=}::")

        # ---- draw an empty cell
        if value in ["0", None, ".", ""]:
            rect = Rectangle(
                x=cell_x,
                y=cell_y,
                height=self.height,
                width=self.width,
                stroke="white",
                stroke_width=self.stroke_width,
                stroke_transparency=100,
                fill=None,
            )
            track_geo(rect)
            if not border:
                return

        # ---- style border/outline
        if border:
            border_color = (
                self.outline_stroke if kwargs.get("outline_stroke") else "red"
            )
            border_width = self.outline_width if kwargs.get("outline_width") else 3
            Rectangle(
                x=cell_x,
                y=cell_y,
                height=self.height,
                width=self.width,
                stroke=border_color,
                stroke_width=border_width,
                stroke_transparency=self.outline_transparency,
                fill=None,
            )
            if value is None:
                return

        # ---- draw an outline
        rect = Rectangle(
            x=cell_x,
            y=cell_y,
            height=self.height,
            width=self.width,
            stroke=self.stroke,
            stroke_width=self.stroke_width,
            stroke_transparency=self.stroke_transparency,
            fill=cell_color,
        )
        track_geo(rect)

        # ---- draw the value
        if value not in [None, "~"]:
            align, point = self.get_label_xy(rect)
            Text(
                str(value),
                x=point.x,
                y=point.y,
                align=align,
                stroke=self.font_stroke,
                font_size=self.font_size,
                font_name=self.font_name,
            )

        # ---- draw arrow(s)
        if arrow:
            _value = _lower(arrow)
            match _value:
                case "a":
                    if not self.arrow:
                        feedback(
                            "The arrow property is not set for the XX18Market.",
                            True,
                            True,
                        )
                        return
                    else:
                        off_x = getattr(self.arrow_down, "offset_x", 0.0)
                        off_y = getattr(self.arrow_down, "offset_y", 0.0)
                        cx = (rect.geo.c.x + self.margin_left + off_x) * globals.units
                        cy = (rect.geo.c.y + self.margin_top + off_y) * globals.units
                        self.arrow.draw(_abs_cx=cx, _abs_cy=cy, use_abs_c=True)
                case "d":
                    if not self.arrow_down:
                        xa = rect.geo.w.x + rect.geo.width / 10.0
                        if _lower(self.value_direction) in ["s", "se", "sw", "c", "ne"]:
                            ya = rect.geo.n.y + rect.geo.height / 10.0
                        else:
                            ya = rect.geo.w.y - rect.geo.height / 10.0
                        length = rect.geo.height / 2.0
                        Line(
                            x=xa,
                            y=ya,
                            length=length,
                            stroke_width=1.25,
                            angle=270,
                            arrow=True,
                            arrow_style="angle",
                        )
                    else:
                        off_x = getattr(self.arrow_down, "offset_x", 0.0)
                        off_y = getattr(self.arrow_down, "offset_y", 0.0)
                        kwargs["rotation"] = getattr(self.arrow_down, "rotation", None)
                        cx = (rect.geo.c.x + self.margin_left + off_x) * globals.units
                        cy = (rect.geo.c.y + self.margin_top + off_y) * globals.units
                        self.arrow_down.draw(_abs_cx=cx, _abs_cy=cy, use_abs_c=True)
                case "u":
                    if not self.arrow_up:
                        xa = rect.geo.e.x - rect.geo.width / 10.0
                        if _lower(self.value_direction) in ["se"]:
                            ya = rect.geo.e.y + rect.geo.height / 10.0
                        else:
                            ya = rect.geo.s.y - rect.geo.height / 10.0
                        length = rect.geo.height / 2.0
                        Line(
                            x=xa,
                            y=ya,
                            length=length,
                            stroke_width=1.25,
                            angle=90,
                            arrow=True,
                            arrow_style="angle",
                        )
                    else:
                        off_x = getattr(self.arrow_up, "offset_x", 0.0)
                        off_y = getattr(self.arrow_up, "offset_y", 0.0)
                        kwargs["rotation"] = getattr(self.arrow_up, "rotation", None)
                        cx = (rect.geo.c.x + self.margin_left + off_x) * globals.units
                        cy = (rect.geo.c.y + self.margin_top + off_y) * globals.units
                        self.arrow_up.draw(
                            _abs_cx=cx,
                            _abs_cy=cy,
                            use_abs_c=True,
                        )
                case None:
                    pass
                case _:
                    feedback(
                        f'The arrow property "{arrow}" is not valid for the XX18Market.',
                        True,
                        True,
                    )

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw the XX18MarketObject on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        border_cells = []
        # ---- validate and draw the market values
        for row, value in enumerate(self.values):
            row_values = tools.split(value, separator=" ", clean=True, no_blanks=True)
            # ---- draw the cells
            for col, row_val in enumerate(row_values):
                _items = tools.split(
                    row_val, separator=",", clean=True, no_blanks=False
                )
                items = _items + [None] * (4 - len(_items))
                _border = True if items[3] else False
                _color = items[1] if items[1] else None
                # print(f"&&& mrkt {row=} {col=} {_border=} {_color=} {items=}")
                if _border is True:
                    border_cells.append((col, row))
                self.draw_cell(
                    row=row,
                    col=col,
                    value=items[0],
                    color=_color,
                    arrow=items[2],
                    border=_border,
                    **kwargs,
                )
        # ---- redraw cells with border/outline
        for cell in border_cells:
            self.draw_cell(
                row=cell[1],
                col=cell[0],
                value=None,
                color=None,
                arrow=None,
                border=True,
                **kwargs,
            )
