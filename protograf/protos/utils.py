# -*- coding: utf-8 -*-
from protograf.utils.messaging import feedback

globals_set = False


def validate_globals():
    """Check that Create has been called to set initialise globals"""
    global globals_set
    if not globals_set:
        feedback("Please ensure Create() command is called first!", True)


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
