===========
Terminology
===========

.. |dash| unicode:: U+2014 .. EM DASH SIGN

:doc:`protograf <index>` uses many terms; most of which should |dash|
hopefully! |dash| be fairly obvious by their name, or by the context in
which they are used.

However, in order to help with clarity, below is a reasonably comprehensive
list of terms used in different places, grouped by what aspects they affect.

Note that some shapes, such as the :ref:`Hexagon <hexIndex>`, or
:ref:`Circle <circleIndex>`, have extensive customisation properties
available; its better to refer to their specific descriptions to understand
exactly how these can used.

.. _table-of-contents-terms:

- `protograf Jargon`_
- `Color-orientated Terms`_
- `Position- and Location-orientated Terms`_
- `Size- and Length-orientated Terms`_
- `Amount- and Count-orientated Terms`_
- `Direction-orientated Terms`_
- `Styling-orientated Terms`_
- `Display-orientated Terms`_
- `Area-orientated Terms`_
- `Miscellaneous Terms`_


protograf Jargon
==================
`↑ <table-of-contents-terms_>`_

**protograf** uses a number of 'generic' terms which you'll see in many
places in the documentation:

- **command** - an instruction that is specified in a **protograf** script;
  see a full list in the :doc:`Commands <commands>` section
- **default**  - a value set by **protograf** if no other is given;
  for example, the line length defaults to being 1 centimetre long
- **list** - a number of comma-separated values enclosed in square brackets
  e.g. ``[1, 2, 3]`` |dash| whihc are usually assigned to a **property**
- **property** - an aspect of a command or shape that helps define how it works
  or looks; for example, a circle might have its size defined by using a radius
  property of 2 centimetres - in a script this would be shown as ``radius=2``
- **shape** - a geometric element, for example, a circle, square, text or
  line i.e. something that can be drawn |dash| see a list in the
  :doc:`Shapes <core_shapes>` section
- **script** - a file,  that can be **run**, containing various **protograf**
  commands |dash| see an outline in :doc:`Script Anatomy <script_anatomy>`
- **set** - a number of comma-separated values enclosed in round brackets
  e.g. ``(1, "a")`` |dash| these are usually assigned to a **property**
- **run** - to cause Python to act on the script so that all instructions in
  it are carried out |dash| this should usually cause an output file to be
  created (or recreated)
- **vertex** / **vertices** - the sharp "points" at the intersection of the
  lines used to construct a shape; for example, a triangle has 3 verticesl;
  a square has 4 vertices and a hexagon has 6 vertices.
- **_x** and **_y** - some terms can be modified to be specific for
  *x* (left to right) or *y* (top to bottom) distances by appending one of
  these underscore-prefixed terms to them


.. _termsColor:

Color-orientated Terms
======================
`↑ <table-of-contents-terms_>`_

Color is defined in the same way as it is in pages that appear on the
web i.e. in RGB (red-green-blue) *hexadecimal* format, for example,
``#A0522D`` represents a shade of the color that we would likely term
"brown".

Colors can also be chosen from a pre-defined list of names, for example
``#A0522D`` is pre-defined in **protograf** as the color *sienna*.

A PDF file
`colorset.pdf <https://github.com/gamesbook/protograf/blob/master/examples/colorset.pdf>`_
shows all the names and colors that are available.

.. HINT::

   For more details on hexadecimal colors, refer to
   http://www.w3.org/TR/css3-color; the color names are listed in the
   section https://www.w3.org/TR/css-color-3/#svg-color (this list can
   also be found at https://en.wikipedia.org/wiki/X11_color_names)

In general, color can be set for the lines (**stroke**) and areas
(**fill**) that are being drawn on a page.

-  **dot_fill** - the color in which a circle is to be drawn at the
   centre of a shape
-  **fill** - the color with which an area is filled
-  **outline** - sets the line color, and at the same time sets the fill
   to be ``None``
-  **stroke** - the color in which a line or text is drawn; there are
   many strokes for particular types of lines that are set by prefixing
   this term with the name of the item in question; for example:
   **cross_stroke**; **grid_stroke**; **label_stroke**; **petals_stroke**,
   **perbis_stroke**; **radii_stroke**; etc.
