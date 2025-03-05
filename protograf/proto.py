# -*- coding: utf-8 -*-
"""
Primary interface for protograf (imported at top-level)

Note:
    Some imports here are for sake of reuse by the top-level import
"""
# lib
import argparse
from copy import copy
from datetime import datetime
import itertools
import logging
import math
import os
import pathlib
import random
import sys
from typing import Union, Any

# third party
import jinja2
from reportlab.lib.pagesizes import *
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4

# from reportlab.lib.colors import black, white
from reportlab.lib.units import cm, inch
from reportlab.lib.colors import (
    Color,
    aliceblue,
    antiquewhite,
    aqua,
    aquamarine,
    azure,
    beige,
    bisque,
    black,
    blanchedalmond,
    blue,
    blueviolet,
    brown,
    burlywood,
    cadetblue,
    chartreuse,
    chocolate,
    coral,
    cornflowerblue,
    cornsilk,
    crimson,
    cyan,
    darkblue,
    darkcyan,
    darkgoldenrod,
    darkgray,
    darkgrey,
    darkgreen,
    darkkhaki,
    darkmagenta,
    darkolivegreen,
    darkorange,
    darkorchid,
    darkred,
    darksalmon,
    darkseagreen,
    darkslateblue,
    darkslategray,
    darkslategrey,
    darkturquoise,
    darkviolet,
    deeppink,
    deepskyblue,
    dimgray,
    dimgrey,
    dodgerblue,
    floralwhite,
    forestgreen,
    fuchsia,
    gainsboro,
    ghostwhite,
    gold,
    goldenrod,
    gray,
    grey,
    green,
    greenyellow,
    honeydew,
    hotpink,
    indianred,
    indigo,
    ivory,
    khaki,
    lavender,
    lavenderblush,
    lawngreen,
    lemonchiffon,
    lightblue,
    lightcoral,
    lightcyan,
    lightgoldenrodyellow,
    lightgreen,
    lightgrey,
    lightpink,
    lightsalmon,
    lightseagreen,
    lightskyblue,
    lightslategray,
    lightslategrey,
    lightsteelblue,
    lightyellow,
    lime,
    limegreen,
    linen,
    magenta,
    maroon,
    mediumaquamarine,
    mediumblue,
    mediumorchid,
    mediumpurple,
    mediumseagreen,
    mediumslateblue,
    mediumspringgreen,
    mediumturquoise,
    mediumvioletred,
    midnightblue,
    mintcream,
    mistyrose,
    moccasin,
    navajowhite,
    navy,
    oldlace,
    olive,
    olivedrab,
    orange,
    orangered,
    orchid,
    palegoldenrod,
    palegreen,
    paleturquoise,
    palevioletred,
    papayawhip,
    peachpuff,
    peru,
    pink,
    plum,
    powderblue,
    purple,
    red,
    rosybrown,
    royalblue,
    saddlebrown,
    salmon,
    sandybrown,
    seagreen,
    seashell,
    sienna,
    silver,
    skyblue,
    slateblue,
    slategray,
    slategrey,
    snow,
    springgreen,
    steelblue,
    tan,
    teal,
    thistle,
    tomato,
    turquoise,
    violet,
    wheat,
    white,
    whitesmoke,
    yellow,
    yellowgreen,
    fidblue,
    fidred,
    fidlightblue,
    cornflower,
    firebrick,
)

# local
from .bgg import BGGGame, BGGGameList
from .base import BaseCanvas, GroupBase, COLORS, DEBUG_COLOR
from .dice import Dice, DiceD4, DiceD6, DiceD8, DiceD10, DiceD12, DiceD20, DiceD100
from .shapes import (
    BaseShape,
    ArcShape,
    ArrowShape,
    BezierShape,
    ChordShape,
    CircleShape,
    CommonShape,
    CompassShape,
    DotShape,
    EllipseShape,
    EquilateralTriangleShape,
    FooterShape,
    HexShape,
    ImageShape,
    LineShape,
    QRCodeShape,
    PolygonShape,
    PolylineShape,
    RectangleShape,
    RhombusShape,
    RightAngledTriangleShape,
    SectorShape,
    ShapeShape,
    SquareShape,
    StadiumShape,
    StarShape,
    StarFieldShape,
    TextShape,
    TrapezoidShape,
    GRID_SHAPES_WITH_CENTRE,
    GRID_SHAPES_NO_CENTRE,
    SHAPES_FOR_TRACK,
)
from .layouts import (
    GridShape,
    DotGridShape,
    RectangularLocations,
    TriangularLocations,
    VirtualLocations,
    ConnectShape,
    RepeatShape,
    SequenceShape,
)
from .groups import DeckShape, Switch
from ._version import __version__

# from protograf.utils.support import (
#     steps, excels, excel_column,  numbers, letters)
from protograf.utils.tools import base_fonts, DatasetType
from protograf.utils import geoms, tools, support
from protograf.utils.geoms import Locale, Point, Place, Ray, equilateral_height
from protograf.utils.support import LookupType, steps

from protograf import globals

log = logging.getLogger(__name__)
globals_set = False


def validate_globals():
    """Check that Create has been called to set initialise globals"""
    global globals_set
    if not globals_set:
        tools.feedback("Please ensure Create() command is called first!", True)


# ---- page-related ====


def Create(**kwargs):
    """Initialisation of page, units and canvas.

    NOTES:
        * Will use argparse to process command-line keyword args
        * Allows shortcut creation of cards
    """
    global globals_set

    # ---- set and confirm globals
    globals.initialize()
    globals_set = True

    # ---- margins
    globals.margin = kwargs.get("margin", globals.margin)
    globals.margin_left = kwargs.get("margin_left", globals.margin)
    globals.margin_top = kwargs.get("margin_top", globals.margin)
    globals.margin_bottom = kwargs.get("margin_bottom", globals.margin)
    globals.margin_right = kwargs.get("margin_right", globals.margin)

    # ---- cards and page
    _cards = kwargs.get("cards", 0)
    landscape = kwargs.get("landscape", False)
    kwargs = margins(**kwargs)
    globals.paper = kwargs.get("paper", globals.paper)
    defaults = kwargs.get("defaults", None)
    globals.units = kwargs.get("units", globals.units)

    # ---- fonts
    base_fonts()
    globals.font_size = kwargs.get("font_size", 12)

    # ---- command-line arguments
    parser = argparse.ArgumentParser()
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
    parser.add_argument(
        "-p", "--pages", help="Specify which pages to process", default=""
    )
    globals.pargs = parser.parse_args()
    # NB - pages does not work - see notes in PageBreak()
    if globals.pargs.pages:
        tools.feedback("Pages is not an implemented feature - sorry!")

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
    globals.filename = os.path.join(globals.pargs.directory, _filename)
    # tools.feedback(f"output: {filename}", False)

    # ---- canvas, paper, page size, and deck
    globals.cnv = BaseCanvas(
        globals.filename, paper=globals.paper, defaults=defaults, kwargs=kwargs
    )
    if landscape:
        globals.cnv.canvas.setPageSize(landscape(globals.cnv.paper))
        globals.page_width = globals.cnv.paper[1]  # point units (1/72 of an inch)
        globals.page_height = globals.cnv.paper[0]  # point units (1/72 of an inch)
    else:
        globals.page_width = globals.cnv.paper[0]  # point units (1/72 of an inch)
        globals.page_height = globals.cnv.paper[1]  # point units (1/72 of an inch)
    if kwargs.get("page_fill"):
        globals.cnv.canvas.setFillColor(kwargs.get("page_fill"))
        globals.cnv.canvas.rect(
            0, 0, globals.page_width, globals.page_height, stroke=0, fill=1
        )

    # ---- cards
    if _cards:
        Deck(canvas=globals.cnv, sequence=range(1, _cards + 1), **kwargs)  # deck var


