# -*- coding: utf-8 -*-
"""
Create CardShapes and Decks of Cards for protograf
"""

# lib
import logging
from collections import namedtuple
import copy as copy_object
import math
import os
from pathlib import Path
import sys

# third party
import jinja2
from PIL import Image as PIL_Image
import pymupdf
from pymupdf import Rect as muRect

# project
from protograf.protos.utils import GRAYS

from protograf.base import BaseCanvas,  BaseShape, GroupBase, WIDTH
from protograf.utils import colrs, tools, support
from protograf.utils.constants import (
    DEFAULT_CARD_WIDTH,  # cm
    DEFAULT_CARD_HEIGHT,  # cm
    DEFAULT_CARD_COUNT,
    DEFAULT_CARD_RADIUS,  # cm
    DEFAULT_COUNTER_SIZE,  # cm
    DEFAULT_COUNTER_RADIUS,  # cm
)
from protograf.utils.messaging import feedback
from protograf.utils.support import (  # used in scripts
    CACHE_DIRECTORY,
)
from protograf.utils.tools import (  # used in scripts
    as_bool,
    _lower,
)
from protograf.utils.structures import (
    BBox,
    CardFrame,
    DatasetType,
    DeckPrintState,
    Locale,
    Point,
    ShapeGeometry,
)

log = logging.getLogger(__name__)

# ---- Support Functions


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
        self.test = None

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
        log.debug("data:%s cid:%s", self.data, cid)
        try:
            return None
        except (ValueError, TypeError, IndexError):
            return None


# ---- Deck / Card related ====


