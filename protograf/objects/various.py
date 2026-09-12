# -*- coding: utf-8 -*-
"""
protograf assorted shapes
"""

# lib
import logging
import math
import random

# third party

# module
from protograf import globals
from protograf.utils import geoms, tools
from protograf.utils.structures import (  # named tuples
    Point,
    ShapeGeometry,
)
from protograf.utils.messaging import feedback
from protograf.base import BaseShape
from protograf.shapes import (
    BandShape,
    CircleShape,
    PolygonShape,
    RectangleShape,
)

log = logging.getLogger(__name__)


class RaceTrackObject(BaseShape):
    """Draw RaceTrack composite shape on a given canvas.

    Reference:

    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super().__init__(_object=_object, canvas=canvas, **kwargs)
        self.kwargs = kwargs
        self.set_unit_properties()
        # ---- validate user-choices
        self.stages = kwargs.get("stages", None)
        if not self.stages:
            feedback(
                "The RaceTrack 'stages' property must be"
                " a list of one or more Rectangles and Bands.",
                True,
            )
        if not isinstance(self.stages, (list, tuple)):
            feedback(
                "The RaceTrack 'stages' property must be in the form of a list,"
                f" not a '{type(self.stages).__name__}'.",
                True,
            )
        for stage in self.stages:
            if not isinstance(stage, (RectangleShape, BandShape)):
                invalid = stage.simple_name()
                feedback(
                    f"Each stage must be either a Rectangle or a Band - not a {invalid}.",
                    True,
                    True,
                )

    @property
    def shape_centre(self) -> Point:
        """Centre of RaceTrackObject."""
        return None

    @property
    def geo(self) -> ShapeGeometry:
        """Geometry of RaceTrackObject in user units."""
        return ShapeGeometry()

    @property
    def geometry(self) -> ShapeGeometry:
        """Geometry of RaceTrackObject - alias for geo."""
        return self.geo

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw the RaceTrackObject on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- draw by stage
        old_stage, track_height = None, 0.0
        for key, stage in enumerate(self.stages):
            if key == 0:
                # print("\nstage:first")
                # FIRST stage ONLY - draw "as is"
                stage.draw()
                old_stage = stage
                # use settings of first stage to determine kwarg overrides
                track_height = stage.geo.height
            if key > 0:
                # print(key, type(stage), f"{old_stage.geo.nw=}", f"{old_stage.geo.sw=}")
                supplied_kwargs = stage.kwargs
                supplied_kwargs["height"] = track_height
                stage_type = type(stage)
                # coordinates of old_stage used to calculate props of this stage
                if getattr(old_stage, "inverted", False):
                    # previous curve was drawn bulging "inwards"
                    old_nw = old_stage.geo.se
                    old_sw = old_stage.geo.ne
                else:
                    old_nw = old_stage.geo.nw
                    old_sw = old_stage.geo.sw
                if isinstance(stage, RectangleShape):
                    # print("\nstage:rect")
                    new_center, new_rotation = geoms.racetrack_rectangle_properties(
                        ur=old_sw, lr=old_nw, width=stage.width
                    )
                    supplied_kwargs.pop("x", None)
                    supplied_kwargs.pop("y", None)
                    supplied_kwargs.pop("cxy", None)
                    supplied_kwargs["x"] = new_center.x - stage.width / 2.0
                    supplied_kwargs["y"] = new_center.y - track_height / 2.0
                    supplied_kwargs["rotation"] = 360.0 - new_rotation
                elif isinstance(stage, BandShape):
                    # print("\nstage:band")
                    if track_height > stage.radius:
                        feedback(
                            "The RaceTrack's adjusted Band height is greater than its radius",
                            True,
                            True,
                        )
                    corner_to_centre = stage.radius - track_height
                    if stage.inverted:  # draw with curve towards the "inside"
                        new_rotation = (
                            geoms.angle_between_points(first=old_nw, second=old_sw)
                            - stage.angle_width
                        )

                        pid = geoms.point_in_direction(
                            point_start=old_sw,
                            point_end=old_nw,
                            distance_factor=corner_to_centre / track_height,
                        )
                    else:
                        new_rotation = geoms.angle_between_points(
                            first=old_sw, second=old_nw
                        )

                        pid = geoms.point_in_direction(
                            point_start=old_nw,
                            point_end=old_sw,
                            distance_factor=corner_to_centre / track_height,
                        )

                    supplied_kwargs.pop("width", None)
                    supplied_kwargs["angle_start"] = new_rotation
                    supplied_kwargs["cx"] = pid.x
                    supplied_kwargs["cy"] = pid.y
                    # print(f"band {pid=} angle_start={new_rotation}")
                else:
                    raise ValueError(
                        f'A RaceTrack cannot contain shapes of type "{stage_type}"'
                    )
                shadow_stage = stage_type(canvas=globals.canvas, **supplied_kwargs)
                shadow_stage.draw()
                old_stage = shadow_stage


class StarFieldObject(BaseShape):
    """Draw StarField pattern on a given canvas.

    Reference:

        https://codeboje.de/starfields-and-galaxies-python/

    TODO:

        Implement the createElipticStarfield()
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super().__init__(_object=_object, canvas=canvas, **kwargs)
        self.kwargs = kwargs
        # override to set the randomisation sequence
        if self.seeding:
            self.seed = tools.as_float(self.seeding, "seeding")
        else:
            self.seed = None
        self.star_count = 0
        # validation
        for size in self.sizes:
            tools.as_float(size, 'the Starfield "size"', minimum=0.000000001)

    def draw_star(self, cnv, position: Point):
        """Draw a single star at a Point (x,y)."""
        color = self.colors[random.randint(0, len(self.colors) - 1)]
        size = self.sizes[random.randint(0, len(self.sizes) - 1)]
        # feedback(f'*** StarFld {color=} {size=} {position=}')
        cnv.draw_circle((position.x, position.y), size)
        self.set_canvas_props(cnv=cnv, index=None, stroke=color, fill=color)

    def cluster_stars(self, cnv):
        """Draw cluster of stars at a Point (x,y)."""
        feedback("CLUSTER NOT IMPLEMENTED", True)
        for _star in range(0, self.star_count):
            pass
        log.warning("No star cluster for %s", cnv)

    def random_stars(self, cnv):
        """Generate random star locations within an enclosing Shape."""
        # feedback(f'*** StarFld {self.enclosure=}')
        if isinstance(self.enclosure, CircleShape):
            ccentre = self.enclosure._shape_centre
            x_c, y_c = ccentre.x, ccentre.y
        if isinstance(self.enclosure, PolygonShape):
            _geom = self.enclosure.get_geometry()
            x_c, y_c, radius, vertices = _geom.x, _geom.y, _geom.radius, _geom.vertices
        stars = 0
        if self.seed:
            random.seed(self.seed)
        while stars < self.star_count:
            if isinstance(self.enclosure, RectangleShape):
                x_y = Point(
                    random.random() * self.enclosure._u.width + self._o.delta_x,
                    random.random() * self.enclosure._u.height + self._o.delta_y,
                )
            elif isinstance(self.enclosure, CircleShape):
                r_fraction = random.random() * self.enclosure._u.radius
                angle = math.radians(random.random() * 360.0)
                x = r_fraction * math.cos(angle) + x_c
                y = r_fraction * math.sin(angle) + y_c
                x_y = Point(x, y)
            elif isinstance(self.enclosure, PolygonShape):
                r_fraction = random.random() * radius
                angle = math.radians(random.random() * 360.0)
                x = r_fraction * math.cos(angle) + x_c
                y = r_fraction * math.sin(angle) + y_c
                x_y = Point(x, y)
                if not geoms.point_in_polygon(x_y, vertices):
                    continue
            else:
                feedback(f"{self.enclosure} IS NOT AN IMPLEMENTED SHAPE!", True)
            self.draw_star(cnv, x_y)
            stars += 1

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw StarField pattern on a given canvas."""
        kwargs = self.kwargs | kwargs
        cnv = cnv if cnv else globals.canvas  # a new Page/Shape may now exist
        super().draw(cnv, off_x, off_y, ID, **kwargs)  # unit-based props
        # ---- settings
        if self.enclosure is None:
            self.enclosure = RectangleShape()
        # ---- calculations
        random.seed()
        area = math.sqrt(self.enclosure._shape_area)
        self.star_count = round(self.density * self.points_to_value(area))
        # feedback(f'*** StarFld {self.star_pattern =} {self.enclosure}')
        # feedback(f'*** StarFld {area=} {self.density=} {self.star_count=}')
        # ---- set canvas
        self.set_canvas_props(index=ID)
        # ---- draw starfield
        if self.star_pattern in ["r", "random"]:
            self.random_stars(cnv)
        if self.star_pattern in ["c", "cluster"]:
            self.cluster_stars(cnv)
