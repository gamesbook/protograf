==============
Script Anatomy
==============

.. |dash| unicode:: U+2014 .. EM DASH SIGN

A "script" is the short-cut name for a file containing a list of instructions
that will be read and processed by Python.  The script filename is usually given
an extension of ``.py``

.. HINT::

    This document assumes that :doc:`protograf <index>` is working on your
    computer after successfully :doc:`Setting Up <setting_up>`, and that you
    have read and understood the :doc:`Basic Concepts <basic_concepts>`

.. _table-of-contents:

Table of Contents
=================

- `Start, Middle and End`_
- `Key Commands`_

  - `Create Command`_
  - `PageBreak Command`_
  - `Save Command`_
- `Other Commands`_
- `Comments`_
- `Drawing vs Assigning`_
- `Basic Shapes`_
- `Card Decks`_
- `Layouts, Sequences, Tracks and Grids`_
- `The FEEDBACK Message`_
- `Making Mistakes`_


Start, Middle and End
=====================
`↑ <table-of-contents_>`_

A script will normally start with a `Create command`_, then contain a series
of `other commands`_ with the instructions for your particular needs (each
command can run over multiple lines).


.. HINT::

    If your needs are more complex, you have the options of embedding "pure"
    Python commands and/or using tools provided by other Python libraries.

If the design you are working on requires multiple pages, then a
`PageBreak command`_ can be inserted, followed again by the specific commands
you need.

The final command in the script will be the `Save command`_, which triggers the
creation of the output; by default a PDF file |dash| optional PNG or GIF output
is available as well.

.. _key-commands:

Key Commands
============
`↑ <table-of-contents_>`_

- `Create Command`_
- `PageBreak Command`_
- `Save Command`_
- `Other Commands`_

.. _create-command:

Create Command
--------------
`^ <key-commands_>`_

The ``Create()`` command is the essential command that **must** appear first
in every script.

``Create()`` sets up the basic document framework to support all of the
elements that will appear after it.

.. HINT::

    If you omit the ``Create()`` command, you should get a
    `FEEDBACK <feedback-message_>`_ message::

        FEEDBACK:: Please ensure Create() command has been called first!

By default, this command will setup an A4 page |dash| in portrait mode |dash|
with a margin of one-half inch (1.25cm), and units of centimetres;
the resulting output file will have the same name as the script,
but with a '.pdf' extension.

To customise the command, set its properties as follows:

- **paper** - use a paper size from either of the ISO series - A0 down to A8;
  or B6 down to B0 - or a USA type - letter, legal or elevenSeventeen; to change
  the page orientation to **landscape** simply append ``-l`` to the name |dash|
  for example, ``"A3-l"`` is a landscape A3 paper size
- **filename** - name of the output PDF file; by default this is the prefix
  name of the script, with a ``.pdf`` extension
- **units** - these can be ``cm`` (centimetres), ``in`` (inches), ``mm``
  (millimetres), or ``points``; the default is ``cm``
- **margin** - set the value for *all* margins using the defined *units*
- **margin_top** - set the top margin
- **margin_bottom** - set the bottom margin
- **margin_left** - set the left margin
- **margin_right** - set the the right margin


Example 1
~~~~~~~~~

Here is an example of a customised ``Create`` command, for an A3-sized page
in landscape mode, with top and left margins being 2 inches each:

.. code:: python

    Create(
        paper="A3-l",
        units="in",
        filename="testA3.pdf",
        margin_top=2,
        margin_left=2,
    )

.. _pagebreak-command:

PageBreak Command
-----------------
`^ <key-commands_>`_

The ``PageBreak()`` command is only needed when you need to start a new page.

When generating a :doc:`deck of cards<card_decks>` the program will
automatically insert ``PageBreak()`` commands as needed, if the cards occupy
multiple pages.

.. _save-command:

Save Command
------------
`^ <key-commands_>`_

The ``Save()`` is usually the last to appear in a script.

