# -*- coding: utf-8 -*-
"""
protograf function for creating card and counter layouts
"""

# lib
from copy import copy
import itertools
import logging
import os
from pathlib import Path
import random
import sys
import types
from typing import Any

# third party
import jinja2
from PIL import Image as PIL_Image
import pymupdf
from pymupdf import Rect as muRect

# module
from protograf import globals

# from protograf.protos import Switch
from protograf.base import BaseShape, BaseCanvas, GroupBase, WIDTH
from protograf.shapes import (
    RectangleShape,
    CardShape,
)
from protograf.utils.messaging import feedback
from protograf.utils import colrs, loadr, tools, support
from protograf.utils.constants import (
    DEFAULT_CARD_WIDTH,  # cm
    DEFAULT_CARD_HEIGHT,  # cm
    DEFAULT_CARD_COUNT,
    DEFAULT_CARD_RADIUS,  # cm
    DEFAULT_COUNTER_SIZE,  # cm
    DEFAULT_COUNTER_RADIUS,  # cm
)
from protograf.utils.docstrings import docstring_card
from protograf.utils.support import CACHE_DIRECTORY
from protograf.utils.structures import (
    CardBleed,
    CardFrame,
    DatasetType,
    DeckPrintState,
    LookupType,
    Locale,
    PageMargins,
    Point,
    TemplatingType,
)
from protograf.utils.tools import _lower

# local
from .utils import validate_globals, margins, GRAYS
from .proto_commands import page_setup

log = logging.getLogger(__name__)


def Matrix(labels: list | None = None, data: list | None = None) -> list:
    """Return list of dicts; each element is a unique combo of all the items in `data`

    Args:

    - labels (list): a list of strings representing key names
    - data (list):  a list of lists; each nested list contains one or more string or
      numbers representing a set of common attributes e.g. card suits

    """
    if data is None:
        return []
    combos = list(itertools.product(*data))
    # check labels
    data_length = len(combos[0])
    if labels == [] or labels is None:
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


