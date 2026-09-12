# -*- coding: utf-8 -*-
"""
Create grids, repeats, sequences, and layouts for protograf
"""

# lib
import copy
from functools import lru_cache
import logging

# third party

# local
from protograf import globals
from protograf.utils.messaging import feedback
from protograf.utils.structures import (
    Point,
    HexOrientation,
    Locale,
)
from protograf.utils import tools, support
from protograf.utils.tools import _lower
from protograf.base import BaseShape, BaseCanvas
from protograf.shapes import HexShape, TextShape

# local
from .virtuals import HexHexLocations

log = logging.getLogger(__name__)
DEBUG = False


# ---- BaseShape-derived


class GridBase(BaseShape):
    """
    Base functionality for a drawing grid-like shapes on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super().__init__(_object=_object, canvas=canvas, **kwargs)
        self.use_side = False
        if "side" in kwargs:
            self.use_side = True
            if "width" in kwargs or "height" in kwargs:
                self.use_side = False
        self.y_cols, self.x_cols = [], []
        self.start_x, self.start_y = 0.0, 0.0  # top-left corner of grid
        # edge settings
        omit_a = tools.as_bool(kwargs.get("omit_all", False))
        omit_b = tools.as_bool(kwargs.get("omit_outer", False))
        omit_c = tools.as_bool(kwargs.get("omit_edges", False))
        self.omit_all = True if (omit_a or omit_b or omit_c) else False
        self.omit_top = tools.as_bool(kwargs.get("omit_top", False))
        self.omit_bottom = tools.as_bool(kwargs.get("omit_bottom", False))
        self.omit_left = tools.as_bool(kwargs.get("omit_left", False))
        self.omit_right = tools.as_bool(kwargs.get("omit_right", False))

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a grid on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else self.canvas
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- set x,y and calculate space available
        # print(f'\n~~~ GridBase {ID=} {off_x=} {self._u.x=}  {self._o.delta_x=} ')
        # print(f'~~~ GridBase {ID=} {off_y=} {self._u.y=}  {self._o.delta_y=} ')
        space_bottom = 0
        space_right = 0
        if ID is None:  # being used on a page - absolute offset
            self.start_x = self._u.x + self._o.delta_x
            self.start_y = self._u.y + self._o.delta_y
            max_width = self.page_width
            max_height = self.page_height
            if self.margin_fit:
                space_bottom = self._u.margin_bottom
                space_right = self._u.margin_right
            else:
                self.start_x = self._u.x
                self.start_y = self._u.y
            offset_x, offset_y = self.start_x, self.start_y
        else:  # being used on a card - x,y are relative offset - no margins
            # see proto/draw_element() function for these kwargs settings
            self.start_x = kwargs.get("card_x", 0) + self._u.x
            self.start_y = kwargs.get("card_y", 0) + self._u.y
            max_width = self.unit(kwargs.get("card_width", 0))
            max_height = self.unit(kwargs.get("card_height", 0))
            offset_x, offset_y = 0, 0
            # print(f'\n~~~ GridBase-card {ID=} {self.start_x=} {self.start_y=}')
            # print(f'\n~~~ GridBase-card {ID=} {max_width=} {max_height=}')

        self.height = self._u.height  # of each grid item
        self.width = self._u.width  # of each grid item
        if self.side and self.use_side:  # square grid
            side = self.unit(self.side)
            self.height, self.width = side, side
        # ---- number of blocks in grid
        bonus = 1 if isinstance(self, DotGridShape) else 0
        if self.rows == 0:
            self.rows = (
                int((max_height - space_bottom - offset_y) / self.height) + bonus
            )
        if self.cols == 0:
            self.cols = int((max_width - space_right - offset_x) / self.width) + bonus
        # print(f'~~~ GridBase {self.rows=} {self.cols=} {self.width=} {self.height=}')
        for y_col in range(0, self.rows + 1):
            self.y_cols.append(self.start_y + y_col * self.height)
        for x_col in range(0, self.cols + 1):
            self.x_cols.append(self.start_x + x_col * self.width)


class GridShape(GridBase):
    """
    Grid on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a grid on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else self.canvas
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- fill
        if kwargs.get("fill"):
            gwargs = copy.copy(kwargs)
            gwargs["stroke"] = None
            gwidth = self.width * (len(self.x_cols) - 1)
            gheight = self.height * (len(self.y_cols) - 1)
            cnv.draw_rect(
                (
                    self.start_x,
                    self.start_y,
                    self.start_x + gwidth,
                    self.start_y + gheight,
                )
            )
            self.set_canvas_props(  # shape.finish()
                cnv=cnv,
                index=ID,
                **gwargs,
            )
            cnv.commit()
        # ---- draw grid
        match kwargs.get("lines"):
            case "horizontal" | "horiz" | "h":
                horizontal, vertical = True, False
            case "vertical" | "vert" | "v":
                horizontal, vertical = False, True
            case _:
                horizontal, vertical = True, True
        if vertical:
            for col_no, x in enumerate(self.x_cols):
                skip = False
                if col_no == 0 and (self.omit_all or self.omit_left):
                    skip = True
                if col_no == len(self.x_cols) - 1 and (
                    self.omit_all or self.omit_right
                ):
                    skip = True
                if not skip:
                    cnv.draw_line(Point(x, self.y_cols[0]), Point(x, self.y_cols[-1]))
        if horizontal:
            for row_no, y in enumerate(self.y_cols):
                skip = False
                if row_no == 0 and (self.omit_all or self.omit_top):
                    skip = True
                if row_no == len(self.y_cols) - 1 and (
                    self.omit_all or self.omit_bottom
                ):
                    skip = True
                if not skip:
                    cnv.draw_line(Point(self.x_cols[0], y), Point(self.x_cols[-1], y))
        kwargs["stroke_ends"] = "squared"
        self.set_canvas_props(  # shape.finish()
            cnv=cnv,
            index=ID,
            **kwargs,
        )
        cnv.commit()  # if not, then Page objects e.g. Image not layered
        # ---- text
        x_d = self.start_x + (self.cols * self.width) / 2.0
        y_d = self.start_y + (self.rows * self.height) / 2.0
        self.draw_heading(cnv, ID, x_d, self.start_y, **kwargs)
        self.draw_label(cnv, ID, x_d, y_d, **kwargs)
        self.draw_title(
            cnv, ID, x_d, self.start_y + (self.rows * self.height), **kwargs
        )