The ``Save()`` command, by default, simply results in the outcome of all the
commands used to that point being written out to a PDF file; either with a
default filename, or with the one set in the `Create Command`_ .

To customise the command, set its properties as follows:

- **output** - this can be set to ``png`` to create one image file per page of
  the PDF; by default the name of the PNG files are derived using the PDF filename,
  with a ``-`` followed by the page number; if set to ``gif`` will create a GIF
  file composed of all the PNG pages that would have been created
- **dpi** - can be set to the dots-per-inch resolution required; by default
  this is ``300``
- **names** - this can be used to provide a list of names |dash| without an
  extension |dash| for the image files that will be created from the PDF; the
  first name corresponds to the first page, the second name to the second and
  so on.  Each will automatically get the ``.png`` extension added to it.
  If the term ``None`` is used in place of a name, then that page will **not**
  have a PNG file created for it.
- **framerate** - the delay in seconds between each "page" of a GIF image; by
  default this is ``1`` second

Example 1
~~~~~~~~~

Here is an example of a customised ``Save`` command:

.. code:: python

    Save(
        output='png',
        dpi=600,
        names=['pageOne', None, 'pageThree']
    )

In this example, **no** PNG file will be created from the second page, while PNG
files named ``pageOne.png`` and ``pageThree.png`` will be created from
the first and third pages of the PDF file.

Example 2
~~~~~~~~~

Here is another example of a customised ``Save`` command:

.. code:: python

    Save(
        output='gif',
        dpi=300,
        framerate=0.5
    )

In this example, an animated GIF image will be created, assembled out of the
PNG images; one per page of the PDF.  There will be a delay of half-a-second
between the showing of each image.


Other Commands
--------------
`^ <key-commands_>`_

There are numerous other commands which are either used to draw shapes, or
sets of shapes, or to control how and where sets of shapes appear on a page.
See:

- :doc:`Core Shapes <core_shapes>`
- :doc:`Card and Deck commands <card_decks>`
- :doc:`Further commands <additional_commands>`
- :doc:`Layout <layouts>` commands
- :doc:`Hexagonal Grid <hexagonal_grids>` commands


Comments
========
`↑ <table-of-contents_>`_

It can be useful to "annotate" a script with other details that can remind
you, as a reader, about any of the "what" or "why" aspects of the script.

These comments are effectively ignored by Python and **protograf** and
have no effect on the output.

Single Line Comments
--------------------

Simply insert a ``#``, followed by space, at the start of the comment line:

.. code:: python

    # this is the rim of the clock
    Circle(stroke_width=5)

Multiple Line Comments
----------------------

Use a pair of triple-quotes to surround all the lines of comments:

.. code:: python

    """
    This is a useful script.
    It was created to remind me about Circles.
    It should not be used for normal designs.
    """
    Circle(stroke_width=5)

Make sure the quotes appear at the **start** of the lines they are used in.


Drawing vs Assigning
====================
`↑ <table-of-contents_>`_

All of the :doc:`shape <core_shapes>` commands can either be called with a
**capital** letter or a **lowercase** letter.

The use of a capital is the more common case, and it effectively tells
**protograf** to "draw this shape now":

.. code:: python

    Circle(stroke_width=5)

The use of a lowercase is normally when you assign a shape to a name, so that
it can be used |dash| or drawn |dash| later on in the script:

.. code:: python

    # this circle is *not* drawn at this point of the script
    clock = circle(stroke_width=5)

    # the circle - aka "clock" - drawn when cards are drawn
    Card("1-9", clock)


Basic Shapes
============
`↑ <table-of-contents_>`_

**protograf**  allows for the creation of many shapes, with a command for
each one.

These are described in the :doc:`Core Shapes <core_shapes>` section, which
also covers common customisation options.

More extensive customisation of some shapes is also possible; see the
:doc:`Customised Shapes <customised_shapes>` section.


Card Decks
==========
`↑ <table-of-contents_>`_

