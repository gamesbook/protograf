#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 16:21:42 2026

@author: derek
"""

# module
from protograf import globals

# from protograf.utils.messaging import feedback
from protograf.utils.docstrings import docstring_base, docstring_center, docstring_onimo
from protograf.shapes import (
    CircleShape,
    HexShape,
    PolygonShape,
    RectangleShape,
)
from protograf.shapes.core import (
    BaseShape,
    ArcShape,
    ArrowShape,
    BezierShape,
    ChordShape,
    CommonShape,
    CrossShape,
    DefaultShape,
    DotShape,
    EllipseShape,
    # FooterShape,
    ImageShape,
    LineShape,
    QRCodeShape,
    PodShape,
    PolylineShape,
    RhombusShape,
    SectorShape,
    ShapeShape,
    SquareShape,
    StadiumShape,
    StarShape,
    StarLineShape,
    TextShape,
    TrapezoidShape,
    TriangleShape,
    BandShape,
)
from protograf.objects import (
    AbstractStateObject,
    AbstractGameObject,
    CardBoxObject,
    CubeObject,
    D6Object,
    DominoObject,
    PolyominoObject,
    PentominoObject,
    RaceTrackObject,
    TetrominoObject,
    StarFieldObject,
)

# local
from . import utils  # globals_set, validate_globals, margins

# ---- shapes ====


def base_shape(source=None, **kwargs):
    kwargs = utils.margins(**kwargs)
    kwargs["source"] = source
    bshape = BaseShape(canvas=globals.canvas, **kwargs)
    return bshape


def Common(source=None, **kwargs):
    """Store properties that will be used by one or more other Shapes.

    Args:

    - source (object): any object can be the source

    Notes:

    * Any kwargs can be used; they are stored for further use by other Shapes
    * `common_kwargs` will overwrite normal **kwargs supplied to a Shape
    """
    base_kwargs = kwargs
    kwargs = utils.margins(**kwargs)
    kwargs["source"] = source
    cshape = CommonShape(canvas=globals.canvas, common_kwargs=base_kwargs, **kwargs)
    return cshape


def common(source=None, **kwargs):
    base_kwargs = kwargs
    kwargs = utils.margins(**kwargs)
    kwargs["source"] = source
    cshape = CommonShape(canvas=globals.canvas, common_kwargs=base_kwargs, **kwargs)
    return cshape


def Default(source=None, **kwargs):
    """Store properties that can be used, or overridden by one or more other Shapes.

    Args:

    - source (object): any object can be the source

    Notes:

    * Any kwargs can be used; they are stored for possible further use by other Shapes
    * `default_kwargs` will be overwritten by equivalent **kwargs supplied to a Shape
    """
    base_kwargs = kwargs
    kwargs = utils.margins(**kwargs)
    kwargs["source"] = source
    dshape = DefaultShape(canvas=globals.canvas, default_kwargs=base_kwargs, **kwargs)
    return dshape


def default(source=None, **kwargs):
    base_kwargs = kwargs
    kwargs = utils.margins(**kwargs)
    kwargs["source"] = source
    dshape = DefaultShape(canvas=globals.canvas, default_kwargs=base_kwargs, **kwargs)
    return dshape


@docstring_base
def Image(source=None, **kwargs):
    """Draw an image on the canvas.

    Args:
    - the first argument must be the filename of the image, prefixed by the
      path or URL where the image can be sourced, if not in the same directory
      as the script.

    Kwargs:
    <base>

    -  *sliced* (str) - a letter used to indicate which portion of the
       image to extract:

       - *l* - the left fraction, matching the image's width:height ratio
       - *c* - the centre fraction, matching the image's width:height ratio
       - *r* - the right fraction, matching the image's width:height ratio
       - *t* - the top fraction, matching the image's height:width ratio
       - *m* - the middle fraction, matching the image's height:width ratio
       - *b* - the botttom fraction, matching the image's height:width ratio
    - *align_horizontal* (str) - position of the image relative to its (x,y):

      - *left* - left edge of image aligned to the x-position (default)
      - *centre* - centre of image aligned to the x-position
      - *right* - right edge of image aligned to the x-position
    - *align_vertical* (str) - position of the image relative to its (x,y):

      - *top* - top edge of image aligned to the y-position (default)
      - *middle* - middle/centre of image aligned to the y-position
      - *bottom* - bottom edge of image aligned to the y-position

    """
    kwargs = utils.margins(**kwargs)
    kwargs["source"] = source
    image = ImageShape(canvas=globals.canvas, **kwargs)
    image.draw()
    return image


def image(source=None, **kwargs):
    kwargs = utils.margins(**kwargs)
    kwargs["source"] = source
    return ImageShape(canvas=globals.canvas, **kwargs)


@docstring_base
def Arc(**kwargs):
    """Draw an Arc shape on the canvas.

    Kwargs:

    <base>

    """
    kwargs = utils.margins(**kwargs)
    arc = ArcShape(canvas=globals.canvas, **kwargs)
    arc.draw()
    return arc


def arc(**kwargs):
    kwargs = utils.margins(**kwargs)
    return ArcShape(canvas=globals.canvas, **kwargs)


@docstring_base
def Arrow(row=None, col=None, **kwargs):
    """Draw a Arrow shape on the canvas.

    Args:

    - row (int): row in which the shape is drawn.
    - col (int): column in which shape is drawn.

    Kwargs:

    <base>

    """
    kwargs = utils.margins(**kwargs)
    arr = arrow(row=row, col=col, **kwargs)
    arr.draw()
    return arr


def arrow(row=None, col=None, **kwargs):
    kwargs = utils.margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return ArrowShape(canvas=globals.canvas, **kwargs)


@docstring_base
def Bezier(**kwargs):
    """Draw a Bezier shape on the canvas.

    Kwargs:

    <base>

    """
    kwargs = utils.margins(**kwargs)
    bezier = BezierShape(canvas=globals.canvas, **kwargs)
    bezier.draw()
    return bezier


def bezier(**kwargs):
    kwargs = utils.margins(**kwargs)
    return BezierShape(canvas=globals.canvas, **kwargs)


@docstring_base
def Chord(row=None, col=None, **kwargs):
    """Draw a Chord shape on the canvas.

    Args:

    - row (int): row in which the shape is drawn.
    - col (int): column in which shape is drawn.

    Kwargs:

    <base>

    """
    kwargs = utils.margins(**kwargs)
    chd = chord(row=row, col=col, **kwargs)
    chd.draw()
    return chd


def chord(row=None, col=None, **kwargs):
    kwargs = utils.margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return ChordShape(canvas=globals.canvas, **kwargs)


@docstring_center
def Circle(row=None, col=None, **kwargs):
    """Draw a Circle shape on the canvas.

    Args:

    - row (int): row in which the shape is drawn.
    - col (int): column in which shape is drawn.

    Kwargs:

    <center>
    - hatches (str): edge-to-edge lines that, if not specified, will
      be drawn in all directions - otherwise:

      - ``n`` (North) or ``s`` (South) draws vertical lines;
      - ``w`` (West) or ``e`` (East) draws horizontal lines;
      - ``nw`` (North-West) or ``se`` (South-East) draws diagonal lines
        from top-left to bottom-right;
      - ``ne`` (North-East) or ``sw`` (South-West) draws diagonal lines
        from bottom-left to top-right;
      - ``o`` (orthogonal) draws vertical **and** horizontal lines;
      - ``d`` (diagonal) draws diagonal lines between adjacent sides.
    - hatches_count (int): sets the **number** of lines to be drawn; the
      intervals between them are equal and depend on the direction
    - hatches_stroke_width (float): hatches line thickness; defaults to 0.1 points
    - hatches_stroke (str): the named or hexadecimal color of the hatches line;
      defaults to ``black``
    - petals (int): sets the number of petals to drawn
    - petals_style (str): a style of ``p`` or ``petal`` causes petals
      to be drawn as arcs; a style of ``t`` or ``triangle`` causes petals
      to be drawn as sharp triangle
    - petals_offset (float): sets the distance of the lowest point of the petal
      line away from the circle's circumference
    - petals_stroke_width (float): sets the thickness of the line used to draw
      the petals
    - petals_fill (str): the named or hexadecimal color of the area inside the
      line used to draw the petals. Any *fill* or *stroke* settings for the
      circle itself may appear superimposed on this area.
    - petals_dotted (bool): if ``True``, sets the line style to *dotted*
    - petals_height (float): sets the distance between the highest and the lowest
      points of the petal line
    - radii (float): a list of angles (in N|deg|) sets the directions at which
      the radii lines are drawn
    - radii_stroke_width (float): determines the thickness of the radii
    - radii_dotted (bool): if set to True, will make the radii lines dotted
    - radii_stroke (str): the named or hexadecimal color of the hatches line;
      defaults to ``black``
    - radii_length (float): changes the length of the radii lines
      (centre to circumference)
    - radii_offset (float): moves the endpoint of the radii line
      **away** from the centre
    - radii_labels (str|list): a string or list of strings used for text labels
    - radii_labels_font (str): name of the font used for the labels
    - radii_labels_rotation(float): rotation in degrees relative to radius angle
    - radii_labels_size (float): point size of label text
    - radii_labels_stroke (str): the named or hexadecimal color of the label text
    - radii_labels_stroke_width (float): thickness of the label text
    - slices (list): colors (named or hexadecimal) used to draw pie slices; if
      None is used then no slice will be drawn in that position
    - slices_fractions (list): the "length" of the slices; if not specified,
      then by default all slices will have their fraction set to 1 i.e. equal
      to the radius of the circle - values smaller than 1 will be drawn inside
      the circle and values larger than 1 will extend slices outside the circle
    - slices_angles (list): the "width" of the slices; if not specified,
      then by default all slices will be of equally-sized angles and occupy
      the full circumference of the circle
    """
    kwargs = utils.margins(**kwargs)
    circle = CircleShape(canvas=globals.canvas, **kwargs)
    circle.draw()
    return circle


def circle(**kwargs):
    kwargs = utils.margins(**kwargs)
    return CircleShape(canvas=globals.canvas, **kwargs)


@docstring_base
def Dot(row=None, col=None, **kwargs):
    """Draw a Dot shape on the canvas.

    Args:

    - row (int): row in which the shape is drawn.
    - col (int): column in which shape is drawn.

    Kwargs:

    <base>

    """
    kwargs = utils.margins(**kwargs)
    dtt = dot(row=row, col=col, **kwargs)
    dtt.draw()
    return dtt


def dot(row=None, col=None, **kwargs):
    kwargs = utils.margins(**kwargs)
    return DotShape(canvas=globals.canvas, **kwargs)


@docstring_base
def Cross(row=None, col=None, **kwargs):
    """Draw a Cross shape on the canvas.

    Args:

    - row (int): row in which the shape is drawn.
    - col (int): column in which shape is drawn.

    Kwargs:

    <base>

    """
    kwargs = utils.margins(**kwargs)
    crs = cross(**kwargs)
    crs.draw()
    return crs


def cross(row=None, col=None, **kwargs):
    kwargs = utils.margins(**kwargs)
    return CrossShape(canvas=globals.canvas, **kwargs)


@docstring_center
def Ellipse(row=None, col=None, **kwargs):
    """Draw a Ellipse shape on the canvas.

    Args:

    - row (int): row in which the shape is drawn.
    - col (int): column in which shape is drawn.

    Kwargs:

    <center>

    """
    kwargs = utils.margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    ellipse = EllipseShape(canvas=globals.canvas, **kwargs)
    ellipse.draw()
    return ellipse


def ellipse(**kwargs):
    kwargs = utils.margins(**kwargs)
    return EllipseShape(canvas=globals.canvas, **kwargs)


@docstring_center
def Hexagon(row=None, col=None, **kwargs):
    """Draw a Hexagon shape on the canvas.

    Args:

    - row (int): row in which the shape is drawn.
    - col (int): column in which shape is drawn.

    Kwargs:

    <center>
    - orientation (str): either *float*, the default, or *pointy*
    - perbii (str): a compass direction in which a bisector is drawn
      (from centre to mid-point of the edge in that direction); directions:

      - ``n`` (North) / ``s`` (South) draws vertical perbii for flat hex;
      - ``w`` (West) / ``e`` (East) draws horizontal perbii for pointy hex;
      - ``nw`` (North-West) / ``se`` (South-East) draws diagonal perbii.
    - slices (list): set of colors that are drawn as triangles  in a clockwise
      direction starting from the "North East"
    - border (list): overide the normal edge line; specify a set of values, which
      are comma-separated inside round brackets, in the following order:

      - direction (str): one of (n)orth, (s)outh, (e)ast or (w)est,
        nw (north-west) or se (south-east)
      - width (float): the line thickness
      - color (str): either a named or hexadecimal color
      - style  (bool): True makes a dotted line; or a list of values creates dashes
    - hatches (str): edge-to-edge lines that, if not specified, will
      be drawn in all directions - otherwise:

      - ``n`` (North) or ``s`` (South) draws vertical lines for flat hex;
      - ``w`` (West) or ``e`` (East) draws horizontal lines for pointy hex;
      - ``nw`` (North-West) or ``se`` (South-East) draws diagonal lines.
    - hatches_count (int): sets the **number** of lines to be drawn the
      intervals between them are equal and depend on the direction
    - hatches_stroke_width (float): hatches line thickness; defaults to 0.1 points
    - hatches_stroke (str): the named or hexadecimal color of the hatches line;
      defaults to ``black``
    - paths (list): one or more pairs of compass directions between
      which a line - straight or an arc - is drawn
    - paths_dotted (bool): if set to True, will make the paths lines dotted
    - paths_stroke_width (float): determines the thickness of the paths
    - paths_stroke (str): the named or hexadecimal color of the paths line;
      defaults to ``black`
    - radii_dotted (bool): if set to True, will make the radii lines dotted
    - radii_stroke_width (float): determines the thickness of the radii
    - radii_stroke (str): the named or hexadecimal color of the hatches line;
      defaults to ``black``
    - radii_length (float): changes the length of the radii lines
      (centre to circumference)
    - radii_offset (float): moves the endpoint of the radii line
      **away** from the centre
    - radii_labels (str|list): a string or list of strings used for text labels
    - radii_labels_font (str): name of the font used for the labels
    - radii_labels_rotation(float): rotation in degrees relative to radius angle
    - radii_labels_size (float): point size of label text
    - radii_labels_stroke (str): the named or hexadecimal color of the label text
    - radii_labels_stroke_width (float): thickness of the label text
    """
    kwargs = utils.margins(**kwargs)
    # print(f'$$$ Will draw HexShape: {kwargs}')
    kwargs["row"] = row
    kwargs["col"] = col
    hexagon = HexShape(canvas=globals.canvas, **kwargs)
    hexagon.draw()
    return hexagon


def hexagon(row=None, col=None, **kwargs):
    kwargs = utils.margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return HexShape(canvas=globals.canvas, **kwargs)


@docstring_base
def Line(row=None, col=None, **kwargs):
    """Draw a Line shape on the canvas.

    Kwargs:

    <base>
    - angle (float): the number of degrees clockwise from the baseline; used in
      conjunction with *length*
    - cx and cy (floats): if set, will replace the use of *x* and *y* for the
      starting point, and work in conjunction with *angle* and *length* to
      create the line around a centre point
    - length (float): sets the specific size of the line; used in conjunction
      with *angle* (which defaults to 0 |deg|)
    - x1 and y1 (floats): a fixed endpoint for the line end (if not calculated by
      *angle* and *length*)
    - wave_style (str):  either wave or sawtooth
    - wave_height (float): the height of each peak

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
    kwargs = utils.margins(**kwargs)
    lin = line(row=row, col=col, **kwargs)
    lin.draw()
    return lin


def line(row=None, col=None, **kwargs):
    kwargs = utils.margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return LineShape(canvas=globals.canvas, **kwargs)


@docstring_center
def Pod(row=None, col=None, **kwargs):
    """Draw a Pod shape on the canvas.

    Args:

    - row (int): row in which the shape is drawn.
    - col (int): column in which shape is drawn.

    Kwargs:

    <center>

    """
    kwargs = utils.margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    pod = PodShape(canvas=globals.canvas, **kwargs)
    pod.draw()
    return pod


def pod(**kwargs):
    kwargs = utils.margins(**kwargs)
    return PodShape(canvas=globals.canvas, **kwargs)


@docstring_center
def Polygon(row=None, col=None, **kwargs):
    """Draw a Polygon shape on the canvas.

    Args:

    - row (int): row in which the shape is drawn.
    - col (int): column in which shape is drawn.

    Kwargs:

    <center>

    """
    kwargs = utils.margins(**kwargs)
    poly = polygon(row=row, col=col, **kwargs)
    poly.draw()
    return poly


def polygon(row=None, col=None, **kwargs):
    kwargs = utils.margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return PolygonShape(canvas=globals.canvas, **kwargs)


@docstring_base
def Polyline(row=None, col=None, **kwargs):
    """Draw a Polyline shape on the canvas.

    Args:

    - row (int): row in which the shape is drawn.
    - col (int): column in which the shape is drawn.

    Kwargs:

    <base>

    """
    kwargs = utils.margins(**kwargs)
    polylin = polyline(row=row, col=col, **kwargs)
    polylin.draw()
    return polylin


def polyline(row=None, col=None, **kwargs):
    kwargs = utils.margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return PolylineShape(canvas=globals.canvas, **kwargs)


@docstring_center
def Rhombus(row=None, col=None, **kwargs):
    """Draw a Rhombus shape on the canvas.

    Args:

    - row (int): row in which the shape is drawn.
    - col (int): column in which the shape is drawn.

    Kwargs:

    <center>

    """
    kwargs = utils.margins(**kwargs)
    rhomb = rhombus(row=row, col=col, **kwargs)
    rhomb.draw()
    return rhomb


def rhombus(row=None, col=None, **kwargs):
    kwargs = utils.margins(**kwargs)
    return RhombusShape(canvas=globals.canvas, **kwargs)


@docstring_center
def Rectangle(row=None, col=None, **kwargs):
    """Draw a Rectangle shape on the canvas.

    Args:

    - row (int): row in which the shape is drawn.
    - col (int): column in which the shape is drawn.

    Kwargs:

    <center>

    - rounding (float): the radius of the circle used to round the corner
    - borders (list): overide the normal edge lines; specify a set of values, which
      are comma-separated inside round brackets, in the following order:

      - direction (str): one of (n)orth, (s)outh, (e)ast or (w)est,
        nw (north-west) or se (south-east)
      - width (float): the line thickness
      - color (str): either a named or hexadecimal color
      - style (bool): True makes a dotted line; or a list of values creates dashes
    - chevron (str): the primary compass direction in which a peak is
      pointing; n(orth), s(outh), e(ast) or w(est)
    - chevron_height (float): the distance of the chevron peak from the side of
      the rectangle it is adjacent to
    - hatches (str): if not specified, hatches will be drawn
      in all directions - otherwise:

      - ``n`` (North) or ``s`` (South) draws vertical lines;
      - ``w`` (West) or ``e`` (East) draws horizontal lines;
      - ``nw`` (North-West) or ``se`` (South-East) draws diagonal lines
        from top-left to bottom-right;
      - ``ne`` (North-East) or ``sw`` (South-West) draws diagonal lines
        from bottom-left to top-right;
      - ``o`` (orthogonal) draws vertical **and** horizontal lines;
      - ``d`` (diagonal) draws diagonal lines between adjacent sides.
    - corners (float): the size of the shape that will be drawn in the
      corners of the rectangle
    - corners_stroke_width (float): corners line thickness; defaults to 0.1 points
    - corners_stroke (str): the named or hexadecimal color of the corners line;
      defaults to ``black` (for RGB color_model)
    - corners_fill (str): the named or hexadecimal color of the corners area;
      defaults to ```white`` (for RGB color_model)
    - corners_x (float): the length of the corners in the x-direction
    - corners_y (float): the length of the corners in the y-direction
    - corners_directions (str): the specific corners of the rectangle where the
      corners is drawn, given as secondary compass directions - ne, se, sw, nw
    - corners_style (str): defines the corners appearance:

      - *normal* - a simple line
      - *triangle* - a triangular shape
      - *curve* - a triangular shape with a curved lower edge
      - *arch* - an arrow-shape with with a cut-out curved notch
      - *photo* - a triangular shape with a cut-out notch
    - hatches_count (int): sets the **number** of lines to be drawn; the
      intervals between them are equal and depend on the direction
    - hatches_stroke_width (float): hatches line thickness; defaults to 0.1 points
    - hatches_stroke (str): the named or hexadecimal color of the hatches line;
      defaults to ``black``
    - notch (float): the size of the triangular shape that will be "cut" off the
      corners of the rectangle
    - notch_x (float): the distance from the corner in the x-direction where the
      notch will start
    - notch_y (float): the distance from the corner in the y-direction where the
      notch will start
    - notch_directions (str): the specific corners of the rectangle where the notch
      is applied, given as secondary compass directions - ne, se, sw, nw
    - notch_style (str): defines the notch appearance:

      - *snip* - is a small triangle "cut out"; this is the default style
      - *step* - is sillohette of a step "cut out"
      - *fold* - makes it appear there is a crease across the corner
      - *flap* - makes it appear that the corner has a small, liftable flap
    - peaks (list): a list of one or more sets, each enclosed by round brackets,
      consisting of a *direction* and a peak *size*:

      - Directions are the primary compass directions - (n)orth,
        (s)outh, (e)ast and (w)est
        Sizes are the distances of the centre of the peak from the edge
        of the Rectangle
    - prows (list): a list of one or more sets, each enclosed by round brackets.
      A set contains a *direction* (secondary compass - ne, se, sw, nw), a
      peak *distance* (away from the edge), and a pair of *x* and *y* offsets
      for the control points of the curves drawn for the prows
    - slices (list): list of two or four  named or hexadecimal colors, as
      comma-separated strings
    - slices_line (float): the width of a line drawn centered in the rectangle
    - slices_stroke (str): the named or hexadecimal color of the slice line;
      defaults to ``black``
    """
    kwargs = utils.margins(**kwargs)
    rect = rectangle(row=row, col=col, **kwargs)
    rect.draw()
    return rect


def rectangle(row=None, col=None, **kwargs):
    kwargs = utils.margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return RectangleShape(canvas=globals.canvas, **kwargs)


@docstring_base
def Polyshape(row=None, col=None, **kwargs):
    """Draw a Polyshape shape on the canvas.

    Args:

    - row (int): row in which the shape is drawn.
    - col (int): column in which the shape is drawn.

    Kwargs:

    <base>

    """
    kwargs = utils.margins(**kwargs)
    shapeshape = polyshape(row=row, col=col, **kwargs)
    shapeshape.draw()
    return shapeshape


def polyshape(row=None, col=None, **kwargs):
    kwargs = utils.margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return ShapeShape(canvas=globals.canvas, **kwargs)


@docstring_base
def QRCode(source=None, **kwargs):
    """Draw a QRCode shape on the canvas.

    Args:

    - row (int): row in which the shape is drawn.
    - col (int): column in which the shape is drawn.

    Kwargs:

    <base>

    """
    kwargs = utils.margins(**kwargs)
    kwargs["source"] = source
    image = QRCodeShape(canvas=globals.canvas, **kwargs)
    image.draw()
    return image


def qrcode(source=None, **kwargs):
    kwargs = utils.margins(**kwargs)
    kwargs["source"] = source
    return QRCodeShape(canvas=globals.canvas, **kwargs)


@docstring_base
def Sector(row=None, col=None, **kwargs):
    """Draw a Sector shape on the canvas.

    Args:

    - row (int): row in which the shape is drawn.
    - col (int): column in which the shape is drawn.

    Kwargs:

    <base>

    """
    kwargs = utils.margins(**kwargs)
    sct = sector(row=row, col=col, **kwargs)
    sct.draw()
    return sct


def sector(row=None, col=None, **kwargs):
    kwargs = utils.margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return SectorShape(canvas=globals.canvas, **kwargs)


@docstring_center
def Square(row=None, col=None, **kwargs):
    """Draw a Square shape on the canvas.

    Args:

    - row (int): row in which the shape is drawn.
    - col (int): column in which the shape is drawn.

    Kwargs:

    <center>

    """
    kwargs = utils.margins(**kwargs)
    sqr = square(row=row, col=col, **kwargs)
    sqr.draw()
    return sqr


def square(row=None, col=None, **kwargs):
    kwargs = utils.margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return SquareShape(canvas=globals.canvas, **kwargs)


@docstring_center
def Stadium(row=None, col=None, **kwargs):
    """Draw a Stadium shape on the canvas.

    Args:

    - row (int): row in which the shape is drawn.
    - col (int): column in which the shape is drawn.

    Kwargs:

    <center>

    """
    kwargs = utils.margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    std = StadiumShape(canvas=globals.canvas, **kwargs)
    std.draw()
    return std


def stadium(row=None, col=None, **kwargs):
    kwargs = utils.margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return StadiumShape(canvas=globals.canvas, **kwargs)


@docstring_center
def Star(row=None, col=None, **kwargs):
    """Draw a Star shape on the canvas.

    Args:

    - row (int): row in which the shape is drawn.
    - col (int): column in which the shape is drawn.

    Kwargs:

    <center>

    """
    kwargs = utils.margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    star = StarShape(canvas=globals.canvas, **kwargs)
    star.draw()
    return star


def star(row=None, col=None, **kwargs):
    kwargs = utils.margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return StarShape(canvas=globals.canvas, **kwargs)


@docstring_center
def StarLine(row=None, col=None, **kwargs):
    """Draw a StarLine shape on the canvas.

    Args:

    - row (int): row in which the shape is drawn.
    - col (int): column in which the shape is drawn.

    Kwargs:

    <center>

    """
    kwargs = utils.margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    starline = StarLineShape(canvas=globals.canvas, **kwargs)
    starline.draw()
    return starline


def starline(row=None, col=None, **kwargs):
    kwargs = utils.margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return StarLineShape(canvas=globals.canvas, **kwargs)


@docstring_base
def Text(text: str | None = None, row=None, col=None, **kwargs):
    """Draw a Text shape on the canvas.

    Args:

    - row (int): row in which the shape is drawn.
    - col (int): column in which the shape is drawn.

    Kwargs:

    <base>

    """
    kwargs = utils.margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    if text and not kwargs.get("text"):
        kwargs["text"] = text
    text = TextShape(canvas=globals.canvas, **kwargs)
    text.draw()
    return text


def text(text: str | None = None, row=None, col=None, **kwargs):
    kwargs = utils.margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    if text and not kwargs.get("text"):
        kwargs["text"] = text
    return TextShape(canvas=globals.canvas, **kwargs)


@docstring_center
def Trapezoid(row=None, col=None, **kwargs):
    """Draw a Trapezoid shape on the canvas.

    Args:

    - row (int): row in which the shape is drawn.
    - col (int): column in which the shape is drawn.

    Kwargs:

    <center>

    """
    kwargs = utils.margins(**kwargs)
    trp = trapezoid(row=row, col=col, **kwargs)
    trp.draw()
    return trp


def trapezoid(row=None, col=None, **kwargs):
    kwargs = utils.margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return TrapezoidShape(canvas=globals.canvas, **kwargs)


@docstring_center
def Triangle(row=None, col=None, **kwargs):
    """Draw a Triangle shape on the canvas.

    Args:

    - row (int): row in which the shape is drawn.
    - col (int): column in which shape is drawn.

    Kwargs:

    <center>

    """
    kwargs = utils.margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    eqt = TriangleShape(canvas=globals.canvas, **kwargs)
    eqt.draw()
    return eqt


def triangle(row=None, col=None, **kwargs):
    kwargs = utils.margins(**kwargs)
    return TriangleShape(canvas=globals.canvas, **kwargs)


def Band(row=None, col=None, **kwargs):
    """Draw a Band shape on the canvas.

    Args:

    - row (int): row in which the shape is drawn.
    - col (int): column in which shape is drawn.

    Kwargs:

    <center>

    """
    kwargs = utils.margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    bnd = BandShape(canvas=globals.canvas, **kwargs)
    bnd.draw()
    return bnd


def band(row=None, col=None, **kwargs):
    kwargs = utils.margins(**kwargs)
    return BandShape(canvas=globals.canvas, **kwargs)


# ---- objects ====


@docstring_base
def AbstractGame(row=None, col=None, **kwargs):
    """Store an AbstractGameObject for the canvas.

    Args:

    - row (int): row in which the shape is located.
    - col (int): column in which the shape is located.

    Kwargs:

    - name (str): the name of a type of board (default is Checkers)
    - colors (list): a list of one or more Colors in which to draw alternating
      board spaces (default is `white`)
    - hairs (bool): if True, draw small lines extending outwards from board
      gridlines of one-quarter cell size
    - labels (bool): if True, draw labels along board edges, using notation
      appropriate to the type of board; Chess notation is the common default
    - grid_align (bool): if True, draw pieces on grid intersections, not grid
      spaces
    - pieces (list|str): details of pieces that will be placed on the board
    - pieces_resize (float): a fractional value by which to resize the piece
      shapes or images (default: 1.0)
    - rows (int): if no game name (which has a predefined number of rows) is
      set, these are the number of cells in the vertical direction for a
      regular grid (default: 8)
    - cols (int): if no game name (which has a predefined number of rows) is
      set, these are the number of cells in the horizontal direction for a
      regular grid (default: 8)
    - annotations (list): a list of game annotations (optional)


    <base>

    """
    kwargs = utils.margins(**kwargs)
    absboard = AbstractGameObject(canvas=globals.canvas, **kwargs)
    # absboard.draw()
    return absboard


def abstractboard(*args, **kwargs):
    kwargs = utils.margins(**kwargs)
    _obj = args[0] if args else None
    return AbstractGameObject(_object=_obj, canvas=globals.canvas, **kwargs)


@docstring_base
def AbstractState(row=None, col=None, **kwargs):
    """Draw an AbstractStateObject on the canvas.

    Args:

    - row (int): row in which the shape is drawn.
    - col (int): column in which the shape is drawn.

    Kwargs:

    - board (str): an AbstractGameObject (default board type is Checkers)
      which should be displayed
    - positions (str): details of where an AbstractGameObject's pieces go
      on the board display
    - annotations (list): a list of state annotations (optional)

    <base>

    """
    kwargs = utils.margins(**kwargs)
    absgame = AbstractStateObject(canvas=globals.canvas, **kwargs)
    absgame.draw()
    return absgame


def abstractgame(*args, **kwargs):
    kwargs = utils.margins(**kwargs)
    _obj = args[0] if args else None
    return AbstractStateObject(_object=_obj, canvas=globals.canvas, **kwargs)


@docstring_base
def Cube(row=None, col=None, **kwargs):
    """Draw a Cube shape with shading on the canvas.

    Args:

    - row (int): row in which the shape is drawn.
    - col (int): column in which the shape is drawn.

    Kwargs:

    - shades (list|str): list of one or three colors used to shade 'sides'
      of the cube; a single string is converted into light and dark shading
    - shades_stroke (str): line color used to outline the shade areas;
      defaults to match shade color
    - shades_stroke_width (str): line width used to outline the shade areas;
      defaults to match shape stroke width
    <base>

    """
    kwargs = utils.margins(**kwargs)
    Cube = CubeObject(canvas=globals.canvas, **kwargs)
    Cube.draw()
    return Cube


def cube(*args, **kwargs):
    kwargs = utils.margins(**kwargs)
    _obj = args[0] if args else None
    return CubeObject(_object=_obj, canvas=globals.canvas, **kwargs)


@docstring_base
def D6(row=None, col=None, **kwargs):
    """Draw a D6 shape with "pips" on the canvas.

    Args:

    - row (int): row in which the shape is drawn.
    - col (int): column in which the shape is drawn.

    Kwargs:

    - random (bool):
    - roll (int): a number from 1 to 6 representing the number of pips
    - pip_stroke (str):
    - pip_fill (str):
    - pip_fraction (float):
    <base>

    """
    kwargs = utils.margins(**kwargs)
    d6 = D6Object(canvas=globals.canvas, **kwargs)
    d6.draw()
    return d6


def d6(*args, **kwargs):
    kwargs = utils.margins(**kwargs)
    _obj = args[0] if args else None
    return D6Object(_object=_obj, canvas=globals.canvas, **kwargs)


@docstring_base
def CardBox(row=None, col=None, **kwargs):
    """Draw a CardBox shape on the canvas.

    Args:

    - row (int): row in which the shape is drawn.
    - col (int): column in which the shape is drawn.

    Kwargs:

    - card_size (str): the name of a type of card (default is Poker)
    - depth (float): the "thickness" of the box
    - thumb (float): the diameter of a half-circle drawn at the top of the back area
    - rounded (bool): if True, the primary flaps have rounded corners (default is False)
    - fold (bool): if True, the fold lines are displayed (default is False)
    - fold_stroke (str): line color of the *grid_marks*; defaults to ``dimgray``
    - fold_stroke_width (float): line width of a *fold*; defaults to 0.1
    - flap (float): the height of the primary flaps
    - flap_inner (float): the height of the inner flaps
    - flap_glued (float): the height of the flap to be glued
    - padding (float): the extra size added to the height and width (default is 2mm)
    - padding_width (float): the extra size added to the width
    - padding_height (float): the extra size added to the height
    - shapes_front (shape|list): either a shape, or a list shapes, to be drawn centred
      in the front rectangle of the box
    - shapes_left (shape|list): either a shape, or a list shapes, to be drawn centred
      in the left side rectangle of the box
    - shapes_right (shape|list): either a shape, or a list shapes, to be drawn centred
      in the right side rectangle of the box
    - shapes_back (shape|list): either a shape, or a list shapes, to be drawn centred
      in the back rectangle of the box
    - shapes_top (shape|list): either a shape, or a list shapes, to be drawn centred
      in the top-side rectangle of the box
    - shapes_bottom (shape|list): either a shape, or a list shapes, to be drawn centred
      in the under-side rectangle of the box

    <base>

    """
    kwargs = utils.margins(**kwargs)
    cardbox = CardBoxObject(canvas=globals.canvas, **kwargs)
    cardbox.draw()
    return cardbox


def cardbox(*args, **kwargs):
    kwargs = utils.margins(**kwargs)
    _obj = args[0] if args else None
    return CardBoxObject(_object=_obj, canvas=globals.canvas, **kwargs)


def TuckBox(row=None, col=None, **kwargs):
    return CardBox(row=row, col=col, **kwargs)


def tuckbox(*args, **kwargs):
    return cardbox(*args, **kwargs)


@docstring_base
def Domino(row=None, col=None, **kwargs):
    """Draw a Domino shape with "pips" on the canvas.

    Args:

    - row (int): row in which the shape is drawn.
    - col (int): column in which the shape is drawn.

    Kwargs:

    - random (bool):
    - rolls (tuple): a pair of number (each 1 to 6) representing the number of pips
    - pip_stroke (str):
    - pip_fill (str):
    - pip_fraction (float):
    <base>

    """
    kwargs = utils.margins(**kwargs)
    domino = DominoObject(canvas=globals.canvas, **kwargs)
    domino.draw()
    return domino


def domino(*args, **kwargs):
    kwargs = utils.margins(**kwargs)
    _obj = args[0] if args else None
    return DominoObject(_object=_obj, canvas=globals.canvas, **kwargs)


@docstring_base
@docstring_onimo
def Polyomino(row=None, col=None, **kwargs) -> PolyominoObject:
    """Create a Polyomino object

    Args:

    - row (int): row in which Polyomino is drawn.
    - col (int): column in which Polyomino is drawn.

    Kwargs:

    - pattern (list): a list of string values; one string per row. Each string
      contains one or more numbers aka "columns". Each number represents a square,
      with a zero (0) representing a space.
    <onimo>
    <base>

    Returns:
        PolyominoObject

    """
    kwargs = utils.margins(**kwargs)
    polym = polyomino(row=row, col=col, **kwargs)
    polym.draw()
    return polym


def polyomino(row=None, col=None, **kwargs) -> PolyominoObject:
    kwargs = utils.margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return PolyominoObject(canvas=globals.canvas, **kwargs)


@docstring_base
@docstring_onimo
def Pentomino(row=None, col=None, **kwargs):
    """Create a Polyomino object

    Args:

    - row (int): row in which Pentomino is drawn.
    - col (int): column in which Pentomino is drawn.

    Kwargs:

    - letter (str): a single character representing a unique arrangement of 5 squares
    <onimo>
    <base>

    Returns:
        PentominoObject
    """
    kwargs = utils.margins(**kwargs)
    pentm = pentomino(row=row, col=col, **kwargs)
    pentm.draw()
    return pentm


def pentomino(row=None, col=None, **kwargs):
    kwargs = utils.margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return PentominoObject(canvas=globals.canvas, **kwargs)


def Tetromino(row=None, col=None, **kwargs):
    """Create a Tetromino object

    Args:

    - row (int): row in which Tetromino is drawn.
    - col (int): column in which Tetromino is drawn.

    Kwargs:

    - letter (str): a single character representing a unique arrangement
      of 4 squares
    <onimo>
    <base>

    Returns:

        TetrominoObject
    """
    kwargs = utils.margins(**kwargs)
    tetrm = tetromino(row=row, col=col, **kwargs)
    tetrm.draw()
    return tetrm


def tetromino(row=None, col=None, **kwargs):
    kwargs = utils.margins(**kwargs)
    kwargs["row"] = row
    kwargs["col"] = col
    return TetrominoObject(canvas=globals.canvas, **kwargs)


@docstring_base
def RaceTrack(row=None, col=None, **kwargs):
    """Draw a RaceTrack shape with "pips" on the canvas.

    Args:

    - row (int): row in which the shape is drawn.
    - col (int): column in which the shape is drawn.

    Kwargs:

    - stages (list): list of Reactangle and/or Band shapes
    - lanes_*: styling for lines running parallel to top&bottom
    - segments_*: styling for lines running parallel to left&right
    <base>

    """
    kwargs = utils.margins(**kwargs)
    racetrak = RaceTrackObject(canvas=globals.canvas, **kwargs)
    racetrak.draw()
    return racetrak


def racetrack(*args, **kwargs):
    kwargs = utils.margins(**kwargs)
    _obj = args[0] if args else None
    return RaceTrackObject(_object=_obj, canvas=globals.canvas, **kwargs)


@docstring_base
def StarField(**kwargs):
    """Draw a Starfield object on the canvas.

    Kwargs:

    <base>
    - density (int): average number of stars per square unit; default is 10
    - colors (list): individual star colors; default is ["white"] for RGB color_model
    - enclosure (str): the name of the regular shape inside which the
      StarFieldObject is drawn; default is a `rectangle`
    - sizes (list): the individual star sizes; default is [0.1]
    - star_pattern (random | cluster) - NOT YET IMPLEMENTED
    - seeding (float): if set, predetermines the randomisation sequenc

    Reference:

        https://codeboje.de/starfields-and-galaxies-python/
    """
    kwargs = utils.margins(**kwargs)
    starfield = StarFieldObject(canvas=globals.canvas, **kwargs)
    starfield.draw()
    return starfield


def starfield(**kwargs):
    kwargs = utils.margins(**kwargs)
    return StarFieldObject(canvas=globals.canvas, **kwargs)


common.__doc__ = Common.__doc__
arc.__doc__ = Arc.__doc__
arrow.__doc__ = Arrow.__doc__
bezier.__doc__ = Bezier.__doc__
chord.__doc__ = Chord.__doc__
circle.__doc__ = Circle.__doc__
dot.__doc__ = Dot.__doc__
ellipse.__doc__ = Ellipse.__doc__
hexagon.__doc__ = Hexagon.__doc__
image.__doc__ = Image.__doc__
line.__doc__ = Line.__doc__
pentomino.__doc__ = Pentomino.__doc__
pod.__doc__ = Pod.__doc__
polygon.__doc__ = Polygon.__doc__
polyline.__doc__ = Polyline.__doc__
polyomino.__doc__ = Polyomino.__doc__
polyshape.__doc__ = Polyshape.__doc__
rectangle.__doc__ = Rectangle.__doc__
rhombus.__doc__ = Rhombus.__doc__
star.__doc__ = Star.__doc__
starfield.__doc__ = StarField.__doc__
tetromino.__doc__ = Tetromino.__doc__
triangle.__doc__ = Triangle.__doc__
# .__doc__ = .__doc__
