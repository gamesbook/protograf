# -*- coding: utf-8 -*-
"""
protograf CoreState class for games

Notes:
    * all arrays, such the cells of a board, are (col,row) with 1-based values
"""

# lib

# third party

# module
from protograf.base import BaseShape
from protograf.utils import tools
from protograf.utils.messaging import feedback
from protograf.utils.structures import (  # named tuples; enums
    Point,
    ShapeGeometry,
)

# local


class CoreStateObject(BaseShape):
    """Draw CoreState composite shape on a given canvas."""

    def __init__(self, _object=None, canvas=None, **kwargs):
        super().__init__(_object=_object, canvas=canvas, **kwargs)
        # self.kwargs = kwargs
        # self.set_unit_properties()
        # self.cnv = (
        #     canvas if canvas else globals.canvas
        # )  # a new Page/Shape may now exist
        # ---- unique properties
        self.board = self._commons("board") or kwargs.get("board") or None
        self.positions = self._commons("positions") or kwargs.get("positions") or "."
        self.setup = self._commons("setup") or kwargs.get("setup") or False
        self.setup = tools.as_bool(self.setup, False)
        self.moves = self._commons("moves") or kwargs.get("moves") or None
        self.markers = self._commons("markers") or kwargs.get("markers") or None
        self.markers_stroke = (
            self._commons("markers_stroke") or kwargs.get("markers_stroke") or "yellow"
        )
        self.markers_fraction = (
            self._commons("markers_fraction") or kwargs.get("markers_fraction") or 0.1
        )
        self.markers_fraction = tools.as_float(
            self.markers_fraction, "markers_fraction", minimum=0
        )
        self.markers_transparency = (
            self._commons("markers_transparency")
            or kwargs.get("markers_transparency")
            or 1
        )
        self.markers_transparency = tools.as_float(
            self.markers_transparency, "markers_transparency", minimum=0
        )
        self.markers_shapes = (
            self._commons("markers_shapes") or kwargs.get("markers_shapes") or None
        )
        self.annotations = (
            self._commons("annotations") or kwargs.get("annotations") or None
        )
        # ---- internal properties
        self.game_class = None
        self.position_shapes = []

    def initialise_pieces(self) -> str:
        """Create initial positions."""
        pass

    def _validate_choices(self) -> bool:
        """Check user choices for valid selections."""
        from .core_game import CoreGameObject

        if self.board is None:
            feedback(
                f"The {self.game_class} 'board' property must be set!",
                True,
                True,
            )
        if not isinstance(self.board, CoreGameObject):
            feedback(
                f"The {self.game_class} 'board' property must be a Game shape, "
                f" not a '{type(self.board.name).__name__}'.",
                True,
                True,
            )
            if self.board.pieces is not None:
                if not isinstance(self.board.pieces, (list, tuple)):
                    feedback(
                        f"The {self.game_class} 'pieces' property must be a list of pieces, "
                        f" not a '{type(self.board.pieces).__name__}'.",
                        True,
                        True,
                    )
        if self.positions is not None:
            if not isinstance(self.positions, str):
                feedback(
                    f"The {self.game_class} 'positions' property must"
                    " be a string with positions setting or layout, "
                    f" not a '{type(self.positions).__name__}'.",
                    True,
                    True,
                )
        if self.moves is not None:
            if not isinstance(self.moves, (list, tuple)):
                feedback(
                    f"The {self.game_class} 'moves' property must be a list of moves, "
                    f" not a '{type(self.moves).__name__}'.",
                    True,
                    True,
                )
        if self.markers is not None:
            if not isinstance(self.markers, (list, tuple)):
                feedback(
                    f"The {self.game_class} 'markers' property must be a list of elements, "
                    f" not a '{type(self.markers).__name__}'.",
                    True,
                    True,
                )
        if self.markers_shapes is not None:
            if not isinstance(self.markers_shapes, (list, tuple)):
                feedback(
                    f"The {self.game_class} 'markers_shapes' property must be a list of elements, "
                    f" not a '{type(self.markers_shapes).__name__}'.",
                    True,
                    True,
                )
        if self.annotations is not None:
            if not isinstance(self.annotations, (list, tuple)):
                feedback(
                    f"The {self.game_class} 'annotations' property must be a list of elements, "
                    f" not a '{type(self.annotations).__name__}'.",
                    True,
                    True,
                )
        return True

    @property
    def shape_centre(self) -> Point:
        """Centre of CoreStateObject."""
        return None

    @property
    def geo(self) -> ShapeGeometry:
        """Geometry of CoreStateObject in user units."""
        return None

    @property
    def geometry(self) -> ShapeGeometry:
        """Geometry of CoreStateObject - alias for geo."""
        return self.geo

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw the CoreStateObject on a given canvas."""
        pass
