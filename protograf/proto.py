# -*- coding: utf-8 -*-
"""
Primary interface for protograf (imported at top-level)

Note:
    Some imports here are for sake of reuse by the top-level import
"""
# lib
import argparse
from copy import copy
from datetime import datetime
import itertools
import logging
import math
import os
from pathlib import Path
import random
import sys
from typing import Union, Any

# third party
import jinja2
import pymupdf
from pymupdf import Rect as muRect, Archive

# local
from .bgg import BGGGame, BGGGameList
from .base import BaseCanvas, GroupBase, WIDTH
from .dice import Dice, DiceD4, DiceD6, DiceD8, DiceD10, DiceD12, DiceD20, DiceD100
from .shapes import (
    BaseShape,
    ArcShape,
    ArrowShape,
    BezierShape,
    ChordShape,
    CircleShape,
    CommonShape,
    CompassShape,
    DotShape,
    EllipseShape,
    EquilateralTriangleShape,
    FooterShape,
    HexShape,
    ImageShape,
    LineShape,
    QRCodeShape,
    PolygonShape,
    PolylineShape,
    RectangleShape,
    RhombusShape,
    RightAngledTriangleShape,
    SectorShape,
    ShapeShape,
    SquareShape,
    StadiumShape,
    StarShape,
    StarFieldShape,
    TextShape,
    TrapezoidShape,
)
from .objects import PolyominoObject, PentominoObject, TetrominoObject
from .layouts import (
    GridShape,
    DotGridShape,
    RectangularLocations,
    TriangularLocations,
    VirtualLocations,
    ConnectShape,
    RepeatShape,
    SequenceShape,
)
from .globals import unit
from .groups import Switch, Lookup  # used in scripts
from ._version import __version__

from protograf.utils import geoms, tools, support
from protograf.utils.constants import (
    DEFAULT_FONT,
    DEBUG_COLOR,
    DEFAULT_CARD_WIDTH,  # cm
    DEFAULT_CARD_HEIGHT,  # cm
    DEFAULT_CARD_COUNT,
    DEFAULT_CARD_RADIUS,  # cm
    DEFAULT_COUNTER_SIZE,  # cm
    DEFAULT_COUNTER_RADIUS,  # cm
    DEFAULT_DPI,
    DEFAULT_MARGIN_SIZE,  # cm
    GRID_SHAPES_WITH_CENTRE,
    GRID_SHAPES_NO_CENTRE,
    SHAPES_FOR_TRACK,
)
from protograf.utils.fonts import builtin_font, FontInterface
from protograf.utils.geoms import equilateral_height  # used in scripts
from protograf.utils.messaging import feedback
from protograf.utils.support import (  # used in scripts
    steps,
    uni,
    uc,
    CACHE_DIRECTORY,
)
from protograf.utils.structures import (
    BBox,
    CardFrame,
    DatasetType,
    DeckPrintState,
    DirectionGroup,
    ExportFormat,
    LookupType,
    Locale,
    PageMargins,
    Point,
    Place,
    Ray,
    TemplatingType,
)
from protograf.utils.tools import (
    base_fonts,
    split,
    save_globals,
    restore_globals,
)  # used in scripts
from protograf import globals

log = logging.getLogger(__name__)
globals_set = False

# user constants
YES = True
NO = False


def validate_globals():
    """Check that Create has been called to set initialise globals"""
    global globals_set
    if not globals_set:
        feedback("Please ensure Create() command is called first!", True)


# ---- Deck / Card related ====


