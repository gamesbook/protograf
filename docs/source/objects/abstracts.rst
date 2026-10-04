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

.. _abstractIndex:

- `Overview`_
- `AbstractGame Command`_
- `AbstractState Command`_
- `Abstract Resources`_

.. _abstractOver:

Overview
========
`↑ <abstractIndex_>`_

Abstract games are the ancestors of many modern games.  They continue to be
played and appreciated by gamers of all ages across many societies.
In addition, many new abstract games are still being designed and tested.

The aim of the ``AbstractGame`` and ``AbstractState`` commands is to allow
diagrams for such games to be readily created.

The ``AbstractGame`` command allows for the details of the board and pieces
for such a game to be specified and, optionally, annotated and/or labelled
via markers. However, an ``AbstractGame`` is **not** designed to be drawn
|dash| it can be thought of as the game being "still in the box".

The ``AbstractState`` command will, when supplied with a previously defined
``AbstractGame``, allow for a position in the game |dash| at any point from
the setup through to its end state |dash| to be shown in diagrammatic form
and also, optionally, annotated and/or labelled via markers.

A series of ``AbstractState`` commands, all using the same ``AbstractGame``
could, if so required, depict an entire game but this is not the primary
intended use of the ``AbstractState`` command.

.. NOTE::

  An AbstractState command does **not** have the concept of a game "move".
  Tracking and processing moves is beyond the scope of **protograf**.
  The *markers* property for the AbstractState can be used to show
  how a piece might move with, for example, the aid of a line or arrow.

.. _abstractgame-command:

AbstractGame Command
====================
`↑ <abstractIndex_>`_

The ``AbstractGame()`` command defines the parts of an abstract game; primarily
the type, and styling, of the board and pieces that it uses.

A board can be specifed either by referring to an existing abstract game by
name |dash| for example, Chess, Checkers (aka Draughts), Go or Shogi |dash|
or via a specific combination of rows and columns, plus type of grid.

Pieces can also be specified by the type of game that they are usually used
with |dash| for example, Chess, Checkers (aka Draughts), Go or Shogi. It is
also possible to create completely unique pieces either by using one or more
of *protograf* shapes and/or images of your choice.

- `AbstractGame Properties`_
- `AbstractGame Board`_
- `AbstractGame Pieces`_
- `AbstractGame Markers`_
- `AbstractGame Examples`_

.. _abstractGameProperties:

AbstractGame Properties
-----------------------
`^ <abstractgame-command_>`_

The key properties that can be set for an AbstractGame are:

* *name*: the name of a type of board; which can chosen from  one of:
  ``chess``, ``checkers``, ``go``; if omitted, the default is a ``grid``
* *pieces*: details of pieces that will be placed on the board; these
  pieces can:

  * each be chosen |dash| **independantly** of the board name |dash| from a
    pre-existing set: ``chess``, ``checkers`` (the default), ``go``,
    ``shogi``, ``shogi-int``; or
  * make use of the full set available from a pre-existing game by using
    *pieces_type* property (see below); or
  * be defined with a customised list of piece names and shapes; see below
    for `AbstractGame Pieces`_
* *cols*: if no game *name* has been set |dash| each game is already associated
  with a predefined number of columns |dash| then this is the number of cells,
  in the horizontal direction, for a regular grid; a default of  ``8`` is used
* *rows*: if no game *name* has been set |dash| each game is already associated
  with a predefined number of rows |dash| then this is the number of cells,
  in the vertical direction, for a regular grid; a default of  ``8`` is used

Other useful properties that can be set for an AbstractGame are:

