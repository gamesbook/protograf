===================
Repetitive Elements
===================

.. |dash| unicode:: U+2014 .. EM DASH SIGN

This section assumes you are very familiar with the concepts, terms and ideas
for :doc:`protograf <index>`  as presented in the
:doc:`Basic Concepts <basic_concepts>` , that you understand all of the
:doc:`Additional Concepts <additional_concepts>` and that you've created some
basic scripts of your own using the :doc:`Core Shapes <core_shapes>`.


Overview
========

**protograf** allows you to directly define where elements, that make up
your design, should be placed within a page, or over a series of pages
within a :doc:`Deck <card_decks>`, but it also includes commands that let
you place, or "layout", elements in a more repetitive or regular way
within a page.

Sequences
---------

The most basic repetition is that of a simple **sequence**, with elements
placed at regular x- and y-positions in a linear direction.

Repeats
-------

The other fairly basic repetition is that of a **repeat**, with elements
placed at grid locations within a page.

Tracks
------

Elements can also be placed repetitively along a **track**.

A track can be defined as the border of a rectangle or polygon shape;
or at specific angles along the circumference of a circle.

The properties needed to construct this kind of repetition differ
slightly from that of a simple linear one but the principle is the
same. The track can be visible, or not.

Locations and Layouts
---------------------

The other way that elements can be laid out repetitively on a page
is through grid **locations**.

In **protograf**, such a grid can be derived from various built-in shapes -
for example, ``Hexagons`` - or it can be constructed using a supplied set
of properties. Because these grids do not themselves appear on the page,
they are termed *"virtual grids"*.

A virtual grid is **not** specifically drawn on the page; rather it creates
a set of point locations at which other elements can be drawn. This set of
points can be used for creating a **layout** by:

1. providing a sequence or list of elements, which are then drawn in the
   order specified by the "virtual grid" points, starting from a known point
   on the grid; *or*
2. refering to each point directly, by using the identity of its locations,
   and then drawing the element using that point’s position.

.. HINT::

    The *first approach* is useful when the entire grid will be filled with a
    single element (or a repeating set of elements).

    The *second approach* is more suitable when only some locations of the grid
    will be used, or if a much finer degree of control is needed with differing
    elements going into very specific |dash| and possibly irregular |dash| places
    that the script specifies.


Commands Summary
================

Very briefly, the different kinds of layout commands are as follows.

Linear layouts, where elements appear in one-dimensional space:

-  :doc:`Sequence() <layouts_sequence>` - allows a set of elements to be
   placed at regular intervals in a straight line
-  :doc:`Track() <layouts_track>` - the elements are positioned along the
   line used to delineate a shape; they can be placed either at the vertices
   of that line (e.g. at the corners of a square) or in the centre between
   two sequential vertices.

Grid-based layouts, where elements appear in two-dimensional space:

-  :doc:`Repeat() <layouts_repeat>` - allows an element to be placed multiple
   times onto a grid
-  :doc:`RectangularLocations() <layouts_rectangular>` - defines a series of
   differing x- and y-points in a rectangular pattern; these x- and y-values
   will set the centre of any element being placed on the grid
-  :doc:`TriangularLocations() <layouts_triangular>` - defines a series of
   differing x- and y-points in a triangular pattern; these x- and y-values
   will set the centre of any element being placed on the grid

These location-types are paired with a **Layout()** command, which
links them with the shapes that need to be drawn at their locations.

.. HINT::

    :doc:`Hexagonal Grids <hexagonal_grids>` are a special kind of repetition
    that can be more specifically customised.
