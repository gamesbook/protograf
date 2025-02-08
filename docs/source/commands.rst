=============
Commands List
=============

.. |dash| unicode:: U+2014 .. EM DASH SIGN

This list provides an alphabetic summary of all the
:ref:`commands <command-concept>` specific to
:ref:`protograf <index>`.  It is not intended to be used for learning
but is a handy cross-reference to the detailed information for that command.

.. HINT::

  :doc:`protograf <index>` is a small, specialised tool; but its part of a much
  greater Python language "ecosystem", and commands and tools from the
  :doc:`Python language <python_commands>` |dash| or other
  `Python packages <https://pypi.org>`_  |dash| can be used to further enhance
  your own script.

-  :ref:`Arc <arc-command>` * - a geometric shape that can be drawn on a page
-  :ref:`Arrow <arrow-command>` * - a geometric shape that can be drawn on a page
-  :ref:`Blueprint <blueprint-command>` - a grid of lines that can be drawn on a page
   (see also further :ref:`customisation options <blueprintIndex>`)
-  :ref:`Bezier <bezier-command>` * - a geometric shape that can be drawn on a page
-  :ref:`BGG <the-bgg-command>` - access boardgame data from BGG (typically for display
   on one or more :ref:`cards <the-card-command>`)
-  :ref:`Card <the-card-command>`  - details for a card that is part of a
   :ref:`deck <the-deck-command>`
-  :ref:`Circle <circle-command>` * - a geometric shape that can be drawn on a page
   (see also further :ref:`customisation options <circleIndex>`)
-  :ref:`Compass <compass-command>` * - a geometric shape that can be drawn on a page
-  :ref:`Chord <chord-command>` * - a geometric shape that can be drawn on a page
-  :ref:`Counter <the-countersheet-command>`  - details for a counter that is part
   of a :ref:`countersheet <the-countersheet-command>`
-  :ref:`countersheet <the-countersheet-command>`  - details for a
   countersheet, containing one or more counters
-  :ref:`Create <create-command>` - start of a script; define the
   paper size, output filename, margins, units, fill color etc.
-  :ref:`Data <the-data-command>` - provides a setof information for
   a :ref:`deck <the-deck-command>` or a
   :ref:`countersheet <the-countersheet-command>` ; typically sourced from a CSV or
   Excel file
-  :ref:`Deck <the-deck-command>`  - details for a deck, containing one or
   more :ref:`cards <the-card-command>`
-  :ref:`Dot <dot-command>` * - a geometric shape that can be drawn on a page
-  :ref:`DotGrid <dotgrid-command>` - a set, or group, of dots that can be drawn on a page
-  :ref:`Ellipse <ellipse-command>` * - a geometric shape that can be drawn on a page
-  :ref:`EquilateralTriangle <equilateraltriangle-command>` * - a geometric shape that can be drawn on a page
-  :ref:`Font <the-font-command>` - set the font properties for any :ref:`Text <text-command>` drawn on a page
-  :ref:`Grid <grid-command>` - a set, or group, of lines that can be drawn on a page
-  :ref:`group <group-command>` - a way to  reference a stack of shapes that
   all need to be drawn together on a :ref:`card <the-card-command>`
-  :ref:`Hexagon <hexagon-command>` * - a geometric shape that can be drawn on a page
   (see also further :ref:`customisation options <hexIndex>`)
-  :ref:`Hexagons <hexagons-command>` - a set, or group, of hexagons that can be
   drawn on a page (see also :doc:`hexagonal grids <hexagonal_grids>`)
-  :ref:`Image <image-command>` - an external image that can be shown on a page
-  :ref:`L <the-lookup-command>` - short for *Lookup*; a way to access data in a set
   from another :ref:`card <the-card-command>` in a :ref:`deck <the-deck-command>`
-  :ref:`Layout <layoutIndex>` -  used in conjuction with a location-based
   grid and specifies the shapes that are to be drawn at the grid locations
-  :ref:`Line <line-command>` * - a geometric shape that can be drawn on a page
-  :ref:`Lines <lines-command>` - a set, or group, of lines that can be drawn on a page
-  :ref:`Matrix <the-matrix-command>` - a way to create a set of data, inside a script,
   for use in a :ref:`deck <the-deck-command>` of cards
-  :ref:`PageBreak <pagebreak-command>` - set the start of a new page in
   the document; not required for a :ref:`Deck <the-deck-command>`
-  :ref:`Polygon <polygon-command>` * - a geometric shape that can be drawn on a page
-  :ref:`Polyline <polyline-command>` * - a geometric shape that can be drawn on a page
-  :ref:`Polyshape <polyshape-command>` * - an irregular geometric shape that can be drawn on a page
-  :doc:`Repeat <layouts_repeat>` - repeat the drawing of a shape across a rectangular grid pattern
-  :ref:`Rectangle <rectangle-command>` * - a geometric shape that can be drawn on a page
   (see also further :ref:`customisation options <rectangleIndex>`)
-  :ref:`Rectangles <rectangles-command>` - a set, or group, of rectangles that can be drawn on a page
-  :doc:`RectangularLocations <layouts_rectangular>` - defines an ordered series of
   row and column locations that create a rectangular grid of shapes - the grid itself
   is not displayed; it is used in a :ref:`Layout <layoutIndex>` command.
-  :ref:`Rhombus <rhombus-command>` * - a geometric shape that can be drawn on a page
-  :ref:`S <the-selection-command>` - short for *Selection*; the way to draw a
   shape on a :ref:`card <the-card-command>` depending on a condition
-  :ref:`Save <save-command>` - end of a script; set the export
   image file type and filenames, as well as resolution
-  :ref:`Sector <sector-command>` * - a geometric shape that can be drawn on a page
-  :doc:`Sequence <layouts_sequence>` - lay out a number of items in a straight line
-  :ref:`Square <square-command>` * - a geometric shape that can be drawn on a page
-  :ref:`Stadium <stadium-command>` * - a geometric shape that can be drawn on a page
-  :ref:`Star <star-command>` * - a geometric shape that can be drawn on a page
-  :ref:`Starfield <star-command>` - a set, or group, of dots that can be drawn on a page
-  :ref:`T <the-template-command>` - short for *Template*; the way to access an
   item in a column from a set of :ref:`data <the-data-command>` for a
   :ref:`card <the-card-command>`
-  :ref:`Text <text-command>` * - a shape containing text that can be displayed on a page
-  :ref:`Today <the-today-command>` - display - as text - the current date and time
-  :doc:`Track <layouts_track>` - draw any number of shapes at the vertices of another shape
-  :ref:`Trapezoid <trapezoid-command>` * - a geometric shape that can be drawn on a page
-  :doc:`TriangularLocations <layouts_triangular>`- defines an ordered series of
   row and column locations that create a triangular grid of shapes - the grid itself
   is not displayed; it is used in a :ref:`Layout <layoutIndex>` command.

.. IMPORTANT::

   Commands marked with an asterisk (``*``) can be given with a uppercase or
   lowercase initial (``Commmand`` vs ``command``); meaning the shape should
   either be drawn directly at that point in the script, or that it should be
   "stored" to be drawn later.
