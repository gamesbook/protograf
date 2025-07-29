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
        '<base>',
        """
    - x (float): The left-most edge of the shape; defaults to 1
    - y (float): The top-most edge of the shape; defaults to 1
    - stroke (str): The named or hexadecimal color of shape's line;
      defaults to ``black``
    - stroke_width (float): The point width of the shape's line;
      defaults to 0.1.
    - dotted (bool): if True, create a series of small lines i.e. the
      "dots", followed by gaps, of size equal to the lines *stroke_width*
    - dashed (list): a list of two floats: the first is the length of
      the dash; the second is the length of the space between each dash
    - rounded (bool): if True, draw small semicircles at the ends of the line
    - squared (bool): if True, draw small squares, centred at the ends of the line"""
     )
    return func


def docstring_card(func):
    func.__doc__ = func.__doc__.replace(
        '<card>',
        """
    - The first argument must be an expression that can be evaulated to
      create a list of one or more numbers; e.g. "1-10", "1,3,5-10",
      [1,3,7,9]; the terms "*" or "all" represent all possible values
    - The second and further arguments must one of these type of objects:
      - a Shape
      - a T() expression
      - a S() expression
      - the name of a function that returns one or more Shapes"""
    )


def docstring_area(func):
    func.__doc__ = func.__doc__.replace(
        '<area>',
        """
     - fill (str): The named or hexadecimal color of shape's area;
       defaults to ``white``."""
    )
