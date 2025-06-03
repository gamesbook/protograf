# -*- coding: utf-8 -*-
"""
Global variables for proto (import at top-level)
"""
from pymupdf import paper_size
from protograf.utils.support import unit


def initialize():
    global archive
    global css
    global document
    global base
    global back
    global deck
    global deck_settings
    global card_frames  # card boundaries - use for image extraction
    global dataset
    global dataset_type
    global image_list
    global filename
    global margins
    global footer
    global footer_draw
    global pargs
    global paper
    global page  #  (width, height) in points
    global page_width  # user units
    global page_height  # user units
    global page_fill
    global page_count
    global page_grid
    global font_size
    global units

    archive = None  # will become a pymupdf.Archive()
    css = None  # will become a string containing CSS font details
    document = None  # will become a pymupdf.Document object
    doc_page = None  # will become a pymupdf.Page object
    canvas = None  # will become a pymupdf.Shape object; one created per Page
    base = None  # will become a base.BaseCanvas object
    deck = None  # will become a proto.DeckOfCards object
    deck_settings = (
        {}
    )  # holds kwargs passed to DeckOfCards ; #cards, copy, extra, grid_marks
    card_frames = {}  # list of proto.BBox card outlines; keyed on page number
    filename = None
    dataset = None  # will become a dictionary of data loaded from a file
    dataset_type = None  # set when Data is loaded; enum DatasetType
    image_list = []  # filenames stored when Data is loaded from image dir
    margins = None  # will become a proto.PageMargins object
    footer = None
    footer_draw = False
    page_count = 0
    pargs = None
    units = unit.cm
    paper = "A4"
    page = paper_size(paper)  # (width, height) in points
    page_width = page[0] / units  # width in user units
    page_height = page[1] / units  # height in user units
    page_fill = "white"  # page color
    page_grid = False
    font_size = 12
