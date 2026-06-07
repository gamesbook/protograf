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
    global page
    global pargs
    global paper
    global page_count
    global units
    global white

    archive = None  # will become a pymupdf Archive
    base = None  # will become a base.BaseCanvas object
    black = "black"  # stroke color for RGB
    canvas = None  # will become a pymupdf Shape object; one created per pymupdf Page
    card_frames = {}  # list of protograf.BBox card frames; keyed on page number
    color_model = "RGB"
    css = None  # will become a string containing CSS font location
    dataset = None  # will become a dictionary of data loaded from a file
    dataset_type = None  # set when Data is loaded; enum DatasetType
    debug_color = RGB_DEBUG_COLOR
    deck = None  # will become a protograf.DeckOfCards object
    deck_settings = {}  # DeckOfCards; cards, copy, card_name, extra, grid_marks, zones
    directory = None  # set by Save() command
    doc_page = None  # will become a pymupdf Page object
    document = None  # will become a pymupdf Document object
    extracts = {}  # list of protograf.BBox areas to be extracted, keyed on page number
    filename = None
    font_size = 12
    footer_draw = False
    footer = None
    image_list = []  # filenames stored when Data is loaded from image dir
    margins = None  # will become a protograf.PageMargins object
    override = False  # used, as needed, to override Shape properties with globals
    page_count = 0
    page = None  # will become a protograf.DocumentPage object
    paper = DEFAULT_PAGE_SIZE
    pargs = None
    units = unit.cm
    white = "white"  # fill color for RGB