class DeckOfCards:
    """
    Placeholder for the deck design; storing lists of CardShapes; allowing export
    """

    def __init__(self, canvas=None, **kwargs):
        self.cnv = canvas  # initial pymupdf Shape object (need one per Page)
        self.kwargs = kwargs
        # feedback(f'$$$ DeckShape KW=> {self.kwargs}')
        # ---- INVALID KWARGS
        if kwargs.get("bleed_x") is not None or kwargs.get("bleed_y") is not None:
            feedback('Cannot set "bleed_x" for "bleed_y" for a Deck!', True)
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
        self.cx = self.width / 2.0
        self.cy = self.height / 2.0
        self.cxy = Point(self.cx, self.cy)
        # print(f"$$$ Deck {size=} {self.width=} {self.height} {self.cx=} {self.cy=}")
        self.kwargs["width"] = self.width  # used for create_cardshapes()
        self.kwargs["height"] = self.height  # used for create_cardshapes()
        self.radius = kwargs.get("radius", default_radius)  # OVERWRITE
        # ---- spacing
        self.spacing = tools.as_float(kwargs.get("spacing", 0), "spacing")
        self.spacing_x = tools.as_float(
            kwargs.get("spacing_x", self.spacing), "spacing_x"
        )
        self.spacing_y = tools.as_float(
            kwargs.get("spacing_y", self.spacing), "spacing_y"
        )
        # ---- dataset (list of dicts)
        self.dataset = kwargs.get("dataset", None)
        self.set_dataset()  # globals override : dataset AND cards
        if self.dataset:
            self.cards = len(self.dataset)
        # ---- behaviour
        self.sequence = kwargs.get("sequence", [])  # e.g. "1-2" or "1-5,8,10"
        self.template = kwargs.get("template", None)
        self.copy = kwargs.get("copy", None)
        self.card_name = kwargs.get("card_name", None)
        self.card_grid = kwargs.get("card_grid", None)
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
        # ---- offset
        self.offset = tools.as_float(kwargs.get("offset", 0), "offset")
        self.offset_x = tools.as_float(kwargs.get("offset_x", self.offset), "offset_x")
        self.offset_y = tools.as_float(kwargs.get("offset_y", self.offset), "offset_y")
        # ---- gutter (put backs of Cards on same page)
        self.gutter = tools.as_float(kwargs.get("gutter", 0), "gutter")  # none if zero
        self.gutter_stroke = kwargs.get("gutter_stroke", None)
        self.gutter_stroke_width = kwargs.get("gutter_stroke_width", WIDTH)
        self.gutter_dotted = kwargs.get("gutter_dotted", None)
        self.gutter_layout = kwargs.get("gutter_layout", "portrait")
        self.show_backs = False
        # ---- zones (non-card shapes)
        self.zones = kwargs.get("zones", None)
        # ---- export options
        self.export_cards = kwargs.get("export_cards", False)
        self.dpi = kwargs.get("dpi", None)
        self.directory = kwargs.get("directory", None)
        extra = globals.deck_settings.get("extra", 0)
        self.cards += extra
        # print(f'$$$ Card Count: {self.cards} Deck Settings: {globals.deck_settings}')
        # ---- gallery options: settings override e.g. margin and page size
        self.gallery = kwargs.get("gallery", None)  # card grid size per page
        # ---- gallery - trigger overrides of settings in DeckOfCards draw!
        if self.gallery:
            self.gallery_overrides(self.gallery)
        # ----- set card frame type
        self.frame = kwargs.get("frame", "rectangle")
        match self.frame:
            case "rectangle" | "r":
                self.frame_type = CardFrame.RECTANGLE
                if self.height > (
                    globals.page.height - globals.margins.top - globals.margins.bottom
                ):
                    feedback("Card height cannot exceed available page height.", True)
                if self.width > (
                    globals.page.width - globals.margins.left - globals.margins.right
                ):
                    feedback("Card width cannot exceed available page width.", True)
            case "circle" | "c":
                self.frame_type = CardFrame.CIRCLE
                if 2 * self.radius > (
                    globals.page.height - globals.margins.top - globals.margins.bottom
                ):
                    feedback("Card diameter cannot exceed available page height.", True)
                if 2 * self.radius > (
                    globals.page.width - globals.margins.left - globals.margins.right
                ):
                    feedback("Card diameter cannot exceed available page width.", True)
            case "hexagon" | "h":
                self.frame_type = CardFrame.HEXAGON
                if 2 * self.radius > (
                    globals.page.height - globals.margins.top - globals.margins.bottom
                ):
                    feedback("Card diameter cannot exceed available page height.", True)
                if 2 * self.radius > (
                    globals.page.width - globals.margins.left - globals.margins.right
                ):
                    feedback("Card diameter cannot exceed available page width.", True)
                if (
                    self.spacing_x
                    and self.spacing_y
                    and self.spacing_x == self.spacing_y
                ):
                    feedback(
                        "Equal card spacing implies hexagon diagonal edges are not aligned.",
                        False,
                        True,
                    )
            case _:
                hint = " Try rectangle, hexagon, or circle."
                feedback(f"Unable to draw a {self.frame}-shaped card. {hint}", True)
        self.kwargs["frame_type"] = self.frame_type  # used for create_cardshapes()

        # ---- FINALLY...
        self.prime_globals = None  # save main document settings for reuse after gutters
        # print(f'$$$ {self.cards=}, {globals.deck_settings=}')
        self.create_cardshapes(self.cards)

    def gallery_overrides(self, gallery):
        """Reset document and page properties to handle NxM card layouts"""
        # from protograf.protos import PageBreak, page_setup, Switch
        err = f'The gallery property must be a pair of numbers in (M, N) format; not "{
            gallery}".'
        if isinstance(gallery, tuple) and len(gallery) == 2:
            if not isinstance(gallery[0], int) or not isinstance(gallery[1], int):
                feedback(err, True)
        else:
            feedback(err, True)

        cols, rows = gallery[0], gallery[1]
        # print(f"### Gallery  {cols=} {rows=}")
        # alter card settings
        self.gutter_layout = None
        self.gutter = 0
        self.grouping_rows = 1
        self.grouping_cols = 1
        self.card_cols = cols
        self.card_rows = rows
        self.spacing_x = 0
        self.spacing_y = 0
        # remove initial default page
        globals.document.delete_page(0)
        # alter page settings
        globals.page.size = (
            globals.units * self.width * cols,
            globals.units * self.height * rows,
        )
        globals.margins = PageMargins(
            margin=0,
            left=0,
            right=0,
            bottom=0,
            top=0,
            debug=False,
            units=globals.units,
            units_type=globals.units_type,
        )
        globals.page.width = globals.page.size[0] / globals.units  # width ~user units
        globals.page.height = globals.page.size[1] / globals.units  # height ~user units
        # print(f"###   {globals.page.size=} {globals.margins=}")
        globals.override = True  # allows Shape margins to be overridden
        # create new, larger, page to hold card array
        globals.doc_page = globals.document.new_page(
            width=globals.page.size[0], height=globals.page.size[1]
        )  # pymupdf Page object
        globals.canvas = globals.doc_page.new_shape()  # pymupdf Shape object
        page_setup()  # page color, grid and debug margins

    def set_dataset(self):
        """Create deck dataset from globals dataset"""
        if globals.dataset_type in [
            DatasetType.DICT,
            DatasetType.FILE,
            DatasetType.MATRIX,
        ]:
            log.debug("globals.dataset_type: %s", globals.dataset_type)
            if len(globals.dataset) == 0:
                feedback("The provided data is empty or cannot be loaded!")
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
            rect.draw()
        # ---- bleed areas (custom)
        # for area in self.bleed_areas:
        #     #print('$$$  BLEED AREA $$$ ', area)

    def export_cards_as_images(
        self,
        filename: str,
        directory: str,
        output: str | None = None,
        fformat: str = "png",
    ) -> list:
        """Save individual cards as PNG images using their frames."""
        card_names = []
        if self.export_cards and globals.pargs.png:  # pargs.png should default to True
            card_names = support.pdf_frames_to_png(
                source_file=filename,
                output=output or filename,
                fformat=fformat,
                dpi=self.dpi,
                directory=directory or self.directory,
                frames=globals.card_frames,
                # page_height=globals.page.size[1],
            )
        return card_names

    def export_cards_as_single_image(
        self,
        card_names: list,
        filename: str,
        output: str | None = None,
        directory: str = "/tmp/demo",
        fformat: str = "png",
    ):
        """Combine individual card PNG images into a single large one.

        Notes:
            * This kind of image is used by TTS (Table Top Simulator)
        """
        # new, transparent canvas
        output_name = "deck_image.png"  # set via user?
        MAX_X, MAX_Y = 500, 800  # set by user or default to 4096, 4096
        new_image = PIL_Image.new("RGBA", (MAX_X, MAX_Y), color=(0, 0, 0, 0))
        # source images
        card_names = card_names or ["image", "image-1-2", "image-1-3", "image-1-4"]
        # TODO - load first image to get its dimensions
        x, y = 0, 0  # top-left
        # add source images to new canvas
        for key, image in enumerate(card_names):
            if x > MAX_X:
                x = 0
                y = y + 400  # image height
                if y > MAX_Y:
                    # maybe start a new image ???
                    feedback(f"Too many card images to fit into {output_name}!", True)
            _file = Path(directory, f"{image}.{fformat}")
            card_image = PIL_Image.open(_file).convert("RGBA")
            new_image.paste(card_image, (x, y), mask=card_image)
            x = x + 250  # image width
        # save final result
        file_out = Path(directory, output_name)
        new_image.save(file_out, "PNG")

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw all cards for a DeckOfCards.

        Kwargs:

        - cards (int): number of cards to draw
        - extra (int): number of extra cards to draw (beyond Data count)
        - copy - name of Data column used to set number of copies of a Card
        - image_list (list): list of image filenames
        - export_cards (bool): if True, then export Card fronts as individual images
        - card_name (str): name of Data column used to create filename for export Cards
        - card_rows (int): maximum number of rows of cards on a page
        - card_cols (int): maximum number of columns of cards on a page
        - dpi (int): resolution for output PNG
        - directory (str): path to save output(s)
        - zones (list): tuples of form (str|int, Shape), where 0-position is the
          page number, and 1-position is the Shape to be drawn there

        # grid_marks=globals.deck_settings.get("grid_marks", None)

        Note:
            DeckOfCards draw() is called by Save() function.
        """

        def draw_the_zones(
            cnv, page_number: int = 0, zones: list | None = None
        ) -> DeckPrintState:
            """Process a list of Zones for a page

            Args:
                cnv: pymupdf Shape object (one per Page)
                page_number: current page (0-based)
            """
            # print(f'$$$ draw_the_zones {page_number=}')
            if zones is None:
                return
            if zones and isinstance(zones, list):
                # set meta data for shape draw
                _locale = Locale(
                    col=0,
                    row=0,
                    id=None,
                    sequence=0,
                    page=page_number + 1,
                )
                kwargs["locale"] = _locale._asdict()
                for zone in zones:
                    try:
                        numbers = tools.sequence_split(zone[0], unique=True, star=True)
                        shape = zone[1]
                        if not isinstance(shape, BaseShape):
                            feedback(
                                f'Cannot process zones item "{zone}" -'
                                " only a shape can be used for drawing!",
                                True,
                            )
                        for number in numbers:
                            if number == page_number + 1 or number == "*":
                                rkwargs = copy(kwargs)
                                rkwargs.pop("grid_marks", None)
                                rkwargs.pop("stroke", None)
                                rkwargs.pop("fill", None)
                                shape.draw(cnv=cnv, **rkwargs)
                    except IndexError:
                        feedback(
                            f'Cannot process zones item "{zone}" -'
                            " please check formatting and values!",
                            True,
                        )
            else:
                feedback(
                    f'Cannot process zones "{zones}" - needs a list of paired items!'
                )

        def draw_the_cards(
            cnv,
            state: DeckPrintState,
            page_number: int = 0,
            front: bool = True,
            right_gap: float = 0.0,
        ) -> DeckPrintState:
            """Process a page of Cards for front or back of a DeckOfCards

            Args:

            - cnv (pymupdf.Shape): shape object; one per Page
            - state (DeckPrintState): track what is being printed on the page
            - page_number (int): current page
            - front (bool): if True, print CardShapes in `deck.fronts`
            - right_gap (float): space left after the last card
            - card_grid (float): interval between card grid lines

            Returns:
                DeckPrintState at the end of a Page
            """
            from protograf.protos import PageBreak

            # print(f'\n$$$ draw_the_cards {page_number=} {front=}')
            start_card = state.card_number
            card_count = state.card_count
            card_number = start_card
            if front:
                row, col = 0, 0
            else:
                row, col = 0, max_cols - 1  # draw left-to-right for back

            # for bleed INSIDE face cards ONLY, disable this!
            self.draw_bleed(cnv, page_across, page_down)

            rendered_one = False
            for card_num in range(start_card, card_count):
                # print(f"$$$ {card_num+1} of {card_count=}")
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
                    page=page_number + 1,
                )
                kwargs["locale"] = _locale._asdict()
                kwargs["grouping_cols"] = self.grouping_cols
                kwargs["grouping_rows"] = self.grouping_rows
                kwargs["page_number"] = page_number
                kwargs["card_number"] = card_number
                kwargs["cardname"] = None
                kwargs["right_gap"] = right_gap
                kwargs["card_grid"] = self.card_grid
                image = images[card_num] if images and card_num <= len(images) else None
                card.deck_data = self.dataset

                mask = False
                if self.mask:
                    _check = tools.eval_template(
                        self.mask, self.dataset[card_num]  # , label="mask"
                    )
                    mask = tools.as_bool(_check, allow_none=False)
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
                    # get card name (for output png image)
                    if card.kwargs.get("dataset") and self.card_name:
                        cardname = card.deck_data[card_num].get(self.card_name, None)
                        kwargs["cardname"] = cardname

                    for i in range(state.copies_done, copies):
                        rendered_one = True
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
                        # print(f"$$$ CARD DRAWN #{card_num+1} {col+1=} {row+1=}")
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
                            # print(f"$$$ {card_num=} => {col=} {row=} // {max_cols=} {max_rows=}")
                            if front:
                                row, col = 0, 0
                            else:
                                row, col = 0, max_cols - 1
                            PageBreak(**kwargs)
                            cnv = globals.canvas  # new one from page break
                            # print(f"$$$ card_draw - RETURN FROM rows / {front=} : {card_number + 1}")
                            return cnv, DeckPrintState(
                                card_count=state.card_count,
                                card_number=card_number,
                                copies_done=i + 1,
                                start_x=0,
                            )
                state = DeckPrintState(
                    card_count=state.card_count,
                    card_number=card_number,
                    copies_done=0,
                    start_x=0,
                )
            if rendered_one:
                # If we're here, the last call finished rendering without a full page
                # Add a page break to match what happens when it finishes with a full page
                PageBreak(**kwargs)
                cnv = globals.canvas  # new one from page break
                self.draw_bleed(cnv, page_across, page_down)
            # print(f"$$$ card_draw - RETURN FROM end  / {front=} : {card_number + 1}")
            return cnv, DeckPrintState(
                card_count=state.card_count,
                card_number=card_number + 1,
                copies_done=0,
                start_x=0,
            )

        def draw_gutter_cards() -> tuple:
            """Reset page size and associated globals."""
            self.prime_globals = tools.save_globals()
            globals_page = copy(globals.page)
            gutter = tools.as_float(kwargs.get("gutter", 0.0), "gutter")
            # ---- pymupdf: new file, doc, page, shape/canvas
            cache_directory = Path(Path.home() / CACHE_DIRECTORY)
            gutter_filename = os.path.join(cache_directory, "gutter.pdf")
            globals.filename = gutter_filename
            globals.document = pymupdf.open()  # pymupdf Document

            if self.gutter_layout:
                _gutter_layout = _lower(self.gutter_layout)
                if _gutter_layout not in ["p", "portrait", "l", "landscape"]:
                    feedback(
                        f'The gutter_layout "{self.gutter_layout}" is not valid'
                        ' - use "portrait" or "landscape"'
                    )
                    return "", False

            if globals_page.size[0] > globals_page.size[1]:
                width = globals_page.size[0]
                height = globals_page.size[1] / 2
                is_landscape = True
            else:
                width = globals_page.size[1]
                height = globals_page.size[0] / 2
                is_landscape = False

            # WIP for landscape layout with TALL cards
            # height = globals_page.size[1] / 2
            # width = globals_page.size[0]
            # if globals_page.size[0] > globals_page.size[1]:
            #     is_landscape = True
            # else:
            #     is_landscape = False
            # print(f"$$$ {globals_page.size[0]=} {globals_page.size[1]=} {width=} {height=} ")

            globals.doc_page = globals.document.new_page(
                width=width, height=height
            )  # pymupdf Page
            # ---- new globals for gutter
            globals.page.width = width / globals.units
            globals.page.height = height / globals.units
            globals.page.size = (width, height)
            # ---- BaseCanvas
            globals.base = BaseCanvas(
                globals.document, paper=globals.paper, defaults=None, kwargs=kwargs
            )
            globals.margins = PageMargins(
                margin=self.prime_globals.margins.margin,
                left=self.prime_globals.margins.left,
                right=self.prime_globals.margins.right,
                top=self.prime_globals.margins.top - gutter / 2.0,
                bottom=self.prime_globals.margins.bottom,
                debug=self.prime_globals.margins.debug,
                units=globals.units,
                units_type=self.prime_globals.margins.units_type,
            )
            cnv = globals.doc_page.new_shape()  # pymupdf Shape
            globals.canvas = cnv
            page_setup()  # draw margin/grid
            # ---- validate card fit
            vspace = globals.page.height - globals.margins.top - globals.margins.bottom
            if self.height + self.offset_y > vspace:
                feedback(
                    "Rotated cards cannot fit into the available space!"
                    " Reduce card height, or top/bottom margins, or offset from top.",
                    True,
                )

            return gutter_filename, is_landscape

        def load_gutter_pages(is_landscape: bool, gutter_filename: str):
            """Insert gutter pages into primary document and reset globals."""
            from protograf.protos import PageBreak

            # ---- * save gutter document
            gutterfile = os.path.join(globals.directory, globals.filename)
            try:
                globals.document.save(gutterfile)
            except ValueError as err:
                feedback(f"Unable to save file: {err}", True, True)
            except Exception() as err:
                feedback(f"Unable to save file: {err}", True, True)
            # ---- * export individual cards
            self.export_cards_as_images(
                filename=globals.filename,
                directory=globals.directory,
                output=self.prime_globals.filename,
            )  # default to PNG format
            # ---- * reset primary document globals and setup fresh document
            tools.restore_globals(self.prime_globals)
            globals.document.delete_pages(0, globals.document.page_count - 1)
            globals.doc_page = globals.document.new_page(
                width=globals.page.size[0], height=globals.page.size[1]
            )  # pymupdf Page
            globals.page_count = 1
            globals.canvas = globals.doc_page.new_shape()  # pymupdf Shape
            page_setup()
            cnv = globals.canvas
            # ---- * open gutter document
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
            # ---- * insert pages from gutter.pdf
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
                        pt1 = (0, globals.page.size[1] / 2.0)
                        pt2 = (globals.page.size[0], globals.page.size[1] / 2.0)
                    else:
                        pt1 = (globals.page.size[0] / 2.0, 0)
                        pt2 = (globals.page.size[0] / 2.0, globals.page.size[1])
                    globals.canvas.draw_line(pt1, pt2)
                    gwargs = {}  # kwargs
                    GRAY = GRAYS[0] if globals.color_model == "CMYK" else GRAYS[1]
                    gwargs["stroke"] = self.gutter_stroke or colrs.get_color(GRAY)
                    gwargs["stroke_width"] = self.gutter_stroke_width
                    gwargs["dotted"] = self.gutter_dotted
                    tools.set_canvas_props(cnv=globals.canvas, index=None, **gwargs)
                PageBreak()
            # ---- * delete extra blank page at the end
            globals.document.delete_page(globals.page_count - 1)
            # ---- delete gutter PDF document
            # TODO !!! unc
            # if os.path.exists(gutter_filename):
            #     os.remove(gutter_filename)

        # ---- * DRAW START * ----

        # ---- primary layout settings for card.draw()
        # cnv = cnv if cnv else globals.canvas  # no card draw on first page for gutter?
        cnv = globals.canvas

        # feedback(f'$$$ DeckShape.draw {cnv=} KW=> {kwargs}')
        # log.debug("Deck cnv:%s type:%s", type(globals.canvas), type(cnv))
        kwargs = self.kwargs | kwargs
        images = kwargs.get("image_list", [])
        kwargs["frame_type"] = self.frame_type

        # ---- user-defined rows and cols
        max_rows = self.card_rows
        max_cols = self.card_cols

        # print(f"###    {globals.page=} {globals.page.width=} {globals.page.height=}")
        # print(f"###    {globals.margins=}")
        # print(f"$$$ {globals.page.width=} card{self.width=} {max_cols=}")
        # print(f"$$$ {globals.page.height=} card{self.height=} {max_rows=}")
        # print(f"===================================================================")

        # ---- other settings
        self.export_cards = kwargs.get("export_cards", False)
        self.dpi = kwargs.get("dpi", 300)

        # ---- local defaults
        is_landscape, gutter_filename = False, ""

        # ---- gutter-based settings (new doc)
        if self.gutter > 0:
            gutter_filename, is_landscape = draw_gutter_cards()

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
        page_across = globals.page.width - margin_right - margin_left  # user units
        page_down = globals.page.height - margin_top - margin_bottom  # user units
        _height, _width, _radius = self.height, self.width, self.radius
        if self.gallery is not None:
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
        # _radius = _card.outline.radius
        # print(f'$$$ _card: {_height=} {_width=} {_radius=}')

        # ---- space calcs for rows/cols
        # Note: units here are user-based
        if not max_rows:
            row_space = globals.page.height - margin_bottom - margin_top - self.offset_y
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
            col_space = globals.page.width - margin_left - margin_right - self.offset_x
            # print(f'$$$ {globals.page.width=} {margin_left=} {margin_right=} {self.offset_x=}')
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
        right_gap = globals.page.width - effective_right

        # ---- prep for card drawing
        page_number = -1
        state_front = DeckPrintState(
            card_count=len(self.fronts), card_number=0, copies_done=0, start_x=0
        )
        state_back = DeckPrintState(
            card_count=len(self.backs), card_number=0, copies_done=0, start_x=0
        )
        for back in self.backs:
            if back.elements:
                self.show_backs = True
                continue

        # ---- actually draw zones and cards!
        while state_front.card_number < len(self.fronts):
            page_number += 1  # for back-to-back OR no backs
            draw_the_zones(cnv, page_number, self.zones)
            cnv, state_front = draw_the_cards(cnv, state_front, page_number, True, 0)
            if self.show_backs:
                page_number += 1  # for back-to-back
                draw_the_zones(cnv, page_number, self.zones)
                cnv, state_back = draw_the_cards(
                    cnv, state_back, page_number, False, right_gap
                )
            if page_number > 9999:
                feedback(
                    f"Exceeded maximum number of 9999 pages ({page_number})", False
                )
                break

        # print(f"===================================================================")
        # print(f"$$$ {right_gap=} {globals.page.width=} {effective_right=}")
        # print(f"$$$ {globals.page.width=} card{_width=} {col_space=} {max_cols=}")
        # print(f"$$$ {globals.page.height=} card{_height=} {row_space=} {max_rows=}")

        # ---- delete extra blank page at the end
        globals.document.delete_page(globals.page_count)
        # ---- reset to prime globals and load-in the gutter pages
        if self.gutter > 0:
            load_gutter_pages(is_landscape, gutter_filename)

    def get(self, cid):
        """Return a card based on the internal ID"""
        for card in self.fronts:
            if card.shape_id == cid:
                return card
        return None

    def count(self):
        """Return number of cards in the deck"""
        return len(self.fronts)


@docstring_card
def Card(
    sequence: object = None,
    *elements,
    **kwargs,
):
    """Add one or more elements to a card or cards.

    Args:
    <card>

    Kwargs:
    - bleed_fill (str): the color with which to create the bleed area
    - bleed_x (float): the x-distance away from the card frame to which the bleed extends
    - bleed_y (float): the y-distance away from the card frame to which the bleed extends

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
            elif isinstance(element, BaseShape):
                name = element.simple_name()
                feedback(f'Cannot use a "{name}" shape for a Card or CardBack.', True)
            elif isinstance(element, list):
                feedback(
                    "Cannot use a list for a Card or CardBack; try the group command.",
                    True,
                )
            else:
                feedback(f'Cannot use "{element}" for a Card or CardBack.', True)

    kwargs = margins(**kwargs)
    # print(f'*** Card: {kwargs}')
    # print(f'*** Card: {elements}')
    if not globals.deck:
        feedback("The Deck() has not been defined or is incorrect.", True)
    if not sequence:
        feedback(
            "A Card() does not have a valid sequence and will be skipped.", False, True
        )
        return
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
            if isinstance(sequence, types.FunctionType):
                sequence = sequence()
            if isinstance(sequence, list) and not isinstance(sequence, str):
                _cards = sequence
            elif _lower(sequence) == "all" or _lower(sequence) == "*":
                _cards = list(range(1, card_count + 1))
            elif _lower(sequence) == "odd" or _lower(sequence) == "o":
                _cards = list(range(1, card_count + 1, 2))
            elif _lower(sequence) == "even" or _lower(sequence) == "e":
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
                f'Unable to convert Card "{sequence}" into a range of cards.',
                False,
                True,
            )
            return
    if not _cards:
        feedback(
            "A Card() does not have a valid sequence and will be skipped.", False, True
        )
        return
    max_cards = len(globals.deck.fronts)
    for index, _card in enumerate(_cards):
        if _card > max_cards:
            feedback(
                f"There are {max_cards} cards in the deck;"
                f" a reference to card #{_card} is not valid.",
                True,
            )
        card = globals.deck.fronts[_card - 1]  # cards internally number from ZERO

        if card:
            # ---- add elements to card
            for element in elements:
                # print(f"$$$  Card() {element=} {type(element)=}")
                if isinstance(element, TemplatingType):
                    add_members_to_card(element)
                else:
                    add_members_to_card(element)
            # ---- set card bleed
            if kwargs.get("bleed_fill") and (
                kwargs.get("bleed")
                or kwargs.get("bleed_y")
                or kwargs.get("bleed_x")
                or kwargs.get("bleed_radius")
            ):
                fill = kwargs.get("bleed_fill")
                offset_x = kwargs.get("bleed_x", kwargs.get("bleed", 0.0))
                offset_y = kwargs.get("bleed_y", kwargs.get("bleed", 0.0))
                offset_radius = kwargs.get("bleed_radius", 0.0)
                card.card_bleed = CardBleed(
                    fill=colrs.get_color(fill),
                    offset_x=tools.as_float(offset_x, "bleed_x"),
                    offset_y=tools.as_float(offset_y, "bleed_y"),
                    offset_radius=tools.as_float(offset_radius, "bleed_radius"),
                )
        else:
            feedback(f'Cannot find card#{_card}. (Check "cards" setting in Deck)')


