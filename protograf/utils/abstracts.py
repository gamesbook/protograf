# -*- coding: utf-8 -*-
"""
Abstract Class definitions for protograf
"""

# lib
from abc import ABC, abstractmethod


class ProtografGrid(ABC):

    def __init__(self, rows=1, cols=1, **kwargs):
        """
        Args:

        - rows (int): the number to be drawn in the vertical direction
        - cols (int): the number to be drawn in the horizontal direction
        """
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.kwargs = kwargs
        self.common = kwargs.get("common", None)
        self.locales = []  # should be list of Locale namedtuples
        self.cells = {}  # store ShapeGeometry keyed on location

    @abstractmethod
    def cell(self):
        """All grids must be able to return a grid cell."""
        pass

    def _commons(self, prop: str) -> object:
        """re"""
        if self.common:
            return vars(self.common).get(prop)
