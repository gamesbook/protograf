# -*- coding: utf-8 -*-
"""
Create Polygon shape for protograf
"""
# lib
from functools import cached_property
import logging
import math

# third party
from pymupdf import Point as muPoint

# local
from protograf import globals
from protograf.shapes_utils import draw_line
from protograf.utils import colrs, geoms, tools
from protograf.utils.tools import _lower
from protograf.utils.messaging import feedback
from protograf.utils.structures import (
    BBox,
    DirectionGroup,
    Perbis,
    Point,
    PolyGeometry,
    Radius,
    ShapeGeometry,
    Vertex,
)  # named tuples
from protograf.base import BaseShape

log = logging.getLogger(__name__)
DEBUG = False


class PolygonShape(BaseShape):
    """
    Regular Polygon on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super().__init__(_object=_object, canvas=canvas, **kwargs)
        self.use_diameter = self.is_kwarg("diameter")
        self.use_height = self.is_kwarg("height")
        self.use_width = self.is_kwarg("width")
        self.use_radius = self.is_kwarg("radius")
        self.calculated_left = None
        self.calculated_top = None
        # ---- perform overrides
        if self.perbii:
            if isinstance(self.perbii, str):
                if _lower(self.perbii) in ["all", "*"]:
                    sides = tools.as_int(self.sides, label="sides", minimum=1)
                    self.perbii = list(range(1, sides + 1))
                else:
                    self.perbii = tools.sequence_split(self.perbii)
            if not isinstance(self.perbii, list):
                feedback("The perbii value must be a list of numbers!", True)
        if self.cx is not None and self.cy is not None:
            self.x, self.y = self.cx, self.cy
        # ---- RESET UNIT PROPS (last!)
        self.set_unit_properties()

    @cached_property
    def shape_area(self) -> float:
        """Area of Polygon."""
        return self._p2v(self._shape_area)

    @cached_property
    def shape_centre(self) -> Point:
        """Centre of Polygon"""
        return Point(
            self._p2v(self._shape_centre.x, 3), self._p2v(self._shape_centre.y, 3)
        )

    @cached_property
    def shape_vertices(self) -> dict:
        """Vertices of Polygon."""
        vtc = self._shape_vertexes_named
        shape_vtc = {
            key: Point(self._p2v(value.point.x, 3), self._p2v(value.point.y, 3))
            for key, value in vtc.items()
        }
        return shape_vtc

    @cached_property
    def shape_perbii(self) -> dict:
        """Perbii of Polygon."""
        return {}

    @cached_property
    def shape_geom(self) -> ShapeGeometry:
        """Geometry of Polygon."""
        return ShapeGeometry()

    @cached_property
    def geom(self) -> ShapeGeometry:
        """Geometry of Polygon - alias for shape_geom."""
        return self.shape_geom

    @cached_property
    def _shape_area(self) -> float:
        """Area of Polygon in points."""
        sides = tools.as_int(self.sides, label="sides", minimum=1)
        area = (sides * self._shape_radius**2 / 2.0) * math.sin(2.0 * math.pi / sides)
        return area

    @cached_property
    def _shape_centre(self) -> Point:
        """Centre of Polygon in points"""
        if self.cx is not None and self.cy is not None:
            x = self._u.cx + self._o.delta_x
            y = self._u.cy + self._o.delta_y
        else:
            x = self._u.x + self._o.delta_x
            y = self._u.y + self._o.delta_y
        # recalculate centre if preset
        if self.use_abs_c:
            if self._abs_cx is not None and self._abs_cy is not None:
                x = self._abs_cx
                y = self._abs_cy
        return Point(x, y)

    @cached_property
    def _shape_radius(self) -> float:
        """Radius of Polygon in points."""
        if self.radius and self.use_radius:
            radius = self._u.radius
        elif self.diameter and self.use_diameter:
            radius = self._u.diameter / 2.0
        elif self.height and self.use_height:
            radius = self._u.height / 2.0
        elif self.width and self.use_width:
            radius = self._u.width / 2.0
        else:
            side = self._u.side
            sides = int(self.sides)
            # 180 degrees is math.pi radians
            radius = side / (2.0 * math.sin(math.pi / sides))
        return radius

    @cached_property
    def _shape_vertexes(self):
        """Vertices of Polygon in points."""
        the_geom = self.get_geometry()
        vertices = the_geom.vertices
        # for p in vertices: print(f'*POLYGON* vtx: {p.x / 28.3465}, {p.y / 28.3465}')
        if the_geom.sides & 1 == 1:  # odd no.of sides
            # move back so the vertices start at "top right"
            vertices_shift = vertices[1:] + vertices[0:1]
            return vertices_shift
        return vertices

    @cached_property
    def _shape_vertexes_named(self):
        """Named (by number) vertices of Polygon."""
        vertices = self._shape_vertexes
        vertex_dict = {}
        for key, vertex in enumerate(vertices):
            _vertex = Vertex(
                point=vertex,
                direction=key + 1,
            )
            vertex_dict[key + 1] = _vertex
        return vertex_dict

    def draw_mesh(self, cnv, ID):
        """Lines connecting each vertex to mid-points of opposing sides."""
        feedback("Mesh for Polygon is not yet implemented.", alert=True)
        vertexes = self._shape_vertexes
        log.debug("%s %s %s", cnv, ID, vertexes)
        # TODO - autodraw (without dirs)

    def get_angles(self) -> list:
        """Angles of lines connecting the Polygon centre to each of the vertices.

        NOTE:
            Used by other Shapes e.g. Track
        """
        pre_geom = self.get_geometry()
        x, y, vertices = (
            pre_geom.x,
            pre_geom.y,
            pre_geom.vertices,
        )
        # for p in vertices: print(f'*POLYG vert x={self._p2v(p.x)} y={self._p2v(p.y)}')
        angles = []
        for vertex in vertices:
            _, angle = geoms.angles_from_points(Point(x, y), vertex)
            angles.append(angle)
        return angles

    def calculate_perbii(self, centre: Point, **kwargs) -> dict:
        """Calculate centre points for each Polygon edge and angles from centre.

        Args:
            centre (Point):
                the centre Point of the Polygon

        Returns:
            dict of Perbis objects keyed on direction number
        """
        perbii_dict = {}
        _perbii_pts = []
        _vertices = self._shape_vertexes
        the_geom = self.get_geometry()
        if the_geom.sides & 1 == 1:  # odd no.of sides
            vertices = _vertices
        else:  # even no.of sides
            vertices = _vertices[2:] + _vertices[0:2]
        # print(f"*** POLYGON *** \n{_vertices=}\n{vertices=}")
        vcount = len(_vertices) - 1
        for key, vertex in enumerate(_vertices):
            # print(f"*** POLYGON *** vertex {key=} {vertex=}")
            if key == 0:
                p1 = Point(vertex.x, vertex.y)
                p2 = Point(vertices[vcount].x, vertices[vcount].y)
            else:
                p1 = Point(vertex.x, vertex.y)
                p2 = Point(vertices[key - 1].x, vertices[key - 1].y)
            # print(f"*** POLYGON *** perbii {key=} {p1=} {p2=}")
            pc = geoms.fraction_along_line(p1, p2, 0.5)  # centre pt of edge
            _perbii_pts.append(pc)
            compass, angle = geoms.angles_from_points(centre, pc)
            angle = 360.0 - angle if angle > 0.0 else angle
            # print(f"*** POLYGON *** perbii {key=} {pc=} {compass=} {angle=}")
            _perbii = Perbis(
                point=pc,
                direction=key + 1,
                v1=p1,
                v2=p2,
                compass=compass,
                angle=angle,
            )
            # print(f"*** POLYGON *** perbii {key=} {_perbii=}")
            perbii_dict[key + 1] = _perbii
        if kwargs.get("debug"):
            pass
            # self.run_debug = True
            # self._debug(cnv, vertices=_perbii_pts)
        return perbii_dict

    def calculate_radii(
        self,
        centre: Point,
        poly_vertices: list,
    ) -> dict:
        """Calculate radii for each Polygon vertex and angles from centre.

        Args:
            poly_vertices: list of Polygon's nodes as Points
            centre: the centre Point of the Polygon

        Returns:
            dict of Radius objects keyed on direction
        """
        radii_dict = {}
        vertices = poly_vertices  # [::-1] # reversed
        # print(f"*** POLYGON radii {centre=} {vertices=}")
        for key, vertex in enumerate(vertices):
            compass, angle = geoms.angles_from_points(centre, vertex)
            # print(f"*** POLYGON radii {key=} {directions[key]=} {compass=} {angle=}")
            _radii = Radius(
                point=vertex,
                direction=key + 1,
                compass=compass,
                angle=360 - angle,  # inverse flip (y is reveresed)
            )
            # print(f"*** POLYGON radii {_radii=} {self.fill=}")
            radii_dict[key + 1] = _radii
        return radii_dict

    def draw_perbii(
        self,
        cnv,
        ID,
        centre: Point,
        rotation: float = None,
    ):
        """Draw lines connecting the Polygon centre to the centre of each edge.

        Def:
            A perpendicular bisector ("perbii") of a chord is:
            A line passing through the center of circle such that it divides the
            chord into two equal parts and meets the chord at a right angle;
            for a polygon, each edge is effectively a chord.
        """
        pb_offset = self.unit(self.perbii_offset, label="perbii offset") or 0
        pb_length = (
            self.unit(self.perbii_length, label="perbii length")
            if self.perbii_length
            else self._shape_radius
        )
        centre = centre or self._shape_centre
        perbii_dict = self.calculate_perbii(centre)
        # ---- set perbii waves
        lkwargs = {}
        lkwargs["wave_style"] = self.kwargs.get("perbii_wave_style", None)
        lkwargs["wave_height"] = self.kwargs.get("perbii_wave_height", 0)
        for key in self.perbii:
            # points based on length of line, offset and the angle in degrees
            the_perbii = perbii_dict.get(int(key), None)
            # print(f'*** POLYGON {key=} {the_perbii.v1=} {the_perbii.v2=}')
            if the_perbii is None:
                feedback(f"{key} is not a valid perbii direction!", True)
            edge_pt = geoms.fraction_along_line(
                the_perbii.v1, the_perbii.v2, 0.5
            )  # centre pt of edge
            # print(f'*** POLYGON {pb_angle=} {edge_pt=} {centre=}')
            if pb_offset is not None and pb_offset != 0:
                offset_pt = geoms.point_on_circle(centre, pb_offset, the_perbii.angle)
                end_pt = geoms.point_on_line(offset_pt, edge_pt, pb_length)
                start_point = offset_pt.x, offset_pt.y
                end_point = end_pt.x, end_pt.y
            else:
                start_point = centre.x, centre.y
                end_point = edge_pt.x, edge_pt.y
            # ---- draw a perbii line
            draw_line(
                cnv,
                start_point,
                end_point,
                shape=self,
                **lkwargs,
            )

        # ---- style all perbii
        rotation_point = centre if rotation else None
        # print(f"*** POLYGON perbii {len(vertices)=} {rotation_point=} {rotation=}")
        self.set_canvas_props(
            index=ID,
            stroke=self.perbii_stroke,
            stroke_width=self.perbii_stroke_width,
            stroke_ends=self.perbii_ends,
            dashed=self.perbii_dashed,
            dotted=self.perbii_dotted,
            rotation=rotation,
            rotation_point=rotation_point,
        )

    def draw_radii(
        self,
        cnv,
        ID,
        centre: Point,
        rotation: float = None,
    ):
        """Draw lines connecting the Polygon centre to each of the vertices."""
        _radii = []
        vertices = self._shape_vertexes
        _dirs = tools.validated_directions(
            self.radii, DirectionGroup.POLYGONAL, "polygon radii", len(vertices)
        )
        for key, vertex in enumerate(vertices):
            if key + 1 in _dirs:
                _, angle = geoms.angles_from_points(vertex, centre)
                # compass, angle = geoms.angles_from_points(vertex, centre)
                mirror_angle = 180 - angle
                # print(f'*** POLYGON {key+1=} {vertex=} {compass=} {mirror_angle=}')
                _radii.append(mirror_angle)
        rad_offset = self.unit(self.radii_offset, label="radii offset") or 0
        rad_length = (
            self.unit(self.radii_length, label="radii length")
            if self.radii_length
            else self._shape_radius
        )
        # ---- set radii styles
        lkwargs = {}
        lkwargs["wave_style"] = self.kwargs.get("radii_wave_style", None)
        lkwargs["wave_height"] = self.kwargs.get("radii_wave_height", 0)
        for rad_angle in _radii:
            # points based on length of line, offset and the angle in degrees
            diam_pt = geoms.point_on_circle(centre, rad_length, rad_angle)
            if rad_offset is not None and rad_offset != 0:
                offset_pt = geoms.point_on_circle(centre, rad_offset, rad_angle)
                end_pt = geoms.point_on_line(offset_pt, diam_pt, rad_length)
                # print('*** POLYGON', rad_angle, offset_pt, f'{x_c=}, {y_c=}')
                start_point = offset_pt.x, offset_pt.y
                end_point = end_pt.x, end_pt.y
            else:
                start_point = centre.x, centre.y
                end_point = diam_pt.x, diam_pt.y
            # ---- draw a radii line
            draw_line(
                cnv,
                start_point,
                end_point,
                shape=self,
                **lkwargs,
            )

        # ---- style all radii
        rotation_point = centre if rotation else None
        # print(f"*** POLYGON radii {rotation_point=} {rotation=}")
        self.set_canvas_props(
            cnv=cnv,
            index=ID,
            stroke=self.radii_stroke,
            stroke_width=self.radii_stroke_width,
            dashed=self.radii_dashed,
            dotted=self.radii_dotted,
            rotation=rotation,
            rotation_point=rotation_point,
        )

    def draw_slices(self, cnv, ID, centre: Point, rotation=0):
        """Draw triangles inside the Polygon

        Args:
            ID: unique ID
            vertexes: list of Polygon's nodes as Points
            centre: the centre Point of the Polygon
            rotation: degrees anti-clockwise from horizontal "east"
        """
        vertexes = self._shape_vertexes
        # ---- get slices color list from string
        if isinstance(self.slices, str):
            _slices = tools.split(self.slices.strip())
        else:
            _slices = self.slices
        # ---- validate slices color settings
        slices_colors = [
            colrs.get_color(slcolor)
            for slcolor in _slices
            if not isinstance(slcolor, bool)
        ]
        # ---- draw triangle per slice; iterate through colors as needed!
        # print(f'*** POLYGON {slices_colors=} {vertexes=}')
        cid = 0
        for vid, vertex in enumerate(vertexes):
            scolor = slices_colors[cid]
            vnext = vid + 1 if vid < len(vertexes) - 1 else 0
            vertexes_slice = [vertex, centre, vertexes[vnext]]
            cnv.draw_polyline(vertexes_slice)
            self.set_canvas_props(
                index=ID,
                stroke=self.slices_stroke or scolor,
                stroke_ends=self.slices_ends,
                fill=scolor,
                transparency=self.slices_transparency,
                closed=True,
                rotation=rotation,
                rotation_point=muPoint(centre[0], centre[1]),
            )
            cid += 1
            if cid > len(slices_colors) - 1:
                cid = 0

    def get_geometry(self, rotation: float = None):
        """Calculate centre, radius, side, vertices and sides of Polygon."""
        centre = self._shape_centre
        x, y = centre.x, centre.y
        side, half_flat = 0.0, 0.0
        # ---- calculate side and half_flat
        if self.height:
            side = self._u.height / math.sqrt(3)
            half_flat = self._u.height / 2.0
        elif self.diameter:
            side = self._u.diameter / 2.0
            self._u.side = side
            half_flat = self._u.side * math.sqrt(3) / 2.0
        elif self.radius:
            side = self._u.radius
            half_flat = side * math.sqrt(3) / 2.0
        else:
            feedback(
                "Polygon needs either a valid height, or diameter, or radius", True
            )
        sides = tools.as_int(self.sides, label="sides", minimum=1)
        # ---- calculate vertices - assumes x,y marks the centre point
        vertices = geoms.polygon_vertices(
            sides, self._shape_radius, Point(x, y), rotation
        )
        # for p in vertices: print(f'*PG-V* {p.x / 28.3465}, {p.y / 28.3465}')
        return PolyGeometry(x, y, self._shape_radius, side, half_flat, vertices, sides)

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw a regular Polygon on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- calc centre (in units)
        centre = self._shape_centre
        x, y = centre.x, centre.y
        # ---- handle rotation
        rotation = self.kwargs.get("rotation", self.rotation)
        if rotation:
            self.centroid = muPoint(x, y)
            kwargs["rotation"] = rotation
            kwargs["rotation_point"] = self.centroid
        # ---- calculate vertices
        pre_geom = self.get_geometry()
        x, y, radius = (
            pre_geom.x,
            pre_geom.y,
            pre_geom.radius,
        )
        self._debug(cnv, vertices=self._shape_vertexes)
        # ---- new x/y per col/row
        is_cards = kwargs.get("is_cards", False)
        if self.row is not None and self.col is not None and is_cards:
            if self.kwargs.get("grouping_cols", 1) == 1:
                x = (
                    self.col * (self._u.radius * 2.0 + self._u.spacing_x)
                    + self._o.delta_x
                    + self._u.radius
                    + self._u.offset_x
                )
            else:
                group_no = self.col // self.kwargs["grouping_cols"]
                x = (
                    self.col * self._u.radius * 2.0
                    + self._u.spacing_x * group_no
                    + self._o.delta_x
                    + self._u.radius
                    + self._u.offset_x
                )
            if self.kwargs.get("grouping_rows", 1) == 1:
                y = (
                    self.row * (self._u.radius * 2.0 + self._u.spacing_y)
                    + self._o.delta_y
                    + self._u.radius
                    + self._u.offset_y
                )
            else:
                group_no = self.row // self.kwargs["grouping_rows"]
                y = (
                    self.row * self._u.radius * 2.0
                    + self._u.spacing_y * group_no
                    + self._o.delta_y
                    + self._u.radius
                    + self._u.offset_y
                )
            self.x_c, self.y_c = x, y
            self.bbox = BBox(
                tl=Point(self.x_c - self._u.radius, self.y_c - self._u.radius),
                br=Point(self.x_c + self._u.radius, self.y_c + self._u.radius),
            )
        # ---- invalid polygonArrow
        if not self._shape_vertexes or len(self._shape_vertexes) == 0:
            return

        # ---- determine ordering
        base_ordering = [
            "base",
            # "borders",
            "slices",
            "mesh",
            "radii",
            "perbii",
            "radii_shapes",
            "perbii_shapes",
            "centre_shape",
            "centre_shapes",
            "vertex_shapes",
            "dot",
            "cross",
            "text",
        ]
        ordering = base_ordering
        # feedback(f'*** POLYGON: {ordering=}')
        if self.order_all:
            ordering = tools.list_ordering(base_ordering, self.order_all, only=True)
        else:
            if self.order_first:
                ordering = tools.list_ordering(
                    base_ordering, self.order_first, start=True
                )
            if self.order_last:
                ordering = tools.list_ordering(base_ordering, self.order_last, end=True)

        # ---- draw in ORDER
        for item in ordering:
            if item == "base":
                # ---- * draw polygon
                # feedback(f"*** POLYGON {self.col=} {self.row=} {x=} {y=} \n{elf._shape_vertexes=}")
                cnv.draw_polyline(self._shape_vertexes)
                kwargs["closed"] = True
                self.set_canvas_props(cnv=cnv, index=ID, **kwargs)
            if item == "borders":
                # ---- * draw slices
                feedback("Polygon borders are not implemented yet!", True)
            if item == "slices":
                # ---- * draw slices
                if self.slices:
                    self.draw_slices(
                        cnv,
                        ID,
                        self._shape_centre,
                        rotation=rotation,
                    )
            if item == "radii":
                # ---- * draw radii
                if self.radii:
                    self.draw_radii(cnv, ID, self._shape_centre, rotation=rotation)
            if item == "perbii":
                # ---- * draw perbii
                if self.perbii:
                    self.draw_perbii(cnv, ID, self._shape_centre, rotation=rotation)
            if item == "mesh":
                # ---- * draw mesh
                if self.mesh:
                    self.draw_mesh(cnv, ID)
            if item == "radii_shapes":
                # ---- * draw radii_shapes
                if self.radii_shapes:
                    self.draw_radii_shapes(
                        cnv,
                        radii_shapes=self.radii_shapes,
                        vertexes=self._shape_vertexes,
                        centre=self._shape_centre,
                        direction_group=DirectionGroup.POLYGONAL,
                        rotation=rotation,
                        rotated=self.radii_shapes_rotated,
                    )
            if item == "perbii_shapes":
                # ---- * draw perbii_shapes
                if self.perbii_shapes:
                    self.draw_perbii_shapes(
                        cnv,
                        perbii_shapes=self.perbii_shapes,
                        vertexes=self._shape_vertexes,
                        centre=self._shape_centre,
                        direction_group=DirectionGroup.POLYGONAL,
                        rotation=rotation,
                        rotated=self.perbii_shapes_rotated,
                    )
            if item == "centre_shape":
                # ---- * draw centred shape (with offset)
                if self.centre_shape:
                    if self.can_draw_centred_shape(self.centre_shape):
                        self.centre_shape.draw(
                            _abs_cx=self._shape_centre.x
                            + self.unit(self.centre_shape_mx),
                            _abs_cy=self._shape_centre.y
                            + self.unit(self.centre_shape_my),
                        )
            if item == "centre_shapes":
                # ---- * draw centre_shapes (with offsets)
                if self.centre_shapes:
                    self.draw_centred_shapes(
                        self.centre_shapes, self._shape_centre.x, self._shape_centre.y
                    )
            if item == "vertex_shapes":
                # ---- * draw vertex shapes
                if self.vertex_shapes:
                    self.draw_vertex_shapes(
                        self.vertex_shapes,
                        self._shape_vertexes,
                        self._shape_centre,
                        self.vertex_shapes_rotated,
                    )
            if item == "debug":
                # ---- * draw debug; needs: self.run_debug = True
                pass
            if item == "dot":
                # ---- * draw dot
                self.draw_dot(cnv, self._shape_centre.x, self._shape_centre.y)
            if item == "cross":
                # ---- * draw cross
                self.draw_cross(
                    cnv,
                    self._shape_centre.x,
                    self._shape_centre.y,
                    rotation=kwargs.get("rotation"),
                )
            if item == "text":
                # ---- * draw text
                self.draw_heading(
                    cnv,
                    ID,
                    self._shape_centre.x,
                    self._shape_centre.y,
                    radius,
                    **kwargs,
                )
                self.draw_label(
                    cnv, ID, self._shape_centre.x, self._shape_centre.y, **kwargs
                )
                self.draw_title(
                    cnv,
                    ID,
                    self._shape_centre.x,
                    self._shape_centre.y,
                    radius + 0.5 * self.title_size,
                    **kwargs,
                )

        # ---- set calculated top-left in user units
        self.calculated_left = (x - self._u.radius) / self.units
        self.calculated_top = (x - self._u.radius) / self.units
