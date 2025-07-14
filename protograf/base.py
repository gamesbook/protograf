# -*- coding: utf-8 -*-
"""
Base shape class for protograf
"""
# lib
from collections import namedtuple
import copy
from enum import Enum
import inspect
import json
import io
import logging
import math
import os
from pathlib import Path, PosixPath
from sys import platform
from urllib.parse import urlparse

# third party
import cairosvg
import jinja2
from jinja2.environment import Template
import requests
from PIL import Image, ImageDraw, UnidentifiedImageError
import pymupdf
from pymupdf import (
    Document as muDocument,
    Font as muFont,
    Matrix,
    Point as muPoint,
    Page as muPage,
    Rect as muRect,
)
from pymupdf.utils import Shape as muShape
from pymupdf import (
    TEXT_ALIGN_CENTER,
    TEXT_ALIGN_RIGHT,
    TEXT_ALIGN_JUSTIFY,
    TEXT_ALIGN_LEFT,
)

# local
from protograf.utils import geoms, tools, support
from protograf.utils.constants import (
    CACHE_DIRECTORY,
    DEBUG_COLOR,
    DEFAULT_FONT,
    DEFAULT_MARGIN_SIZE,
    GRID_SHAPES_WITH_CENTRE,
)
from protograf.globals import unit
from protograf.utils.messaging import feedback
from protograf.utils.structures import (
    Bounds,
    GridShape,
    OffsetProperties,
    LookupType,
    TemplatingType,
    UnitProperties,
)
from protograf import globals

log = logging.getLogger(__name__)

DEBUG = False
WIDTH = 0.1