class CardOutline(BaseShape):
    """
    Card outline on a given canvas.

    Note:
        Also use to calculate an area for card bleed.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super().__init__(_object=_object, canvas=canvas, **kwargs)
        self.kwargs = kwargs
        # feedback(f'\n$$$ CardOutline KW=> {self.kwargs}')
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
        self.bleed_x = kwargs.get("bleed_x", 0.0)
        self.bleed_y = kwargs.get("bleed_y", 0.0)
        self.bleed_radius = kwargs.get("bleed_radius", 0.0)
        self.width = kwargs.get("width", default_width) + 2 * self.bleed_x
        self.height = kwargs.get("height", default_height) + 2 * (
            self.bleed_y or self.bleed_radius
        )
        self.radius = kwargs.get("radius", default_radius) + self.bleed_radius
        self.frame_type = kwargs["frame_type"]
        self.outline = self.get_outline(
            cnv=canvas, row=None, col=None, cid=None, label=None, **kwargs
        )
        # print(f'$$$ {self.frame_type=} {self.width=} {self.height=} {self.radius=} ')
        self.kwargs.pop("width", None)
        self.kwargs.pop("height", None)
        self.kwargs.pop("radius", None)

    def get_outline(self, cnv, row, col, cid, label, **kwargs):
        """Get card outline."""
        from protograf.shapes import CircleShape, HexShape, RectangleShape
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
        super().__init__(_object=_object, canvas=canvas, **kwargs)
        self.kwargs = kwargs
        # feedback(f"\n$$$ CardShape KW=> {self.kwargs}")
        self.elements = []  # container for objects which get added to the card
        self.members = None
        self.card_bleed = None  # possible CardBleed namedtuple
        self.card_name = kwargs.get("card_name", None)  # prefix for card PNG images
        self.outline_shape = CardOutline(_object=_object, canvas=canvas, **kwargs)
        self.outline = self.outline_shape.get_outline(
            cnv=canvas, row=None, col=None, cid=None, label=None, **kwargs
        )
        self.image = kwargs.get("image", None)
        self.frame_geometry = ShapeGeometry()  # empty place-holder

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw an element on a given canvas."""
        raise NotImplementedError

    def draw_new_elements(
        self, the_function, new_eles, cnv, off_x, off_y, ID, cid, **kwargs
    ):
        """Draw a list of elements created via a Template or Card function call."""
        # feedback(f"$$$ CardShape elements  {new_eles}")
        for the_new_ele in new_eles:
            try:
                if isinstance(the_new_ele, GroupBase):
                    for new_group_ele in the_new_ele:
                        new_group_ele.draw(
                            cnv=cnv, off_x=off_x, off_y=off_y, ID=ID, **kwargs
                        )
                        cnv.commit()
                else:
                    the_new_ele.draw(cnv=cnv, off_x=off_x, off_y=off_y, ID=ID, **kwargs)
                    cnv.commit()
            except AttributeError:
                feedback(
                    f"Unable to draw card #{cid + 1}. Check that the elements"
                    f" created by '{the_function.__name__}' are all shapes.",
                    True,
                )

    def get_geometry(
        self, frame_type: CardFrame, bbox: BBox, vertices: list
    ) -> ShapeGeometry:
        """Geometry of Card frame.

        Notes:
            * Used by user defined card functions (UDF)
        """
        _type = type(self)
        cntr = Point(
            bbox.tl.x + (bbox.br.x - bbox.tl.x) / 2.0,
            bbox.tl.y + (bbox.br.y - bbox.tl.y) / 2.0,
        )
        cntr_user = self.as_point(cntr, self.units, None, None)
        user_vertices = self._l2v(vertices, margin_offset=True)  # handle margins
        # for i,v in enumerate(user_vertices): print(f'$$$ {frame_type} {i=} {v=}')
        n, ne, nw, e, se, s, sw, w = None, None, None, None, None, None, None, None
        nnw, nne, sse, ssw = None, None, None, None  # pointy hex
        wnw, ene, ese, wsw = None, None, None, None  # flat hex
        perim, radius, diameter, height, width, side, area = (
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        )
        match frame_type:
            case CardFrame.RECTANGLE:
                # user_vertices => clockwise from top-right
                ne = user_vertices[0]
                se = user_vertices[1]
                sw = user_vertices[2]
                nw = user_vertices[3]
                height = self.height
                width = self.width
                area = height * width
                perim = 2.0 * height + 2.0 * width
            case CardFrame.CIRCLE:
                radius = self.radius
                diameter = 2 * self.radius
                area = math.pi * radius**2
            case CardFrame.HEXAGON:
                #   5__4
                #   /  \
                # 0/    \3
                #  \    /
                #  1\__/2
                ne = user_vertices[4]
                e = user_vertices[3]
                se = user_vertices[2]
                sw = user_vertices[1]
                w = user_vertices[0]
                nw = user_vertices[5]
                # radius = self._p2v(hex_geom.radius)
                # diameter = self._p2v(hex_geom.diameter)
                # height = self._p2v(hex_geom.height_flat)
                # side = self._p2v(hex_geom.radius)
                # area = math.sqrt(3) * 3 / 2 * side**2
                # perim = 6 * side
            case _:
                raise NotImplementedError(
                    f"Outline cannot handle card frame type: {frame_type}"
                )

        _type = type(self)
        return ShapeGeometry(
            # centre
            centre=cntr_user,
            center=cntr_user,
            c=cntr_user,
            # vertices and perbii
            n=n,
            ne=ne,
            e=e,
            se=se,
            s=s,
            sw=sw,
            w=w,
            nw=nw,
            nnw=nnw,
            nne=nne,
            sse=sse,
            ssw=ssw,
            wnw=wnw,
            ene=ene,
            ese=ese,
            wsw=wsw,
            # length
            perimeter=perim,
            radius=radius,
            diameter=diameter,
            height=height,
            width=width,
            side=side,
            # other
            area=area,
            # meta
            t=_type,
            type=_type,
            shapetype=_type,
            name=self.simple_name(self),
        )

    def draw_card(self, cnv, row, col, cid, **kwargs):
        """Draw a Card on a given canvas.

        Pass on `deck_data` to other commands, as needed, for them to draw Shapes
        """

        from protograf.shapes import ImageShape, SequenceShape, RepeatShape, GridShape, DotGridShape
        from protograf.protos import PageBreak, TemplatingType

        def draw_element(new_ele, cnv, off_x, off_y, ID, **kwargs):
            """Allow customisation of kwargs before call to Shape's draw()."""
            # print(f'$$$ draw_card::draw_element {cnv} {ID=} {type(new_ele)=}')
            if isinstance(
                new_ele, (SequenceShape, RepeatShape, GridShape, DotGridShape)
            ):
                new_ele.deck_data = self.deck_data
                kwargs["card_width"] = self.width
                kwargs["card_height"] = self.height
                kwargs["card_x"] = base_frame_bbox.tl.x
                kwargs["card_y"] = base_frame_bbox.tl.y

            new_ele.draw(cnv, off_x, off_y, ID, **kwargs)

        # feedback(f'\n$$$ draw_card {cnv=} {cid=} {row=} {col=}')
        # feedback(f'$$$ draw_card  {cid=} KW=> {kwargs}')
        is_card_back = kwargs.get("card_back", False)
        image = kwargs.get("image", None)
        right_gap = kwargs.get("right_gap", 0.0)  # gap between end-of-cards & page edge
        card_grid = kwargs.get("card_grid", None)

        # ---- draw outline
        label = "ID:%s" % cid if self.show_id else ""
        shape_kwargs = copy_object.copy(kwargs)
        shape_kwargs["is_cards"] = True
        if not is_card_back:
            shape_kwargs["fill"] = kwargs.get("fill", kwargs.get("bleed_fill", None))
        else:
            shape_kwargs["fill"] = None
        shape_kwargs.pop("image_list", None)  # do NOT draw linked image
        shape_kwargs.pop("image", None)  # do NOT draw get_outline(linked image
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
        # feedback(f'$$$ 366 {right_gap=} {self.offset_x=} {move_x=}')
        # feedback(f'$$$ 367 {shape_kwargs["frame_type"]=} {shape_kwargs["grid_marks"]=}')
        # feedback(f"$$$ 368 {outline=} {shape_kwargs=}")

        # ---- draw card bleed
        if self.card_bleed:
            # print(f"$$$ 372 {cid=} {self.elements=} {self.card_bleed=}")
            bleed_kwargs = copy_object.copy(shape_kwargs)
            bleed_kwargs["fill"] = self.card_bleed.fill
            bleed_kwargs["stroke"] = self.card_bleed.fill
            bleed_kwargs["bleed_x"] = self.card_bleed.offset_x
            bleed_kwargs["bleed_y"] = self.card_bleed.offset_y
            bleed_kwargs["bleed_radius"] = self.card_bleed.offset_radius
            bleed_kwargs["grid_marks"] = None
            # calculate size for bleed
            bleed_shape = CardOutline(_object=None, canvas=cnv, **bleed_kwargs)
            bleed_outline = bleed_shape.get_outline(
                cnv=cnv, row=row, col=col, cid=cid, label=label, **bleed_kwargs
            )
            # feedback(f"$$$ 386 {cid=} {type(bleed_outline)=} {bleed_kwargs=}")
            bleed_outline.draw(off_x=move_x, off_y=0, **bleed_kwargs)  # NO grid_marks!

        # feedback(f'$$$ draw_card::OUTLINE {cid=} {row=} {col=} {outline._o=}') # KW=> {shape_kwargs}
        outline.draw(
            off_x=move_x, off_y=0, **shape_kwargs
        )  # inc. grid_marks; globals.canvas

        # ---- track frame outlines for possible image extraction
        match kwargs["frame_type"]:
            case CardFrame.RECTANGLE:
                fr_vertices = outline._shape_vertexes  # clockwise from top-right
                base_frame_bbox = BBox(tl=fr_vertices[3], br=fr_vertices[1])
            case CardFrame.CIRCLE:
                fr_vertices = []
                base_frame_bbox = outline.bbox
            case CardFrame.HEXAGON:
                fr_vertices = outline._shape_vertexes  # anti-clockwise from mid-left
                # print(f"$$$ HEXAGON {fr_vertices=}")
                # _vvs = self._l2v(fr_vertices)
                # for i,v in enumerate(_vvs): print(f'$$$ HEX-V {i=} {v=}')
                #   5__4
                #   /  \
                # 0/    \3
                #  \    /
                #  1\__/2
                base_frame_bbox = BBox(
                    tl=Point(fr_vertices[0].x, fr_vertices[5].y),
                    br=Point(fr_vertices[3].x, fr_vertices[2].y),
                )
            case _:
                raise NotImplementedError(
                    f'Outline cannot handle card frame type: {kwargs["frame_type"]}'
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
                        # print('$$$ HEX ODD BACK {_dx=}')
                    else:
                        _dx = _dx + side + outline.spacing_x
            case _:
                raise NotImplementedError(
                    f'Cannot handle card frame type: {kwargs["frame_type"]}'
                )

        # ---- set x-shift to align card backs and fronts (elements)
        if is_card_back:
            _dx = _dx + move_x

        # ---- track/update frame and store card fronts (plus card name)
        if not is_card_back:
            mx = self.unit(_dx or 0) + self._o.delta_x
            my = self.unit(_dy or 0) + self._o.delta_y
            # print(f"$$$ {mx=} {my=} {frame_width=} {frame_height=}")
            frame_bbox = BBox(
                tl=Point(mx, my), br=Point(mx + frame_width, my + frame_height)
            )
            page = kwargs.get("page_number", 0)
            _cframe = (frame_bbox, self.card_name)
            # store for use by pdf_cards_to_png()
            if page not in globals.card_frames:
                globals.card_frames[page] = [_cframe]
            else:
                globals.card_frames[page].append(_cframe)
        else:
            frame_bbox = base_frame_bbox

        # ---- set card frame geometry
        self.frame_geometry = self.get_geometry(
            kwargs["frame_type"], frame_bbox, fr_vertices
        )

        # ---- draw card grid for Rectangle cards
        if card_grid and kwargs["frame_type"] == CardFrame.RECTANGLE:
            _card_grid = tools.as_float(card_grid, "card_grid")
            mx = self.unit(_dx or 0) + self._o.delta_x
            my = self.unit(_dy or 0) + self._o.delta_y
            stroke = colrs.get_color(globals.debug_color)
            grid_size = _card_grid * globals.units
            cols = int(frame_width // grid_size)
            rows = int(frame_height // grid_size)
            for col in range(1, cols + 1):
                globals.doc_page.draw_line(
                    (mx + col * grid_size, my),
                    (mx + col * grid_size, my + frame_height),
                    color=stroke,
                    width=0.1,
                )
            for row in range(1, rows + 1):
                globals.doc_page.draw_line(
                    (mx, my + row * grid_size),
                    (mx + frame_width, my + row * grid_size),
                    color=stroke,
                    width=0.1,
                )

        # ---- draw card elements
        flat_elements = tools.flatten(self.elements)
        # print(f"$$$ draw_card ELEMENTS {flat_elements=} ")
        if cnv != globals.canvas:
            # required because cnv was not reset for first page when using gutter option
            # print(f"$$$ draw_card CANVAS {globals.page.current=}")
            cnv = globals.canvas
        for index, flat_ele in enumerate(flat_elements):
            # ---- * replace image source placeholder
            if image and isinstance(flat_ele, ImageShape):
                if _lower(flat_ele.kwargs.get("source", "")) in ["*", "all"]:
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
                new_ele = self.handle_custom_values(flat_ele, cid)  # calculated values
                # feedback(f'$$$ CS draw_card ele $$$ {type(new_ele)=}')
                if isinstance(
                    new_ele, (SequenceShape, RepeatShape, GridShape, DotGridShape)
                ):
                    new_ele.deck_data = self.deck_data
                    kwargs["card_width"] = self.width
                    kwargs["card_height"] = self.height
                    kwargs["card_x"] = base_frame_bbox.tl.x
                    kwargs["card_y"] = base_frame_bbox.tl.y
                    draw_element(
                        new_ele=new_ele, cnv=cnv, off_x=_dx, off_y=_dy, ID=iid, **kwargs
                    )
                    cnv.commit()
                elif isinstance(new_ele, TemplatingType):
                    # convert Template into a string via render
                    card_value = self.deck_data[iid]
                    custom_value = new_ele.template.render(card_value)
                    _one_or_more_eles = new_ele.function(custom_value)
                    if isinstance(_one_or_more_eles, list):
                        new_eles = _one_or_more_eles
                    else:
                        new_eles = (
                            [
                                _one_or_more_eles,
                            ]
                            if _one_or_more_eles
                            else []
                        )
                    self.draw_new_elements(
                        new_ele.function,
                        new_eles,
                        cnv=cnv,
                        off_x=_dx,
                        off_y=_dy,
                        ID=iid,
                        cid=cid,
                        **kwargs,
                    )
                else:
                    if callable(new_ele) and not isinstance(
                        new_ele, (BaseShape, Switch)
                    ):
                        # call user defined card function or function-like object # UDF
                        try:
                            card_values = self.deck_data[cid]
                        except (IndexError, TypeError):  # may not be any deck_data
                            card_values = {}
                        card_values["geo"] = self.frame_geometry
                        Data = namedtuple("Data", card_values.keys())
                        card_values_tuple = Data(**card_values)
                        try:
                            _one_or_more_eles = new_ele(card_values_tuple) or []
                        except Exception as err:
                            e_n = type(err).__name__
                            fname = new_ele.__name__
                            feedback(
                                f"Unable to create card #{cid + 1}. ({e_n}: {err} for '{fname}' function)",
                                True,
                            )
                        if isinstance(_one_or_more_eles, list):
                            new_eles = _one_or_more_eles
                        else:
                            new_eles = (
                                [
                                    _one_or_more_eles,
                                ]
                                if _one_or_more_eles
                                else []
                            )
                        # print(f'{card_values_tuple=} {new_eles=}')
                        self.draw_new_elements(
                            new_ele,
                            new_eles,
                            cnv=cnv,
                            off_x=_dx,
                            off_y=_dy,
                            ID=iid,
                            cid=cid,
                            **kwargs,
                        )
                    else:
                        draw_element(
                            new_ele=new_ele,
                            cnv=cnv,
                            off_x=_dx,
                            off_y=_dy,
                            ID=iid,
                            **kwargs,
                        )
                        cnv.commit()
            except AttributeError:
                # ---- * switch ... get a new element ... or not!?
                try:
                    new_ele = (
                        flat_ele(cid=self.shape_id) if flat_ele else None
                    )  # uses __call__ on Switch
                    if new_ele:
                        flat_new_eles = tools.flatten(new_ele)
                        for flat_new_ele in flat_new_eles:
                            members = flat_new_ele.members or self.members
                            iid = members.index(cid + 1)
                            # feedback(f'$$$ draw_card $$$ {iid=} {flat_new_ele=}')
                            custom_new_ele = self.handle_custom_values(
                                flat_new_ele, iid
                            )
                            # feedback(f'$$$ draw_card $$$ {iid=} {custom_new_ele=}')
                            if isinstance(custom_new_ele, (SequenceShape, RepeatShape)):
                                custom_new_ele.deck_data = self.deck_data
                            # feedback(f'$$$ draw_card $$$ {self.shape_id=} {custom_new_ele=}')
                            draw_element(
                                new_ele=custom_new_ele,
                                cnv=cnv,
                                off_x=_dx,
                                off_y=_dy,
                                ID=iid,
                                **kwargs,
                            )
                            cnv.commit()
                except Exception as err:
                    feedback(f"Unable to create card #{cid + 1}. (Error: {err})", True)
            except Exception as err:
                t_b = sys.exc_info()[2]
                e_n = type(err).__name__
                feedback(
                    f"Unable to draw card #{cid + 1}. ({e_n}: {err} on line: {t_b.tb_lineno})",
                    True,
                )


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
        from protograf.protos import PageMargins, page_setup
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
        """Draw card bleed."""
        # ---- bleed area for page (default)
        from protograf.shapes import RectangleShape
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
                                rkwargs = copy_object.copy(kwargs)
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
            from protograf.protos import PageMargins, page_setup
            self.prime_globals = tools.save_globals()
            globals_page = copy_object.copy(globals.page)
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
            from protograf.protos import PageBreak, page_setup
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
