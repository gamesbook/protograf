# -*- coding: utf-8 -*-
"""
Common document strings and associated decorator functions.

Written by: Derek Hohls
Created on: 21 July 2024

Example Usage:

    def patch_docstring_a(func):
        func.__doc__ = func.__doc__.replace('<arg_a>', '- a: A common argument.')
        return func


    @patch_docstring_a
    def my_function(a, b):
        '''Performs an operation.

        Args:

        <arg_a>
        - b: Another argument.
        '''
        pass
"""
