# -*- coding: utf-8 -*-
"""
protograf Abstract Class for grid layouts
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
        self.locales = []  # should be list of Locale namedtuples

    @abstractmethod
    def cell(self):
        """All grids must be able to return a grid cell."""
        pass
