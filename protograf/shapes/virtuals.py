# -*- coding: utf-8 -*-
"""
Create grids, repeats, sequences, and layouts for protograf
"""

# lib
import logging
import math

# third party

# project
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

log = logging.getLogger(__name__)
DEBUG = False

# ---- Virtual Class


class VirtualShape:
    """
    Common properties and methods for all virtual shapes (layout and track)
    """

    def __init__(self, rows=None, cols=None, **kwargs):
        """Common properties"""
        self.kwargs = kwargs
        self.centre_x = None
        self.centre_y = None
        self.start_x = None
        self.start_y = None
        self.rows = self.to_int(rows, "rows")
        self.cols = self.to_int(cols, "cols")
        # self.cells = {} - may be needed for some shapes e.g. HexHex

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
            return None

    def to_float(self, value, label="") -> int:
        """Set a value to a float; or stop if an invalid value."""
        try:
            float_value = float(value)
            return float_value
        except Exception:
            _label = f" for {label}" if label else ""
            feedback(f'"{value}"{_label} is not a valid floating number!', True)
            return None

    def unit(
        self, item, units: str | None = None, skip_none: bool = False, label: str = ""
    ):
        """Convert an item into the appropriate unit system."""
        log.debug("units %s %s :: label: %s", units, globals.units, label)
        if item is None and skip_none:
            return None
        units = support.to_units(units) if units is not None else globals.units
        try:
            _item = tools.as_float(item, label)
            return _item * units
        except (TypeError, ValueError):
            _label = f" {label}" if label else ""
            feedback(
                f"Unable to set unit value for{_label}: {item}."
                " Please check that this is a valid value.",
                stop=True,
            )
            return None


