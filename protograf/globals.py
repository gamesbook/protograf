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
    global deck
    global deck_settings
    global card_frames  # card boundaries - use for image extraction
    global dataset
    global dataset_type
    global image_list
    global filename
    global margin
    global margin_left
    global margin_top
    global margin_bottom
    global margin_right
    global footer
    global footer_draw
    global page_count
    global pargs
    global paper
    global page  #  (width, height) in points
    global page_width
    global page_height
    global font_size
    global units

    archive = None  # will become a pymupdf.Archive()
    css = None  # will become a string containing CSS font details
    document = None  # will become a pymupdf.Document object
    doc_page = None  # will become a pymupdf.Page object
    canvas = None  # will become a pymupdf.Shape object; one created per Page
    base = None  # will become a base.BaseCanvas object
    deck = None  # will become a shapes.DeckShape object
    deck_settings = {}  # holds kwargs passed to Deck ; cards, copy, extra, grid_marks
    card_frames = {}  # list of BBox card outlines; keyed on page number
    filename = None
    dataset = None  # will become a dictionary of data loaded from a file
    dataset_type = None  # set when Data is loaded; enum DatasetType
    image_list = []  # filenames stored when Data is loaded from image dir
    margin = 1
    margin_left = margin
    margin_top = margin
    margin_bottom = margin
    margin_right = margin
    footer = None
    footer_draw = False
    page_count = 0
    pargs = None
    paper = "A4"
    font_size = 12
    units = unit.cm
    page = paper_size(paper)  # (width, height) in points
    page_width = page[0] / unit.cm  # width in user units
    page_height = page[1] / unit.cm  # height in user units
