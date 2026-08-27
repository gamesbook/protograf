==============================
AbstractBoard and AbstractGame
==============================

.. |dash| unicode:: U+2014 .. EM DASH SIGN

The AbstractBoard and AbstractGame are one of a number of what are termed
:doc:`Compound Objects <../objects>`.

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

Abstract games are the ancestors of many modern games.  They continue to be very
much played and appreciated by gamers of all ages across many societies.
In addition, many new abstract games are still being designed and tested.

The aim of the ``AbstractBoard`` and ``AbstractGame`` commands is to allow
diagrams for such games to be readily created.

The AbstractBoard command allows for the details of the board and pieces
for such a game to be specified.   However, such an object is **not** designed
to be shown |dash| it can be thought of as the game being "still in the box".

The AbstractGame command will, when supplied with a previously defined
AbstractBoard, allow for a position in the game |dash| from setup through
to end state |dash| to be visualised and, optionally, annotated.  A series
of such AbstractGame objects, all using the same AbstractBoard, could thus
depict an entire game.

.. _abstractBoard:

AbstractBoard Object
====================

An AbstractBoard can be specifed either by referring to an existing abstract
game by name |dash| for example, Chess, Checkers (aka Draughts), or Go |dash|
or via a specific combination of rows and columns.

Similarly, pieces can also be specified by the type of game that they are
usually used with |dash| for example, Chess, Checkers (aka Draughts), or
Go.

It is also possible to create completely unique pieces by using one or
more of *protograf* shapes and/or images.

..NOTE::

    The default settings for an AbstractBoard are:
    * *name*: ``grid``
    * *rows*: ``8`` (the same as Chess or Checkers board)
    * *cols*: ``8`` (the same as Chess or Checkers board)
    * *pieces*: ``checkers`` (simple black and white circles)

.. _abstractBoardProperties:

AbstractBoard Properties
------------------------

The properties that can be set for an AbstractBoard are:

* *name*: the name of a type of board; which can chosen from
  one of: `chess`, `checkers` (the default), `go`; if omitted, no
  type is pre-defined
* *pieces*: details of pieces that will be placed on the board; the piece set
  can |dash| **independantly of the board name |dash| be chosen from a
  prexisting set `chess`, `checkers` (the default), `go` or defined in a
  list - see below for Piece Definitions
* *colors*: a list of one or more Colors in which to draw alternating
  board spaces; the default is to draw all squares ``white``
* *hairs*: if True, draw small lines extending outwards from board gridlines;
  these lines are one-quarter of the length of a board cell, for example, if
  the board had squares of 1", the hairs would be one-quarter inch long
* *labels*: if True, draw labels along board edges, using notation appropriate
  to type of board
* *grid_align*: if True, draw pieces on grid intersections, not grid spaces
* *pieces_resize*: a fractional value by which to resize the built-in piece
  shapes or images; this defaults to ``1`` |dash| note that this does **not**
  apply to custom-made shapes
* *cols*: if no game name (which has a predefined number of columns) is
  set, this is the number of cells in the horizontal direction for a
  regular grid; this value defaults to 8 if not set
* *rows*: if no game name (which has a predefined number of rows) is
  set, this is the number of cells in the vertical direction for a
  regular grid; this value defaults to 8 if not set
* *width* and *height* refer to the overall board size; if omitted, the board
  will be automatically sized to fit within the smallest available space inside
  of the page margins.  The size of cells on the board are based on these values,
  using the required *rows* and *cols:

.. _abstractBoardPieces:

AbstractBoard Pieces
--------------------


AbstractBoard Examples
----------------------


.. _abstractGame:

AbstractGame Object
===================

An AbstractGame object serves to enable the display of the board and its pieces
at a given point in an abstract game |dash| often referred to as the "game state".

.. _abstractGameProperties:

AbstractGame Properties
-----------------------

The properties that can be set for an AbstractBoard are:

* *board*: an AbstractBoard object; this is a required setting and the
  AbstractGame object cannot be displayed without it
* *positions*: details of where an AbstractBoard's pieces go on the board;
  see below for details
* *moves*: a list of moves; see below for details
* *annotations*: a list of board annotations; see below for details

.. _abstractGamePositions:

AbstractGame Positions
----------------------

The *positions* property of an AbstractGame indicates where the pieces |dash|
as defined for the AbstractBoard by the shapes, icons or images associated with
a character |dash| are placed.

The notation for doing this is by providing a string of characters.
There are two options available.

FEN-like Notation
~~~~~~~~~~~~~~~~~

This notation is based on the Chess notation called "FEN" (ref: wikipedia ???)
in which the pieces' characters are separated by a combination of numbers, to
represent blank cells and/or ``/`` (forward slash) to mark the start of the
next row.

For example:

.. code:: python

   positions = "rnbqkbnr/pppppppp/8"

would represent the Black pieces in Chess, as well as the unoccupied row in
front of the pawns.

If there are more than nine adjacent blank cells in a row, as there might be in
a game of Go, then use multiple numbers, For example:

.. code:: python

   positions = ""8B9/B98"

The FEN-like notation is converted internally by *protograf* into
`Line-and-Dot Notation`_.

Line-and-Dot Notation
~~~~~~~~~~~~~~~~~~~~~

This notation represents each row as separate line, and each blank cell
with a ``.`` (dot or full stop).

The best way to represent multi-line sets of characters is by starting
and ending with triple quotes |dash| `"""`.

For example:

.. code:: python

   positions = """r.bqkb.r
   .ppppppp"""

would show the rows where Black has moved both Knights and one Pawn.


.. _abstractGameMoves:

AbstractBoard Moves
-------------------

<TBD>


.. _abstractGameAnnotations:

AbstractBoard Annotations
-------------------------

<TBD>

AbstractGame Examples
---------------------