class CardOutline(BaseShape):
    """
    Card outline on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(CardOutline, self).__init__(_object=_object, canvas=canvas, **kwargs)
        self.kwargs = kwargs
        # feedback(f'\n$$$ CardShape KW=> {self.kwargs}')
        self.elements = []  # container for objects which get added to the card
        self.members = None
        if kwargs.get("_is_countersheet", False):
            default_height = DEFAULT_COUNTER_SIZE / globals.units
            default_width = DEFAULT_COUNTER_SIZE / globals.units
            default_radius = DEFAULT_COUNTER_RADIUS / globals.units
        else:
            default_height = DEFAULT_CARD_HEIGHT / globals.units
            default_width = DEFAULT_CARD_WIDTH / globals.units
            default_radius = DEFAULT_CARD_RADIUS / globals.units

        # print(f'$$$ {default_width=} {default_height=} {default_radius=} {globals.units=}')
        self.height = kwargs.get("height", default_height)
        self.width = kwargs.get("width", default_width)
        self.radius = kwargs.get("radius", default_radius)
        self.frame_type = kwargs["frame_type"]
        self.outline = self.get_outline(
            cnv=canvas, row=None, col=None, cid=None, label=None, **kwargs
        )
        # print(f'$$$ {self.frame_type=} {self.width=} {self.height=} {self.radius=} ')
        self.kwargs.pop("width", None)
        self.kwargs.pop("height", None)
        self.kwargs.pop("radius", None)

    def get_outline(self, cnv, row, col, cid, label, **kwargs):
        outline = None
        # feedback(f"$$$ getoutline {row=}, {col=}, {cid=}, {label=}")
        kwargs["height"] = self.height
        kwargs["width"] = self.width
        kwargs["radius"] = self.radius
        kwargs["spacing_x"] = self.spacing_x
        kwargs["spacing_y"] = self.spacing_y
        # NOTE! If other frametypes are allowed, ensure their H/W/R values are set!
        match kwargs["frame_type"]:
            case CardFrame.RECTANGLE:
                outline = RectangleShape(
                    label=label,
                    canvas=cnv,
                    col=col,
                    row=row,
                    **kwargs,
                )
            case CardFrame.CIRCLE:
                outline = CircleShape(
                    label=label, canvas=cnv, col=col, row=row, **kwargs
                )
                self.height = outline.height
                self.width = outline.width
                self.radius = outline.radius
            case CardFrame.HEXAGON:
                outline = HexShape(label=label, canvas=cnv, col=col, row=row, **kwargs)
                hex_geom = outline.get_geometry()
                self.height = hex_geom.height_flat / globals.units
                self.width = hex_geom.diameter / globals.units
                self.radius = hex_geom.radius / globals.units
            case _:
                raise NotImplementedError(
                    f'Cannot handle card frame type: {kwargs["frame_type"]}'
                )
        self.frame_type = kwargs["frame_type"]
        self.outline = outline
        return outline


class CardShape(BaseShape):
    """
    Card shape on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(CardShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        self.kwargs = kwargs
        # feedback(f'\n$$$ CardShape KW=> {self.kwargs}')
        self.elements = []  # container for objects which get added to the card
        self.members = None
        self.outline_shape = CardOutline(_object=_object, canvas=canvas, **kwargs)
        self.outline = self.outline_shape.get_outline(
            cnv=canvas, row=None, col=None, cid=None, label=None, **kwargs
        )
        self.image = kwargs.get("image", None)

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw an element on a given canvas."""
        raise NotImplementedError

    def draw_card(self, cnv, row, col, cid, **kwargs):
        """Draw a card on a given canvas.

        Pass on `deck_data` to other commands, as needed, for them to draw Shapes
        """
        # feedback(f'\n$$$ draw_card  {cid=} {row=} {col=} {kwargs["card_back"]=}')
        # feedback(f'$$$ draw_card  {cid=} KW=> {kwargs}')
        is_card_back = kwargs.get("card_back", False)
        image = kwargs.get("image", None)
        right_gap = kwargs.get("right_gap", 0.0)  # gap between end-of-cards & page edge

        # ---- draw outline
        label = "ID:%s" % cid if self.show_id else ""
        shape_kwargs = copy(kwargs)
        shape_kwargs["is_cards"] = True
        if not is_card_back:
            shape_kwargs["fill"] = kwargs.get("fill", kwargs.get("bleed_fill", None))
        shape_kwargs.pop("image_list", None)  # do NOT draw linked image
        shape_kwargs.pop("image", None)  # do NOT draw get_outline(linked image
        # feedback(f'$$$ draw_card)() {cid=} {row=} {col=} \nKW=> {shape_kwargs}')
        outline = self.outline_shape.get_outline(
            cnv=cnv, row=row, col=col, cid=cid, label=label, **shape_kwargs
        )

        # ---- custom geometry
        if kwargs["frame_type"] == CardFrame.HEXAGON:
            _geom = outline.get_geometry()
            radius, diameter, side, half_flat = (
                _geom.radius,
                2.0 * _geom.radius,
                _geom.side,
                _geom.half_flat,
            )
            side = self.points_to_value(side)
            half_flat = self.points_to_value(half_flat)
            width = self.points_to_value(diameter)

        # ---- set x-shift to align card backs and fronts (frames)
        if is_card_back:
            # ---- alter right_gap for Hex odd row
            if kwargs["frame_type"] == CardFrame.HEXAGON and row & 1:  # odd row
                right_gap = right_gap - width
            move_x = right_gap - self.offset_x - globals.margins.left
        else:
            move_x = 0
        # feedback(f'$$$ {right_gap=} {self.offset_x=} {move_x=}')
        outline.draw(off_x=move_x, off_y=0, **shape_kwargs)  # inc. grid_marks

        # ---- track frame outlines for possible image extraction
        match kwargs["frame_type"]:
            case CardFrame.RECTANGLE:
                _vertices = outline.get_vertexes()  # clockwise from bottom-left
                base_frame_bbox = BBox(tl=_vertices[0], br=_vertices[2])
            case CardFrame.CIRCLE:
                base_frame_bbox = outline.bbox
            case CardFrame.HEXAGON:
                _vertices = outline.get_vertexes()  # anti-clockwise from mid-left
                # print(f"$$$ HEXAGON {_vertices=}")
                #   5__4
                #   /  \
                # 0/    \3
                #  \    /
                #  1\__/2
                base_frame_bbox = BBox(
                    tl=Point(_vertices[0].x, _vertices[5].y),
                    br=Point(_vertices[3].x, _vertices[2].y),
                )
            case _:
                raise NotImplementedError(
                    f'Cannot handle card frame type: {kwargs["frame_type"]}'
                )
        frame_width = base_frame_bbox.br.x - base_frame_bbox.tl.x
        frame_height = base_frame_bbox.br.y - base_frame_bbox.tl.y
        # print(f"$$$ {base_frame_bbox.tl.x=}  {base_frame_bbox.tl.y=}")
        # print(f"$$$ {base_frame_bbox.br.x=}  {base_frame_bbox.br.y=}")

        # ---- grid marks
        kwargs["grid_marks"] = None  # reset so not used by elements on card

        # ---- card frame shift
        match kwargs["frame_type"]:
            case CardFrame.RECTANGLE | CardFrame.CIRCLE:
                if kwargs["grouping_cols"] == 1:
                    _dx = col * (outline.width + outline.spacing_x) + outline.offset_x
                else:
                    group_no = col // kwargs["grouping_cols"]
                    _dx = (
                        col * outline.width
                        + outline.offset_x
                        + outline.spacing_x * group_no
                    )
                if kwargs["grouping_rows"] == 1:
                    _dy = row * (outline.height + outline.spacing_y) + outline.offset_y

                else:
                    group_no = row // kwargs["grouping_rows"]
                    _dy = (
                        row * outline.height
                        + outline.offset_y
                        + outline.spacing_y * group_no
                    )
                # print(f"$$$ {col=} {outline.width=}  {group_no=} {_dx=}")
                # print(f"$$$ {row=} {outline.height=} {group_no=} {_dy=}")
            case CardFrame.HEXAGON:
                _dx = col * 2.0 * (side + outline.spacing_x) + outline.offset_x
                _dy = row * 2.0 * (half_flat + outline.spacing_y) + outline.offset_y
                if row & 1:  # odd row
                    if is_card_back:
                        _dx = _dx + side - outline.spacing_x
                        # print('HEX ODD BACK {_dx=}')
                    else:
                        _dx = _dx + side + outline.spacing_x
            case _:
                raise NotImplementedError(
                    f'Cannot handle card frame type: {kwargs["frame_type"]}'
                )

        # ---- set x-shift to align card backs and fronts (elements)
        if is_card_back:
            _dx = _dx + move_x

        # ---- track/update frame and store card fronts
        if not is_card_back:
            mx = self.unit(_dx or 0) + self._o.delta_x
            my = self.unit(_dy or 0) + self._o.delta_y
            # print(f"$$$ {mx=} {my=} {frame_width=} {frame_height=}")
            frame_bbox = BBox(
                tl=Point(mx, my), br=Point(mx + frame_width, my + frame_height)
            )
            page = kwargs.get("page_number", 0)
            if page not in globals.card_frames:
                globals.card_frames[page] = [frame_bbox]
            else:
                globals.card_frames[page].append(frame_bbox)

        # ---- draw card elements
        flat_elements = tools.flatten(self.elements)
        for index, flat_ele in enumerate(flat_elements):
            # ---- * replace image source placeholder
            if image and isinstance(flat_ele, ImageShape):
                if flat_ele.kwargs.get("source", "").lower() in ["*", "all"]:
                    flat_ele.source = image

            members = self.members or flat_ele.members
            # ---- * clear kwargs for drawing
            # (otherwise BaseShape self attributes already set are overwritten)
            dargs = {
                key: kwargs.get(key)
                for key in [
                    "dataset",
                    "frame_type",
                    "locale",
                    "_is_countersheet",
                    "page_number",
                    "grouping_cols",
                    "grouping_rows",
                    "deck_data",
                ]
            }
            kwargs = dargs
            try:
                # ---- * normal element
                iid = members.index(cid + 1)
                # convert Template into a string via render
                new_ele = self.handle_custom_values(flat_ele, cid)  # calculated values
                if isinstance(new_ele, (SequenceShape, RepeatShape)):
                    new_ele.deck_data = self.deck_data
                # feedback(f'$$$ CS draw_card $$$ {new_ele=} {kwargs=}')
                if isinstance(new_ele, TemplatingType):
                    card_value = self.deck_data[iid]
                    custom_value = new_ele.template.render(card_value)
                    new_eles = new_ele.function(custom_value) or []
                    for the_new_ele in new_eles:
                        try:
                            the_new_ele.draw(
                                cnv=cnv, off_x=_dx, off_y=_dy, ID=iid, **kwargs
                            )
                            cnv.commit()
                        except AttributeError as err:
                            feedback(
                                f"Unable to draw card #{cid + 1}.  Check that all"
                                f" elements created by '{new_ele.function.__name__}'"
                                " are shapes.",
                                True,
                            )
                else:
                    new_ele.draw(cnv=cnv, off_x=_dx, off_y=_dy, ID=iid, **kwargs)
                    cnv.commit()
            except AttributeError:
                # ---- * switch ... get a new element ... or not!?
                new_ele = (
                    flat_ele(cid=self.shape_id) if flat_ele else None
                )  # uses __call__ on Switch
                if new_ele:
                    flat_new_eles = tools.flatten(new_ele)
                    for flat_new_ele in flat_new_eles:
                        members = flat_new_ele.members or self.members
                        iid = members.index(cid + 1)
                        custom_new_ele = self.handle_custom_values(flat_new_ele, iid)
                        if isinstance(custom_new_ele, (SequenceShape, RepeatShape)):
                            custom_new_ele.deck_data = self.deck_data
                        # feedback(f'$$$ draw_card $$$ {custom_new_ele=}')
                        custom_new_ele.draw(
                            cnv=cnv, off_x=_dx, off_y=_dy, ID=iid, **kwargs
                        )
                        cnv.commit()

            except Exception as err:
                feedback(f"Unable to draw card #{cid + 1}. (Error:{err})", True)


class DeckOfCards:
    """
    Placeholder for the deck design; storing lists of CardShapes; allowing export
    """

    def __init__(self, canvas=None, **kwargs):
        self.cnv = canvas  # initial pymupdf Shape object (need one per Page)
        self.kwargs = kwargs
        # feedback(f'$$$ DeckShape KW=> {self.kwargs}')
        # ---- cards
        self.fronts = []  # container for CardShape objects for front of cards
        self.backs = []  # container for CardShape objects for back of cards
        if kwargs.get("_is_countersheet", False):
            default_items = 70
            default_height = DEFAULT_COUNTER_SIZE / globals.units
            default_width = DEFAULT_COUNTER_SIZE / globals.units
            default_radius = DEFAULT_COUNTER_RADIUS / globals.units
        else:
            default_items = DEFAULT_CARD_COUNT
            default_height = DEFAULT_CARD_HEIGHT / globals.units
            default_width = DEFAULT_CARD_WIDTH / globals.units
            default_radius = DEFAULT_CARD_RADIUS / globals.units
        self.counters = kwargs.get("counters", default_items)
        # ---- set card size
        self.cards = kwargs.get("cards", self.counters)  # default total number of cards
        card_size = kwargs.get("card_size", "")
        the_height, the_width, size = default_height, default_width, None
        size = tools.card_size(card_size)
        if size:
            the_height, the_width = size[1] / globals.units, size[0] / globals.units
        self.height = kwargs.get("height", the_height)  # OVERWRITE
        self.width = kwargs.get("width", the_width)  # OVERWRITE
        # print(f'$$$ {size=}, {self.width=}, {self.height}')
        self.kwargs["width"] = self.width  # used for create_cardshapes()
        self.kwargs["height"] = self.height  # used for create_cardshapes()
        self.radius = kwargs.get("radius", default_radius)  # OVERWRITE
        # ----- set card frame type
        self.frame = kwargs.get("frame", "rectangle")
        match self.frame:
            case "rectangle" | "r":
                self.frame_type = CardFrame.RECTANGLE
            case "circle" | "c":
                self.frame_type = CardFrame.CIRCLE
            case "hexagon" | "h":
                self.frame_type = CardFrame.HEXAGON
            case _:
                hint = " Try rectangle, hexagon, or circle."
                feedback(f"Unable to draw a {self.frame}-shaped card. {hint}", True)
        self.kwargs["frame_type"] = self.frame_type  # used for create_cardshapes()
        # ---- dataset (list of dicts)
        self.dataset = kwargs.get("dataset", None)
        self.set_dataset()  # globals override : dataset AND cards
        if self.dataset:
            self.cards = len(self.dataset)
        # ---- behaviour
        self.sequence = kwargs.get("sequence", [])  # e.g. "1-2" or "1-5,8,10"
        self.template = kwargs.get("template", None)
        self.copy = kwargs.get("copy", None)
        self.mask = kwargs.get("mask", None)
        if self.mask and not self.dataset:
            feedback('Cannot set "mask" for a Deck without any existing Data!', True)
        # ---- bleed
        self.bleed_fill = kwargs.get("bleed_fill", None)
        self.bleed_areas = kwargs.get("bleed_areas", [])
        # ---- user provided-rows and -columns
        self.card_rows = kwargs.get("rows", None)
        self.card_cols = kwargs.get("cols", kwargs.get("columns", None))
        # ---- data file
        self.data_file = kwargs.get("data", None)
        self.data_cols = kwargs.get("data_cols", None)
        self.data_rows = kwargs.get("data_rows", None)
        self.data_header = kwargs.get("data_header", True)
        # ---- images dir and filter
        self.images_front = kwargs.get("images", None)
        self.images_front_filter = kwargs.get("images_filter", None)
        self.images_front_list = []
        # ---- images dir and filter
        self.images_back = kwargs.get("images_back", None)
        self.images_back_filter = kwargs.get("images_back_filter", None)
        self.images_back_list = []
        # ---- card groupings
        self.grouping = tools.as_int(
            kwargs.get("grouping", 1), "grouping"
        )  # no. of cards in a set
        self.grouping_rows = tools.as_int(
            kwargs.get("grouping_rows", self.grouping), "grouping_rows"
        )
        self.grouping_cols = tools.as_int(
            kwargs.get("grouping_cols", self.grouping), "grouping_cols"
        )
        # ---- spacing and offset
        self.offset = tools.as_float(kwargs.get("offset", 0), "offset")
        self.offset_x = tools.as_float(kwargs.get("offset_x", self.offset), "offset_x")
        self.offset_y = tools.as_float(kwargs.get("offset_y", self.offset), "offset_y")
        self.spacing = tools.as_float(kwargs.get("spacing", 0), "spacing")
        self.spacing_x = tools.as_float(
            kwargs.get("spacing_x", self.spacing), "spacing_x"
        )
        self.spacing_y = tools.as_float(
            kwargs.get("spacing_y", self.spacing), "spacing_y"
        )
        # ---- gutter (put backs of Cards on same page)
        self.gutter = tools.as_float(kwargs.get("gutter", 0), "gutter")  # none if zero
        self.gutter_stroke = kwargs.get("gutter_stroke", None)
        self.gutter_stroke_width = kwargs.get("gutter_stroke_width", WIDTH)
        self.gutter_dotted = kwargs.get("gutter_dotted", None)
        self.gutter_layout = kwargs.get("gutter_layout", "portrait")
        self.show_backs = False
        # ---- export options
        self.export_cards = kwargs.get("export_cards", False)
        self.dpi = kwargs.get("dpi", None)
        self.directory = kwargs.get("directory", None)
        # ---- FINALLY...
        extra = globals.deck_settings.get("extra", 0)
        self.cards += extra
        log.debug("Card Counts: %s Settings: %s", self.cards, globals.deck_settings)
        # print(f'$$$ {self.cards=}, {globals.deck_settings=}')
        self.create_cardshapes(self.cards)

    def set_dataset(self):
        """Create deck dataset from globals dataset"""
        if globals.dataset_type in [
            DatasetType.DICT,
            DatasetType.FILE,
            DatasetType.MATRIX,
        ]:
            log.debug("globals.dataset_type: %s", globals.dataset_type)
            if len(globals.dataset) == 0:
                feedback("The provided data is empty or cannot be loaded!", True)
            else:
                # globals.deck.create(len(globals.dataset) + globals.extra)
                self.dataset = globals.dataset
        elif globals.dataset_type == DatasetType.IMAGE:
            # OVERWRITE total number of cards
            self.cards = len(globals.image_list)
        else:
            pass  # no Data created

    def create_cardshapes(self, cards: int = 0):
        """Create a Deck of CardShapes (fronts and backs), based on number of `cards`"""
        log.debug("Cards are: %s", self.sequence)
        # ---- create cardfronts
        log.debug("Deck Fronts => %s cards with kwargs: %s", cards, self.kwargs)
        for card in range(0, cards):
            _card = CardShape(**self.kwargs)
            _card.shape_id = card
            self.fronts.append(_card)
        # ---- create card backs
        log.debug("Deck Backs  => %s cards with kwargs: %s", cards, self.kwargs)
        for back in range(0, cards):
            _back = CardShape(**self.kwargs)
            _back.shape_id = back
            self.backs.append(_back)

    def draw_bleed(self, cnv, page_across: float, page_down: float):
        # ---- bleed area for page (default)
        if self.bleed_fill:
            rect = RectangleShape(
                canvas=cnv,
                width=page_across,
                height=page_down,
                x=0,
                y=0,
                fill_stroke=self.bleed_fill,
            )
            # print(f'$$$  {self.bleed_fill=} {page_across=}, {page_down=}')
            rect.draw()
        # ---- bleed areas (custom)
        # for area in self.bleed_areas:
        #     #print('$$$  BLEED AREA $$$ ', area)

    def export_cards_as_images(
        self,
        filename: str,
        directory: str,
        output: str = None,
        fformat: str = "png",
    ):
        """Save individual cards as PNG images using their frames."""
        if self.export_cards and globals.pargs.png:  # pargs.png should default to True
            support.pdf_cards_to_png(
                source=filename,
                output=output or filename,
                fformat=fformat,
                dpi=self.dpi,
                directory=directory or self.directory,
                card_frames=globals.card_frames,
                page_height=globals.page[1],
            )

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw all cards for a DeckOfCards.

        Kwargs:
            * cards - number of cards to draw
            * extra - number of extra cards to draw (beyond Data count)
            * copy - name of Data column used to set number of copies of a Card
            * image_list - list of image filenames
            * export_cards - if True, then export card as individual images
            * card_rows - maximum number of rows of cards on a page
            * card_cols - maximum number of columns of cards on a page
            * dpi - resolution for output PNG
            * directory - path to save output(s)
            # grid_marks=globals.deck_settings.get("grid_marks", None),

        Note:
            DeckOfCards draw() is called by Save() function.
        """

        def draw_the_cards(
            cnv,
            state: DeckPrintState,
            page_number: int = 0,
            front: bool = True,
            right_gap: float = 0.0,
        ) -> DeckPrintState:
            """Process a Page of Cards for front or back of a DeckOfCards

            Args:
                cnv: pymupdf Shape object (one per Page)
                state: track what is being printed on the page
                page_number: current
                front: if True, print CardShapes in `deck.fronts`
                right_gap: space left after the last card

            Returns:
                DeckPrintState at the end of a Page
            """
            # print(f'$$$  card_draw {page_number=}')
            start_card = state.card_number
            card_count = state.card_count
            if front:
                row, col = 0, 0
            else:
                row, col = 0, max_cols - 1  # draw left-to-right for back
            card_number = start_card

            for card_num in range(start_card, card_count):
                card_number = card_num

                if front:
                    # print(f"$$$ FRONT {card_num=} {self.fronts[card_num]=}")
                    card = self.fronts[card_num]
                    deck_length = len(self.fronts)
                else:
                    # print(f"$$$ BACK {card_num=} {self.backs[card_num]=}")
                    card = self.backs[card_num]
                    deck_length = len(self.backs)

                # set meta data for draw_card
                _locale = Locale(
                    col=col + 1,
                    row=row + 1,
                    id=f"{col + 1}:{row + 1}",
                    sequence=card_num + 1,
                )
                kwargs["locale"] = _locale._asdict()
                kwargs["grouping_cols"] = self.grouping_cols
                kwargs["grouping_rows"] = self.grouping_rows
                kwargs["page_number"] = page_number
                kwargs["right_gap"] = right_gap
                image = images[card_num] if images and card_num <= len(images) else None
                card.deck_data = self.dataset

                mask = False
                if self.mask:
                    _check = tools.eval_template(
                        self.mask, self.dataset[card_num], label="mask"
                    )
                    mask = tools.as_bool(_check, label="mask", allow_none=False)
                    if not isinstance(mask, bool):
                        feedback(
                            'The "mask" test must result in True or False value!', True
                        )
                if not mask:
                    # get number of copies
                    copies = 1
                    if card.kwargs.get("dataset") and self.copy:
                        _copies = card.deck_data[card_num].get(self.copy, None)
                        copies = (
                            tools.as_int(_copies, "copy property", allow_none=True) or 1
                        )

                    for i in range(state.copies_to_do, copies):
                        if not front:
                            kwargs["card_back"] = True  # de/activate grid marks & shift
                        else:
                            kwargs["card_back"] = False
                        card.draw_card(
                            cnv,
                            row=row,
                            col=col,
                            cid=card.shape_id,
                            image=image,
                            **kwargs,
                        )
                        if front:
                            col += 1
                            if col >= max_cols:
                                col = 0
                                row += 1
                            elif (
                                col == max_cols - 1
                                and row % 2
                                and card.kwargs.get("frame_type") == CardFrame.HEXAGON
                            ):
                                col = 0
                                row += 1
                            else:
                                pass
                        else:
                            # if row == 1 or row == 2: breakpoint()
                            col += -1
                            if col < 0:
                                col = max_cols - 1
                                row += 1
                            elif (
                                col == 0
                                and row % 2
                                and card.kwargs.get("frame_type") == CardFrame.HEXAGON
                            ):
                                col = max_cols - 1
                                row += 1
                            else:
                                pass
                        if row >= max_rows:
                            # print(f"$$$ {front} {card_num=} => {col=} {row=} // {max_cols=} {max_rows=}")
                            if front:
                                row, col = 0, 0
                            else:
                                row, col = 0, max_cols - 1
                            PageBreak(**kwargs)
                            cnv = globals.canvas  # new one from page break
                            self.draw_bleed(cnv, page_across, page_down)
                            # print(f"$$$ card_draw - RETURN FROM rows / {front=} : {card_number + 1}")
                            return cnv, DeckPrintState(
                                card_count=state.card_count,
                                card_number=card_number + 1,
                                copies_to_do=copies - i - 1,
                                start_x=0,
                            )

            # if card_num >= deck_length:
            PageBreak(**kwargs)
            cnv = globals.canvas  # new one from page break
            self.draw_bleed(cnv, page_across, page_down)
            # print(f"$$$ card_draw - RETURN FROM end  / {front=} : {card_number + 1}")
            return cnv, DeckPrintState(
                card_count=state.card_count,
                card_number=card_number + 1,
                copies_to_do=0,
                start_x=0,
            )

        # ---- primary layout settings for draw()
        cnv = cnv if cnv else globals.canvas
        # feedback(f'$$$ DeckShape.draw {cnv=} KW=> {kwargs}')
        log.debug("Deck cnv:%s type:%s", type(globals.canvas), type(cnv))
        kwargs = self.kwargs | kwargs
        images = kwargs.get("image_list", [])
        kwargs["frame_type"] = self.frame_type
        # ---- user-defined rows and cols
        max_rows = self.card_rows
        max_cols = self.card_cols
        # ---- other settings
        self.export_cards = kwargs.get("export_cards", False)
        self.dpi = kwargs.get("dpi", 300)
        prime_globals = None

        # ---- gutter-based settings (new doc)
        if self.gutter > 0:
            prime_globals = save_globals()
            globals_page = copy(globals.page)
            gutter = tools.as_float(kwargs.get("gutter", 0.0), "gutter")
            # ---- pymupdf: new file, doc, page, shape/canvas
            gutter_filename = os.path.join(globals.pargs.directory, "gutter.pdf")
            globals.filename = gutter_filename
            globals.document = pymupdf.open()  # pymupdf Document

            if self.gutter_layout:
                _gutter_layout = str(self.gutter_layout).lower()
                if _gutter_layout not in ["p", "portrait", "l", "landscape"]:
                    feedback(
                        f'The gutter_layout "{self.gutter_layout}" is not valid'
                        ' - use "portrait" or "landscape"'
                    )
            if _gutter_layout:  # in ['p', 'portrait']:
                if globals_page[0] > globals_page[1]:
                    width = globals_page[0]
                    height = globals_page[1] / 2
                    is_landscape = True
                else:
                    width = globals_page[1]
                    height = globals_page[0] / 2
                    is_landscape = False

            # WIP for landscape layout with TALL cards
            # height = globals_page[1] / 2
            # width = globals_page[0]
            # if globals_page[0] > globals_page[1]:
            #     is_landscape = True
            # else:
            #     is_landscape = False
            # print(f"$$$ {globals_page[0]=} {globals_page[1]=} {width=} {height=} ")

            globals.doc_page = globals.document.new_page(
                width=width, height=height
            )  # pymupdf Page
            # ---- new globals for gutter
            globals.page_width = width / globals.units
            globals.page_height = height / globals.units
            globals.page = (width, height)
            # print(f"$$$ {width=} {height=} {globals.page_width=} {globals.page_height=} ")
            # ---- BaseCanvas
            globals.base = BaseCanvas(
                globals.document, paper=globals.paper, defaults=None, kwargs=kwargs
            )
            globals.margins = PageMargins(
                margin=prime_globals.margins.margin,
                left=prime_globals.margins.left,
                right=prime_globals.margins.right,
                top=prime_globals.margins.top - gutter / 2.0,
                bottom=prime_globals.margins.bottom,
                debug=prime_globals.margins.debug,
            )
            cnv = globals.doc_page.new_shape()  # pymupdf Shape
            globals.canvas = cnv
            page_setup()  # draw margin/grid
            # ---- validate card fit
            vspace = globals.page_height - globals.margins.top - globals.margins.bottom
            if self.height + self.offset_y > vspace:
                feedback(
                    "Rotated cards cannot fit into the available space!"
                    " Reduce card height, or top/bottom margins, or offset from top.",
                    True,
                )

        # ---- calculate rows/cols based on page size and margins AND card size
        margin_left = (
            globals.margins.left
            if globals.margins.left is not None
            else globals.margins.margin
        )
        margin_bottom = (
            globals.margins.bottom
            if globals.margins.bottom is not None
            else globals.margins.margin
        )
        margin_right = (
            globals.margins.right
            if globals.margins.right is not None
            else globals.margins.margin
        )
        margin_top = (
            globals.margins.top
            if globals.margins.top is not None
            else globals.margins.margin
        )
        page_across = globals.page_width - margin_right - margin_left  # user units
        page_down = globals.page_height - margin_top - margin_bottom  # user units
        _height, _width, _radius = self.height, self.width, self.radius
        self.draw_bleed(cnv, page_across, page_down)

        # ---- deck settings
        col_space, row_space = 0.0, 0.0
        if self.fronts:
            _card = self.fronts[0]
        else:
            _card = self.backs[0]
        (
            _height,
            _width,
        ) = (
            _card.outline.height,
            _card.outline.width,
        )
        _radius = _card.outline.radius
        # print(f'$$$ _card: {_height=} {_width=} {_radius=}')

        # ---- space calcs for rows/cols
        # Note: units here are user-based
        if not max_rows:
            row_space = globals.page_height - margin_bottom - margin_top - self.offset_y
            if self.grouping_rows == 1:
                max_rows = int(
                    (row_space + self.spacing_y) / (float(_height) + self.spacing_y)
                )
            else:
                max_groups = int(
                    (row_space + self.spacing_y)
                    / (float(_height) * self.grouping_rows + self.spacing_y)
                )
                max_rows = max_groups * self.grouping_rows
        if not max_cols:
            col_space = globals.page_width - margin_left - margin_right - self.offset_x
            # print(f'$$$ {globals.page_width=} {margin_left=} {margin_right=} {self.offset_x=}')
            if self.grouping_cols == 1:
                max_cols = int(
                    (col_space + self.spacing_x) / (float(_width) + self.spacing_x)
                )
            else:
                max_groups = int(
                    (col_space + self.spacing_x)
                    / (float(_width) * self.grouping_cols + self.spacing_x)
                )
                max_cols = max_groups * self.grouping_cols
            # print(f'$$$ {col_space=} {self.spacing_x=} {_width=} {max_cols=}') # w = 6.9282?
        if self.grouping_cols == 1:
            effective_right = (
                max_cols * (_width + self.spacing_x)
                + globals.margins.left
                + self.offset_x
            )
        else:
            effective_right = (
                max_cols * _width
                + globals.margins.left
                + self.offset_x
                + (self.grouping_cols - 1) * self.spacing_x
            )

        # ---- gap-at-right (for card back shift)
        right_gap = globals.page_width - effective_right

        # print(f"$$$ {right_gap=} {globals.page_width=} {effective_right=}")
        # print(f"$$$ {self.grouping_cols=} {self.spacing_x=}")
        # print(f"$$$ {globals.page_width=} {_width=} {col_space=} {max_cols=}")
        # print(f"$$${globals.page_height=} {_height=} {row_space=} {max_rows=}")

        # ---- prep for card drawing
        page_number = -1
        state_front = DeckPrintState(
            card_count=len(self.fronts), card_number=0, copies_to_do=0, start_x=0
        )
        state_back = DeckPrintState(
            card_count=len(self.backs), card_number=0, copies_to_do=0, start_x=0
        )
        for back in self.backs:
            if back.elements:
                self.show_backs = True
                continue

        # ---- actually draw cards!
        while state_front.card_number < len(self.fronts):
            # print(f"\n$$$ FRONT {state_front.card_number=} $$$ ")
            page_number += 1  # for back-to-back OR no backs
            cnv, state_front = draw_the_cards(cnv, state_front, page_number, True, 0)
            if self.show_backs:
                # print(f"\n$$$ BACK  {state_back.card_number=} $$$ ")
                page_number += 1  # for back-to-back
                cnv, state_back = draw_the_cards(
                    cnv, state_back, page_number, False, right_gap
                )
        # ---- delete extra blank page at the end
        globals.document.delete_page(globals.page_count)

        # ---- reset to prime and load-in gutter pages
        if self.gutter > 0:
            # save gutter document
            gutterfile = os.path.join(globals.directory, globals.filename)
            globals.document.save(gutterfile)
            # export cards
            self.export_cards_as_images(
                filename=globals.filename,
                directory=globals.directory,
                output=prime_globals.filename,
            )  # default to PNG format
            # reset globals to current doc
            restore_globals(prime_globals)
            cnv = globals.canvas
            # open gutter document
            src = pymupdf.open(gutterfile)
            if is_landscape:
                # upper half page (r1: backs)
                r1 = muRect(0, 0, cnv.width, cnv.height / 2)
                r1_rotate = 180
                # lower half page (r2: fronts)
                r2 = r1 + (0, cnv.height / 2, 0, cnv.height / 2)
                r2_rotate = 0
            else:
                # left half page (r2: fronts)
                r2 = muRect(0, 0, cnv.width / 2, cnv.height)
                r2_rotate = -90
                # right half page (r1: backs)
                r1 = muRect(cnv.width / 2, 0, cnv.width, cnv.height)
                r1_rotate = 90
            # insert pages from gutter.pdf
            for page_number in range(0, src.page_count, 2):
                globals.doc_page.show_pdf_page(
                    r2, src, page_number, rotate=r2_rotate
                )  # fronts
                globals.doc_page.show_pdf_page(
                    r1, src, page_number + 1, rotate=r1_rotate
                )  # backs
                # ---- draw gutter line
                if self.gutter > 0:
                    if is_landscape:
                        pt1 = (0, globals.page[1] / 2.0)
                        pt2 = (globals.page[0], globals.page[1] / 2.0)
                    else:
                        pt1 = (globals.page[0] / 2.0, 0)
                        pt2 = (globals.page[0] / 2.0, globals.page[1])
                    globals.canvas.draw_line(pt1, pt2)
                    gwargs = {}  # kwargs
                    gwargs["stroke"] = self.gutter_stroke or tools.get_color("gray")
                    gwargs["stroke_width"] = self.gutter_stroke_width
                    gwargs["dotted"] = self.gutter_dotted
                    tools.set_canvas_props(cnv=globals.canvas, index=None, **gwargs)
                # if page_number < src.page_count / 2 - 1:
                PageBreak()
            # ---- delete extra blank page at the end
            globals.document.delete_page(globals.page_count)
            # ---- delete gutter PDF document
            os.remove(gutter_filename)
        else:
            pass

    def get(self, cid):
        """Return a card based on the internal ID"""
        for card in self.fronts:
            if card.shape_id == cid:
                return card
        return None

    def count(self):
        """Return number of cards in the deck"""
        return len(self.fronts)


# ---- page-related ====


def page_setup():
    """Set the page color and (optionally) show a dotted margin line and grid."""
    # ---- paper color
    _fill = tools.get_color(globals.page_fill)
    if _fill != tools.get_color("white"):
        globals.doc_page.draw_rect(
            (0, 0, globals.page[0], globals.page[1]), fill=_fill, color=None
        )
    # ---- debug margins
    if globals.margins.debug:
        # print(f'{globals.margins.left=} {globals.margins.right=}')
        stroke = tools.get_color(DEBUG_COLOR)
        globals.doc_page.draw_rect(
            (
                globals.margins.left * globals.units,
                globals.margins.top * globals.units,
                globals.page[0] - (globals.margins.right * globals.units),
                globals.page[1] - (globals.margins.bottom * globals.units),
            ),
            color=stroke,
            dashes="[1 2] 0",
        )
    # ---- page grid
    if globals.page_grid:
        stroke = tools.get_color(DEBUG_COLOR)
        grid_size = globals.page_grid * globals.units
        cols = int(globals.page[0] // grid_size)
        rows = int(globals.page[1] // grid_size)
        for col in range(1, cols + 1):
            globals.doc_page.draw_line(
                (col * grid_size, 0),
                (col * grid_size, globals.page[1]),
                color=stroke,
                width=0.1,
            )
        for row in range(1, rows + 1):
            globals.doc_page.draw_line(
                (0, row * grid_size),
                (globals.page[0], row * grid_size),
                color=stroke,
                width=0.1,
            )


def Create(**kwargs):
    """Initialisation of globals, page, margins, units and canvas.

    Kwargs:

    - paper (str): a paper size from either of the ISO series - A0 down to A8;
      or B6 down to B0 - or a USA type - letter, legal or elevenSeventeen; to
      change the page orientation to **landscape** append ``-l`` to the name.
    - paper_width (float): set specific paper width using the defined *units*
    - paper_height (float): set specific paper height using the defined *units*
      For example, ``"A3-l"`` is a landscape A3 paper size; default is ``A4``
    - filename (str): name of the output PDF file; by default this is the prefix
      name of the script, with a ``.pdf`` extension
    - fill (str): the page color; default is ``white``
    - units (str): can be ``cm`` (centimetres), ``in`` (inches), ``mm``
      (millimetres), or ``points``; default is ``cm``
    - margin (float): set the value for *all* margins using the defined *units*;
      default is ``1`` centimetre.
    - margin_top (float): set the top margin using the defined *units*
    - margin_bottom (float): set the bottom margin using the defined *units*
    - margin_left (float): set the left margin using the defined *units*
    - margin_right (float): set the the right margin using the defined *units*
    - margin_debug (bool): if True, show the margin as a dotted blue line
    - page_grid (float): if a valid float, draw a squared grid covering the paper
      of square size equal to the value
    - cached_fonts (bool): if True, will force reload of Font cache

    Notes:

    - Kwargs to override the default values of any of the various properties
      used for drawing Shapes can be set here as well, for example:
      ``font_size=18`` or ``stroke="red"``.
    - Will use argparse to process command-line keyword args
    - Allows shortcut creation of cards
    """
    global globals_set
    # ---- set and confirm globals
    globals.initialize()
    globals_set = True
    # ---- units
    _units = kwargs.get("units", globals.units)
    globals.units = support.to_units(_units)
    # ---- margins
    the_margin = kwargs.get("margin", DEFAULT_MARGIN_SIZE / globals.units)
    globals.margins = PageMargins(
        margin=the_margin,
        left=kwargs.get("margin_left", the_margin),
        top=kwargs.get("margin_top", the_margin),
        bottom=kwargs.get("margin_bottom", the_margin),
        right=kwargs.get("margin_right", the_margin),
        debug=kwargs.get("margin_debug", False),
    )
    # ---- cards
    _cards = kwargs.get("cards", 0)
    landscape = kwargs.get("landscape", False)
    kwargs = margins(**kwargs)
    defaults = kwargs.get("defaults", None)
    # ---- paper, page, page sizes, page color
    globals.paper = kwargs.get("paper", globals.paper)
    globals.page = pymupdf.paper_size(globals.paper)  # (width, height) in points
    # user overrides
    if kwargs.get("paper_width") or kwargs.get("paper_height"):
        _page_width = tools.as_float(kwargs.get("paper_width", 0), "paper_width")
        _page_height = tools.as_float(kwargs.get("paper_height", 0), "paper_height")
        _page_width_pt = (
            _page_width * globals.units if _page_width > 0 else globals.paper[0]
        )
        _page_height_pt = (
            _page_height * globals.units if _page_height > 0 else globals.paper[1]
        )
        globals.page = (_page_width_pt, _page_height_pt)
    globals.page_width = globals.page[0] / globals.units  # width in user units
    globals.page_height = globals.page[1] / globals.units  # height in user units
    globals.fill = tools.get_color(kwargs.get("fill", "white"))
    globals.page_grid = tools.as_float(kwargs.get("page_grid", 0), "page_grid")
    # ---- fonts
    base_fonts()
    globals.font_size = kwargs.get("font_size", 12)
    # ---- command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--directory", help="Specify output directory", default=""
    )
    # use: --no-png to skip PNG output during Save()
    parser.add_argument(
        "--png",
        help="Whether to create PNG during Save (default is True)",
        default=True,
        action=argparse.BooleanOptionalAction,
    )
    # use: --fonts to force Fonts recreation during Create()
    parser.add_argument(
        "-f",
        "--fonts",
        help="Force reloading of all available fonts at start (default is False)",
        default=False,
        action=argparse.BooleanOptionalAction,
    )
    # use: --no-warning to ignore WARNING:: messages
    parser.add_argument(
        "-nw",
        "--nowarning",
        help="Do NOT show any WARNING:: messages (default is False)",
        default=False,
        action=argparse.BooleanOptionalAction,
    )
    parser.add_argument(
        "-p", "--pages", help="Specify which pages to process", default=""
    )
    globals.pargs = parser.parse_args()
    # NB - pages does not work - see notes in PageBreak()
    if globals.pargs.pages:
        feedback("--pages is not yet an implemented feature - sorry!")
    # ---- filename and fallback
    _filename = kwargs.get("filename", "")
    if not _filename:
        basename = "test"
        # log.debug('basename: "%s" sys.argv[0]: "%s"', basename, sys.argv[0])
        if sys.argv[0]:
            basename = os.path.basename(sys.argv[0]).split(".")[0]
        else:
            if _cards:
                basename = "cards"
        _filename = f"{basename}.pdf"
    # ---- validate directory & set filename
    if globals.pargs.directory and not os.path.exists(globals.pargs.directory):
        feedback(
            f'Unable to find directory "{globals.pargs.directory}" for output.', True
        )
    globals.filename = os.path.join(globals.pargs.directory, _filename)
    # ---- pymupdf doc, page, shape/canvas
    globals.document = pymupdf.open()  # pymupdf.Document
    globals.doc_page = globals.document.new_page(
        width=globals.page[0], height=globals.page[1]
    )  # pymupdf Page
    globals.canvas = globals.doc_page.new_shape()  # pymupdf Shape
    # ---- BaseCanvas
    globals.base = BaseCanvas(
        globals.document, paper=globals.paper, defaults=defaults, kwargs=kwargs
    )
    page_setup()
    # ---- cards
    if _cards:
        Deck(canvas=globals.canvas, sequence=range(1, _cards + 1), **kwargs)  # deck var
    # ---- pickle font info for pymupdf
    globals.archive = Archive()
    globals.css = ""
    cached_fonts = tools.as_bool(kwargs.get("cached_fonts", True))
    if not cached_fonts or globals.pargs.fonts:
        cache_directory = Path(Path.home() / CACHE_DIRECTORY)
        fi = FontInterface(cache_directory=cache_directory)
        fi.load_font_families(cached=False)


def create(**kwargs):
    Create(**kwargs)


def Footer(**kwargs):
    validate_globals()

    kwargs["paper"] = globals.paper
    if not kwargs.get("font_size"):
        kwargs["font_size"] = globals.font_size
    globals.footer_draw = kwargs.get("draw", False)
    globals.footer = FooterShape(_object=None, canvas=globals.canvas, **kwargs)
    # footer.draw() - this is called via PageBreak()


def Header(**kwargs):
    validate_globals()
    pass


def PageBreak(**kwargs):
    validate_globals()

    globals.canvas.commit()  # add all drawings (to current pymupdf Shape/"canvas")
    globals.page_count += 1
    globals.doc_page = globals.document.new_page(
        width=globals.page[0], height=globals.page[1]
    )  # pymupdf Page
    globals.canvas = globals.doc_page.new_shape()  # pymupdf Shape/"canvas" for new Page
    page_setup()

    kwargs = margins(**kwargs)
    if kwargs.get("footer", globals.footer_draw):
        if globals.footer is None:
            kwargs["paper"] = globals.paper
            kwargs["font_size"] = globals.font_size
            globals.footer = FooterShape(_object=None, canvas=globals.canvas, **kwargs)
        globals.footer.draw(
            cnv=globals.canvas, ID=globals.page_count, text=None, **kwargs
        )


def page_break():
    PageBreak()


def Save(**kwargs):
    """Save the result of all commands to a PDF file.

    Kwargs:

    - output (str):can be set to:

      - ``png`` - to create one image file per page of the PDF; by default the
        names of the PNG files are derived using the PDF filename, with a dash (-)
        followed by the page number;
      - ``svg`` - to create one file per page of the PDF; by default the names
        of the SVG files are derived using the PDF filename, with a dash (-)
        followed by the page number;
      - ``gif`` - to create a GIF file composed of all the PNG pages (these will be
        removed after the file been created)
    - dpi (int): can be set to the dots-per-inch resolution required; by default
      this is ``300``
    - directory (str): export path for the PNG or SVG; if None then use the same
      one as the script
    - names (list): provide a list of names -- without an extension -- for the
      *output* files that will be created from the PDF;
      the first name corresponds to the first page, the second name to the second
      and so on.  Each will automatically get the correct extension added to it.
      If the term ``None`` is used in place of a name, then that page will **not**
      have an output file created for it.
    - framerate (float): the delay in seconds between each "page" of a GIF image; by
      default this is ``1`` second
    - cards (bool): if set to ``True`` will cause all the card fronts to be
      exported as PNG files;  the names of the files are derived using the PDF
      filename, with a dash (-) followed by the page number

    Notes:

    - Cards are saved by iterating through all the ``fronts`` and ``backs``
      in a DeckOfCards object
    """
    validate_globals()

    # ---- set local vars from kwargs
    dpi = support.to_int(kwargs.get("dpi", DEFAULT_DPI), "dpi")
    framerate = support.to_float(kwargs.get("framerate", 1), "framerate")
    names = kwargs.get("names", None)
    directory = kwargs.get("directory", None)
    cards = kwargs.get("cards", False)  # export individual cards as PNG
    output = kwargs.get("output", None)  # export document into this format e.g. SVG

    # ---- directory
    globals.directory = directory if directory else os.getcwd()
    if not os.path.exists(globals.directory):
        feedback(
            f'Cannot find the directory "{globals.directory}" - please create this first.',
            True,
        )

    # ---- draw Deck (and export cards)
    if globals.deck and len(globals.deck.fronts) >= 1:
        globals.deck.draw(
            cnv=globals.canvas,
            export_cards=cards,
            cards=globals.deck_settings.get("cards", DEFAULT_CARD_COUNT),
            copy=globals.deck_settings.get("copy", None),
            extra=globals.deck_settings.get("extra", 0),
            grid_marks=globals.deck_settings.get("grid_marks", None),
            image_list=globals.image_list,
            dpi=dpi,
            directory=globals.directory,
        )

    # ---- update current pymupdf Shape
    globals.canvas.commit()  # add all drawings (to current pymupdf Shape)

    # ---- save all Pages to file
    msg = "Please check folder exists and that you have access rights."
    output_filename = os.path.join(globals.directory, globals.filename)
    try:
        globals.document.subset_fonts(verbose=True)  # subset fonts to reduce file size
        globals.document.save(output_filename)
    except RuntimeError as err:
        feedback(f'Unable to save "{output_filename}" - {err} - {msg}', True)
    except FileNotFoundError as err:
        feedback(f'Unable to save "{output_filename}" - {err} - {msg}', True)
    except pymupdf.mupdf.FzErrorSystem as err:
        feedback(f'Unable to save "{output_filename}" - {err} - {msg}', True)

    # ---- export individual Cards (where only Card fronts exist)
    if globals.deck and len(globals.deck.fronts) >= 1:
        globals.deck.export_cards_as_images(
            filename=globals.filename, directory=globals.directory
        )

    # ---- save to PNG image(s) or SVG file(s)
    if output:
        match str(output).lower():
            case "png":
                fformat = ExportFormat.PNG
            case "svg":
                fformat = ExportFormat.SVG
            case "gif":
                fformat = ExportFormat.GIF
            case _:
                feedback(f'Unknown output format "{output}"', True)

    if output and globals.pargs.png:  # pargs.png should default to True
        support.pdf_export(
            globals.filename,
            fformat,
            dpi,
            names,
            globals.directory,
            framerate=framerate,
        )

    # ---- save cards to image(s)
    # MOVED TO DECK DRAW - because of use of intermediate pages for gutter-based layout


def save(**kwargs):
    Save(**kwargs)


def margins(**kwargs):
    """Add margins to a set of kwargs, if not present."""
    validate_globals()

    kwargs["margin"] = kwargs.get("margin", globals.margins.margin)
    kwargs["margin_left"] = kwargs.get("margin_left", globals.margins.left)
    kwargs["margin_top"] = kwargs.get("margin_top", globals.margins.top)
    kwargs["margin_bottom"] = kwargs.get("margin_bottom", globals.margins.bottom)
    kwargs["margin_right"] = kwargs.get("margin_right", globals.margins.right)
    return kwargs


def Font(name=None, **kwargs):
    validate_globals()
    _name = None
    _file = None
    if name:
        _name = builtin_font(name)
        if not _name:  # check for custom font
            cache_directory = Path(Path.home() / CACHE_DIRECTORY)
            fi = FontInterface(cache_directory=cache_directory)
            _name = fi.get_font_family(name)
            _file = fi.get_font_file(name)
            if not _name:
                feedback(
                    f'Cannot find or load a font named "{name}".'
                    f' Defaulting to "{DEFAULT_FONT}".',
                    False,
                    True,
                )
            else:
                font_path, css = fi.font_file_css(_name)
                globals.css += css
                globals.archive.add(font_path)
                _file = font_path

    globals.base.font_name = _name or DEFAULT_FONT
    globals.base.font_file = _file
    globals.base.font_size = kwargs.get("size", 12)
    globals.base.font_style = kwargs.get("style", None)
    globals.base.stroke = kwargs.get("stroke", "black")


# ---- various ====


def Version():
    feedback(f"Running protograf version {__version__}.")


def Feedback(msg):
    feedback(msg)


def Today(details: str = "datetime", style: str = "iso", formatted: str = None) -> str:
    """Return string-formatted current date / datetime in a pre-defined style

    Args:
        details (str): what part of the datetime to format
        style (str): usa, eur (european), or iso - default
        formatted (str): formatting string following Python conventions;
            https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
    """
    current = datetime.now()
    if formatted:
        try:
            return current.strftime(formatted)
        except Exception:
            feedback('Unable to use formatted value  "{formatted}".', True)
    try:
        sstyle = style.lower()
    except Exception:
        feedback('Unable to use style "{style}" - try "eur" or "usa".', True)

    if details == "date" and sstyle == "usa":
        return current.strftime(f"%B {current.day} %Y")  # USA
    if details == "date" and sstyle == "eur":
        return current.strftime("%Y-%m-%d")  # Europe
    if details == "datetime" and sstyle == "eur":
        return current.strftime("%Y-%m-%d %H:%m")  # Europe
    if details == "datetime" and sstyle == "usa":
        return current.strftime("%B %d %Y %I:%m%p")  # USA
    if details == "time" and sstyle == "eur":
        return current.strftime("%H:%m")  # Europe
    if details == "time" and sstyle == "usa":
        return current.strftime("%I:%m%p")  # USA
    if details == "time":
        return current.strftime("%H:%m:%S")  # iso

    if details == "year":
        return current.strftime("%Y")  # all
    if details == "month" and sstyle == "usa":
        return current.strftime("%B")  # USA
    if details == "month":
        return current.strftime("%m")  # eur
    if details == "day" and sstyle == "usa":
        return current.strftime(f"{current.day}")  # usa
    if details == "day":
        return current.strftime("%d")  # other

    return current.isoformat(timespec="seconds")  # ISO


def Random(end: int = 1, start: int = 0, decimals: int = 2):
    """Return a random number, in a range (`start` to `end`), rounded to `decimals`."""
    rrr = random.random() * end + start
    if decimals == 0:
        return int(rrr)
    return round(rrr, decimals)


# ---- cards ====


def Matrix(labels: list = None, data: list = None) -> list:
    """Return list of dicts; each element is a unique combo of all the items in `data`"""
    if data is None:
        return []
    combos = list(itertools.product(*data))
    # check labels
    data_length = len(combos[0])
    if labels == []:
        labels = [f"VALUE{item+1}" for item in range(0, data_length)]
    else:
        if len(labels) != data_length:
            feedback(
                "The number of labels must equal the number of combinations!", True
            )
    result = []
    for item in combos:
        entry = {}
        for key, value in enumerate(item):
            entry[labels[key]] = value
        result.append(entry)
    return result


def Card(sequence: object = None, *elements, **kwargs):
    """Add one or more elements to a card or cards.

    NOTE: A Card receives its `draw()` command via Save()!
    """

    def add_members_to_card(element):
        try:
            element.members = _cards  # track all related cards
            card.members = _cards
            card.elements.append(element)  # may be Group or Shape or Query
        except AttributeError:
            if isinstance(element, str):
                feedback(
                    f'Cannot use the string "{element}" for a Card or CardBack.', True
                )
            else:
                feedback(f'Cannot use "{element}" for a Card or CardBack.', True)

    kwargs = margins(**kwargs)
    if not globals.deck:
        feedback("The Deck() has not been defined or is incorrect.", True)
    if not sequence:
        feedback("The Card() needs to have a valid sequence defined.", True)
    _cards = []
    # int - single card
    try:
        _card = int(sequence)
        _cards = range(_card, _card + 1)
    except Exception:
        pass
    # string - either 'all'/'*'/'even'/'odd' .OR. a range: '1', '1-2', '1-3,5-6'
    if not _cards:
        try:
            card_count = (
                len(globals.dataset)
                if globals.dataset
                else (
                    len(globals.deck.images_front_list)
                    if globals.deck.images_front_list
                    else (
                        tools.as_int(globals.deck.cards, "cards")
                        if globals.deck.cards
                        else 0
                    )
                )
            )
            if isinstance(sequence, list) and not isinstance(sequence, str):
                _cards = sequence
            elif sequence.lower() == "all" or sequence.lower() == "*":
                _cards = list(range(1, card_count + 1))
            elif sequence.lower() == "odd" or sequence.lower() == "o":
                _cards = list(range(1, card_count + 1, 2))
            elif sequence.lower() == "even" or sequence.lower() == "e":
                _cards = list(range(2, card_count + 1, 2))
            else:
                _cards = tools.sequence_split(sequence)
        except Exception as err:
            log.error(
                "Handling sequence:%s with dataset:%s & images:%s - %s",
                sequence,
                globals.dataset,
                globals.deck.images_front_list,
                err,
            )
            feedback(
                f'Unable to convert "{sequence}" into a card or range of cards {globals.deck}.'
            )
    for index, _card in enumerate(_cards):
        card = globals.deck.fronts[_card - 1]  # cards internally number from ZERO
        if card:
            for element in elements:
                # print(f'$$$  Card() {element=} {type(element)=}')
                if isinstance(element, TemplatingType):
                    add_members_to_card(element)
                else:
                    # element.members = _cards  # track all related cards
                    # card.members = _cards
                    # card.elements.append(element)  # may be Group or Shape or Query
                    add_members_to_card(element)
        else:
            feedback(f'Cannot find card#{_card}. (Check "cards" setting in Deck)')


def CardBack(sequence: object = None, *elements, **kwargs):
    """Add one or more elements to the back of a card or cards.

    NOTE: A CardBack receives its `draw()` command via Save()!
    """

    def add_members_to_back(element):
        element.members = _cardbacks  # track all related cards
        cardback.members = _cardbacks
        cardback.elements.append(element)  # may be Group or Shape or Query

    kwargs = margins(**kwargs)
    if not globals.deck:
        feedback("The Deck() has not been defined or is incorrect.", True)
    if not sequence:
        feedback("The Card() needs to have a valid sequence defined.", True)

    _cardbacks = []
    # int - single card
    try:
        _back = int(sequence)
        _cardbacks = range(_back, _back + 1)
    except Exception:
        pass
    # string - either 'all'/'*'/'even'/'odd' .OR. a range: '1', '1-2', '1-3,5-6'
    if not _cardbacks:
        try:
            cardback_count = (
                len(globals.dataset)
                if globals.dataset
                else (
                    len(globals.deck.images_back_list)
                    if globals.deck.images_back_list
                    else (
                        tools.as_int(globals.deck.cards, "cards")
                        if globals.deck.cards
                        else 0
                    )
                )
            )
            if isinstance(sequence, list) and not isinstance(sequence, str):
                _cardbacks = sequence
            elif sequence.lower() == "all" or sequence.lower() == "*":
                _cardbacks = list(range(1, cardback_count + 1))
            elif sequence.lower() == "odd" or sequence.lower() == "o":
                _cardbacks = list(range(1, cardback_count + 1, 2))
            elif sequence.lower() == "even" or sequence.lower() == "e":
                _cardbacks = list(range(2, cardback_count + 1, 2))
            else:
                _cardbacks = tools.sequence_split(sequence)
        except Exception as err:
            log.error(
                "Handling sequence:%s with dataset:%s & images:%s - %s",
                sequence,
                globals.dataset,
                globals.deck.images_back_list,
                err,
            )
            feedback(
                f'Unable to convert "{sequence}" into a cardback or range of cardbacks {globals.deck}.'
            )
    for index, _back in enumerate(_cardbacks):
        if _back - 1 >= len(globals.deck.backs):
            feedback("Number of CardBacks cannot exceed number of Cards!", True)
        cardback = globals.deck.backs[_back - 1]  # cards internally number from ZERO
        if cardback:
            for element in elements:
                # print(f'$$$  CardBack() {element=} {type(element)=}')
                if isinstance(element, TemplatingType):
                    add_members_to_back(element)
                else:
                    # element.members = _cardbacks  # track all related cards
                    # cardback.members = _cardbacks
                    # cardback.elements.append(element)  # may be Group or Shape or Query
                    add_members_to_back(element)
        else:
            feedback(f'Cannot find cardback#{_back}. (Check "cards" setting in Deck)')


def Counter(sequence, *elements, **kwargs):
    """Add one or more elements to a counter or counters.

    NOTE: A Counter receives its `draw()` command via Save()!
    """
    Card(sequence, *elements, **kwargs)


def CounterBack(sequence, *elements, **kwargs):
    """Add one or more elements to a counter or counters.

    NOTE: A CounterBack receives its `draw()` command via Save()!
    """
    CardBack(sequence, *elements, **kwargs)


def Deck(**kwargs):
    """Placeholder for a deck design; storing lists of CardShapes; allowing export

    Kwargs (optional):

    - bleed_fill: background color for the page (up to the margins);
      if no separate **fill** property is set, then this color is used instead
    - cards: the number of cards appearing in the deck; defaults to 9
      Note that other objects such as Data() and Matrix() can alter this value
    - card_size: a pre-existing card size used to set *width* and *height*
      (if values for *width* and *height* are set, they will override this);
      can be one of: ``poker``, ``bridge``, ``tarot``, ``business``, ``mini``,
      ``skat``, ``mini``, ``minieuropean``, ``miniamerican``
    - cols: maximum number of card columns that should appear on a page
    - copy: the name of a column in the dataset defined by Data() that
      specifies how many copies of a card are needed
    - fill: color of the card's area; defaults to ``white``
    - frame: the default card frame is a *rectangle* (or square, if the
      height and width match); but can be set to *hexagon* or *circle*
    - grid_marks: if set to ``True``, will cause small marks to be drawn at
      the border of the page that align with the edges of the card frames
    - grid_marks_length: the length of the *grid_marks*; defaults to ``0.85`` cm
    - grid_marks_stroke: line color of the *grid_marks*; defaults to ``grey``
    - grid_marks_stroke_width: line width of the *grid_marks*; defaults to 0.1
    - grouping: number of cards to be drawn adjacent to each other
      before a blank space is added by the **spacing** property (note that
      **grouping** does not apply to  *hexagon* **frame** cards)
      (about one-third of an inch)
    - grouping_col: number of cards to be drawn adjacent to each other
      in a horizontal direction before a blank space is added by the **spacing**
    - grouping_row: number of cards to be drawn adjacent to each other
      in a vertical direction before a blank space is added by the **spacing**
    - gutter: a value set for this helps determines the spacing between the
      fronts and backs of cards when these are drawn on two halves of the same
      page; its value is divided in half, and added to the top margin value, and
      each set of cards is drawn that distance away from the centre line of the page
    - gutter_stroke: if set, will cause a line of that color to be used
      for the *gutter* line; this defaults to ``gray`` (to match grid marks)
    - gutter_stroke_width: if set to a value, will cause a line of that
      thickness to be used for the *gutter* line
    - gutter_dotted: sets the style of the *gutter* line
    - gutter_layout: sets the orientation of the page for the cards drawn in
      the two gutter "halves"; this can be ``portrait`` (the default) or
      ``landscape``` (the latter is useful when you have very tall cards e.g.
      ``tarot`` sized ones)
    - height: card height for a *rectangular* card; defaults to 8.89 cm
    - mask: an expression which should evaluate to ``True`` or ``False``.
      This expression has the same kind of syntax as T() and it uses data available
      from the Deck object's Data(). If the expression result is ``True``
      then any matching cards will be masked i.e. ignored and not drawn
    - radius: radius for a card of type *hexagon* or *circle*; defaults to 2.54 cm
    - rounding: size of rounding on each corner of a rectangular frame card
    - rows: maximum number of card rows that should appear on a page
    - spacing: size of blank space between each card or grouping in x- and y-direction
    - spacing_x: size of blank space between each card or grouping in a
      horizontal direction
    - spacing_y: size of blank space between each card or grouping in a
      vertical direction
    - stroke: color of the card's border; defaults to ``black``
    - width: card width for a *rectangular* card; defaults to ``6.35`` cm

    Notes:

    - This function instantiates a DeckOfCards object; this object:

        - receives its `draw()` command from Save()
        - draws any gutter lines (one per page)
        - adds any annotations (depending on page ranges)
    """
    validate_globals()

    kwargs = margins(**kwargs)
    kwargs["dataset"] = globals.dataset
    globals.deck = DeckOfCards(canvas=globals.canvas, **kwargs)
    globals.deck_settings["grid_marks"] = kwargs.get("grid_marks", None)


def CounterSheet(**kwargs):
    """Initialise a countersheet with all its settings, including source(s) of data.

    NOTE: A CounterSheet (aka Deck) receives its `draw()` command from Save()!
    """
    kwargs["_is_countersheet"] = True
    Deck(**kwargs)


def group(*args, **kwargs):

    gb = GroupBase(kwargs)
    for arg in args:
        gb.append(arg)
    return gb


# ---- data and functions ====


def Data(**kwargs):
    """Load data from file, dictionary, list-of-lists, directory or Google Sheet.

    Kwargs:

    - filename (str): the full path to the name (including extension) of the
      CSV or Excel file being used; if no directory is supplied in the path,
      then it is assumed to be the same one in which the script is located
    - Access to a **Google Sheet** document is via three properties:

      - *google_key* - an API key that you must request from Google
      - *google_sheet* - the unique ID (a mix of numbers and letters) which is
        randomly assigned by Google to your Google Sheet
      - *google_name* - the name of the tab in the Google Sheet housing your data
    - matrix (str): refers to the name assigned to the ``Matrix`` being used
    - images (str): refers to the directory in which the cards' images are located;
      if a full path is not given, its assumed to be directly under the one in which
      the script is located
    - images_list (list): is used in conjunction with *images* to provide a list of
      file extensions that filter which type of files will be loaded from the
      directory e.g. ``.png`` or ``.jpg``; this is important to set if the
      directory contains files of a type that are not, or cannot be, used
    - data_list (str): refers to the name assigned to the "list of lists" being used;
      this property is also used when linked to data being sourced from the
      BoardGameGeek API
    - extra (int): if additional cards need to be manually created for a Deck,
      that are *not* part of the data source, then the number of those cards
      can be specified here.
    """
    validate_globals()

    filename = kwargs.get("filename", None)  # CSV or Excel
    matrix = kwargs.get("matrix", None)  # Matrix()
    data_list = kwargs.get("data_list", None)  # list-of-lists
    images = kwargs.get("images", None)  # directory
    images_filter = kwargs.get("images_filter", "")  # e.g. .png
    filters = tools.sequence_split(images_filter, False, True)
    source = kwargs.get("source", None)  # dict
    google_sheet = kwargs.get("google_sheet", None)  # Google Sheet
    debug = kwargs.get("debug", False)
    # extra cards added to deck (handle special cases not in the dataset)
    globals.deck_settings["extra"] = tools.as_int(kwargs.get("extra", 0), "extra")
    try:
        int(globals.deck_settings["extra"])
    except Exception:
        feedback(f'Extra must be a whole number, not "{kwargs.get("extra")}"!', True)

    if filename:  # handle excel and CSV
        globals.dataset = tools.load_data(filename, **kwargs)
        globals.dataset_type = DatasetType.FILE
    elif google_sheet:  # handle Google Sheet
        google_key = kwargs.get("google_key", None)
        google_name = kwargs.get("google_name", None)
        globals.dataset = tools.load_googlesheet(
            google_sheet, api_key=google_key, name=google_name
        )
        globals.dataset_type = DatasetType.GSHEET
        if not globals.dataset:
            feedback("No data accessible from the Google Sheet - please check", True)
    elif matrix:  # handle pre-built dict
        globals.dataset = matrix
        globals.dataset_type = DatasetType.MATRIX
    elif data_list:  # handle list-of-lists
        try:
            keys = data_list[0]  # get keys from first sub-list
            dict_list = [dict(zip(keys, values)) for values in data_list[1:]]
            globals.dataset = dict_list
            globals.dataset_type = DatasetType.DICT
        except Exception:
            feedback("The data_list is not valid - please check", True)
    elif source:  # handle pre-built list-of-dict
        if not isinstance(source, list):
            source_type = type(source)
            feedback(
                f"The source must be a list-of-dictionaries, not {source_type}", True
            )
        if not isinstance(source[0], dict):
            sub_type = type(source)
            feedback(f"The list must contain dictionaries, not {sub_type}", True)
        globals.dataset = source
        globals.dataset_type = DatasetType.DICT
    elif images:  # create list of images
        src = Path(images)
        if not src.is_dir():
            # look relative to script's location
            script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
            full_path = os.path.join(script_dir, images)
            src = Path(full_path)
            if not src.is_dir():
                feedback(
                    f"Cannot locate or access directory: {images} or {full_path}", True
                )
        for child in src.iterdir():
            if not filters or child.suffix in filters:
                globals.image_list.append(str(child))
        if globals.image_list is None or len(globals.image_list) == 0:
            feedback(
                f'Directory "{src}" has no relevant files or cannot be loaded!', True
            )
        else:
            globals.dataset_type = DatasetType.IMAGE
    else:
        feedback("You must provide data for the Data command!", True)

    # ---- check keys - cannot use spaces!
    if globals.dataset and len(globals.dataset) > 0:
        first = globals.dataset[0].keys()
        for key in first:
            if not (key.isalpha() or "_" in key):
                feedback(
                    "The Data headers must only be characters (without spaces)"
                    f' e.g. not "{key}"',
                    True,
                )
    if debug:
        if len(globals.dataset) > 0:
            headers = ",".join([*globals.dataset[0]])
            print(f"Initial rows of {globals.dataset_type} data are:")
            print(headers)
            for i in range(0, 3):
                if len(globals.dataset) >= i:
                    _data = list(globals.dataset[i].values())
                    data = ",".join(str(x) for x in _data)
                    print(data)
        else:
            print("No {globals.dataset_type} data was loaded!")

    return globals.dataset


def S(test="", result=None, alternate=None):
    """
    Enable Selection of data from a dataset list

        test: str
            boolean-type Jinja2 expression which can be evaluated to return True/False
            e.g. {{ NAME == 'fred' }} gets the column "NAME" value from the dataset
            and tests its equivalence to the value "fred"
        result: str or element
            returned if `test` evaluates to True
        alternate: str or element
            OPTIONAL; returned if `test` evaluates to False; if not supplied, then None
    """

    if globals.dataset and isinstance(globals.dataset, list):
        environment = jinja2.Environment()
        template = environment.from_string(str(test))
        return Switch(
            template=template,
            result=result,
            alternate=alternate,
            dataset=globals.dataset,
        )
    return None


def L(lookup: str, target: str, result: str, default: Any = "") -> LookupType:
    """Enable Lookup of data in a record of a dataset

        lookup: str
            the lookup column whose value must be used for the match ("source" record)
        target: str
            the name of the column of the data being searched ("target" record)
        result: str
            name of result column containing the data to be returned ("target" record)
        default: Any
            the data to be returned if NO match is made

    In short:
        lookup and target enable finding a matching record in the dataset;
        the data in the 'result' column of that record is stored as an
        `lookup: result` entry in the returned lookups dictionary of the LookupType
    """
    lookups = {}
    if globals.dataset and isinstance(globals.dataset, list):
        # validate the lookup column
        if lookup not in globals.dataset[0].keys():
            feedback(f'The "{lookup}" column is not available.', True)
        for key, record in enumerate(globals.dataset):
            if target in record.keys():
                if result in record.keys():
                    lookups[record[target]] = record[result]
                else:
                    feedback(f'The "{result}" column is not available.', True)
            else:
                feedback(f'The "{target}" column is not available.', True)
    result = LookupType(column=lookup, lookups=lookups)
    return result


def T(string: str, data: dict = None, function: object = None):
    """Use string to create a Jinja2 Template."""
    # print(f'$$$  TEMPLATE {string=} {data=}')
    environment = jinja2.Environment()
    try:
        template = environment.from_string(str(string))
    except jinja2.exceptions.TemplateSyntaxError as err:
        template = None
        feedback(f'Invalid template "{string}" - {err}', True)
    # members can assigned when processing cards
    return TemplatingType(template=template, function=function, members=None)


def Set(_object, **kwargs):
    """Overwrite one or more properties for a Shape/object with new value(s)"""
    for kw in kwargs.keys():
        log.debug("Set: %s %s %s", kw, kwargs[kw], type(kwargs[kw]))
        setattr(_object, kw, kwargs[kw])
    return _object


# ---- shapes ====


def base_shape(source=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["source"] = source
    bshape = BaseShape(canvas=globals.canvas, **kwargs)
    return bshape


def Common(source=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["source"] = source
    cshape = CommonShape(canvas=globals.canvas, **kwargs)
    return cshape


def common(source=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["source"] = source
    cshape = CommonShape(canvas=globals.canvas, **kwargs)
    return cshape


def Image(source=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["source"] = source
    image = ImageShape(canvas=globals.canvas, **kwargs)
    image.draw()
    return image


def image(source=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["source"] = source
    return ImageShape(canvas=globals.canvas, **kwargs)


def Arc(**kwargs):
    kwargs = margins(**kwargs)
    arc = ArcShape(canvas=globals.canvas, **kwargs)
    arc.draw()
    return arc


def arc(**kwargs):
    kwargs = margins(**kwargs)
    return ArcShape(canvas=globals.canvas, **kwargs)


def Arrow(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    arr = arrow(row=row, col=col, **kwargs)
    arr.draw()
    return arr


def arrow(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return ArrowShape(canvas=globals.canvas, **kwargs)


def Bezier(**kwargs):
    kwargs = margins(**kwargs)
    bezier = BezierShape(canvas=globals.canvas, **kwargs)
    bezier.draw()
    return bezier


def bezier(**kwargs):
    kwargs = margins(**kwargs)
    return BezierShape(canvas=globals.canvas, **kwargs)


def Chord(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    chd = chord(row=row, col=col, **kwargs)
    chd.draw()
    return chd


def chord(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return ChordShape(canvas=globals.canvas, **kwargs)


def Circle(**kwargs):
    kwargs = margins(**kwargs)
    circle = CircleShape(canvas=globals.canvas, **kwargs)
    circle.draw()
    return circle


def circle(**kwargs):
    kwargs = margins(**kwargs)
    return CircleShape(canvas=globals.canvas, **kwargs)


def Compass(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    cmpss = compass(row=row, col=col, **kwargs)
    cmpss.draw()
    return cmpss


def compass(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    return CompassShape(canvas=globals.canvas, **kwargs)


def Dot(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    dtt = dot(row=row, col=col, **kwargs)
    dtt.draw()
    return dtt


def dot(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    return DotShape(canvas=globals.canvas, **kwargs)


def Ellipse(**kwargs):
    kwargs = margins(**kwargs)
    ellipse = EllipseShape(canvas=globals.canvas, **kwargs)
    ellipse.draw()
    return ellipse


def ellipse(**kwargs):
    kwargs = margins(**kwargs)
    return EllipseShape(canvas=globals.canvas, **kwargs)


def EquilateralTriangle(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    eqt = EquilateralTriangleShape(canvas=globals.canvas, **kwargs)
    eqt.draw()
    return eqt


def equilateraltriangle(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    return EquilateralTriangleShape(canvas=globals.canvas, **kwargs)


def Hexagon(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    # print(f'$$$ Will draw HexShape: {kwargs}')
    kwargs["row"] = row
    kwargs["col"] = col
    hexagon = HexShape(canvas=globals.canvas, **kwargs)
    hexagon.draw()
    return hexagon


def hexagon(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return HexShape(canvas=globals.canvas, **kwargs)


def Line(row=None, col=None, **kwargs):
    """Draw a Line shape on the canvas.

    Kwargs:

    - angle (float): the number of degrees clockwise from the baseline; used in
      conjunction with *length*
    - cx and cy (floats): if set, will replace the use of *x* and *y* for the
      starting point, and work in conjunction with *angle* and *length* to
      create the line around a centre point
    - dotted (bool): if ``True``, create a series of small lines i.e. the
      "dots", followed by gaps, of sizes equal to the line's *stroke_width*
    - dashed (list): a list of two floats: the first is the length of the dash;
      the second is the length of the space between each dash
    - length (float): sets the specific size of the line; used in conjunction
      with *angle* (which defaults to 0 |deg|)
    - rounded (bool): if ``True``, draw small semicircles at the ends of the line
    - stroke (float): the color of the line
    - stroke_width (str): the thickness of the line, in points
    - x1 and y1 (floats): a fixed endpoint for the line end (if not calculated by
      *angle* and *length*)

    Arrow-related Kwargs:

    - arrow (bool): if set to ``True`` will cause a default arrow to be drawn
    - arrow_style (str): can be set to ``notch``, ``angle``, or ``spear`` to change
      the default shape of the arrow
    - arrow_fill (str): set the color of the arrow, which otherwise defaults to the
      color of the line
    - arrow_stroke (str): set the color of the arrow with style ``angle``, which
      otherwise defaults to the color of the line
    - arrow_width (float): set the width of the arrow at its base,  which otherwise
      defaults to a multiple of the line width
    - arrow_height (float): set the height of the arrow, which otherwise
      defaults to a value proportional to the arrow *width* (specifically, the
      height of the equilateral triangle used for the default arrow style)
    - arrow_position (float|list): set a value (single number), or values (list of
      numbers), that represents the fractional distance along the line at which the
      arrow tip, or tips, must be positioned relative to the start of the line
    - arrow_double (bool): if True, make a copy of the same arrow, with the same properties as
      above, but facing in the opposite direction

    """
    kwargs = margins(**kwargs)
    lin = line(row=row, col=col, **kwargs)
    lin.draw()
    return lin


def line(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return LineShape(canvas=globals.canvas, **kwargs)


def Polygon(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    poly = polygon(row=row, col=col, **kwargs)
    poly.draw()
    return poly


def polygon(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return PolygonShape(canvas=globals.canvas, **kwargs)


def Polyline(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    polylin = polyline(row=row, col=col, **kwargs)
    polylin.draw()
    return polylin


def polyline(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return PolylineShape(canvas=globals.canvas, **kwargs)


def RightAngledTriangle(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    rat = RightAngledTriangleShape(canvas=globals.canvas, **kwargs)
    rat.draw()
    return rat


def rightangledtriangle(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    return RightAngledTriangleShape(canvas=globals.canvas, **kwargs)


def Rhombus(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    rhomb = rhombus(row=row, col=col, **kwargs)
    rhomb.draw()
    return rhomb


def rhombus(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    return RhombusShape(canvas=globals.canvas, **kwargs)


def Rectangle(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    rect = rectangle(row=row, col=col, **kwargs)
    rect.draw()
    return rect


def rectangle(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return RectangleShape(canvas=globals.canvas, **kwargs)


def Polyshape(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    shapeshape = polyshape(row=row, col=col, **kwargs)
    shapeshape.draw()
    return shapeshape


def polyshape(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return ShapeShape(canvas=globals.canvas, **kwargs)


def QRCode(source=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["source"] = source
    image = QRCodeShape(canvas=globals.canvas, **kwargs)
    image.draw()
    return image


def qrcode(source=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["source"] = source
    return QRCodeShape(canvas=globals.canvas, **kwargs)


def Sector(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    sct = sector(row=row, col=col, **kwargs)
    sct.draw()
    return sct


def sector(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return SectorShape(canvas=globals.canvas, **kwargs)


def Square(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    sqr = square(row=row, col=col, **kwargs)
    sqr.draw()
    return sqr


def square(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return SquareShape(canvas=globals.canvas, **kwargs)


def Stadium(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    std = StadiumShape(canvas=globals.canvas, **kwargs)
    std.draw()
    return std


def stadium(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return StadiumShape(canvas=globals.canvas, **kwargs)


def Star(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    star = StarShape(canvas=globals.canvas, **kwargs)
    star.draw()
    return star


def star(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return StarShape(canvas=globals.canvas, **kwargs)


def StarField(**kwargs):
    kwargs = margins(**kwargs)
    starfield = StarFieldShape(canvas=globals.canvas, **kwargs)
    starfield.draw()
    return starfield


def starfield(**kwargs):
    kwargs = margins(**kwargs)
    return StarFieldShape(canvas=globals.canvas, **kwargs)


def Text(**kwargs):
    kwargs = margins(**kwargs)
    text = TextShape(canvas=globals.canvas, **kwargs)
    text.draw()
    return text


def text(*args, **kwargs):
    kwargs = margins(**kwargs)
    _obj = args[0] if args else None
    return TextShape(_object=_obj, canvas=globals.canvas, **kwargs)


def Trapezoid(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    trp = trapezoid(row=row, col=col, **kwargs)
    trp.draw()
    return trp


def trapezoid(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return TrapezoidShape(canvas=globals.canvas, **kwargs)


# ---- grids ====


def DotGrid(**kwargs):
    kwargs = margins(**kwargs)
    # override defaults ... otherwise grid not "next" to margins
    kwargs["x"] = kwargs.get("x", 0)
    kwargs["y"] = kwargs.get("y", 0)
    dgrd = DotGridShape(canvas=globals.canvas, **kwargs)
    dgrd.draw()
    return dgrd


def Grid(**kwargs):
    kwargs = margins(**kwargs)
    # override defaults ... otherwise grid not "next" to margins
    kwargs["x"] = kwargs.get("x", 0)
    kwargs["y"] = kwargs.get("y", 0)
    grid = GridShape(canvas=globals.canvas, **kwargs)
    grid.draw()
    return grid


def Blueprint(**kwargs):
    """Draw a grid extending between page margins.

    Kwargs:

    - subdivisions (int): a number indicating how many lines should be drawn
      within each square; these are evenly spaces; use *subdivisions_dashed*
      to enhance these lines
    - style (str): set to one of: *blue*, *green* or *grey*
    - decimals (float): set to to an integer number for the decimal points which
      are used for the grid numbers (default is ``0``)
    - edges (str): can be set to any combination of *n*, *s*, *e*, or *w* in a
      single comma-delimited string; grid numbers will then be drawn on
      any of the edges specified
    - edges_y (float): the number set for this determines where a horizontal line
      of grid numbers will be drawn
    - edges_x (float): the number set for this determines where a vertical line
      of grid numbers will be drawn

    """

    def set_style(style_name):
        """Set Blueprint color and fill."""
        match style_name:
            case "green":
                color, fill = "#CECE2C", "#35705E"
            case "grey" | "gray":
                color, fill = "white", "#A1969C"
            case "blue" | "invert" | "inverted":
                color, fill = "honeydew", "#3085AC"
            case _:
                color, fill = "#3085AC", None
                if style_name is not None:
                    feedback(
                        f'The Blueprint style "{style_name}" is unknown', False, True
                    )
        return color, fill

    def set_format(num, side):
        return f"{num*side:{1}.{decimals}f}"

    kwargs = margins(**kwargs)
    if kwargs.get("common"):
        feedback('The "common" property cannot be used with a Blueprint.', True)
    kwargs["units"] = kwargs.get("units", globals.units)
    side = 1.0
    if kwargs["units"] == unit.inch:
        side = 0.5
    decimals = tools.as_int(kwargs.get("decimals", 0), "Blueprint decimals")
    # override defaults ... otherwise grid not "next" to margins
    numbering = kwargs.get("numbering", True)
    kwargs["side"] = kwargs.get("side", side)
    number_edges = kwargs.get("edges", "S,W")
    kwargs["x"] = kwargs.get("x", 0)
    kwargs["y"] = kwargs.get("y", 0)
    m_x = kwargs["units"] * (globals.margins.left + globals.margins.right)
    m_y = kwargs["units"] * (globals.margins.top + globals.margins.bottom)
    _cols = (globals.page[0] - m_x) / (kwargs["units"] * float(kwargs["side"]))
    _rows = (globals.page[1] - m_y) / (kwargs["units"] * float(kwargs["side"]))
    rows = int(_rows)
    cols = int(_cols)
    kwargs["rows"] = kwargs.get("rows", rows)
    kwargs["cols"] = kwargs.get("cols", cols)
    kwargs["stroke_width"] = kwargs.get("stroke_width", 0.2)  # fine line
    default_font_size = 10 * math.sqrt(globals.page[0]) / math.sqrt(globals.page[1])
    dotted = kwargs.get("dotted", False)
    kwargs["font_size"] = kwargs.get("font_size", default_font_size)
    line_stroke, page_fill = set_style(kwargs.get("style", None))
    kwargs["stroke"] = kwargs.get("stroke", line_stroke)
    kwargs["fill"] = kwargs.get("fill", page_fill)
    # ---- page color (optional)
    if kwargs["fill"] is not None:
        fill = tools.get_color(kwargs.get("fill", "white"))
        globals.canvas.draw_rect((0, 0, globals.page[0], globals.page[1]))
        globals.canvas.finish(fill=fill)
    kwargs["fill"] = kwargs.get("fill", line_stroke)  # revert back for font
    # ---- number edges
    if number_edges:
        edges = tools.validated_directions(
            number_edges, DirectionGroup.CARDINAL, "blueprint edges"
        )
    else:
        edges = []
    # ---- numbering
    if numbering:
        _common = Common(
            font_size=kwargs["font_size"],
            stroke=kwargs["stroke"],
            fill=kwargs["stroke"],
            units=kwargs["units"],
        )
        offset = _common.points_to_value(kwargs["font_size"]) / 2.0
        offset_edge = _common.points_to_value(kwargs["font_size"]) * 1.25
        # ---- * absolute?
        fixed_y, fixed_x = None, None
        edges_x = kwargs.get("edges_x", None)
        if edges_x:
            fixed_x = tools.as_float(edges_x, "edges_x")
        edges_y = kwargs.get("edges_y", None)
        if edges_y:
            fixed_y = tools.as_float(edges_y, "edges_y")
        if fixed_x:
            for y in range(1, kwargs["rows"] + 1):
                Text(
                    x=fixed_x,
                    y=y * side + offset,
                    text=set_format(y, side),
                    common=_common,
                )
        if fixed_y:
            for x in range(1, kwargs["cols"] + 1):
                Text(
                    x=x * side,
                    y=fixed_y + offset,
                    text=set_format(x, side),
                    common=_common,
                )

        # ---- * relative
        if "n" in edges:
            for x in range(1, kwargs["cols"] + 1):
                Text(
                    x=x * side,
                    y=kwargs["y"] - offset,
                    text=set_format(x, side),
                    common=_common,
                )
        if "s" in edges:
            for x in range(1, kwargs["cols"] + 1):
                Text(
                    x=x * side,
                    y=kwargs["y"] + kwargs["rows"] * side + offset_edge,
                    text=set_format(x, side),
                    common=_common,
                )
        if "e" in edges:
            for y in range(1, kwargs["rows"] + 1):
                Text(
                    x=kwargs["x"] + kwargs["cols"] * side + globals.margins.left / 2.0,
                    y=y * side + offset,
                    text=set_format(y, side),
                    common=_common,
                )
        if "w" in edges:
            for y in range(1, kwargs["rows"] + 1):
                Text(
                    x=kwargs["x"] - globals.margins.left / 2.0,
                    y=y * side + offset,
                    text=set_format(y, side),
                    common=_common,
                )
        # ---- draw "zero" number
        # z_x = kwargs["units"] * globals.margins.left
        # z_y = kwargs["units"] * globals.margins.bottom
        # corner_dist = geoms.length_of_line(Point(0, 0), Point(z_x, z_y))
        # corner_frac = corner_dist * 0.66 / kwargs["units"]
        # # feedback(f'$$$  {z_x=} {z_y=} {corner_dist=}')
        # zero_pt = geoms.point_on_line(Point(0, 0), Point(z_x, z_y), corner_frac)
        # Text(
        #     x=zero_pt.x / kwargs["units"] - kwargs["side"] / 4.0,
        #     y=zero_pt.y / kwargs["units"] - kwargs["side"] / 4.0,
        #     text="0",
        #     common=_common,
        # )

    # ---- draw subgrid
    if kwargs.get("subdivisions"):
        local_kwargs = copy(kwargs)
        sub_count = int(kwargs.get("subdivisions"))
        local_kwargs["side"] = float(side / sub_count)
        local_kwargs["rows"] = sub_count * kwargs["rows"]
        local_kwargs["cols"] = sub_count * kwargs["cols"]
        local_kwargs["stroke_width"] = kwargs.get("stroke_width") / 2.0
        local_kwargs["stroke"] = kwargs.get("subdivisions_stroke", kwargs["stroke"])
        local_kwargs["dashed"] = kwargs.get("subdivisions_dashed", None)
        local_kwargs["dotted"] = kwargs.get("subdivisions_dotted", True)
        if local_kwargs["dashed"]:
            local_kwargs["dotted"] = False
        subgrid = GridShape(canvas=globals.canvas, **local_kwargs)
        subgrid.draw(cnv=globals.canvas)

    # ---- draw Blueprint grid
    grid = GridShape(
        canvas=globals.canvas, dotted=dotted, **kwargs
    )  # don't add canvas as arg here!
    grid.draw(cnv=globals.canvas)
    return grid


# ---- connect ====


def Connect(shape_from, shape_to, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["shape_from"] = shape_from
    kwargs["shape_to"] = shape_to
    connect = ConnectShape(canvas=globals.canvas, **kwargs)
    connect.draw(cnv=globals.canvas)
    return connect


def connect(shape_from, shape_to, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["shape_from"] = shape_from
    kwargs["shape_to"] = shape_to
    return ConnectShape(canvas=globals.canvas, **kwargs)


# ---- repeats ====


def Repeat(shapes=None, **kwargs):
    """Draw multiple copies of a Shape across rows and columns."""
    kwargs = margins(**kwargs)
    kwargs["shapes"] = shapes
    repeat = RepeatShape(**kwargs)
    repeat.draw()


def repeat(shapes=None, **kwargs):
    kwargs = margins(**kwargs)
    return RepeatShape(shapes=shapes, **kwargs)


def Lines(rows=1, cols=1, **kwargs):
    kwargs = margins(**kwargs)
    for row in range(rows):
        for col in range(cols):
            Line(row=row, col=col, **kwargs)


# ---- sequence ====


def Sequence(shapes=None, **kwargs):
    """Draw a list of Shapes in a line."""
    kwargs = margins(**kwargs)
    kwargs["shapes"] = shapes
    sequence = SequenceShape(**kwargs)
    sequence.draw()


def sequence(shapes=None, **kwargs):
    """Draw a list of Shapes in a line."""
    return SequenceShape(shapes=shapes, **kwargs)


# ---- patterns (grid) ====


def Hexagons(rows=1, cols=1, sides=None, **kwargs):
    """Draw a set of hexagons in a pattern."""
    kwargs = kwargs
    locales = []  # list of Locale namedtuples
    if kwargs.get("hidden"):
        hidden = tools.integer_pairs(kwargs.get("hidden"), "hidden")
    else:
        hidden = None

    def draw_hexagons(
        rows: int, cols: int, stop: int, the_cols: list, odd_mid: bool = True
    ):
        """Draw rows of hexagons for each column in `the_cols`"""
        sequence = 0
        top_row = 0
        end_row = rows - 1
        if not odd_mid:
            end_row = rows
            top_row = 1
        for ccol in the_cols:
            top_row = top_row + 1 if ccol & 1 != 0 else top_row  # odd col
            end_row = end_row - 1 if ccol & 1 == 0 else end_row  # even col
            # print('ccol, top_row, end_row', ccol, top_row, end_row)
            for row in range(top_row - 1, end_row + 1):
                _row = row + 1
                # feedback(f'{ccol=}, {_row=}')
                if hidden and (_row, ccol) in hidden:
                    pass
                else:
                    hxgn = hexagon(
                        row=row, col=ccol - 1, hex_rows=rows, hex_cols=cols, **kwargs
                    )
                    hxgn.draw()
                    _locale = Locale(
                        col=ccol - 1,
                        row=row,
                        x=hxgn.grid.x,
                        y=hxgn.grid.y,
                        id=f"{ccol - 1}:{row}",
                        sequence=sequence,
                        label=hxgn.grid.label,
                    )
                    # print(f'$$$ locale {ccol=} {_row=} / {hxgn.grid.x=} {hxgn.grid.y=}')
                    locales.append(_locale)
                    sequence += 1

            if ccol - 1 == stop:  # reached "leftmost" -> reset counters
                top_row = 1
                end_row = rows - 1
        return locales

    if kwargs.get("hex_layout") and kwargs.get("orientation"):
        if kwargs.get("orientation").lower() in ["p", "pointy"] and kwargs.get(
            "hex_layout"
        ) not in ["r", "rec", "rect", "rectangle"]:
            feedback(
                "Cannot use this Hexagons `hex_layout` with pointy hexagons!", True
            )

    if kwargs.get("hex_layout") in ["c", "cir", "circle"]:
        if not sides and (
            (rows is not None and rows < 3) and (cols is not None and cols < 3)
        ):
            feedback("The minimum values for rows/cols is 3!", True)
        if rows and rows > 1:
            cols = rows
        if cols and cols > 1:
            rows = cols
        if rows != cols:
            rows = cols
        if sides:
            if sides < 2:
                feedback("The minimum value for sides is 2!", True)
            rows = 2 * sides - 1
            cols = rows
        else:
            if rows & 1 == 0:
                feedback("An odd number is needed for rows!", True)
            if cols & 1 == 0:
                feedback("An odd number is needed for cols!", True)
            sides = rows // 2 + 1
        odd_mid = False if sides & 1 == 0 else True
        the_cols = list(range(sides, 0, -1)) + list(range(sides + 1, rows + 1))
        locales = draw_hexagons(rows, cols, 0, the_cols, odd_mid=odd_mid)

    elif kwargs.get("hex_layout") in ["d", "dia", "diamond"]:
        cols = rows * 2 - 1
        the_cols = list(range(rows, 0, -1)) + list(range(rows + 1, cols + 1))
        locales = draw_hexagons(rows, cols, 0, the_cols)

    elif kwargs.get("hex_layout") in ["t", "tri", "triangle"]:
        feedback(f"Cannot draw triangle-pattern hexagons: {kwargs}", True)

    elif kwargs.get("hex_layout") in ["l", "loz", "stadium"]:
        feedback(f"Cannot draw stadium-pattern hexagons: {kwargs}", True)

    else:  # default to rectangular layout
        sequence = 0
        for row in range(rows):
            for col in range(cols):
                if hidden and (row + 1, col + 1) in hidden:
                    pass
                else:
                    hxgn = Hexagon(
                        row=row, col=col, hex_rows=rows, hex_cols=cols, **kwargs
                    )
                    _locale = Locale(
                        col=col,
                        row=row,
                        x=hxgn.grid.x,
                        y=hxgn.grid.y,
                        id=f"{col}:{row}",
                        sequence=sequence,
                        label=hxgn.grid.label,
                    )
                    # print(f'$$$ locale {col=} {row=} / {hxgn.grid.x=} {hxgn.grid.y=}')
                    locales.append(_locale)
                    sequence += 1

    return locales


def Rectangles(rows=1, cols=1, **kwargs):
    """Draw a set of rectangles in a pattern."""
    kwargs = kwargs
    locales = []  # list of Locale namedtuples
    if kwargs.get("hidden"):
        hidden = tools.integer_pairs(kwargs.get("hidden"), "hidden")
    else:
        hidden = None

    counter = 0
    sequence = 0
    for row in range(rows):
        for col in range(cols):
            counter += 1
            if hidden and (row + 1, col + 1) in hidden:
                pass
            else:
                rect = rectangle(row=row, col=col, **kwargs)
                _locale = Locale(
                    col=col,
                    row=row,
                    x=rect.x,
                    y=rect.y,
                    id=f"{col}:{row}",
                    sequence=sequence,
                    label=rect.label,
                )
                kwargs["locale"] = _locale._asdict()
                # Note: Rectangle.calculate_xy() uses the row&col to get y&x
                Rectangle(row=row, col=col, **kwargs)
                locales.append(_locale)
                sequence += 1

    return locales


def Squares(rows=1, cols=1, **kwargs):
    """Draw a set of squares in a pattern."""
    kwargs = kwargs
    locations = []
    if kwargs.get("hidden"):
        hidden = tools.integer_pairs(kwargs.get("hidden"), "hidden")
    else:
        hidden = None

    for row in range(rows):
        for col in range(cols):
            if hidden and (row + 1, col + 1) in hidden:
                pass
            else:
                square = Square(row=row, col=col, **kwargs)
                locations.append(square.grid)

    return locations


def Location(grid: list, label: str, shapes: list, **kwargs):
    kwargs = kwargs

    def test_foo(x: bool = True, **kwargs):
        print("--- test only ---", kwargs)

    def draw_shape(shape: BaseShape, point: Point, locale: Locale):
        shape_name = shape.__class__.__name__
        shape_abbr = shape_name.replace("Shape", "")
        # shape._debug(cnv.canvas, point=loc)
        dx = shape.kwargs.get("dx", 0)  # user-units
        dy = shape.kwargs.get("dy", 0)  # user-units
        pts = shape.values_to_points([dx, dy])  # absolute units (points)
        try:
            x = point.x + pts[0]
            y = point.y + pts[1]
            kwargs["locale"] = locale
            # feedback(f"$$$ {shape=} :: {loc.x=}, {loc.y=} // {dx=}, {dy=}")
            # feedback(f"$$$ {kwargs=}")
            # feedback(f"$$$ {label} :: {shape_name=}")
            if shape_name in GRID_SHAPES_WITH_CENTRE:
                shape.draw(_abs_cx=x, _abs_cy=y, **kwargs)
            elif shape_name in GRID_SHAPES_NO_CENTRE:
                shape.draw(_abs_x=x, _abs_y=y, **kwargs)
            else:
                feedback(f"Unable to draw {shape_abbr}s in Location!", True)
        except Exception as err:
            feedback(err, False)
            feedback(
                f"Unable to draw the '{shape_abbr}' - please check its settings!", True
            )

    # checks
    if grid is None or not isinstance(grid, list):
        feedback("The grid (as a list) must be supplied!", True)

    # get location centre from grid via the label
    locale, point = None, None
    for _locale in grid:
        if _locale.label.lower() == str(label).lower():
            point = Point(_locale.x, _locale.y)
            locale = _locale
            break
    if point is None:
        msg = ""
        if label and "," in label:
            msg = " (Did you mean to use Locations?)"
        feedback(f"The Location '{label}' is not in the grid!{msg}", True)

    if shapes:
        try:
            iter(shapes)
        except TypeError:
            feedback("The Location shapes property must contain a list!", True)
        for shape in shapes:
            if shape.__class__.__name__ == "GroupBase":
                feedback(f"Group drawing ({shape}) NOT IMPLEMENTED YET", True)
            else:
                draw_shape(shape, point, locale)


def Locations(grid: list, labels: Union[str, list], shapes: list, **kwargs):
    kwargs = kwargs

    if grid is None or not isinstance(grid, list):
        feedback("The grid (as a list) must be supplied!", True)
    if labels is None:
        feedback("No grid location labels supplied!", True)
    if shapes is None:
        feedback("No list of shapes supplied!", True)
    if isinstance(labels, str):
        _labels = [_label.strip() for _label in labels.split(",")]
        if labels.lower() == "all" or labels.lower() == "*":
            _labels = []
            for loc in grid:
                if isinstance(loc, Locale):
                    _labels.append(loc.label)
    elif isinstance(labels, list):
        _labels = labels
    else:
        feedback(
            "Grid location labels must be a list or a comma-delimited string!", True
        )

    if not isinstance(shapes, list):
        feedback("Shapes must contain a list of shapes!", True)

    for label in _labels:
        # feedback(f'{label=} :: {shapes=}')
        Location(grid, label, shapes)


def LinkLine(grid: list, locations: Union[list, str], **kwargs):
    """Enable a line link between one or more locations in a grid."""
    kwargs = kwargs
    if isinstance(locations, str):  # should be a comma-delimited string
        locations = tools.sequence_split(locations, False, False)
    if not isinstance(locations, list):
        feedback(f"'{locations} is not a list - please check!", True)
    if len(locations) < 2:
        feedback("There should be at least 2 locations to create links!", True)
    dummy = base_shape()  # a BaseShape - not drawable!
    for index, location in enumerate(locations):
        # precheck
        if isinstance(location, str):
            location = (location, 0, 0)  # reformat into standard notation
        if not isinstance(location, tuple) or len(location) != 3:
            feedback(
                f"The location '{location}' is not valid -- please check its syntax!",
                True,
            )
        # get location centre from grid via the label
        loc = None
        try:
            iter(grid)
        except TypeError:
            feedback(f"The grid '{grid}' is not valid - please check it!", True)
        for position in grid:
            if not isinstance(position, Locale):
                feedback(f"The grid '{grid}' is not valid - please check it!", True)
            if location[0] == position.label:
                loc = Point(position.x, position.y)
                break
        if loc is None:
            feedback(f"The location '{location[0]}' is not in the grid!", True)
        # new line?
        if index + 1 < len(locations):
            # location #2
            location_2 = locations[index + 1]
            if isinstance(location_2, str):
                location_2 = (location_2, 0, 0)  # reformat into standard notation
            if not isinstance(location_2, tuple) or len(location_2) != 3:
                feedback(
                    f"The location '{location_2}' is not valid - please check its syntax!",
                    True,
                )
            loc_2 = None
            for position in grid:
                if location_2[0] == position.label:
                    loc_2 = Point(position.x, position.y)
                    break
            if loc_2 is None:
                feedback(f"The location '{location_2[0]}' is not in the grid!", True)
            if location == location_2:
                feedback(
                    "Locations must differ from each other - "
                    f"({location} matches {location_2})!",
                    True,
                )
            # line start/end
            x = dummy.points_to_value(loc.x) + location[1]
            y = dummy.points_to_value(loc.y) + location[2]
            x1 = dummy.points_to_value(loc_2.x) + location_2[1]
            y1 = dummy.points_to_value(loc_2.y) + location_2[2]

            _line = line(x=x, y=y, x1=x1, y1=y1, **kwargs)
            # feedback(f"$$$ {x=}, {y=}, {x1=}, {y1=}")
            delta_x = globals.margins.left
            delta_y = globals.margins.top
            # feedback(f"$$$ {delta_x=}, {delta_y=}")
            _line.draw(
                off_x=-delta_x,
                off_y=-delta_y,
            )


# ---- layout & tracks ====


def Layout(grid, **kwargs):
    """Determine locations for cols&rows in a virtual layout and draw shape(s)"""
    validate_globals()

    kwargs = kwargs
    shapes = kwargs.get("shapes", [])  # shapes or Places
    locations = kwargs.get("locations", [])
    corners = kwargs.get("corners", [])  # shapes or Places for corners only!
    rotations = kwargs.get("rotations", [])  # rotations for an edge
    if kwargs.get("masked") and isinstance(kwargs.get("masked"), str):
        masked = tools.sequence_split(kwargs.get("masked"), "masked")
    else:
        masked = kwargs.get("masked", [])
    if kwargs.get("visible") and isinstance(kwargs.get("visible"), str):
        visible = tools.integer_pairs(kwargs.get("visible"), "visible")
    else:
        visible = kwargs.get("visible", [])

    # ---- validate inputs
    if not shapes:
        feedback("There is no list of shapes to draw!", False, True)
    if shapes and not isinstance(shapes, list):
        feedback("The values for 'shapes' must be in a list!", True)
    if not isinstance(grid, VirtualLocations):
        feedback(f"The grid value '{grid}' is not valid!", True)
    corners_dict = {}
    if corners:
        if not isinstance(corners, list):
            feedback(f"The corners value '{corners}' is not a valid list!", True)
        for corner in corners:
            try:
                value = corner[0]
                shape = corner[1]
                if value.lower() not in ["nw", "ne", "sw", "se", "*"]:
                    feedback(
                        f'The corner must be one of nw, ne, sw, se (not "{value}")!',
                        True,
                    )
                if not isinstance(shape, BaseShape):
                    feedback(f'The corner item must be a shape (not "{shape}") !', True)
                if value == "*":
                    corners_dict["nw"] = shape
                    corners_dict["ne"] = shape
                    corners_dict["sw"] = shape
                    corners_dict["se"] = shape
                else:
                    corners_dict[value] = shape
            except Exception:
                feedback(f'The corners setting "{corner}" is not a valid list', True)

    # ---- setup locations; automatically or via user-specification
    shape_id = 0
    default_locations = enumerate(grid.next_locale())
    if not locations:
        _locations = default_locations
    else:
        _locations = []
        user_locations = tools.integer_pairs(locations, label="locations")
        # restructure and pick locations according to user input
        for key, user_loc in enumerate(user_locations):
            for loc in default_locations:
                if user_loc[0] == loc[1].col and user_loc[1] == loc[1].row:
                    new_loc = (
                        key,
                        Locale(
                            col=loc[1].col,
                            row=loc[1].row,
                            x=loc[1].x,
                            y=loc[1].y,
                            id=f"{loc[1].col}:{loc[1].row}",  # ,loc[1].id,
                            sequence=key,
                            corner=loc[1].corner,
                        ),
                    )
                    _locations.append(new_loc)
            default_locations = enumerate(grid.next_locale())  # regenerate !

    # ---- generate rotations - keyed per sequence number
    rotation_sequence = {}
    if rotations:
        for rotation in rotations:
            if not isinstance(rotation, tuple):
                feedback("The 'rotations' must each contain a set!", True)
            if len(rotation) != 2:
                feedback("The 'rotations' must each contain a set of two items!", True)
            _key = rotation[0]
            if not isinstance(_key, str):
                feedback(
                    "The first value for rreach 'rotations' entry must be a string!",
                    True,
                )
            rotate = tools.as_float(
                rotation[1], " second value for the 'rotations' entry"
            )
            try:
                _keys = list(tools.sequence_split(_key))
            except Exception:
                feedback(f'Unable to convert "{_key}" into a range of values.')
            for the_key in _keys:
                rotation_sequence[the_key] = rotate

    # ---- iterate through locations & draw shape(s)
    for count, loc in _locations:
        if masked and count + 1 in masked:  # ignore if IN masked
            continue
        if visible and count + 1 not in visible:  # ignore if NOT in visible
            continue
        if grid.stop and count + 1 >= grid.stop:
            break
        if grid.pattern in ["o", "outer"]:
            if count + 1 > grid.rows * 2 + (grid.cols - 2) * 2:
                break
        if shapes:
            # ---- * extract shape data
            rotation = rotation_sequence.get(count + 1, 0)  # default rotation
            if isinstance(shapes[shape_id], BaseShape):
                _shape = shapes[shape_id]
            elif isinstance(shapes[shape_id], tuple):
                _shape = shapes[shape_id][0]
                if not isinstance(_shape, BaseShape):
                    feedback(
                        f'The first item in "{shapes[shape_id]}" must be a shape!', True
                    )
                if len(shapes[shape_id]) > 1:
                    rotation = tools.as_float(shapes[shape_id][1], "rotation")
            elif isinstance(shapes[shape_id], Place):
                _shape = shapes[shape_id].shape
                if not isinstance(_shape, BaseShape):
                    feedback(
                        f'The value for "{shapes[shape_id].name}" must be a shape!',
                        True,
                    )
                if shapes[shape_id].rotation:
                    rotation = tools.as_float(shapes[shape_id].rotation, "rotation")
            else:
                feedback(
                    f'Use a shape, or set, or Place - not "{shapes[shape_id]}"!', True
                )
            # ---- * overwrite shape to use for corner
            if corners_dict:
                if loc.corner in corners_dict.keys():
                    _shape = corners_dict[loc.corner]

            # ---- * set shape to enable overwrite/change of properties
            shape = copy(_shape)

            # ---- * execute shape.draw()
            cx = loc.x * shape.units + shape._o.delta_x
            cy = loc.y * shape.units + shape._o.delta_y
            locale = Locale(
                col=loc.col,
                row=loc.row,
                x=loc.x,
                y=loc.y,
                id=f"{loc.col}:{loc.row}",
                sequence=loc.sequence,
            )
            _locale = locale._asdict()
            shape.draw(_abs_cx=cx, _abs_cy=cy, rotation=rotation, locale=_locale)
            shape_id += 1
        if shape_id > len(shapes) - 1:
            shape_id = 0  # reset and start again
        # ---- display debug
        do_debug = kwargs.get("debug", None)
        if do_debug:
            match str(do_debug).lower():
                case "normal" | "none" | "null" | "n":
                    Dot(x=loc.x, y=loc.y, stroke=DEBUG_COLOR, fill=DEBUG_COLOR)
                case "id" | "i":
                    Dot(
                        x=loc.x,
                        y=loc.y,
                        label=loc.id,
                        stroke=DEBUG_COLOR,
                        fill=DEBUG_COLOR,
                    )
                case "sequence" | "s":
                    Dot(
                        x=loc.x,
                        y=loc.y,
                        label=f"{loc.sequence}",
                        stroke=DEBUG_COLOR,
                        fill=DEBUG_COLOR,
                    )
                case "xy" | "xy":
                    Dot(
                        x=loc.x,
                        y=loc.y,
                        label=f"{loc.x},{loc.y}",
                        stroke=DEBUG_COLOR,
                        fill=DEBUG_COLOR,
                    )
                case "yx" | "yx":
                    Dot(
                        x=loc.x,
                        y=loc.y,
                        label=f"{loc.y},{loc.x}",
                        stroke=DEBUG_COLOR,
                        fill=DEBUG_COLOR,
                    )
                case "colrow" | "cr":
                    Dot(
                        x=loc.x,
                        y=loc.y,
                        label=f"{loc.col},{loc.row}",
                        stroke=DEBUG_COLOR,
                        fill=DEBUG_COLOR,
                    )
                case "rowcol" | "rc":
                    Dot(
                        x=loc.x,
                        y=loc.y,
                        label=f"{loc.row},{loc.col}",
                        stroke=DEBUG_COLOR,
                        fill=DEBUG_COLOR,
                    )
                case _:
                    feedback(f'Unknown debug style "{do_debug}"', True)


def Track(track=None, **kwargs):

    def format_label(shape, data):
        # ---- supply data to text fields
        try:
            shape.label = shapes[shape_id].label.format(**data)  # replace {xyz} entries
            shape.title = shapes[shape_id].title.format(**data)
            shape.heading = shapes[shape_id].heading.format(**data)
        except KeyError as err:
            text = str(err).split()
            feedback(
                f"You cannot use {text[0]} as a special field; remove the {{ }} brackets",
                True,
            )

    validate_globals()

    kwargs = kwargs
    angles = kwargs.get("angles", [])
    rotation_style = kwargs.get("rotation_style", None)
    clockwise = tools.as_bool(kwargs.get("clockwise", None))
    stop = tools.as_int(kwargs.get("stop", None), "stop", allow_none=True)
    start = tools.as_int(kwargs.get("start", None), "start", allow_none=True)
    sequences = kwargs.get("sequences", [])  # which sequence positions to show

    # ---- check kwargs inputs
    if sequences and isinstance(sequences, str):
        sequences = tools.sequence_split(sequences)
    if sequences and stop:
        feedback("Both stop and sequences cannot be used together for a Track!", True)
    if not track:
        track = Polygon(sides=4, fill=None)
    track_name = track.__class__.__name__
    track_abbr = track_name.replace("Shape", "")
    if track_name == "CircleShape":
        if not angles or not isinstance(angles, list) or len(angles) < 2:
            feedback(
                f"A list of 2 or more angles is needed for a Circle-based Track!", True
            )
    elif track_name in ["SquareShape", "RectangleShape"]:
        angles = track.get_angles()
        # change behaviour to match Circle and Polygon
        if clockwise is not None:
            clockwise = True
        else:
            clockwise = not clockwise
    elif track_name == "PolygonShape":
        angles = track.get_angles()
    elif track_name not in SHAPES_FOR_TRACK:
        feedback(f"Unable to use a {track_abbr} for a Track!", True)
    if rotation_style:
        _rotation_style = str(rotation_style).lower()
        if _rotation_style not in ["o", "outwards", "inwards", "i"]:
            feedback(f"The rotation_style '{rotation_style}' is not valid", True)
    else:
        _rotation_style = None
    shapes = kwargs.get("shapes", [])  # shape(s) to draw at the locations
    if not shapes:
        feedback("Track needs at least one Shape assigned to shapes list", False, True)

    track_points = []  # a list of Ray tuples
    # ---- create Circle vertices and angles
    if track_name == "CircleShape":
        # calculate vertices along circumference
        for angle in angles:
            c_pt = geoms.point_on_circle(
                point_centre=Point(track._u.cx, track._u.cy),
                radius=track._u.radius,
                angle=angle,
            )
            track_points.append(
                Ray(c_pt.x + track._o.delta_x, c_pt.y + track._o.delta_y, angle)
            )
    else:
        # ---- get normal vertices and angles
        vertices = track.get_vertexes()
        angles = [0] * len(vertices) if not angles else angles  # Polyline-> has none!
        for key, vertex in enumerate(vertices):
            track_points.append(Ray(vertex.x, vertex.y, angles[key]))

    # ---- change drawing order
    if clockwise is not None and clockwise is False:
        track_points = list(reversed(track_points))
        _swop = len(track_points) - 1
        track_points = track_points[_swop:] + track_points[:_swop]

    # ---- change start point
    # move the order of vertices
    if start is not None:
        _start = start - 1
        if _start > len(track_points):
            feedback(
                f'The start value "{start}" must be less than the number of vertices!',
                True,
            )
        track_points = track_points[_start:] + track_points[:_start]

    # ---- walk the track & draw shape(s)
    shape_id = 0
    for index, track_point in enumerate(track_points):
        # TODO - delink shape index from track vertex index !
        # ---- * ignore sequence not in the list
        if sequences:
            if index + 1 not in sequences:
                continue
        # ---- * stop early if index exceeded
        if stop and index >= stop:
            break
        # ---- * enable overwrite/change of properties
        if len(shapes) == 0:
            continue
        shape = copy(shapes[shape_id])
        # ---- * store data for use by text
        data = {
            "x": track_point.x,
            "y": track_point.y,
            "theta": track_point.angle,
            "count": index + 1,
        }
        # feedback(f'*Track* {index=} {data=}')
        # format_label(shape, data)
        # ---- supply data to change shape's location
        # TODO - can choose line centre, not vertex, as the cx,cy position
        shape.cx = shape.points_to_value(track_point.x - track._o.delta_x)
        shape.cy = shape.points_to_value(track_point.y - track._o.delta_y)
        # feedback(f'*Track* {shape.cx=}, {shape.cy=}')
        if _rotation_style:
            match _rotation_style:
                case "i" | "inwards":
                    if track_name == "CircleShape":
                        shape_rotation = 90 + track_point.angle
                    else:
                        shape_rotation = 90 - track_point.angle
                case "o" | "outwards":
                    if track_name == "CircleShape":
                        shape_rotation = 270 + track_point.angle
                    else:
                        shape_rotation = 270 - track_point.angle
                case _:
                    raise NotImplementedError(
                        f"The rotation_style '{_rotation_style}' is not valid"
                    )
        else:
            shape_rotation = 0
        shape.set_unit_properties()
        # feedback(f'$$$ Track {shape._u}')
        locale = Locale(
            x=track_point.x,
            y=track_point.y,
            id=index,
            sequence=index + 1,
        )
        _locale = locale._asdict()
        shape.draw(cnv=globals.canvas, rotation=shape_rotation, locale=_locale)
        shape_id += 1
        if shape_id > len(shapes) - 1:
            shape_id = 0  # reset and start again


# ---- bgg API ====


def BGG(user: str = None, ids: list = None, progress=False, short=500, **kwargs):
    """Access BGG API for game data"""
    ckwargs = {}
    # ---- self filters
    if kwargs.get("own") is not None:
        ckwargs["own"] = tools.as_bool(kwargs.get("pwn"))
    if kwargs.get("rated") is not None:
        ckwargs["rated"] = tools.as_bool(kwargs.get("rate"))
    if kwargs.get("played") is not None:
        ckwargs["played"] = tools.as_bool(kwargs.get("played"))
    if kwargs.get("commented") is not None:
        ckwargs["commented"] = tools.as_bool(kwargs.get("commented"))
    if kwargs.get("trade") is not None:
        ckwargs["trade"] = tools.as_bool(kwargs.get("trade"))
    if kwargs.get("want") is not None:
        ckwargs["want"] = tools.as_bool(kwargs.get("want"))
    if kwargs.get("wishlist") is not None:
        ckwargs["wishlist"] = tools.as_bool(kwargs.get("wishlist"))
    if kwargs.get("preordered") is not None:
        ckwargs["preordered"] = tools.as_bool(kwargs.get("preordered"))
    if kwargs.get("want_to_play") is not None:
        ckwargs["want_to_play"] = tools.as_bool(kwargs.get("want_to_play"))
    if kwargs.get("want_to_buy") is not None:
        ckwargs["want_to_buy"] = tools.as_bool(kwargs.get("want_to_buy"))
    if kwargs.get("prev_owned") is not None:
        ckwargs["prev_owned"] = tools.as_bool(kwargs.get("prev_owned"))
    if kwargs.get("has_parts") is not None:
        ckwargs["has_parts"] = tools.as_bool(kwargs.get("has_parts"))
    if kwargs.get("want_parts") is not None:
        ckwargs["want_parts"] = tools.as_bool(kwargs.get("want_parts"))
    gamelist = BGGGameList(user, **ckwargs)
    if user:
        ids = []
        if gamelist.collection:
            for item in gamelist.collection.items:
                ids.append(item.id)
                _game = BGGGame(game_id=item.id, user_game=item, user=user, short=short)
                gamelist.set_values(_game)
        if not ids:
            feedback(
                f"Sorry - no games could be retrieved for BGG username {user}", True
            )
    elif ids:
        feedback(
            "All board game data accessed via this tool is owned by BoardGameGeek"
            " and provided through their XML API"
        )
        for game_id in ids:
            if progress:
                feedback(f"Retrieving game '{game_id}' from BoardGameGeek...")
            _game = BGGGame(game_id=game_id, short=short)
            gamelist.set_values(_game)
    else:
        feedback(
            "Please supply either `ids` or `user` to retrieve games from BGG", True
        )
    return gamelist


# ---- objects ====


def Polyomino(row=None, col=None, **kwargs) -> PolyominoObject:
    """Create a Polyomino object

    Args:
        - row (int): row in which Polyomino is drawn.
        - col (int): column in which Polyomino is drawn.

    Kwargs:
        - pattern (list): a list of string values; one string per row. Each string
          contains one or more numbers aka "columns". Each number represents a square,
          with a zero (0) representing a space.
        - invert (str): can either be ``leftright`` (``lr``) or ``topbottom``
          (``tb``) and will reverse the order of the numbers, either in a left-to-right
          (numbers at the end of a row go to the start and vice-versa) or top-to-bottom
          (rows at the end go to the start and vice-versa)
        - flip (str): can either be ``north`` (``n``) or ``south`` (``s``) and
          transposes rows and columns; effectively rotating the shape 90 degrees
        - gap (float): the amount of space to leave between each row and each
          column in the pattern
        - outline (bool): along with *outline_stroke* and *outline_stroke_width*
          is used to draw a line around the boundary of all connected squares in
          the pattern |dash| it cannot be used in conjunction with a non-zero *gap*
        - outline_stroke (str): color of boundary line around all connected squares
        - outline_stroke_width (float): width of boundary line around all connected
          squares
        - fills (list): each square can be associated with a different fill color
        - strokes (list): each square can be associated with a different stroke color
        - labels (list): each square can be linked to a different label
        - shapes (list): each square can be linked to a different centred shape

    Returns:
        PolyominoObject

    """
    kwargs = margins(**kwargs)
    polym = polyomino(row=row, col=col, **kwargs)
    polym.draw()
    return polym


def polyomino(row=None, col=None, **kwargs) -> PolyominoObject:
    kwargs = margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return PolyominoObject(canvas=globals.canvas, **kwargs)


def Pentomino(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    pentm = pentomino(row=row, col=col, **kwargs)
    pentm.draw()
    return pentm


def pentomino(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return PentominoObject(canvas=globals.canvas, **kwargs)


def Tetromino(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    tetrm = tetromino(row=row, col=col, **kwargs)
    tetrm.draw()
    return tetrm


def tetromino(row=None, col=None, **kwargs):
    kwargs = margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return TetrominoObject(canvas=globals.canvas, **kwargs)


# ---- dice ====


def dice(dice="1d6", rolls=None):
    """Roll multiple totals for a kind of die.

    Examples:
    >>> dice('2d6')  # Catan dice roll
    [9]
    >>> dice('3D6', 6)  # D&D Basic Character Attributes
    [14, 11, 8, 10, 9, 7]
    >>> dice()  # single D6 roll
    [3]
    """
    if not dice:
        dice = "1d6"
    try:
        dice = dice.replace(" ", "").replace("D", "d")
        _list = dice.split("d")
        _type, pips = int(_list[0]), int(_list[1])
    except Exception:
        feedback(f'Unable to determine dice type/roll for "{dice}"', True)
    return Dice().multi_roll(count=rolls, pips=pips, dice=_type)


def d4(rolls=None):
    return DiceD4().roll(count=rolls)


def d6(rolls=None):
    return DiceD6().roll(count=rolls)


def d8(rolls=None):
    return DiceD8().roll(count=rolls)


def d10(rolls=None):
    return DiceD10().roll(count=rolls)


def d12(rolls=None):
    return DiceD12().roll(count=rolls)


def d20(rolls=None):
    return DiceD20().roll(count=rolls)


def d100(rolls=None):
    return DiceD100().roll(count=rolls)


def named(variable):
    return f"{variable=}".split("=")[0]


# ---- shortcuts ====


def A8BA():
    """Shortcut to setup A8 page with Blueprint; use for examples."""
    Create(
        paper="A8",
        margin_left=0.5,
        margin_right=0.5,
        margin_bottom=0.5,
        margin_top=0.5,
        font_size=8,
    )
    Blueprint(stroke_width=0.5)


# ---- inherited docs ====


create.__doc__ = Create.__doc__
save.__doc__ = Save.__doc__
polyomino.__doc__ = Polyomino.__doc__
DeckOfCards.__doc__ = Deck.__doc__