A common element in many games is a deck - or multiple decks - of cards.
**protograf** also considers items such tiles or counters to be "cards";
they are really just "shapes containing other shapes"

There are two key commands for creating a deck of cards: the ``Card()`` and
the ``Deck()``.  These are discussed in detail in the
:doc:`card decks <card_decks>` section, while the options for customisation of
the deck itself are discussed in the :doc:`Deck command <deck_command>`.

A useful "getting started" approach is to look through the section with
:doc:`worked examples <worked_example>` which shows an increasingly
complex set of examples for setting up and running scripts to generate a
deck of cards.


Layouts, Sequences, Tracks and Grids
====================================
`↑ <table-of-contents_>`_

A basic layout is that of a simple **sequence**, with shapes placed
at regular positions in a linear direction.

A **track** can be defined as the borders of a rectangle or polygon shape;
or at specific angles along the circumference of a circle. Shapes can then
be placed at these locations.

The other way that elements can be laid out on a page is through a
**grid layout** which can be derived from a built-in shape such ``Hexagons``
or constructed using a defined set of properties.

These are all described in the :doc:`Layouts <layouts>` section.

There is also a separate section on :doc:`Hexagonal Grids <hexagonal_grids>`
which describes the variety of these types of grids, as well as some options
for adding shapes to them.


.. _feedback-message:

The FEEDBACK Message
====================
`↑ <table-of-contents_>`_

Normally, a script will run without you seeing anything. However, there are
some occasions when you will see feedback or warning message of some kind.

1. **An error happens** - this is described further in the section on
   `making mistakes`_
2. **Generating Images from Save()** - this will show a message like::

        FEEDBACK:: Saving page(s) from "/tmp/test.pdf" as PNG image file(s)...
3. **Accessing BGG** - you can enable progress when using the
   :ref:`BGG() <the-bgg-command>` command, to retrieve boardgame
   information, as follows::

        # progress is True - games retrieval is shown
        BGG(ids=[1,2,4], progress=True)

   In this case you will see messages like::

        FEEDBACK:: Retrieving game '1' from BoardGameGeek...
4. **An empty Layout** - this is just a warning issued because the
   ``Layout()`` has no shapes allocated for it to draw::

        rect = RectangularLayout(cols=3, rows=4)
        Layout(rect)

   then you will see a message like::

        WARNING:: There is no list of shapes to draw!

   This is not an error, but does act as a reminder about what might still
   be needed.


Making Mistakes
===============
`↑ <table-of-contents_>`_

It is, unfortunately, all too easy to make mistakes while writing scripts.
Some common kinds of mistakes are listed below - these are in no way
meant to be comprehensive!

Supplying the script an **incorrect value**, for example, giving the
location a value of ``3.0`` when you meant to give it ``0.3``; this kind
of mistake can usually be detected when you look at the PDF, although it
may not be immediately obvious exactly what has happened.

Supplying the script an **incorrect kind of value**, for example, giving
the ``y`` location a value of ``a`` instead of a number. The script will
stop at this point and give you a feedback message::

    FEEDBACK:: The "a" is not a valid float number!
    FEEDBACK:: Could not continue with program.

Supplying the script a **property that does not exist**, for example,
using ``u=2.0`` when you meant to say ``y=2.0``. This can happen
because those two letters are located right next to each other on a
keyboard and the letters are a little similar. In this case, the script will
"fail silently" because properties that don’t exist are simply ignored.
This kind of mistake is much harder to spot; often because the default value
will then be used instead and it will seem as though the script is drawing
something incorrectly.

Supplying the script with a **duplicate property**, for example:

.. code:: python

   display = hexagon(stroke="black", fill="white", height=2, stroke=2)
                                                             ^^^^^^^^
   SyntaxError: keyword argument repeated: stroke

This kind of mistake is usually easier to see as both keywords, in this
case, are part of the same command and the error message that you see also
highlights the repetition with the ``^^^^^^^^`` characters.

.. HINT::

   Errors are discussed further in the :ref:`Script Errors <script-errors>`
   section.
