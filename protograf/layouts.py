# -*- coding: utf-8 -*-
"""
Create grids, repeats, sequences, layouts, and connections for protograf
"""
# lib
import copy
import logging
import math

# third party
# local
from protograf import globals
from protograf.utils.messaging import feedback
from protograf.utils.structures import (
    Point,
    HexGeometry,
    HexOrientation,
    VirtualHex,
    Locale,
)
from protograf.utils import geoms, tools, support
from protograf.utils.tools import _lower
from protograf.base import BaseShape, BaseCanvas
from protograf.shapes import (
    # CircleShape,
    LineShape,
    # PolygonShape,
    PolylineShape,
    # RectangleShape,
    TextShape,
)
from protograf.shapes_hexagon import HexShape

log = logging.getLogger(__name__)
DEBUG = False


# ---- BaseShape-derived


class GridShape(BaseShape):
    """
    Grid on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super().__init__(_object=_object, canvas=canvas, **kwargs)
        self.use_side = False
        if "side" in kwargs:
            self.use_side = True
            if "width" in kwargs or "height" in kwargs:
                self.use_side = False

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a grid on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else self.canvas
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- convert to using units
        x = self._u.x + self._o.delta_x
        y = self._u.y + self._o.delta_y
        height = self._u.height  # of each grid item
        width = self._u.width  # of each grid item
        if self.side and self.use_side:  # square grid
            side = self.unit(self.side)
            height, width = side, side
        # ---- number of blocks in grid:
        if self.rows == 0:
            self.rows = int(
                (self.page_height - self.margin_bottom - self.margin_top)
                / self.points_to_value(height)
            )
        if self.cols == 0:
            self.cols = int(
                (self.page_width - self.margin_left - self.margin_right)
                / self.points_to_value(width)
            )
        y_cols, x_cols = [], []
        for y_col in range(0, self.rows + 1):
            y_cols.append(y + y_col * height)
        for x_col in range(0, self.cols + 1):
            x_cols.append(x + x_col * width)
        # ---- draw grid
        match kwargs.get("lines"):
            case "horizontal" | "horiz" | "h":
                horizontal, vertical = True, False
            case "vertical" | "vert" | "v":
                horizontal, vertical = False, True
            case _:
                horizontal, vertical = True, True
        if vertical:
            for x in x_cols:
                cnv.draw_line(Point(x, y_cols[0]), Point(x, y_cols[-1]))
        if horizontal:
            for y in y_cols:
                cnv.draw_line(Point(x_cols[0], y), Point(x_cols[-1], y))
        self.set_canvas_props(  # shape.finish()
            cnv=cnv,
            index=ID,
            **kwargs,
        )
        cnv.commit()  # if not, then Page objects e.g. Image not layered
        # ---- text
        x = self._u.x + self._o.delta_x
        y = self._u.y + self._o.delta_y
        x_d = x + (self.cols * width) / 2.0
        y_d = y + (self.rows * height) / 2.0
        self.draw_heading(cnv, ID, x_d, y, **kwargs)
        self.draw_label(cnv, ID, x_d, y_d, **kwargs)
        self.draw_title(cnv, ID, x_d, y + (self.rows * height), **kwargs)


class DotGridShape(BaseShape):
    """
    Dot Grid on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super().__init__(_object=_object, canvas=canvas, **kwargs)

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a dot grid on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else self.canvas
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- switch to use of units
        x = 0 + self._u.offset_x
        y = 0 + self._u.offset_y
        height = self._u.height  # of each grid item
        width = self._u.width  # of each grid item
        if "side" in self.kwargs and not (
            "height" in self.kwargs or "width" in self.kwargs
        ):
            # square grid
            side = self.unit(self.side)
            height, width = side, side
        if "side" in self.kwargs and (
            "height" in self.kwargs or "width" in self.kwargs
        ):
            feedback(
                "Set either height & width OR side, but not both, for a DotGrid",
                False,
                True,
            )
        # ---- number of blocks in grid
        if self.rows == 0:
            self.rows = int((self.page_height) / height) + 1
        if self.cols == 0:
            self.cols = int((self.page_width) / width) + 1
        # ---- set canvas
        size = self.dot_width / 2.0  # diameter is 3 points ~ 1mm or 1/32"
        self.fill = self.stroke
        # ---- draw dot grid
        for y_col in range(0, self.rows):
            for x_col in range(0, self.cols):
                cnv.draw_circle((x + x_col * width, y + y_col * height), size)
        self.set_canvas_props(cnv=cnv, index=ID, **kwargs)
        cnv.commit()  # if not, then Page objects e.g. Image not layered


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

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a hexhex layout on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else self.canvas
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
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
            # radius = tools.points(hex_geometry.radius)
            height = tools.points(hex_geometry.height_flat)
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
                                _ring, as_int=True, unique=True, star=True
                            )
                            _hex_set = tools.sequence_split(
                                _hex, as_int=True, unique=True, star=False
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
                                        values, as_int=True, unique=True, star=True
                                    )
                                case "r":
                                    rings_set += tools.sequence_split(
                                        values, as_int=True, unique=True, star=True
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
                self.locations, as_int=True, unique=True
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
        self.use_side = False
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

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a table on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else self.canvas
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- convert to using units
        x = self._u.x + self._o.delta_x
        y = self._u.y + self._o.delta_y
        # ---- iterate cols and rows
        cell_y = y
        sequence = 0
        for row_no in range(0, self.row_count):
            cell_x = x
            rheight = self.unit(self.row_heights[row_no], label="row height")
            for col_no in range(0, self.col_count):
                cwidth = self.unit(self.col_widths[col_no], label="column width")
                cnv.draw_rect((cell_x, cell_y, cell_x + cwidth, cell_y + rheight))
                cx, cy = cell_x + cwidth / 2.0, cell_y + rheight / 2.0
                ID = tools.sheet_column(col_no + 1) + str(row_no + 1)
                locale = Locale(
                    col=col_no, row=row_no, x=cx, y=cy, id=ID, sequence=sequence
                )
                self.locales.append(locale)
                # finally ...
                cell_x = cell_x + cwidth
                sequence += 1
            cell_y = cell_y + rheight
        self.set_canvas_props(  # shape.finish()
            cnv=cnv,
            index=ID,
            **kwargs,
        )
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


# ---- Virtual Class


class VirtualShape:
    """
    Common properties and methods for all virtual shapes (layout and track)
    """

    def to_int(self, value, label="", maximum=None, minimum=None) -> int:
        """Set a value to an int; or stop if an invalid value."""
        try:
            int_value = int(value)
            if minimum and int_value < minimum:
                feedback(
                    f"{label} integer is less than the minimum of {minimum}!", True
                )
            if maximum and int_value > maximum:
                feedback(
                    f"{label} integer is more than the maximum of {maximum}!", True
                )
            return int_value
        except Exception:
            feedback(f"{value} is not a valid {label} integer!", True)

    def to_float(self, value, label="") -> int:
        """Set a value to a float; or stop if an invalid value."""
        try:
            float_value = float(value)
            return float_value
        except Exception:
            _label = f" for {label}" if label else ""
            feedback(f'"{value}"{_label} is not a valid floating number!', True)


# ---- virtual HexHex grid


class HexHexLocations(VirtualShape):
    """
    HexHex Locations are not drawn on the canvas; they provide the
    locations/points where user-defined shapes will be drawn.
    """

    def __init__(self, **kwargs):
        base = globals.base  # protograf BaseCanvas
        self.kwargs = kwargs
        # inject and then override kwargs supplied by DefaultShape
        if kwargs.get("default"):
            try:
                if kwargs.get("default"):
                    self.kwargs = kwargs["default"]._default_kwargs | kwargs
            except Exception:
                self.kwargs = kwargs
        else:
            self.kwargs = kwargs
        self.kwargs.pop("default", None)
        # inject and overwrite kwargs with those set by CommonShape
        try:
            if kwargs.get("common"):
                self.kwargs = kwargs | kwargs["common"]._common_kwargs
        except AttributeError:
            pass  # ignore, for example, CommonShape
        self.cx = tools.as_float(kwargs.get("cx", 1.0), "x")  # hexhex centre
        self.cy = tools.as_float(kwargs.get("cy", 1.0), "y")  # hexhex centre
        self.rings = tools.as_int(kwargs.get("rings", 1), "rings")
        self.radius = kwargs.get("radius", None)
        self.diameter = kwargs.get("diameter", None)
        self.height = kwargs.get("height", 1.0)
        self.side = kwargs.get("side", None)
        self.orientation = kwargs.get("orientation", "flat")
        self.common = kwargs.get("common", None)
        self.hexes = []
        # ---- UPDATE SELF WITH COMMON
        if self.common:
            try:
                attrs = vars(self.common)
            except TypeError:
                feedback(
                    f'Cannot process the Common property "{self.common}"'
                    " - please check!",
                    True,
                )
            for attr in attrs.keys():
                if (
                    attr not in ["canvas", "common", "stylesheet", "kwargs"]
                    and attr[0] != "_"
                ):
                    common_attr = getattr(self.common, attr)
                    base_attr = getattr(base, attr)
                    if common_attr != base_attr:
                        setattr(self, attr, common_attr)
        # ---- check construction type
        self.use_diameter = self.is_kwarg("diameter")
        self.use_height = self.is_kwarg("height")
        self.use_radius = self.is_kwarg("radius")
        self.use_side = False
        if "side" in self.kwargs:
            self.use_side = True
            if (
                "radius" in self.kwargs
                or "height" in self.kwargs
                or "diameter" in self.kwargs
            ):
                self.use_side = False
        # ---- fallback / default
        if not self.use_diameter and not self.use_radius and not self.use_side:
            hex_base = None
            self.use_height = True
            if not self.height:
                if self.radius:
                    hex_base = tools.as_float(self.radius, "hexagon radius")
                elif self.diameter:
                    hex_base = tools.as_float(self.diameter, "hexagon diameter") / 2.0
                elif self.side:
                    hex_base = tools.as_float(self.side, "hexagon side")
                else:
                    feedback(
                        "No dimensions (greater than zero) set to draw the Hexagon",
                        True,
                    )
                self.height = hex_base * math.sqrt(3)
        self.ORIENTATION = self.get_orientation()
        # ---- get grid
        self.hex_count = 0  # useful to check grid size
        self.grid = self.construct_grid()

    def is_kwarg(self, value) -> bool:
        """Validate if value is in direct kwargs OR in Common _kwargs."""
        if value in self.kwargs:
            return True
        return False

    def get_orientation(self) -> HexOrientation:
        """Return HexOrientation for the Hexagon."""
        orientation = None
        if _lower(self.orientation) in ["p", "pointy"]:
            orientation = HexOrientation.POINTY
        elif _lower(self.orientation) in ["f", "flat"]:
            orientation = HexOrientation.FLAT
        else:
            feedback(
                'Invalid orientation "{self.orientation}" supplied for hexagon.', True
            )
        return orientation

    def get_geometry(self):
        """Calculate geometric settings of a single hexagon."""
        half_flat = 0
        # ---- calculate half_flat & half_side
        if self.height and self.use_height:
            side = self.height / math.sqrt(3)
            half_flat = self.height / 2.0
        elif self.diameter and self.use_diameter:
            side = self.diameter / 2.0
            half_flat = side * math.sqrt(3) / 2.0
        elif self.radius and self.use_radius:
            side = self.radius
            half_flat = side * math.sqrt(3) / 2.0
        else:
            pass
        if self.side and self.use_side:
            side = self.side
            half_flat = side * math.sqrt(3) / 2.0
        if not self.radius and not self.height and not self.diameter and not self.side:
            feedback(
                "No value for side or height or diameter or radius"
                " supplied to construct hexagon for HexHexLocations.",
                True,
            )
        half_side = side / 2.0
        height_flat = 2 * half_flat
        diameter = 2.0 * side
        radius = side
        z_fraction = (diameter - side) / 2.0
        self.ORIENTATION = self.get_orientation()
        hex_geometry = HexGeometry(  # in point units
            tools.unit(radius),
            tools.unit(diameter),
            tools.unit(side),
            tools.unit(half_side),
            tools.unit(half_flat),
            tools.unit(height_flat),
            z_fraction,
        )
        return hex_geometry

    def construct_grid(self):
        """Create a virtual hexhex grid, with identified locations."""
        ghex = self.get_geometry()
        cxu, cyu = tools.unit(self.cx), tools.unit(self.cy)
        n = self.rings + 1
        self.hex_count = 3 * n * (n - 1) + 1
        self.hexes = []
        # ---- angles
        vertex_angles = []
        if self.ORIENTATION == HexOrientation.FLAT:
            vertex_angles = [0.0, 30.0, 90.0, 150.0, -150.0, -90.0, -30.0]
        elif self.ORIENTATION == HexOrientation.POINTY:
            vertex_angles = [
                0.0,
                60.0,
                120.0,
                180.0,
                -120.0,
                -60.0,
                0.0,
                60.0,
            ]  # TODO - set
        else:
            feedback(
                'Invalid orientation "{self.ORIENTATION}" supplied for hexagon.', True
            )
        # ---- centre hex
        hex0 = VirtualHex(
            centre=Point(cxu, cyu),
            id=0,
            ring=0,
            counter=1,
            spine=0,
            zone=0,
            orientation=self.ORIENTATION,
        )
        self.hexes.append(hex0)
        # ---- iterate over all ring hexes
        chex = Point(cxu, cyu)
        hex_zero = Point(cxu, cyu)
        ring = 1
        ring_counter = 1  # space number "around" a given ring
        spine_interval = 1  # distance between "spine" hexes in a given ring
        spine_location = 1
        is_spine = True
        spine = 1
        for location in range(1, self.hex_count):
            if self.ORIENTATION == HexOrientation.POINTY:
                if is_spine and spine == 1:  # first spine hex
                    chex = geoms.point_from_angle(
                        hex_zero, ghex.height_flat * ring, 300.0
                    )
                elif is_spine and ring > 1:
                    chex = geoms.point_from_angle(
                        chex, ghex.height_flat, vertex_angles[spine - 2]
                    )
                else:
                    sid = spine - 1
                    chex = geoms.point_from_angle(
                        chex, ghex.height_flat, vertex_angles[spine - 1]
                    )
            elif self.ORIENTATION == HexOrientation.FLAT:
                if is_spine and spine == 1:  # first spine hex
                    chex = Point(cxu, cyu - ghex.height_flat * ring)
                elif is_spine and ring > 1:
                    chex = geoms.point_from_angle(
                        chex, ghex.height_flat, vertex_angles[spine - 2]
                    )
                else:
                    chex = geoms.point_from_angle(
                        chex, ghex.height_flat, vertex_angles[spine - 1]
                    )
            _hex = VirtualHex(
                centre=chex,
                id=location,
                ring=ring,
                counter=ring_counter,
                spine=spine if is_spine else 0,
                zone=0,
                orientation=self.ORIENTATION,
            )
            self.hexes.append(_hex)
            # next hex
            ring_counter += 1
            if (location + 1) - spine_location == spine_interval:
                # set values related to NEXT (upcoming hex)
                is_spine = True
                spine += 1
                spine_location = location + 1
            else:
                is_spine = False
            # increment ring? reset spine value & ring_counter
            if ring_counter - 1 == 6 * ring:
                ring += 1
                ring_counter = 1
                spine_interval += 1
                is_spine = True
                spine = 1
                if ring == 2:
                    del vertex_angles[0]
        # ---- done
        return self.hexes


# ---- virtual Locations


class VirtualLocations(VirtualShape):
    """
    Common properties and methods to define virtual Locations.

    Virtual Locations are not drawn on the canvas; they provide the
    locations/points where user-defined shapes will be drawn.
    """

    def __init__(self, rows, cols, **kwargs):
        self.x = self.to_float(kwargs.get("x", 1.0), "x")  # left(upper) corner
        self.y = self.to_float(kwargs.get("y", 1.0), "y")  # top(uppper) corner
        self.rows = self.to_int(rows, "rows")
        self.cols = self.to_int(cols, "cols")
        self.side = self.to_float(kwargs.get("side", 0), "side")
        self.layout_size = self.rows * self.cols
        self.interval = kwargs.get("interval", 1)
        self.interval_y = kwargs.get("interval_y", self.interval)
        self.interval_x = kwargs.get("interval_x", self.interval)
        # offset
        self.col_even = kwargs.get("col_even", 0)
        self.col_odd = kwargs.get("col_odd", 0)
        self.row_even = kwargs.get("row_even", 0)
        self.row_odd = kwargs.get("row_odd", 0)
        # layout
        self.pattern = kwargs.get("pattern", "default")
        self.direction = kwargs.get("direction", "east")
        self.facing = kwargs.get("facing", "east")  # for diamond, triangle
        self.flow = None  # used for snake; see validate() for setting
        # start / end
        self.start = kwargs.get("start", None)
        self.stop = kwargs.get("stop", 0)
        self.label_style = kwargs.get("label_style", None)
        self.validate()

    def validate(self):
        """Check for valid settings and combos."""
        self.stop = self.to_int(self.stop, "stop")
        self.rows = self.to_int(self.rows, "rows")
        self.cols = self.to_int(self.cols, "cols")
        self.start = str(self.start)
        self.pattern = str(self.pattern)
        self.direction = str(self.direction)
        if _lower(self.pattern) not in ["default", "d", "snake", "s", "outer", "o"]:
            feedback(
                f"{self.pattern} is not a valid pattern - "
                "use 'default', 'outer', 'snake'",
                True,
            )
        if _lower(self.direction) not in [
            "north",
            "n",
            "south",
            "s",
            "west",
            "w",
            "east",
            "e",
        ]:
            feedback(
                f"{self.direction} is not a valid direction - "
                "use 'north', south', 'west', or 'east'",
                True,
            )
        if _lower(self.facing) not in [
            "north",
            "n",
            "south",
            "s",
            "west",
            "w",
            "east",
            "e",
        ]:
            feedback(
                f"{self.facing} is not a valid facing - "
                "use 'north', south', 'west', or 'east'",
                True,
            )
        if (
            "n" in _lower(self.start)[0]
            and "n" in _lower(self.direction)[0]
            or "s" in _lower(self.start)[0]
            and "s" in _lower(self.direction)[0]
            or "w" in _lower(self.start)[0]
            and "w" in _lower(self.direction)[0]
            or "e" in _lower(self.start)[0]
            and "e" in _lower(self.direction)[0]
        ):
            feedback(f"Cannot use {self.start} with {self.direction}!", True)
        if _lower(self.direction) in ["north", "n", "south", "s"]:
            self.flow = "vert"
        elif _lower(self.direction) in ["west", "w", "east", "e"]:
            self.flow = "hori"
        else:
            feedback(f"{self.direction} is not a valid direction!", True)
        if self.label_style and _lower(self.label_style) != "excel":
            feedback(f"{self.label_style } is not a valid label_style !", True)
        if self.col_odd and self.col_even:
            feedback("Cannot use 'col_odd' and 'col_even' together!", True)
        if self.row_odd and self.row_even:
            feedback("Cannot use 'row_odd' and 'row_even' together!", True)

    def set_id(self, col: int, row: int) -> str:
        """Create an ID from row and col values."""
        if self.label_style and _lower(self.label_style) == "excel":
            _col = tools.sheet_column(col)
            return f"{_col}{row}"
        else:
            return f"{col},{row}"

    def set_compass(self, compass: str) -> str:
        """Return full lower-case value of primary compass direction."""
        if not compass:
            return None
        _compass = _lower(compass)
        match _compass:
            case "n" | "north":
                return "north"
            case "s" | "south":
                return "south"
            case "e" | "east":
                return "east"
            case "w" | "west":
                return "west"
            case _:
                raise ValueError(
                    f'"{compass}" is an invalid primary compass direction!'
                )

    def next_locale(self) -> Locale:
        """Yield next Locale for each call."""


class RectangularLocations(VirtualLocations):
    """
    Common properties and methods to define a virtual rectangular layout.
    """

    def __init__(self, rows=2, cols=2, **kwargs):
        super().__init__(rows, cols, **kwargs)
        self.kwargs = kwargs
        _interval = kwargs.get("interval", 1)
        self.interval = tools.as_float(_interval, "interval")
        if kwargs.get("interval_x"):
            self.interval_x = tools.as_float(kwargs.get("interval_x"), "interval_x")
        else:
            self.interval_x = self.interval
        if kwargs.get("interval_y"):
            self.interval_y = tools.as_float(kwargs.get("interval_y"), "interval_y")
        else:
            self.interval_y = self.interval
        self.start = kwargs.get("start", "sw")
        if self.cols < 2 or self.rows < 2:
            feedback(
                f"Minimum layout size is 2x2 (cannot use {self.cols }x{self.rows})!",
                True,
            )
        if _lower(self.start) not in ["sw", "se", "nw", "ne"]:
            feedback(
                f"{self.start} is not a valid start - "
                "use: 'sw', 'se', 'nw', or 'ne'",
                True,
            )
        if self.side and kwargs.get("interval_x"):
            feedback("Using side will override interval_x and offset values!", False)
        if self.side and kwargs.get("interval_y"):
            feedback("Using side will override interval_y and offset values!", False)

    def next_locale(self) -> Locale:
        """Yield next Location for each call."""
        _start = _lower(self.start)
        _dir = _lower(self.direction)
        current_dir = _dir
        match _start:
            case "sw":
                row_start = self.rows
                col_start = 1
                clockwise = _dir in ["north", "n"]
            case "se":
                row_start = self.rows
                col_start = self.cols
                clockwise = _dir in ["west", "w"]
            case "nw":
                row_start = 1
                col_start = 1
                clockwise = _dir in ["east", "e"]
            case "ne":
                row_start = 1
                col_start = self.cols
                clockwise = _dir in ["south", "s"]
            case _:
                raise ValueError(
                    f'"{self.direction}" is an invalid secondary compass direction!'
                )
        col, row, count = col_start, row_start, 0
        max_outer = 2 * self.rows + (self.cols - 2) * 2
        corner = None
        # ---- triangular layout
        if self.side:
            self.interval_x = self.side
            self.interval_y = math.sqrt(3) / 2.0 * self.side
            _dir = -1 if self.row_odd < 0 else 1
            self.row_odd = _dir * (self.interval_x / 2.0)
            if self.row_even:
                _dir = -1 if self.row_even < 0 else 1
                self.row_odd = 0
                self.row_even = _dir * (self.interval_x / 2.0)
        while True:  # rows <= self.rows and col <= self.cols:
            count += 1
            # calculate point based on row/col
            # TODO!  set actual x and y
            x = self.x + (col - 1) * self.interval_x
            y = self.y + (row - 1) * self.interval_y
            # offset(s)
            if self.side:
                if row & 1:
                    x = x + self.row_odd
                if not row & 1:
                    x = x + self.row_even
            else:
                if self.col_odd and col & 1:
                    y = y + self.col_odd
                if self.col_even and not col & 1:
                    y = y + self.col_even
                if self.row_odd and row & 1:
                    x = x + self.row_odd
                if self.row_even and not row & 1:
                    x = x + self.row_even
            # ---- set next grid location
            match _lower(self.pattern):
                # ---- * snake
                case "snake" | "snaking" | "s":
                    # feedback(f'+++ {count=} {self.layout_size=} {self.stop=}')
                    if count > self.layout_size or (self.stop and count > self.stop):
                        return
                    yield Locale(col, row, x, y, self.set_id(col, row), count, corner)
                    # next grid location
                    match _lower(self.direction):
                        case "e" | "east":
                            col = col + 1
                            if col > self.cols:
                                col = self.cols
                                if row_start == self.rows:
                                    row = row - 1
                                else:
                                    row = row + 1
                                self.direction = "w"

                        case "w" | "west":
                            col = col - 1
                            if col < 1:
                                col = 1
                                if row_start == self.rows:
                                    row = row - 1
                                else:
                                    row = row + 1
                                self.direction = "e"

                        case "s" | "south":
                            row = row + 1
                            if row > self.rows:
                                row = self.rows
                                if col_start == self.cols:
                                    col = col - 1
                                else:
                                    col = col + 1
                                self.direction = "n"

                        case "n" | "north":
                            row = row - 1
                            if row < 1:
                                row = 1
                                if col_start == self.cols:
                                    col = col - 1
                                else:
                                    col = col + 1
                                self.direction = "s"

                    x = self.x + (col - 1) * self.interval_x
                    y = self.y + (row - 1) * self.interval_y

                # ---- * outer
                case "outer" | "o":
                    if count > max_outer:
                        return
                    corner = None
                    if row == 1 and col == 1:
                        corner = "nw"
                    if row == self.rows and col == 1:
                        corner = "sw"
                    if row == self.rows and col == self.cols:
                        corner = "se"
                    if row == 1 and col == self.cols:
                        corner = "ne"
                    yield Locale(col, row, x, y, self.set_id(col, row), count, corner)

                    # next grid location
                    if row == 1 and col == 1:
                        corner = "nw"
                        if clockwise:
                            current_dir = "e"
                            col = col + 1
                        else:
                            current_dir = "s"
                            row = row + 1

                    if row == self.rows and col == 1:
                        corner = "sw"
                        if clockwise:
                            current_dir = "n"
                            row = row - 1
                        else:
                            current_dir = "e"
                            col = col + 1

                    if row == self.rows and col == self.cols:
                        corner = "se"
                        if clockwise:
                            current_dir = "w"
                            col = col - 1
                        else:
                            current_dir = "n"
                            row = row - 1

                    if row == 1 and col == self.cols:
                        corner = "ne"
                        if clockwise:
                            current_dir = "s"
                            row = row + 1
                        else:
                            current_dir = "w"
                            col = col - 1

                    if not corner:
                        match current_dir:
                            case "e" | "east":
                                col = col + 1
                            case "w" | "west":
                                col = col - 1
                            case "n" | "north":
                                row = row - 1
                            case "s" | "south":
                                row = row + 1

                    x = self.x + (col - 1) * self.interval_x
                    y = self.y + (row - 1) * self.interval_y

                # ---- * regular
                case _:  # default pattern
                    yield Locale(col, row, x, y, self.set_id(col, row), count, corner)
                    # next grid location
                    match _lower(self.direction):
                        case "e" | "east":
                            col = col + 1
                            if col > self.cols:
                                col = col_start
                                if row_start == self.rows:
                                    row = row - 1
                                    if row < 1:
                                        return  # end
                                else:
                                    row = row + 1
                                    if row > self.rows:
                                        return  # end
                        case "w" | "west":
                            col = col - 1
                            if col < 1:
                                col = col_start
                                if row_start == self.rows:
                                    row = row - 1
                                    if row < 1:
                                        return  # end
                                else:
                                    row = row + 1
                                    if row > self.rows:
                                        return  # end
                        case "s" | "south":
                            row = row + 1
                            if row > self.rows:
                                row = row_start
                                if col_start == self.cols:
                                    col = col - 1
                                    if col < 1:
                                        return  # end
                                else:
                                    col = col + 1
                                    if col > self.cols:
                                        return  # end
                        case "n" | "north":
                            row = row - 1
                            if row < 1:
                                row = row_start
                                if col_start == self.cols:
                                    col = col - 1
                                    if col < 1:
                                        return  # end
                                else:
                                    col = col + 1
                                    if col > self.cols:
                                        return  # end

                    x = self.x + (col - 1) * self.interval_x
                    y = self.y + (row - 1) * self.interval_y


class TriangularLocations(VirtualLocations):
    """
    Common properties and methods to define virtual triangular locations.
    """

    def __init__(self, rows=2, cols=2, **kwargs):
        super().__init__(rows, cols, **kwargs)
        self.kwargs = kwargs
        self.start = kwargs.get("start", "north")
        self.facing = kwargs.get("facing", "north")
        if (self.cols < 2 and self.rows < 1) or (self.cols < 1 and self.rows < 2):
            feedback(
                f"Minimum layout size is 2x1 or 1x2 (cannot use {self.cols }x{self.rows})!",
                True,
            )
        if _lower(self.start) not in [
            "north",
            "south",
            "east",
            "west",
            "n",
            "e",
            "w",
            "s",
        ]:
            feedback(
                f"{self.start} is not a valid start - " "use: 'n', 's', 'e', or 'w'",
                True,
            )

    def next_locale(self) -> Locale:
        """Yield next Location for each call."""
        _start = self.set_compass(_lower(self.start))
        # _dir = self.set_compass(_lower(self.direction))
        _facing = self.set_compass(_lower(self.facing))

        # TODO - create logic
        if _lower(self.pattern) in ["snake", "snaking", "s"]:
            feedback("Snake pattern NOT YET IMPLEMENTED", True)

        # ---- store row/col as list of lists
        array = []
        match _facing:
            case "north" | "south":
                for length in range(1, self.cols + 1):
                    _cols = list(range(1, length + 1))
                    if _cols:
                        array.append(_cols)
            case "east" | "west":
                for length in range(1, self.rows + 1):
                    _rows = list(range(1, length + 1))
                    if _rows:
                        array.append(_rows)
            case _:
                feedback(f"The facing value {self.facing} is not valid!", True)

        # ---- calculate initial conditions
        col_start, row_start = 1, 1
        match (_facing, _start):
            case ("north", "north"):
                row_start = 1
                col_start = 1
                # clockwise = True if _dir == "north" else False
            case ("north", "west"):
                row_start = 1
                col_start = self.cols
                # clockwise = True if _dir == "west" else False
            case ("north", "east"):
                row_start = self.rows
                col_start = 1
                # clockwise = True if _dir == "east" else False

        col, row, count = col_start, row_start, 0
        # max_outer = 2 * self.rows + (self.cols - 2) * 2
        corner = None
        # ---- set row and col interval
        match _facing:
            case "north" | "south":  # layout is row-oriented
                self.interval_x = self.side
                self.interval_y = math.sqrt(3) / 2.0 * self.side
            case "east" | "west":  # layout is col-oriented
                self.interval_x = math.sqrt(3) / 2.0 * self.side
                self.interval_y = self.side
        # ---- iterate the rows and cols
        # hlf_side = self.side / 2.0
        for key, entry in enumerate(array):
            match _facing:
                case "south":  # layout is row-oriented
                    y = (
                        self.y
                        + (self.rows - 1) * self.interval_y
                        - (key + 1) * self.interval_y
                    )
                    dx = (
                        0.5 * (self.cols - len(entry)) * self.interval_x
                        - (self.cols - 1) * 0.5 * self.interval_x
                    )
                    for val, loc in enumerate(entry):
                        count += 1
                        x = self.x + dx + val * self.interval_x
                        yield Locale(
                            loc, key + 1, x, y, self.set_id(loc, key + 1), count, corner
                        )
                case "north":  # layout is row-oriented
                    y = self.y + key * self.interval_y
                    dx = (
                        0.5 * (self.cols - len(entry)) * self.interval_x
                        - (self.cols - 1) * 0.5 * self.interval_x
                    )
                    for val, loc in enumerate(entry):
                        count += 1
                        x = self.x + dx + val * self.interval_x
                        yield Locale(
                            loc, key + 1, x, y, self.set_id(loc, key + 1), count, corner
                        )
                case "east":  # layout is col-oriented
                    x = (
                        self.x
                        + self.cols * self.interval_x
                        - (key + 2) * self.interval_x
                    )
                    dy = (
                        0.5 * (self.rows - len(entry)) * self.interval_y
                        - (self.rows - 1) * 0.5 * self.interval_y
                    )
                    for val, loc in enumerate(entry):
                        count += 1
                        y = self.y + dy + val * self.interval_y
                        yield Locale(
                            key + 1, loc, x, y, self.set_id(key + 1, loc), count, corner
                        )
                case "west":  # layout is col-oriented
                    x = self.x + key * self.interval_x
                    dy = (
                        0.5 * (self.rows - len(entry)) * self.interval_y
                        - (self.rows - 1) * 0.5 * self.interval_y
                    )
                    for val, loc in enumerate(entry):
                        count += 1
                        y = self.y + dy + val * self.interval_y
                        yield Locale(
                            key + 1, loc, x, y, self.set_id(key + 1, loc), count, corner
                        )


class DiamondLocations(VirtualLocations):
    """
    Common properties and methods to define virtual diamond locations.
    """

    def __init__(self, rows=1, cols=2, **kwargs):
        super().__init__(rows, cols, **kwargs)
        self.kwargs = kwargs
        if (self.cols < 2 and self.rows < 1) or (self.cols < 1 and self.rows < 2):
            feedback(
                f"Minimum layout size is 2x1 or 1x2 (cannot use {self.cols }x{self.rows})!",
                True,
            )

    def next_locale(self) -> Locale:
        """Yield next Location for each call."""


# ---- tracks

# See proto.py

# ---- other layouts


class ConnectShape(BaseShape):
    """
    Connect two shapes (Rectangle), based on a position, on a given canvas.

       Q4 | Q1
       -------
       Q3 | Q2

    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super().__init__(_object=_object, canvas=canvas, **kwargs)
        # overrides
        self.shape_from = kwargs.get("shape_from", None)  # could be a GridShape
        self.shape_to = kwargs.get("shape_to", None)  # could be a GridShape

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a connection (line) between two shapes on given canvas."""
        kwargs = self.kwargs | kwargs
        base_canvas = cnv
        cnv = cnv if cnv else self.canvas
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- style
        style = "direct"
        # ---- shapes and positions
        try:
            shp_from, shape_from_position = self.shape_from  # tuple form
        except Exception:
            shp_from, shape_from_position = self.shape_from, "S"
        try:
            shp_to, shape_to_position = self.shape_to  # tuple form
        except Exception:
            shp_to, shape_to_position = self.shape_to, "N"
        # ---- shape props
        shape_from = self.get_shape_in_grid(shp_from)
        shape_to = self.get_shape_in_grid(shp_to)
        edge_from = shape_from.get_bounds()
        edge_to = shape_to.get_bounds()
        x_f, y_f = self.key_positions(shape_from, shape_from_position)
        x_t, y_t = self.key_positions(shape_to, shape_to_position)
        xc_f, yc_f = shape_from.get_center()
        xc_t, yc_t = shape_to.get_center()
        # x,y: use fixed/supplied; or by "name"; or by default; or by "smart"
        if style == "path":
            # ---- path points
            points = []

            if xc_f == xc_t and yc_f > yc_t:  # above
                points = [
                    self.key_positions(shape_from, "S"),
                    self.key_positions(shape_to, "N"),
                ]
            if xc_f == xc_t and yc_f < yc_t:  # below
                points = [
                    self.key_positions(shape_from, "N"),
                    self.key_positions(shape_to, "S"),
                ]
            if xc_f > xc_t and yc_f == yc_t:  # left
                points = [
                    self.key_positions(shape_from, "W"),
                    self.key_positions(shape_to, "E"),
                ]
            if xc_f < xc_t and yc_f == yc_t:  # right
                points = [
                    self.key_positions(shape_from, "E"),
                    self.key_positions(shape_to, "W"),
                ]

            if xc_f < xc_t and yc_f < yc_t:  # Q1
                if edge_from.right < edge_to.left:
                    if edge_from.top < edge_to.bottom:
                        log.debug("A t:%s b:%s", edge_from.top, edge_to.bottom)
                        delta = (edge_to.bottom - edge_from.top) / 2.0
                        points = [
                            self.key_positions(shape_from, "N"),
                            (xc_f, edge_from.top + delta),
                            (xc_t, edge_from.top + delta),
                            self.key_positions(shape_to, "S"),
                        ]
                    elif edge_from.top > edge_to.bottom:
                        log.debug("B t:%s b:%s", edge_from.top, edge_to.bottom)
                        points = [
                            self.key_positions(shape_from, "N"),
                            (xc_f, yc_t),
                            self.key_positions(shape_to, "W"),
                        ]
                    else:
                        pass
                else:
                    log.debug("C t:%s b:%s", edge_from.top, edge_to.bottom)
                    points = [
                        self.key_positions(shape_from, "N"),
                        (xc_f, yc_t),
                        self.key_positions(shape_to, "W"),
                    ]
            if xc_f < xc_t and yc_f > yc_t:  # Q2
                log.debug("Q2")

            if xc_f > xc_t and yc_f > yc_t:  # Q3
                log.debug("Q3")

            if xc_f > xc_t and yc_f < yc_t:  # Q4
                log.debug("Q4")
                if edge_from.left < edge_to.right:
                    if edge_from.top < edge_to.bottom:
                        log.debug(" A t:%s b:%s", edge_from.top, edge_to.bottom)
                        delta = (edge_to.bottom - edge_from.top) / 2.0
                        points = [
                            self.key_positions(shape_from, "N"),
                            (xc_f, edge_from.top + delta),
                            (xc_t, edge_from.top + delta),
                            self.key_positions(shape_to, "S"),
                        ]
                    elif edge_from.top > edge_to.bottom:
                        log.debug(" B t:%s b:%s", edge_from.top, edge_to.bottom)
                        points = [
                            self.key_positions(shape_from, "N"),
                            (xc_f, yc_t),
                            self.key_positions(shape_to, "E"),
                        ]
                    else:
                        pass
                else:
                    log.debug(" C t:%s b:%s", edge_from.top, edge_to.bottom)
                    points = [
                        self.key_positions(shape_from, "N"),
                        (xc_f, yc_t),
                        self.key_positions(shape_to, "E"),
                    ]

            if xc_f == xc_t and yc_f == yc_t:  # same!
                return
            self.kwargs["points"] = points
            plin = PolylineShape(None, base_canvas, **self.kwargs)
            plin.draw(ID=ID)
        elif style == "direct":  # straight line
            # ---- direct points
            self.kwargs["x"] = x_f
            self.kwargs["y"] = y_f
            self.kwargs["x1"] = x_t
            self.kwargs["y1"] = y_t
            lin = LineShape(None, base_canvas, **self.kwargs)
            lin.draw(ID=ID)
        else:
            feedback('Style "{style}" is unknown.')

    def key_positions(self, _shape, location=None):
        """Calculate a dictionary of key positions around a Rectangle.

        N,S,E,W = North, South, East, West
        """
        top = _shape.y
        btm = _shape.y + _shape.height
        mid_horizontal = _shape.x + _shape.width / 2.0
        mid_vertical = _shape.y + _shape.height / 2.0
        left = _shape.x
        right = _shape.x + _shape.width
        _positions = {
            "NW": (left, top),
            "N": (mid_horizontal, top),
            "NE": (right, top),
            "SW": (left, btm),
            "S": (mid_horizontal, btm),
            "SE": (right, btm),
            "W": (left, mid_vertical),
            "E": (right, mid_vertical),
            # '': (),
        }
        if location:
            return _positions.get(location, ())
        return _positions