class HexHexLocations(VirtualShape):
    """
    HexHex Locations are not drawn on the canvas; they provide the
    locations/points where user-defined shapes will be drawn.
    """

    def __init__(self, rows=0, cols=0, **kwargs):
        super().__init__(rows=rows, cols=cols, **kwargs)
        base = globals.base  # protograf BaseCanvas
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
        # ---- custom properties
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
        self.cells = {}  # store (ring,ring_counter) : Point(x,y) at centre of cell
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
            radius=tools.unit(radius),
            diameter=tools.unit(diameter),
            side=tools.unit(side),
            half_side=tools.unit(half_side),
            half_flat=tools.unit(half_flat),
            height_flat=tools.unit(height_flat),
            z_fraction=z_fraction,
        )
        return hex_geometry

    @property
    def grid_centroid(self) -> Point:
        """Centre point of Grid in user units."""
        return None

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
        self.cells[(hex0.ring, hex0.counter)] = hex0.centre
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
            self.cells[(_hex.ring, _hex.counter)] = _hex.centre
            # ---- next hex
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
    locations/points where user-defined shapes can be drawn.
    """

    def __init__(self, rows, cols, **kwargs):
        super().__init__(rows=rows, cols=cols, **kwargs)
        self.x = self.to_float(kwargs.get("x", 1.0), "x")  # left(upper) corner
        self.y = self.to_float(kwargs.get("y", 1.0), "y")  # top(uppper) corner
        self.side = self.to_float(kwargs.get("side", 0), "side")
        self.layout_size = self.rows * self.cols
        self.interval = kwargs.get("interval", 1)
        self.interval_y = kwargs.get("interval_y", self.interval)
        self.interval_x = kwargs.get("interval_x", self.interval)
        # ---- offset
        self.col_even = kwargs.get("col_even", 0)
        self.col_odd = kwargs.get("col_odd", 0)
        self.row_even = kwargs.get("row_even", 0)
        self.row_odd = kwargs.get("row_odd", 0)
        # ---- layout
        self.pattern = kwargs.get("pattern", "default")
        self.direction = kwargs.get("direction", "east")  # for diamond, triangle
        self.facing = kwargs.get("facing", "east")
        self.flow = None  # used for snake; see validate() for setting
        # ---- start / end
        self.start = kwargs.get("start", None)
        self.stop = kwargs.get("stop", 0)
        self.label_style = kwargs.get("label_style", None)
        # ---- locations
        self.cells = {}  # store (col,row) : Point(x,y) at centre of cell
        # ----  check!
        self.validate()

    def validate(self):
        """Check for valid settings and combos."""
        self.stop = self.to_int(self.stop, "stop")
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
            if not isinstance(self, DiamondLocations):  # diamond does not use facing
                feedback(
                    f"Cannot use start '{self.start}' with facing '{self.direction}'!",
                    True,
                )
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
        return f"{col},{row}"

    def set_compass_primary(self, compass: str) -> str:
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

    def set_compass_secondary(self, compass: str) -> str:
        """Return full lower-case value of secondary compass direction."""
        if not compass:
            return None
        _compass = _lower(compass)
        match _compass:
            case "nw" | "northwest":
                return "northwest"
            case "sw" | "southwest":
                return "southwest"
            case "se" | "southeast":
                return "southeast"
            case "ne" | "northeast":
                return "northeast"
            case _:
                raise ValueError(
                    f'"{compass}" is an invalid secondary compass direction!'
                )

    @property
    def grid_centroid(self) -> Point:
        """Centre point of Grid in user units."""
        return None

    def next_locale(self) -> Locale:
        """Yield next Locale for each call."""


class RectangularLocations(VirtualLocations):
    """
    Common properties and methods to define a virtual rectangular layout.
    """

    def __init__(self, rows=2, cols=2, **kwargs):
        super().__init__(rows, cols, **kwargs)
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
        self.rectangle_validate(**kwargs)
        # ---- calculated values
        self.total_height = self.interval_x * (self.rows - 1)
        self.total_width = self.interval_y * (self.cols - 1)

    def rectangle_validate(self, **kwargs):
        """Check that settings for RectangularLocations are correct."""
        if self.cols < 2 or self.rows < 2:
            feedback(
                f"Minimum rectangular layout size is 2x2 (cannot use {self.cols }x{self.rows})!",
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

    @property
    def grid_centroid(self) -> Point:
        """Centre point of Grid in user units."""
        self.centre_x = self.x + 0.5 * self.total_width
        self.centre_y = self.y + 0.5 * self.total_height
        # _start = self.set_compass_secondary(_lower(self.start))
        # # ---- calculate centre points relative to facing
        # match _start:
        #     case "northwest":
        #         self.centre_x = self.x + 0.5 * self.total_width
        #         self.centre_y = self.y + 0.5 * self.total_height
        #     case "northeast":
        #         self.centre_x = self.x - 0.5 * self.total_width
        #         self.centre_y = self.y + 0.5 * self.total_height
        #     case "southwest":
        #         self.centre_x = self.x + 0.5 * self.total_width
        #         self.centre_y = self.y + 0.5 * self.total_height
        #     case "southeast":
        #         self.centre_x = self.x - 0.5 * self.total_width
        #         self.centre_y = self.y - 0.5 * self.total_height
        return Point(self.centre_x, self.centre_y)

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
            self.cells[(col, row)] = Point(
                x + self.interval_x / 2.0,
                y + self.interval_y / 2.0,
            )  # centre of cell
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
        self.start = kwargs.get("start", "north")
        self.facing = kwargs.get("facing", "north")
        self.triangle_validate()
        # ---- calculated values
        _facing = self.set_compass_primary(_lower(self.facing))
        match _facing:
            case "north" | "south":  # layout is row-oriented
                self.interval_x = self.side
                self.interval_y = math.sqrt(3) / 2.0 * self.side
                self.total_width = self.side * (self.cols - 1)
            case "east" | "west":  # layout is col-oriented
                self.interval_x = math.sqrt(3) / 2.0 * self.side
                self.interval_y = self.side
                self.total_width = self.side * (self.rows - 1)
        self.total_height = math.sqrt(self.total_width**2 * 0.5)

    def triangle_validate(self):
        """Check that settings for TriangularLocations are correct."""
        if (self.cols < 2 and self.rows < 1) or (self.cols < 1 and self.rows < 2):
            feedback(
                f"Minimum triangular layout size is 2x1 or 1x2 (cannot use {self.cols }x{self.rows})!",
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

    @property
    def grid_centroid(self) -> Point:
        """Centre point of Grid in user units."""
        _facing = self.set_compass_primary(_lower(self.facing))
        match _facing:
            case "north":
                self.centre_x = self.x
                self.centre_y = self.y + self.total_width / math.sqrt(3)
            case "south":
                self.centre_x = self.x
                self.centre_y = self.y - self.total_width * math.sqrt(3) / 6
                # but need to shift back up because tri rotated around centre
                self.centre_y = self.centre_y - math.sqrt(
                    0.75 * (self.total_width / 3.0) ** 2
                )
            case "east":
                self.centre_y = self.y
                self.centre_x = self.x - self.total_width / math.sqrt(3)
            case "west":
                self.centre_y = self.y
                self.centre_x = self.x + self.total_width / math.sqrt(3)
            case _:
                raise NotImplementedError(f"Cannot yet calculate centre for {_facing}")
        return Point(self.centre_x, self.centre_y)

    def next_locale(self) -> Locale:
        """Yield next Location for each call."""
        _start = self.set_compass_primary(_lower(self.start))
        _facing = self.set_compass_primary(_lower(self.facing))
        # TODO - create logic
        if _lower(self.pattern) in ["snake", "snaking", "s"]:
            feedback("Snake pattern NOT YET IMPLEMENTED for TriangleLocations", True)

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

        _, _, count = col_start, row_start, 0
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
                        self.cells[(loc, key + 1)] = Point(
                            x, y
                        )  # TODO centre of cell ???
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
                        self.cells[(loc, key + 1)] = Point(
                            x, y
                        )  # TODO centre of cell ???
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
                        self.cells[(loc, key + 1)] = Point(
                            x, y
                        )  # TODO centre of cell ???
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
                        self.cells[(loc, key + 1)] = Point(
                            x, y
                        )  # TODO centre of cell ???
                        yield Locale(
                            key + 1, loc, x, y, self.set_id(key + 1, loc), count, corner
                        )


class DiamondLocations(VirtualLocations):
    """
    Common properties and methods to define virtual diamond locations.
    """

    def __init__(self, rows=0, cols=0, **kwargs):
        super().__init__(rows, cols, **kwargs)
        if self.cols and not self.rows:
            self.rows = self.cols
        if self.rows and not self.cols:
            self.cols = self.rows
        if not self.rows and not self.cols:
            self.cols = 3
            self.rows = 3
        self.diamond_validate()
        # ---- calculated settings
        self._side = self.side  # self.unit(self.side) KEEP USER UNITS
        self.gap_col = math.sqrt(self._side**2 - (0.5 * self._side) ** 2)
        self.gap_row = self._side * 0.5
        self.total_height = 2 * self.gap_row * (self.rows // 2)
        self.total_width = self.gap_col * (self.cols - 1)
        self.array = self.diamond_array()
        # feedback(f"~~~ Dia {self.gap_col=} {self.total_height=} {self.total_width=}", False)

    def diamond_validate(self):
        """Check that settings for DiamondLayout are correct."""
        if self.cols < 3 or self.rows < 3:
            feedback(
                f"Minimum diamond layout size is 3x3 (cannot use {self.cols }x{self.rows})!",
                True,
            )
        if self.cols != self.rows:
            feedback(
                f"Diamond layout requires equal rows and cols (cannot use {self.cols }x{self.rows})!",
                True,
            )
        if not self.cols & 1 == 1:
            feedback(
                f"Diamond layout requires odd rows and cols (cannot use {self.cols }x{self.rows})!",
                True,
            )
        if _lower(self.facing) not in [
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
                f"'{self.facing}' is not a valid facing - use: 'n', 's', 'e', or 'w'",
                True,
            )

    def diamond_array(self) -> list:
        """Calculate sequenced rows and columns for DiamondLayout."""
        _facing = self.set_compass_primary(_lower(self.facing))
        # ---- store col/row as list of lists
        array = []
        match _facing:
            case "north":
                start_col = self.cols // 2 + 1
                mid_row = self.rows // 2 + 1
                items = 1
                for row in range(1, self.rows + 1):
                    for arr in range(0, items):
                        array.append([start_col + arr * 2, row])
                    if row < mid_row:
                        items += 1
                        start_col -= 1
                    else:
                        items -= 1
                        start_col += 1
            case "south":
                start_col = self.cols // 2 + 1
                mid_row = self.rows // 2 + 1
                items = 1
                for row in range(self.rows, 0, -1):
                    for arr in range(0, items):
                        array.append([start_col + arr * 2, row])
                    if row > mid_row:
                        items += 1
                        start_col -= 1
                    else:
                        items -= 1
                        start_col += 1
            case "east":
                start_row = self.rows // 2 + 1
                mid_col = self.cols // 2 + 1
                items = 1
                for col in range(self.cols, 0, -1):
                    for arr in range(0, items):
                        array.append([col, start_row + arr * 2])
                    if col > mid_col:
                        items += 1
                        start_row -= 1
                    else:
                        items -= 1
                        start_row += 1
            case "west":
                start_row = self.rows // 2 + 1
                mid_col = self.cols // 2 + 1
                items = 1
                for col in range(1, self.cols + 1):
                    for arr in range(0, items):
                        array.append([col, start_row + arr * 2])
                    if col < mid_col:
                        items += 1
                        start_row -= 1
                    else:
                        items -= 1
                        start_row += 1
            case _:
                feedback(
                    f"'{self.start}' is not a valid start - use: 'n', 's', 'e', or 'w'",
                    True,
                )
        # feedback(f"~~~ Dia {_facing=} {array=}", False)
        return array

    @property
    def grid_centroid(self) -> Point:
        """Centre point of Grid in user units."""
        _facing = self.set_compass_primary(_lower(self.facing))
        # ---- calculate centre points relative to facing
        match _facing:
            case "north":
                self.centre_x = self.x
                self.centre_y = self.y + 0.5 * self.total_height
            case "south":
                self.centre_x = self.x
                self.centre_y = self.y - 0.5 * self.total_height
            case "east":
                self.centre_x = self.x - 0.5 * self.total_width
                self.centre_y = self.y
            case "west":
                self.centre_x = self.x + 0.5 * self.total_width
                self.centre_y = self.y
        return Point(self.centre_x, self.centre_y)

    def next_locale(self) -> Locale:
        """Yield next Location for each call."""
        corner = None
        # ---- get offset
        _facing = self.set_compass_primary(_lower(self.facing))
        # ---- calculate initial location relative to facing
        match _facing:
            case "north":
                self.start_x = self.x - 0.5 * self.total_width
                self.start_y = self.y
            case "south":
                self.start_x = self.x - 0.5 * self.total_width
                self.start_y = self.y - self.total_height
            case "east":
                self.start_x = self.x - self.total_width
                self.start_y = self.y - 0.5 * self.total_height
            case "west":
                self.start_x = self.x
                self.start_y = self.y - 0.5 * self.total_height
        # ---- iterate the array
        for key, entry in enumerate(self.array):
            if entry[0] == self.cols // 2 + 1 and (
                entry[1] == 1 or entry[1] == self.rows
            ):
                corner = True
            elif entry[1] == self.rows // 2 + 1 and (
                entry[0] == 1 or entry[0] == self.cols
            ):
                corner = True
            else:
                corner = None
            dx, dy = entry[0], entry[1]  # col & row numbers
            x = self.start_x + (dx - 1) * self.gap_col
            y = self.start_y + (dy - 1) * self.gap_row
            # ("col", "row", "x", "y", "id", "sequence", "corner", "label", "page")
            _locale = Locale(
                entry[0],
                entry[1],
                x,
                y,
                self.set_id(entry[0], entry[1]),
                key + 1,
                corner,
            )
            self.cells[(entry[0], entry[1])] = Point(x, y)  # TODO centre of cell ???
            yield _locale


# ---- tracks

# See proto.py
