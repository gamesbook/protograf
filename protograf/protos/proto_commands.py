# -*- coding: utf-8 -*-
"""
Primary interface for protograf (imported at top-level)

Note:
    Some imports here are for sake of reuse by the top-level import
"""

# lib
import argparse
from collections import namedtuple
from contextlib import suppress
from copy import copy
from datetime import datetime
import itertools
import logging
import math
import os
from pathlib import Path
import random
import sys
import types
from typing import Union, Any

# third party
import jinja2
from PIL import Image as PIL_Image
import pymupdf
from pymupdf import Rect as muRect, Archive

# local
from .bgg import BGGGame, BGGGameList
from .base import BaseCanvas, GroupBase, WIDTH
from .dice import Dice, DiceD4, DiceD6, DiceD8, DiceD10, DiceD12, DiceD20, DiceD100
from .shapes import (
    BaseShape,
    ArcShape,
    ArrowShape,
    BezierShape,
    ChordShape,
    CommonShape,
    CrossShape,
    DefaultShape,
    DotShape,
    EllipseShape,
    FooterShape,
    ImageShape,
    LineShape,
    QRCodeShape,
    PodShape,
    PolylineShape,
    RectangleShape,
    RhombusShape,
    SectorShape,
    ShapeShape,
    SquareShape,
    StadiumShape,
    StarShape,
    StarLineShape,
    TextShape,
    TrapezoidShape,
    TriangleShape,
    BandShape,
)

from .layouts import (
    GridShape,
    DotGridShape,
    HexHexShape,
    DiamondLocations,  # used in user scripts
    RectangularLocations,  # used in user scripts
    TriangularLocations,  # used in user scripts
    VirtualLocations,
    RepeatShape,
    SequenceShape,
    TableShape,
)
from .globals import unit  # used in scripts
from .groups import Switch, Lookup  # used in scripts
from ._version import __version__

from protograf.utils import colrs, geoms, loadr, tools, support
from protograf.utils.constants import (
    DEFAULT_FONT,
    RGB_DEBUG_COLOR,
    RGB_BLACK,
    RGB_WHITE,
    CMYK_DEBUG_COLOR,
    CMYK_BLACK,
    CMYK_WHITE,
    DEFAULT_CARD_WIDTH,  # cm
    DEFAULT_CARD_HEIGHT,  # cm
    DEFAULT_CARD_COUNT,
    DEFAULT_CARD_RADIUS,  # cm
    DEFAULT_COUNTER_SIZE,  # cm
    DEFAULT_COUNTER_RADIUS,  # cm
    DEFAULT_DPI,
    DEFAULT_MARGIN_SIZE,  # cm
    GRID_SHAPES_WITH_CENTRE,
    GRID_SHAPES_NO_CENTRE,
    SHAPES_FOR_TRACK,
    YES,  # used in scripts
    NO,  # used in scripts
)
from protograf.utils.docstrings import (
    docstring_area,
    docstring_base,
    docstring_card,
    docstring_center,
    docstring_loc,
    docstring_onimo,
)
from protograf.utils.colrs import lighten, darken  # used in scripts
from protograf.utils.fonts import FontInterface
from protograf.utils.geoms import equilateral_height  # used in scripts
from protograf.utils.messaging import feedback
from protograf.utils.support import (  # used in scripts
    steps,
    uni,
    uc,
    CACHE_DIRECTORY,
)
from protograf.utils.structures import (
    BBox,
    CardBleed,
    CardFrame,
    DatasetType,
    DeckPrintState,
    DirectionGroup,
    DocumentPage,
    ExportFormat,
    HEX_FLAT_EDGE_TRAVEL,
    HexOrientation,
    LookupType,
    Locale,
    PageMargins,
    Point,
    Place,
    Ray,
    ShapeGeometry,
    TemplatingType,
)
from protograf.utils.tools import (  # used in scripts
    base_fonts,
    _lower,
    split,
    uniques,
)

from protograf import globals

log = logging.getLogger(__name__)
globals_set = False

GRAYS = ("0,0,0,25.5", "#BEBEBE")


def validate_globals():
    """Check that Create has been called to set initialise globals"""
    global globals_set
    if not globals_set:
        feedback("Please ensure Create() command is called first!", True)


# ---- page-related ====


