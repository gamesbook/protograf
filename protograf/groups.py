# -*- coding: utf-8 -*-
"""
Create layouts - grids, repeats, sequences and tracks - for protograf
"""
# lib
import copy
import logging

# third party
import jinja2

# local
from protograf.utils import tools
from protograf.utils.tools import DatasetType, CardFrame  # enums
from protograf.base import BaseShape
from protograf.layouts import SequenceShape, RepeatShape
from protograf.shapes import (
    CircleShape,
    HexShape,
    ImageShape,
    PolygonShape,
    RectangleShape,
)
from protograf.utils.geoms import Locale, Point, BBox
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
            boolean = tools.as_bool(outcome)
            if boolean:
                return self.result
            else:
                return self.alternate
        except jinja2.exceptions.UndefinedError as err:
            tools.feedback(
                f'Switch "{self.test}" is incorrectly constructed ({err})', True
            )
        except Exception as err:
            tools.feedback(
                f'Switch "{self.test}" is incorrectly constructed ({err})', True
            )
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


# ---- Deck / Card related


class CardShape(BaseShape):
    """
    Card shape on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(CardShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        self.kwargs = kwargs
        # tools.feedback(f'$$$ CardShape KW=> {self.kwargs}')
        self.elements = []  # container for objects which get added to the card
        if kwargs.get("_is_countersheet", False):
            default_height = 2.54
            default_width = 2.54
            default_radius = 0.635
        else:
            default_height = 8.8
            default_width = 6.3
            default_radius = 2.54
        self.height = kwargs.get("height", default_height)
        self.width = kwargs.get("width", default_width)
        self.radius = kwargs.get("radius", default_radius)
        self.outline = self.get_outline(
            cnv=canvas, row=None, col=None, cid=None, label=None, **kwargs
        )
        self.kwargs.pop("width", None)
        self.kwargs.pop("height", None)
        self.kwargs.pop("radius", None)
        self.image = kwargs.get("image", None)

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw an element on a given canvas."""
        raise NotImplementedError

    def get_outline(self, cnv, row, col, cid, label, **kwargs):
        outline = None
        kwargs["height"] = self.height
        kwargs["width"] = self.width
        kwargs["radius"] = self.radius
        kwargs["spacing_x"] = self.spacing_x
        kwargs["spacing_y"] = self.spacing_y
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
            case CardFrame.HEXAGON:
                kwargs["sides"] = 6
                outline = PolygonShape(
                    label=label, canvas=cnv, col=col, row=row, **kwargs
                )
                # outline.hex_height_width()
            case _:
                raise NotImplementedError(
                    f'Cannot handle card frame type: {kwargs["frame_type"]}'
                )
        return outline

    def draw_card(self, cnv, row, col, cid, **kwargs):
        """Draw a card on a given canvas.

        Pass on `deck_data` to other commands, as needed, for them to draw Shapes
        """
        image = kwargs.get("image", None)
        # tools.feedback(f'$$$ draw_card  KW=> {kwargs}')
        # ---- draw outline
        label = "ID:%s" % cid if self.show_id else ""
        shape_kwargs = copy.copy(kwargs)
        shape_kwargs["is_cards"] = True
        shape_kwargs["fill"] = kwargs.get("fill", kwargs.get("bleed_fill", None))
        shape_kwargs.pop("image_list", None)  # do NOT draw linked image
        shape_kwargs.pop("image", None)  # do NOT draw linked image
        # tools.feedback(f'$$$ draw_card SKW=> {shape_kwargs}')
        outline = self.get_outline(
            cnv=cnv, row=row, col=col, cid=cid, label=label, **shape_kwargs
        )
        outline.draw(**shape_kwargs)

        # ---- track frame outlines for possible image extraction
        match kwargs["frame_type"]:
            case CardFrame.RECTANGLE:
                _vertices = outline.get_vertices()  # clockwise from bottom-left
                base_frame_bbox = BBox(bl=_vertices[0], tr=_vertices[2])
            case CardFrame.CIRCLE:
                base_frame_bbox = None
            case CardFrame.HEXAGON:
                _vertices = outline.get_vertices()  # anti-clockwise from mid-right
                base_frame_bbox = BBox(
                    bl=Point(_vertices[3].x, _vertices[4].y),
                    tr=Point(_vertices[0].x, _vertices[1].y),
                )
            case _:
                raise NotImplementedError(
                    f'Cannot handle card frame type: {kwargs["frame_type"]}'
                )
        frame_height = base_frame_bbox.tr.x - base_frame_bbox.bl.x
        frame_width = base_frame_bbox.tr.y - base_frame_bbox.bl.y

        # ---- grid marks
        kwargs["grid_marks"] = None  # reset so not used by elements on card
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

        # ---- draw card elements
        flat_elements = tools.flatten(self.elements)
        for index, flat_ele in enumerate(flat_elements):
            # ---- * replace image source placeholder
            if image and isinstance(flat_ele, ImageShape):
                if flat_ele.kwargs.get("source", "").lower() in ["*", "all"]:
                    flat_ele.source = image

            # ---- * calculate card frame shift
            match kwargs["frame_type"]:
                case CardFrame.RECTANGLE | CardFrame.CIRCLE:
                    if kwargs["grouping_cols"] == 1:
                        _dx = (
                            col * (outline.width + outline.spacing_x) + outline.offset_x
                        )
                    else:
                        group_no = col // kwargs["grouping_cols"]
                        _dx = (
                            col * outline.width
                            + outline.offset_x
                            + outline.spacing_x * group_no
                        )
                    if kwargs["grouping_rows"] == 1:
                        _dy = (
                            row * (outline.height + outline.spacing_y)
                            + outline.offset_y
                        )
                        # print(f"{col=} {outline.width=} {group_no=} {_dx=}")
                    else:
                        group_no = row // kwargs["grouping_rows"]
                        _dy = (
                            row * outline.height
                            + outline.offset_y
                            + outline.spacing_y * group_no
                        )
                        # print(f"{row=} {outline.height=} {group_no=} {_dy=}")
                case CardFrame.HEXAGON:
                    _dx = col * 2.0 * (side + outline.spacing_x) + outline.offset_x
                    _dy = row * 2.0 * (half_flat + outline.spacing_y) + outline.offset_y
                    if row & 1:
                        _dx = _dx + side + outline.spacing_x
                case _:
                    raise NotImplementedError(
                        f'Cannot handle card frame type: {kwargs["frame_type"]}'
                    )

            # ---- * track/update frame and store
            mx = self.unit(_dx or 0) + self._o.delta_x
            my = self.unit(_dy or 0) + self._o.delta_y
            frame_bbox = BBox(
                bl=Point(mx, my), tr=Point(mx + frame_width, my + frame_height)
            )
            page = kwargs.get("page_number", 0)
            if page not in globals.card_frames:
                globals.card_frames[page] = [frame_bbox]
            else:
                globals.card_frames[page].append(frame_bbox)

            members = self.members or flat_ele.members
            try:
                # ---- * normal element
                iid = members.index(cid + 1)
                new_ele = self.handle_custom_values(flat_ele, cid)  # calculated values
                if isinstance(new_ele, (SequenceShape, RepeatShape)):
                    new_ele.deck_data = self.deck_data
                # tools.feedback(f'$$$ draw_card $$$ {new_ele=}')
                new_ele.draw(cnv=cnv, off_x=_dx, off_y=_dy, ID=iid, **kwargs)
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
                        # tools.feedback(f'$$$ draw_card $$$ {custom_new_ele=}')
                        custom_new_ele.draw(
                            cnv=cnv, off_x=_dx, off_y=_dy, ID=iid, **kwargs
                        )

            except Exception as err:
                tools.feedback(f"Unable to draw card #{cid + 1}. (Error:{err})", True)


