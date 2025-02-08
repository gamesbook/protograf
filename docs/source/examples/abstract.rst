==============================
Examples: Abstract Board Games
==============================

These examples are meant to demonstrate the type of output you can expect
to create with **protograf**.  They are *not* meant to be exhaustive or
comprehensive!

Bear in mind that the images shown in these examples are lower-resolution
screenshots; the original PDFs that can be generated from the source scripts
will demonstrate full scalability.

.. |dash| unicode:: U+2014 .. EM DASH SIGN

.. _table-of-contents:

Table of Contents
=================

- `Chess`_
- `Backgammon`_
- `Go`_
- `Hex`_
- `HexHex Games`_
- `Octagons`_
- `TicTacToe`_

Chess
=====
`↑ <table-of-contents_>`_

=========== ==================================================================
Title       *Chess Board*
----------- ------------------------------------------------------------------
Source Code `chessboard.py <https://github.com/gamesbook/protograf/blob/master/examples/boards/abstract/chessboard.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a regular Chess board.

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/boards/abstract/chessboard.png
               :width: 90%
=========== ==================================================================

=========== ==================================================================
Title       *Chess Board - Brown*
----------- ------------------------------------------------------------------
Source Code `chessboard_brown.py <https://github.com/gamesbook/protograf/blob/master/examples/boards/abstract/chessboard_brown.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a regular Chess board with
            brown styling and grid references.

            This example uses a Square grid with alphanumeric locations.
            These locations are then referenced and drawn with a ``Location()``
            command.

            The grid notation along the board edges is created via
            ``Sequence()`` commands.

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/boards/abstract/chessboard_brown.png
               :width: 70%
=========== ==================================================================


Backgammon
==========
`↑ <table-of-contents_>`_

=========== ==================================================================
Title       *Backgammon Board*
----------- ------------------------------------------------------------------
Source Code `backgammon.py <https://github.com/gamesbook/protograf/blob/master/examples/boards/abstract/backgammon.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a regular Backgammon board.

            This uses Trapezoid shape with a very narrow *top* to represent a
            point; this can be copied across in a line using a ``Sequence()``
            command.

            There is one Sequence command for each section of the
            board |dash| top and bottom sections of each panel |dash| and each
            Sequence draws a pair of Trapezoid shapes multiple times.

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/boards/abstract/backgammon.png
               :width: 80%
=========== ==================================================================


Go
==
`↑ <table-of-contents_>`_

=========== ==================================================================
Title       *Go Board*
----------- ------------------------------------------------------------------
Source Code `go.py <https://github.com/gamesbook/protograf/blob/master/examples/boards/abstract/go.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a regular Go board.

            The script is fairly simple; the board itself is contructed from a
            ``Grid``, and relies on the default interval being ``1`` cm.

            The handicap points are constructed using a ``DotGrid``, with
            larger than default dot sizes. The DotGrid offset is from the
            *page* edge, not the margin!

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/boards/abstract/go.png
               :width: 80%
=========== ==================================================================


Hex
===
`↑ <table-of-contents_>`_

"Hex" is the title of a game invented by Piet Hein.

=========== ==================================================================
Title       *Hex Board*
----------- ------------------------------------------------------------------
Source Code `hex_game.py <https://github.com/gamesbook/protograf/blob/master/examples/boards/abstract/hex_game.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a Hex game board.

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/boards/abstract/hex_game.png
               :width: 90%
=========== ==================================================================


HexHex Games
============
`↑ <table-of-contents_>`_

There are many games that are played on "hexagonal" board i.e. a board that is
hexagonal in outline and is composed of many hexagons.

The number of hexagons on the side of such a board is used to identify the
board size, for example; *hexhex5* is a board with 5 smaller hexagons along
each side.

=========== ==================================================================
Title       *Plain HexHex Board*
----------- ------------------------------------------------------------------
Source Code `hexhex.py <https://github.com/gamesbook/protograf/blob/master/examples/boards/abstract/hexhex.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a regular HexHex board.

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/boards/abstract/hexhex.png
               :width: 66%
=========== ==================================================================

=========== ==================================================================
Title       *HexHex Board - Circular Spaces*
----------- ------------------------------------------------------------------
Source Code `hexhex_circles.py <https://github.com/gamesbook/protograf/blob/master/examples/boards/abstract/hexhex_circles.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a HexHex board, but with
            circles replacing the usual hexagons in the layout; these are
            placed at the centre of where that hexagon would normally
            be drawn.

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/boards/abstract/hexhex_circles.png
               :width: 66%
=========== ==================================================================

=========== ==================================================================
Title       *HexHex Board - Hexagonal Spaces*
----------- ------------------------------------------------------------------
Source Code `hexhex_hexagons.py <https://github.com/gamesbook/protograf/blob/master/examples/boards/abstract/hexhex_hexagons.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a HexHex board, but with
            smaller hexagons replacing the usual hexagons in the layout; these
            are placed at the centre of where that hexagon would normally
            be drawn.

            In addition, the centre space is masked.

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/boards/abstract/hexhex_hexagons.png
               :width: 66%
=========== ==================================================================


Octagons
========
`↑ <table-of-contents_>`_

In Octagons, players alternate taking turns. On their turn, a player can
either fill in one half of an octagon or two squares. The player who first
forms an unbroken connection between the edges of their colour wins.

=========== ==================================================================
Title       *Octagons Board*
----------- ------------------------------------------------------------------
Source Code `octagons.py <https://github.com/gamesbook/protograf/blob/master/examples/boards/abstract/octagons.py>`_
----------- ------------------------------------------------------------------
Discussion  The code uses a basic 8-sided ``Polygon()``, with the *perbis*
            property being set to construct either a horizontal or vertical
            line inside it.

            The ``Repeat()`` command is used to lay out either of these shapes
            into part of an 8x8 "grid"; choosing which rows or columns are
            used by means of the *down* or *across* properties; with some
            rows "indented" by means of the *offset_x* property.

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/boards/abstract/octagons.png
               :width: 90%
=========== ==================================================================


TicTacToe
=========
`↑ <table-of-contents_>`_

=========== ==================================================================
Title       *TicTacToe Board and Game*
----------- ------------------------------------------------------------------
Source Code `tictactoe.py <https://github.com/gamesbook/protograf/blob/master/examples/boards/abstract/tictactoe.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a board and then show a series
            of moves played out on that board.

            This example uses ``RectangularLocations()`` to create a virtual
            grid representing the centres of each space on the board.  One
            ``Layout()`` command then places green Squares representing board
            spaces on that grid ; another ``Layout()`` command then places
            a set of colored Circles, representing all pieces placed on the
            board up to that turn, using their grid-location as a reference.

            The example requires the use of Python lists to record the moves,
            showing for each player in which grid row and column their piece
            was placed:

              .. code:: python

                turns = [(me,1,1), (you,2,2), (me,1,3), (you,1,2)]

            The use of a loop allows the program to process the moves and
            create one page for the board state as it would be after all
            moves *up to that point* have been carried out:

              .. code:: python

                for number, turn in enumerate(turns):
                   # create board for all turns up to this one

            Finally, the ``Save()`` command specifies output to a GIF image,
            along with the framerate (interval between showing each new image).

              .. code:: python

                Save(output='gif',framerate=0.5)

            (*Hint:* normally, you will need to do a "refresh" of this page to
            see the GIF animation in action.)

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/boards/abstract/tictactoe.gif
               :width: 50%
=========== ==================================================================