def page_setup():
    """Set the page color and (optionally) show a dotted margin line and grid."""
    # ---- paper color
    _fill = (
        globals.page.fill
        if isinstance(globals.page.fill, tuple)
        else colrs.get_color(globals.page.fill)
    )
    if _fill != colrs.get_color(globals.white):
        globals.doc_page.draw_rect(
            (0, 0, globals.page.size[0], globals.page.size[1]), fill=_fill, color=None
        )
    # ---- debug margins
    if globals.margins.debug:
        # print(f'$$$ {globals.margins.left=} {globals.margins.right=}')
        stroke = colrs.get_color(globals.debug_color)
        globals.doc_page.draw_rect(
            (
                globals.margins.left * globals.units,
                globals.margins.top * globals.units,
                globals.page.size[0] - (globals.margins.right * globals.units),
                globals.page.size[1] - (globals.margins.bottom * globals.units),
            ),
            color=stroke,
            dashes="[1 2] 0",
        )
    # ---- page grid
    if globals.page.grid:
        stroke = colrs.get_color(globals.debug_color)
        grid_size = globals.page.grid * globals.units
        cols = int(globals.page.size[0] // grid_size)
        rows = int(globals.page.size[1] // grid_size)
        for col in range(1, cols + 1):
            globals.doc_page.draw_line(
                (col * grid_size, 0),
                (col * grid_size, globals.page.size[1]),
                color=stroke,
                width=0.1,
            )
        for row in range(1, rows + 1):
            globals.doc_page.draw_line(
                (0, row * grid_size),
                (globals.page.size[0], row * grid_size),
                color=stroke,
                width=0.1,
            )


def Create(**kwargs):
    """Initialisation of globals, page, margins, units and canvas.

    Kwargs:

    - paper (str): a paper size from either of the ISO series - A0 down to A8;
      or B6 down to B0 - or a USA type - letter, legal or elevenSeventeen; to
      change the page orientation to **landscape** append ``-l`` to the name.
    - paper_width (float): set specific paper width using the defined *units*
    - paper_height (float): set specific paper height using the defined *units*
      For example, ``"A3-l"`` is a landscape A3 paper size; default is ``A4``
    - color_model (str): either ``RBG`` (default) or ``CMYK``
    - filename (str): name of the output PDF file; by default this is the prefix
      name of the script, with a ``.pdf`` extension
    - fill (str): the page color; default is ``white`` (CMYK equivalent)
    - units (str): can be ``cm`` (centimetres), ``in`` (inches), ``mm``
      (millimetres), or ``points``; default is ``cm``
    - margin (float): set the value for *all* margins using the defined *units*;
      default is ``1`` centimetre.
    - margin_top (float): set the top margin using the defined *units*
    - margin_bottom (float): set the bottom margin using the defined *units*
    - margin_left (float): set the left margin using the defined *units*
    - margin_right (float): set the the right margin using the defined *units*
    - margin_debug (bool): if True, show the margin as a dotted blue line
    - page_grid (float): if a valid float, draw a squared grid covering the paper
      of square size equal to the value
    - cached_fonts (bool): if True, will force reload of Font cache
    - globals_reset (bool): if True, will ignore warning for setting properties

    Notes:

    - Kwargs to override the default values of any of the various properties
      used for drawing Shapes can be set here as well, for example:
      ``font_size=18`` or ``stroke="red"``.
    - Will use argparse to process command-line keyword args
    - Allows shortcut creation of cards
    """
    global globals_set
    # ---- set and confirm globals
    globals.initialize()
    if globals_set:
        if not kwargs.get("globals_reset", False):
            feedback("Another document is already open or initialised", True)
    globals_set = True
    # ---- units
    _units = kwargs.get("units", "cm")
    globals.units = support.to_units(_units)
    # ---- margins
    the_margin = kwargs.get("margin", DEFAULT_MARGIN_SIZE / globals.units)
    globals.margins = PageMargins(
        margin=the_margin,
        left=kwargs.get("margin_left", the_margin),
        top=kwargs.get("margin_top", the_margin),
        bottom=kwargs.get("margin_bottom", the_margin),
        right=kwargs.get("margin_right", the_margin),
        debug=kwargs.get("margin_debug", False),
        units=globals.units,
        units_type=_units,
    )
    # ---- cards
    _cards = kwargs.get("cards", 0)
    # landscape = kwargs.get("landscape", False)  # deprecated
    kwargs = margins(**kwargs)
    defaults = kwargs.get("defaults", None)
    # ---- color_model, paper, page, page sizes, page color
    globals.color_model = kwargs.get("color_model", "RGB")
    if globals.color_model not in ["RGB", "CMYK"]:
        feedback('The color_model must be set to "RGB" or "CMYK"', True)
    globals.black = CMYK_BLACK if globals.color_model == "CMYK" else RGB_BLACK
    globals.white = CMYK_WHITE if globals.color_model == "CMYK" else RGB_WHITE
    globals.debug_color = (
        CMYK_DEBUG_COLOR if globals.color_model == "CMYK" else RGB_DEBUG_COLOR
    )
    globals.paper = kwargs.get("paper", globals.paper)
    # user overrides
    _page = pymupdf.paper_size(globals.paper)  # (width, height) in points
    if kwargs.get("paper_width") or kwargs.get("paper_height"):
        _page_width = tools.as_float(kwargs.get("paper_width", 0), "paper_width")
        _page_height = tools.as_float(kwargs.get("paper_height", 0), "paper_height")
        _page_width_pt = (
            _page_width * globals.units if _page_width > 0 else globals.paper[0]
        )
        _page_height_pt = (
            _page_height * globals.units if _page_height > 0 else globals.paper[1]
        )
        _page = (_page_width_pt, _page_height_pt)
    globals.page = DocumentPage(
        size=(_page[0], _page[1]),  # page.rect is visible area of page
        width=_page[0] / globals.units,  # width in user units
        height=_page[1] / globals.units,  # height in user units
        fill=colrs.get_color(kwargs.get("fill", globals.white)),
        grid=tools.as_float(kwargs.get("page_grid", 0), "page_grid"),
        current=0,
    )
    # ---- fonts
    base_fonts()
    globals.font_size = kwargs.get("font_size", 12)
    # ---- command-line arguments
    parser = argparse.ArgumentParser(exit_on_error=False)
    parser.add_argument(
        "-b", "--bggapi", help="Specify token for access to BGG API", default=""
    )
    parser.add_argument(
        "-d", "--directory", help="Specify output directory", default=""
    )
    # use: --fonts to force Fonts recreation during Create()
    parser.add_argument(
        "-f",
        "--fonts",
        help="Force reloading of all available fonts at start (default is False)",
        default=False,
        action=argparse.BooleanOptionalAction,
    )
    # use: --no-warning to ignore WARNING:: messages
    parser.add_argument(
        "-w",
        "--warning",
        help="Do NOT show any WARNING:: messages (default is False)",
        default=False,
        action=argparse.BooleanOptionalAction,
    )
    # use: --no-png to skip PNG output during Save()
    parser.add_argument(
        "-p",
        "--png",
        help="Whether to create PNG during Save (default is True)",
        default=True,
        action=argparse.BooleanOptionalAction,
    )
    parser.add_argument(
        "-g", "--pages", help="Specify which pages to process", default=""
    )
    parser.add_argument(
        "-t",
        "--trace",
        help="Print a program trace for an error (default is False)",
        default=False,
        action=argparse.BooleanOptionalAction,
    )
    # ---- filename and fallback
    _filename = kwargs.get("filename", "")
    if not _filename:
        basename = "test"
        # log.debug('basename: "%s" sys.argv[0]: "%s"', basename, sys.argv[0])
        if sys.argv[0]:
            basename = os.path.basename(sys.argv[0]).split(".")[0]
        else:
            if _cards:
                basename = "cards"
        _filename = f"{basename}.pdf"
    globals.filename = os.path.join(os.getcwd(), _filename)
    # ---- parser args
    try:
        globals.pargs = parser.parse_args()
        # NB - pages does not work - see notes in PageBreak()
        if globals.pargs.pages:
            feedback("--pages is not yet an implemented feature - sorry!")
        # ---- validate directory & set filename
        if globals.pargs.directory and not os.path.exists(globals.pargs.directory):
            feedback(
                f'Unable to find directory "{globals.pargs.directory}" for output.',
                True,
            )
        globals.filename = os.path.join(globals.pargs.directory, _filename)
    except SystemExit:
        print("Ignoring ArgumentParser exit!")
    except Exception as err:
        globals.pargs = None
    # ---- pymupdf doc, page, shape/canvas
    globals.document = pymupdf.open()  # pymupdf.Document
    globals.doc_page = globals.document.new_page(
        width=globals.page.size[0], height=globals.page.size[1]
    )  # pymupdf Page
    globals.canvas = globals.doc_page.new_shape()  # pymupdf Shape
    # ---- BaseCanvas (base.py)
    globals.base = BaseCanvas(
        globals.document,
        paper=globals.paper,
        color_model=globals.color_model,
        defaults=defaults,
        kwargs=kwargs,
    )
    page_setup()
    # ---- cards
    if _cards:
        Deck(canvas=globals.canvas, sequence=range(1, _cards + 1), **kwargs)  # deck var
    # ---- pickle font info for pymupdf
    globals.archive = Archive()
    globals.css = ""
    cached_fonts = tools.as_bool(kwargs.get("cached_fonts", True))
    if not cached_fonts or (globals.pargs and globals.pargs.fonts):
        cache_directory = Path(Path.home() / CACHE_DIRECTORY)
        fi = FontInterface(cache_directory=cache_directory)
        fi.load_font_families(cached=False)


def create(**kwargs):
    Create(**kwargs)


def Load(**kwargs):
    """Set globals, page, margins, units and canvas from existing PDF

    Kwargs:

    - filename (str): name of the input PDF file
    - units (str): can be ``cm`` (centimetres), ``in`` (inches), ``mm``
      (millimetres), or ``points``; default is ``cm``
    - margin (float): set the value for *all* margins using the defined *units*;
      default is ``1`` centimetre.
    - margin_top (float): set the top margin using the defined *units*
    - margin_bottom (float): set the bottom margin using the defined *units*
    - margin_left (float): set the left margin using the defined *units*
    - margin_right (float): set the the right margin using the defined *units*
    - margin_debug (bool): if True, show the margin as a dotted blue line
    - cached_fonts (bool): if True, will force reload of Font cache

    Notes:

    - Kwargs to override the default values of any of the various properties
      used for drawing Shapes can be set here as well, for example:
      ``font_size=18`` or ``stroke="red"``.
    - Will use argparse to process command-line keyword args
    - Allows shortcut creation of cards
    """
    global globals_set
    # ---- set and confirm globals
    globals.initialize()
    if globals_set:
        feedback("Another document is already open or initialised", True)
    globals_set = True
    # ---- units
    _units = kwargs.get("units", globals.units)
    globals.units = support.to_units(_units)
    # ---- margins
    the_margin = kwargs.get("margin", DEFAULT_MARGIN_SIZE / globals.units)
    globals.margins = PageMargins(
        margin=the_margin,
        left=kwargs.get("margin_left", the_margin),
        top=kwargs.get("margin_top", the_margin),
        bottom=kwargs.get("margin_bottom", the_margin),
        right=kwargs.get("margin_right", the_margin),
        debug=kwargs.get("margin_debug", False),
        units=globals.units,
        units_type=globals.units_type,
    )
    # ---- defaults
    defaults = kwargs.get("defaults", None)
    # ---- color_model, paper, page, page sizes
    globals.color_model = kwargs.get("color_model", "RGB")
    if globals.color_model not in ["RGB", "CMYK"]:
        feedback('The color_model must be set to "RGB" or "CMYK"', True)
    globals.black = CMYK_BLACK if globals.color_model == "CMYK" else RGB_BLACK
    globals.white = CMYK_WHITE if globals.color_model == "CMYK" else RGB_WHITE
    globals.paper = kwargs.get("paper", globals.paper)
    globals.page_size = pymupdf.paper_size(globals.paper)  # (width, height) in points
    # ---- fonts
    base_fonts()
    globals.font_size = kwargs.get("font_size", 12)
    # ---- command-line arguments
    parser = argparse.ArgumentParser(exit_on_error=False)
    parser.add_argument(
        "-d", "--directory", help="Specify output directory", default=""
    )
    # use: --no-png to skip PNG output during Save()
    parser.add_argument(
        "--png",
        help="Whether to create PNG during Save (default is True)",
        default=True,
        action=argparse.BooleanOptionalAction,
    )
    # use: --fonts to force Fonts recreation during Create()
    parser.add_argument(
        "-f",
        "--fonts",
        help="Force reloading of all available fonts at start (default is False)",
        default=False,
        action=argparse.BooleanOptionalAction,
    )
    # use: --no-warning to ignore WARNING:: messages
    parser.add_argument(
        "-nw",
        "--nowarning",
        help="Do NOT show any WARNING:: messages (default is False)",
        default=False,
        action=argparse.BooleanOptionalAction,
    )
    parser.add_argument(
        "-p", "--pages", help="Specify which pages to process", default=""
    )
    parser.add_argument(
        "-t",
        "--trace",
        help="Print a program trace for an error (default is False)",
        default=False,
        action=argparse.BooleanOptionalAction,
    )
    # ---- filename and fallback
    _filename = kwargs.get("filename", "")
    if not _filename:
        basename = "test"
        # log.debug('basename: "%s" sys.argv[0]: "%s"', basename, sys.argv[0])
        if sys.argv[0]:
            basename = os.path.basename(sys.argv[0]).split(".")[0]
        _filename = f"{basename}.pdf"
    globals.filename = os.path.join(os.getcwd(), _filename)
    try:
        globals.pargs = parser.parse_args()
        # NB - pages does not work - see notes in PageBreak()
        if globals.pargs.pages:
            feedback("--pages is not yet an implemented feature - sorry!")
        # ---- validate directory & set filename
        if globals.pargs.directory and not os.path.exists(globals.pargs.directory):
            feedback(
                f'Unable to find directory "{globals.pargs.directory}" for output.',
                True,
            )
        globals.filename = os.path.join(globals.pargs.directory, _filename)
    except SystemExit:
        print("Ignoring ArgumentParser exit!")
    except Exception as err:
        globals.pargs = None
    # ---- Open pymupdf doc, page, shape/canvas
    if not os.path.exists(globals.filename):
        script_path = os.path.abspath(__file__)
        script_directory = os.path.dirname(script_path)
        globals.filename = os.path.join(script_directory, globals.filename)
    try:
        globals.document = pymupdf.open(globals.filename)  # existing Document
    except Exception as err:
        feedback(f"Unable to load {globals.filename} ({err})", True)
        # ---- Extract and record doc info
        page = globals.document[0]
        globals.page = DocumentPage(
            size=(page.rect.width, page.rect.height),  # page.rect is visible page area
            width=page.rect.width / globals.units,
            height=page.rect.height / globals.units,
            fill=colrs.get_color(kwargs.get("fill", globals.white)),
            grid=tools.as_float(kwargs.get("page_grid", 0), "page_grid"),
            current=0,
        )
    globals.doc_page = globals.document.new_page(
        width=globals.page.size[0], height=globals.page.size[1]
    )  # pymupdf Page
    # ---- BaseCanvas (base.py)
    globals.canvas = globals.doc_page.new_shape()  # pymupdf Shape
    globals.base = BaseCanvas(
        globals.document, paper=globals.paper, defaults=defaults, kwargs=kwargs
    )
    page_setup()
    # ---- pickle font info for pymupdf
    globals.archive = Archive()
    globals.css = ""
    cached_fonts = tools.as_bool(kwargs.get("cached_fonts", True))
    if not cached_fonts or globals.pargs.fonts:
        cache_directory = Path(Path.home() / CACHE_DIRECTORY)
        fi = FontInterface(cache_directory=cache_directory)
        fi.load_font_families(cached=False)


def load(**kwargs):
    Load(**kwargs)


def Footer(**kwargs):
    validate_globals()

    kwargs["paper"] = globals.paper
    if not kwargs.get("font_size"):
        kwargs["font_size"] = globals.font_size
    globals.footer_draw = kwargs.get("draw", False)
    globals.footer = FooterShape(_object=None, canvas=globals.canvas, **kwargs)
    # footer.draw() - this is called via PageBreak()


def Header(**kwargs):
    validate_globals()
    pass


def PageBreak(**kwargs):
    """Start a new page in the output PDF.

    Kwargs:

    - footer (bool): should a Footer object be drawn before starting next page

    """
    validate_globals()

    globals.canvas.commit()  # add all drawings (to current pymupdf Shape/"canvas")
    globals.page_count += 1
    globals.doc_page = globals.document.new_page(
        width=globals.page.size[0], height=globals.page.size[1]
    )  # pymupdf Page
    globals.canvas = globals.doc_page.new_shape()  # pymupdf Shape/"canvas" for new Page
    page_setup()

    kwargs = margins(**kwargs)
    if kwargs.get("footer", globals.footer_draw):
        if globals.footer is None:
            kwargs["paper"] = globals.paper
            kwargs["font_size"] = globals.font_size
            globals.footer = FooterShape(_object=None, canvas=globals.canvas, **kwargs)
        globals.footer.draw(
            cnv=globals.canvas, ID=globals.page_count, text=None, **kwargs
        )


def page_break():
    PageBreak()


def Extract(pages: object, **kwargs):
    """Extract one or more page parts from the final PDF file as images.

    Args:

    - pages (str|list): one or more numbers - either space-separated in
      text form or in a list.

    Kwargs:

    - names (list): a set of strings as names for the images.  If the list is
      not long enough for all the images, naming reverts back to defaults.
    - cols_rows (str|list): two numbers - either comma-separated in text form
      or in a list. The first number is how many columns the page should be
      divided into, and the second number is how many rows the page should be
      divided into.
    - areas (list): a list of sets of numbers, with four numbers
      in each.  The set numbers represent the top-left *x* and *y* and the
      bottom-right *x* and *y* locations on the page of a rectangle that must be
      extracted
    - height (float): the height of an area to be extracted
    - width (float): the width of an area to be extracted
    - x (float): the X-value of top-left corner of an area to be extracted
    - y (float): the Y-value top-left corner of an area to be extracted
    - repeat (bool): if True, extract the height & width area multiple times
    - x_gap (float): the x gap used when extracting a repeated area
    - y_gap (float): the y gap used when extracting a repeated area

    Notes:

      All areas are specified as a (BBox, name) tuple, added to a list
      keyed on page number, and stored in `globals.extracts`. They are
      processed during/after document Save()
    """
    _pages = tools.sequence_split(pages, star=True)
    if not _pages:
        feedback("At least one page must be specified for Extract.", True)
    # ---- set local vars from kwargs
    names = kwargs.get("names", [])
    areas = kwargs.get("areas", None)
    cols_rows = kwargs.get("cols_rows", None)
    if ("*" in _pages or "all" in _pages) and names:
        feedback(
            "Must specify actual page numbers for Extract if also using names.", True
        )
    # settings used for card area extraction
    height = tools.as_float(kwargs.get("height", 0), "height")
    width = tools.as_float(kwargs.get("width", 0), "width")
    tl_x = tools.as_float(kwargs.get("x", 1), "x")
    tl_y = tools.as_float(kwargs.get("y", 1), "y")
    gap_x = tools.as_float(kwargs.get("x_gap", 0), "x_gap")
    gap_y = tools.as_float(kwargs.get("y_gap", 0), "y_gap")
    repeat = tools.as_bool(kwargs.get("repeat", False))
    cards = True if (height and width) else False
    if (cols_rows and areas and cards) or (not areas and not cols_rows and not cards):
        feedback(
            "Specify either areas OR cols_rows OR height & width for Extract -"
            " only one of these options must be chosen.",
            True,
        )
    if areas:
        if not isinstance(areas, list):
            feedback("The areas specified for Extract must be a list.", True)
        for area in areas:
            if not isinstance(area, tuple) or len(area) != 4:
                feedback(
                    "The area bounds specified for Extract must be a set of 4 numbers,"
                    f' not "{area}".',
                    True,
                )
            for item in area:
                if not isinstance(item, (int, float)):
                    feedback(
                        "The area bounds specified for Extract must all be numeric,"
                        f' not "{area}".',
                        True,
                    )

    if cols_rows:
        _cols_rows = tools.sequence_split(cols_rows, unique=False)
        if len(_cols_rows) != 2:
            feedback(
                "The cols_rows specified for Extract must be a set of 2 numbers,"
                f' not "{_cols_rows}".',
                True,
            )
        for item in _cols_rows:
            if not isinstance(item, int):
                feedback(
                    "The cols_rows specified for Extract must all be integers,"
                    f' not "{_cols_rows}".',
                    True,
                )
    if cards:
        if height > globals.page.height:
            feedback(
                "The height specified for Extract is greater than the page height",
                True,
            )
        if width > globals.page.width:
            feedback(
                "The width specified for Extract is greater than the page width",
                True,
            )
        if tl_y > globals.page.height:
            feedback(
                "The y specified for Extract is greater than the page height",
                True,
            )
        if tl_x > globals.page.width:
            feedback(
                "The x specified for Extract is greater than the page width",
                True,
            )
        if gap_y > globals.page.height:
            feedback(
                "The y_gap specified for Extract is greater than the page height",
                True,
            )
        if gap_x > globals.page.width:
            feedback(
                "The x_gap specified for Extract is greater than the page width",
                True,
            )

    extract_dict = globals.extracts
    name_idx = 0
    for _page in _pages:
        if _page in extract_dict or "*" in extract_dict or "all" in extract_dict:
            data = extract_dict[_page]
        else:
            data = []
        if areas:
            for area in areas:
                try:
                    name = names[name_idx]
                except IndexError:
                    name = None
                name_idx += 1
                # check x1<x2 and y1<y2
                if area[2] < area[0]:
                    feedback(
                        "The second x location must be to the right (higher value)"
                        f' than the first for "{area}".',
                        True,
                    )
                if area[3] < area[1]:
                    feedback(
                        "The second y location must be below (higher value)"
                        f' the first for "{area}".,',
                        True,
                    )
                xl = globals.units * area[0]
                yt = globals.units * area[1]
                xr = globals.units * area[2]
                yb = globals.units * area[3]
                data.append((BBox(tl=Point(xl, yt), br=Point(xr, yb)), name))
        elif cols_rows:
            col_width = globals.page.size[0] / _cols_rows[0]
            row_width = globals.page.size[1] / _cols_rows[1]
            for col in range(0, _cols_rows[0]):
                xl = col * col_width
                xr = (col + 1) * col_width
                for row in range(0, _cols_rows[1]):
                    yt = row * row_width
                    yb = (row + 1) * row_width
                    try:
                        name = names[name_idx]
                    except IndexError:
                        name = None
                    name_idx += 1
                    data.append((BBox(tl=Point(xl, yt), br=Point(xr, yb)), name))
        elif cards:
            _height = height * globals.units
            _width = width * globals.units
            _gap_x = gap_x * globals.units
            _gap_y = gap_y * globals.units

            start_y = tl_y * globals.units
            while start_y + _height < globals.page.size[1]:
                start_x = tl_x * globals.units
                while start_x + _width < globals.page.size[0]:
                    try:
                        name = names[name_idx]
                    except IndexError:
                        name = None
                    name_idx += 1
                    data.append(
                        (
                            BBox(
                                tl=Point(start_x, start_y),
                                br=Point(start_x + _width, start_y + _height),
                            ),
                            name,
                        )
                    )
                    start_x = start_x + _width + _gap_x
                    if not repeat:
                        break
                start_y = start_y + _height + _gap_y
                if not repeat:
                    break
        else:
            pass
        if isinstance(_page, int):
            globals.extracts[_page - 1] = data
        else:
            globals.extracts[_page] = data  # handle `*` and `all`


def extract(pages: object, **kwargs):
    Extract(pages=pages, **kwargs)


def Save(**kwargs):
    """Save the result of all commands to a PDF file.

    Kwargs:

    - output (str):can be set to:

      - ``png`` - to create one image file per page of the PDF; by default the
        names of the PNG files are derived using the PDF filename, with a dash (-)
        followed by the page number;
      - ``svg`` - to create one file per page of the PDF; by default the names
        of the SVG files are derived using the PDF filename, with a dash (-)
        followed by the page number;
      - ``gif`` - to create a GIF file composed of all the PNG pages (these will be
        removed after the file been created)
    - dpi (int): can be set to the dots-per-inch resolution required; by default
      this is ``300``
    - directory (str): export path for the PNG or SVG; if None then use the same
      one as the script
    - filename (str): name of export PDF; if None then use the one from Create()
    - names (list): provide a list of names -- without an extension -- for the
      *output* files that will be created from the PDF;
      the first name corresponds to the first page, the second name to the second
      and so on.  Each will automatically get the correct extension added to it.
      If the term ``None`` is used in place of a name, then that page will **not**
      have an output file created for it.
    - framerate (float): the delay in seconds between each "page" of a GIF image; by
      default this is ``1`` second
    - cards (bool): if set to ``True`` will cause all the card fronts to be
      exported as PNG files;  the names of the files are either derived using the
      PDF filename, with a dash (-) followed by the page number OR set by the user
      with ``card_name`` property in the Deck()
    - stop (bool): if set to ``True`` will cause all the script to stop at this point
    - compression (int): value set will indicate the percentage of compression;
      0 (default) is no compression and 100 is maximum compression (but slowest)

    Notes:

    - Cards are saved by iterating through all the ``fronts`` and ``backs``
      in a DeckOfCards object
    - Zones (defined in the Deck) are drawn before the Cards
    """
    validate_globals()

    # ---- set local vars from kwargs
    dpi = support.to_int(kwargs.get("dpi", DEFAULT_DPI), "dpi")
    framerate = support.to_float(kwargs.get("framerate", 1), "framerate")
    names = kwargs.get("names", None)
    directory = kwargs.get("directory", None)
    cards = kwargs.get("cards", False)  # export individual cards as PNG
    output = kwargs.get("output", None)  # export document into this format e.g. SVG
    local_filename = kwargs.get("filename", None)  # override Create()
    stop_here = kwargs.get("stop", False)  # stop script
    compression = kwargs.get("compression", 0)  # compress output

    # ---- directory
    if globals.pargs.directory:
        globals.directory = globals.pargs.directory
    elif directory:
        globals.directory = directory
    else:
        globals.directory = os.getcwd()
    # print(f'$$$ SAVE {globals.directory=}')
    if not os.path.exists(globals.directory):
        feedback(
            f'Cannot find the directory "{
                globals.directory}" - please create this first.',
            True,
        )

    # ---- draw Deck (and export cards)
    if globals.deck and len(globals.deck.fronts) >= 1:
        globals.deck.draw(
            cnv=globals.canvas,
            export_cards=cards,
            cards=globals.deck_settings.get("cards", DEFAULT_CARD_COUNT),
            copy=globals.deck_settings.get("copy", None),
            card_name=globals.deck_settings.get("card_name", None),
            extra=globals.deck_settings.get("extra", 0),
            grid_marks=globals.deck_settings.get("grid_marks", None),
            zones=globals.deck_settings.get("zones", None),
            image_list=globals.image_list,
            dpi=dpi,
            directory=globals.directory,
        )

    # ---- update current pymupdf Shape
    try:
        globals.canvas.commit()  # add all drawings (to current pymupdf Shape)
    except AssertionError:
        pass  # ignore `assert 0, f'page is None'` from pymupdf

    # ---- save all Pages to file
    msg = "Please check the folder exists and that you have access rights."
    the_filename = local_filename or globals.filename
    output_filepath = os.path.join(globals.directory, the_filename)
    compress_value = 0
    if compression:
        compress_value = tools.as_int(
            compression, "compression", maximum=100, minimum=0
        )
    try:
        globals.document.subset_fonts(verbose=True)  # subset fonts to reduce file size
        if compress_value:
            globals.document.save(
                output_filepath,
                compression_effort=compress_value,  # Brotli compression algorithm
                garbage=4,  # remove unused & duplicates
            )
        else:
            globals.document.save(
                output_filepath, garbage=4
            )  # remove unused & duplicates
    # TODO - allow appending?
    except ValueError as err:
        feedback(f'Unable to overwrite "{output_filepath} - {err}"', False, True)
    except RuntimeError as err:
        feedback(f'Unable to save "{output_filepath}" - {err} - {msg}', True)
    except FileNotFoundError as err:
        feedback(f'Unable to save "{output_filepath}" - {err} - {msg}', True)
    except pymupdf.mupdf.FzErrorSystem as err:
        feedback(f'Unable to save "{output_filepath}" - {err} - {msg}', True)

    # ---- export individual Cards (where only Card fronts exist)
    if globals.deck and len(globals.deck.fronts) >= 1:
        card_names = globals.deck.export_cards_as_images(
            filename=the_filename, directory=globals.directory
        )
        # ---- * export cards as single image
        if False:  # TODO - set and read self.deck_image
            globals.deck.export_cards_as_single_image(
                card_names=card_names,
                filename=the_filename,
                directory=globals.directory,
            )  # default to PNG format

    # ---- save to PNG image(s) or SVG file(s)
    fformat = None
    if output:
        match _lower(output):
            case "png":
                fformat = ExportFormat.PNG
            case "svg":
                fformat = ExportFormat.SVG
            case "gif":
                fformat = ExportFormat.GIF
            case _:
                feedback(f'Unknown output format "{output}"', True)

    if output and globals.pargs.png:  # pargs.png should default to True
        support.pdf_export(
            the_filename,
            fformat,
            dpi,
            names,
            globals.directory,
            framerate=framerate,
        )

    # ---- process area/cols_rows extracts
    support.pdf_frames_to_png(
        source_file=the_filename,
        output=None,  # ??? FIXME
        fformat="png",
        dpi=300,  # ??? FIXME
        directory=directory or globals.directory,
        frames=globals.extracts,
        # page_height=globals.page.size[1],
    )

    # ---- reset key globals to allow for new Deck()
    # ---- pymupdf doc, page, shape/canvas
    globals.document = pymupdf.open()  # pymupdf.Document
    globals.doc_page = globals.document.new_page(
        width=globals.page.size[0], height=globals.page.size[1]
    )  # pymupdf Page
    globals.canvas = globals.doc_page.new_shape()  # pymupdf Shape
    # ---- BaseCanvas
    globals.base = BaseCanvas(
        globals.document, paper=globals.paper  # , defaults=defaults, kwargs=kwargs
    )
    globals.page_count = 0
    globals.extracts = {}
    page_setup()
    # ---- possibly stop?
    if stop_here:
        sys.exit(0)


def save(**kwargs):
    Save(**kwargs)


def margins(**kwargs):
    """Add margins, based on globals settings to a set of kwargs, if not present.

    Kwargs:

    - margin (float): default size of every margin on the page
    - margin_left (float): size of left margin on the page
    - margin_top (float): size of top margin on the page
    - margin_bottom (float): size of bottom margin on the page
    - margin_right (float): size of right margin on the page

    """
    validate_globals()

    kwargs["margin"] = kwargs.get("margin", globals.margins.margin)
    kwargs["margin_left"] = kwargs.get("margin_left", globals.margins.left)
    kwargs["margin_top"] = kwargs.get("margin_top", globals.margins.top)
    kwargs["margin_bottom"] = kwargs.get("margin_bottom", globals.margins.bottom)
    kwargs["margin_right"] = kwargs.get("margin_right", globals.margins.right)
    return kwargs


def Font(name=None, **kwargs):
    """Set the Font for all subsequent text in the output PDF.

    Args:

    - name (str|list): the name of the Font(s)

    Kwargs:

    - size (float): point size of the Font; default is 12
    - stroke (str): named or hexadecimal color of the Font;
      default is "black" for RGB color_model
    - style (str): style, if available, for the Font e.g. "bold", "italic"

    """
    validate_globals()
    _name, _path, _file = tools.get_font_file(name)
    globals.base.font_name = _name or DEFAULT_FONT
    globals.base.font_file = _file
    globals.base.font_size = kwargs.get("size", 12)
    globals.base.font_style = kwargs.get("style", None)
    globals.base.stroke = kwargs.get("stroke", globals.black)


def IconFont(name=None, **kwargs):
    """Set the Font for all subsequent icons in the output PDF.

    Args:

    - name (str): the name of the Font

    Kwargs:

    - size (float): the point size of the Font; default is 12
    - stroke (str): the named or hexadecimal color of the Font;
      default is "black" for RGB color_model
    - style (str): the style, if available, for the Font e.g. "bold", "italic"

    """
    validate_globals()
    _name, _path, _file = tools.get_font_file(name)
    globals.base.icon_font_name = _name or DEFAULT_FONT
    globals.base.icon_font_file = _file
    globals.base.icon_font_size = kwargs.get("size", 12)
    globals.base.icon_font_style = kwargs.get("style", None)
    globals.base.icon_stroke = kwargs.get("stroke", globals.black)


# ---- various ====


def Version():
    """Display the version information."""
    feedback(f"Running protograf version {__version__}.")


def Feedback(msg):
    """Use the feedback() function to display a feedback message.

    Args:

    - msg (str): the message to be displayed
    """
    feedback(msg)


def Today(
    details: str = "datetime", style: str = "iso", formatted: str | None = None
) -> str:
    """Return string-formatted current date / datetime in a pre-defined style

    Args:

    - details (str): what part of the datetime to format
    - style (str): usa, eur (european), or iso - default
    - formatted (str): formatting string following Python conventions;
      https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
    """
    current = datetime.now()
    if formatted:
        try:
            return current.strftime(formatted)
        except Exception:
            feedback('Unable to use formatted value  "{formatted}".', True)
    try:
        sstyle = style.lower()
    except Exception:
        feedback('Unable to use style "{style}" - try "eur" or "usa".', True)

    if details == "date" and sstyle == "usa":
        return current.strftime(f"%B {current.day} %Y")  # USA
    if details == "date" and sstyle == "eur":
        return current.strftime("%Y-%m-%d")  # Europe
    if details == "datetime" and sstyle == "eur":
        return current.strftime("%Y-%m-%d %H:%m")  # Europe
    if details == "datetime" and sstyle == "usa":
        return current.strftime("%B %d %Y %I:%m%p")  # USA
    if details == "time" and sstyle == "eur":
        return current.strftime("%H:%m")  # Europe
    if details == "time" and sstyle == "usa":
        return current.strftime("%I:%m%p")  # USA
    if details == "time":
        return current.strftime("%H:%m:%S")  # iso

    if details == "year":
        return current.strftime("%Y")  # all
    if details == "month" and sstyle == "usa":
        return current.strftime("%B")  # USA
    if details == "month":
        return current.strftime("%m")  # eur
    if details == "day" and sstyle == "usa":
        return current.strftime(f"{current.day}")  # usa
    if details == "day":
        return current.strftime("%d")  # other

    return current.isoformat(timespec="seconds")  # ISO


def Random(end: int = 1, start: int = 0, decimals: int = 2) -> float:
    """Return a random number, in a range, with decimal rounding.

    Args:

    - end (int): maximum last value in the range; defaults to 1
    - start (int): minimum first value in the range; defaults to 0
    - decimals (int): formatting of decimal number being returned; defaults to 2
    """
    rrr = random.random() * end + start
    if decimals == 0:
        return int(rrr)
    return round(rrr, decimals)


# ---- grids ====


def DotGrid(**kwargs):
    kwargs = margins(**kwargs)
    # override defaults ... otherwise grid not "next" to margins
    kwargs["x"] = kwargs.get("x", 0)
    kwargs["y"] = kwargs.get("y", 0)
    dgrd = DotGridShape(canvas=globals.canvas, **kwargs)
    dgrd.draw()
    return dgrd


def dotgrid(row=None, col=None, **kwargs):
    return DotGridShape(**kwargs)


@docstring_loc
def Grid(**kwargs):
    """Draw a lined grid on the canvas.

    Kwargs:

    <base>

    """
    kwargs = margins(**kwargs)
    # override defaults ... otherwise grid not "next" to margins
    kwargs["x"] = kwargs.get("x", 0)
    kwargs["y"] = kwargs.get("y", 0)
    grid = GridShape(canvas=globals.canvas, **kwargs)
    grid.draw()
    return grid


def grid(row=None, col=None, **kwargs):
    return GridShape(**kwargs)


@docstring_loc
def HexHex(**kwargs):
    """Draw a hexhex-based layout on the canvas.

    Kwargs:

    <base>

    """
    kwargs = margins(**kwargs)
    hhgrid = HexHexShape(canvas=globals.canvas, **kwargs)
    # feedback(f'HexHex {kwargs=}')
    hhgrid.draw()
    return hhgrid


def hexhex(row=None, col=None, **kwargs):
    kwargs.pop("canvas", None)
    return HexHexShape(canvas=globals.canvas, **kwargs)


# ---- layouts ====


def Repeat(shapes=None, **kwargs):
    """Draw multiple copies of a Shape across rows and columns.

    Args:

    - shapes (list): the Shapes to be drawn

    Kwargs:

    """
    kwargs = margins(**kwargs)
    kwargs["shapes"] = shapes
    repeat = RepeatShape(**kwargs)
    repeat.draw()


def repeat(shapes=None, **kwargs):
    """Create multiple copies of a Shape across rows and columns."""
    kwargs = margins(**kwargs)
    return RepeatShape(shapes=shapes, **kwargs)


def Lines(rows=1, cols=1, **kwargs):
    """Draw multiple copies of a Line across rows and columns.

    Args:

    - rows (int): the number to be drawn in the vertical direction
    - cols (int): the number to be drawn in the horizontal direction

    Notes:

    The same kwargs as used for a Line shape can be applied here.

    """
    kwargs = margins(**kwargs)
    for row in range(rows):
        for col in range(cols):
            Line(row=row, col=col, **kwargs)


def Sequence(shapes=None, **kwargs):
    """Draw a list of Shapes in a line."""
    kwargs = margins(**kwargs)
    kwargs["shapes"] = shapes
    sequence = SequenceShape(**kwargs)
    sequence.draw()


def sequence(shapes=None, **kwargs):
    """Create a list of Shapes in a line."""
    return SequenceShape(shapes=shapes, **kwargs)


def Table(shapes=None, **kwargs):
    """Draw a grid of rectangles."""
    kwargs = margins(**kwargs)
    kwargs["shapes"] = shapes
    tbl = TableShape(**kwargs)
    tbl.draw()
    return tbl


def table(shapes=None, **kwargs):
    """Create a grid of rectangles."""
    return TableShape(shapes=shapes, **kwargs)


# ---- patterns (grid) ====


def Rectangles(rows=1, cols=1, **kwargs):
    """Draw multiple copies of a Rectangle across rows and columns.

    Args:

    - rows (int): the number to be drawn in the vertical direction
    - cols (int): the number to be drawn in the horizontal direction

    Notes:

    The same kwargs as used for a Rectangle shape can be applied here.

    """
    kwargs = kwargs
    locales = []  # list of Locale namedtuples
    if kwargs.get("hidden"):
        hidden = tools.integer_pairs(kwargs.get("hidden"), "hidden")
    else:
        hidden = None

    counter = 0
    sequence = 0
    for row in range(rows):
        for col in range(cols):
            counter += 1
            if hidden and (row + 1, col + 1) in hidden:
                pass
            else:
                rect = rectangle(row=row, col=col, **kwargs)
                _locale = Locale(
                    col=col,
                    row=row,
                    x=rect.x,
                    y=rect.y,
                    id=f"{col}:{row}",
                    sequence=sequence,
                    label=rect.label,
                    page=globals.page_count + 1,
                )
                kwargs["locale"] = _locale._asdict()
                # Note: Rectangle.calculate_xy() uses the row&col to get y&x
                Rectangle(row=row, col=col, **kwargs)
                locales.append(_locale)
                sequence += 1

    return locales


def Squares(rows=1, cols=1, **kwargs):
    """Draw multiple copies of a Square across rows and columns.

    Args:

    - rows (int): the number to be drawn in the vertical direction
    - cols (int): the number to be drawn in the horizontal direction

    Notes:

    The same kwargs as used for a Square shape can be applied here.

    """
    kwargs = kwargs
    locations = []
    if kwargs.get("hidden"):
        hidden = tools.integer_pairs(kwargs.get("hidden"), "hidden")
    else:
        hidden = None

    for row in range(rows):
        for col in range(cols):
            if hidden and (row + 1, col + 1) in hidden:
                pass
            else:
                square = Square(row=row, col=col, **kwargs)
                locations.append(square.grid)

    return locations


# ---- layout & tracks ====


def Layout(grid, **kwargs):
    """Draw shape(s) in locations, cols, & rows in a virtual layout"""
    validate_globals()

    grid_classname = grid.__class__.__name__ if grid else ""
    kwargs = kwargs
    shapes = kwargs.get("shapes", [])  # shapes or Places
    locations = kwargs.get("locations", [])
    location_rows = kwargs.get("rows", [])
    location_cols = kwargs.get("cols", [])
    corners = kwargs.get("corners", [])  # shapes or Places for corners only!
    rotations = kwargs.get("rotations", [])  # rotations for an edge
    if kwargs.get("masked") and isinstance(kwargs.get("masked"), str):
        masked = tools.sequence_split(kwargs.get("masked"), "masked")
    else:
        masked = kwargs.get("masked", [])
    if kwargs.get("visible") and isinstance(kwargs.get("visible"), str):
        visible = tools.integer_pairs(kwargs.get("visible"), "visible")
    else:
        visible = kwargs.get("visible", [])
    # ---- grid
    layout_grid = kwargs.get("gridlines", None)  # directions ...
    _grid_stroke = kwargs.get("gridlines_stroke", globals.black)
    layout_grid_ends = kwargs.get("gridlines_ends", None)
    layout_grid_fill = kwargs.get("gridlines_fill", None)
    layout_grid_stroke = colrs.get_color(_grid_stroke)
    layout_grid_stroke_width = kwargs.get("gridlines_stroke_width", WIDTH)
    layout_grid_dotted = kwargs.get("gridlines_dotted", False)
    layout_grid_dashed = kwargs.get("gridlines_dashed", None)
    layout_grid_transparency = kwargs.get("gridlines_transparency", None)

    # ---- validate inputs
    if not shapes:
        feedback(f"There is no list of {grid_classname} shapes to draw!", False, True)
    if shapes and not isinstance(shapes, list):
        feedback(f"The values for {grid_classname} 'shapes' must be in a list!", True)
    if not isinstance(grid, VirtualLocations):
        feedback(f"The grid type '{grid_classname} ' is not valid!", True)
    corners_dict = {}
    if corners:
        if not isinstance(corners, list):
            feedback(
                f"The {grid_classname} corners value '{corners}' is not a valid list!",
                True,
            )
        for corner in corners:
            try:
                value = corner[0]
                shape = corner[1]
                if _lower(value) not in ["nw", "ne", "sw", "se", "*"]:
                    feedback(
                        f'The {grid_classname} corner must be one of nw, ne, sw, se (not "{
                            value}")!',
                        True,
                    )
                if not isinstance(shape, BaseShape):
                    feedback(
                        f'The {grid_classname} corner item must be a shape (not "{
                            shape}") !',
                        True,
                    )
                if value == "*":
                    corners_dict["nw"] = shape
                    corners_dict["ne"] = shape
                    corners_dict["sw"] = shape
                    corners_dict["se"] = shape
                else:
                    corners_dict[value] = shape
            except Exception:
                feedback(
                    f'The {grid_classname} corners setting "{
                        corner}" is not a valid list',
                    True,
                )

    # ---- draw grid (using a Shape)
    if layout_grid:
        layout_grid_centroid = grid.grid_centroid  # calculated in layouts
        match grid_classname:
            case "DiamondLocations":
                # ---- get gridlines params
                layout_grid_dirs = tools.validated_gridlines(
                    layout_grid, DirectionGroup.COMPASS, "gridlines"
                )
                layout_grid_hatches = grid.cols // 2 - 1  # for Diamond, rows == cols
                # ---- setup gridlines configuration # eg.  [('d', 10), ('ne', 10)]
                gridlines_count = {
                    "n": grid.cols // 2,
                    "s": grid.cols // 2,
                    "e": grid.rows // 2,
                    "w": grid.rows // 2,
                    "ne": grid.cols // 2 - 1,
                    "nw": grid.cols // 2 - 1,
                    "se": grid.rows // 2 - 1,
                    "sw": grid.rows // 2 - 1,
                }
                gridlines_config = [
                    (_dir, gridlines_count[_dir]) for _dir in layout_grid_dirs
                ]
                # ---- draw lines
                Rhombus(
                    cx=layout_grid_centroid.x,
                    cy=layout_grid_centroid.y,
                    height=grid.total_height,
                    width=grid.total_width,
                    stroke=layout_grid_stroke,
                    stroke_width=layout_grid_stroke_width,
                    stroke_ends=layout_grid_ends,
                    dotted=layout_grid_dotted,
                    dashed=layout_grid_dashed,
                    fill=layout_grid_fill,
                    transparency=layout_grid_transparency,
                    hatches_count=layout_grid_hatches,
                    hatches=gridlines_config,
                    hatches_stroke=layout_grid_stroke,
                    hatches_stroke_width=layout_grid_stroke_width,
                    hatches_ends=layout_grid_ends,
                    hatches_dotted=layout_grid_dotted,
                    hatches_dashed=layout_grid_dashed,
                    # rotation=0,
                )
            case "RectangularLocations":
                # ---- get gridlines params
                layout_grid_dirs = tools.validated_gridlines(
                    layout_grid, DirectionGroup.COMPASS, "gridlines"
                )
                # ---- NO diags for unequal rows & cols:
                if grid.cols != grid.rows:
                    with suppress(ValueError):
                        layout_grid_dirs.remove("ne")
                    with suppress(ValueError):
                        layout_grid_dirs.remove("nw")
                    with suppress(ValueError):
                        layout_grid_dirs.remove("se")
                    with suppress(ValueError):
                        layout_grid_dirs.remove("sw")
                    with suppress(ValueError):
                        layout_grid_dirs.remove("d")
                layout_grid_hatches = grid.cols
                # ---- setup gridlines configuration
                gridlines_config = layout_grid  # eg. '*', 'd', 'ne' etc. or [('d', 10)]
                gridlines_count = {
                    "n": grid.cols // 2,
                    "s": grid.cols // 2,
                    "e": grid.rows // 2 + 1,
                    "w": grid.rows // 2 + 1,
                    "ne": grid.cols + 1,
                    "nw": grid.cols + 1,
                    "se": grid.rows + 1,
                    "sw": grid.rows + 1,
                }
                gridlines_config = [
                    (_dir, gridlines_count[_dir]) for _dir in layout_grid_dirs
                ]
                # ---- draw lines
                Rectangle(
                    cx=layout_grid_centroid.x,
                    cy=layout_grid_centroid.y,
                    height=grid.total_height,
                    width=grid.total_width,
                    stroke=layout_grid_stroke,
                    stroke_width=layout_grid_stroke_width,
                    stroke_ends=layout_grid_ends,
                    dotted=layout_grid_dotted,
                    dashed=layout_grid_dashed,
                    fill=layout_grid_fill,
                    transparency=layout_grid_transparency,
                    hatches_count=layout_grid_hatches,
                    hatches=gridlines_config,
                    hatches_stroke=layout_grid_stroke,
                    hatches_stroke_width=layout_grid_stroke_width,
                    hatches_ends=layout_grid_ends,
                    hatches_dotted=layout_grid_dotted,
                    hatches_dashed=layout_grid_dashed,
                    # rotation=rotation,
                )
            case "TriangularLocations":
                # ---- get gridlines params
                layout_grid_dirs = tools.validated_gridlines(
                    layout_grid, DirectionGroup.TRIANGULAR_HATCH, "gridlines"
                )
                layout_grid_hatches = grid.cols // 2 - 1  # for Diamond, rows == cols
                # ---- setup gridlines configuration # eg.  [('d', 10), ('ne', 10)]
                match grid.facing:
                    case "north" | "south":
                        gridlines_count = {
                            "e": grid.rows * 2,
                            "w": grid.rows * 2,
                            "ne": grid.cols // 2 + 1,
                            "nw": grid.cols // 2 + 1,
                            "se": grid.cols // 2 + 1,
                            "sw": grid.cols // 2 + 1,
                        }
                    case "east" | "west":
                        gridlines_count = {
                            "e": grid.cols * 2,
                            "w": grid.cols * 2,
                            "ne": grid.rows // 2 + 1,
                            "nw": grid.rows // 2 + 1,
                            "se": grid.rows // 2 + 1,
                            "sw": grid.rows // 2 + 1,
                        }
                gridlines_config = [
                    (_dir, gridlines_count[_dir]) for _dir in layout_grid_dirs
                ]
                match grid.facing:
                    case "south":
                        rotation = 180
                    case "east":
                        rotation = 30
                    case "west":
                        rotation = -30
                    case _:
                        rotation = 0
                # ---- draw lines
                Triangle(
                    cx=layout_grid_centroid.x,
                    cy=layout_grid_centroid.y,
                    # height=grid.total_height,
                    side=grid.total_width,
                    stroke=layout_grid_stroke,
                    stroke_width=layout_grid_stroke_width,
                    stroke_ends=layout_grid_ends,
                    dotted=layout_grid_dotted,
                    dashed=layout_grid_dashed,
                    fill=layout_grid_fill,
                    transparency=layout_grid_transparency,
                    hatches_count=layout_grid_hatches,
                    hatches=gridlines_config,
                    hatches_stroke=layout_grid_stroke,
                    hatches_stroke_width=layout_grid_stroke_width,
                    hatches_ends=layout_grid_ends,
                    hatches_dotted=layout_grid_dotted,
                    hatches_dashed=layout_grid_dashed,
                    rotation=rotation,
                )
            case _:
                feedback(
                    f"The grid type '{grid_classname}' does not support gridlines!",
                    True,
                )

    # ---- setup locations; automatically or via user-specification
    shape_id = 0
    _default_locations = enumerate(grid.next_locale())
    default_locations = [*_default_locations]
    if not locations and not location_rows and not location_cols:
        _locations = default_locations
    else:
        _locations = []
        user_locations = tools.integer_pairs(locations, label="locations")
        user_location_rows = tools.sequence_split(
            location_rows, to_int=True, unique=True, msg="rows"
        )
        user_location_cols = tools.sequence_split(
            location_cols, to_int=True, unique=True, msg="col"
        )

        # ---- pick locations according to user input
        for key, user_loc in enumerate(user_locations):
            for loc in default_locations:
                if user_loc[0] == loc[1].col and user_loc[1] == loc[1].row:
                    new_loc = (
                        key,
                        Locale(
                            col=loc[1].col,
                            row=loc[1].row,
                            x=loc[1].x,
                            y=loc[1].y,
                            xy=Point(loc[1].x, loc[1].y),
                            id=f"{loc[1].col}:{loc[1].row}",  # ,loc[1].id,
                            sequence=key,
                            corner=loc[1].corner,
                            page=globals.page_count + 1,
                        ),
                    )
                    _locations.append(new_loc)
            default_locations = enumerate(grid.next_locale())  # regenerate !

        # ---- pick locations by row according to user input
        for key, user_loc in enumerate(user_location_rows):
            for loc in default_locations:
                if user_loc == loc[1].row:
                    new_loc = (
                        key,
                        Locale(
                            col=loc[1].col,
                            row=loc[1].row,
                            x=loc[1].x,
                            y=loc[1].y,
                            xy=Point(loc[1].x, loc[1].y),
                            id=f"{loc[1].col}:{loc[1].row}",  # ,loc[1].id,
                            sequence=key,
                            corner=loc[1].corner,
                            page=globals.page_count + 1,
                        ),
                    )
                    if new_loc not in _locations:
                        _locations.append(new_loc)
            default_locations = enumerate(grid.next_locale())  # regenerate !

        # ---- pick locations by col according to user input
        for key, user_loc in enumerate(user_location_cols):
            for loc in default_locations:
                if user_loc == loc[1].col:
                    new_loc = (
                        key,
                        Locale(
                            col=loc[1].col,
                            row=loc[1].row,
                            x=loc[1].x,
                            y=loc[1].y,
                            xy=Point(loc[1].x, loc[1].y),
                            id=f"{loc[1].col}:{loc[1].row}",  # ,loc[1].id,
                            sequence=key,
                            corner=loc[1].corner,
                            page=globals.page_count + 1,
                        ),
                    )
                    if new_loc not in _locations:
                        _locations.append(new_loc)
            default_locations = enumerate(grid.next_locale())  # regenerate !

    # ---- generate rotations - keyed per sequence number
    rotation_sequence = {}
    if rotations:
        for rotation in rotations:
            if not isinstance(rotation, tuple):
                feedback("The 'rotations' must each contain a set!", True)
            if len(rotation) != 2:
                feedback("The 'rotations' must each contain a set of two items!", True)
            _key = rotation[0]
            if not isinstance(_key, str):
                feedback(
                    "The first value for each 'rotations' entry must be a string!",
                    True,
                )
            rotate = tools.as_float(
                rotation[1], " second value for the 'rotations' entry"
            )
            try:
                _keys = list(tools.sequence_split(_key))
            except Exception:
                feedback(f'Unable to convert "{_key}" into a range of values.')
            for the_key in _keys:
                rotation_sequence[the_key] = rotate

    # ---- iterate through locations & draw shape(s)
    for count, loc in _locations:
        # print("time to draw locs:", count, loc)
        if masked and count + 1 in masked:  # ignore if IN masked
            continue
        if visible and count + 1 not in visible:  # ignore if NOT in visible
            continue
        if grid.stop and count + 1 >= grid.stop:
            break
        if grid.pattern in ["o", "outer"]:  # Rectangle only?
            if count + 1 > grid.rows * 2 + (grid.cols - 2) * 2:
                break
        if shapes:
            # ---- * extract shape data
            rotation = rotation_sequence.get(count + 1, 0)  # default rotation
            if isinstance(shapes[shape_id], BaseShape):
                _shape = shapes[shape_id]
            elif isinstance(shapes[shape_id], tuple):
                _shape = shapes[shape_id][0]
                if not isinstance(_shape, BaseShape):
                    feedback(
                        f'The first item in "{shapes[shape_id]}" must be a shape!', True
                    )
                if len(shapes[shape_id]) > 1:
                    rotation = tools.as_float(shapes[shape_id][1], "rotation")
            elif isinstance(shapes[shape_id], Place):
                _shape = shapes[shape_id].shape
                if not isinstance(_shape, BaseShape):
                    feedback(
                        f'The value for "{shapes[shape_id].name}" must be a shape!',
                        True,
                    )
                if shapes[shape_id].rotation:
                    rotation = tools.as_float(shapes[shape_id].rotation, "rotation")
            else:
                feedback(
                    f'Use a shape, or set, or Place - not "{shapes[shape_id]}"!', True
                )
            # ---- * overwrite shape to use for corner
            if corners_dict:
                if loc.corner in corners_dict.keys():
                    _shape = corners_dict[loc.corner]

            # ---- * set shape to enable overwrite/change of properties
            shape = copy(_shape)

            # ---- * execute shape.draw()
            # breakpoint()
            cx = loc.x * shape.units + shape._o.delta_x
            cy = loc.y * shape.units + shape._o.delta_y
            locale = Locale(
                col=loc.col,
                row=loc.row,
                x=loc.x,
                y=loc.y,
                xy=Point(loc.x, loc.y),
                id=f"{loc.col}:{loc.row}",
                label=f"{loc.col}:{loc.row}",
                sequence=loc.sequence or count,
                page=globals.page_count + 1,
            )
            _locale = locale._asdict()
            shape.draw(_abs_cx=cx, _abs_cy=cy, rotation=rotation, locale=_locale)
            shape_id += 1
        if shape_id > len(shapes) - 1:
            shape_id = 0  # reset and start again
        # ---- display debug
        do_debug = kwargs.get("debug", None)
        if do_debug:
            match _lower(do_debug):
                case "normal" | "none" | "null" | "n":
                    Dot(
                        x=loc.x,
                        y=loc.y,
                        stroke=globals.debug_color,
                        fill=globals.debug_color,
                    )
                case "id" | "i":
                    Dot(
                        x=loc.x,
                        y=loc.y,
                        label=loc.id,
                        stroke=globals.debug_color,
                        fill=globals.debug_color,
                    )
                case "sequence" | "s":
                    Dot(
                        x=loc.x,
                        y=loc.y,
                        label=f"{loc.sequence}",
                        stroke=globals.debug_color,
                        fill=globals.debug_color,
                    )
                case "xy" | "xy":
                    Dot(
                        x=loc.x,
                        y=loc.y,
                        label=f"{round(loc.x, 2)},{round(loc.y, 2)}",
                        stroke=globals.debug_color,
                        fill=globals.debug_color,
                    )
                case "yx" | "yx":
                    Dot(
                        x=loc.x,
                        y=loc.y,
                        label=f"{loc.y},{loc.x}",
                        stroke=globals.debug_color,
                        fill=globals.debug_color,
                    )
                case "colrow" | "cr":
                    Dot(
                        x=loc.x,
                        y=loc.y,
                        label=f"{loc.col},{loc.row}",
                        stroke=globals.debug_color,
                        fill=globals.debug_color,
                    )
                case "col" | "c":
                    Dot(
                        x=loc.x,
                        y=loc.y,
                        label=f"{loc.col}",
                        stroke=globals.debug_color,
                        fill=globals.debug_color,
                    )
                case "row" | "r":
                    Dot(
                        x=loc.x,
                        y=loc.y,
                        label=f"{loc.row}",
                        stroke=globals.debug_color,
                        fill=globals.debug_color,
                    )
                case "rowcol" | "rc":
                    Dot(
                        x=loc.x,
                        y=loc.y,
                        label=f"{loc.row},{loc.col}",
                        stroke=globals.debug_color,
                        fill=globals.debug_color,
                    )
                case _:
                    feedback(f'Unknown debug style "{do_debug}"', True)