class BaseCanvas:
    """Wrapper/extension for a PyMuPDF Page."""

    def __init__(
        self,
        document: muDocument,
        paper: str = None,  # e.g. "A4", "Letter"
        defaults: dict = None,
        **kwargs,
    ):
        """Create self.doc_page as Page-equivalent."""
        self.jsonfile = kwargs.get("defaults", None)
        self.document = document
        self.doc_page = None
        self.defaults = {}
        # print(f"### {kwargs=}")
        # ---- setup defaults
        if self.jsonfile:
            try:
                with open(self.jsonfile) as data_file:
                    self.defaults = json.load(data_file)
            except (IOError, ValueError):
                filepath = tools.script_path()
                _jsonfile = os.path.join(filepath, self.jsonfile)
                try:
                    with open(_jsonfile) as data_file:
                        self.defaults = json.load(data_file)
                except (IOError, ValueError):
                    feedback(
                        f'Unable to find or load the file "{self.jsonfile}"'
                        f' - also checked in "{filepath}".',
                        True,
                    )
        # ---- override file defaults with BaseCanvas kwargs
        if kwargs:
            _kwargs = kwargs["kwargs"]
            for kwarg in _kwargs:
                self.defaults[kwarg] = _kwargs[kwarg]
            # print(f"### {self.defaults=}")
        # ---- constants
        self.default_length = 1
        self.show_id = False
        # ---- general
        self.shape = None
        self.shape_id = None
        self.sequence = self.defaults.get("sequence", [])
        self.dataset = []
        self.members = []  # card IDs, of which current card is a member
        self.bbox = None
        self._objects = None
        self.kwargs = kwargs
        self.run_debug = False
        _units = self.defaults.get("units", unit.cm)
        self.units = support.to_units(_units)
        # print(f'### {self.units=} {self.defaults=} {self.defaults.get("margin")=}')
        # ---- paper
        _paper = paper or self.defaults.get("paper", "A4")
        if isinstance(_paper, tuple) and len(_paper) == 2:
            self.paper = _paper
        else:
            try:
                self.paper = pymupdf.paper_size(_paper)  # (width, height) in points
                if self.paper == (-1, -1):  # pymupdf fallback ...
                    raise ValueError
            except Exception:
                feedback(f"Unable to use {_paper} as paper size!", True)
        # ---- paper size overrides
        self.paper_width = self.defaults.get("paper_width", self.paper[0])
        self.paper_height = self.defaults.get("paper_height", self.paper[1])
        # ---- paper size in units & margins
        self.page_width = self.paper[0] / self.units  # user-units e.g. cm
        self.page_height = self.paper[1] / self.units  # user-units e.g. cm
        self.margin = self.defaults.get("margin", DEFAULT_MARGIN_SIZE / self.units)
        # print(f"### {self.page_height=} {self.page_width=} {self.margin=} {self.units=}")
        self.margin_top = self.defaults.get("margin_top", self.margin)
        self.margin_bottom = self.defaults.get("margin_bottom", self.margin)
        self.margin_left = self.defaults.get("margin_left", self.margin)
        self.margin_right = self.defaults.get("margin_right", self.margin)
        # ---- sizes and positions
        self.row = self.defaults.get("row", None)
        self.col = self.defaults.get("col", self.defaults.get("column", None))
        self.side = self.defaults.get("side", 1)  # equal length sides
        self.height = self.defaults.get("height", self.side)
        self.width = self.defaults.get("width", self.side)
        self.top = self.defaults.get("width", self.width * 0.5)
        self.depth = self.defaults.get("depth", self.side)  # diamond
        self.x = self.defaults.get("x", self.defaults.get("left", 1))
        self.y = self.defaults.get("y", self.defaults.get("bottom", 1))
        self.cx = self.defaults.get("cx", None)  # NB! not 0; needed for internal check
        self.cy = self.defaults.get("cy", None)  # NB! not 0; needed for internal check
        self.scaling = self.defaults.get("scaling", None)
        self.dot_point = self.defaults.get("dot_point", 3.0)  # points
        # ---- to be calculated ...
        self.area = None
        self.vertexes = []
        # ---- repeats
        self.fill_pattern = self.defaults.get("fill_pattern", None)
        self.repeat = self.defaults.get("repeat", True)
        self.interval = self.defaults.get("interval", 0)
        self.interval_x = self.defaults.get("interval_x", self.interval)
        self.interval_y = self.defaults.get("interval_y", self.interval)
        # ---- rotation / position /elevation
        self.rotation = self.defaults.get("rotation", 0)  # degrees
        self.rotation_point = self.defaults.get("rotation_point", "centre")
        self.direction = self.defaults.get("direction", "north")
        self.position = self.defaults.get("position", None)
        self.flip = self.defaults.get("flip", "north")  # north/south
        self.elevation = self.defaults.get("elevation", "horizontal")
        self.facing = self.defaults.get("facing", "out")  # out/in
        # ---- fill color
        fill = self.defaults.get("fill", self.defaults.get("fill_color")) or "white"
        self.fill_transparency = self.defaults.get(
            "fill_transparency", 1
        )  # NOT transparent
        self.fill = tools.get_color(fill)
        self.fill_stroke = self.defaults.get("fill_stroke", None)
        self.stroke_fill = self.defaults.get("stroke_fill", None)  # alias
        # ---- stroke
        stroke = (
            self.defaults.get("stroke", self.defaults.get("stroke_color")) or "black"
        )
        self.stroke = tools.get_color(stroke)
        self.stroke_width = self.defaults.get("stroke_width", WIDTH)
        self.stroke_width_border = self.defaults.get("stroke_width_border", None)
        # pymupdf lineCap: 0 = line ends in sharp edge; 1 = adds semi-circle at end
        self.stroke_cap = self.defaults.get("stroke_cap", 0)
        self.stroke_transparency = self.defaults.get(
            "stroke_transparency", 1
        )  # NOT transparent
        self.outline = self.defaults.get("outline", None)
        self.outlined = self.defaults.get("outlined", False)
        # ---- overwrite fill & stroke
        if self.stroke_fill:  # alias
            self.stroke = self.stroke_fill
            self.fill = self.stroke_fill
        if self.fill_stroke:
            self.stroke = self.fill_stroke
            self.fill = self.fill_stroke
        # ---- debug color & transparency
        debug_color = self.defaults.get("debug_color", DEBUG_COLOR)
        self.debug_color = tools.get_color(debug_color)
        self.transparency = self.defaults.get("transparency", 1)  # NOT transparent
        # ---- font
        self.font_name = self.defaults.get("font_name", DEFAULT_FONT)
        self.font_file = self.defaults.get("font_file", None)
        self.font_size = self.defaults.get("font_size", 12)
        self.font_style = self.defaults.get("font_style", None)
        self.font_directory = self.defaults.get("font_directory", None)
        self.style = self.defaults.get("style", None)
        self.wrap = self.defaults.get("wrap", False)
        self.align = self.defaults.get("align", "centre")  # centre,left,right,justify
        self._alignment = TEXT_ALIGN_LEFT  # see to_alignment()
        # ---- grid cut marks
        self.grid_marks = self.defaults.get("grid_marks_marks", False)
        grid_marks_stroke = self.defaults.get("grid_marks_stroke", "gray")
        self.grid_marks_stroke = tools.get_color(grid_marks_stroke)
        self.grid_marks_stroke_width = self.defaults.get(
            "grid_marks_stroke_width", self.stroke_width
        )
        self.grid_marks_length = self.defaults.get(
            "grid_marks_length", 0.85
        )  # 1/3 inch
        self.grid_marks_offset = self.defaults.get("grid_marks_offset", 0)
        # ---- line style
        self.line_stroke = self.defaults.get("line_stroke", WIDTH)
        self.line_width = self.defaults.get("line_width", self.stroke_width)
        self.line_cap = self.defaults.get("line_cap", None)
        self.dotted = self.defaults.get("dotted", self.defaults.get("dotted", False))
        self.dashed = self.defaults.get("dashed", None)
        # ---- text: base
        self.text = self.defaults.get("text", "")
        self.text_size = self.defaults.get("text_size", self.font_size)
        text_stroke = self.defaults.get("text_stroke", self.stroke)
        self.text_stroke = tools.get_color(text_stroke)
        self.text_stroke_width = self.defaults.get("text_stroke_width", 0.05)  # pymu
        self.invisible = self.defaults.get("invisible", False)
        # ---- text: label
        self.label = self.defaults.get("label", "")
        self.label_size = self.defaults.get("label_size", self.font_size)
        self.label_face = self.defaults.get("label_face", self.font_name)
        label_stroke = self.defaults.get("label_stroke", self.stroke)
        self.label_stroke = tools.get_color(label_stroke)
        self.label_stroke_width = self.defaults.get(
            "label_stroke_width", self.stroke_width
        )
        self.label_mx = self.defaults.get("label_mx", 0)
        self.label_my = self.defaults.get("label_my", 0)
        self.label_rotation = self.defaults.get("label_rotation", 0)
        # ---- text: title
        self.title = self.defaults.get("title", "")
        self.title_size = self.defaults.get("title_size", self.font_size)
        self.title_face = self.defaults.get("title_face", self.font_name)
        title_stroke = self.defaults.get("title_stroke", self.stroke)
        self.title_stroke = tools.get_color(title_stroke)
        self.title_stroke_width = self.defaults.get(
            "title_stroke_width", self.stroke_width
        )
        self.title_mx = self.defaults.get("title_mx", 0)
        self.title_my = self.defaults.get("title_my", 0)
        self.title_rotation = self.defaults.get("title_rotation", 0)
        # ---- text: heading
        self.heading = self.defaults.get("heading", "")
        self.heading_size = self.defaults.get("heading_size", self.font_size)
        self.heading_face = self.defaults.get("heading_face", self.font_name)
        heading_stroke = self.defaults.get("heading_stroke", self.stroke)
        self.heading_stroke = tools.get_color(heading_stroke)
        self.heading_stroke_width = self.defaults.get(
            "heading_stroke_width", self.stroke_width
        )
        self.heading_mx = self.defaults.get("heading_mx", 0)
        self.heading_my = self.defaults.get("heading_my", 0)
        self.heading_rotation = self.defaults.get("heading_rotation", 0)
        # ---- text block
        self.leading = self.defaults.get("leading", self.font_size)
        self.transform = self.defaults.get("transform", None)
        self.html = self.defaults.get("html", False)
        self.css = self.defaults.get("css", None)
        # ---- polyomino / text outline
        self.outline_stroke = self.defaults.get("outline_stroke", None)
        self.outline_width = self.defaults.get("outline_width", 0)
        self.outline_dashed = self.defaults.get("outline_dashed", None)
        self.outline_dotted = self.defaults.get("outline_dotted", None)
        # if self.outlined:
        #     self.stroke = self.outline_stroke
        #     self.fill = None
        # ---- text block rectangle
        self.block_fill = self.defaults.get("block_fill", None)
        self.block_stroke = self.defaults.get("block_stroke", None)
        self.block_stroke_width = self.defaults.get("block_stroke_width", 0)
        self.block_dashed = self.defaults.get("block_dashed", None)
        self.block_dotted = self.defaults.get("block_dotted", None)
        self.block_transparency = self.defaults.get("block_transparency", None)
        # ---- image / file
        self.source = self.defaults.get("source", None)  # file or http://
        self.cache_directory = None  # should be a pathlib.Path object
        self.sliced = ""
        self.image_location = None
        # ---- line / ellipse / bezier / sector
        self.length = self.defaults.get("length", self.default_length)
        self.angle = self.defaults.get("angle", 0)
        self.angle_width = self.defaults.get("angle_width", 90)
        self.angle_start = self.defaults.get("angle_start", 0)
        # ---- chord
        self.angle_1 = self.defaults.get("angle1", 0)
        # ---- arc / sector
        self.filled = self.defaults.get("filled", False)
        # ---- arrow shape: head and tail
        self.points_offset = self.defaults.get("points_offset", 0)
        self.head_height = self.defaults.get("head_height", self.height)
        self.head_width = self.defaults.get("head_width", 2 * self.width)
        self.tail_width = self.defaults.get("tail_width", 0)  # adjusted in ArrowShape
        self.tail_notch = self.defaults.get("tail_notch", 0)
        # ---- arrowhead (on-a-line)
        self.arrow = self.defaults.get("arrow", False)
        self.arrow_double = self.defaults.get("arrow_double", False)
        self.arrow_style = self.defaults.get("arrow_style", None)
        self.arrow_position = self.defaults.get("arrow_position", None)  # 1 => end
        self.arrow_width = self.defaults.get("arrow_width", None)
        self.arrow_height = self.defaults.get("arrow_height", None)
        self.arrow_stroke = self.defaults.get(
            "arrow_stroke", None
        )  # see draw_arrowhead()
        self.arrow_fill = self.defaults.get("arrow_fill", None)  # see draw_arrowhead()
        # ---- line / bezier
        self.x_1 = self.defaults.get("x1", 0)
        self.y_1 = self.defaults.get("y1", 0)
        # ---- bezier
        self.x_2 = self.defaults.get("x2", 1)
        self.y_2 = self.defaults.get("y2", 1)
        self.x_3 = self.defaults.get("x3", 1)
        self.y_3 = self.defaults.get("y3", 1)
        # ---- rectangle / card
        self.rounding = self.defaults.get("rounding", 0)
        self.rounded = self.defaults.get("rounded", False)
        self.notch = self.defaults.get("notch", 0)
        self.notch_corners = self.defaults.get("notch_corners", "sw nw ne se")
        self.notch_x = self.defaults.get("notch_x", 0)
        self.notch_y = self.defaults.get("notch_y", 0)
        self.notch_style = self.defaults.get("notch_style", "snip")
        self.chevron = self.defaults.get("chevron", "")
        self.chevron_height = kwargs.get("chevron_height", 0)
        self.peaks = kwargs.get("peaks", [])
        self.peaks_dict = {}
        self.borders = kwargs.get("borders", [])
        self.rounded_radius = self.defaults.get(
            "rounded_radius", 0.05
        )  # fraction of smallest side
        self.roof = self.defaults.get("roof", [])
        self.roof_line = self.defaults.get("roof_line", 0)
        self.roof_line_mx = self.defaults.get("roof_line_mx", 0)
        self.roof_line_my = self.defaults.get("roof_line_my", 0)
        self.roof_stroke = self.defaults.get("roof_stroke", None)
        self.roof_stroke_width = self.defaults.get("roof_stroke", None)
        self.roof_reverse = self.defaults.get("roof_reverse", False)
        # ---- stadium
        self.edges = self.defaults.get("edges", "E W")
        # ---- grid layout
        self.grid = None  # some Shapes can auto-generate a GridShape
        self.rows = self.defaults.get("rows", 0)
        self.cols = self.defaults.get("cols", self.defaults.get("columns", 0))
        self.frame = self.defaults.get("frame", "rectangle")
        self.offset = self.defaults.get("offset", 0)  # from margin
        self.offset_x = self.defaults.get("offset_x", self.offset)
        self.offset_y = self.defaults.get("offset_y", self.offset)
        self.spacing = self.defaults.get("spacing", 0)  # between cards
        self.spacing_x = self.defaults.get("spacing_x", self.spacing)
        self.spacing_y = self.defaults.get("spacing_y", self.spacing)
        self.grouping = self.defaults.get("grouping", 1)  # no. of cards in a set
        self.grouping_rows = self.defaults.get("grouping_rows", self.grouping)
        self.grouping_cols = self.defaults.get("grouping_cols", self.grouping)
        self.lines = self.defaults.get("lines", "all")  # which direction to draw
        # ---- circle / star / polygon
        self.diameter = self.defaults.get("diameter", 1)
        self.radius = self.defaults.get("radius", self.diameter / 2.0)
        self.vertices = self.defaults.get("vertices", 5)
        self.sides = self.defaults.get("sides", 6)
        self.points = self.defaults.get("points", [])
        self.x_c = self.defaults.get("xc", 0)
        self.y_c = self.defaults.get("yc", 0)
        # ---- radii (circle, hex & polygon)
        self.radii = self.defaults.get("radii", [])
        self.radii_stroke = self.defaults.get("radii_stroke", self.stroke)
        self.radii_stroke_width = self.defaults.get(
            "radii_stroke_width", self.stroke_width
        )
        self.radii_length = self.defaults.get(
            "radii_length", None
        )  # default: circle radius
        self.radii_offset = self.defaults.get("radii_offset", 0)
        self.radii_cap = self.defaults.get("radii_cap", None)
        self.radii_dotted = self.defaults.get("radii_dotted", self.dotted)
        self.radii_dashed = self.defaults.get("radii_dashed", self.dashed)
        self.radii_labels = self.defaults.get("radii_labels", "")
        self.radii_labels_size = self.defaults.get("radii_labels_size", self.font_size)
        self.radii_labels_face = self.defaults.get("radii_labels_face", self.font_name)
        radii_labels_stroke = self.defaults.get("radii_labels_stroke", self.stroke)
        self.radii_labels_stroke = tools.get_color(radii_labels_stroke)
        self.radii_labels_stroke_width = self.defaults.get(
            "radii_labels_stroke_width", self.stroke_width
        )
        self.radii_labels_rotation = self.defaults.get("radii_labels_rotation", 0)
        self.radii_labels_my = self.defaults.get("radii_labels_my", 0)
        self.radii_labels_mx = self.defaults.get("radii_labels_mx", 0)
        # ---- circle
        self.petals = self.defaults.get("petals", 0)
        self.petals_style = self.defaults.get("petals_style", "triangle")
        self.petals_height = self.defaults.get("petals_height", 1)
        self.petals_offset = self.defaults.get("petals_offset", 0)
        self.petals_stroke = self.defaults.get("petals_stroke", self.stroke)
        self.petals_stroke_width = self.defaults.get(
            "petals_stroke_width", self.stroke_width
        )
        self.petals_fill = self.defaults.get("petals_fill", None)
        self.petals_dotted = self.defaults.get("petals_dotted", self.dotted)
        self.petals_dashed = self.defaults.get("petals_dashed", self.dashed)
        # ---- compass
        self.perimeter = self.defaults.get("perimeter", "circle")
        self.directions = self.defaults.get("directions", None)
        # ---- triangle / trapezoid / polyomino
        self.flip = self.defaults.get("flip", None)
        # ---- triangle / polyomino
        self.hand = self.defaults.get("hand", None)
        # ---- hexagon / circle
        self.centre_shape = self.defaults.get("centre_shape", "")
        self.centre_shape_mx = self.defaults.get("centre_shape_mx", 0)
        self.centre_shape_my = self.defaults.get("centre_shape_my", 0)
        self.dot = self.defaults.get("dot", 0)
        dot_stroke = self.defaults.get("dot_stroke", self.stroke)
        self.dot_stroke = tools.get_color(dot_stroke)
        self.dot_stroke_width = self.defaults.get("dot_stroke_width", self.stroke_width)
        self.dot_fill = self.defaults.get("dot_fill", self.dot_stroke)  # colors match
        self.cross = self.defaults.get("cross", 0)
        cross_stroke = self.defaults.get("cross_stroke", self.stroke)
        self.cross_stroke = tools.get_color(cross_stroke)
        self.cross_stroke_width = self.defaults.get(
            "cross_stroke_width", self.stroke_width
        )
        # ---- hexagon / polygon
        self.orientation = self.defaults.get("orientation", "flat")  # flat|pointy
        self.perbis = self.defaults.get("perbis", None)  # directions
        self.perbis_stroke = self.defaults.get("perbis_stroke", "black")
        self.perbis_stroke_width = self.defaults.get(
            "perbis_stroke_width", self.stroke_width
        )
        self.perbis_length = self.defaults.get("perbis_length", None)
        self.perbis_offset = self.defaults.get("perbis_offset", 0)
        self.perbis_cap = self.defaults.get("perbis_cap", None)
        self.perbis_dotted = self.defaults.get("perbis_dotted", self.dotted)
        self.perbis_dashed = self.defaults.get("perbis_dashed", self.dashed)
        # ---- hexagon
        self.caltrops = self.defaults.get("caltrops", None)
        self.caltrops_invert = self.defaults.get("caltrops_invert", False)
        self.links = self.defaults.get("links", None)
        self.link_stroke_width = self.defaults.get(
            "link_stroke_width", self.stroke_width
        )
        self.link_stroke = self.defaults.get("link_stroke", self.stroke)
        self.link_cap = self.defaults.get("link_cap", self.line_cap)
        # ---- hexagons
        self.hid = self.defaults.get("id", "")  # HEX ID
        self.hex_rows = self.defaults.get("hex_rows", 0)
        self.hex_cols = self.defaults.get("hex_cols", 0)
        self.hex_offset = self.defaults.get("hex_offset", "even")  # even|odd
        self.hex_layout = self.defaults.get("hex_layout", "rectangle")  # rectangle
        self.coord_type_x = self.defaults.get("coord_type_x", "number")  # number|letter
        self.coord_type_y = self.defaults.get("coord_type_y", "number")  # number|letter
        self.coord_start_x = self.defaults.get("coord_start_x", 0)
        self.coord_start_y = self.defaults.get("coord_start_y", 0)
        self.coord_elevation = self.defaults.get(
            "coord_elevation", None
        )  # top|middle|bottom
        self.coord_offset = self.defaults.get("coord_offset", 0)
        self.coord_font_name = self.defaults.get("coord_font_name", DEFAULT_FONT)
        self.coord_font_size = self.defaults.get(
            "coord_font_size", int(self.font_size * 0.5)
        )
        coord_stroke = self.defaults.get("coord_stroke", "black")
        self.coord_stroke = tools.get_color(coord_stroke)
        self.coord_padding = self.defaults.get("coord_padding", 2)
        self.coord_separator = self.defaults.get("coord_separator", "")
        self.coord_prefix = self.defaults.get("coord_prefix", "")
        self.coord_suffix = self.defaults.get("coord_suffix", "")
        self.coord_style = self.defaults.get("coord_style", "")
        self.hidden = self.defaults.get("hidden", [])
        # ---- starfield
        self.enclosure = None
        self.colors = ["white"]
        self.sizes = [self.defaults.get("stroke_width", WIDTH)]
        self.density = self.defaults.get("density", 10)
        self.star_pattern = "random"
        self.seeding = self.defaults.get("seeding", None)
        # ---- mesh
        self.mesh = self.defaults.get("mesh", None)
        # ---- hatches
        self.hatch_count = self.defaults.get("hatch_count", 0)
        self.hatch = self.defaults.get("hatch", "*")
        self.hatch_stroke = self.defaults.get("hatch_stroke", self.stroke)
        self.hatch_stroke_width = self.defaults.get(
            "hatch_stroke_width", self.stroke_width
        )
        self.hatch_dots = self.defaults.get("hatch_dots", None)
        self.hatch_cap = self.defaults.get("hatch_cap", self.line_cap)
        self.hatch_dashed = self.defaults.get("hatch_dashed", None)  # ---- OTHER
        # defaults for attributes called/set elsewhere e.g. in draw()
        self.use_abs = False
        self.use_abs_1 = False
        self.use_abs_c = False
        self.clockwise = True
        # ---- deck
        self.deck_data = []

    def get_canvas(self):
        """Return canvas (page) object"""
        return self.canvas

    def get_page(self, name="A4"):
        """Get a paper format by name from a pre-defined dictionary."""
        return pymupdf.paper_size(name)