-  **stroke_fill** - sets both the line ("stroke") and area ("fill") to
   be the *same* color

.. IMPORTANT::

   **Note** that it is possible to use the term *None* in place of a
   specific color; this effectively means that nothing will be drawn
   there - this results in an "invisible" line or area!


.. _termsPosition:

Position- and Location-orientated Terms
=======================================
`↑ <table-of-contents-terms_>`_

Everything in **protograf** that needs to be displayed or drawn or
positioned must be placed at a **position** on the page; i.e. each thing
must have both a horizontal position - its **x** value - and a vertical
position - its **y** value. These respectively represent the distances
from the left- and top-edge of a page or a card.

**Location** is a more general term; it can be a combination of the **x**
and **y** positions; it could be a row and/or column identifier; it
could be a sequence identifier; or just a indicator of where something
is relative to something else, for example, a coordinate being drawn
at the *top* of a Hexagon.

-  **align** - used to move text horizontally, relative to its starting
   location; can be one of: *justify*, *left*, *right*, or *centre*
-  **cx** - the centre position of a shape, going in the horizontal
   direction; its usually the case that the distance is not absolute, but
   relative to some other value e.g. distance from a margin; or the edge
   of a ``Card``
-  **cy** - the centre position of a shape, going in the vertical
   direction; its usually the case that the distance is not absolute, but
   relative to some other value e.g. distance from a margin; or the edge
   of a ``Card``
-  **elevation** - a relative vertical location within a shape; can be one
   of: *top*, *middle*, or *bottom*
-  **x** - the position of a point in the horizontal direction; its
   usually the case that the distance is not absolute, but relative to
   some other value e.g. distance from a margin; or the edge of a
   ``Card``; or the away from the centre of a Hexagon in a grid
-  **y** - the position of a point in the vertical direction; its usually
   the case that the distance is not absolute, but relative to some
   other value e.g. distance from a margin; or the top edge of a ``Card``


.. _termsSize:

Size- and Length-orientated Terms
=================================
`↑ <table-of-contents-terms_>`_

The majority of length properties |dash| width, height, diameter etc. |dash|
will be numeric values, corresponding to the **unit** in use unless
otherwise noted. The default is usually ``1``.  The default **unit** is
*centimetres* ("cm"), so the default length is 1 centimetre.

Some sizes are set in **points** |dash| there are 72 points in an inch
|dash| so as to align with existing conventions, or simply because these
items are typically very tiny. As far as possible, the term **size** is
reserved for these settings; for example, **font_size** and **dot**.
An exception is **stroke_width** which is also in points, again
because of convention.

A few sizes are given descriptive names; this makes them a little easier
to set.

-  **caltrops** - a descriptive term for the relative dimensions of a
   "caltrop" - the small three-pointed shape drawn at the vertex of a
   hexagon
-  **dot** - the diameter of a small ``Dot`` in **points**
-  **cross** - the height and width of the intersecting lines drawn at
   the centre of a shape
-  **height** - the vertical dimension of a shape e.g. a ``Rectangle``
   or a bitmap ``Image``
-  **leading** - the spacing, in points, between lines of wrapped ``Text``
-  **interval** - the distance between the centres of a series of shapes;
   typically in a repeated pattern of some type
-  **margin** - used in ``Create`` command to set all margins for a
   page; the default for any margin is 0.635cm or 6.35mm (quarter of an inch)
-  **margin_top** - used in ``Create`` command to set a top margin for a
   page |dash| this overrides the **margin** property, if any
-  **margin_bottom** - used in ``Create`` command to set a bottom margin
   for a page  |dash| this overrides the **margin** property, if any
-  **margin_left** - used in ``Create`` command to set a left margin for a
   page |dash| this overrides the **margin** property, if any
-  **margin_right** - used in ``Create`` command to set a right margin for
   a page |dash| this overrides the **margin** property, if any
-  **paper** - used in ``Create`` command to set the paper format in the
   document; either ISO series |dash| A0 down to A8; or B6 down to B0 |dash|
   or a USA type; the default is A4.
   **NOTE:** to switch to landscape orientation, append an ``l`` to the name;
   so ``"A5-1"`` set the page to use A5 landscape paper
