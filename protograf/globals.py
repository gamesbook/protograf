# -*- coding: utf-8 -*-
"""
Global variables for proto (import at top-level)
"""

# lib
from collections import namedtuple

# third-party
from pymupdf import paper_size

# local
from protograf.utils.constants import (
    RGB_DEBUG_COLOR,
    DEFAULT_MARGIN_SIZE,
    DEFAULT_PAGE_SIZE,
)

UnitPoints = namedtuple(
    "UnitPoints",
    [
        "cm",
        "mm",
        "inch",
        "pt",
    ],
)
# ---- units point equivalents
unit = UnitPoints(
    cm=28.3465,
    mm=2.83465,
    inch=72.0,
    pt=1.0,
)


def initialize():
    global archive
    global css
    global document
    global base
    global back
    global black
    global deck
    global deck_settings
    global debug_color
    global card_frames  # card boundaries - use for image extraction
    global color_model
    global dataset
    global dataset_type
    global directory
    global extracts
    global filename
    global font_size
    global footer
    global footer_draw
    global image_list
    global margins
    global override  # boolean
    global pargs
    global paper
    global page  #  (width, height) in points
    global page_width  # user units
    global page_height  # user units
    global page_fill
    global page_count
    global page_grid  # user units
    global units
    global white

    archive = None  # will become a pymupdf Archive
    css = None  # will become a string containing CSS font location
    document = None  # will become a pymupdf Document object
    doc_page = None  # will become a pymupdf Page object
    canvas = None  # will become a pymupdf Shape object; one created per Page
    base = None  # will become a base.BaseCanvas object
    deck = None  # will become a proto.DeckOfCards object
    # store kwargs for DeckOfCards; #cards, copy, card_name, extra, grid_marks, zones
    deck_settings = {}
    debug_color = RGB_DEBUG_COLOR
    card_frames = {}  # list of proto.BBox card frames; keyed on page number
    filename = None
    directory = None  # set by Save() command
    dataset = None  # will become a dictionary of data loaded from a file
    dataset_type = None  # set when Data is loaded; enum DatasetType
    image_list = []  # filenames stored when Data is loaded from image dir
    extracts = {}  # list of proto.BBox areas to be extracted, keyed on page number
    margins = None  # will become a proto.PageMargins object
    footer = None
    footer_draw = False
    font_size = 12
    pargs = None
    units = unit.cm
    color_model = "RGB"
    override = False  # used, as needed, to override Shape properties with globals
    black = "black"  # stroke color for RGB
    white = "white"  # fill color for RGB
    page_count = 0
    paper = DEFAULT_PAGE_SIZE
    page = paper_size(paper)  # (width, height) in points
    page_width = page[0] / units  # width in user units
    page_height = page[1] / units  # height in user units
    page_fill = "white"  # page color for RGB
    page_grid = None  # grid interval in user units