* *fills*: a list of one or more :ref:`colors <basic-color>`  in which to draw
  alternating board spaces; the default is to draw all cells ``white`` (or
  the board's *fill* color); for Chess or Checker games, the squares are drawn
  in a snake-like pattern |dash| line properties can be set with the normal
  *stroke* and *stroke_width*
* *frame*: if ``True``, draw a frame around the board's gridlines; use the
  normal styling options for the frame; *frame_width*, *frame_stroke*,
  *frame_dotted*, and/or *frame_dashed* to customize it
* *pattern*: an on/off design showing which cells should be blank i.e. unused
* *intersections*: if ``True``, draw pieces on **grid intersections**, not
  grid spaces, and label the lines, not the spaces
* *label*: if ``True``, draw a labels around the board's edges; use the
  normal styling options for a label; *label_font*, *label_stroke* etc.
* *label_type*: the type of label, drawn on the board edges, which is
  used to identify a row or column; it can be  either *alpha-numeric*,
  or *AN* (the default), which is the labelling used for Chess boards;
  or *numeric*, or *NN*, which is the labelling used for Shogi boards
* *label_start*: the corner of the board at which the labelling starts; this
  can be: *bottom-left* (*BL*), *bottom-right* (*BR*), *top-left* (*TL*),
  or *top-right* (*TR*). Chess boards use the *bottom-left*, the default, while
  Shogi boards use the *top-right*.
* *label_offset*: how far away a label are drawn from the board edge(s); if not
  set, this is calculated from the label's font size
* *markers*: a list of AbstractGame markers; see below for details
* *pieces_type*: choose a predefined set of pieces from well-known abstract
  games; possible choices areL ``chess``, ``checkers``, ``go``, ``shogi`` or
  ``shog-int`` (International, or Westernised, Shogi)
* *pieces_resize*: a fractional value by which to resize the built-in piece
  shapes or images; this defaults to ``1`` |dash| note that this does **not**
  apply to custom-made shapes
* *width* and *height* refer to the overall board size on the page; if omitted,
  the board will be automatically sized to fit within the smallest available
  space inside of the page margins.  The size of cells on the board are based
  on these values, using the *rows* and *cols* values

.. NOTE::

    The default settings for an AbstractGame are:

    * *name*: ``grid``
    * *rows*: ``8`` (the same as Chess or Checkers board)
    * *cols*: ``8`` (the same as Chess or Checkers board)
    * *pieces*: ``checkers`` (simple black and white circles)

    Note also that the definitions of the board and pieces are **not** the
    determinants of where the pieces get placed; how many pieces there are,
    or what the rules are for their movement!


.. _abstractGameBoard:

AbstractGame Board
------------------
`^ <abstractgame-command_>`_

A basic AbstractGame board is just a square grid and, depending on the game,
will contain either an equal or unequal number of rows and columms.

Such a grid allows pieces to be placed either in the spaces between the lines
or on their intersection points |dash| **protograf** terms these locations
*cells*.


.. _abstractGameHexagonPattern:

AbstractGame Hexagon Pattern
-----------------------------
`^ <abstractgame-command_>`_

If a hexagonal grid for a game does not contain an equal number of
hexagons in every row of the board, then a pattern design, or layout,
can be defined, using a cell-and-dot notation defined for the *hex_pattern*
property.

This notation represents each row as separate line, with each regular, or
normal hexagon with a ``O`` (the letter "oh"), and each blank, or missing,
cell with a ``.`` (dot or full stop).

There should be as many lines in the pattern as are set in the *rows* value
for the AbstractGame.

The best way to represent multi-line list of characters such as this is by
starting and ending with triple quotes |dash| ``"""``.`

For example, for an AbstractGame with ``cols=5`` and ``rows=5`` a valid
*hex_pattern* could be:

.. code:: python

   hex_pattern = """
   . O O O .
    0 O O O .
   O O O O O
    0 O O O .
   . O O O .
   """

Note that empty lines and "whitespace" at the start and end of a line is
ignored; but each line **must** contain an equal number of characters |dash|
again, ignoring any whitespace |dash| corresponding to the *cols* value.

If a row on the board contains only normal cells, this can be shown with a
single ``O``.


.. _abstractGamePieces:

AbstractGame Pieces
-------------------
`^ <abstractgame-command_>`_

Built-in Pieces
~~~~~~~~~~~~~~~

There are a number of shapes of pieces from well-known games available within
 *protograf's* library.  They can be used as set or indiviually. If you have
 already chosen a "named" game, the default set of pieces corresponding to that
 game will automatically have been selected.


Custom Pieces
~~~~~~~~~~~~~

You can supply your own set of shapes to be used with a game.

Shapes can either be designed with *protograf's* built-in shapes, or with a
pre-create image.

.. NOTE::

    If you use an image for a shape, ensure that it is square to fit into a
    standard grid cell |dash| square or hexagon.


.. _abstractGameMarkers:

AbstractGame Markers
--------------------
`^ <abstractgame-command_>`_


.. _abstractGameExamples:


AbstractGame Examples
----------------------
`^ <abstractgame-command_>`_



.. _abstractstate-command:

AbstractState Command
=====================
`↑ <abstractIndex_>`_

The ``AbstractState()`` command will create a display of a board and its pieces
that have been defined in an :ref:`AbstractGame <abstractgame-command>`. This
display represents a given point in an abstract game |dash| a situation commonly
referred to as "the game state".

- `AbstractState Properties`_
- `AbstractState Positions`_
- `AbstractState Markers`_
- `AbstractState Examples`_


.. _AbstractStateProperties:

AbstractState Properties
------------------------
`^ <abstractstate-command_>`_

The properties that can be set for an AbstractState command are:

* *board*: an AbstractGame object; this is a required setting and the
  AbstractState object cannot be displayed without it
* *positions*: details of where an AbstractGame's pieces go on the board;
  see below for details
* *setup*: if set to ``True``, and the game is one whose initial position is
  stored in *protograf*, then the pieces will be assigned to the board to
  match that defined setup
* *markers*: a list of AbstractState markers; see below for details


.. _abstractStatePositions:

AbstractState Positions
-----------------------
`^ <abstractstate-command_>`_

The *positions* property of an AbstractState indicates where the pieces |dash|
as defined for the AbstractGame by the shapes, icons or images associated with
a character |dash| are placed.

The notation for doing this is by providing a string of characters.
There are two options available.

FEN-like Notation
~~~~~~~~~~~~~~~~~

This notation is based on the Chess notation called "FEN" (see:
https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation)
in which the characters, representing pieces, are separated by a combination
of numbers, to represent consecutive blank cells, and/or ``/`` (forward slash)
characters to mark the end of row.

For example:

.. code:: python

   positions = "rnbqkbnr/pppppppp/8"

would represent the Black pieces at the start of a Chess game, as well as the
unoccupied row in front of the pawns.

If there are more than nine adjacent blank cells in a row, as there might be in
a game of Go, then use multiple numbers, For example:

.. code:: python

   positions = "9B9/B99"

This represents a situation where the first row has 9 empty points, a Black
stone, and then 9 empty points; whereas the second row has a Black stone,
followed by 9 empty points, and then another 9 empty points.

The FEN-like notation is converted internally by *protograf* into
`Piece-and-Dot Notation`_.

Piece-and-Dot Notation
~~~~~~~~~~~~~~~~~~~~~~

This notation represents each row as separate line, and each blank cell
with a ``.`` (dot or full stop).

The best way to represent multi-line list of characters such as this is by
starting and ending with triple quotes |dash| ``"""``.

For example:

.. code:: python

   positions = """
   r.bqkb.r
   .ppppppp
   """

would show two rows near the start of a Chess game where Black has moved
both Knights and one Pawn.

Note that empty lines and "whitespace" at the start and end of a line is
ignored.

If a row on the board contains **no** pieces, this can be shown with a single
``.``.


.. _abstractStateMarkers:

AbstractState Markers
---------------------
`^ <abstractstate-command_>`_

<TBD>


.. _abstractStateExamples:

AbstractState Examples
----------------------
`^ <abstractstate-command_>`_


.. _abstract-resources:


Abstract Resources
==================
`↑ <abstractIndex_>`_

Chess
-----

The following are the SVG images, sourced from Wikipedia Commons, available
for use in constructing abstract games.  The pieces are referenced, using the
notation described above, via the letter in the last column of the table.

Uppercase letters are used for White pieces; lowercase letters for Black.

 .. |icon-king| image:: ../../../protograf/resources/abstracts/chess/Chess_klt45.svg
      :width: 35px
      :height: 35px
      :alt: King
 .. |icon-queen| image:: ../../../protograf/resources/abstracts/chess/Chess_qlt45.svg
      :width: 35px
      :height: 35px
      :alt: Queen
 .. |icon-bishop| image:: ../../../protograf/resources/abstracts/chess/Chess_blt45.svg
      :width: 35px
      :height: 35px
      :alt: Bishop
 .. |icon-knight| image:: ../../../protograf/resources/abstracts/chess/Chess_nlt45.svg
      :width: 35px
      :height: 35px
      :alt: Knight
 .. |icon-rook| image:: ../../../protograf/resources/abstracts/chess/Chess_rlt45.svg
      :width: 35px
      :height: 35px
      :alt: Rook
 .. |icon-pawn| image:: ../../../protograf/resources/abstracts/chess/Chess_plt45.svg
      :width: 35px
      :height: 35px
      :alt: Pawn


.. list-table:: Chess Pieces
   :widths: 60 20 30
   :header-rows: 1

   * - English Name
     - Image
     - protograf
   * - King
     - |icon-king|
     - ``K``
   * - Queen
     - |icon-queen|
     - ``Q``
   * - Bishop
     - |icon-bishop|
     - ``B``
   * - Knight
     - |icon-knight|
     - ``N``
   * - Rook
     - |icon-rook|
     - ``R``
   * - Pawn
     - |icon-pawn|
     - ``P``

Shogi
-----

The following are the SVG images, sourced from Wikipedia Commons, available
for use in constructing abstract games.  The pieces are referenced, using the
notation described above, via the letter in the last column of the table.

In Japanese the two opposing sides are called *Sente* ("earlier move") and
*Gote* ("later move"), but in English they are referred to as Black and White,
with Black being the first to play, with pieces shown as upright, on the
nearer/closer side of the board.

As in Chess, uppercase letters are used for White pieces; lowercase letters
for Black.

 .. |icon-osho| image:: ../../../protograf/resources/abstracts/shogi/Shogi_osho(svg).svg
       :width: 35px
       :height: 35px
       :alt:  ōshō (king - champion; general)
 .. |icon-gyokusho| image:: ../../../protograf/resources/abstracts/shogi/Shogi_gyokusho(svg).svg
       :width: 35px
       :height: 35px
       :alt:  gyokushō (king - challenger; jeweled general)
 .. |icon-hisha| image:: ../../../protograf/resources/abstracts/shogi/Shogi_hisha(svg).svg
       :width: 35px
       :height: 35px
       :alt:  hisha (rook; flying chariot)
 .. |icon-ryuo| image:: ../../../protograf/resources/abstracts/shogi/Shogi_ryuo(svg).svg
       :width: 35px
       :height: 35px
       :alt:  ryūō (promoted rook; dragon king)
 .. |icon-kakugyo| image:: ../../../protograf/resources/abstracts/shogi/Shogi_kakugyo(svg).svg
       :width: 35px
       :height: 35px
       :alt:  kakugyō (bishop; angle mover)
 .. |icon-ryuma| image:: ../../../protograf/resources/abstracts/shogi/Shogi_ryuma(svg).svg
       :width: 35px
       :height: 35px
       :alt:  ryūma / ryūme (promoted bishop; dragon horse)
 .. |icon-kinsho| image:: ../../../protograf/resources/abstracts/shogi/Shogi_kinsho(svg).svg
       :width: 35px
       :height: 35px
       :alt:  kinshō (gold general)
 .. |icon-ginsho| image:: ../../../protograf/resources/abstracts/shogi/Shogi_ginsho(svg).svg
       :width: 35px
       :height: 35px
       :alt:  ginshō (silver general)
 .. |icon-narigin| image:: ../../../protograf/resources/abstracts/shogi/Shogi_narigin(svg).svg
       :width: 35px
       :height: 35px
       :alt:  narigin (promoted silver general)
 .. |icon-keima| image:: ../../../protograf/resources/abstracts/shogi/Shogi_keima(svg).svg
       :width: 35px
       :height: 35px
       :alt:  keima (knight; horse)
 .. |icon-narikei| image:: ../../../protograf/resources/abstracts/shogi/Shogi_narikei(svg).svg
       :width: 35px
       :height: 35px
       :alt:  narikei (promoted knight; cassia)
 .. |icon-kyosha| image:: ../../../protograf/resources/abstracts/shogi/Shogi_kyosha(svg).svg
       :width: 35px
       :height: 35px
       :alt:  kyōsha (lance; chariot)
 .. |icon-narikyo| image:: ../../../protograf/resources/abstracts/shogi/Shogi_narikyo(svg).svg
       :width: 35px
       :height: 35px
       :alt:  narikyō (promoted lance; incense)
 .. |icon-fuhyo| image:: ../../../protograf/resources/abstracts/shogi/Shogi_fuhyo(svg).svg
       :width: 35px
       :height: 35px
       :alt:  fuhyō (pawn; foot soldier)
 .. |icon-tokin| image:: ../../../protograf/resources/abstracts/shogi/Shogi_tokin(svg).svg
       :width: 35px
       :height: 35px
       :alt:  tokin (promoted pawn; reaches gold)

.. list-table:: Shogi Pieces
   :widths: 30 10 20 20 10 10
   :header-rows: 1

   * - English Name
     - Image
     - Kanji
     - Meaning
     - Abbreviation
     - protograf
   * - King (champion)
     - |icon-osho|
     - ōshō
     - king general
     - K
     - ``K``
   * - King (challenger)
     - |icon-gyokusho|
     - gyokushō
     - jeweled general
     - K
     - ``J``
   * - Rook
     - |icon-hisha|
     - hisha
     - flying chariot
     - R
     - ``R``
   * - Promoted rook ("Dragon")
     - |icon-ryuo|
     - ryūō
     - dragon king
     - +R
     - ``D``
   * - Bishop
     - |icon-kakugyo|
     - kakugyō
     - angle mover
     - B
     - ``B``
   * - Promoted bishop ("Horse")
     - |icon-ryuma|
     - ryūma / ryūme
     - dragon horse
     - +B
     - ``H``
   * - Gold general ("Gold")
     - |icon-kinsho|
     - kinshō
     - gold general
     - G
     - ``G``
   * - Silver general ("Silver")
     - |icon-ginsho|
     - ginshō
     - silver general
     - S
     - ``S``
   * - Promoted silver
     - |icon-narigin|
     - narigin
     - promoted silver
     - +S
     - ``V``
   * - Knight
     - |icon-keima|
     - keima
     - horse
     - N
     - ``N``
   * - Promoted knight
     - |icon-narikei|
     - narikei
     - promoted cassia
     - +N
     - ``T``
   * - Lance
     - |icon-kyosha|
     - kyōsha
     - chariot
     - L
     - ``L``
   * - Promoted lance
     - |icon-narikyo|
     - narikyō
     - promoted incense
     - +L
     - ``A``
   * - Pawn
     - |icon-fuhyo|
     - fuhyō
     - foot soldier
     - P
     - ``P``
   * - Promoted pawn
     - |icon-tokin|
     - tokin
     - reaches gold
     - +P
     - ``W``