-  **radius** - the radius of a ``Circle``
-  **scaling** - the amount by which an SVG image should be shrunk or
   expanded e.g. 0.5 makes it half-size and 2.0 doubles its size; but
   because SVG is a vector-format, there will be no loss of resolution
   through scaling
-  **side** - the length of a side of some shapes (e.g. ``Square``,
   ``Polygon``, ``Grid``) as well as the distance between each adjacent
   point in a ``TriangularLayout``
-  **stroke_width** - the thickness of a line in **points**; many
   specific widths are set by prefixing this term with the name of the
   item in question; examples: **cross_stroke_width**;
   **grid_stroke_width**; **radii_stroke_width**; **perbsis_stroke_width**,
   etc.
-  **width** - the horizontal dimension of a shape e.g. a ``Rectangle``
   or a bitmap ``Image``


.. _termsAmount:

Amount- and Count-orientated Terms
==================================
`↑ <table-of-contents-terms_>`_

-  **sides** - the number of sides of a ``Polygon`` shape


.. HINT::

    The concept of counting is also important when creating a ``Track`` or a
    ``Sequence`` or a deck of ``Card`` s |dash| each item being created is
    assigned a **sequence** number which can be used for reference or
    labels or text.


.. _termsDirection:

Direction-orientated Terms
==========================

In general, there are two primary ways of determining direction of
something; either by a **compass direction** or by an **angle**.
Other, more descriptive directions are also used.

The *angle* is the amount of rotation, in degrees, starting from a value
of zero (0) which is assumed to be the line parallel to the bottom of
the page as you would normally look at it. Ninety (90) degrees is the
angle of a line parallel to the vertical sides of the page, and so on.

The maximum allowed rotation is 360 degrees i.e. a full sweep around a
circle.

A *compass direction* is one of the following:

Primary compass directions |dash| with full names shown in brackets:

-  n (north) - normally corresponds to an angle of 90 degrees
-  s (south) - normally corresponds to an angle of 270 degrees
-  e (east) - normally corresponds to an angle of 0 degrees
-  w (west) - normally corresponds to an angle of 180 degrees

Secondary compass directions |dash| with full names shown in brackets:

-  ne (north-east) - normally corresponds to an angle of 45 degrees
-  se (south-east) - normally corresponds to an angle of 315 degrees
-  nw (north-west) - normally corresponds to an angle of 135 degrees
-  sw (south-west) - normally corresponds to an angle of 225 degrees

.. NOTE::

   If a compass direction is used in the context of a ``Hexagon``,
   then the angle is "reinterpreted" to match its context
   e.g. the *NE* angle for a ‘pointy’ hexagon is 60, not 45, degrees.

Properties that use direction include:

-  **clockwise** - a ``True`` or ``False`` setting used to determine
   direction of travel around a circle
-  **direction** - can be any primary compass direction; used to show
   the travel route when moving through various types of layouts
   e.g. ``RectangularLayout``
-  **edges** - can be any primary compass direction; used to indicate
   the sides of a ``Square`` or ``Rectangle``
-  **flat** - the *orientation* of a ``Hexagon``, meaning the top of it will
   be parallel to the bottom edge of the paper
-  **facing** - can be any primary compass direction; used to show
   orientation of some types of layouts e.g. ``DiamondLayout``
-  **flip** - the relative vertical direction in which a triangle or rhombus
   must be drawn; can be either: *north* or *south*
-  **hand** - the relative horizontal direction in which a triangle must
   be drawn; can be either: *east* or *west*
-  **orientation** - used for drawing hexagons; can be either: *flat* or
   *pointy*
-  **pointy** - the *orientation* of a ``Hexagon``, meaning the top of it will
   make a "peak" relative to the bottom edge of the paper, and the flat edge
   will be parallel to the left side of the paper.
-  **start** - can be any secondary compass direction; for example, it is
   used to show in which corner of a ``RectangularLayout`` that shapes
   should first placed when creating a track


.. _termsStyling:

Styling-orientated Terms
========================
`↑ <table-of-contents-terms_>`_

-  **dotted** - allows a line to be broken into a series of "dots" |dash| very
   short lines |dash| of length equal to the width of the line being drawn,
   with spacing in-between each dot of that same length; to make a line dotted,
   simply use ``dotted=True``
