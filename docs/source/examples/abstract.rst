====================
Abstract Board Games
====================

These examples are meant to demonstrate the type of output you are able
to create with **protograf**.  They are *not* meant to be exhaustive or
comprehensive!

Bear in mind that the images shown in these examples are lower-resolution
screenshots; the original PDFs that can be generated from the source scripts
will demonstrate full scalability.

.. |dash| unicode:: U+2014 .. EM DASH SIGN

.. _table-of-contents-exabs:

- `Chess`_
- `Backgammon`_
- `Dejarik`_
- `Go`_
- `Hex`_
- `HexHex Games`_
- `Morabaraba`_
- `Octagons`_
- `Snex`_
- `TicTacToe`_
- `Meridians`_

Chess
=====
`↑ <table-of-contents-exabs_>`_

=========== ==================================================================
Title       *Chess Board*
----------- ------------------------------------------------------------------
Script      `chessboard.py <https://github.com/gamesbook/protograf/blob/master/examples/boards/abstract/chessboard.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a regular Chess board.

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/boards/abstract/chessboard.png
               :width: 90%
=========== ==================================================================

=========== ==================================================================
Title       *Chess Board - Brown*
----------- ------------------------------------------------------------------
Script      `chessboard_brown.py <https://github.com/gamesbook/protograf/blob/master/examples/boards/abstract/chessboard_brown.py>`_
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
`↑ <table-of-contents-exabs_>`_

=========== ==================================================================
Title       *Backgammon Board*
----------- ------------------------------------------------------------------
Script      `backgammon.py <https://github.com/gamesbook/protograf/blob/master/examples/boards/abstract/backgammon.py>`_
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


Dejarik
=======
`↑ <table-of-contents-exabs_>`_

`Dejarik <https://en.wikipedia.org/wiki/Dejarik>`__ is a holographic, 
Chess-like game depicted in the "Star Wars" movies.

=========== ==================================================================
Title       *Dejarik Board*
----------- ------------------------------------------------------------------
Script      `dejarik.py <https://github.com/gamesbook/protograf/blob/master/examples/boards/abstract/dejarik.py>`_
----------- ------------------------------------------------------------------
Discussion  The code uses a basic ``Circle()``, with the *slices*
            property being used to construct the internal sectors that creates
            the "dartboard-like" effect of radiating spaces. The
            *centre_shapes* property adds more overlapping circles.

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/boards/abstract/dejarik.png
               :width: 90%
=========== ==================================================================


Go
==
`↑ <table-of-contents-exabs_>`_

=========== ==================================================================
Title       *Go Board*
----------- ------------------------------------------------------------------
Script      `go.py <https://github.com/gamesbook/protograf/blob/master/examples/boards/abstract/go.py>`_
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
`↑ <table-of-contents-exabs_>`_

`Hex <https://en.wikipedia.org/wiki/Hex_(board_game)>`__ is the title of a game 
invented by Piet Hein.

=========== ==================================================================
Title       *Hex Board*
----------- ------------------------------------------------------------------
Script      `hex_game.py <https://github.com/gamesbook/protograf/blob/master/examples/boards/abstract/hex_game.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a *Hex* game board.

            The primary board is drawn using the ``Hexagons`` command, which
            specifies rows, columns and the hex layout pattern |dash| in this
            case a *diamond*.   The background edges are drawn as *slices*
            within a ``Rhombus`` shape.

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/boards/abstract/hex_game.png
               :width: 90%
=========== ==================================================================


HexHex Games
============
`↑ <table-of-contents-exabs_>`_

There are many games that are played on "hexagonal" board i.e. a board that is
hexagonal in outline and is composed of many hexagons.

The number of hexagons on the side of such a board is used to identify the
board size, for example; *hexhex4* is a board with 4 smaller hexagons along
each side.

=========== ==================================================================
Title       *Plain HexHex Board*
----------- ------------------------------------------------------------------
Script      `hexhex.py <https://github.com/gamesbook/protograf/blob/master/examples/boards/abstract/hexhex.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a regular HexHex board.

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/boards/abstract/hexhex.png
               :width: 66%
=========== ==================================================================

=========== ==================================================================
Title       *HexHex Board - Circular Spaces*
----------- ------------------------------------------------------------------
Script      `hexhex_circles.py <https://github.com/gamesbook/protograf/blob/master/examples/boards/abstract/hexhex_circles.py>`_
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
Script      `hexhex_hexagons.py <https://github.com/gamesbook/protograf/blob/master/examples/boards/abstract/hexhex_hexagons.py>`_
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


