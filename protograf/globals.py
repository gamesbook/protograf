# -*- coding: utf-8 -*-
"""
Global variables for proto (import at top-level)
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm


def initialize():
    global cnv
    global deck
    global deck_settings
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
    global page_width
    global page_height
    global font_size
    global units

    cnv = None  # will become a reportlab.canvas object
    deck = None  # will become a shapes.DeckShape object
    deck_settings = {}  # holds kwargs passed to Deck ; cards, copy, extra, grid_marks
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
    paper = A4
    font_size = 12
    units = cm
    page_width = paper[0] / cm
    page_height = paper[1] / cm