class DeckShape(BaseShape):
    """
    Placeholder for the deck design; list of CardShapes and Shapes.

    NOTE: draw() is called via the Deck function in proto.py
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(DeckShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        self.kwargs = kwargs
        # tools.feedback(f'$$$ DeckShape KW=> {self.kwargs}')
        # ---- cards
        self.deck = []  # container for CardShape objects
        if kwargs.get("_is_countersheet", False):
            default_items = 70
            default_height = 2.54
            default_width = 2.54
            default_radius = 0.635
        else:
            default_items = 9
            default_height = 8.8
            default_width = 6.3
            default_radius = 2.54
        self.counters = kwargs.get("counters", default_items)
        self.cards = kwargs.get("cards", self.counters)  # default total number of cards
        self.height = kwargs.get("height", default_height)  # OVERWRITE
        self.width = kwargs.get("width", default_width)  # OVERWRITE
        self.radius = kwargs.get("radius", default_radius)  # OVERWRITE
        # ----- set card frame type
        match self.frame:
            case "rectangle" | "r":
                self.frame_type = CardFrame.RECTANGLE
            case "circle" | "c":
                self.frame_type = CardFrame.CIRCLE
            case "hexagon" | "h":
                self.frame_type = CardFrame.HEXAGON
            case _:
                hint = " Try rectangle, hexagon, or circle."
                tools.feedback(
                    f"Unable to draw a {self.frame}-shaped card. {hint}", True
                )
        self.kwargs["frame_type"] = self.frame_type
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
            tools.feedback(
                'Cannot set "mask" for a Deck without any existing Data!', True
            )
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
        self.images = kwargs.get("images", None)
        self.images_filter = kwargs.get("images_filter", None)
        self.image_list = []
        # ---- FINALLY...
        extra = globals.deck_settings.get("extra", 0)
        self.cards += extra
        log.debug("Cards: %s Settings: %s", self.cards, globals.deck_settings)
        self.create(self.cards)

    def set_dataset(self):
        """Create deck dataset from globals dataset"""
        if globals.dataset_type in [
            DatasetType.DICT,
            DatasetType.FILE,
            DatasetType.MATRIX,
        ]:
            log.debug("globals.dataset_type: %s", globals.dataset_type)
            if len(globals.dataset) == 0:
                tools.feedback("The provided data is empty or cannot be loaded!", True)
            else:
                # globals.deck.create(len(globals.dataset) + globals.extra)
                self.dataset = globals.dataset
        elif globals.dataset_type == DatasetType.IMAGE:
            # OVERWRITE total number of cards
            self.cards = len(globals.image_list)
        else:
            pass  # no Data created

    def create(self, cards: int = 0):
        """Create a new Deck of CardShapes, based on number of `cards`"""
        log.debug("Cards are: %s", self.sequence)
        self.deck = []
        log.debug("Deck => %s cards with kwargs: %s", cards, self.kwargs)
        for card in range(0, cards):
            _card = CardShape(**self.kwargs)
            _card.shape_id = card
            self.deck.append(_card)

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
            # print(f'*** {page_across=}, {page_down=}')
            rect.draw()
        # ---- bleed areas (custom)
        # for area in self.bleed_areas:
        #     #print('*** BLEED AREA ***', area)

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Method called by Save() in proto.

        Kwargs:
            * cards - number of cards in Deck
            * copy - name of column to use to set number of copies of a Card
            * image_list - list of image filenames
            * card_rows - maximum number of rows of cards on a page
            * card_cols - maximum number of columns of cards on a page
        """
        cnv = cnv if cnv else self.canvas
        log.debug("Deck cnv:%s type:%s", type(self.canvas), type(cnv))
        # ---- handle kwargs
        kwargs = self.kwargs | kwargs
        images = kwargs.get("image_list", [])
        cards = kwargs.get("cards", None)
        kwargs["frame_type"] = self.frame_type
        # ---- user-defined rows and cols
        max_rows = self.card_rows
        max_cols = self.card_cols
        # ---- calculate rows/cols based on page size and margins AND card size
        margin_left = self.margin_left if self.margin_left is not None else self.margin
        margin_bottom = (
            self.margin_bottom if self.margin_bottom is not None else self.margin
        )
        margin_right = (
            self.margin_right if self.margin_right is not None else self.margin
        )
        margin_top = self.margin_top if self.margin_top is not None else self.margin
        page_across = (
            self.points_to_value(globals.page_width) - margin_right - margin_left
        )
        page_down = (
            self.points_to_value(globals.page_height) - margin_top - margin_bottom
        )
        _height, _width, _radius = self.width, self.width, self.radius
        _spacing_x = self.unit(self.spacing_x)
        _spacing_y = self.unit(self.spacing_y)
        self.draw_bleed(cnv, page_across, page_down)
        # ---- deck settings
        col_space, row_space = 0.0, 0.0
        if self.deck:
            _card = self.deck[0]
            (
                _height,
                _width,
            ) = (
                _card.outline.height,
                _card.outline.width,
            )
            _radius = _card.outline.radius
        if not max_rows:
            row_space = (
                float(globals.page_height / globals.units) - margin_bottom - margin_top
            )
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
            col_space = (
                float(globals.page_width / globals.units) - margin_left - margin_right
            )
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
        # log.warning("PW:%s width:%s c-space:%s max-cols:%s",
        #             globals.page_width, _width, col_space, max_cols)
        # log.warning("PH:%s heiht:%s r-space:%s max-rows:%s",
        #             globals.page_height, _height, row_space, max_rows)
        row, col = 0, 0
        # ---- draw cards
        page_number = 0
        for key, card in enumerate(self.deck):
            # set meta data
            _locale = Locale(
                col=col + 1, row=row + 1, id=f"{col + 1}:{row + 1}", sequence=key + 1
            )
            kwargs["locale"] = _locale._asdict()
            kwargs["grouping_cols"] = self.grouping_cols
            kwargs["grouping_rows"] = self.grouping_rows
            kwargs["page_number"] = page_number
            image = images[key] if images and key <= len(images) else None
            card.deck_data = self.dataset

            mask = False
            if self.mask:
                _check = tools.eval_template(self.mask, self.dataset[key], label="mask")
                mask = tools.as_bool(_check, label="mask", allow_none=False)
                if not isinstance(mask, bool):
                    tools.feedback(
                        'The "mask" test must result in True or False value!', True
                    )
            if not mask:
                # get number of copies
                copies = 1
                if card.kwargs.get("dataset") and self.copy:
                    _copies = card.deck_data[key].get(self.copy, None)
                    copies = (
                        tools.as_int(_copies, "copy property", allow_none=True) or 1
                    )

                for i in range(0, copies):
                    card.draw_card(
                        cnv, row=row, col=col, cid=card.shape_id, image=image, **kwargs
                    )
                    col += 1
                    if col >= max_cols:
                        col = 0
                        row += 1
                    if row >= max_rows:
                        row, col = 0, 0
                        if key != len(self.deck) - 1 or (i < (copies - 1)):
                            cnv.canvas.showPage()
                            self.draw_bleed(cnv, page_across, page_down)
                            page_number += 1

    def get(self, cid):
        """Return a card based on the internal ID"""
        for card in self.deck:
            if card.shape_id == cid:
                return card
        return None

    def count(self):
        """Return number of cards in the deck"""
        return len(self.deck)