@docstring_card
def CardBack(sequence: object = None, *elements, **kwargs):
    """Add one or more elements to the back of a card or cards.

    Args:
    <card>

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
            if isinstance(sequence, types.FunctionType):
                sequence = sequence()
            if isinstance(sequence, list) and not isinstance(sequence, str):
                _cardbacks = sequence
            elif _lower(sequence) == "all" or _lower(sequence) == "*":
                _cardbacks = list(range(1, cardback_count + 1))
            elif _lower(sequence) == "odd" or _lower(sequence) == "o":
                _cardbacks = list(range(1, cardback_count + 1, 2))
            elif _lower(sequence) == "even" or _lower(sequence) == "e":
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
            feedback(f'Unable to convert "{
                    sequence}" into a cardback or range of cardbacks {globals.deck}.')
    max_backs = len(globals.deck.backs)
    for index, _back in enumerate(_cardbacks):
        if _back > max_backs:
            feedback(
                f"There are {max_backs} card backs in the deck;"
                f" a reference to card #{_back} is not valid.",
                True,
            )
        cardback = globals.deck.backs[_back - 1]  # cards internally number from ZERO
        if cardback:
            for element in elements:
                # print(f'$$$  CardBack() {element=} {type(element)=}')
                if isinstance(element, TemplatingType):
                    add_members_to_back(element)
                else:
                    add_members_to_back(element)
        else:
            feedback(f'Cannot find cardback#{_back}. (Check "cards" setting in Deck)')


@docstring_card
def Counter(sequence, *elements, **kwargs):
    """Add one or more elements to a counter or counters.

    Args:
    <card>

    NOTE: A Counter receives its `draw()` command via Save()!
    """
    Card(sequence, *elements, **kwargs)


@docstring_card
def CounterBack(sequence, *elements, **kwargs):
    """Add one or more elements to the back of a counter or counters.

    Args:
    <card>

    NOTE: A CounterBack receives its `draw()` command via Save()!
    """
    CardBack(sequence, *elements, **kwargs)


def Deck(**kwargs):
    """Placeholder for a deck design; storing lists of CardShapes; allowing export

    Kwargs (optional):

    - bleed_fill (str): background color for the page (up to the margins);
      if no separate **fill** property is set, then this color is used instead
    - cards (int): the number of cards appearing in the deck; defaults to 9
      Note that other objects such as Data() and Matrix() can alter this value
    - card_size (str): a pre-existing card size used to set *width* and *height*
      (if values for *width* and *height* are set, they will override this);
      can be one of: ``poker``, ``bridge``, ``tarot``, ``business``, ``mini``,
      ``skat``, ``mini``, ``minieuropean``, ``miniamerican``
    - cols (int): maximum number of card columns that should appear on a page
    - copy (str): the name of a column in the dataset defined by Data() that
      specifies how many copies of a card are needed
    - fill (str): color of the card's area; defaults to ``white`` (for RGB color_model)
    - frame (str): the default card frame is a *rectangle* (or square, if the
      height and width match); but can be set to *hexagon* or *circle*
    - grid_marks (bool): if set to ``True``, will cause small marks to be drawn at
      the border of the page that align with the edges of the card frames
    - grid_marks_length (float): the length of the *grid_marks*; defaults to ``0.85`` cm
    - grid_marks_stroke (str): line color of the *grid_marks*; defaults to ``grey``
    - grid_marks_stroke_width (float): line width of the *grid_marks*; defaults to 0.1
    - grouping (int): number of cards to be drawn adjacent to each other
      before a blank space is added by the **spacing** property (note that
      **grouping** does not apply to  *hexagon* **frame** cards)
      (about one-third of an inch)
    - grouping_col (int): number of cards to be drawn adjacent to each other
      in a horizontal direction before a blank space is added by the **spacing**
    - grouping_row (int): number of cards to be drawn adjacent to each other
      in a vertical direction before a blank space is added by the **spacing**
    - gutter (float): a value set for this helps determines the spacing between the
      fronts and backs of cards when these are drawn on two halves of the same
      page; its value is divided in half, and added to the top margin value, and
      each set of cards is drawn that distance away from the centre line of the page
    - gutter_stroke (str): if set, will cause a line of that color to be used
      for the *gutter* line; this defaults to ``gray``, for RGB, (to match grid marks)
    - gutter_stroke_width (float): if set to a value, will cause a line of that
      thickness to be used for the *gutter* line
    - gutter_dotted (bool): sets the style of the *gutter* line
    - gutter_layout (str): sets the orientation of the page for the cards drawn in
      the two gutter "halves"; this can be ``portrait`` (the default) or
      ``landscape``` (the latter is useful when you have very tall cards e.g.
      ``tarot`` sized ones)
    - height (float): card height for a *rectangular* card; defaults to 8.89 cm
    - mask (str): an expression which should evaluate to ``True`` or ``False``.
      This expression has the same kind of syntax as T() and it uses data available
      from the Deck object's Data(). If the expression result is ``True``
      then any matching cards will be masked i.e. ignored and not drawn
    - radius (float): radius for a card of type *hexagon* or *circle*; defaults to 2.54 cm
    - rounding: (float) size of rounding on each corner of a rectangular frame card
    - rows (int): maximum number of card rows that should appear on a page
    - spacing (float): size of blank space between each card or grouping in x- and y-direction
    - spacing_x (float): size of blank space between each card or grouping in a
      horizontal direction
    - spacing_y (float): size of blank space between each card or grouping in a
      vertical direction
    - stroke (str): color of the card's border; defaults to ``black`` (for RGB color_model)
    - width (float): card width for a *rectangular* card; defaults to ``6.35`` cm
    - zones (list): list of tuples; each with page number(s) and a shape
    - gallery (tuple): if set to a pair of numbers e.g. ``(6,9)`` will cause that
      many *cards* to be drawn on a page; the page size will be changed to fit them
      all; and all margins will be set to zero |dash| this can be used as an input
      for programs such as Tabletop Simulator (TTS)

    Notes:

    - This function instantiates the object; the object in turn:

        - receives its `draw()` command from Save()
        - draws any gutter lines (one per page)
        - adds any annotations (depending on page ranges)
    """
    validate_globals()

    kwargs = margins(**kwargs)
    kwargs["dataset"] = globals.dataset
    globals.deck = DeckOfCards(canvas=globals.canvas, **kwargs)
    globals.deck_settings["grid_marks"] = kwargs.get("grid_marks", None)
    return globals.deck


def CounterSheet(**kwargs):
    """Initialise a countersheet with all its settings, including source(s) of data."""
    kwargs["_is_countersheet"] = True
    return Deck(**kwargs)


def group(*args, **kwargs) -> GroupBase:
    """Store a list of Shapes to be drawn by a Card-type object."""
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
    - sheet (int): the number of sheet in the Excel file being used; defaults
      to the first one
    - sheetname (str): the name of sheet in the Excel file being used; defaults
      to the first one
    - cells (str): a range of cells delimiting data in the col:row format
      from top-left to bottom-right e.g. 'A3:E12'
    - a **Google Sheet** document is accessed via three properties:

      - google_key (str): an API key that you must request from Google
      - google_sheet (str): the unique ID (a mix of numbers and letters) which is
        randomly assigned by Google to your Google Sheet
      - sheetname (str): the name of the tab in the Google Sheet housing your data
    - matrix (str): refers to the name assigned to the ``Matrix`` being used
    - images (str): refers to the directory in which the cards' images are
      located;  if a full path is not given, its assumed to be directly under
      the one in which the script is located
    - images_list (list): is used in conjunction with *images* to provide a
      list of file extensions that filter which type of files will be loaded
      from the directory e.g. ``.png`` or ``.jpg``; this is important to set if
      the directory contains files of a type that are not, or cannot be, used
    - data_list (str): refers to the name assigned to the "list of lists" being
      used; this property is also used when linked to data being sourced from
      the BoardGameGeek API
    - extra (int): if additional cards need to be manually created for a Deck,
      that are *not* part of the data source, then the number of those cards
      can be specified here.
    - filters (list): a list of ('key', 'value', 'type') items on which the
      data must be filtered; 'type' is optional and defaults to '='
    - randoms: a number of records to be randomly selected from the data
    """
    validate_globals()

    filename = kwargs.get("filename", None)  # CSV or Excel
    matrix = kwargs.get("matrix", None)  # Matrix()
    data_list = kwargs.get("data_list", None)  # list-of-lists
    images = kwargs.get("images", None)  # directory
    images_filter = kwargs.get("images_filter", "")  # e.g. .png
    image_filter_list = tools.sequence_split(images_filter, to_int=False, unique=True)
    source = kwargs.get("source", None)  # dict
    google_sheet = kwargs.get("google_sheet", None)  # Google Sheet
    debug = kwargs.get("debug", False)
    filters = kwargs.get("filters", None)
    randoms = kwargs.get("randoms", None)
    # extra cards added to deck (handle special cases not in the dataset)
    globals.deck_settings["extra"] = tools.as_int(kwargs.get("extra", 0), "extra")
    try:
        int(globals.deck_settings["extra"])
    except Exception:
        feedback(f'Extra must be a whole number, not "{kwargs.get("extra")}"!', True)

    if filename:  # handle excel and CSV; kwargs include cell, sheet, sheetname
        globals.dataset = loadr.load_data(filename, **kwargs)
        globals.dataset_type = DatasetType.FILE
    elif google_sheet:  # handle Google Sheet
        google_key = kwargs.get("google_key", None)
        sheetname = kwargs.get("sheetname", None)
        globals.dataset = loadr.load_googlesheet(
            google_sheet, api_key=google_key, name=sheetname
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
            if not image_filter_list or child.suffix in image_filter_list:
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
            if not (key.isalnum() or "_" in key):
                feedback(
                    "The Data headers must only be characters (without spaces)"
                    f' e.g. not "{key}"',
                    True,
                )
            if not (key[0].isalpha() or key[0] == "_"):
                feedback(
                    "The Data headers must start with a character or underscore"
                    f' - it cannot be "{key[0]}"',
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
                    print(f"{data=}")
        else:
            print("No {globals.dataset_type} data was loaded!")

    # ---- filters
    if filters:
        if not isinstance(filters, list):
            feedback(
                "Data() filters must be a list of sets of the form (key, value).", True
            )
        for _filter in filters:
            # validate filter
            if not isinstance(_filter, tuple) and len(_filter) < 2:
                feedback(
                    "Data() filters must be a list of sets of the form (key, value, type).",
                    True,
                )
            key, value = _filter[0], _filter[1]
            if key not in globals.dataset[0].keys():
                feedback(
                    f'Data filter key "{key}" is not in the available columns.', True
                )
            # do filtering
            if len(_filter) == 2:
                globals.dataset = [d for d in globals.dataset if d[key] == value]
            if len(_filter) == 3:
                ftype = _lower(_filter[2])
                match ftype:
                    case "<" | "less than" | "less" | "fewer than" | "fewer" | "lt":
                        globals.dataset = [
                            ds for ds in globals.dataset if ds[key] < value
                        ]
                    case ">" | "greater than" | "greater" | "more than" | "more" | "gt":
                        globals.dataset = [d for d in globals.dataset if d[key] > value]
                    case "<>" | "!=" | "not equal" | "not" | "ne":
                        globals.dataset = [
                            ds for ds in globals.dataset if ds[key] != value
                        ]
                    case "=" | "==" | "equals" | "equal to" | "eq":
                        globals.dataset = [
                            ds for ds in globals.dataset if ds[key] != value
                        ]
                    case "~" | "in" | "is in" | "contains":
                        globals.dataset = [
                            ds for ds in globals.dataset if str(value) in str(ds[key])
                        ]
                    case _:
                        feedback(
                            f'Data filter type "{ftype}" is not an available option.',
                            True,
                        )
    # ---- randoms
    if randoms:
        if not isinstance(randoms, int):
            feedback("Data() randoms must be a single integer.", True)
        records = random.sample(range(0, len(globals.dataset)), randoms)
        _dataset = [globals.dataset[r] for r in records]
        globals.dataset = _dataset

    return globals.dataset


def S(test="", result=None, alternate=None) -> object:
    """Enable selection of data from a dataset list

    Args:

    - test (str): a boolean-type Jinja2 expression which can be evaluated to return
      True/False e.g. {{ NAME == 'fred' }} gets the column "NAME" value from the
      dataset and tests its equivalence to the value "fred"
    - result (str / element): returned if `test` evaluates to True
    - alternate (str / element): OPTIONAL; returned if `test` evaluates to False;
      if not supplied, then defaults to None
    """
    from protograf.shapes import Switch

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

    Args:

    - lookup (str): lookup column whose value must be used for the match
      ("source" record)
    - target (str): name of the column of the data being searched ("target" record)
    - result (str):  name of result column containing the data to be returned
      ("target" record)
    - default (Any):  the data to be returned if NO match is made

    Notes:

    The lookup and target enable finding a matching record in the dataset;
    the data in the result column of that record is stored as an
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


def T(string: str, data: dict = None, function: object = None) -> TemplatingType:
    """

    Args:

    - string (str): a Jinja2 expression which can be evaluated using data
    - data (dict): keys from the dict can be used for the Jinja2 expression
    - function (object): a local function provided in the script that must return
      one or more shapes

    """
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


DeckOfCards.__doc__ = Deck.__doc__
CounterSheet.__doc__ = Deck.__doc__
