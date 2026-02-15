==============
Basic Concepts
==============

.. |dash| unicode:: U+2014 .. EM DASH SIGN

.. raw:: html

    <style>
    .blue {color:#0000FF; font-weight:bold}
    .cyan {color:#00FFFF; font-weight:bold}
    .dark-blue {color:#293BC7; font-weight:bold}
    .natural {color:#F3B54A; font-weight:bold}
    .forest-green {color:#007700; font-weight:bold}
    .malachite {color:#32CD32; font-weight:bold}
    .cinnamon {color:#D2691E; font-weight:bold}
    .pink {color:#E6506E; font-weight:bold}
    .black {color:#000000; font-weight:bold}
    .picton-blue {color:#00BFFF; font-weight:bold}
    .magenta {color:#BF00BF; font-weight:bold}
    .orange {color:#FFA500; font-weight:bold}
    .white {color:#FFFFFF; font-weight:bold}
    .purple {color:#EE82EE; font-weight:bold}
    .red {color:#FF0000; font-weight:bold}
    .silver {color:#C0C0C0; font-weight:bold}
    .dark-brown {color:#4C271B; font-weight:bold}
    .yellow {color:#FFFF00; font-weight:bold}
    </style>

.. role:: red
.. role:: yellow
.. role:: blue
.. role:: dark-brown


Like many other specialised tools, :doc:`protograf <index>` has its
own set of terms and concepts that act as "short-cuts" to define
its functions and behaviour. Some of these are likely to be common to
other graphics editing or programming tools, but some are specific to it.

This is a general discussion; it may also be useful to look at the more
detailed definitions of some of the terms in the section covering
:doc:`terminology <terminology>`.

.. _table-of-contents-basic:

- `How you’ll use protograf`_
- `The "script" concept`_
- `The "position" concept`_
- `The "command" concept`_
- `The "element" concept`_
- `Element properties`_
- `Working with color`_
- `Working with units`_
- `The "stroke" concept`_
- `The "default" concept`_


How you’ll use **protograf**
============================
`↑ <table-of-contents-basic_>`_

You will be using **protograf** to write what is termed a **script**
i.e. a recipe or list of instructions that are stored in a file.

A script's instructions are used to define a game board, a set of cards
or tiles, or any other, similar, regular graphical design of your choice.

You will then use Python to "run" the script. Python will take the file
you have written, and step through it, line by line, from top to bottom,
to finally create an output PDF file or, optionally, PNG or GIF images,
that will show the outcome of this process - hopefully with your desired
design!

If you want to make changes to the design, then you add to, delete, or
change, the instructions in your script and use Python to process it
again to create an updated version.

.. _script-concept:

The "script" concept
====================
`↑ <table-of-contents-basic_>`_

Creating a *script* is similar to the process of building a house; in
the sense that the instructions which come first create underlying parts
that are "deeper down"; in the same way that a foundation is below a
floor, which in turn is below the walls, which are below the ceiling,
which is below the roof. The lower layers are often not "visible", even
if they are there, but they are just as important!

So, for example, a page may contain rectangles representing cards. Each
card may then have additional rectangles placed on it, representing some
aspect that is part of your card design. Those rectangles, in turn,
could have text, images or icons on/inside them. So, each item that is
created later can "obscure" some part - or even all - of item, or items,
defined previously.

Its also possible to define things earlier in a script that are used, or
reused, later on.

In summary - the *order* of instructions in a script is important as this
will affect what you see at the end!

.. HINT::

   For more detail on what goes into a script, see the section on
   :doc:`Script Anatomy <script_anatomy>`.

.. _position-concept:

The "position" concept
======================
`↑ <table-of-contents-basic_>`_

When using **protograf** what you are doing is defining *where* and
*how* various things should appear on a *page*. A script can create multiple
pages, but will always have at least one.

The position of something is *where* it will be drawn on the page. To do
this, you provide values for both **x** - the horizontal position - and
**y** - the vertical position - for each thing that you want to appear
on the page.

If you look at upright A4 paper - which is 21cm wide and just less
than 30cm high - then a point in the middle of the page will have an **x
position** of 10.5cm - its distance from the left edge of the page; and
a **y position** of 14.8cm - its distance from the top edge of the
page. Similarly, for a US Letter-sized page of 8.5" by 11", a point in
the middle of the page would have an **x position** of 4.25" and a **y
position** of 5.5".

As the use of margins is common for most documents and drawings, nearly all
distances in **protograf** are considered to be relative to the margin
settings i.e. if the page margin, for the A4 page mentioned above,
was set to 2.5cm (1") then to locate a point at those same distances would mean
using an **x position** of 8cm and a **y position** of 12.3cm, as the margin
size will be automatically added onto the values you specify for the position.

.. _command-concept:

The "command" concept
=====================
`↑ <table-of-contents-basic_>`_

Instructions in **protograf** are termed *commands*.

Commands are usually written with an initial **capital** letter. They are
effectively "imperative" in nature, causing something to happen right away;
for example:

- ``Save()`` - instructs the program to save the output to file
- ``Circle()`` - instructs the program to draw a circle at this point in the
  script

The :doc:`summary list of all commands <commands>` is a useful reference
for checking what is available.

.. IMPORTANT::

   In some cases you will use the same command but with a **lowercase initial**
   |dash| often when defining :doc:`shapes <core_shapes>` (including images and
   text) for cards when constructing decks
   (see :doc:`Working with Cards <card_deck_introduction>`).

   When used in this way, the command is **not** carried out straightaway, but
   deferred for activation later on in the script.


.. _element-concept:

The "element" concept
=====================
`↑ <table-of-contents-basic_>`_

Rather than use the slightly clumsy term "thing", **protograf** uses
the term *element*.

Almost everything in **protograf** that appears in the output is
considered to be an element of some sort.

Elements are often geometric **shapes**, such lines, circles or rectangles,
but can also be text or images.

Examples of some of the available geometric **shapes** include:

-  Circle
-  Ellipse
-  Hexagon
-  Polygon
-  Rectangle
-  Rhombus
-  Square
-  Stadium
-  Star
-  Triangle

Descriptions of all of these kinds of shapes, and how to create and use them,
are provided in the section on :doc:`core shapes <core_shapes>`.

Other *elements* include things like :doc:`hexagonal grids <hexagonal_grids>`,
regular :doc:`layouts <layouts>` and :doc:`cards <card_deck_introduction>`.

.. _element-properties:

Element properties
==================
`↑ <table-of-contents-basic_>`_

*Elements*, including *shapes*, can have other settings apart from their
:ref:`position <position-concept>`.

For example, settings can include:

- the *height* |dash| size in the vertical direction and *width* |dash| the
  size in the horizontal direction, of some shapes
- the *stroke*, i.e. color, of the line used to draw a shape
- the *radius* or *diameter* |dash| to set the size of a circle or polygon
- the *paper* size, *margins*, and so forth for the document as a whole

All of these types of settings are termed **properties**.

Most of the common properties are defined in the section covering
:doc:`terminology <terminology>` and their usage is covered in
the section on :doc:`core chapes <core_shapes>`.  Some shapes have
more :doc:`extensive properties  <customised_shapes>`.

.. _basic-color:

Working with color
==================
`↑ <table-of-contents-basic_>`_

Everything we see has color.

Color in **protograf**, is defined in the same way as it is in pages
that appear on the web i.e. in RGB |dash| red-green-blue |dash| *hexadecimal*
format; for example, ``#4C271B`` represents a dark shade of the color that we
would likely term :dark-brown:`"brown"`, while "basic" colors have their own
values; :yellow:`"yellow"` is ``#FFFF00``, :red:`"red"` is ``#FF0000``, and
:blue:`"blue"` is ``#0000FF``.

Colors in **protograf** can also make use of names from a pre-defined
list - for example ``#A0522D`` is defined as the color *sienna*. The
`colorset.pdf <https://github.com/gamesbook/protograf/blob/master/examples/colorset.pdf>`_
file shows all the names of colors that are available, along with their
*hexadecimal* value.  The
`colorset_svg.pdf <https://github.com/gamesbook/protograf/blob/master/examples/colorset_svg.pdf>`_
shows the subset of names and colors available for SVG documents.

Color properties in **protograf** are typically set either with a *"fill"*,
which defines the color of a whole area, or a *"stroke"* which determines
the color of a line or of text.

The :ref:`default <default-concept>` **colors** in **protograf**  are
``white`` for areas and ``black`` for lines.

.. HINT::

   For more details on hexadecimal colors, refer to
   http://www.w3.org/TR/css3-color; the color names are listed in the
   section https://www.w3.org/TR/css-color-3/#svg-color (this list can
   also be found at https://en.wikipedia.org/wiki/X11_color_names)

Quick Colors
------------
`↑ <table-of-contents-basic_>`_

A list of "one-letter" colors is also available (based off of a popular
Python library called *matplotlib*); their hexadecimal codes are also
shown here for reference:

- ``b`` is blue ("#0000FF")
- ``c`` is cyan ("#00FFFF")
- ``d`` is dark blue ("#293BC7")
- ``e`` is earth/natural ("#F3B54A")
- ``f`` is forest green ("#007700")
- ``g`` is green/malachite ("#32CD32")
- ``h`` is brown/cinnamon ("#D2691E")
- ``i`` is pink ("#E6506E")
- ``k`` is black ("#000000")
- ``l`` is picton blue ("#00BFFF")
- ``m`` is magenta/violet ("#BF00BF")
- ``n`` is orange ("#FFA500")
- ``o`` is white ("#FFFFFF")
- ``p`` is purple/lavender ("#EE82EE")
- ``r`` is red ("#FF0000")
- ``s`` is silver/gray ("#C0C0C0")
- ``u`` is dark/derby brown ("#4C271B")
- ``w`` is white ("#FFFFFF")
- ``y`` is yellow ("#FFFF00")
- ``x`` is black ("#000000")


.. _basic-units:

Working with units
==================
`↑ <table-of-contents-basic_>`_

All positions, heights, widths, distances, line thicknesses and other
kinds of lengths or sizes all need to be measured in a particular set of
**units**.

Units are important, and **protograf** requires that the same set of units
applies throughout a specific script (see this
`cautionary story <https://www.simscale.com/blog/nasa-mars-climate-orbiter-metric/>`_
on why not to mix units!)

In the USA, people tend to use the so-called Imperial System. In
**protograf** this means that distances might be measured in units of
*inches*. Inches are often shown with a double-quotes symbol (``"``)
in documents; in **protograf** inches are often referred to using the
abbreviation *in*.

In almost all of the rest of the world, the Metric System is in use. In
**protograf** this means that distances will be measured in units of
centimetres; referred to in **protograf** as *cm*. Alternatively, you
can choose to use millimetres, abbreviated in **protograf** as *mm*.

The :ref:`default <default-concept>` **units** in **protograf**  are *cm*.

.. HINT::

   For conversion purposes, 1 inch equals 2.54 centimetres or 25.4
   millimetres.

**protograf** also allows units of *points*, which are the measurement
units traditionally used in the printing industry. There are 72 points
in 1 inch. Internal calculations in **protograf** are all done in
point units i.e. all inputs, regardless of being inches, centimetres,
millimetres |dash| or anything else |dash| are converted to points.

.. NOTE::

   In a few cases, **protograf** adopts the word "size" or "width" where
   point units are in use e.g. font size, stroke width and dot width, but
   because "size" is such a general term, it's not really used elsewhere.


.. _stroke-concept:

The "stroke" concept
====================
`↑ <table-of-contents-basic_>`_

While the majority of size-based `element properties`_ in **protograf**
work with the "normal" units you have chosen |dash| inches or centimetres
|dash| some use points (see `working with units`_ above). These include
*font size*,  that you’re likely familiar with from word processing programs,
and line thickness |dash| termed "stroke width". The reason for doing this
is to maintain consistency with other, existing tools.


.. _default-concept:

The "default" concept
=====================
`↑ <table-of-contents-basic_>`_

A "default", in terms of **protograf**, is a value or setting for
something |dash| usually a `property <element properties_>`_ |dash| which is
used unless you specify otherwise.

Defaults are helpful for quickly drawing or testing something until you're
ready to make decisions about your own specific settings or values.

Some examples of defaults are:

-  the default *margin* for pages in the output PDF is ``0.635`` cm
   or 1/4" (one quarter of one inch); the main reason for this choice is to
   ensure that a 3x3 grid of Poker-sized cards fits onto one page!
-  the default *paper* size for pages in the output PDF is ``A4`` |dash| similar
   to the US ``Letter`` size i.e. A4 paper is 21 cm x 29.7 cm (8.268 inch x
   11.693 inch) and Letter paper is 8.5 inch x 11 inch (21.59 cm x 27.94 cm)
-  the default *units* are centimetres (*cm*)
-  the default *x* and *y* positions are each ``1`` (one) |dash| with default
   units that equates to *1 cm*
-  the default line *length* is ``1`` (one)  |dash| with default units that
   corresponds to *1 cm*
-  the default line *stroke width* is ``1`` point |dash| that corresponds to
   1/72 inches (or 0.353 mm)
-  the default line *stroke* color is ``black`` |dash| a hexadecimal
   value of ``#000000``
-  the default area *fill* color is ``white`` |dash| a hexadecimal
   value of ``#FFFFFF``
-  the default *font* is ``Helvetica``, with a *size* (height) of ``12`` points
   and a *stroke* color of ``black``

.. HINT::

  A default which may be less obvious is the name of the output file created
  by :doc:`protograf <index>`.  This matches the name of the script but the
  extension is changed to ``.pdf`` because this is the default output type
  that is created. So, if your script is called ``test01.py`` then the
  default output file that is created will be called ``test01.pdf``.

  Use the :ref:`Create <create-command>` command to set your own output
  *filename*.