Morabaraba
==========
`↑ <table-of-contents-exabs_>`_

=========== ==================================================================
Title       *Morabaraba Board*
----------- ------------------------------------------------------------------
Script      `morabaraba.py <https://github.com/gamesbook/protograf/blob/master/examples/boards/abstract/morabaraba.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a Morabaraba board.

            There is just a simple set of Rectangles, with corners connected by
            Lines.

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/boards/abstract/morabaraba.png
               :width: 66%
=========== ==================================================================


Octagons
========
`↑ <table-of-contents-exabs_>`_

In Octagons, players alternate taking turns. On their turn, a player can
either fill in one half of an octagon or two squares. The player who first
forms an unbroken connection between the edges of their colour wins.

=========== ==================================================================
Title       *Octagons Board*
----------- ------------------------------------------------------------------
Script      `octagons.py <https://github.com/gamesbook/protograf/blob/master/examples/boards/abstract/octagons.py>`_
----------- ------------------------------------------------------------------
Discussion  The code uses a basic 8-sided ``Polygon()``, with the *perbii*
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


Snex
====
`↑ <table-of-contents-exabs_>`_

=========== ==================================================================
Title       *Snex Board and Game*
----------- ------------------------------------------------------------------
Script      `snex.py <https://github.com/gamesbook/protograf/blob/master/examples/boards/abstract/snex.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a board and then show a series
            of moves played out on that board.

            This example uses a number of different commands:

            - ``RectangularLocations()`` creates a virtual grid representing
              possible locations on a square board;
            - The ``Grid()`` command constructs the lines of the board;
            - The ``Layout()`` command places a set of ``Image`` s,
              representing all pieces placed on the board up to that turn,
              using their grid-locations as a reference;
            - The ``Star()`` command places a yellow-colored star at the
              grid-location corresponding to that of the most recently placed
              piece.

            The example requires the use of a Python list to store the moves,
            showing for each side on which grid row/column intersection their
            piece was placed.  Here ``blk`` corresponds to the black-colored
            pieces of the Black player, and ``wht`` corresponds to the
            white-colored pieces of the White player.

              .. code:: python

                turns = [
                    (blk,7,6), (wht,4,2), (blk,3,4), (wht,7,3), (blk,2,2),
                    (wht,3,6), (blk,5,5), (wht,6,6), (blk,6,5), (wht,4,4),
                ]

            The use of a `for` loop allows the program to process the moves
            and create a page for the board state as it would be after **all**
            moves *up to that point* have been carried out:

              .. code:: python

                for number, turn in enumerate(turns):
                   # create board for all turns up to this one

            Finally, the ``Save()`` command specifies output to a GIF image,
            along with the framerate (interval in seconds between showing each
            new image) and the image DPI resolution (a higher value creates
            larger images).

              .. code:: python

                Save(output='gif', dpi=150, framerate=1)

            The GIF will always "loop" |dash| starting the animation again
            once all frames have been shown.

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/boards/abstract/snex.gif
               :width: 50%
=========== ==================================================================


TicTacToe
=========
`↑ <table-of-contents-exabs_>`_

=========== ==================================================================
Title       *TicTacToe Board and Game*
----------- ------------------------------------------------------------------
Script      `tictactoe.py <https://github.com/gamesbook/protograf/blob/master/examples/boards/abstract/tictactoe.py>`_
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
            along with the framerate (interval in seconds between showing
            each new image).

              .. code:: python

                Save(output='gif', framerate=0.5)

            The GIF will always "loop" |dash| starting the animation again
            once all images have been shown.

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/boards/abstract/tictactoe.gif
               :width: 50%
=========== ==================================================================


Meridians
=========
`↑ <table-of-contents-exabs_>`_

In *Meridians*, players alternate taking turns to place stones and capture
the opponent's pieces.

=========== ==================================================================
Title       *Meridians Board*
----------- ------------------------------------------------------------------
Script      `meridians.py <https://github.com/gamesbook/protograf/blob/master/examples/boards/abstract/meridians.py>`_
----------- ------------------------------------------------------------------
Discussion  The code uses a basic ``Hexagon()``, with the *hatches_count*
            property being set to construct the internal lines to create
            the effect of triangular spaces.

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/boards/abstract/meridians.png
               :width: 90%
=========== ==================================================================
