# -*- coding: utf-8 -*-
"""
Common document strings and associated decorator functions.

Written by: Derek Hohls
Created on: 21 July 2024

Example Usage:

    def patch_docstring_a(func):
        func.__doc__ = func.__doc__.replace('<arg_a>', '- a: A common argument.')
        return func


    @docstring_x
    def my_function(a, b):
        '''Performs an operation.

        Args:

        <arg_a>
        - b: Another argument.
        '''
        pass
"""


def docstring_base(func):
    func.__doc__ = func.__doc__.replace(
        "<base>",
        """- x (float): the left-most edge of the shape; defaults to 1
    - y (float): the top-most edge of the shape; defaults to 1
    - stroke (str): the named or hexadecimal color of shape's line;
      defaults to ``black``
    - stroke_width (float): the point width of the shape's line;
      defaults to 0.1.
    - dotted (bool): if True, create a series of small lines i.e. the
      "dots", followed by gaps, of size equal to the lines *stroke_width*
    - dashed (list): a list of two floats: the first is the length of
      the dash; the second is the length of the space between each dash
    - rounded (bool): if True, draw small semicircles at the ends of the line
    - squared (bool): if True, draw small squares, centred at the ends of the line""",
    )
    return func


def docstring_loc(func):
    func.__doc__ = func.__doc__.replace(
        "<loc>",
        """- x (float): the left-most edge of the shape; defaults to 1
    - y (float): the top-most edge of the shape; defaults to 1""",
    )
    return func


def docstring_card(func):
    func.__doc__ = func.__doc__.replace(
        "<card>",
        """- The first argument must be an expression that can be evaulated to
      create a list of one or more numbers; e.g. "1-10", "1,3,5-10",
      [1,3,7,9]; the terms "*" or "all" represent all possible values
    - The second and further arguments must one of these type of objects:
      - a Shape
      - a T() expression
      - a S() expression
      - the name of a function that returns one or more Shapes""",
    )
    return func


def docstring_area(func):
    func.__doc__ = func.__doc__.replace(
        "<area>",
        """- fill (str): the named or hexadecimal color of shape's area;
      defaults to ``white``.
    - fill_stroke(str): the named or hexadecimal color for the shape's
      line and area colors.""",
    )
    return func


def docstring_center(func):
    func.__doc__ = func.__doc__.replace(
        "<center>",
        """- x (float): the left-most edge of the shape; defaults to 1
    - y (float): the top-most edge of the shape; defaults to 1
    - cx (float): the centre position of the shape, relative to the left edge
    - cy (float): the centre position of the shape, relative to the top edge
    - rotation (float): the rotation of the shape in degrees, anti-clockwise
      from the baseline
    - dot (int): the size of a small dot to be drawn at the centre of the shape
    - dot_stroke (str): the named or hexadecimal color of dot's line;
      defaults to ``black``
    - dot_stroke_width (float): the point width of the dot's line;
      defaults to 0.1
    - cross (int): the size of a small cross to be drawn at the centre of the
      shape
    - cross_stroke (str): the named or hexadecimal color of the cross's line;
      defaults to ``black``
    - cross_stroke_width (float): the point width of the cross's line;
      defaults to 0.1.
    - label (str): text to be displayed in the middle of the shape
    - label_stroke (str): the named or hexadecimal color of the label's line;
      defaults to ``black``
    - label_size (float): the point size of the label's text; defaults to 12
    - heading (str): text to be displayed above the shape
    - label_mx (float): the distance the label should be shifted away from the
      centre of the shape to the left or right
    - label_my (float): the distance the label should be shifted away from the
      centre of the shape either up or down
    - heading_stroke (str): the named or hexadecimal color of the heading's line;
      defaults to ``black``
    - heading_size (float): the point size of the heading's text; defaults to 12
    - title (str): text to be displayed below the shape
    - title_stroke (str): the named or hexadecimal color of the title's line;
      defaults to ``black``
    - title_size (float): the point size of the title's text; defaults to 12""",
    )
    return func


def docstring_onimo(func):
    func.__doc__ = func.__doc__.replace(
        "<onimo>",
        """- invert (str): can either be ``leftright`` (``lr``) or ``topbottom``
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
    - shapes (list): each square can be linked to a different centred shape""",
    )
    return func
