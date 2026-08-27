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

The aim of AbstractBoard and AbstractGame is to allow diagrams for such games to
be readily created.

The AbstractBoard compound object allows for the details of the board and pieces
for such a game to be specified.   However, such an object is **not** designed
to be shown |dash| it can be thought of as the game being "still in the box".

The AbstractGame compound object will, when supplied with a given AbstractBoard,
allow for a position in the game |dash| from setup through to end state |dash|
to be visualised and, optionally, annotated.  A series of such AbstractGame
objects, all using the same AbstractBoard, could thus depict an entire game.

.. _abstractBoard:

AbstractBoard Object
====================

An AbstractBoard can be specifed either by referring to an existing abstract
game by name |dash| for example, Chess, Checkers, or Go |dash| or via specific
combination of rows and columns. Similarly, pieces can also be specified by the
type of game  |dash| for example, Chess, Checkers, or Go |dash| or completely
unique ones can be created using *protograf* shapes and/or images.

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


AbstractBoard Examples
----------------------


.. _abstractGame:

AbstractGame Object
===================

An AbstractGame object serves to enable the display of the board and its pieces
at a given point in an abstract game |dash| often referred to as the "game state".

AbstractGame Properties
-----------------------

The properties that can be set for an AbstractBoard are:

* *board*: an AbstractBoard object; this is a required setting and the
  AbstractGame object cannot be displayed without it
* *positions*: details of where an AbstractBoard's pieces go on the board;
  see below for details
* *moves*: a list of moves; see below for details
* *annotations*: a list of board annotations; see below for details

AbstractGame Examples
---------------------