class DotGridShape(GridBase):
    """
    Dot Grid on a given canvas.
    """

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a dot grid on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else self.canvas
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- set properties
        size = self.dot_width / 2.0  # diameter is 3 points ~ 1mm or 1/32"
        self.fill = self.stroke
        # ---- draw dot grid
        for y_col in range(0, self.rows):
            for x_col in range(0, self.cols):
                cnv.draw_circle(
                    (
                        self.start_x + x_col * self.width,
                        self.start_y + y_col * self.height,
                    ),
                    size,
                )
        self.set_canvas_props(cnv=cnv, index=ID, **kwargs)
        cnv.commit()  # if not, then Page objects e.g. Image not layered
        # ---- text
        x_d = self.start_x + (self.cols * self.width) / 2.0
        y_d = self.start_y + (self.rows * self.height) / 2.0
        self.draw_heading(cnv, ID, x_d, self.start_y, **kwargs)
        self.draw_label(cnv, ID, x_d, y_d, **kwargs)
        self.draw_title(
            cnv, ID, x_d, self.start_y + (self.rows * self.height), **kwargs
        )


class HexHexShape(BaseShape):
    """
    HexHex Grid on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super().__init__(_object=_object, canvas=canvas, **kwargs)
        self.show_sequence = kwargs.get("show_sequence", False)
        self.show_counter = kwargs.get("show_counter", False)
        # ---- create virtual grid
        self.hexhex_locations = HexHexLocations(
            cx=self.cx or self.x,  # no default value for cx
            cy=self.cy or self.y,  # no default value for cy
            radius=self.radius,
            diameter=self.diameter,
            height=self.height,
            side=self.side,
            rings=self.rings,
            orientation=self.orientation,
        )

    def calculate_xy(self) -> tuple:
        """Calculate centre of grid."""
        # ---- adjust start
        if self.row is not None and self.col is not None:
            x = self.col * self._u.width + self._o.delta_x
            y = self.row * self._u.height + self._o.delta_y
        elif self.cx is not None and self.cy is not None:
            x = self._u.cx - self._u.width / 2.0 + self._o.delta_x
            y = self._u.cy - self._u.height / 2.0 + self._o.delta_y
        else:
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
        # ---- overrides for grid layout
        if self._abs_cx is not None and self._abs_cy is not None:
            cx = self._abs_cx
            cy = self._abs_cy
            x = cx - self._u.width / 2.0
            y = cy - self._u.height / 2.0
        return x, y

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a hexhex layout on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else self.canvas
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- calculate centre of the shape (might be on cards)
        if "locale" in kwargs.keys():  # hexhex is being drawn on cards or row/col
            x, y = self.calculate_xy()
            self.cx = self._p2v(x - globals.margins.left_u, decimals=9)
            self.cy = self._p2v(y - globals.margins.top_u, decimals=9)
            # print(f'~~~ HexHexShape:draw {self.cx=} {self.cy=} {kwargs=}')
            self.hexhex_locations = HexHexLocations(
                cx=self.cx,
                cy=self.cy,
                radius=self.radius,
                diameter=self.diameter,
                height=self.height,
                side=self.side,
                rings=self.rings,
                orientation=self.orientation,
            )
        # ---- set local props
        locations = self.hexhex_locations.grid
        hex_count = self.hexhex_locations.hex_count
        hex_geometry = self.hexhex_locations.get_geometry()
        hex_orientation = self.hexhex_locations.get_orientation()
        # ---- set shape to draw
        if not self.shape and not self.is_kwarg("shape"):
            self.shape = HexShape(
                radius=self.radius,
                diameter=self.diameter,
                height=self.height,
                side=self.side,
                fill=self.fill,
                orientation=hex_orientation.name,
            )
        # ---- actual grid lines
        if self.gridlines:
            height = self.points_to_value(hex_geometry.height_flat)  # points=>units
            orientation = (
                "flat"
                if self.hexhex_locations.ORIENTATION == HexOrientation.POINTY
                else "pointy"
            )
            grid_hex = HexShape(
                cx=self.cx,
                cy=self.cy,
                radius=self.rings * height,
                hatches_count=2 * self.rings - 1,
                orientation=orientation,
                fill=self.gridlines_fill,
                stroke=self.gridlines_stroke,
                stroke_width=self.gridlines_stroke_width,
                stroke_ends=self.gridlines_ends,
                dotted=self.gridlines_dotted,
                dashed=self.gridlines_dashed,
                hatches_stroke=self.gridlines_stroke,
                hatches_stroke_width=self.gridlines_stroke_width,
                hatches_stroke_ends=self.gridlines_ends,
                hatches_dotted=self.gridlines_dotted,
                hatches_dashed=self.gridlines_dashed,
            )
            cxu = tools.unit(self.cx) + globals.margins.left_u
            cyu = tools.unit(self.cy) + globals.margins.top_u
            grid_hex.draw(_abs_cx=cxu, _abs_cy=cyu)
        # ---- set the range of required locations
        id_locations = range(0, hex_count + 1)
        # ---- process filters for conditional drawing of shape(s)
        spine_set, rings_set, counters_set = [], [], []
        if self.ranges:
            try:
                id_locations = []
                _ranges = tools.separate(self.ranges, separator=" ", clean=True)
                for rng in _ranges:
                    if rng != "":
                        if ":" in rng:
                            _ring, _hex = rng.split(":")
                            _ring_set = tools.sequence_split(
                                _ring, to_int=True, unique=True, star=True
                            )
                            _hex_set = tools.sequence_split(
                                _hex, to_int=True, unique=True, star=False
                            )
                            if "*" in _ring_set:
                                _ring_set += range(1, self.rings + 1)
                            for rval in _ring_set:
                                for hval in _hex_set:
                                    counters_set.append((rval, hval))
                        else:
                            values = rng[1:] if len(rng) > 1 else "*"
                            match _lower(rng[0]):
                                case "s":
                                    spine_set += tools.sequence_split(
                                        values, to_int=True, unique=True, star=True
                                    )
                                case "r":
                                    rings_set += tools.sequence_split(
                                        values, to_int=True, unique=True, star=True
                                    )
                if "*" in spine_set:
                    spine_set += [1, 2, 3, 4, 5, 6]
                if "*" in rings_set:
                    rings_set += range(1, self.rings + 1)
            except ValueError:
                feedback(
                    f'Unable to process HexHex ranges "{self.ranges}".'
                    " Please check and correct this property."
                )
        if self.locations:
            id_locations = tools.sequence_split(
                self.locations, to_int=True, unique=True
            )
        # ---- draw shapes on grid
        if self.shapes:
            # create shapes dist
            shapes_dict = {}
            if not isinstance(self.shapes, list):
                feedback("HexHex shapes must be a list of sets!", True)
            for key, item in enumerate(self.shapes):
                if not isinstance(item, tuple):
                    feedback("HexHex shapes must be a list of sets!", True)
                _key = tools.as_int(item[0], f"ring #{key}")
                if not isinstance(item[1], list):
                    feedback(
                        f"HexHex shapes ring #{key} must contain a list of shapes!",
                        True,
                    )
                _items = list(tools.flatten(item[1]))
                shapes_dict[_key] = _items
            # create dict for location retrieval
            location_dict = {}
            for location in locations:
                location_dict[(location.ring, location.counter)] = location
            # work through shapes; arranged in counter order for each ring
            for ring in range(0, self.rings + 1):
                shapes = shapes_dict.get(ring)
                if not shapes:
                    continue  # might not be shapes defined for a given ring
                # check no. of shapes vs size of ring
                if ring == 0 and len(shapes) != 1:
                    feedback("There must only be one HexHex shape for ring#0", True)
                if ring != 0 and len(shapes) != ring * 6:
                    feedback(
                        "There is a mismatch between the number of HexHex shapes"
                        f" and the ring locations ({ring * 6}) for ring#{ring}",
                        True,
                    )
                for key, the_shape in enumerate(shapes):
                    loc = location_dict.get((ring, key + 1))
                    cx = loc.centre.x + globals.margins.left_u
                    cy = loc.centre.y + globals.margins.top_u
                    hex_id = key
                    if self.show_counter:
                        hex_id = loc.counter
                    if self.show_sequence:
                        hex_id = loc.id
                    if the_shape:  # TODO - test for centre-able?
                        the_shape.draw(
                            _abs_cx=cx,
                            _abs_cy=cy,
                            ID=hex_id,
                            label_sequence=self.show_sequence or self.show_counter,
                        )
        elif self.shape:
            for key, location in enumerate(locations):
                draw = False
                if location.id in id_locations:
                    draw = True
                if location.spine in spine_set:
                    draw = True
                if location.ring in rings_set:
                    draw = True
                if (location.ring, location.counter) in counters_set:
                    draw = True
                if draw:
                    cx = location.centre.x + globals.margins.left_u
                    cy = location.centre.y + globals.margins.top_u
                    hex_id = key
                    if self.show_counter:
                        hex_id = location.counter
                    if self.show_sequence:
                        hex_id = location.id
                    self.shape.draw(
                        _abs_cx=cx,
                        _abs_cy=cy,
                        ID=hex_id,
                        label_sequence=self.show_sequence or self.show_counter,
                    )
                self.set_canvas_props(cnv=cnv, index=ID, **kwargs)
        else:
            if not self.gridlines:
                feedback("No grid lines, shape or shapes set for HexHex!", False, True)
        cnv.commit()  # if not, then Page objects e.g. Image not layered


class TableShape(BaseShape):
    """
    Table on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super().__init__(_object=_object, canvas=canvas, **kwargs)
        self.locales = []
        self.cells = {}  # store Locale data indexed by spreadsheet coordinates
        self.vertexes_header = [None, None, None, None]  # TL, BL, BR, TR
        self.vertexes_footer = [None, None, None, None]  # TL, BL, BR, TR
        self.use_side = False
        self.disable_row = self.kwargs.get("disable_row", False)
        self.disable_col = self.kwargs.get("disable_col", False)
        self.is_filled = False if kwargs.get("fill") == None else True
        if "side" in self.kwargs:
            self.use_side = True
            if "width" in self.kwargs or "height" in self.kwargs:
                self.use_side = False
        self.col_count, self.row_count = 0, 0
        # validate settings
        if isinstance(self.cols, int):
            self.col_count = self.cols
            self.col_widths = [
                self.width / self.col_count for col in range(0, self.col_count)
            ]
        elif isinstance(self.cols, list):
            if all(isinstance(item, (int, float)) for item in self.cols):
                self.col_count = len(self.cols)
                self.col_widths = self.cols
        else:
            pass
        if self.col_count < 2:
            feedback(
                "The cols value must be a number greater than one or list of numbers!",
                True,
            )
        if isinstance(self.rows, int):
            self.row_count = self.rows
            self.row_heights = [
                self.height / self.row_count for row in range(0, self.row_count)
            ]
        elif isinstance(self.rows, list):
            if all(isinstance(item, (int, float)) for item in self.rows):
                self.row_count = len(self.rows)
                self.row_heights = self.rows
        else:
            pass
        if self.row_count < 2:
            feedback(
                "The rows value must be a number greater than one or list of numbers!",
                True,
            )
        # combined?
        if self.col_count < 2 or self.row_count < 2:
            feedback("Minimum layout size is 2 columns x 2 rows!", True)

    @lru_cache(maxsize=999)
    def cell(
        self,
        cell_id: str | None = None,
        pad_x: float | None = None,
        pad_y: float | None = None,
    ) -> Locale:
        """Retrieve cell attributes as a Locale in user units."""
        data = self._cell(cell_id)
        # print('~~~ Table Cell', cell_id, data.x, data.y, data.xy, self.padding)
        padding_x = (
            tools.as_float(pad_x, "cell padding_x")
            if pad_x is not None
            else self.padding
        )
        padding_y = (
            tools.as_float(pad_y, "cell padding_y")
            if pad_y is not None
            else self.padding
        )
        _x = self._p2v(data.x, decimals=9) + padding_x - globals.margins.left
        _y = self._p2v(data.y, decimals=9) + padding_y - globals.margins.top
        user_cell = Locale(
            col=data.col,
            row=data.row,
            x=_x,
            y=_y,
            xy=Point(_x, _y),
            cxy=self.as_point(data.cxy, self.units, None, None),
            height=self._p2v(data.height, decimals=9) - 2 * padding_y,
            width=self._p2v(data.width, decimals=9) - 2 * padding_x,
            id=data.id,
            sequence=data.sequence,
        )
        return user_cell

    @lru_cache(maxsize=999)
    def _cell(self, cell_id: str | None = None) -> Locale:
        """Retrieve cell attributes as a Locale excluding Table padding."""
        try:
            _id = cell_id.upper()
            return self.cells[_id]
        except (AttributeError, KeyError):
            feedback(f'Cannot access cell "{cell_id}" for the Table!', True)

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a Table on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else self.canvas
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- convert to using units
        x = self._u.x + self._o.delta_x
        y = self._u.y + self._o.delta_y
        # ---- background rect
        if self.is_filled:
            twidths = [
                self.unit(self.col_widths[col_no])
                for col_no in range(0, self.col_count)
            ]
            theights = [
                self.unit(self.row_heights[row_no])
                for row_no in range(0, self.row_count)
            ]
            cnv.draw_rect((x, y, x + sum(twidths), y + sum(theights)))
            bargs = copy.copy(kwargs)
            bargs["stroke"] = None
            self.set_canvas_props(  # shape.finish()
                cnv=cnv,
                index=ID,
                **bargs,
            )
        # ---- iterate cols and rows
        cell_y = y
        sequence = 0
        self.vertexes = [None, None, None, None]  # TL, BL, BR, TR
        for row_no in range(0, self.row_count):
            cell_x = x
            rheight = self.unit(self.row_heights[row_no], label="row height")
            for col_no in range(0, self.col_count):
                cwidth = self.unit(self.col_widths[col_no], label="column width")
                # ---- * conditional line draw
                if self.disable_col:
                    cnv.draw_line(Point(cell_x, cell_y), Point(cell_x + cwidth, cell_y))
                    cnv.draw_line(
                        Point(cell_x, cell_y + rheight),
                        Point(cell_x + cwidth, cell_y + rheight),
                    )
                elif self.disable_row:
                    cnv.draw_line(
                        Point(cell_x, cell_y), Point(cell_x, cell_y + rheight)
                    )
                    cnv.draw_line(
                        Point(cell_x + cwidth, cell_y),
                        Point(cell_x + cwidth, cell_y + rheight),
                    )
                else:
                    cnv.draw_rect((cell_x, cell_y, cell_x + cwidth, cell_y + rheight))
                cx, cy = cell_x + cwidth / 2.0, cell_y + rheight / 2.0
                cell_id = tools.sheet_column(col_no + 1) + str(row_no + 1)
                locale = Locale(
                    col=col_no,
                    row=row_no,
                    x=cell_x,
                    y=cell_y,
                    xy=Point(cell_x, cell_y),
                    cxy=Point(cx, cy),
                    height=rheight,
                    width=cwidth,
                    id=cell_id,
                    label=cell_id,
                    sequence=sequence,
                )
                self.locales.append(locale)
                self.cells[cell_id] = locale
                # track vertices for outline of Table and Header/Footer rows
                if row_no == 0 and col_no == 0:
                    # top_left
                    self.vertexes[0] = [cell_x, cell_y]
                    self.vertexes_header[0] = [cell_x, cell_y]
                    self.vertexes_header[1] = [cell_x, cell_y + rheight]
                if row_no == self.row_count - 1 and col_no == 0:
                    # bottom_left
                    self.vertexes[1] = [cell_x, cell_y + rheight]
                    self.vertexes_footer[0] = [cell_x, cell_y]
                    self.vertexes_footer[1] = [cell_x, cell_y + rheight]
                if (
                    row_no == self.row_count - 1 and col_no == self.col_count - 1
                ):  # bottom_right
                    self.vertexes[2] = [cell_x + cwidth, cell_y + rheight]
                    self.vertexes_footer[3] = [cell_x + cwidth, cell_y]
                    self.vertexes_footer[2] = [cell_x + cwidth, cell_y + rheight]
                if row_no == 0 and col_no == self.col_count - 1:
                    # top_right
                    self.vertexes[3] = [cell_x + cwidth, cell_y]
                    self.vertexes_header[3] = [cell_x + cwidth, cell_y]
                    self.vertexes_header[2] = [cell_x + cwidth, cell_y + rheight]
                # finally ...
                cell_x = cell_x + cwidth
                sequence += 1
            cell_y = cell_y + rheight
        # ---- row/col line styles
        self.set_canvas_props(  # shape.finish()
            cnv=cnv,
            index=ID,
            **kwargs,
        )
        # ----  header row borders (override row)
        if self.borders_header:
            if isinstance(self.borders_header, tuple):
                self.borders_header = [
                    self.borders_header,
                ]
            if not isinstance(self.borders_header, list):
                feedback(
                    'The "borders_header" property must be a list of sets or a set'
                )
            for border in self.borders_header:
                kwargs["vertexes"] = self.vertexes_header
                self.draw_border(cnv, border, ID, **kwargs)
        # ----  footer row borders (override row)
        if self.borders_footer:
            if isinstance(self.borders_footer, tuple):
                self.borders_footer = [self.borders_footer]
            if not isinstance(self.borders_footer, list):
                feedback(
                    'The "borders_footer" property must be a list of sets or a set'
                )
            for border in self.borders_footer:
                kwargs["vertexes"] = self.vertexes_footer
                self.draw_border(cnv, border, ID, **kwargs)
        # ----  table borders (override)
        if self.borders:
            if isinstance(self.borders, tuple):
                self.borders = [self.borders]
            if not isinstance(self.borders, list):
                feedback('The "borders" property must be a list of sets or a set')
            for border in self.borders:
                self.draw_border(cnv, border, ID, **kwargs)

        cnv.commit()  # if not, then Page objects e.g. Image not layered
        return self.locales