def Track(track=None, **kwargs):

    def format_label(shape, data):
        # ---- supply data to text fields
        try:
            shape.label = shapes[shape_id].label.format(**data)  # replace {xyz} entries
            shape.title = shapes[shape_id].title.format(**data)
            shape.heading = shapes[shape_id].heading.format(**data)
        except KeyError as err:
            text = str(err).split()
            feedback(
                f"You cannot use {
                    text[0]} as a special field; remove the {{ }} brackets",
                True,
            )

    validate_globals()

    kwargs = kwargs
    angles = kwargs.get("angles", [])
    rotation_style = kwargs.get("rotation_style", None)
    clockwise = tools.as_bool(kwargs.get("clockwise", None))
    stop = tools.as_int(kwargs.get("stop", None), "stop", allow_none=True)
    start = tools.as_int(kwargs.get("start", None), "start", allow_none=True)
    sequences = kwargs.get("sequences", [])  # which sequence positions to show

    # ---- check kwargs inputs
    if sequences and isinstance(sequences, str):
        sequences = tools.sequence_split(sequences)
    if sequences and stop:
        feedback("Both stop and sequences cannot be used together for a Track!", True)
    if not track:
        track = Polygon(sides=4, fill=None)
    track_name = track.__class__.__name__
    track_abbr = track_name.replace("Shape", "")
    if track_name == "CircleShape":
        if not angles or not isinstance(angles, list) or len(angles) < 2:
            feedback(
                "A list of 2 or more angles is needed for a Circle-based Track!", True
            )
    elif track_name in ["SquareShape", "RectangleShape"]:
        angles = track.get_angles()
        # change behaviour to match Circle and Polygon
        if clockwise is not None:
            clockwise = True
        else:
            clockwise = not clockwise
    elif track_name == "PolygonShape":
        angles = track.get_angles()
    elif track_name not in SHAPES_FOR_TRACK:
        feedback(f"Unable to use a {track_abbr} for a Track!", True)
    if rotation_style:
        _rotation_style = _lower(rotation_style)
        if _rotation_style not in ["o", "outwards", "inwards", "i"]:
            feedback(f"The rotation_style '{rotation_style}' is not valid", True)
    else:
        _rotation_style = None
    shapes = kwargs.get("shapes", [])  # shape(s) to draw at the locations
    if not shapes:
        feedback("Track needs at least one Shape assigned to shapes list", False, True)

    track_points = []  # a list of Ray tuples
    # ---- create Circle vertices and angles
    if track_name == "CircleShape":
        # calculate vertices along circumference
        for angle in angles:
            c_pt = geoms.point_on_circle(
                point_centre=Point(track._u.cx, track._u.cy),
                radius=track._u.radius,
                angle=angle,
            )
            track_points.append(
                Ray(c_pt.x + track._o.delta_x, c_pt.y + track._o.delta_y, angle)
            )
    else:
        # ---- get normal vertices and angles
        vertices = track._shape_vertexes
        angles = [0] * len(vertices) if not angles else angles  # Polyline-> has none!
        for key, vertex in enumerate(vertices):
            track_points.append(Ray(vertex.x, vertex.y, angles[key]))

    # ---- change drawing order
    if clockwise is not None and clockwise is False:
        track_points = list(reversed(track_points))
        _swop = len(track_points) - 1
        track_points = track_points[_swop:] + track_points[:_swop]

    # ---- change start point
    # move the order of vertices
    if start is not None:
        _start = start - 1
        if _start > len(track_points):
            feedback(
                f'The start value "{start}" must be less than the number of vertices!',
                True,
            )
        track_points = track_points[_start:] + track_points[:_start]

    # ---- walk the track & draw shape(s)
    shape_id = 0
    for index, track_point in enumerate(track_points):
        # TODO - delink shape index from track vertex index !
        # ---- * ignore sequence not in the list
        if sequences:
            if index + 1 not in sequences:
                continue
        # ---- * stop early if index exceeded
        if stop and index >= stop:
            break
        # ---- * enable overwrite/change of properties
        if len(shapes) == 0:
            continue
        shape = copy(shapes[shape_id])
        # ---- * store data for use by text
        data = {
            "x": track_point.x,
            "y": track_point.y,
            "theta": track_point.angle,
            "count": index + 1,
        }
        # feedback(f'$$$ Track {index=} {data=}')
        # format_label(shape, data)
        # ---- supply data to change shape's location
        # TODO - can choose line centre, not vertex, as the cx,cy position
        shape.cx = shape.points_to_value(track_point.x - track._o.delta_x)
        shape.cy = shape.points_to_value(track_point.y - track._o.delta_y)
        # feedback(f'\n $$$ Track {track_name=} {shape.cx=}, {shape.cy=}')
        if _rotation_style:
            match _rotation_style:
                case "i" | "inwards":
                    if track_name == "CircleShape":
                        shape_rotation = 90 + track_point.angle
                    elif track_name == "PolygonShape":
                        shape_rotation = 90 + track_point.angle
                    else:
                        shape_rotation = 90 - track_point.angle
                case "o" | "outwards":
                    if track_name == "CircleShape":
                        shape_rotation = 270 + track_point.angle
                    elif track_name in ["SquareShape", "RectangleShape"]:
                        shape_rotation = 270 - track_point.angle
                    elif track_name == "PolygonShape":
                        shape_rotation = 270 + track_point.angle
                    else:
                        shape_rotation = 90 - track_point.angle
                case "f" | "flow" | "follow":
                    if track_name == "CircleShape":
                        shape_rotation = 90 + track_point.angle
                    elif track_name == "PolygonShape":
                        shape_rotation = track_point.angle
                    else:
                        shape_rotation = 90 - track_point.angle
                case _:
                    raise NotImplementedError(
                        f"The rotation_style '{_rotation_style}' is not valid"
                    )
        else:
            shape_rotation = 0
        shape.set_unit_properties()
        # feedback(f'$$$ Track {shape._u}')
        locale = Locale(
            x=track_point.x,
            y=track_point.y,
            id=index,
            sequence=index + 1,
            page=globals.page_count + 1,
        )
        _locale = locale._asdict()
        # print(f'$$$ Track {type(shape)=} {shape_rotation=}')
        # print(f'$$$ Track x,y={track._p2v(locale.x)},{track._p2v(locale.y)})')
        shape.draw(cnv=globals.canvas, rotation=shape_rotation, locale=_locale)
        shape_id += 1
        if shape_id > len(shapes) - 1:
            shape_id = 0  # reset and start again