def create(**kwargs):
    Create(**kwargs)


def Footer(**kwargs):
    validate_globals()

    kwargs["paper"] = globals.paper
    if not kwargs.get("font_size"):
        kwargs["font_size"] = globals.font_size
    globals.footer_draw = kwargs.get("draw", False)
    globals.footer = FooterShape(_object=None, canvas=globals.cnv, **kwargs)
    # footer.draw() - this is called via PageBreak()


def Header(**kwargs):
    validate_globals()
    pass


def PageBreak(**kwargs):
    validate_globals()

    globals.page_count += 1
    kwargs = margins(**kwargs)
    if kwargs.get("footer", globals.footer_draw):
        if globals.footer is None:
            kwargs["paper"] = globals.paper
            kwargs["font_size"] = globals.font_size
            globals.footer = FooterShape(_object=None, canvas=globals.cnv, **kwargs)
        globals.footer.draw(cnv=globals.cnv, ID=globals.page_count, text=None, **kwargs)

    # If count not in the required pargs.pages then do NOT display!
    # Note: this code does not work; seems there is no way to clear or hide the canvas
    #       in ReportLab that would support this operation
    # try:
    #     pages = tools.sequence_split(pargs.pages) if pargs.pages else None
    # except:
    #     tools.feedback(
    #         f'Cannot process "pages" value {pargs.pages} - please check and try again!',
    #         True)
    # if pages and page_count not in pages:
    #     pass
    # else:
    #     cnv.canvas.showPage()
    globals.cnv.canvas.showPage()


def page_break():
    PageBreak()


def Save(**kwargs):
    validate_globals()

    # ---- draw Deck
    if globals.deck and len(globals.deck.deck) >= 1:
        globals.deck.draw(
            globals.cnv,
            cards=globals.deck_settings.get("cards", 9),
            copy=globals.deck_settings.get("copy", None),
            extra=globals.deck_settings.get("extra", 0),
            grid_marks=globals.deck_settings.get("grid_marks", None),
            image_list=globals.image_list,
        )
        globals.cnv.canvas.showPage()

    # ---- save canvas to file
    try:
        globals.cnv.canvas.save()
    except RuntimeError as err:
        tools.feedback(f'Unable to save "{globals.filename}" - {err}', True)
    except FileNotFoundError as err:
        tools.feedback(f'Unable to save "{globals.filename}" - {err}', True)

    # ---- save to image(s)
    output = kwargs.get("output", None)
    dpi = support.to_int(kwargs.get("dpi", 300), "dpi")
    framerate = support.to_float(kwargs.get("framerate", 1), "framerate")
    names = kwargs.get("names", None)
    directory = kwargs.get("directory", None)
    if output and globals.pargs.png:  # pargs.png should default to True
        support.pdf_to_png(
            globals.filename, output, dpi, names, directory, framerate=framerate
        )

    # ---- save cards to image(s)
    cards = kwargs.get("cards", None)
    if cards and globals.pargs.png:  # pargs.png should default to True
        support.pdf_cards_to_png(
            globals.filename,
            output,
            dpi,
            directory,
            globals.card_frames,
            globals.paper[1],
        )


def save(**kwargs):
    Save(**kwargs)


def margins(**kwargs):
    """Add margins to a set of kwargs, if not present."""
    validate_globals()

    kwargs["margin"] = kwargs.get("margin", globals.margin)
    kwargs["margin_left"] = kwargs.get(
        "margin_left", globals.margin_left or globals.margin
    )
    kwargs["margin_top"] = kwargs.get(
        "margin_top", globals.margin_top or globals.margin
    )
    kwargs["margin_bottom"] = kwargs.get(
        "margin_bottom", globals.margin_bottom or globals.margin
    )
    kwargs["margin_right"] = kwargs.get(
        "margin_right", globals.margin_right or globals.margin
    )
    return kwargs


def Font(name=None, **kwargs):
    validate_globals()

    globals.cnv.font_name = name or "Helvetica"
    globals.cnv.font_size = kwargs.get("size", 12)
    globals.cnv.font_style = kwargs.get("style", None)
    globals.cnv.font_directory = kwargs.get("directory", None)
    globals.cnv.stroke = kwargs.get("stroke", black)


# ---- various ====


def Version():
    tools.feedback(f"Running protograf version {__version__}.")


def Feedback(msg):
    tools.feedback(msg)


def Today(details: str = "datetime", style: str = "iso"):
    """Return string-formatted current date / datetime in a pre-defined style"""
    current = datetime.now()
    if details == "date" and style == "usa":
        return current.strftime("%B %d %Y")  # USA
    if details == "date" and style == "eur":
        return current.strftime("%Y-%m-%d")  # Europe
    if details == "datetime" and style == "eur":
        return current.strftime("%Y-%m-%d %H:%m")  # Europe
    if details == "datetime" and style == "usa":
        return current.strftime("%B %d %Y %I:%m%p")  # USA
    return current.isoformat(timespec="seconds")  # ISO


def Random(end: int = 1, start: int = 0, decimals: int = 2):
    """Return a random number, in a range (`start` to `end`), rounded to `decimals`."""
    rrr = random.random() * end + start
    if decimals == 0:
        return int(rrr)
    return round(rrr, decimals)


# ---- cards ====


def Matrix(labels: list = None, data: list = None) -> list:
    """Return list of dicts; each element is a unique combo of all the items in `data`"""
    if data is None:
        return []
    combos = list(itertools.product(*data))
    # check labels
    data_length = len(combos[0])
    if labels == []:
        labels = [f"VALUE{item+1}" for item in range(0, data_length)]
    else:
        if len(labels) != data_length:
            tools.feedback(
                "The number of labels must equal the number of combinations!", True
            )
    result = []
    for item in combos:
        entry = {}
        for key, value in enumerate(item):
            entry[labels[key]] = value
        result.append(entry)
    return result


def Card(sequence, *elements, **kwargs):
    """Add one or more elements to a card or cards.

    NOTE: A Card receives its `draw()` command via Save()!
    """
    kwargs = margins(**kwargs)
    if not globals.deck:
        tools.feedback("The Deck() has not been defined or is incorrect.", True)
    _cards = []
    # int - single card
    try:
        _card = int(sequence)
        _cards = range(_card, _card + 1)
    except Exception:
        pass
    # string - either 'all'/'*' .OR. a range: '1', '1-2', '1-3,5-6'
    if not _cards:
        try:
            card_count = (
                len(globals.dataset)
                if globals.dataset
                else (
                    len(globals.deck.image_list)
                    if globals.deck.image_list
                    else (
                        tools.as_int(globals.deck.cards, "cards")
                        if globals.deck.cards
                        else 0
                    )
                )
            )
            if isinstance(sequence, list) and not isinstance(sequence, str):
                _cards = sequence
            elif sequence.lower() == "all" or sequence.lower() == "*":
                _cards = list(range(1, card_count + 1))
            else:
                _cards = tools.sequence_split(sequence)
        except Exception as err:
            log.error(
                "Handling sequence:%s with dataset:%s & images:%s - %s",
                sequence,
                globals.dataset,
                globals.deck.image_list,
                err,
            )
            tools.feedback(
                f'Unable to convert "{sequence}" into a card or range or cards {globals.deck}.'
            )
    for index, _card in enumerate(_cards):
        card = globals.deck.get(_card - 1)  # cards internally number from ZERO
        if card:
            for element in elements:
                element.members = _cards  # track all related cards
                card.members = _cards
                card.elements.append(element)  # may be Group or Shape or Query
        else:
            tools.feedback(f'Cannot find card#{_card}. (Check "cards" setting in Deck)')