class SequenceShape(BaseShape):
    """
    Set of Shapes drawn at points

    Notes:
        * `deck_data` is used, if provided by CardShape, to draw Shapes in the sequence.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        # feedback(f'+++ SequenceShape {_object=} {canvas=} {kwargs=}')
        super().__init__(_object=_object, canvas=canvas, **kwargs)
        self._objects = kwargs.get(
            "shapes", TextShape(_object=None, canvas=canvas, **kwargs)
        )
        self.setting = kwargs.get("setting", (1, 1, 1, "number"))
        if isinstance(self.setting, list):
            self.setting_list = self.setting
        else:
            self.calculate_setting_list()
        self.interval_x = self.interval_x or self.interval
        self.interval_y = self.interval_y or self.interval
        # convert/use interval lists
        if isinstance(self.interval_x, list):
            if len(self.interval_x) != len(self.setting_list):
                feedback(
                    'The number of items in "interval_x" must match those in'
                    ' the "setting".',
                    True,
                )
        else:
            int_x = tools.as_float(self.interval_x, "interval_x")
            self.interval_x = [int_x] * len(self.setting_list)
        if isinstance(self.interval_y, list):
            if len(self.interval_y) != len(self.setting_list):
                feedback(
                    'The number of items in "interval_y" must match those in'
                    ' the "setting".',
                    True,
                )
        else:
            int_y = tools.as_float(self.interval_y, "interval_y")
            self.interval_y = [int_y] * len(self.setting_list)
        # validate intervals
        for item in self.interval_y:
            if not isinstance(item, (float, int)):
                feedback('Values for "interval_y" must be numeric!', True)
        for item in self.interval_x:
            if not isinstance(item, (float, int)):
                feedback('Values for "interval_x" must be numeric!', True)

    def calculate_setting_list(self):
        """Create settings for sequence."""
        if not isinstance(self.setting, tuple):
            feedback(f"Sequence setting '{self.setting}' must be a set!", True)
        if len(self.setting) < 2:
            feedback(
                f"Sequence setting '{self.setting}' must include start and end values!",
                True,
            )
        self.set_start = self.setting[0]
        self.set_stop = self.setting[1]
        self.set_inc = self.setting[2] if len(self.setting) > 2 else 1
        if len(self.setting) > 3:
            self.set_type = self.setting[3]
        else:
            self.set_type = (
                "number"
                if isinstance(self.set_start, (int, float, complex))
                else "letter"
            )
        # ---- store sequence values in setting_list
        self.setting_list = []
        try:
            if _lower(self.set_type) in ["n", "number"]:
                self.set_stop = (
                    self.setting[1] + 1 if self.set_inc > 0 else self.setting[1] - 1
                )
                self.setting_iterator = range(
                    self.set_start, self.set_stop, self.set_inc
                )
                self.setting_list = list(self.setting_iterator)
            elif _lower(self.set_type) in ["l", "letter"]:
                self.setting_list = []
                start, stop = ord(self.set_start), ord(self.set_stop)
                curr = start
                while True:
                    if self.set_inc > 0 and curr > stop:
                        break
                    if self.set_inc < 0 and curr < stop:
                        break
                    self.setting_list.append(chr(curr))
                    curr += self.set_inc
            elif _lower(self.set_type) in ["r", "roman"]:
                self.set_stop = (
                    self.setting[1] + 1 if self.set_inc > 0 else self.setting[1] - 1
                )
                self.setting_iterator = range(
                    self.set_start, self.set_stop, self.set_inc
                )
                _setting_list = list(self.setting_iterator)
                self.setting_list = [
                    support.roman(int(value)) for value in _setting_list
                ]
            elif _lower(self.set_type) in ["e", "excel"]:
                self.set_stop = (
                    self.setting[1] + 1 if self.set_inc > 0 else self.setting[1] - 1
                )
                self.setting_iterator = range(
                    self.set_start, self.set_stop, self.set_inc
                )
                _setting_list = list(self.setting_iterator)
                self.setting_list = [
                    support.excel_column(int(value)) for value in _setting_list
                ]
            else:
                feedback(
                    f"The settings type '{self.set_type}' must rather be one of:"
                    " number, roman, excel or letter!",
                    True,
                )
        except Exception as err:
            log.warning(err)
            feedback(
                f"Unable to evaluate Sequence setting '{self.setting}';"
                " - please check and try again!",
                True,
            )

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else self.canvas
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # _off_x, _off_y = off_x, off_y

        for key, item in enumerate(self.setting_list):
            _ID = ID if ID is not None else self.shape_id
            _locale = Locale(sequence=item)
            kwargs["locale"] = _locale._asdict()
            # feedback(f'+++ @Seqnc@ {kwargs["locale"]}')
            flat_elements = tools.flatten(self._objects)
            log.debug("flat_eles:%s", flat_elements)
            for each_flat_ele in flat_elements:
                flat_ele = copy.copy(each_flat_ele)  # allow props to be reset
                try:  # normal element
                    if self.deck_data:
                        new_ele = self.handle_custom_values(flat_ele, _ID)
                    else:
                        new_ele = flat_ele
                    new_ele.draw(off_x=off_x, off_y=off_y, ID=_ID, **kwargs)
                except AttributeError:
                    new_ele = flat_ele(cid=_ID) if flat_ele else None
                    if new_ele:
                        flat_new_eles = tools.flatten(new_ele)
                        log.debug("%s", flat_new_eles)
                        for flat_new_ele in flat_new_eles:
                            log.debug("%s", flat_new_ele)
                            if self.deck_data:
                                new_flat_new_ele = self.handle_custom_values(
                                    flat_new_ele, _ID
                                )
                            else:
                                new_flat_new_ele = flat_new_ele
                            new_flat_new_ele.draw(
                                off_x=off_x, off_y=off_y, ID=_ID, **kwargs
                            )

            off_x = off_x + self.interval_x[key]
            off_y = off_y + self.interval_y[key]


class RepeatShape(BaseShape):
    """
    Shape is drawn multiple times.

    Notes:
        *  `deck_data` is used, if provided by CardShape, to draw Shape(s) repeatedly.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super().__init__(_object=_object, canvas=canvas, **kwargs)
        self._objects = kwargs.get("shapes", [])  # incoming Shape object(s)
        # feedback(f'*** REPEAT {self._objects=} {kwargs=}')
        # UPDATE SELF WITH COMMON
        if self.common:
            attrs = vars(self.common)
            for attr in list(attrs.keys()):
                if attr not in ["canvas", "common", "stylesheet"] and attr[0] != "_":
                    common_attr = getattr(self.common, attr)
                    base_attr = getattr(BaseCanvas(), attr)
                    if common_attr != base_attr:
                        setattr(self, attr, common_attr)

        # ---- repeat
        self.rows = kwargs.get("rows", 1)
        self.cols = kwargs.get("cols", kwargs.get("columns", 1))
        self.repeat = kwargs.get("repeat", None)
        self.offset_x = self.offset_x or self.offset
        self.offset_y = self.offset_y or self.offset
        self.interval_x = self.interval_x or self.interval
        self.interval_y = self.interval_y or self.interval
        if self.repeat:
            (
                self.repeat_across,
                self.repeat_down,
                self.interval_y,
                self.interval_x,
                self.offset_x,
                self.offset_y,
            ) = self.repeat.split(",")
        else:
            self.across = kwargs.get("across", self.cols)
            self.down = kwargs.get("down", self.rows)
            try:
                self.down = list(range(1, self.down + 1))
            except TypeError:
                pass
            try:
                self.across = list(range(1, self.across + 1))
            except TypeError:
                pass

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        _ID = ID if ID is not None else self.shape_id
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else self.canvas
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        _off_x, _off_y = off_x or self.offset_x or 0, off_y or self.offset_y or 0
        # feedback(f'*** REPEAT {self._objects=} {ID=} {self.cols=} {self.rows=}')

        for col in range(self.cols):
            for row in range(self.rows):
                if ((col + 1) in self.across) and ((row + 1) in self.down):
                    off_x = _off_x + col * self.interval_x  # WAS self.offset_x
                    off_y = _off_y + row * self.interval_y  # WAS self.offset_y
                    flat_elements = tools.flatten(self._objects)
                    log.debug("flat_eles:%s", flat_elements)
                    for flat_ele in flat_elements:
                        log.debug("flat_ele:%s", flat_ele)
                        try:  # normal element
                            if self.deck_data:
                                new_ele = self.handle_custom_values(flat_ele, _ID)
                            else:
                                new_ele = flat_ele
                            new_ele.draw(off_x=off_x, off_y=off_y, ID=_ID, **kwargs)
                        except AttributeError:
                            if not flat_ele:
                                feedback("No shape to repeat!", True)
                            new_ele = flat_ele(cid=self.shape_id)
                            log.debug("%s %s", new_ele, type(new_ele))
                            if new_ele:
                                flat_new_eles = tools.flatten(new_ele)
                                log.debug("%s", flat_new_eles)
                                for flat_new_ele in flat_new_eles:
                                    log.debug("%s", flat_new_ele)
                                    if self.deck_data:
                                        new_flat_new_ele = self.handle_custom_values(
                                            flat_new_ele, _ID
                                        )
                                    else:
                                        new_flat_new_ele = flat_new_ele
                                    new_flat_new_ele.draw(
                                        off_x=off_x, off_y=off_y, ID=self.shape_id
                                    )


# ---- virtual Locations

# see virtuals.py


# ---- tracks

# See proto.py
