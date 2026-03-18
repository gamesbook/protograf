# -*- coding: utf-8 -*-
"""
Support functions for Shapes for protograf
"""
# lib
import copy
import logging
from pathlib import Path
from urllib.parse import urlparse

# third party

# local
from protograf.base import (
    BaseShape,
)
from protograf.utils import geoms, tools
from protograf.utils.tools import _lower
from protograf.utils.constants import (
    BGG_IMAGES,
)
from protograf.utils.messaging import feedback
from protograf.utils.structures import (
    Point,
)  # named tuples
from protograf.utils.support import CACHE_DIRECTORY

log = logging.getLogger(__name__)
DEBUG = False


def set_cached_dir(source):
    """Set special cached directory, depending on source being a URL."""
    if not tools.is_url_valid(url=source):
        return None
    loc = urlparse(source)
    # print('*** @http@',  loc)
    # handle special case of BGG images
    # ... BGG gives thumb and original images the EXACT SAME filename :(
    if loc.netloc == BGG_IMAGES:
        subfolder = "images"
        if "thumb" in loc.path:
            subfolder = "thumbs"
        the_cache = Path(Path.home() / CACHE_DIRECTORY / "bgg" / subfolder)
        the_cache.mkdir(parents=True, exist_ok=True)
        return str(the_cache)
    return None


def draw_line(
    cnv=None, start: Point = None, end: Point = None, shape: BaseShape = None, **kwargs
) -> dict:
    """Draw a line on the canvas (Page) between two points for a Shape.

    Args:

        cnv (PyMuPDF Page object):
            where the line is drawn
        start (Point):
            start of the line
        end (Point):
            end of the line
        shape (BaseShape): shape
            for which line is being drawn

    Returns:
        kwargs (modified for styled lines)
    """
    result = False
    if start and end and cnv:
        if kwargs.get("wave_height"):
            _height = tools.as_float(kwargs.get("wave_height", 0.5), "wave_height")
            try:
                if _lower(kwargs.get("wave_style", "w")) in ["w", "wave", "squiggle"]:
                    cnv.draw_squiggle(start, end, tools.unit(_height))
                    result = True
                elif _lower(kwargs.get("wave_style", "w")) in [
                    "s",
                    "sawtooth",
                    "zigzag",
                    "z",
                ]:
                    cnv.draw_zigzag(start, end, tools.unit(_height))
                    result = True
                else:
                    feedback(
                        f'Unable to handle wave_style {kwargs.get("wave_style")}.', True
                    )
            except ValueError:
                feedback(
                    f'The height of {kwargs.get("wave_height")} is too large'
                    " to allow the line pattern to be drawn.",
                    True,
                )
        else:
            cnv.draw_line(start, end)
            result = False
    if result:
        klargs = copy.copy(kwargs)
        klargs["fill"] = None
        return klargs
    return kwargs


def draw_line_curve(
    cnv=None,
    start: Point = None,
    end: Point = None,
    curve_height: float = None,
    **kwargs,
) -> dict:
    """Draw a curved line on the canvas (Page) between two points for a Shape.

    Args:

        cnv (PyMuPDF Page object):
            where the line is drawn
        start (Point):
            start of the line
        end (Point):
            end of the line
        curve_height (float):
            height of curve above centre point of line

    Returns:
        kwargs (modified for styled lines)
    """
    result = False
    if start and end and curve_height:
        curve_centre = geoms.fraction_along_line(start, end, 0.5)
        _, rotation = geoms.angles_from_points(start, end)
        adjust = 90 if curve_height < 0 else -90
        u_curve_height = tools.unit(curve_height)
        curve_point = geoms.point_from_angle(
            curve_centre, abs(u_curve_height), rotation + adjust
        )
        ccentre, _ = geoms.centre_radius_from_points(start, curve_point, end)
        angle_width = geoms.circle_angle_between_points(start, end, ccentre)
        # feedback(f'***Line Curve: {start=} {end=} {u_curve_height=} {angle_width=}')
        cnv.draw_sector(  # anti-clockwise from end pt; 90° default
            (ccentre.x, ccentre.y), (end.x, end.y), angle_width, fullSector=False
        )
        result = True
    if result:
        klargs = copy.copy(kwargs)
        klargs["closed"] = False
        klargs["fill"] = None  # may want to allow this? curve_fill?
        return klargs, curve_point.x, curve_point.y
    return kwargs, None, None