# ---- bgg API ====


def BGG(
    token: str | None = None,
    user: str | None = None,
    ids: list | None = None,
    progress=False,
    short=500,
    **kwargs,
):
    """Access BGG API for game data"""
    ckwargs = {}
    # ---- self filters
    if kwargs.get("own") is not None:
        ckwargs["own"] = tools.as_bool(kwargs.get("own"))
    if kwargs.get("rated") is not None:
        ckwargs["rated"] = tools.as_bool(kwargs.get("rate"))
    if kwargs.get("played") is not None:
        ckwargs["played"]
    # lib = tools.as_bool(kwargs.get("played"))
    if kwargs.get("commented") is not None:
        ckwargs["commented"] = tools.as_bool(kwargs.get("commented"))
    if kwargs.get("trade") is not None:
        ckwargs["trade"] = tools.as_bool(kwargs.get("trade"))
    if kwargs.get("want") is not None:
        ckwargs["want"] = tools.as_bool(kwargs.get("want"))
    if kwargs.get("wishlist") is not None:
        ckwargs["wishlist"] = tools.as_bool(kwargs.get("wishlist"))
    if kwargs.get("preordered") is not None:
        ckwargs["preordered"] = tools.as_bool(kwargs.get("preordered"))
    if kwargs.get("want_to_play") is not None:
        ckwargs["want_to_play"] = tools.as_bool(kwargs.get("want_to_play"))
    if kwargs.get("want_to_buy") is not None:
        ckwargs["want_to_buy"] = tools.as_bool(kwargs.get("want_to_buy"))
    if kwargs.get("prev_owned") is not None:
        ckwargs["prev_owned"] = tools.as_bool(kwargs.get("prev_owned"))
    if kwargs.get("has_parts") is not None:
        ckwargs["has_parts"] = tools.as_bool(kwargs.get("has_parts"))
    if kwargs.get("want_parts") is not None:
        ckwargs["want_parts"] = tools.as_bool(kwargs.get("want_parts"))
    if kwargs.get("requests") is not None:
        ckwargs["requests"] = tools.as_int(kwargs.get("requests", 60), "requests")
    gamelist = BGGGameList(token, user, **ckwargs)
    if user:
        ids = []
        if gamelist.collection:
            for item in gamelist.collection.items:
                ids.append(item.id)
                _game = BGGGame(
                    token=token, game_id=item.id, user_game=item, user=user, short=short
                )
                gamelist.set_values(_game)
        if not ids:
            feedback(
                f"Sorry - no games could be retrieved for BGG username {user}", True
            )
    elif ids:
        feedback(
            "All board game data accessed via this tool is owned by BoardGameGeek"
            " and provided through their XML API"
        )
        for game_id in ids:
            if progress:
                feedback(f"Retrieving game '{game_id}' from BoardGameGeek...")
            _game = BGGGame(token=token, game_id=game_id, short=short)
            gamelist.set_values(_game)
    else:
        feedback(
            "Please supply either `ids` or `user` to retrieve games from BGG", True
        )
    return gamelist


def named(variable):
    return f"{variable=}".split("=")[0]


# ---- shortcuts ====


def A8BA():
    """Shortcut to setup an A8 page with a Blueprint; use for examples."""
    Create(
        paper="A8",
        margin_left=0.5,
        margin_right=0.5,
        margin_bottom=0.5,
        margin_top=0.5,
        font_size=8,
    )
    Blueprint(stroke_width=0.5)


# ---- inherited docs ====


create.__doc__ = Create.__doc__
page_break.__doc__ = PageBreak.__doc__
save.__doc__ = Save.__doc__


# .__doc__ = .__doc__