class BaseShape:
    """Base class for objects drawn on a given canvas aka a pymupdf_utils_Shape"""

    def __init__(self, _object: muShape = None, canvas: BaseCanvas = None, **kwargs):
        self.kwargs = kwargs
        # feedback(f'### BaseShape {_object=} {canvas=} {kwargs=}')
        # ---- constants
        self.default_length = 1
        self.show_id = False  # True
        # ---- KEY
        self.doc_page = globals.doc_page
        self.canvas = canvas or globals.canvas  # pymupdf Shape
        base = _object or globals.base  # protograf BaseCanvas
        # print(f"### {type(self.canvas)=} {type(cnv)=} {type(base=)}")
        # print(f"### {self.canvas=} {cnv=} {base=}")
        self.shape_id = None
        self.sequence = kwargs.get("sequence", [])  # e.g. card numbers
        self.dataset = []  # list of dict data (loaded from file)
        self.members = []  # card IDs, of which current card is a member
        self._objects = None  # used by e.g. SequenceShape
        self.bbox = None
        # ---- general
        self.common = kwargs.get("common", None)
        self.shape = kwargs.get("shape", base.shape)
        self.run_debug = kwargs.get("debug", base.run_debug)
        _units = kwargs.get("units", base.units)
        self.units = support.to_units(_units)
        # print(f"### {self.units=}")
        # ---- paper
        _paper = kwargs.get("paper", base.paper)
        if isinstance(_paper, tuple) and len(_paper) == 2:
            self.paper = _paper
        else:
            try:
                self.paper = pymupdf.paper_size(_paper)  # (width, height) in points
                if self.paper == (-1, -1):  # pymupdf fallback ...
                    raise ValueError
            except Exception:
                feedback(f"Unable to use {_paper} as paper size!", True)
        # ---- paper overrides
        self.paper_width = self.kw_float(kwargs.get("paper_width", base.paper_width))
        self.paper_height = self.kw_float(kwargs.get("paper_height", base.paper_height))
        self.paper = (self.paper_width * self.units, self.paper_height * self.units)
        # ---- paper size in units
        self.page_width = self.paper[0] / self.units  # user-units e.g. cm
        self.page_height = self.paper[1] / self.units  # user-units e.g. cm
        # print(f"### {self.page_height=} {self.page_width=}")
        # ---- margins
        self.margin = self.kw_float(kwargs.get("margin", base.margin))
        self.margin_top = self.kw_float(kwargs.get("margin_top", self.margin))
        self.margin_bottom = self.kw_float(kwargs.get("margin_bottom", self.margin))
        self.margin_left = self.kw_float(kwargs.get("margin_left", self.margin))
        self.margin_right = self.kw_float(kwargs.get("margin_right", self.margin))
        # ---- grid marks
        self.grid_marks = self.kw_float(kwargs.get("grid_marks", base.grid_marks))
        self.grid_marks_stroke = kwargs.get("grid_marks_stroke", base.grid_marks_stroke)
        self.grid_marks_stroke_width = self.kw_float(
            kwargs.get("grid_marks_stroke_width", base.grid_marks_stroke_width)
        )
        self.grid_marks_length = self.kw_float(
            kwargs.get("grid_marks_length", base.grid_marks_length)
        )
        self.grid_marks_offset = self.kw_float(
            kwargs.get("grid_marks_offset", base.grid_marks_offset)
        )
        # ---- sizes and positions
        self.row = kwargs.get("row", base.row)
        self.col = self.kw_int(kwargs.get("col", kwargs.get("column", base.col)), "col")
        self.side = self.kw_float(kwargs.get("side", base.side))  # equal length sides
        self.height = self.kw_float(kwargs.get("height", self.side))
        self.width = self.kw_float(kwargs.get("width", self.side))
        self.top = self.kw_float(kwargs.get("top", base.top))
        self.depth = self.kw_float(kwargs.get("depth", self.side))  # diamond
        self.x = self.kw_float(kwargs.get("x", kwargs.get("left", base.x)))
        self.y = self.kw_float(kwargs.get("y", kwargs.get("top", base.y)))
        self.cx = self.kw_float(kwargs.get("cx", base.cx))  # centre (for some shapes)
        self.cy = self.kw_float(kwargs.get("cy", base.cy))  # centre (for some shapes)
        self.scaling = self.kw_float(kwargs.get("scaling", None))  # SVG images
        self.dot_point = self.kw_float(
            kwargs.get("dot_point", base.dot_point)
        )  # points
        # ---- to be calculated ...
        self.area = base.area
        self.vertexes = base.vertexes  # list of shape's "points"
        # ---- repeats
        self.fill_pattern = kwargs.get("fill_pattern", base.fill_pattern)
        self.repeat = kwargs.get("repeat", base.repeat)
        self.interval = self.kw_float(kwargs.get("interval", base.interval))
        self.interval_x = self.kw_float(kwargs.get("interval_x", base.interval_x))
        self.interval_y = self.kw_float(kwargs.get("interval_y", base.interval_y))
        # ---- rotation / position /elevation
        self.rotation = self.kw_float(
            kwargs.get("rotation", kwargs.get("rotation", base.rotation))
        )  # degrees anti-clockwise for text
        self.rotation_point = kwargs.get("rotation_point", None)
        self._rotation_theta = math.radians(self.rotation or 0)  # radians
        self.direction = kwargs.get("direction", base.direction)
        self.position = kwargs.get("position", base.position)
        self.elevation = kwargs.get("elevation", base.elevation)
        self.facing = kwargs.get("facing", base.facing)
        # ---- line style
        self.line_width = self.kw_float(kwargs.get("line_width", base.line_width))
        self.line_cap = kwargs.get("line_cap", base.line_cap)
        self.dotted = kwargs.get("dotted", kwargs.get("dots", base.dotted))
        self.dashed = kwargs.get("dashed", base.dashed)
        # ---- fill color
        self.fill = kwargs.get("fill", kwargs.get("fill_color", base.fill))
        self.fill_transparency = kwargs.get("fill_transparency", base.fill_transparency)
        # ---- stroke
        self.stroke = kwargs.get("stroke", kwargs.get("stroke_color", base.stroke))
        self.stroke_transparency = kwargs.get(
            "stroke_transparency", base.stroke_transparency
        )
        self.fill_stroke = kwargs.get("fill_stroke", base.fill_stroke)
        self.outline = kwargs.get("outline", base.outline)
        self.outlined = kwargs.get("outlined", base.outlined)
        self.stroke_width = self.kw_float(kwargs.get("stroke_width", base.stroke_width))
        self.stroke_width_border = self.kw_float(
            kwargs.get("stroke_width_border", base.stroke_width_border)
        )
        self.stroke_cap = self.kw_int(kwargs.get("stroke_cap", base.stroke_cap))
        # ---- overwrite fill&stroke colors
        if self.fill_stroke and self.outline:
            feedback("Cannot set 'fill_stroke' and 'outline' together!", True)
        if self.fill_stroke:
            self.stroke = self.fill_stroke
            self.fill = self.fill_stroke
        # ---- debug color & transparency
        self.debug_color = kwargs.get("debug_color", base.debug_color)
        self.transparency = self.kw_float(kwargs.get("transparency", base.transparency))
        # ---- font
        self.font_name = kwargs.get("font_name", base.font_name)
        self.font_file = kwargs.get("font_file", base.font_file)
        self.font_size = self.kw_float(kwargs.get("font_size", base.font_size))
        self.font_style = kwargs.get("font_style", base.font_style)
        self.font_directory = kwargs.get("font_directory", base.font_directory)
        self.style = kwargs.get("style", base.style)
        self.wrap = kwargs.get("wrap", base.wrap)
        self.align = kwargs.get("align", base.align)  # centre,left,right,justify
        self._alignment = TEXT_ALIGN_LEFT  # see to_alignment()
        # ---- text: base
        self.text = kwargs.get("text", base.text)
        self.text_size = self.kw_float(kwargs.get("text_size", base.text_size))
        self.text_stroke = kwargs.get("text_stroke", base.text_stroke)
        self.text_stroke_width = self.kw_float(
            kwargs.get("text_stroke_width", base.text_stroke_width)
        )
        self.invisible = self.kw_bool(kwargs.get("invisible", base.invisible))
        # ---- text: label
        self.label = kwargs.get("label", base.label)
        self.label_size = self.kw_float(kwargs.get("label_size", self.font_size))
        self.label_face = kwargs.get("label_face", self.font_name)
        self.label_stroke = kwargs.get("label_stroke", self.stroke)
        self.label_stroke_width = self.kw_float(
            kwargs.get("label_stroke_width", self.stroke_width)
        )
        self.label_mx = self.kw_float(kwargs.get("label_mx", 0))
        self.label_my = self.kw_float(kwargs.get("label_my", 0))
        self.label_rotation = self.kw_float(kwargs.get("label_rotation", 0))
        # ---- text: title
        self.title = kwargs.get("title", base.title)
        self.title_size = self.kw_float(kwargs.get("title_size", self.font_size))
        self.title_face = kwargs.get("title_face", self.font_name)
        self.title_stroke = kwargs.get("title_stroke", self.stroke)
        self.title_stroke_width = self.kw_float(
            kwargs.get("title_stroke_width", self.stroke_width)
        )
        self.title_mx = self.kw_float(kwargs.get("title_mx", 0))
        self.title_my = self.kw_float(kwargs.get("title_my", 0))
        self.title_rotation = self.kw_float(kwargs.get("title_rotation", 0))
        # ---- text: heading
        self.heading = kwargs.get("heading", base.heading)
        self.heading_size = self.kw_float(kwargs.get("heading_size", self.font_size))
        self.heading_face = kwargs.get("heading_face", self.font_name)
        self.heading_stroke = kwargs.get("heading_stroke", self.stroke)
        self.heading_stroke_width = self.kw_float(
            kwargs.get("heading_stroke_width", self.stroke_width)
        )
        self.heading_mx = self.kw_float(kwargs.get("heading_mx", 0))
        self.heading_my = self.kw_float(kwargs.get("heading_my", 0))
        self.heading_rotation = self.kw_float(kwargs.get("heading_rotation", 0))
        # ---- text block
        self.transform = kwargs.get("transform", base.transform)
        self.html = self.kw_bool(kwargs.get("html", base.html))
        self.css = kwargs.get("css", base.css)
        self.leading = self.kw_float(kwargs.get("leading", self.font_size))
        # ---- polyomino / text outline
        self.outline_stroke = kwargs.get("outline_stroke", base.outline_stroke)
        self.outline_width = self.kw_float(
            kwargs.get("outline_width", base.outline_width)
        )
        self.outline_dashed = kwargs.get("outline_dashed", base.outline_dashed)
        self.outline_dotted = kwargs.get("outline_dotted", base.outline_dotted)
        # if self.outlined:
        #     self.stroke = self.outline_stroke
        #     self.fill = None
        # ---- text block
        self.block_stroke = kwargs.get("block_stroke", base.block_stroke)
        self.block_fill = kwargs.get("block_fill", base.block_fill)
        self.block_stroke_width = self.kw_float(
            kwargs.get("block_stroke_width", base.block_stroke_width)
        )
        self.block_dashed = kwargs.get("block_dashed", base.block_dashed)
        self.block_dotted = kwargs.get("block_dotted", base.block_dotted)
        self.block_transparency = kwargs.get(
            "block_transparency", base.block_transparency
        )
        # feedback(f"### BShp:"
        # f"{self} {kwargs.get('fill')=} {self.fill=} {kwargs.get('fill_color')=}")
        # ---- image / file
        self.source = kwargs.get("source", base.source)  # file or http://
        self.sliced = ""
        self.image_location = None
        # ---- line / ellipse / bezier / arc / polygon
        self.length = self.kw_float(kwargs.get("length", base.length))
        self.angle = self.kw_float(
            kwargs.get("angle", base.angle)
        )  # anti-clockwise from flat
        self.angle_width = self.kw_float(
            kwargs.get("angle_width", base.angle_width)
        )  # delta degrees
        self.angle_start = self.kw_float(
            kwargs.get("angle_start", base.angle_start)
        )  # degrees anti-clockwise from flat
        self._angle_theta = math.radians(self.angle)
        # ---- image
        self.cache_directory = None  # should be a pathlib.Path object
        # ---- chord
        self.angle_1 = self.kw_float(
            kwargs.get("angle1", base.angle_1)
        )  # anti-clockwise from flat
        self._angle_1_theta = math.radians(self.angle_1)
        # ---- arc / sector
        self.filled = self.kw_bool(kwargs.get("filled", base.filled))
        # ---- arrow shape: head, points and tail
        self.points_offset = self.kw_float(
            kwargs.get("points_offset", base.points_offset)
        )
        self.head_height = self.kw_float(kwargs.get("head_height", base.head_height))
        self.head_width = self.kw_float(kwargs.get("head_width", base.head_width))
        self.tail_width = self.kw_float(kwargs.get("tail_width", base.tail_width))
        self.tail_notch = self.kw_float(kwargs.get("tail_notch", base.tail_notch))
        # ---- arrowhead (on-a-line)
        self.arrow = self.kw_bool(kwargs.get("arrow", base.arrow))
        self.arrow_double = self.kw_bool(kwargs.get("arrow_double", base.arrow_double))
        self.arrow_style = kwargs.get("arrow_style", base.arrow_style)
        self.arrow_position = kwargs.get("arrow_position", base.arrow_position)
        self.arrow_width = kwargs.get("arrow_width", base.arrow_width)
        self.arrow_height = kwargs.get("arrow_height", base.arrow_height)
        self.arrow_stroke = kwargs.get("arrow_stroke", base.arrow_stroke)
        self.arrow_fill = kwargs.get("arrow_fill", base.arrow_fill)
        # ---- line / bezier / sector
        self.x_1 = self.kw_float(kwargs.get("x1", base.x_1))
        self.y_1 = self.kw_float(kwargs.get("y1", base.y_1))
        # ---- bezier / sector
        self.x_2 = self.kw_float(kwargs.get("x2", base.x_2))
        self.y_2 = self.kw_float(kwargs.get("y2", base.y_2))
        self.x_3 = self.kw_float(kwargs.get("x3", base.x_3))
        self.y_3 = self.kw_float(kwargs.get("y3", base.y_3))
        # ---- rectangle / card
        self.rounding = self.kw_float(kwargs.get("rounding", base.rounding))
        self.rounded = kwargs.get("rounded", base.rounded)
        self.notch = self.kw_float(kwargs.get("notch", base.notch))
        self.notch_corners = kwargs.get("notch_corners", base.notch_corners)
        self.notch_x = self.kw_float(kwargs.get("notch_x", base.notch_x))
        self.notch_y = self.kw_float(kwargs.get("notch_y", base.notch_y))
        self.notch_style = kwargs.get("notch_style", base.notch_style)
        self.chevron = kwargs.get("chevron", base.chevron)
        self.chevron_height = self.kw_float(
            kwargs.get("chevron_height", base.chevron_height)
        )
        self.peaks = kwargs.get("peaks", base.peaks)
        self.peaks_dict = {}
        self.borders = kwargs.get("borders", base.borders)
        self.rounded_radius = base.rounded_radius
        self.roof = kwargs.get("roof", base.roof)
        self.roof_line = kwargs.get("roof_line", base.roof_line)
        self.roof_line_mx = kwargs.get("roof_line_mx", base.roof_line_mx)
        self.roof_line_my = kwargs.get("roof_line_my", base.roof_line_my)
        self.roof_reverse = kwargs.get("roof_reverse", base.roof_reverse)
        self.roof_stroke = kwargs.get("roof_stroke", base.roof_stroke)
        self.roof_stroke_width = kwargs.get("roof_stroke_width", base.roof_stroke_width)
        # ---- stadium
        self.edges = kwargs.get("edges", base.edges)
        # ---- grid layout
        self.rows = self.kw_int(kwargs.get("rows", base.rows), "rows")
        self.cols = self.kw_int(
            kwargs.get("cols", kwargs.get("columns", base.cols)), "cols"
        )
        self.frame = kwargs.get("frame", base.frame)
        self.offset = self.kw_float(kwargs.get("offset", base.offset))
        self.offset_x = self.kw_float(kwargs.get("offset_x", self.offset))
        self.offset_y = self.kw_float(kwargs.get("offset_y", self.offset))
        self.spacing = self.kw_float(kwargs.get("spacing", base.spacing))
        self.spacing_x = self.kw_float(kwargs.get("spacing_x", self.spacing))
        self.spacing_y = self.kw_float(kwargs.get("spacing_y", self.spacing))
        self.grouping = self.kw_int(
            kwargs.get("grouping", 1), "grouping"
        )  # no. of cards in a set
        self.grouping_rows = self.kw_int(
            kwargs.get("grouping_rows", self.grouping), "grouping_rows"
        )
        self.grouping_cols = self.kw_int(
            kwargs.get("grouping_cols", self.grouping), "grouping_cols"
        )
        self.lines = kwargs.get("lines", base.lines)
        # ---- circle / star / polygon
        self.diameter = self.kw_float(kwargs.get("diameter", base.diameter))
        self.radius = self.kw_float(kwargs.get("radius", base.radius))
        self.vertices = self.kw_int(kwargs.get("vertices", base.vertices), "vertices")
        self.sides = kwargs.get("sides", base.sides)
        self.points = kwargs.get("points", base.points)
        # ---- radii (circle / hexagon / polygon / compass)
        self.radii = kwargs.get("radii", base.radii)
        self.radii_stroke = kwargs.get("radii_stroke", self.stroke)
        self.radii_stroke_width = self.kw_float(
            kwargs.get("radii_stroke_width", base.radii_stroke_width)
        )
        self.radii_length = self.kw_float(kwargs.get("radii_length", base.radii_length))
        self.radii_offset = self.kw_float(kwargs.get("radii_offset", base.radii_offset))
        self.radii_cap = kwargs.get("radii_cap", base.radii_cap)
        self.radii_dotted = kwargs.get("radii_dotted", base.dotted)
        self.radii_dashed = kwargs.get("radii_dashed", self.dashed)
        self.radii_labels = kwargs.get("radii_labels", base.radii_labels)
        self.radii_labels_size = self.kw_float(
            kwargs.get("radii_labels_size", self.font_size)
        )
        self.radii_labels_face = kwargs.get("radii_labels_face", self.font_name)
        self.radii_labels_stroke = kwargs.get("radii_labels_stroke", self.stroke)
        self.radii_labels_stroke_width = self.kw_float(
            kwargs.get("radii_labels_stroke_width", self.stroke_width)
        )
        self.radii_labels_rotation = self.kw_float(
            kwargs.get("radii_labels_rotation", 0)
        )
        self.radii_labels_my = self.kw_float(kwargs.get("radii_labels_my", 0))
        self.radii_labels_mx = self.kw_float(kwargs.get("radii_labels_mx", 0))
        # ---- circle
        self.petals = self.kw_int(kwargs.get("petals", base.petals), "petals")
        self.petals_style = kwargs.get("petals_style", base.petals_style)
        self.petals_height = self.kw_float(
            kwargs.get("petals_height", base.petals_height)
        )
        self.petals_offset = self.kw_float(
            kwargs.get("petals_offset", base.petals_offset)
        )
        self.petals_stroke = kwargs.get("petals_stroke", base.petals_stroke)
        self.petals_stroke_width = self.kw_float(
            kwargs.get("petals_stroke_width", base.petals_stroke_width)
        )
        self.petals_fill = kwargs.get("petals_fill", base.petals_fill)
        self.petals_dotted = kwargs.get("petals_dotted", base.petals_dotted)
        self.petals_dashed = kwargs.get("petals_dashed", self.dashed)
        # ---- compass
        self.perimeter = kwargs.get("perimeter", "circle")  # circle|rectangle|hexagon
        self.directions = kwargs.get("directions", None)
        # ---- triangle / trapezoid / polyomino
        self.flip = kwargs.get("flip", base.flip)
        # ---- triangle / polyomino
        self.hand = kwargs.get("hand", base.hand)
        # ---- hexagon / circle / polygon
        self.centre_shape = kwargs.get("centre_shape", "")
        self.centre_shape_mx = self.kw_float(
            kwargs.get("centre_shape_mx", base.centre_shape_mx)
        )
        self.centre_shape_my = self.kw_float(
            kwargs.get("centre_shape_my", base.centre_shape_my)
        )
        self.dot_stroke = kwargs.get("dot_stroke", self.stroke)
        self.dot_stroke_width = self.kw_float(
            kwargs.get("dot_stroke_width", base.dot_stroke_width)
        )
        self.dot_fill = kwargs.get("dot_fill", self.stroke)
        self.dot = self.kw_float(kwargs.get("dot", base.dot))
        self.cross_stroke = kwargs.get("cross_stroke", self.stroke)
        self.cross_stroke_width = self.kw_float(
            kwargs.get("cross_stroke_width", base.cross_stroke_width)
        )
        self.cross = self.kw_float(kwargs.get("cross", base.cross))
        # ---- hexagon / polygon
        self.orientation = kwargs.get("orientation", base.orientation)
        self.perbis = kwargs.get("perbis", base.perbis)  # directions
        self.perbis_stroke = kwargs.get("perbis_stroke", base.perbis_stroke)
        self.perbis_stroke_width = self.kw_float(
            kwargs.get("perbis_stroke_width", base.perbis_stroke_width)
        )
        self.perbis_length = self.kw_float(
            kwargs.get("perbis_length", base.perbis_length)
        )
        self.perbis_offset = self.kw_float(
            kwargs.get("perbis_offset", base.perbis_offset)
        )
        self.perbis_cap = kwargs.get("perbis_cap", base.perbis_cap)
        self.perbis_dotted = kwargs.get("perbis_dotted", base.dotted)
        self.perbis_dashed = kwargs.get("perbis_dashed", self.dashed)
        # ---- hexagon
        self.caltrops = self.kw_float(kwargs.get("caltrops", base.caltrops))
        self.caltrops_invert = self.kw_bool(
            kwargs.get("caltrops_invert", base.caltrops_invert)
        )
        self.links = kwargs.get("links", base.links)
        self.link_stroke_width = self.kw_float(
            kwargs.get("link_stroke_width", base.link_stroke_width)
        )
        self.link_stroke = kwargs.get("link_stroke", base.stroke)
        self.link_cap = kwargs.get("link_cap", base.link_cap)
        # ---- hexagons
        self.hid = kwargs.get("id", base.hid)  # HEX ID
        self.hex_rows = self.kw_int(kwargs.get("hex_rows", base.hex_rows), "hex_rows")
        self.hex_cols = self.kw_int(kwargs.get("hex_cols", base.hex_cols), "hex_cols")
        self.hex_layout = kwargs.get(
            "hex_layout", base.hex_layout
        )  # rectangle|circle|diamond|triangle
        self.hex_offset = kwargs.get("hex_offset", base.hex_offset)  # even|odd
        self.coord_type_x = kwargs.get(
            "coord_type_x", base.coord_type_x
        )  # number|letter
        self.coord_type_y = kwargs.get(
            "coord_type_y", base.coord_type_y
        )  # number|letter
        self.coord_start_x = self.kw_int(
            kwargs.get("coord_start_x", base.coord_start_x), "coord_start_x"
        )
        self.coord_start_y = self.kw_int(
            kwargs.get("coord_start_y", base.coord_start_y), "coord_start_y"
        )
        self.coord_elevation = kwargs.get(
            "coord_elevation", base.coord_elevation
        )  # top|middle|bottom
        self.coord_offset = self.kw_float(kwargs.get("coord_offset", base.coord_offset))
        self.coord_font_name = kwargs.get("coord_font_name", base.coord_font_name)
        self.coord_font_size = self.kw_float(
            kwargs.get("coord_font_size", base.coord_font_size)
        )
        self.coord_stroke = kwargs.get("coord_stroke", base.coord_stroke)
        self.coord_padding = self.kw_int(
            kwargs.get("coord_padding", base.coord_padding), "coord_padding"
        )
        self.coord_separator = kwargs.get("coord_separator", base.coord_separator)
        self.coord_prefix = kwargs.get("coord_prefix", base.coord_prefix)
        self.coord_suffix = kwargs.get("coord_suffix", base.coord_suffix)
        self.coord_style = kwargs.get("coord_style", "")  # linear|diagonal
        self.hidden = kwargs.get("hidden", base.hidden)
        # ---- starfield
        self.enclosure = kwargs.get("enclosure", base.enclosure)
        self.colors = kwargs.get("colors", base.colors)
        self.sizes = kwargs.get("sizes", base.sizes)
        self.density = self.kw_int(kwargs.get("density", base.density), "density")
        self.star_pattern = kwargs.get("star_pattern", base.star_pattern)
        self.seeding = kwargs.get("seeding", base.seeding)
        # ---- mesh
        self.mesh = kwargs.get("mesh", base.mesh)
        # ---- hatches
        self.hatch_count = kwargs.get("hatch_count", base.hatch_count)
        self.hatch = kwargs.get("hatch", base.hatch)
        self.hatch_stroke_width = self.kw_float(
            kwargs.get("hatch_width", base.hatch_stroke_width)
        )
        self.hatch_stroke = kwargs.get("hatch_stroke", base.stroke)
        self.hatch_cap = kwargs.get("hatch_cap", base.hatch_cap)
        self.hatch_dots = kwargs.get("hatch_dots", base.dotted)
        self.hatch_dashed = kwargs.get("hatch_dashed", self.dashed)
        # ---- deck
        self.deck_data = kwargs.get("deck_data", [])  # list of dicts

        # ---- OTHER
        # defaults for attributes called/set elsewhere e.g. in draw()
        self.use_abs = False
        self.use_abs_1 = False
        self.use_abs_c = False
        # ---- CHECK ALL
        correct, issue = self.check_settings()
        if not correct:
            feedback("Problem with settings: %s." % "; ".join(issue))
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
                    # print(f'### Common {attr=} {base=} {type(base)=}')
                    common_attr = getattr(self.common, attr)
                    base_attr = getattr(base, attr)
                    if common_attr != base_attr:
                        setattr(self, attr, common_attr)

        # ---- SET offset properties to correct units
        self._o = self.set_offset_props()
        # ---- SET UNIT PROPS (last!)
        self.set_unit_properties()

    def __str__(self):
        try:
            return f"{self.__class__.__name__}::{self.kwargs}"
        except:
            return f"{self.__class__.__name__}"

    def kw_float(self, value, label: str = ""):
        return tools.as_float(value, label) if value is not None else value

    def kw_int(self, value, label: str = ""):
        return tools.as_int(value, label) if value is not None else value

    def kw_bool(self, value, label: str = ""):
        return tools.as_bool(value, label) if value is not None else value

    def unit(self, item, units: str = None, skip_none: bool = False, label: str = ""):
        """Convert an item into the appropriate unit system."""
        log.debug("units %s %s :: label: %s", units, self.units, label)
        if item is None and skip_none:
            return None
        units = support.to_units(units) if units is not None else self.units
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

    def set_unit_properties(self):
        """Convert base properties into unit-based values."""
        # set a "width" value for use in calculations e.g. Track
        if self.radius and not self.width:
            self.width = 2.0 * self.radius
            self.diameter = 2.0 * self.radius
        if self.diameter and not self.width:
            self.width = self.diameter
        if self.side and not self.width:
            self.width = self.side  # square
        if self.side and not self.height:
            self.height = self.side  # square
        if self.diameter and not self.radius:
            self.radius = self.diameter / 2.0
        if self.width and not self.top:
            self.top = 0.5 * self.width

        self._u = UnitProperties(
            self.paper[0],  # width, in points
            self.paper[1],  # height, in points
            self.unit(self.margin_left) if self.margin_left is not None else None,
            self.unit(self.margin_right) if self.margin_right is not None else None,
            self.unit(self.margin_bottom) if self.margin_bottom is not None else None,
            self.unit(self.margin_top) if self.margin_top else None,
            self.unit(self.x) if self.x is not None else None,
            self.unit(self.y) if self.y is not None else None,
            self.unit(self.cx) if self.cx is not None else None,
            self.unit(self.cy) if self.cy is not None else None,
            self.unit(self.height) if self.height is not None else None,
            self.unit(self.width) if self.width is not None else None,
            self.unit(self.top) if self.top is not None else None,
            self.unit(self.radius) if self.radius is not None else None,
            self.unit(self.diameter) if self.diameter is not None else None,
            self.unit(self.side) if self.side is not None else None,
            self.unit(self.length) if self.length is not None else None,
            self.unit(self.spacing_x) if self.spacing_x is not None else None,
            self.unit(self.spacing_y) if self.spacing_y is not None else None,
            self.unit(self.offset_x) if self.offset_x is not None else None,
            self.unit(self.offset_y) if self.offset_y is not None else None,
        )

    def set_offset_props(self, off_x=0, off_y=0):
        """OffsetProperties in point units for a Shape."""
        margin_left = (
            self.unit(self.margin_left) if self.margin_left is not None else self.margin
        )
        margin_bottom = (
            self.unit(self.margin_bottom)
            if self.margin_bottom is not None
            else self.margin
        )
        margin_top = (
            self.unit(self.margin_top) if self.margin_top is not None else self.margin
        )
        off_x = self.unit(off_x) if off_x is not None else None
        off_y = self.unit(off_y) if off_y is not None else None
        return OffsetProperties(
            off_x=off_x,
            off_y=off_y,
            delta_x=off_x + margin_left,
            delta_y=off_y + margin_top,
        )

    def draw_polyline_props(self, cnv: muShape, vertexes: list, **kwargs) -> bool:
        """Draw polyline IF either fill or stroke is set.

        Args:
            vertexes (list): Point tuples

        Notes:
            Ensure that **kwargs default to `self` values!
        """
        # print(f'### dpp {kwargs.get("fill")=} {kwargs.get("stroke")=} {vertexes=}')
        if kwargs.get("stroke") or kwargs.get("fill"):
            cnv.draw_polyline(vertexes)
            return True
        return False

    def set_canvas_props(
        self,
        cnv=None,
        index=None,  # extract from list of potential values (usually Card options)
        **kwargs,
    ):
        """Wrapper is here to pass self attributes into set_canvas_props."""
        defaults = {}
        defaults["fill"] = self.fill
        defaults["stroke"] = self.stroke
        defaults["stroke_cap"] = self.stroke_cap
        defaults["stroke_width"] = self.stroke_width
        defaults["transparency"] = self.transparency
        defaults["dotted"] = self.dotted
        defaults["dashed"] = self.dashed
        if kwargs.get("rounded"):
            kwargs["lineJoin"] = 1
        # print(f'### SetCnvProps: {kwargs.keys()} \n {kwargs.get("closed", "?")=}')
        return tools.set_canvas_props(cnv, index, defaults, **kwargs)

    def set_abs_and_offset(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        self._o = self.set_offset_props(off_x, off_y)
        # self._abs... variable are absolute locations in native units;
        #  They are for internal use only and are not expected
        #  to be called by the user.
        #  If set, they should be used to ignore/bypass any other values
        #  for calculating the starting point or centre point
        #  for drawing a shape
        self._abs_x = kwargs.get("_abs_x", None)
        self._abs_y = kwargs.get("_abs_y", None)
        self._abs_x1 = kwargs.get("_abs_x1", None)
        self._abs_y1 = kwargs.get("_abs_y1", None)
        self._abs_cx = kwargs.get("_abs_cx", None)
        self._abs_cy = kwargs.get("_abs_cy", None)
        self.use_abs = (
            True if self._abs_x is not None and self._abs_y is not None else False
        )
        self.use_abs_1 = (
            True if self._abs_x1 is not None and self._abs_y1 is not None else False
        )
        self.use_abs_c = (
            True if self._abs_cx is not None and self._abs_cy is not None else False
        )

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw an element on a given canvas."""
        self.set_abs_and_offset(cnv=cnv, off_x=off_x, off_y=off_y, ID=ID, **kwargs)
        # feedback(f'### draw baseshape: {self._abs_x=} {self._abs_y=} {self._abs_cx=} {self._abs_cy=}')

    def check_settings(self) -> tuple:
        """Validate that the user-supplied parameters for choices are correct"""
        correct = True
        issue = []
        if self.align:
            if str(self.align).lower() not in [
                "left",
                "right",
                "justify",
                "centre",
                "l",
                "r",
                "j",
                "c",
            ]:
                issue.append(f'"{self.align}" is an invalid align!')
                correct = False
        if self.edges:
            if not isinstance(self.edges, list):
                _edges = (
                    self.edges.split(",") if "," in self.edges else self.edges.split()
                )
            else:
                _edges = self.edges
            for edge in _edges:
                if str(edge).lower() not in [
                    "north",
                    "south",
                    "east",
                    "west",
                    "n",
                    "e",
                    "w",
                    "s",
                ]:
                    issue.append(
                        f'"{edge}" is an invalid choice in edges {self.edges}!'
                    )
                    correct = False
        if self.flip:
            if str(self.flip).lower() not in ["north", "south", "n", "s"]:
                issue.append(f'"{self.flip}" is an invalid flip!')
                correct = False
        if self.hand:
            if str(self.hand).lower() not in [
                "west",
                "east",
                "w",
                "e",
            ]:
                issue.append(f'"{self.hand}" is an invalid hand!')
                correct = False
        if self.lines:
            if str(self.lines).lower() not in [
                "all",
                "vertical",
                "horizontal",
                "vert",
                "horiz",
                "a",
                "v",
                "h",
            ]:
                issue.append(f'"{self.lines}" is an invalid lines setting!')
                correct = False
        if self.elevation:
            if str(self.elevation).lower() not in [
                "vertical",
                "horizontal",
                "v",
                "h",
            ]:
                issue.append(f'"{self.elevation}" is an invalid elevation!')
                correct = False
        if self.orientation:
            if str(self.orientation).lower() not in ["flat", "pointy", "f", "p"]:
                issue.append(f'"{self.orientation}" is an invalid orientation!')
                correct = False
        if self.perimeter:
            if str(self.perimeter).lower() not in [
                "circle",
                "rectangle",
                "hexagon",
                "c",
                "r",
                "h",
            ]:
                issue.append(f'"{self.perimeter}" is an invalid perimeter!')
                correct = False
        if self.position:
            if str(self.position).lower() not in [
                "top",
                "bottom",
                "center",
                "middle",
                "t",
                "b",
                "c",
                "m",
            ]:
                issue.append(f'"{self.position}" is an invalid position!')
                correct = False
        if self.petals_style:
            if str(self.petals_style).lower() not in [
                "triangle",
                "curve",
                "rectangle",
                "petal",
                "windmill",
                "t",
                "c",
                "r",
                "p",
                "w",
            ]:
                issue.append(f'"{self.petals_style}" is an invalid petals style!')
                correct = False
        # ---- line / arrow
        if self.rotation_point:
            if str(self.rotation_point).lower() not in [
                "start",
                "centre",
                "end",
                "s",
                "c",
                "e",
            ]:
                issue.append(f'"{self.rotation_point}" is an invalid rotation_point!')
                correct = False
        # ---- hexagons
        if self.coord_style:
            if str(self.coord_style).lower() not in ["linear", "diagonal", "l", "d"]:
                issue.append(f'"{self.coord_style}" is an invalid coord style!')
                correct = False
        # ---- arrowhead style
        if self.arrow_style:
            if str(self.arrow_style).lower() not in [
                "angle",
                "angled",
                "a",
                "notch",
                "notched",
                "n",
                "spear",
                "s",
                "triangle",  # default
                "t",
                # "circle",
                # "c",
            ]:
                issue.append(f'"{self.arrow_style}" is an invalid arrow_style!')
                correct = False
        # ---- line arrows
        # if self.arrow_tail_style:
        #     if str(self.arrow_tail_style).lower() not in [
        #         "line",
        #         "l",
        #         "line2",
        #         "l2",
        #         "line3",
        #         "l3",
        #         "feather",
        #         "f",
        #         "circle",
        #         "c",
        #     ]:
        #         issue.append(
        #             f'"{self.arrow_tail_style}" is an invalid arrow tail style!'
        #         )
        #         correct = False
        # ---- starfield
        if self.star_pattern:
            if str(self.star_pattern).lower() not in ["random", "cluster", "r", "c"]:
                issue.append(f'"{self.pattern}" is an invalid starfield pattern!')
                correct = False
        # ---- rectangle - notches
        if self.notch_style:
            if str(self.notch_style).lower() not in [
                "snip",
                "s",
                "fold",
                "o",
                "bite",
                "b",
                "flap",
                "l",
                "step",
                "t",
            ]:
                issue.append(f'"{self.notch_style}" is an invalid notch_style!')
                correct = False
        # ---- rectangle - peaks
        if self.peaks:
            if not isinstance(self.peaks, list):
                feedback(f"The peaks '{self.peaks}' is not a valid list!", True)
            for point in self.peaks:
                try:
                    _dir = point[0]
                    value = tools.as_float(point[1], " peaks value")
                    if _dir.lower() not in ["n", "e", "w", "s", "*"]:
                        feedback(
                            f'The peaks direction must be one of n, e, s, w (not "{_dir}")!',
                            True,
                        )
                    if _dir == "*":
                        self.peaks_dict["n"] = value
                        self.peaks_dict["e"] = value
                        self.peaks_dict["w"] = value
                        self.peaks_dict["s"] = value
                    else:
                        self.peaks_dict[_dir] = value
                except Exception:
                    feedback(f'The peaks setting "{point}" is not valid!', True)

        return correct, issue

    def to_alignment(self) -> Enum:
        """Convert local, English-friendly alignments to a PyMuPDF Enum."""
        match self.align:
            case "centre" | "center":
                self._alignment = TEXT_ALIGN_CENTER
            case "right":
                self._alignment = TEXT_ALIGN_RIGHT
            case "justify":
                # TEXT_ALIGN_JUSTIFY only achievable with “simple” (singlebyte) fonts
                # this includes the PDF Base 14 Fonts.
                self._alignment = TEXT_ALIGN_JUSTIFY
            case _:
                self._alignment = TEXT_ALIGN_LEFT
        return self._alignment

    def is_kwarg(self, value) -> bool:
        """Validate if value is in direct kwargs OR in Common _kwargs."""
        if value in self.kwargs:
            return True
        if "common" in self.kwargs:
            try:
                if value in self.kwargs.get("common")._kwargs:
                    return True
            except AttributeError:
                feedback(
                    "Unable to process Common properties"
                    " - has the Common command been set?",
                    True,
                )
        return False

    def load_image(
        self,
        pdf_page: muPage,
        image_location: str = None,
        origin: tuple = None,
        sliced: str = None,
        width_height: tuple = None,
        cache_directory: str = None,
        rotation: float = 0,
    ) -> tuple:
        """Load an image from file or website.

        Attempt to use local cache directory to retrieve an image
        for web-based assets, if possible.

        If image_location not found; try path in which script located.

        Args:
            image_location:
                full path or URL for image
            origin:
                x, y location of image on Page
            sliced:
                what fraction of the image to return; one of
                't', 'm', 'b', 'l', 'c', or 'r'
            width_height:
                the (width, height) of the output frame for the image;
                will be used along with x,y to set size and position;
                will be recalcuated if image is rotated
            cache_directory:
                where to store a local for copy for URL-sourced images
            rotation:
                angle of image rotation (in degrees)

        Returns:
            tuple:
                * Image
                * boolean (True if file is a directory)

        Notes:

        """

        def slice_image(
            img_path, slice_portion: str = None, width_height: tuple = (1, 1)
        ):
            """Slice off a portion of an image while maintaining its aspect ratio

            Args:
                img_path:
                    Pathlib file
                sliced:
                    what portion of the image to return
                width_height:
                    the (width, height) of the output frame for the image
            """
            # feedback(f"### {img_path=} {slice_portion=}")
            if not slice_portion:
                return None
            try:
                _slice = slice_portion.lower()
                if _slice[0] not in ["t", "m", "b", "l", "c", "r"]:
                    feedback(f'The sliced value "{slice_portion}" is not valid!', True)
                img = Image.open(img_path)
                iwidth = img.size[0]
                iheight = img.size[1]
                icentre = (int(iwidth / 2), int(iheight / 2))
                # calculate height of horizontal slice
                if _slice[0] in ["t", "m", "b"]:
                    slice_height = int(
                        min(iwidth * (width_height[1] / width_height[0]), iheight)
                    )
                # calculate width of vertical slice
                if _slice[0] in ["l", "c", "r"]:
                    slice_width = int(
                        min(iheight * (width_height[0] / width_height[1]), iwidth)
                    )
                # crop - needs a "box" which accepts a tuple with four values for
                #        the rectangle: left, upper, right, and lower
                match _slice[0]:
                    case "t":  # top (horizontal slice)
                        img2 = img.crop((0, 0, iwidth, slice_height))
                    case "m":  # middle (horizontal slice)
                        upper = icentre[1] - int(slice_height / 2)
                        img2 = img.crop((0, upper, iwidth, upper + slice_height))
                    case "b":  # bottom (horizontal slice)
                        img2 = img.crop((0, iheight - slice_height, iwidth, iheight))
                    case "l":  # left (vertical slice)
                        img2 = img.crop((0, 0, slice_width, iheight))
                    case "c":  # centre (vertical slice)
                        middle = icentre[0] - int(slice_width / 2)
                        img2 = img.crop((middle, 0, middle + slice_width, iheight))
                    case "r":  # right (vertical slice)
                        img2 = img.crop((iwidth - slice_width, 0, iwidth, iheight))
                    case _:
                        raise NotImplementedError(f"Cannot process {slice_portion}")
                # create new file with sliced image
                img2_filename = img_path.stem + "_" + _slice[0] + img_path.suffix
                sliced_filename = os.path.join(str(img_path.parent), img2_filename)
                img2.save(sliced_filename)
                return sliced_filename
            except Exception as err:
                feedback(
                    f'The sliced value "{slice_portion}" is not valid! ({err})', True
                )
            return None

        def get_image_from_svg(image_location: str = None):
            """Load SVG image and convert to PNG."""
            with open(image_location) as f:
                svg_code = f.read()
            png_bytes = cairosvg.svg2png(bytestring=svg_code.encode("utf-8"), dpi=300)
            image = Image.open(io.BytesIO(png_bytes))
            return image

        def save_image_from_url(url: str):
            """Download image from network and save locally if not present."""
            # feedback(f"### image save: {url=} ")
            loc = urlparse(url)
            filename = loc.path.split("/")[-1]
            image_local = os.path.join(cache_directory, filename)
            if not os.path.exists(image_local):
                image = requests.get(url)
                with open(image_local, "wb") as f:
                    f.write(image.content)
            return image_local

        def image_box_resize(bbox: muRect, img_path: str, rotation: float) -> muRect:
            """Recompute bounding Rect for a rotated image to maintain image size.

            Args
                bbox: pymupdf Rect; original bounding box for the image
                image_path: str; full path to image file
                rotation: angle; degrees of image rotation
            Returns
                adjusted Rect (new bounding box)
            """
            if not rotation or rotation == 0:
                return bbox
            # Compute Rect center point
            center = (bbox.tl + bbox.br) / 2
            # Define the desired rotation matrix
            matrx = Matrix(rotation)
            # Compute the tetragon (Quad) for the Rect rotated around its center `
            quad = bbox.morph(center, matrx)
            # Compute the rectangle hull of the quad for new boundary box
            new_bbox = quad.rect
            # Check image dimensions and ratios
            try:
                img = Image.open(img_path)
            except UnidentifiedImageError:
                try:
                    img = get_image_from_svg(img_path)
                except Exception:
                    feedback(f'Unable to open and process the image "{img_path}"', True)
            iwidth = img.size[0]
            iheight = img.size[1]
            iratio = iwidth / iheight
            bratio = new_bbox.width / new_bbox.height
            # Calculate new BBOX size based on image
            if iratio != bratio:
                if rotation > 270.0:
                    _rotation = rotation - 270.0
                elif rotation > 180.0:
                    _rotation = rotation - 180.0
                elif rotation > 90.0:
                    _rotation = rotation - 90.0
                else:
                    _rotation = rotation
                rotation_rad = math.radians(_rotation)
                img_height = bbox.width * iheight / iwidth
                new_box_height = bbox.width * math.sin(
                    rotation_rad
                ) + img_height * math.cos(rotation_rad)
                new_box_width = bbox.width * math.cos(
                    rotation_rad
                ) + img_height * math.sin(rotation_rad)
                new_bbox = muRect(
                    (center.x - new_box_width / 2.0, center.y - new_box_height / 2.0),
                    (center.x + new_box_width / 2.0, center.y + new_box_height / 2.0),
                )
            return new_bbox

        def image_render(image_location) -> object:
            """Load, first from local cache then network, and draw."""
            image_local = image_location
            if cache_directory:
                if tools.is_url_valid(image_location):
                    image_local = save_image_from_url(image_location)

            # ---- round image
            if self.rounding:
                image_in = Image.open(image_local)
                mask = Image.new("L", image_in.size, 0)
                draw = ImageDraw.Draw(mask)
                # draw.ellipse((0, 0, image_in.size[0], image_in.size[1]), fill=255)
                draw.rounded_rectangle(
                    ((0, 0), (image_in.size[0], image_in.size[1])),
                    self.rounding,
                    fill=255,
                )
                rounded_image = Image.composite(
                    image_in, Image.new("RGBA", image_in.size, (0, 0, 0, 0)), mask
                )

                membuf = io.BytesIO()
                rounded_image.save(membuf, format="png")
                png_data = membuf.getvalue()
                imgdoc = pymupdf.open(stream=png_data)  # in-memory image document
            else:
                imgdoc = pymupdf.open(image_local)  # open file image as document

            # ---- draw image
            pdfbytes = imgdoc.convert_to_pdf()  # make a 1-page PDF of it
            imgpdf = pymupdf.open("pdf", pdfbytes)
            rct = muRect(scaffold)
            pdf_page.show_pdf_page(
                rct,  # where to place the image (rect-like)
                imgpdf,  # source PDF
                pno=0,  # page number in *source* PDF (NOT current PDF)
                clip=None,  # only display this area (rect-like)
                rotate=self.rotation,  # rotate (float, any value)
                oc=0,  # control visibility via OCG / OCMD
                keep_proportion=True,  # keep aspect ratio
                overlay=True,  # put in foreground
            )
            if self.run_debug:
                pdf_page.draw_rect(rct, color=get_color(DEBUG_COLOR))
            return image_local

        img = False
        is_directory = False

        if not image_location:  # not the droids you're looking for... move along
            return img, None
        base_image_location = image_location

        if cache_directory:
            if tools.is_url_valid(image_location):
                image_local = save_image_from_url(image_location)
        # ---- check local files
        if not tools.is_url_valid(image_location):
            # relative paths
            if not os.path.isabs(image_location):
                filepath = tools.script_path()
                image_local = os.path.join(filepath, image_location)
            else:
                image_local = image_location
            # no filename
            is_directory = os.path.isdir(image_local)
            if is_directory:
                return img, True
            # check image exists
            if platform == "linux" or platform == "linux2":
                image_local = os.path.normpath(image_local.replace("\\", "/")).replace(
                    os.sep, "/"
                )
            if not os.path.exists(image_local):
                feedback(
                    f'Unable to find or open image "{image_location}" (also tried in "{image_local}"',
                    False,
                    True,
                )
                return img, True

        # ---- calculate BBOX for image
        width, height = width_height[0], width_height[1]
        scaffold = (origin[0], origin[1], origin[0] + width, origin[1] + height)
        if rotation is not None:
            # need a larger rect!
            new_origin = image_box_resize(muRect(scaffold), image_local, rotation)
            scaffold = (
                new_origin[0],
                new_origin[1],
                new_origin[2],
                new_origin[3],
            )

        # ---- render image
        try:
            if sliced:
                sliced_filename = slice_image(Path(image_local), sliced, width_height)
                if sliced_filename:
                    img = image_render(sliced_filename)
            else:
                img = image_render(image_local)
            return img, is_directory
        except IOError as err:
            feedback(
                f'Unable to find or open image "{base_image_location}"' f" ({err}).",
                False,
                True,
            )

        return img, is_directory

    def process_template(self, _dict):
        """Set values for properties based on those defined in a dictionary."""
        if not _dict:
            return
        if _dict.get("x"):
            self.x = _dict.get("x", 1)
        if _dict.get("y"):
            self.y = _dict.get("y", 1)
        if _dict.get("height"):
            self.height = _dict.get("height", 1)
        if _dict.get("width"):
            self.width = _dict.get("width", 1)
        if _dict.get("diameter"):
            self.diameter = _dict.get("diameter", 1)
        if _dict.get("radius"):
            self.radius = _dict.get("radius", self.diameter / 2.0 or 1)
        if _dict.get("rounding"):
            self.rounding = _dict.get("rounding", None)
        # if _dict.get('x'):
        #    self.x = _dict.get('x', 1)

    def get_center(self) -> tuple:
        """Attempt to get centre (x,y) tuple for a shape."""
        if self.cx and self.cy:
            return (self.cx, self.cy)
        if self.x and self.y and self.width and self.height:
            return (self.x + self.width / 2.0, self.y + self.height / 2.0)
        return ()

    def get_bounds(self) -> Bounds:
        """Attempt to get bounds of Rectangle (or any Shape with height and width)."""
        if self.x and self.y and self.width and self.height:
            bounds = Bounds(self.x, self.x + self.width, self.y, self.y + self.height)
            return bounds
        return None

    def get_shape_in_grid(self, the_shape):
        """Returns shape contained in GridShape class."""
        # if inspect.isclass(the_shape) and the_shape.__class__.__name__ == 'GridShape':
        if isinstance(the_shape, GridShape):
            return the_shape.shape
        else:
            return the_shape

    def get_font_height(self) -> float:
        # see Span Dictionary for ascender and descender of the font (float).
        # face = pdfmetrics.getFont(self.font_name).face
        # height = (face.ascent - face.descent) / 1000 * self.font_size
        # return height
        return float(self.font_size)

    def textify(self, index: int = None, text: str = "", default: bool = True) -> str:
        """Extract text from a list, or create string, based on index & type."""
        _text = text
        if not _text and default:
            _text = self.text
        log.debug("text %s %s %s %s", index, text, _text, type(_text))
        if _text is None:
            return
        if hasattr(_text, "lower"):
            return _text
        try:
            return _text[index]
        except TypeError:
            return _text

    def points_to_value(self, value: float, units_name=None) -> float:
        """Convert a point value to a units-based value."""
        try:
            match units_name:
                case "cm" | "centimetres":
                    return float(value) / unit.cm
                case "mm" | "millimetres":
                    return float(value) / unit.mm
                case "inch" | "in" | "inches":
                    return float(value) / unit.inch
                case "points" | "pts":
                    return float(value) / unit.pt
                case _:
                    return float(value) / self.units
        except Exception as err:
            log.exception(err)
            feedback(
                f'Unable to do unit conversion from "{value}" using {self.units}!', True
            )

    def values_to_points(self, items: list, units_name=None) -> list:
        """Convert a list of values to point units."""
        try:
            match units_name:
                case "cm" | "centimetres":
                    return [float(item) * unit.cm for item in items]
                case "mm" | "millimetres":
                    return [float(item) * unit.mm for item in items]
                case "inch" | "in" | "inches":
                    return [float(item) * unit.inch for item in items]
                case "points" | "pts":
                    return [float(item) * unit.pt for item in items]
                case None:
                    return [float(item) * self.units for item in items]
                case _:
                    feedback(f'Unable to convert units "{units_name}" to points!', True)
        except Exception as err:
            log.exception(err)
            feedback(f'Unable to convert value(s) "{items}" to points!', True)

    def text_properties(self, string=None, **kwargs) -> dict:
        """Set properties used by PyMuPDF to draw text."""
        keys = {}
        keys["fontsize"] = kwargs.get("font_size", self.font_size)
        keys["fontname"] = kwargs.get("font_name", self.font_name)
        font, keys["fontfile"], keys["fontname"] = tools.get_font_by_name(
            keys["fontname"]
        )

        _outlined = kwargs.get("outlined", self.outlined)
        if _outlined:
            keys["render_mode"] = 2  # default render_mode=0

        _color = kwargs.get("stroke", self.stroke)
        keys["color"] = tools.get_color(_color)

        if kwargs.get("fill") and _outlined:
            _fill = kwargs.get("fill", self.fill)
            keys["fill"] = tools.get_color(_fill)
        else:
            keys["fill"] = keys["color"]

        keys["align"] = self.to_alignment()

        _lineheight = kwargs.get("line_height", None)
        keys["lineheight"] = self.kw_float(_lineheight, "line_height")

        _border_width = kwargs.get("text_stroke_width", self.text_stroke_width)
        if _border_width is not None:
            keys["border_width"] = tools.as_float(_border_width, "border_width")

        _invisible = kwargs.get("invisible", self.invisible)
        if _invisible:
            keys["render_mode"] = 3

        _stroke_transparency = kwargs.get(
            "stroke_transparency", self.stroke_transparency
        )
        if _stroke_transparency is not None:
            _stroke_opacity = tools.as_float(
                _stroke_transparency, "stroke_transparency"
            )
            keys["stroke_opacity"] = tools.get_opacity(_stroke_opacity)

        _fill_transparency = kwargs.get("fill_transparency", self.fill_transparency)
        if _fill_transparency is not None:
            _fill_opacity = tools.as_float(_fill_transparency, "fill_transparency")
            keys["fill_opacity"] = tools.get_opacity(_fill_opacity)

        # potential other properties
        # keys['idx'] = 0
        # keys['miter_limit'] = 1
        # keys['encoding'] = pymupdf.TEXT_ENCODING_LATIN
        # keys['oc'] = 0
        # keys['overlay'] = True
        # keys['expandtabs'] = 8
        # keys['charwidths'] = None

        return keys

    def draw_multi_string(
        self, canvas, xm, ym, string, align=None, rotation=0, **kwargs
    ):
        """Low-level text drawing, split string (\n) if needed, with align and rotation.

        Args:
            * canvas (pymupdf Shape): set by calling function; which
              should access globals.canvas or BaseShape.canvas
            * xm (float) and ym (float): must be in native units (i.e. points)!
            * string (str): the text to draw/write
            * align (str): one of [centre|right|left|None] alignment of text
            * rotation (float): an angle in degrees; anti-clockwise from East

        Kwargs:
            * locale (dict): created from Locale namedtuple
            * font_size (float): height of characters
            * font_name (str): name pf font
            * stroke (str): color of text outline
            * fill (str): color of text fill
            * fill_transparency (float): percent transparent (100 is non-transparent)
            * stroke_transparency (float): percent transparent (100 is non-transparent)
            * outlined (bool): draw outline without fill
            * invisible (bool): do not draw text at all
            * stroke_width (float): thickness of text outline

        Notes:
            Drawing using HTML CSS-styling is handled in the Text shape
        """

        def move_string_start(text, point, font, fontsize, align):
            # compute length of written text under font and fontsize:
            tl = font.text_length(text, fontsize=fontsize)
            # insertion point ("origin"):
            if align == "centre":
                origin = muPoint(point.x - tl / 2.0, point.y)
            elif align == "right":
                origin = muPoint(point.x - tl, point.y)
            else:
                origin = point
            return origin

        # feedback(f"### {string=} {kwargs=} {rotation=}")
        if not string:
            return
        # ---- deprecated
        if kwargs.get("text_sequence", None):
            raise NotImplementedError("No text_sequence please!")
        # ---- process locale data (from Locale namedtuple) via jinja2
        _locale = kwargs.get("locale", None)
        if _locale:
            string = tools.eval_template(string, _locale)
        # ---- align and font
        align = align or self.align
        mvy = copy.copy(ym)
        # ---- text properties
        keys = self.text_properties(**kwargs)
        keys.pop("align")
        # TODO - recalculate xm, ym based on align and text width
        # keys["align"] = align or self.align
        font, _, _ = tools.get_font_by_name(keys["fontname"])
        # ---- draw
        point = muPoint(xm, ym)
        if self.align:
            point = move_string_start(string, point, font, keys["fontsize"], self.align)
        if rotation:
            dx = pymupdf.get_text_length(string, fontsize=keys["fontsize"]) / 2
            midpt = muPoint(point.x + dx, point.y)
            # self.dot = 0.05; self.draw_dot(canvas, midpt.x, midpt.y)
            morph = (midpt, Matrix(rotation))
        else:
            morph = None

        try:
            # insert_text(
            #     point, text, *, fontsize=11, fontname='helv', fontfile=None,
            #     set_simple=False, encoding=TEXT_ENCODING_LATIN, color=None,
            #     lineheight=None, fill=None, render_mode=0, miter_limit=1,
            #     border_width=1, rotate=0, morph=None, stroke_opacity=1,
            #     fill_opacity=1, oc=0)
            # print(f'### insert_text:: {point=} {string=} {morph=} \n{keys=}')
            canvas.insert_text(point, string, morph=morph, **keys)
        except Exception as err:
            if "need font file" in str(err):
                feedback(
                    f'The font "{self.font_name}" cannot be found -'
                    " please check spelling and/or location",
                    True,
                )
            else:
                feedback(f'Cannot write "{string}" (Error: {err})', True)

    def draw_string(self, canvas, xs, ys, string, align=None, rotation=0, **kwargs):
        """Draw a multi-string on the canvas."""
        self.draw_multi_string(
            canvas=canvas,
            x=xs,
            y=ys,
            string=string,
            align=align,
            rotation=rotation,
            **kwargs,
        )

    def draw_heading(
        self, canvas, ID, xh, yh, y_offset=0, align=None, rotation=0, **kwargs
    ):
        """Draw the heading for a shape (normally above the shape).

        Requires native units (i.e. points)!
        """
        ttext = self.textify(index=ID, text=self.heading, default=False)
        _rotation = rotation or self.heading_rotation
        if ttext:
            _ttext = str(ttext)
            y_off = y_offset or self.title_size / 2.0
            y = yh + self.unit(self.heading_my)
            x = xh + self.unit(self.heading_mx)
            kwargs["font_name"] = self.heading_face or self.font_name
            kwargs["stroke"] = self.heading_stroke
            kwargs["font_size"] = self.heading_size
            center_point = kwargs.get("rotation_point", None)
            if center_point and _rotation:
                point_to_rotate = muPoint(x, y - y_off)
                rpt = geoms.rotate_point_around_point(
                    point_to_rotate, center_point, _rotation
                )
                # self.dot = 0.05; self.draw_dot(canvas, rpt.x, rpt.y)
                self.draw_multi_string(
                    canvas,
                    rpt.x,
                    rpt.y,
                    _ttext,
                    align=align,
                    rotation=_rotation,
                    **kwargs,
                )
            else:
                # self.dot = 0.05; self.draw_dot(canvas, x, y - y_off)
                self.draw_multi_string(
                    canvas,
                    x,
                    y - y_off,
                    _ttext,
                    align=align,
                    rotation=_rotation,
                    **kwargs,
                )
            if isinstance(canvas, muShape):
                canvas.commit()

    def draw_label(
        self, canvas, ID, xl, yl, align=None, rotation=0, centred=True, **kwargs
    ):
        """Draw the label for a shape (usually at the centre).

        Requires native units (i.e. points)!
        """
        ttext = self.textify(index=ID, text=self.label, default=False)
        _rotation = rotation or self.label_rotation
        if ttext:
            _ttext = str(ttext)
            yl = yl + (self.label_size / 3.0) if centred else yl
            y = yl + self.unit(self.label_my)
            x = xl + self.unit(self.label_mx)
            kwargs["font_name"] = self.label_face or self.font_name
            kwargs["stroke"] = self.label_stroke
            kwargs["font_size"] = self.label_size
            center_point = kwargs.get("rotation_point", None)
            if center_point and _rotation:
                point_to_rotate = muPoint(x, y)
                rpt = geoms.rotate_point_around_point(
                    point_to_rotate, center_point, _rotation
                )
                # self.dot = 0.05; self.draw_dot(canvas, rpt.x, rpt.y)
                self.draw_multi_string(
                    canvas,
                    rpt.x,
                    rpt.y,
                    _ttext,
                    align=align,
                    rotation=_rotation,
                    **kwargs,
                )
            else:
                # self.dot = 0.05; self.draw_dot(canvas, x, y)
                self.draw_multi_string(
                    canvas, x, y, _ttext, align=align, rotation=_rotation, **kwargs
                )
            if isinstance(canvas, muShape):
                canvas.commit()

    def draw_title(
        self, canvas, ID, xt, yt, y_offset=0, align=None, rotation=0, **kwargs
    ):
        """Draw the title for a shape (normally below the shape).

        Requires native units (i.e. points)!
        """
        ttext = self.textify(index=ID, text=self.title, default=False)
        _rotation = rotation or self.title_rotation
        if ttext:
            _ttext = str(ttext)
            y_off = y_offset or self.title_size
            y = yt + self.unit(self.title_my)
            x = xt + self.unit(self.title_mx)
            kwargs["font_name"] = self.title_face or self.font_name
            kwargs["stroke"] = self.title_stroke
            kwargs["font_size"] = self.title_size
            center_point = kwargs.get("rotation_point", None)
            if center_point and _rotation:
                point_to_rotate = muPoint(x, y + y_off)
                rpt = geoms.rotate_point_around_point(
                    point_to_rotate, center_point, _rotation
                )
                # self.dot = 0.05; self.draw_dot(canvas, rpt.x, rpt.y)
                self.draw_multi_string(
                    canvas,
                    rpt.x,
                    rpt.y,
                    _ttext,
                    align=align,
                    rotation=_rotation,
                    **kwargs,
                )
            else:
                # self.dot = 0.05; self.draw_dot(canvas, x, y + y_off)
                self.draw_multi_string(
                    canvas,
                    x,
                    y + y_off,
                    _ttext,
                    align=align,
                    rotation=_rotation,
                    **kwargs,
                )
            if isinstance(canvas, muShape):
                canvas.commit()

    def draw_radii_label(
        self, canvas, ID, xl, yl, align=None, rotation=0, centred=True, **kwargs
    ):
        """Draw the label for a radius (usually at the centre).

        Requires native units (i.e. points)!
        """
        if not self.radii_label:
            return
        ttext = self.textify(index=ID, text=self.radii_label, default=False)
        _rotation = rotation or self.radii_labels_rotation
        if ttext:
            _ttext = str(ttext)
            yl = yl - (self.radii_labels_size / 3.0) if centred else yl
            y = yl + self.unit(self.radii_labels_my)
            x = xl + self.unit(self.radii_labels_mx)
            kwargs["font_name"] = self.radii_labels_face
            kwargs["stroke"] = self.radii_labels_stroke
            kwargs["font_size"] = self.radii_labels_size
            # print(f'*** draw_radii_label {rotation=}')
            self.draw_multi_string(
                canvas, x, y, _ttext, align=align, rotation=_rotation, **kwargs
            )
            if isinstance(canvas, muShape):
                canvas.commit()

    def draw_dot(self, canvas, x, y):
        """Draw a small dot on a shape (normally the centre)."""
        if self.dot:
            # print(f'*** draw_dot {x=} {y=}' )
            dot_size = self.unit(self.dot)
            kwargs = {}
            kwargs["fill"] = self.dot_stroke
            kwargs["stroke"] = self.dot_stroke
            canvas.draw_circle((x, y), dot_size)
            self.set_canvas_props(cnv=canvas, index=None, **kwargs)

    def draw_cross(self, canvas, xd, yd, **kwargs):
        """Draw a cross on a shape (normally the centre)."""
        if self.cross:
            # ---- properties
            kwargs = {}
            cross_size = self.unit(self.cross)
            rotation = kwargs.get("rotation", self.rotation)
            if rotation:
                kwargs["rotation"] = rotation
                kwargs["rotation_point"] = muPoint(xd, yd)
            kwargs["fill"] = self.cross_stroke
            kwargs["stroke"] = self.cross_stroke
            kwargs["stroke_width"] = self.cross_stroke_width
            # ---- horizontal line
            pt1 = geoms.Point(xd - cross_size / 2.0, yd)
            pt2 = geoms.Point(xd + cross_size / 2.0, yd)
            canvas.draw_line(pt1, pt2)
            # ---- vertical line
            pt1 = geoms.Point(xd, yd - cross_size / 2.0)
            pt2 = geoms.Point(xd, yd + cross_size / 2.0)
            canvas.draw_line(pt1, pt2)
            self.set_canvas_props(cnv=canvas, index=None, **kwargs)

    def draw_arrowhead(
        self, cnv, point_start: geoms.Point, point_end: geoms.Point, **kwargs
    ):
        """Draw arrowhead at the end of a straight line segment

        Args:
            point_start: start point of line
            point_end: end point of line
        """
        self.arrow_style = self.arrow_style or "triangle"  # default
        if self.arrow_position:
            tips = []
            steps = tools.sequence_split(
                self.arrow_position,
                unique=False,
                as_int=False,
                as_float=True,
                msg=" for arrow_position",
            )
            for step in steps:
                if step > 1:
                    feedback("The arrow_position value must be less than 1", True)
                the_tip = geoms.fraction_along_line(point_start, point_end, step)
                tips.append(the_tip)
        else:
            tips = [point_end]
        for the_tip in tips:
            head_width = (
                self.unit(self.arrow_width)
                if self.arrow_width
                else (self.stroke_width * 4 + self.stroke_width)
            )
            _head_height = math.sqrt(head_width**2 - (0.5 * head_width) ** 2)
            head_height = (
                self.unit(self.arrow_height) if self.arrow_height else _head_height
            )
            pt1 = geoms.Point(the_tip.x - head_width / 2.0, the_tip.y + head_height)
            pt2 = the_tip
            pt3 = geoms.Point(the_tip.x + head_width / 2.0, the_tip.y + head_height)
            vertexes = [pt1, pt2, pt3]
            kwargs["vertices"] = vertexes
            kwargs["stroke_width"] = 0.01
            # print(f'{self.arrow_stroke=} {self.arrow_fill=} {self.stroke=}')
            kwargs["fill"] = self.arrow_fill or self.stroke
            kwargs["stroke"] = self.arrow_stroke or self.stroke
            kwargs["fill"] = self.arrow_fill or self.stroke
            kwargs["closed"] = True
            deg, angle = geoms.angles_from_points(point_start, point_end)
            # print(f'{deg=} {angle=} ')
            if point_start.x != point_end.x:
                kwargs["rotation"] = 180 + deg
                kwargs["rotation_point"] = the_tip
            else:
                if point_end.y > point_start.y:
                    kwargs["rotation"] = 180
                    kwargs["rotation_point"] = the_tip
                else:
                    kwargs["rotation"] = 0
                    kwargs["rotation_point"] = None

            match str(self.arrow_style).lower():
                case "triangle" | "t":
                    pass
                case "spear" | "s":
                    pt4 = geoms.Point(the_tip.x, the_tip.y + 2 * head_height)
                    vertexes.append(pt4)
                case "angle" | "angled" | "a":
                    kwargs["stroke_width"] = self.stroke_width
                    kwargs["closed"] = False
                    kwargs["fill"] = None
                case "notch" | "notched" | "n":
                    pt4 = geoms.Point(the_tip.x, the_tip.y + 0.5 * head_height)
                    vertexes.append(pt4)
            # set props
            # print(f'{vertexes=}' {kwargs=}')
            self._debug(cnv, vertices=vertexes)  # needs: self.debug=True
            cnv.draw_polyline(vertexes)
            self.set_canvas_props(cnv=cnv, index=None, **kwargs)

    def make_path_vertices(self, cnv, vertices: list, v1: int, v2: int):
        """Draw line between two vertices"""
        cnv.draw_line(vertices[v1], vertices[v2])

    def draw_lines_between_sides(
        self,
        cnv,
        side: float,
        line_count: int,
        vertices: list,
        left_nodes: tuple,
        right_nodes: tuple,
        skip_ends: bool = True,
    ):
        """Draw lines between opposing sides of a shape

        Args:
            side: length of a side
            line_count: number of connections
            vertices: list of the Points making up the shape
            left_nodes: IDs of the two vertices on either end of one of the sides
            right_nodes: IDs of the two vertices on either end of the opposite side
            skip_ends: if True, do not draw the first or last connection

        Note:
            * Vertices normally go clockwise from bottom/lower left
            * Directions of vertex indices in left- and right-sides must be the same
        """
        delta = side / (line_count + 1)
        # feedback(f'### {side=} {line_count=} {delta=} {skip_ends=}')
        for number in range(0, line_count + 2):
            if skip_ends:
                if number == line_count + 1 or number == 0:
                    continue
            left_pt = geoms.point_on_line(
                vertices[left_nodes[0]], vertices[left_nodes[1]], delta * number
            )
            right_pt = geoms.point_on_line(
                vertices[right_nodes[0]], vertices[right_nodes[1]], delta * number
            )
            cnv.draw_line(left_pt, right_pt)

    def _debug(self, canvas, **kwargs):
        """Execute any debug statements."""
        if self.run_debug:
            # display vertex index number next to vertex
            if kwargs.get("vertices", []):
                kwargs["stroke"] = self.debug_color
                kwargs["fill"] = self.debug_color
                kwargs["font_name"] = self.font_name
                kwargs["font_size"] = 4
                for key, vert in enumerate(kwargs.get("vertices")):
                    x = self.points_to_value(vert.x)
                    y = self.points_to_value(vert.y)
                    self.draw_multi_string(
                        # canvas, vert.x, vert.y, f"{key}:{x:.2f},{y:.2f}", **kwargs
                        canvas,
                        vert.x,
                        vert.y,
                        f"{key}:{vert.x:.1f},{vert.y:.1f}",
                        **kwargs,
                    )
                    canvas.draw_circle((vert.x, vert.y), 1)
            # display labelled point (geoms.Point)
            if kwargs.get("point", []):
                point = kwargs.get("point")
                label = kwargs.get("label", "")
                kwargs["fill"] = kwargs.get("color", self.debug_color)
                kwargs["stroke"] = kwargs.get("color", self.debug_color)
                kwargs["stroke_width"] = 0.1
                kwargs["font_size"] = 4
                x = self.points_to_value(point.x)
                y = self.points_to_value(point.y)
                self.draw_multi_string(
                    canvas, point.x, point.y, f"{label}:{point.x:.1f},{point.y:.1f}"
                )
                canvas.draw_circle((point.x, point.y), 1)
            self.set_canvas_props(cnv=canvas, index=None, **kwargs)

    def handle_custom_values(self, the_element, ID):
        """Process custom values for a Shape's properties.

        Custom values should be stored in self.deck_data as a list of dicts:
        e.g. [{'SUIT': 'hearts', 'VALUE': 10}, {'SUIT': 'clubs', 'VALUE': 10}]
        which are used for a set of Cards, or similar placeholder items.

        Values can be accessed via a Jinja template using e.g. T("{{ SUIT }}")
        """

        def processed_value(value):

            if isinstance(value, (BaseShape, muShape, muPage)):
                return None

            elif isinstance(value, Template):
                if not self.deck_data:
                    feedback(
                        "Cannot use T() or S() command without Data already defined!",
                        False,
                    )
                    feedback(
                        "Check that Data command is used before Deck command.",
                        True,
                    )
                record = self.deck_data[ID]
                try:
                    custom_value = value.render(record)
                    # print('### Template', f'{ID=} {key=} {custom_value=}')
                    return custom_value
                except jinja2.exceptions.UndefinedError as err:
                    feedback(f"Unable to process data with this template ({err})", True)
                except Exception as err:
                    feedback(f"Unable to process data with this template ({err})", True)

            elif isinstance(value, TemplatingType):
                if not self.deck_data:
                    feedback(
                        "Cannot use T() or S() command without Data already defined!",
                        False,
                    )
                    feedback(
                        "Check that Data command is used before Deck command.",
                        True,
                    )
                record = self.deck_data[ID]
                try:
                    custom_value = value.template.render(record)
                    # print('### TT', f'{ID=} {key=} {custom_value=} {value.function=}')
                    if value.function:
                        try:
                            custom_value = value.function(custom_value)
                        except Exception as err:
                            feedback(
                                f"Unable to process data with function '{ value.function}' ({err})",
                                True,
                            )

                    return custom_value
                except jinja2.exceptions.UndefinedError as err:
                    feedback(f"Unable to process data with this template ({err})", True)
                except Exception as err:
                    feedback(f"Unable to process data with this template ({err})", True)

            elif isinstance(value, LookupType):
                record = self.deck_data[ID]
                lookup_value = record[value.column]
                custom_value = value.lookups.get(lookup_value, None)
                return custom_value
                # print('### LookupType', f'{ID=} {key=} {custom_value=}', '=>', getattr(new_element, key))
            elif isinstance(value, PosixPath):
                # print(f'### HCV {ID=} {key=} {value=}')
                return None
            else:
                raise NotImplementedError(f"Cannot handle value of type: {type(value)}")

            return None

        new_element = None
        # print('### ShapeType ::', type(the_element))
        if isinstance(the_element, BaseShape):
            new_element = copy.copy(the_element)
            keys = vars(the_element).keys()
            for key in keys:
                value = getattr(the_element, key)
                if value is None or isinstance(
                    value, (str, int, float, list, tuple, range)
                ):
                    continue
                elif isinstance(value, dict):
                    updated = False
                    for dkey, val in value.items():
                        if val is None or isinstance(
                            val, (str, int, float, list, tuple, range)
                        ):
                            continue
                        custom_value = processed_value(val)
                        if custom_value is not None:
                            value[dkey] = custom_value
                            updated = True
                    if updated:
                        setattr(new_element, key, value)
                else:
                    custom_value = processed_value(value)
                    if custom_value is not None:
                        setattr(new_element, key, custom_value)
            return new_element
        return the_element  # no changes needed or made

    def draw_border(self, cnv, border: tuple, ID: int = None):
        """Draw a border line based its settings."""
        # feedback(f'### border {self.__class__.__name__} {border=} {ID=}')
        if not isinstance(border, tuple):
            feedback(
                'The "borders" property must contain a list of one or more sets'
                f' - not "{border}"',
                True,
            )
        # ---- assign tuple values
        bdirections, bwidth, bcolor, bstyle, dotted, dashed = (
            None,
            None,
            "black",
            None,
            False,
            None,
        )
        if len(border) >= 4:
            bstyle = border[3]
        if len(border) >= 3:
            bcolor = border[2]
        if len(border) >= 2:
            bdirections = border[0]
            bwidth = border[1]
        if len(border) <= 1:
            feedback(
                'A "borders" set must contain: direction, width, color'
                f' and an optional style - not "{border}"',
                True,
            )
        # ---- line styles
        bwidth = tools.as_float(bwidth, "")
        if bstyle is True:
            dotted = True
        else:
            dashed = bstyle
        # ---- multi-directions
        shape_name = self.__class__.__name__.replace("Shape", "")
        _bdirections = tools.validated_directions(
            bdirections, tools.DirectionGroup.COMPASS, f"{shape_name.lower()} border"
        )
        for bdirection in _bdirections:
            if not bdirection:
                continue
            # ---- get line start & end
            match self.__class__.__name__:
                # ---- * Rect, Sq, Trap
                case "RectangleShape" | "SquareShape" | "TrapezoidShape":
                    match bdirection:  # vertices anti-clockwise from top-left
                        case "w":
                            x, y = self.vertexes[0][0], self.vertexes[0][1]
                            x_1, y_1 = self.vertexes[1][0], self.vertexes[1][1]
                        case "s":
                            x, y = self.vertexes[1][0], self.vertexes[1][1]
                            x_1, y_1 = self.vertexes[2][0], self.vertexes[2][1]
                        case "e":
                            x, y = self.vertexes[2][0], self.vertexes[2][1]
                            x_1, y_1 = self.vertexes[3][0], self.vertexes[3][1]
                        case "n":
                            x, y = self.vertexes[3][0], self.vertexes[3][1]
                            x_1, y_1 = self.vertexes[0][0], self.vertexes[0][1]
                        case _:
                            feedback(
                                f"Invalid direction ({bdirection}) for {shape_name} border",
                                True,
                            )
                # ---- * Rhombus
                case "RhombusShape":
                    match bdirection:
                        case "se":
                            x, y = self.vertexes[1][0], self.vertexes[1][1]
                            x_1, y_1 = self.vertexes[2][0], self.vertexes[2][1]
                        case "ne":
                            x, y = self.vertexes[2][0], self.vertexes[2][1]
                            x_1, y_1 = self.vertexes[3][0], self.vertexes[3][1]
                        case "nw":
                            x, y = self.vertexes[3][0], self.vertexes[3][1]
                            x_1, y_1 = self.vertexes[0][0], self.vertexes[0][1]
                        case "sw":
                            x, y = self.vertexes[0][0], self.vertexes[0][1]
                            x_1, y_1 = self.vertexes[1][0], self.vertexes[1][1]
                        case _:
                            feedback(
                                f"Invalid direction ({bdirection}) for {shape_name} border",
                                True,
                            )
                # ---- * Hex
                case "HexShape":
                    if self.orientation == "pointy":
                        match bdirection:
                            case "se":
                                x, y = self.vertexes[2][0], self.vertexes[2][1]
                                x_1, y_1 = self.vertexes[3][0], self.vertexes[3][1]
                            case "e":
                                x, y = self.vertexes[3][0], self.vertexes[3][1]
                                x_1, y_1 = self.vertexes[4][0], self.vertexes[4][1]
                            case "ne":
                                x, y = self.vertexes[4][0], self.vertexes[4][1]
                                x_1, y_1 = self.vertexes[5][0], self.vertexes[5][1]
                            case "nw":
                                x, y = self.vertexes[5][0], self.vertexes[5][1]
                                x_1, y_1 = self.vertexes[0][0], self.vertexes[0][1]
                            case "w":
                                x, y = self.vertexes[0][0], self.vertexes[0][1]
                                x_1, y_1 = self.vertexes[1][0], self.vertexes[1][1]
                            case "sw":
                                x, y = self.vertexes[1][0], self.vertexes[1][1]
                                x_1, y_1 = self.vertexes[2][0], self.vertexes[2][1]
                            case _:
                                feedback(
                                    f"Invalid direction ({bdirection}) for pointy {shape_name} border",
                                    True,
                                )
                    elif self.orientation == "flat":
                        match bdirection:
                            case "s":
                                x, y = self.vertexes[1][0], self.vertexes[1][1]
                                x_1, y_1 = self.vertexes[2][0], self.vertexes[2][1]
                            case "se":
                                x, y = self.vertexes[2][0], self.vertexes[2][1]
                                x_1, y_1 = self.vertexes[3][0], self.vertexes[3][1]
                            case "ne":
                                x, y = self.vertexes[3][0], self.vertexes[3][1]
                                x_1, y_1 = self.vertexes[4][0], self.vertexes[4][1]
                            case "n":
                                x, y = self.vertexes[4][0], self.vertexes[4][1]
                                x_1, y_1 = self.vertexes[5][0], self.vertexes[5][1]
                            case "nw":
                                x, y = self.vertexes[5][0], self.vertexes[5][1]
                                x_1, y_1 = self.vertexes[0][0], self.vertexes[0][1]
                            case "sw":
                                x, y = self.vertexes[0][0], self.vertexes[0][1]
                                x_1, y_1 = self.vertexes[1][0], self.vertexes[1][1]
                            case _:
                                feedback(
                                    f"Invalid direction ({bdirection}) for flat {shape_name} border",
                                    True,
                                )
                    else:
                        raise ValueError(
                            'Invalid orientation "{self.orientation}" for border'
                        )

                case _:
                    match bdirection:
                        case _:
                            feedback(f"Cannot draw borders for a {shape_name}")

            # ---- draw line
            cnv.draw_line((x, y), (x_1, y_1))
            self.set_canvas_props(
                index=ID,
                stroke=bcolor,
                stroke_width=bwidth,
                dotted=dotted,
                dashed=dashed,
            )

    def can_draw_centred_shape(self, centre_shape) -> bool:
        """Test if a given Shape can be drawn at centre of another."""
        cshape_name = centre_shape.__class__.__name__
        if cshape_name in GRID_SHAPES_WITH_CENTRE:
            return True
        else:
            _name = cshape_name.replace("Shape", "")
            feedback(f"Cannot draw a centered {_name}!")
        return False


class GroupBase(list):
    """Class for group base."""

    def __init__(self, *args, **kwargs):
        list.__init__(self, *args)
        self.kwargs = kwargs
