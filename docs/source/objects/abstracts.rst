==============================
AbstractGame and AbstractState
==============================

.. |dash| unicode:: U+2014 .. EM DASH SIGN

The ``AbstractGame`` and ``AbstractState`` are two of a number of commands
used to create what are termed :doc:`Compound Objects <index>`.

This section assumes you are very familiar with the concepts, terms and ideas
for :doc:`protograf <../index>`  as presented in the
:doc:`Basic Concepts <../basic_concepts>` , that you understand all of the
:doc:`Additional Concepts <../additional_concepts>` and that you've created some
basic scripts of your own using the :doc:`Core Shapes <../core_shapes>`. You
should also be familiar with the various types of shapes' properties described in
the :doc:`Customised Shapes <../customised_shapes>`.

.. _abstractOver:

Overview
========

Abstract games are the ancestors of many modern games.  They continue to be
much played and appreciated by gamers of all ages across many societies.
In addition, many new abstract games are still being designed and tested.

The aim of the ``AbstractGame`` and ``AbstractState`` commands is to allow
diagrams for such games to be readily created.

The ``AbstractGame`` command allows for the details of the board and pieces
for such a game to be specified.   However, such an object is **not** designed
to be drawn |dash| it can be thought of as the game being "still in the box".

The ``AbstractState`` command will, when supplied with a previously defined
AbstractGame, allow for a position in the game |dash| at any point from
the setup through to its end state |dash| to be shown in diagrammatic form
and, optionally, annotated.

A series of ``AbstractState`` commands, all using the same AbstractGame could,
if required, depict an entire game but this is not the primary intended use
of the AbstractState command.

.. NOTE::

  An AbstractState command does not have the concept of a game "move".
  Tracking and processing such is beyond the scope of **protograf**.
  The *annotations* property for the AbstractState can be used to show
  movement of pieces with, for example, a line or arrow.

.. _abstractgame-command:

AbstractGame Command
====================

The ``AbstractGame()`` command defines the parts of an abstract game; primarily
the type of board and pieces that it uses.

A board can be specifed either by referring to an existing abstract game by
name |dash| for example, Chess, Checkers (aka Draughts), or Go |dash| or via
a specific combination of rows and columns.

Pieces can also be specified by the type of game that they are usually used
with |dash| for example, Chess, Checkers (aka Draughts), or Go. It is also
possible to create completely unique pieces by using one or more of
*protograf* shapes and/or images.

.. NOTE::

    The default settings for an AbstractGame are:

    * *name*: ``grid``
    * *rows*: ``8`` (the same as Chess or Checkers board)
    * *cols*: ``8`` (the same as Chess or Checkers board)
    * *pieces*: ``checkers`` (simple black and white circles)

    Note also that the definitions of the board and pieces are **not** the
    determinants of where the pieces get placed; how many pieces there are,
    or what the rules are for their movement!

.. _abstractGameProperties:

AbstractGame Properties
-----------------------

The properties that can be set for an AbstractGame are:

* *name*: the name of a type of board; which can chosen from
  one of: ``chess``, ``checkers``, ``go``; if omitted, the
  type is a simply a ``grid``
* *pieces*: details of pieces that will be placed on the board; the piece set
  can |dash| **independantly** of the board name |dash| be chosen from a
  pre-existing set: ``chess``, ``checkers`` (the default), ``go`` or a
  customised list; see below for `AbstractGame Pieces`_
* *colors*: a list of one or more :ref:`colors <basic-color>`  in which to draw
  alternating board spaces; the default is to draw all squares ``white`` (or
  the board's *fill* color)
* *hairs*: if ``True``, draw small lines extending outwards from the board's
  gridlines; these lines are one-quarter of the length of a board cell, for
  example, if the board had squares of side 1 inch, then the hairs would be
  one-quarter of an inch long
* *labels*: if ``True``, draw labels along board edges, using notation
  appropriate to the type of board; the primary labelling system is based on
  the one used for Chess
* *grid_align*: if ``True``, draw pieces on grid intersections, not grid spaces,
  and label lines, not spaces
* *pieces_resize*: a fractional value by which to resize the built-in piece
  shapes or images; this defaults to ``1`` |dash| note that this does **not**
  apply to custom-made shapes
* *cols*: if no game *name* is set |dash| each associated with a predefined
  number of columns |dash| then this is the number of cells in the horizontal
  direction for a regular grid; a default of  ``8`` is used
* *rows*: if no game *name* is set |dash| each associated with a predefined
  number of columns |dash| then this is the number of cells in the vertical
  direction for a regular grid; a default of  ``8`` is used
* *width* and *height* refer to the overall board size on the page; if omitted,
  the board will be automatically sized to fit within the smallest available
  space inside of the page margins.  The size of cells on the board are based
  on these values, using the *rows* and *cols* values
* *annotations*: a list of AbstractGame annotations; see below for details


.. _abstractGameBoard:

AbstractGame Board
------------------

A basic AbstractGame board is just a square grid and, depending on the game,
will contain either an equal or unequal number of rows and columms.

Such a grid allows pieces to be placed either in the spaces between the lines
or on their intersection points |dash| **protograf** terms these locations
*cells*.


.. _abstractGamePieces:

AbstractGame Pieces
-------------------


.. _abstractGameAnnotations:

AbstractGame Annotations
------------------------


.. _abstractGameExamples:

AbstractGame Examples
----------------------


.. _abstractstate-command:

AbstractState Command
=====================

The ``AbstractState()`` command will create a display of a board and its pieces
that have been defined in an :ref:`AbstractGame <abstractgame-command>`. This
display represents a given point in an abstract game |dash| a situation commonly
referred to as "the game state".

.. _AbstractStateProperties:

AbstractState Properties
------------------------

The properties that can be set for an AbstractState command are:

* *board*: an AbstractGame object; this is a required setting and the
  AbstractState object cannot be displayed without it
* *positions*: details of where an AbstractGame's pieces go on the board;
  see below for details
* *annotations*: a list of AbstractState annotations; see below for details

.. _abstractStatePositions:

AbstractState Positions
-----------------------

The *positions* property of an AbstractState indicates where the pieces |dash|
as defined for the AbstractGame by the shapes, icons or images associated with
a character |dash| are placed.

The notation for doing this is by providing a string of characters.
There are two options available.

FEN-like Notation
~~~~~~~~~~~~~~~~~

This notation is based on the Chess notation called "FEN" (see:
https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation)
in which the pieces' characters are separated by a combination of numbers, to
represent blank cells and/or ``/`` (forward slash) characters to mark the
start of the next row.

For example:

.. code:: python

   positions = "rnbqkbnr/pppppppp/8"

would represent the Black pieces in Chess, as well as the unoccupied row in
front of the pawns.

If there are more than nine adjacent blank cells in a row, as there might be in
a game of Go, then use multiple numbers, For example:

.. code:: python

   positions = "8B9/B98"

The FEN-like notation is converted internally by *protograf* into
`Line-and-Dot Notation`_.

Line-and-Dot Notation
~~~~~~~~~~~~~~~~~~~~~

This notation represents each row as separate line, and each blank cell
with a ``.`` (dot or full stop).

The best way to represent multi-line sets of characters is by starting
and ending with triple quotes |dash| ``"""``.

For example:

.. code:: python

   positions = """r.bqkb.r
   .ppppppp"""

would show the rows in a Chess game where Black has moved both Knights
and one Pawn.

If row is entirely blank, it can be shown with a single ``.``.


.. _abstractStateAnnotations:

AbstractState Annotations
-------------------------

<TBD>


.. _abstractStateExamples:

AbstractState Examples
----------------------