def Counter(sequence, *elements, **kwargs):
    """Add one or more elements to a counter or counters.

    NOTE: A Counter receives its `draw()` command via Save()!
    """
    Card(sequence, *elements, **kwargs)


def Deck(**kwargs):
    """Initialise a deck with all its settings, including source(s) of data.

    NOTE: A Deck receives its `draw()` command from Save()!
    """
    validate_globals()

    kwargs = margins(**kwargs)
    kwargs["dataset"] = globals.dataset
    globals.deck = DeckShape(**kwargs)
    globals.deck_settings["grid_marks"] = kwargs.get("grid_marks", None)


def CounterSheet(**kwargs):
    """Initialise a countersheet with all its settings, including source(s) of data.

    NOTE: A CounterSheet (aka Deck) receives its `draw()` command from Save()!
    """
    kwargs["_is_countersheet"] = True
    Deck(**kwargs)


def group(*args, **kwargs):

    gb = GroupBase(kwargs)
    for arg in args:
        gb.append(arg)
    return gb


# ---- data and functions ====


def Data(**kwargs):
    """Load data from file, dictionary, list-of-lists, or directory for later access."""
    validate_globals()

    filename = kwargs.get("filename", None)  # CSV or Excel
    matrix = kwargs.get("matrix", None)  # Matrix()
    data_list = kwargs.get("data_list", None)  # list-of-lists
    images = kwargs.get("images", None)  # directory
    images_filter = kwargs.get("images_filter", "")  # e.g. .png
    filters = tools.sequence_split(images_filter, False, True)
    source = kwargs.get("source", None)  # dict
    # extra cards added to deck (handle special cases not in the dataset)
    globals.deck_settings["extra"] = tools.as_int(kwargs.get("extra", 0), "extra")
    try:
        int(globals.deck_settings["extra"])
    except Exception:
        tools.feedback(
            f'Extra must be a whole number, not "{kwargs.get("extra")}"!', True
        )

    if filename:  # handle excel and CSV
        globals.dataset = tools.load_data(filename, **kwargs)
        globals.dataset_type = DatasetType.FILE
    elif matrix:  # handle pre-built dict
        globals.dataset = matrix
        globals.dataset_type = DatasetType.MATRIX
    elif data_list:  # handle list-of-lists
        try:
            keys = data_list[0]  # get keys from first sub-list
            dict_list = [dict(zip(keys, values)) for values in data_list[1:]]
            globals.dataset = dict_list
            globals.dataset_type = DatasetType.DICT
        except Exception:
            tools.feedback("The data_list is not valid - please check", True)
    elif source:  # handle pre-built dict
        if not isinstance(source, dict):
            source_type = type(source)
            tools.feedback(f"The source must be a dictionary, not {source_type}", True)
        globals.dataset = source
        globals.dataset_type = DatasetType.DICT
    elif images:  # create list of images
        src = pathlib.Path(images)
        if not src.is_dir():
            # look relative to script's location
            script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
            full_path = os.path.join(script_dir, images)
            src = pathlib.Path(full_path)
            if not src.is_dir():
                tools.feedback(
                    f"Cannot locate or access directory: {images} or {full_path}", True
                )
        for child in src.iterdir():
            if not filters or child.suffix in filters:
                globals.image_list.append(str(child))
        if len(globals.image_list) == 0:
            tools.feedback(
                f'Directory "{src}" has no relevant files or cannot be loaded!', True
            )
        else:
            globals.dataset_type = DatasetType.IMAGE
    else:
        tools.feedback("You must provide data for the Data command!", True)

    return globals.dataset


def S(test="", result=None, alternate=None):
    """
    Enable Selection of data from a dataset list

        test: str
            boolean-type Jinja2 expression which can be evaluated to return True/False
            e.g. {{ NAME == 'fred' }} gets the column "NAME" value from the dataset
            and tests its equivalence to the value "fred"
        result: str or element
            returned if `test` evaluates to True
        alternate: str or element
            OPTIONAL; returned if `test` evaluates to False; if not supplied, then None
    """

    if globals.dataset and isinstance(globals.dataset, list):
        environment = jinja2.Environment()
        template = environment.from_string(str(test))
        return Switch(
            template=template,
            result=result,
            alternate=alternate,
            dataset=globals.dataset,
        )
    return None


def L(lookup: str, target: str, result: str, default: Any = "") -> LookupType:
    """Enable Lookup of data in a record of a dataset

        lookup: str
            the lookup column whose value must be used for the match ("source" record)
        target: str
            the name of the column of the data being searched ("target" record)
        result: str
            name of result column containing the data to be returned ("target" record)
        default: Any
            the data to be returned if NO match is made

    In short:
        lookup and target enable finding a matching record in the dataset;
        the data in the 'result' column of that record is stored as an
        `lookup: result` entry in the returned lookups dictionary of the LookupType
    """
    lookups = {}
    if globals.dataset and isinstance(globals.dataset, list):
        # validate the lookup column
        if lookup not in globals.dataset[0].keys():
            tools.feedback(f'The "{lookup}" column is not available.', True)
        for key, record in enumerate(globals.dataset):
            if target in record.keys():
                if result in record.keys():
                    lookups[record[target]] = record[result]
                else:
                    tools.feedback(f'The "{result}" column is not available.', True)
            else:
                tools.feedback(f'The "{target}" column is not available.', True)
    result = LookupType(column=lookup, lookups=lookups)
    return result


def T(string: str, data: dict = None):
    """Use string to create a Jinja2 Template."""
    environment = jinja2.Environment()
    template = environment.from_string(str(string))
    return template


def Set(_object, **kwargs):
    """Overwrite one or more properties for a Shape/object with new value(s)"""
    for kw in kwargs.keys():
        log.debug("Set: %s %s %s", kw, kwargs[kw], type(kwargs[kw]))
        setattr(_object, kw, kwargs[kw])
    return _object


# ---- shapes ====


