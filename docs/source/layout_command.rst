==============
Layout Command
==============

.. |dash| unicode:: U+2014 .. EM DASH SIGN
.. |deg|  unicode:: U+00B0 .. DEGREE SIGN
   :ltrim:

This section assumes you are very familiar with the concepts, terms and
ideas for :doc:`protograf <index>` as presented in the
:doc:`Basic Concepts <basic_concepts>` , that you understand all of the
:doc:`Additional Concepts <additional_concepts>`
and that you've created some basic scripts of your own using the
:doc:`Core Shapes <core_shapes>`.

This is part of the set of commands used for :doc:`Layouts <layouts>`.

.. _layout-command:

Overview
========

The ``Layout()`` command is designed to be used in conjuction with a
Location-based grid; it specifies the shapes that are to be drawn at locations.

The location-based grids that are available are:

-  :doc:`RectangularLocations() <layouts_rectangular>` - defines a series of
   differing x- and y-points in a rectangular pattern; these x- and y-values
   will set the centre of any element being placed on the grid
-  :doc:`TriangularLocations() <layouts_triangular>` - defines a series of
   differing x- and y-points in a triangular pattern; these x- and y-values
   will set the centre of any element being placed on the grid
-  :doc:`DiamondLocations() <layouts_diamond>` - defines a series of
   differing x- and y-points in a diamond pattern; these x- and y-values
   will set the centre of any element being placed on the grid

Properties
==========

The Location command accepts the following properties:

- **grid** - this *must* be the first property used for the command; it will
  refer to a row & column grid created by any of the Locations commands
- **locations** - a list of sets of ``(col, row)`` pairs; these are locations
  that will be used for drawing, in the order that they appear
- **rows** - a list of row locations that will be used for drawing
- **cols** - a list of column locations that will be used for drawing
- **shapes** - this is a list of one or more of the core shapes available,
  for example, a circle or rectangle; if no shapes are provided, the program
  will issue a ``WARNING`` message
- **masked** - a list of sequence numbers for the locations in which shapes
  should **not** be displayed
- **visible** - a list of sequence numbers for the **only** locations in
  which shapes should be displayed


.. NOTE::

    Usage of the Layout command is illustrated by the examples provided
    with the various "Locations()" command listed above.

Debug
-----

A property that is not usually used for a final layout, but can be helpful
during the design stage is  **debug**.

**debug** will display the centre points of the grid, along with any
extra information specified.  Allowed values for debug include:

  - *none* - only the locations are shown as small dots; matching the color
    of the :ref:`Blueprint <blueprintIndex>`
  - *count* - shows the sequence number i.e. the order of drawing
  - *xy* - shows x- and y-values
  - *yx* - shows y- and x-values
  - *rowcol* - shows row and column numbers
  - *colrow* - shows column and row numbers
  - *id* - shows the internal ID number assigned to the location