-  **dashed** - allows a line to be broken into a series of short lines,
   separated by spaces defined in a list; the first number is the length of
   the dash; the second is the length of the space between two dashes |dash|
   note that sizes will be rounded to the nearest whole point value; so ``2cm``
   which is equivalent to ``56.693`` points will be changed to ``57`` points
-  **rounded** - causes the end of a line to be drawn with a semi-circle; to
   make a line rounded, simply use ``rounded=True``
-  **transform** - will change text in a ``Text`` command to *uppercase*,
   *lowercase*, or *capitalise* it
-  **transparency** - a percentage value from 1 to 100 that determines how
   "see through" a shape, or line, or area is; where ``1`` means it is nearly
   not transparent and `100` means it is completely transparent. It is also
   possible to use a fractional number e.g. ``0.5`` equates to 50%. Some
   programs use the term *opacity*; but note that that is the inverse of
   transparency.

.. _termsDisplay:

Display-orientated Terms
========================
`↑ <table-of-contents-terms_>`_

-  **hidden** - a list of locations, indicated by their *row and
   column* identifier, which should **not** be used for display - the rest
   are displayed as normal
-  **hatch** - when used in combination with **hatch_count** will draw a series
   of parallel lines between two opposing sides of a regular shape in the
   specified direction
-  **masked** - a list of locations, indicated by their *sequence
   number* |dash| i.e. their position in the drawing order |dash| which
   should **not** be used for display |dash| the rest are displayed as normal
-  **radii** - if given a value of ``True`` will cause the radii of a
   ``Polygon``or ``Hexagon`` to be shown
-  *paths* - a list of one or more pairs of *compass directions*, representing
   two edges of a hexagon shap,e between which a line |dash| straight or an
   arc |dash| is drawns
-  **perbis** - if given one or more numbers will cause the perpendicular
   bisectors |dash| lines from centre to the middle of the edges |dash| of
   a ``Polygon`` or ``Hexagon`` to be shown; edges are numbered from the
   east-facing one in an anti-clockwise direction
-  **shown** - a list of locations, indicated by their *row and
   column* identifier which are the only ones that **must** be used for
   display - the rest are ignored
-  **visible** - a list of locations, indicated by their *sequence
   number* |dash| i.e. their position in the drawing order |dash| that
   **must** be used for display - the rest are ignored

.. _termsArea:

Area-orientated Terms
=====================
`↑ <table-of-contents-terms_>`_

-  **frame** - used to demarcate the boundary of a ``Card``; one of
   *rectangle*, *hexagon*, or *circle*
-  **perimeter** - used to demarcate the boundary of a ``StarField``;
   one of *circle*, *rectangle* or *polygon*
-  **peaks** - a series of **sets**, each containing a primary compass
   direction and a value, that designate that the edge of a rectangle
   should be drawn as a triangular "peak"; e.g. a **set** of ``('n', 2)``
   would draw a 2cm high triangle on the upper (north) edge
-  **shades** - a way to fill in the rhombus-shaped subsections of a hexagon
   in order to create the effect of a ``Cube``
-  **slices** - a way to fill in triangular sections of a square, rectangle or
   rhombus by supplying a list of colors; for a square or rectangle, a
   **slices_line** can also be used to create both trapezoids and triangles
   which gives the appearance of a building's roof when viewed from above
-  **tetris** - when set to ``True`` will cause a ``Tetronimo`` to be styled
   as per the original Tetris game pieces

.. _termsMiscellaneous:

Miscellaneous Terms
===================
`↑ <table-of-contents-terms_>`_

-  **debug** - a value can be set for this that will cause underlying
   values or locations or positions to be displayed e.g. using ``debug="n"``
   for a layout will show small dots where each point in that layout exists
-  **GIF** - Graphics Interchange Format. A file format in which an image
   can be stored; its useful because it supports multiple layers and can be
   animated
-  **PNG** - Portable Network Graphic. A file format in which an image can
   be stored; its useful because it supports transparent backgrounds
-  **SVG** - Scaleable Vector Graphics. A file format in which an image can
   be stored; its a vector-format unlike the bitmap- or raster-format of PNG
   and JPEG files, so its size can be changed without loss of quality
