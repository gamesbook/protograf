# -*- coding: utf-8 -*-
"""
Create layouts - grids, repeats, sequences and tracks - for protograf
"""
# lib
import logging

# third party
import jinja2

# local
from protograf.utils.messaging import feedback
from protograf.utils.tools import as_bool
from protograf.base import BaseShape
from protograf.layouts import SequenceShape, RepeatShape
from protograf.shapes import (
    CircleShape,
    HexShape,
    ImageShape,
    PolygonShape,
    RectangleShape,
)
from protograf import globals

log = logging.getLogger(__name__)

DEBUG = False

# ---- Functions


class Switch:
    """
    Decide if to use an element or a value for a card attribute.

    Note:
        * This class is instantiated in the `proto` module, via a script's call
          to the S() function.
        * The class __call__ is accessed via the CardShape draw_card() method
    """

    def __init__(self, **kwargs):
        self.switch_template = kwargs.get("template", None)
        self.result = kwargs.get("result", None)  # usually a Shape
        self.alternate = kwargs.get("alternate", None)  # usually a Shape
        self.dataset = kwargs.get("dataset", [])
        self.members = []  # card IDs, of which the affected card is a member

    def __call__(self, cid):
        """Process the test, for a given card 'ID' in the dataset."""
        record = self.dataset[cid]  # dict data for chosen card
        try:
            outcome = self.switch_template.render(record)
            # print('  +++', f'{ID=} {self.test} {outcome=}')
            boolean = as_bool(outcome)
            if boolean:
                return self.result
            else:
                return self.alternate
        except jinja2.exceptions.UndefinedError as err:
            feedback(f'Switch "{self.test}" is incorrectly constructed ({err})', True)
        except Exception as err:
            feedback(f'Switch "{self.test}" is incorrectly constructed ({err})', True)
        return None


class Lookup:
    """Enable lookup of data in a record of a dataset

    Kwargs:
        lookup: Any
            the lookup column whose value must be used for the match
        target: str
            the name of the column of the data being searched
        result: str
            name of result column containing the data to be returned
        default: Any
            the data to be returned if no match is made

    In short:
        lookup and target enable finding a matching record in the dataset;
        the data in the 'result' column of that record will be returned.

    Note:
        This class will be instantiated in the `proto` module, via a
        script's call to the L() function.
    """

    def __init__(self, **kwargs):
        self.data = kwargs.get("datalist", [])
        self.lookup = kwargs.get("lookup", "")
        self.members = []  # card IDs, of which the affected card is a member

    def __call__(self, cid):
        """Return datalist item number 'ID' (card number)."""
        log.debug("datalist:%s cid:%s", self.datalist, cid)
        try:
            return None
        except (ValueError, TypeError, IndexError):
            return None
