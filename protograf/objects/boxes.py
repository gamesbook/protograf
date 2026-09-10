# -*- coding: utf-8 -*-
"""
protograf box-like shapes
"""

# lib
# import os

# third party

# project
from protograf.base import BaseShape
from protograf.shapes.utils import draw_line
from protograf.utils import tools
from protograf.utils.messaging import feedback
from protograf.utils.structures import (  # named tuples
    Point,
    ShapeGeometry,
)


class CardBoxObject(BaseShape):
    """Draw CardBox outline on a given canvas.

    Reference:

    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super().__init__(_object=_object, canvas=canvas, **kwargs)
        self.kwargs = kwargs
        card_size = self.kwargs.get("card_size", "Poker")
        card_hw = tools.card_size(card_size, globals.margins.units_type)
        # ----  overrides to create sensible defaults
        if not kwargs.get("height"):
            self.height = card_hw[1]
        if not kwargs.get("width"):
            self.width = card_hw[0]
        if not kwargs.get("depth"):
            self.depth = 51.0 / globals.units  # ~ 1.8 cm or 0.7"
        # print(f'***  pos: {self.x=} {self.y=}')
        # print(f'*** size: {self.height=} {self.width=} {self.depth=}')
        self.set_unit_properties()
        # ---- user-selections
        _fg = kwargs.get("flap_glue", None)
        self._flap_glue = (
            tools.as_float(_fg, "flap_glue") * globals.units if _fg else None
        )
        _fi = kwargs.get("flap_inner", None)
        self._flap_inner = (
            tools.as_float(_fi, "flap_inner") * globals.units if _fi else None
        )
        _ft = kwargs.get("flap", None)
        self._flap_tuck = tools.as_float(_ft, "flap") * globals.units if _ft else None
        self._flap_size = 0  # NB!! see _shape_vertexes => calculated based on flap_tuck
        _th = kwargs.get("thumb", None)
        self._thumb = tools.as_float(_th, "thumb") * globals.units if _th else None
        self._padding = self.padding * globals.units if self.padding else None
        self._padding_width = (
            self.padding_width * globals.units if self.padding_width else self._padding
        )
        self._padding_height = (
            self.padding_height * globals.units
            if self.padding_height
            else self._padding
        )
        # ---- placeholders for user-defined items to be drawn
        self.shapes_front = kwargs.get("shapes_front", None)
        self.shapes_back = kwargs.get("shapes_back", None)
        self.shapes_left = kwargs.get("shapes_left", None)
        self.shapes_right = kwargs.get("shapes_right", None)
        self.shapes_top = kwargs.get("shapes_top", None)
        self.shapes_bottom = kwargs.get("shapes_bottom", None)
        self.shapes_wrap = kwargs.get("shapes_wrap", None)  # front,left,right,back
        # ---- vertices for panels
        # topleft, topright, bottomright, bottomleft
        self.panel_front = []
        self.panel_back = []
        self.panel_left = []
        self.panel_right = []
        self.panel_wrap = []
        # need placeholders because drawing order does not match
        self.panel_top = [None, None, None, None]
        self.panel_bottom = [None, None, None, None]
        # ---- set vertices and panel_* for point-based draw
        self.vertexes = self._shape_vertexes

    @property
    def shape_centre(self) -> Point:
        """Centre of CardBoxObject."""
        if self.cx and self.cy:
            return Point(self.cx, self.cy)
        return None

    @property
    def geo(self) -> ShapeGeometry:
        """Geometry of CardBoxObject in user units."""
        return ShapeGeometry()

    @property
    def geometry(self) -> ShapeGeometry:
        """Geometry of CardBoxObject - alias for geo."""
        return self.geo

    @property  # must be able to change e.g. for layout
    def _shape_vertexes(self):
        """Vertices and Panels of CardBoxObject in points."""

        def next_pt(ax, ay):
            vertices.append(Point(ax, ay))
            return ax, ay

        default_padding = 2 * 2.83465  # 2mm padding all round
        padding_height = (
            self._padding_height
            if self._padding_height is not None
            else default_padding
        )
        padding_width = (
            self._padding_width if self._padding_width is not None else default_padding
        )
        w_p = self._u.width + padding_width
        h_p = self._u.height + padding_height
        d_p = self._u.depth
        # ---- flaps
        flap = self._flap_inner if self._flap_inner is not None else 0.25 * w_p
        flap_tuck = self._flap_tuck if self._flap_tuck is not None else 0.15 * w_p
        if flap_tuck * 2.0 > w_p:
            feedback("Flap size cannot be greater than half of the box width.", True)
        self._flap_size = flap_tuck
        flap_glue = self._flap_glue if self._flap_glue is not None else 0.66 * d_p
        # print(f'*** size: {h_p=} {w_p=} {d_p=} {flap=} {flap_tuck=} {flap_glue=}')
        f_i_1 = 0.1
        f_i_2 = 0.8
        flap_offcut = flap_tuck  # create 45 deg angle OR use for quarter-round
        flap_midcut = w_p - 2 * flap_offcut

        # ---- vertices
        vertices = []
        offset_y = flap_tuck + d_p - flap
        sx, sy = (
            self._u.x + self._u.margin_left,
            self._u.y + self._u.margin_top + offset_y,
        )
        # ... TOP EDGE
        px, py = next_pt(sx, sy)  # 0
        self.panel_front.append(Point(px, py))  # TL
        self.panel_top[3] = Point(px, py)  # BL
        px, py = next_pt(px, py - d_p)  # 1
        self.panel_top[0] = Point(px, py)  # TL
        px, py = next_pt(px + flap_offcut, py - flap_tuck)  # 2
        px, py = next_pt(px + flap_midcut, py)  # 3
        px, py = next_pt(px + flap_offcut, py + flap_tuck)  # 4
        self.panel_top[1] = Point(px, py)  # TR
        px, py = next_pt(px, sy)  # 5
        self.panel_front.append(Point(px, py))  # TR
        self.panel_right.append(Point(px, py))  # TL
        self.panel_top[2] = Point(px, py)  # BR
        px, py = next_pt(px + f_i_1 * d_p, py - flap)  # 6
        px, py = next_pt(px + f_i_2 * d_p, py)  # 7
        px, py = next_pt(px + f_i_1 * d_p, py + flap)  # 8
        self.panel_right.append(Point(px, py))  # TR
        self.panel_back.append(Point(px, py))  # TL
        px, py = next_pt(px + w_p, py)  # 9
        self.panel_left.append(Point(px, py))  # TL
        self.panel_back.append(Point(px, py))  # TR
        px, py = next_pt(px + f_i_1 * d_p, py - flap)  # 10
        px, py = next_pt(px + f_i_2 * d_p, py)  # 11
        px, py = next_pt(px + f_i_1 * d_p, py + flap)  # 12
        self.panel_left.append(Point(px, py))  # TR
        # ... BOTTOM EDGE
        px, py = next_pt(px, py + h_p)  # 13
        self.panel_left.append(Point(px, py))  # BR
        px, py = next_pt(px - f_i_1 * d_p, py + flap)  # 14
        px, py = next_pt(px - f_i_2 * d_p, py)  # 15
        px, py = next_pt(px - f_i_1 * d_p, py - flap)  # 16
        self.panel_left.append(Point(px, py))  # BL
        self.panel_back.append(Point(px, py))  # BR
        self.panel_bottom[1] = Point(px, py)  # TR
        px, py = next_pt(px, py + d_p)  # 17
        self.panel_bottom[2] = Point(px, py)  # BR
        px, py = next_pt(px - flap_offcut, py + flap_tuck)  # 18
        px, py = next_pt(px - flap_midcut, py)  # 19
        px, py = next_pt(px - flap_offcut, py - flap_tuck)  # 20
        self.panel_bottom[3] = Point(px, py)  # BL
        px, py = next_pt(px, py - d_p)  # 21
        self.panel_back.append(Point(px, py))  # BL
        self.panel_bottom[0] = Point(px, py)  # TL
        self.panel_right.append(Point(px, py))  # BR
        px, py = next_pt(px - f_i_1 * d_p, py + flap)  # 22
        px, py = next_pt(px - f_i_2 * d_p, py)  # 23
        px, py = next_pt(px - f_i_1 * d_p, py - flap)  # 24
        self.panel_front.append(Point(px, py))  # BR
        self.panel_right.append(Point(px, py))  # BL
        px, py = next_pt(sx, py)  # 25
        self.panel_front.append(Point(px, py))  # BL
        # ... GLUE FLAP
        px, py = next_pt(px - flap_glue, py - 0.05 * h_p)  # 26
        px, py = next_pt(px, py - 0.9 * h_p)  # 27
        # ... START
        px, py = next_pt(sx, sy)  # 0

        # wrap
        # topleft, topright, bottomright, bottomleft
        self.panel_wrap = [
            self.panel_front[0],
            self.panel_left[1],
            self.panel_left[2],
            self.panel_front[3],
        ]

        return vertices

    def draw_item(self, item, area):
        """Draw one or shapes on an area of the card"""
        if item is None:
            return
        _cx = (area[1].x - area[0].x) / 2.0 + area[0].x
        _cy = (area[3].y - area[0].y) / 2.0 + area[0].y
        if isinstance(item, (list, tuple)):
            for shp in item:
                if shp is not None:
                    shp.draw(_abs_cx=_cx, _abs_cy=_cy)  # used by set_abs_and_offset()
        else:
            if item is not None:
                item.draw(_abs_cx=_cx, _abs_cy=_cy)  # used by set_abs_and_offset()

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw the CardBoxObject on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- draw outline by vertices
        # feedback(f'***CardBoxObject {x=} {y=} {self.vertexes=}')
        if self.vertexes:
            for key, vertex in enumerate(self.vertexes):
                if key < len(self.vertexes) - 1:
                    # ---- * curved flaps
                    if self.rounded and key in [1, 3, 17, 19]:
                        if key in [1, 17]:
                            midpt = Point(vertex.x, self.vertexes[key + 1].y)
                        else:
                            midpt = Point(self.vertexes[key + 1].x, vertex.y)
                        cnv.draw_curve(vertex, midpt, self.vertexes[key + 1])
                    else:
                        draw_line(
                            cnv, vertex, self.vertexes[key + 1], shape=self, **kwargs
                        )
                else:
                    draw_line(cnv, vertex, self.vertexes[0], shape=self, **kwargs)
            kwargs["closed"] = True
            if kwargs.get("rounded"):
                kwargs["lineJoin"] = 1
            self.set_canvas_props(cnv=cnv, index=ID, **kwargs)

        # ---- process folds (OVER any fill for box)
        if self.vertexes and self.fold:
            # ---- * set fold style
            pargs = {}
            pargs["stroke"] = self.fold_stroke
            pargs["stroke_width"] = self.fold_stroke_width
            pargs["dotted"] = self.fold_dotted
            pargs["dashed"] = self.fold_dashed
            pargs["closed"] = False
            pargs["fill"] = None
            # ----- * draw fold lines
            cnv.draw_line(self.panel_left[0], self.panel_left[1])
            cnv.draw_line(self.panel_left[2], self.panel_left[3])
            cnv.draw_line(self.panel_front[0], self.panel_front[3])
            cnv.draw_line(self.panel_front[1], self.panel_front[2])
            cnv.draw_line(self.panel_right[0], self.panel_right[1])
            cnv.draw_line(self.panel_right[2], self.panel_right[3])
            cnv.draw_line(self.panel_back[0], self.panel_back[3])
            cnv.draw_line(self.panel_back[1], self.panel_back[2])
            cnv.draw_line(self.panel_top[0], self.panel_top[1])
            cnv.draw_line(self.panel_top[2], self.panel_top[3])
            cnv.draw_line(self.panel_bottom[0], self.panel_bottom[1])
            cnv.draw_line(self.panel_bottom[2], self.panel_bottom[3])
            self.set_canvas_props(cnv=cnv, index=ID, **pargs)

        # ---- draw wrap-around shape/image
        self.draw_item(self.shapes_wrap, self.panel_wrap)
        # ---- draw front shape/image
        self.draw_item(self.shapes_front, self.panel_front)
        # ---- draw back shape/image
        self.draw_item(self.shapes_back, self.panel_back)
        # ---- draw top shape/image
        self.draw_item(self.shapes_top, self.panel_top)
        # ---- draw bottom shape/image
        self.draw_item(self.shapes_bottom, self.panel_bottom)
        # ---- draw left shape/image
        self.draw_item(self.shapes_left, self.panel_left)
        # ---- right shape/image
        self.draw_item(self.shapes_right, self.panel_right)

        # ---- draw thumb
        if self._thumb:
            midx = (
                self.panel_back[1].x - self.panel_back[0].x
            ) / 2.0 + self.panel_back[0].x
            tcentre = Point(midx, self.panel_back[1].y)
            tstart = Point(midx - (self._thumb / 2.0), self.panel_back[1].y)
            cnv.draw_sector(
                (tcentre.x, tcentre.y),
                (tstart.x, tstart.y),
                180,
                fullSector=False,
            )
            kwargs["closed"] = False
            kwargs["fill"] = None
            self.set_canvas_props(cnv=cnv, index=ID, **kwargs)