def base_shape(source=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["source"] = source
    bshape = BaseShape(canvas=globals.cnv, **kwargs)
    return bshape


def Common(source=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["source"] = source
    cshape = CommonShape(canvas=globals.cnv, **kwargs)
    return cshape


def common(source=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["source"] = source
    cshape = CommonShape(canvas=globals.cnv, **kwargs)
    return cshape


def Image(source=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["source"] = source
    image = ImageShape(canvas=globals.cnv, **kwargs)
    image.draw()
    return image


def image(source=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["source"] = source
    return ImageShape(canvas=globals.cnv, **kwargs)


def Arc(**kwargs):
    kwargs = margins(**kwargs)
    arc = ArcShape(canvas=globals.cnv, **kwargs)
    arc.draw()
    return arc


def arc(**kwargs):
    kwargs = margins(**kwargs)
    return ArcShape(canvas=globals.cnv, **kwargs)


def Arrow(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    arr = arrow(row=row, col=col, **kwargs)
    arr.draw()
    return arr


def arrow(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return ArrowShape(canvas=globals.cnv, **kwargs)


def Bezier(**kwargs):
    kwargs = margins(**kwargs)
    bezier = BezierShape(canvas=globals.cnv, **kwargs)
    bezier.draw()
    return bezier


def bezier(**kwargs):
    kwargs = margins(**kwargs)
    return BezierShape(canvas=globals.cnv, **kwargs)


def Chord(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    chd = chord(row=row, col=col, **kwargs)
    chd.draw()
    return chd


def chord(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return ChordShape(canvas=globals.cnv, **kwargs)


def Circle(**kwargs):
    kwargs = margins(**kwargs)
    circle = CircleShape(canvas=globals.cnv, **kwargs)
    circle.draw()
    return circle


def circle(**kwargs):
    kwargs = margins(**kwargs)
    return CircleShape(canvas=globals.cnv, **kwargs)


def Compass(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    cmpss = compass(row=row, col=col, **kwargs)
    cmpss.draw()
    return cmpss


def compass(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    return CompassShape(canvas=globals.cnv, **kwargs)


def Dot(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    dtt = dot(row=row, col=col, **kwargs)
    dtt.draw()
    return dtt


def dot(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    return DotShape(canvas=globals.cnv, **kwargs)


def Ellipse(**kwargs):
    kwargs = margins(**kwargs)
    ellipse = EllipseShape(canvas=globals.cnv, **kwargs)
    ellipse.draw()
    return ellipse


def ellipse(**kwargs):
    kwargs = margins(**kwargs)
    return EllipseShape(canvas=globals.cnv, **kwargs)


def EquilateralTriangle(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    eqt = EquilateralTriangleShape(canvas=globals.cnv, **kwargs)
    eqt.draw()
    return eqt


def equilateraltriangle(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    return EquilateralTriangleShape(canvas=globals.cnv, **kwargs)


def Hexagon(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    # print(f'Will draw HexShape: {kwargs}')
    kwargs["row"] = row
    kwargs["col"] = col
    hexagon = HexShape(canvas=globals.cnv, **kwargs)
    hexagon.draw()
    return hexagon


def hexagon(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return HexShape(canvas=globals.cnv, **kwargs)


def Line(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    lin = line(row=row, col=col, **kwargs)
    lin.draw()
    return lin


def line(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return LineShape(canvas=globals.cnv, **kwargs)


def Polygon(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    poly = polygon(row=row, col=col, **kwargs)
    poly.draw()
    return poly


def polygon(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return PolygonShape(canvas=globals.cnv, **kwargs)


def Polyline(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    polylin = polyline(row=row, col=col, **kwargs)
    polylin.draw()
    return polylin


def polyline(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return PolylineShape(canvas=globals.cnv, **kwargs)


def RightAngledTriangle(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    rat = RightAngledTriangleShape(canvas=globals.cnv, **kwargs)
    rat.draw()
    return rat


def rightangledtriangle(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    return RightAngledTriangleShape(canvas=globals.cnv, **kwargs)


def Rhombus(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    rhomb = rhombus(row=row, col=col, **kwargs)
    rhomb.draw()
    return rhomb


def rhombus(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    return RhombusShape(canvas=globals.cnv, **kwargs)


def Rectangle(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    rect = rectangle(row=row, col=col, **kwargs)
    rect.draw()
    return rect


def rectangle(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return RectangleShape(canvas=globals.cnv, **kwargs)


def Polyshape(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    shapeshape = polyshape(row=row, col=col, **kwargs)
    shapeshape.draw()
    return shapeshape


def polyshape(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return ShapeShape(canvas=globals.cnv, **kwargs)


def QRCode(source=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["source"] = source
    image = QRCodeShape(canvas=globals.cnv, **kwargs)
    image.draw()
    return image


def qrcode(source=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["source"] = source
    return QRCodeShape(canvas=globals.cnv, **kwargs)


def Sector(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    sct = sector(row=row, col=col, **kwargs)
    sct.draw()
    return sct


def sector(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return SectorShape(canvas=globals.cnv, **kwargs)


def Square(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    sqr = square(row=row, col=col, **kwargs)
    sqr.draw()
    return sqr


def square(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return SquareShape(canvas=globals.cnv, **kwargs)


def Stadium(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    std = StadiumShape(canvas=globals.cnv, **kwargs)
    std.draw()
    return std


def stadium(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return StadiumShape(canvas=globals.cnv, **kwargs)


def Star(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    star = StarShape(canvas=globals.cnv, **kwargs)
    star.draw()
    return star


def star(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return StarShape(canvas=globals.cnv, **kwargs)


def StarField(**kwargs):
    kwargs = margins(**kwargs)
    starfield = StarFieldShape(canvas=globals.cnv, **kwargs)
    starfield.draw()
    return starfield


def starfield(**kwargs):
    kwargs = margins(**kwargs)
    return StarFieldShape(canvas=globals.cnv, **kwargs)


def Text(**kwargs):
    kwargs = margins(**kwargs)
    text = TextShape(canvas=globals.cnv, **kwargs)
    text.draw()
    return text


def text(*args, **kwargs):
    kwargs = margins(**kwargs)
    _obj = args[0] if args else None
    return TextShape(_object=_obj, canvas=globals.cnv, **kwargs)


def Trapezoid(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    trp = trapezoid(row=row, col=col, **kwargs)
    trp.draw()
    return trp


def trapezoid(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return TrapezoidShape(canvas=globals.cnv, **kwargs)


# ---- grids ====


def DotGrid(**kwargs):
    kwargs = margins(**kwargs)
    # override defaults ... otherwise grid not "next" to margins
    kwargs["x"] = kwargs.get("x", 0)
    kwargs["y"] = kwargs.get("y", 0)
    dgrd = DotGridShape(canvas=globals.cnv, **kwargs)
    dgrd.draw()
    return dgrd


def Grid(**kwargs):
    kwargs = margins(**kwargs)
    # override defaults ... otherwise grid not "next" to margins
    kwargs["x"] = kwargs.get("x", 0)
    kwargs["y"] = kwargs.get("y", 0)
    grid = GridShape(canvas=globals.cnv, **kwargs)
    grid.draw()
    return grid


def Blueprint(**kwargs):

    def set_style(style_name):
        """Set Blueprint color and fill."""
        match style_name:
            case "green":
                color, fill = "#CECE2C", "#35705E"
            case "grey" | "gray":
                color, fill = white, "#A1969C"
            case "blue" | "invert" | "inverted":
                color, fill = honeydew, "#3085AC"
            case _:
                color, fill = "#3085AC", None
                if style_name is not None:
                    tools.feedback(
                        f'The Blueprint style "{style_name}" is unknown', False, True
                    )
        return color, fill

    kwargs = margins(**kwargs)
    if kwargs.get("common"):
        tools.feedback('The "common" property cannot be used with a Blueprint.', True)
    kwargs["units"] = kwargs.get("units", globals.units)
    side = 1.0
    if kwargs["units"] == inch:
        side = 0.5
    decimals = tools.as_int(kwargs.get("decimals", 0), "Blueprint decimals")
    # override defaults ... otherwise grid not "next" to margins
    numbering = kwargs.get("numbering", True)
    kwargs["side"] = kwargs.get("side", side)
    kwargs["x"] = kwargs.get("x", 0)
    kwargs["y"] = kwargs.get("y", 0)
    m_x = kwargs["units"] * (globals.margin_left + globals.margin_right)
    m_y = kwargs["units"] * (globals.margin_top + globals.margin_bottom)
    _cols = (globals.paper[0] - m_x) / (kwargs["units"] * float(kwargs["side"]))
    _rows = (globals.paper[1] - m_y) / (kwargs["units"] * float(kwargs["side"]))
    rows = int(_rows)
    cols = int(_cols)
    kwargs["rows"] = kwargs.get("rows", rows)
    kwargs["cols"] = kwargs.get("cols", cols)
    kwargs["stroke_width"] = kwargs.get("stroke_width", 0.2)  # fine line
    default_font_size = 10 * math.sqrt(globals.paper[0]) / math.sqrt(A4[0])
    dotted = kwargs.get("dotted", False)
    kwargs["font_size"] = kwargs.get("font_size", default_font_size)
    line_stroke, page_fill = set_style(kwargs.get("style", None))
    kwargs["stroke"] = kwargs.get("stroke", line_stroke)
    kwargs["fill"] = kwargs.get("fill", page_fill)
    # ---- page color (optional)
    if kwargs["fill"] is not None:
        globals.cnv.canvas.setFillColor(kwargs["fill"])
        globals.cnv.canvas.rect(
            0, 0, globals.paper[0], globals.paper[1], stroke=0, fill=1
        )
    # ---- numbering
    if numbering:
        _common = Common(
            font_size=kwargs["font_size"],
            stroke=kwargs["stroke"],
            units=kwargs["units"],
        )
        for x in range(1, kwargs["cols"] + 1):
            Text(
                x=x * side,
                y=kwargs["y"] - kwargs["side"] / 2.0,
                text=f"{x*side:{1}.{decimals}f}",
                common=_common,
            )
        for y in range(1, kwargs["rows"] + 1):
            Text(
                x=kwargs["x"] - kwargs["side"] / 2.0,
                y=y * side - _common.points_to_value(kwargs["font_size"]) / 2.0,
                text=f"{y*side:{1}.{decimals}f}",
                common=_common,
            )
        # draw "zero" number
        z_x = kwargs["units"] * globals.margin_left
        z_y = kwargs["units"] * globals.margin_bottom
        corner_dist = geoms.length_of_line(Point(0, 0), Point(z_x, z_y))
        corner_frac = corner_dist * 0.66 / kwargs["units"]
        # tools.feedback(f'*** {z_x=} {z_y=} {corner_dist=}')
        zero_pt = geoms.point_on_line(Point(0, 0), Point(z_x, z_y), corner_frac)
        Text(
            x=zero_pt.x / kwargs["units"] - kwargs["side"] / 4.0,
            y=zero_pt.y / kwargs["units"] - kwargs["side"] / 4.0,
            text="0",
            common=_common,
        )
    # ---- draw subgrid
    if kwargs.get("subdivisions"):
        local_kwargs = copy(kwargs)
        sub_count = int(kwargs.get("subdivisions"))
        local_kwargs["side"] = float(side / sub_count)
        local_kwargs["rows"] = sub_count * kwargs["rows"]
        local_kwargs["cols"] = sub_count * kwargs["cols"]
        local_kwargs["stroke_width"] = kwargs.get("stroke_width") / 2.0
        local_kwargs["stroke"] = kwargs.get("subdivisions_stroke", kwargs["stroke"])
        local_kwargs["dashed"] = kwargs.get("subdivisions_dashed", [])
        local_kwargs["dotted"] = kwargs.get("subdivisions_dotted", True)
        if local_kwargs["dashed"]:
            local_kwargs["dotted"] = False
        subgrid = GridShape(canvas=globals.cnv, **local_kwargs)
        subgrid.draw(cnv=globals.cnv)
    # ---- draw Blueprint grid
    grid = GridShape(
        canvas=globals.cnv, dotted=dotted, **kwargs
    )  # don't add canvas as arg here!
    grid.draw(cnv=globals.cnv)
    return grid


# ---- connect ====


def Connect(shape_from, shape_to, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["shape_from"] = shape_from
    kwargs["shape_to"] = shape_to
    connect = ConnectShape(canvas=globals.cnv, **kwargs)
    connect.draw(cnv=globals.cnv)
    return connect


def connect(shape_from, shape_to, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["shape_from"] = shape_from
    kwargs["shape_to"] = shape_to
    return ConnectShape(canvas=globals.cnv, **kwargs)


# ---- repeats ====


def Repeat(_object, **kwargs):
    """Draw multiple copies of a shape across rows and columns."""
    kwargs = margins(**kwargs)
    repeat = RepeatShape(_object=_object, **kwargs)
    repeat.draw()


def repeat(_object, **kwargs):
    kwargs = margins(**kwargs)
    return RepeatShape(_object=_object, **kwargs)


def Lines(rows=1, cols=1, **kwargs):
    kwargs = margins(**kwargs)
    for row in range(rows):
        for col in range(cols):
            Line(row=row, col=col, **kwargs)


# ---- sequence ====


def Sequence(_object=None, **kwargs):
    """Draw a set of objects in a line."""
    kwargs = margins(**kwargs)
    sequence = SequenceShape(_object=_object, **kwargs)
    sequence.draw()


def sequence(_object=None, **kwargs):
    """Draw a set of objects in a line."""
    return SequenceShape(_object=_object, **kwargs)


# ---- patterns (grid) ====


def Hexagons(rows=1, cols=1, sides=None, **kwargs):
    """Draw a set of hexagons in a pattern."""
    kwargs = kwargs
    locales = []  # list of Locale namedtuples
    if kwargs.get("hidden"):
        hidden = tools.integer_pairs(kwargs.get("hidden"), "hidden")
    else:
        hidden = None

    def draw_hexagons(
        rows: int, cols: int, stop: int, the_cols: list, odd_mid: bool = True
    ):
        """Draw rows of hexagons for each column in `the_cols`"""
        sequence = 0
        top_row = 0
        end_row = rows - 1
        if not odd_mid:
            end_row = rows
            top_row = 1
        for ccol in the_cols:
            top_row = top_row + 1 if ccol & 1 != 0 else top_row  # odd col
            end_row = end_row - 1 if ccol & 1 == 0 else end_row  # even col
            # print('ccol, top_row, end_row', ccol, top_row, end_row)
            for row in range(top_row - 1, end_row + 1):
                _row = row + 1
                # tools.feedback(f'{ccol=}, {_row=}')
                if hidden and (_row, ccol) in hidden:
                    pass
                else:
                    hxgn = Hexagon(
                        row=row, col=ccol - 1, hex_rows=rows, hex_cols=cols, **kwargs
                    )
                    _locale = Locale(
                        col=ccol - 1,
                        row=row,
                        x=hxgn.grid.x,
                        y=hxgn.grid.y,
                        id=f"{ccol - 1}:{row}",
                        sequence=sequence,
                        label=hxgn.grid.label,
                    )
                    locales.append(_locale)
                    sequence += 1

            if ccol - 1 == stop:  # reached "leftmost" -> reset counters
                top_row = 1
                end_row = rows - 1
        return locales

    if kwargs.get("hex_layout") and kwargs.get("orientation"):
        if kwargs.get("orientation").lower() in ["p", "pointy"] and kwargs.get(
            "hex_layout"
        ) not in ["r", "rec", "rect", "rectangle"]:
            tools.feedback(
                "Cannot use this Hexagons `hex_layout` with pointy hexagons!", True
            )

    if kwargs.get("hex_layout") in ["c", "cir", "circle"]:
        if not sides and (
            (rows is not None and rows < 3) and (cols is not None and cols < 3)
        ):
            tools.feedback("The minimum values for rows/cols is 3!", True)
        if rows and rows > 1:
            cols = rows
        if cols and cols > 1:
            rows = cols
        if rows != cols:
            rows = cols
        if sides:
            if sides < 2:
                tools.feedback("The minimum value for sides is 2!", True)
            rows = 2 * sides - 1
            cols = rows
        else:
            if rows & 1 == 0:
                tools.feedback("An odd number is needed for rows!", True)
            if cols & 1 == 0:
                tools.feedback("An odd number is needed for cols!", True)
            sides = rows // 2 + 1
        odd_mid = False if sides & 1 == 0 else True
        the_cols = list(range(sides, 0, -1)) + list(range(sides + 1, rows + 1))
        locales = draw_hexagons(rows, cols, 0, the_cols, odd_mid=odd_mid)

    elif kwargs.get("hex_layout") in ["d", "dia", "diamond"]:
        cols = rows * 2 - 1
        the_cols = list(range(rows, 0, -1)) + list(range(rows + 1, cols + 1))
        locales = draw_hexagons(rows, cols, 0, the_cols)

    elif kwargs.get("hex_layout") in ["t", "tri", "triangle"]:
        tools.feedback(f"Cannot draw triangle-pattern hexagons: {kwargs}", True)

    elif kwargs.get("hex_layout") in ["l", "loz", "stadium"]:
        tools.feedback(f"Cannot draw stadium-pattern hexagons: {kwargs}", True)

    else:  # default to rectangular layout
        sequence = 0
        for row in range(rows):
            for col in range(cols):
                if hidden and (row + 1, col + 1) in hidden:
                    pass
                else:
                    hxgn = Hexagon(
                        row=row, col=col, hex_rows=rows, hex_cols=cols, **kwargs
                    )
                    _locale = Locale(
                        col=col,
                        row=row,
                        x=hxgn.grid.x,
                        y=hxgn.grid.y,
                        id=f"{col}:{row}",
                        sequence=sequence,
                        label=hxgn.grid.label,
                    )
                    locales.append(_locale)
                    sequence += 1

    return locales


def Rectangles(rows=1, cols=1, **kwargs):
    """Draw a set of rectangles in a pattern."""
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
                )
                kwargs["locale"] = _locale._asdict()
                Rectangle(row=row, col=col, **kwargs)
                locales.append(_locale)
                sequence += 1

    return locales


def Squares(rows=1, cols=1, **kwargs):
    """Draw a set of squares in a pattern."""
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


def Location(grid: list, label: str, shapes: list, **kwargs):
    kwargs = kwargs

    def test_foo(x: bool = True, **kwargs):
        print("--- test only ---", kwargs)

    def draw_shape(shape: BaseShape, point: Point, locale: Locale):
        shape_name = shape.__class__.__name__
        shape_abbr = shape_name.replace("Shape", "")
        # shape._debug(cnv.canvas, point=loc)
        dx = shape.kwargs.get("dx", 0)  # user-units
        dy = shape.kwargs.get("dy", 0)  # user-units
        pts = shape.values_to_points([dx, dy])  # absolute units (points)
        try:
            x = point.x + pts[0]
            y = point.y + pts[1]
            kwargs["locale"] = locale
            # tools.feedback(f"{shape=} :: {loc.x=}, {loc.y=} // {dx=}, {dy=}")
            # tools.feedback(f"{kwargs=}")
            # tools.feedback(f"{label} :: {shape_name=}")
            if shape_name in GRID_SHAPES_WITH_CENTRE:
                shape.draw(_abs_cx=x, _abs_cy=y, **kwargs)
            elif shape_name in GRID_SHAPES_NO_CENTRE:
                shape.draw(_abs_x=x, _abs_y=y, **kwargs)
            else:
                tools.feedback(f"Unable to draw {shape_abbr}s in Location!", True)
        except Exception as err:
            tools.feedback(err, False)
            tools.feedback(
                f"Unable to draw the '{shape_abbr}' - please check its settings!", True
            )

    # checks
    if grid is None or not isinstance(grid, list):
        tools.feedback("The grid (as a list) must be supplied!", True)

    # get location centre from grid via the label
    locale, point = None, None
    for _locale in grid:
        if _locale.label.lower() == str(label).lower():
            point = Point(_locale.x, _locale.y)
            locale = _locale
            break
    if point is None:
        msg = ""
        if label and "," in label:
            msg = " (Did you mean to use Locations?)"
        tools.feedback(f"The Location '{label}' is not in the grid!{msg}", True)

    if shapes:
        try:
            iter(shapes)
        except TypeError:
            tools.feedback("The Location shapes property must contain a list!", True)
        for shape in shapes:
            if shape.__class__.__name__ == "GroupBase":
                tools.feedback(f"Group drawing ({shape}) NOT IMPLEMENTED YET", True)
            else:
                draw_shape(shape, point, locale)


def Locations(grid: list, labels: Union[str, list], shapes: list, **kwargs):
    kwargs = kwargs

    if grid is None or not isinstance(grid, list):
        tools.feedback("The grid (as a list) must be supplied!", True)
    if labels is None:
        tools.feedback("No grid location labels supplied!", True)
    if shapes is None:
        tools.feedback("No list of shapes supplied!", True)
    if isinstance(labels, str):
        _labels = [_label.strip() for _label in labels.split(",")]
        if labels.lower() == "all" or labels.lower() == "*":
            _labels = []
            for loc in grid:
                if isinstance(loc, Locale):
                    _labels.append(loc.label)
    elif isinstance(labels, list):
        _labels = labels
    else:
        tools.feedback(
            "Grid location labels must be a list or a comma-delimited string!", True
        )

    if not isinstance(shapes, list):
        tools.feedback("Shapes must contain a list of shapes!", True)

    for label in _labels:
        # tools.feedback(f'{label=} :: {shapes=}')
        Location(grid, label, shapes)


def LinkLine(grid: list, locations: Union[list, str], **kwargs):
    """Enable a line link between one or more locations in a grid."""
    kwargs = kwargs
    if isinstance(locations, str):  # should be a comma-delimited string
        locations = tools.sequence_split(locations, False, False)
    if not isinstance(locations, list):
        tools.feedback(f"'{locations} is not a list - please check!", True)
    if len(locations) < 2:
        tools.feedback("There should be at least 2 locations to create links!", True)
    dummy = base_shape()  # a BaseShape - not drawable!
    for index, location in enumerate(locations):
        # precheck
        if isinstance(location, str):
            location = (location, 0, 0)  # reformat into standard notation
        if not isinstance(location, tuple) or len(location) != 3:
            tools.feedback(
                f"The location '{location}' is not valid -- please check its syntax!",
                True,
            )
        # get location centre from grid via the label
        loc = None
        for position in grid:
            if location[0] == position.label:
                loc = Point(position.x, position.y)
                break
        if loc is None:
            tools.feedback(f"The location '{location[0]}' is not in the grid!", True)
        # new line?
        if index + 1 < len(locations):
            # location #2
            location_2 = locations[index + 1]
            if isinstance(location_2, str):
                location_2 = (location_2, 0, 0)  # reformat into standard notation
            if not isinstance(location_2, tuple) or len(location_2) != 3:
                tools.feedback(
                    f"The location '{location_2}' is not valid - please check its syntax!",
                    True,
                )
            loc_2 = None
            for position in grid:
                if location_2[0] == position.label:
                    loc_2 = Point(position.x, position.y)
                    break
            if loc_2 is None:
                tools.feedback(
                    f"The location '{location_2[0]}' is not in the grid!", True
                )
            if location == location_2:
                tools.feedback(
                    "Locations must differ from each other - "
                    f"({location} matches {location_2})!",
                    True,
                )
            # line start/end
            x = dummy.points_to_value(loc.x) + location[1]
            y = dummy.points_to_value(loc.y) + location[2]
            x1 = dummy.points_to_value(loc_2.x) + location_2[1]
            y1 = dummy.points_to_value(loc_2.y) + location_2[2]

            _line = line(x=x, y=y, x1=x1, y1=y1, **kwargs)
            # tools.feedback(f"{x=}, {y=}, {x1=}, {y1=}")
            delta_x = globals.margin_left
            delta_y = globals.margin_bottom
            # tools.feedback(f"{delta_x=}, {delta_y=}")
            _line.draw(
                off_x=-delta_x,
                off_y=-delta_y,
            )


# ---- layout & tracks ====


def Layout(grid, **kwargs):
    """Determine locations for cols&rows in a virtual layout and draw shape(s)"""
    validate_globals()

    kwargs = kwargs
    shapes = kwargs.get("shapes", [])  # shapes or Places
    locations = kwargs.get("locations", [])
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

    # ---- validate inputs
    if not shapes:
        tools.feedback("There is no list of shapes to draw!", False, True)
    if shapes and not isinstance(shapes, list):
        tools.feedback("The values for 'shapes' must be in a list!", True)
    if not isinstance(grid, VirtualLocations):
        tools.feedback(f"The grid value '{grid}' is not valid!", True)
    corners_dict = {}
    if corners:
        if not isinstance(corners, list):
            tools.feedback(f"The corners value '{corners}' is not a valid list!", True)
        for corner in corners:
            try:
                value = corner[0]
                shape = corner[1]
                if value.lower() not in ["nw", "ne", "sw", "se", "*"]:
                    tools.feedback(
                        f'The corner must be one of nw, ne, sw, se (not "{value}")!',
                        True,
                    )
                if not isinstance(shape, BaseShape):
                    tools.feedback(
                        f'The corner item must be a shape (not "{shape}") !', True
                    )
                if value == "*":
                    corners_dict["nw"] = shape
                    corners_dict["ne"] = shape
                    corners_dict["sw"] = shape
                    corners_dict["se"] = shape
                else:
                    corners_dict[value] = shape
            except Exception:
                tools.feedback(
                    f'The corners setting "{corner}" is not a valid list', True
                )

    # ---- setup locations; automatically or via user-specification
    shape_id = 0
    default_locations = enumerate(grid.next_locale())
    if not locations:
        _locations = default_locations
    else:
        _locations = []
        user_locations = tools.integer_pairs(locations, label="locations")
        # restructure and pick locations according to user input
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
                            id=f"{loc[1].col}:{loc[1].row}",  # ,loc[1].id,
                            sequence=key,
                            corner=loc[1].corner,
                        ),
                    )
                    _locations.append(new_loc)
            default_locations = enumerate(grid.next_locale())  # regenerate !

    # ---- generate rotations - keyed per sequence number
    rotation_sequence = {}
    if rotations:
        for rotation in rotations:
            if not isinstance(rotation, tuple):
                tools.feedback("The 'rotations' must each contain a set!", True)
            if len(rotation) != 2:
                tools.feedback(
                    "The 'rotations' must each contain a set of two items!", True
                )
            _key = rotation[0]
            if not isinstance(_key, str):
                tools.feedback(
                    "The first value for rreach 'rotations' entry must be a string!",
                    True,
                )
            rotate = tools.as_float(
                rotation[1], " second value for the 'rotations' entry"
            )
            try:
                _keys = list(tools.sequence_split(_key))
            except Exception:
                tools.feedback(f'Unable to convert "{_key}" into a range of values.')
            for the_key in _keys:
                rotation_sequence[the_key] = rotate

    # ---- iterate through locations & draw shape(s)
    for count, loc in _locations:
        if masked and count + 1 in masked:  # ignore if IN masked
            continue
        if visible and count + 1 not in visible:  # ignore if NOT in visible
            continue
        if grid.stop and count + 1 >= grid.stop:
            break
        if grid.pattern in ["o", "outer"]:
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
                    tools.feedback(
                        f'The first item in "{shapes[shape_id]}" must be a shape!', True
                    )
                if len(shapes[shape_id]) > 1:
                    rotation = tools.as_float(shapes[shape_id][1], "rotation")
            elif isinstance(shapes[shape_id], Place):
                _shape = shapes[shape_id].shape
                if not isinstance(_shape, BaseShape):
                    tools.feedback(
                        f'The value for "{shapes[shape_id].name}" must be a shape!',
                        True,
                    )
                if shapes[shape_id].rotation:
                    rotation = tools.as_float(shapes[shape_id].rotation, "rotation")
            else:
                tools.feedback(
                    f'Use a shape, or set, or Place - not "{shapes[shape_id]}"!', True
                )
            # ---- * overwrite shape to use for corner
            if corners_dict:
                if loc.corner in corners_dict.keys():
                    _shape = corners_dict[loc.corner]

            # ---- * set shape to enable overwrite/change of properties
            shape = copy(_shape)

            # DEPRECATED - now use jinja2 templates
            # ---- * update shape's text fields
            # data = {
            #     'col': loc.col, 'row': loc.row, 'x': loc.x, 'y': loc.y,
            #     'count': count + 1, 'count_zero': count}
            # try:
            #     shape.label = shapes[shape_id].label.format(**data)  # replace {xyz} entries
            #     shape.title = shapes[shape_id].title.format(**data)
            #     shape.heading = shapes[shape_id].heading.format(**data)
            # except KeyError as err:
            #     text = str(err).split()
            #     tools.feedback(
            #         f'You cannot use {text[0]} as a special field; remove the {{ }} brackets',
            #         True)

            # ---- * execute shape.draw()
            cx = loc.x * shape.units + shape._o.delta_x
            cy = loc.y * shape.units + shape._o.delta_y
            locale = Locale(
                col=loc.col,
                row=loc.row,
                x=loc.x,
                y=loc.y,
                id=f"{loc.col}:{loc.row}",
                sequence=loc.sequence,
            )
            _locale = locale._asdict()
            shape.draw(_abs_cx=cx, _abs_cy=cy, rotation=rotation, locale=_locale)
            shape_id += 1
        if shape_id > len(shapes) - 1:
            shape_id = 0  # reset and start again
        # ---- display debug
        do_debug = kwargs.get("debug", None)
        if do_debug:
            match str(do_debug).lower():
                case "normal" | "none" | "null" | "n":
                    Dot(x=loc.x, y=loc.y, stroke=DEBUG_COLOR, fill=DEBUG_COLOR)
                case "id" | "i":
                    Dot(
                        x=loc.x,
                        y=loc.y,
                        label=loc.id,
                        stroke=DEBUG_COLOR,
                        fill=DEBUG_COLOR,
                    )
                case "sequence" | "s":
                    Dot(
                        x=loc.x,
                        y=loc.y,
                        label=f"{loc.sequence}",
                        stroke=DEBUG_COLOR,
                        fill=DEBUG_COLOR,
                    )
                case "xy" | "xy":
                    Dot(
                        x=loc.x,
                        y=loc.y,
                        label=f"{loc.x},{loc.y}",
                        stroke=DEBUG_COLOR,
                        fill=DEBUG_COLOR,
                    )
                case "yx" | "yx":
                    Dot(
                        x=loc.x,
                        y=loc.y,
                        label=f"{loc.y},{loc.x}",
                        stroke=DEBUG_COLOR,
                        fill=DEBUG_COLOR,
                    )
                case "colrow" | "cr":
                    Dot(
                        x=loc.x,
                        y=loc.y,
                        label=f"{loc.col},{loc.row}",
                        stroke=DEBUG_COLOR,
                        fill=DEBUG_COLOR,
                    )
                case "rowcol" | "rc":
                    Dot(
                        x=loc.x,
                        y=loc.y,
                        label=f"{loc.row},{loc.col}",
                        stroke=DEBUG_COLOR,
                        fill=DEBUG_COLOR,
                    )
                case _:
                    tools.feedback(f'Unknown debug style "{do_debug}"', True)


def Track(track=None, **kwargs):

    def format_label(shape, data):
        # ---- supply data to text fields
        try:
            shape.label = shapes[shape_id].label.format(**data)  # replace {xyz} entries
            shape.title = shapes[shape_id].title.format(**data)
            shape.heading = shapes[shape_id].heading.format(**data)
        except KeyError as err:
            text = str(err).split()
            tools.feedback(
                f"You cannot use {text[0]} as a special field; remove the {{ }} brackets",
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
        tools.feedback(
            "Both stop and sequences cannot be used together for a Track!", True
        )
    if not track:
        track = Polygon(sides=4, fill=None)
    track_name = track.__class__.__name__
    track_abbr = track_name.replace("Shape", "")
    if track_name == "CircleShape":
        if not angles or not isinstance(angles, list) or len(angles) < 2:
            tools.feedback(
                f"A list of 2 or more angles is needed for a Circle-based Track!", True
            )
    elif track_name in ["SquareShape", "RectangleShape"]:
        angles = track.get_angles()
        # change behaviour to match Circle and Polygon
        if clockwise is not None:
            clockwise = not clockwise
        else:
            clockwise = True
    elif track_name == "PolygonShape":
        angles = track.get_angles()
    elif track_name not in SHAPES_FOR_TRACK:
        tools.feedback(f"Unable to use a {track_abbr} for a Track!", True)
    if rotation_style:
        _rotation_style = str(rotation_style).lower()
        if _rotation_style not in ["o", "outwards", "inwards", "i"]:
            tools.feedback(f"The rotation_style '{rotation_style}' is not valid", True)
    else:
        _rotation_style = None
    shapes = kwargs.get("shapes", [])  # shape(s) to draw at the locations
    if not shapes:
        tools.feedback(
            "Track needs at least one Shape assigned to shapes list", False, True
        )

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
        vertices = track.get_vertices()
        angles = [0] * len(vertices) if not angles else angles  # Polyline-> has none!
        for key, vertex in enumerate(vertices):
            track_points.append(Ray(vertex.x, vertex.y, angles[key]))

    # ---- change drawing order
    if clockwise is not None and clockwise:
        track_points = list(reversed(track_points))
        _swop = len(track_points) - 1
        track_points = track_points[_swop:] + track_points[:_swop]

    # ---- change start point
    # move the order of vertices
    if start is not None:
        _start = start - 1
        if _start > len(track_points):
            tools.feedback(
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
        # tools.feedback(f'*Track* {index=} {data=}')
        # format_label(shape, data)
        # ---- supply data to change shape's location
        # TODO - can choose line centre, not vertex, as the cx,cy position
        shape.cx = shape.points_to_value(track_point.x - track._o.delta_x)
        shape.cy = shape.points_to_value(track_point.y - track._o.delta_y)
        # tools.feedback(f'*Track* {shape.cx=}, {shape.cy=}')
        if _rotation_style:
            match _rotation_style:
                case "i" | "inwards":
                    shape_rotation = 90 + track_point.angle
                case "o" | "outwards":
                    shape_rotation = track_point.angle - 90
                case _:
                    raise NotImplementedError(
                        f"The rotation_style '{_rotation_style}' is not valid"
                    )
        else:
            shape_rotation = 0
        shape.set_unit_properties()
        # tools.feedback(f'Track*** {shape._u}')
        locale = Locale(
            x=track_point.x,
            y=track_point.y,
            id=index,
            sequence=index + 1,
        )
        _locale = locale._asdict()
        shape.draw(cnv=globals.cnv, rotation=shape_rotation, locale=_locale)
        shape_id += 1
        if shape_id > len(shapes) - 1:
            shape_id = 0  # reset and start again


# ---- bgg API ====


def BGG(user: str = None, ids: list = None, progress=False, short=500, **kwargs):
    """Access BGG API for game data"""
    ckwargs = {}
    # ---- self filters
    if kwargs.get("own") is not None:
        ckwargs["own"] = tools.as_bool(kwargs.get("pwn"))
    if kwargs.get("rated") is not None:
        ckwargs["rated"] = tools.as_bool(kwargs.get("rate"))
    if kwargs.get("played") is not None:
        ckwargs["played"] = tools.as_bool(kwargs.get("played"))
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
    gamelist = BGGGameList(user, **ckwargs)
    if user:
        ids = []
        if gamelist.collection:
            for item in gamelist.collection.items:
                ids.append(item.id)
                _game = BGGGame(game_id=item.id, user_game=item, user=user, short=short)
                gamelist.set_values(_game)
        if not ids:
            tools.feedback(
                f"Sorry - no games could be retrieved for BGG username {user}", True
            )
    elif ids:
        tools.feedback(
            "All board game data accessed via this tool is owned by BoardGameGeek"
            " and provided through their XML API"
        )
        for game_id in ids:
            if progress:
                tools.feedback(f"Retrieving game '{game_id}' from BoardGameGeek...")
            _game = BGGGame(game_id=game_id, short=short)
            gamelist.set_values(_game)
    else:
        tools.feedback(
            "Please supply either `ids` or `user` to retrieve games from BGG", True
        )
    return gamelist


# ---- dice ====


def dice(dice="1d6", rolls=None):
    """Roll multiple totals for a kind of die.

    Examples:
    >>> dice('2d6')  # Catan dice roll
    [9]
    >>> dice('3D6', 6)  # D&D Basic Character Attributes
    [14, 11, 8, 10, 9, 7]
    >>> dice()  # single D6 roll
    [3]
    """
    if not dice:
        dice = "1d6"
    try:
        dice = dice.replace(" ", "").replace("D", "d")
        _list = dice.split("d")
        _type, pips = int(_list[0]), int(_list[1])
    except Exception:
        tools.feedback(f'Unable to determine dice type/roll for "{dice}"', True)
    return Dice().multi_roll(count=rolls, pips=pips, dice=_type)


def d4(rolls=None):
    return DiceD4().roll(count=rolls)


def d6(rolls=None):
    return DiceD6().roll(count=rolls)


def d8(rolls=None):
    return DiceD8().roll(count=rolls)


def d10(rolls=None):
    return DiceD10().roll(count=rolls)


def d12(rolls=None):
    return DiceD12().roll(count=rolls)


def d20(rolls=None):
    return DiceD20().roll(count=rolls)


def d100(rolls=None):
    return DiceD100().roll(count=rolls)


def named(variable):
    return f"{variable=}".split("=")[0]
