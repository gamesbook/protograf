=========================================
Examples: Commercial Board Games and Maps
=========================================

.. |dash| unicode:: U+2014 .. EM DASH SIGN

These examples are meant to demonstrate the type of output you can expect
to create with **protograf**.  They are *not* meant to be exhaustive or
comprehensive!

Bear in mind that the images shown in these examples are lower-resolution
screenshots; the original PDFs that can be generated from the source scripts
will demonstrate full scalability.

.. IMPORTANT::

    Note that there is *no* intention to infringe on copyright; these are
    partial examples designed to show possibilities and **not** to encourage
    copying or reproduction of any copyrighted game material.

.. _table-of-contents-excomm:

- `Squad Leader`_
- `Orion`_
- `Adventurer Conqueror King`_
- `Traveller: Draft`_
- `Traveller: Black`_
- `Warp War`_
- `Underwater Cities`_
- `The Honorverse`_


Squad Leader
============
`↑ <table-of-contents-excomm_>`_

=========== ==================================================================
Title       *Squad Leader Modular Board Section*
----------- ------------------------------------------------------------------
Script      `squad_leader.py <https://github.com/gamesbook/protograf/blob/master/examples/boards/commercial/squad_leader.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a board for a wargame - in
            this Avalon Hill's "Squad Leader" - using a hexagonal grid.

            The grid's properties, such as alphanumeric coordinates and hex
            column offsets are used for overall appearance; the use of a blank
            white rectangle enables the  "half-hex" effect at the lower edge
            of the board.
----------- ------------------------------------------------------------------
Screenshot  .. image:: images/boards/commercial/squadleader_blank.png
               :width: 90%
=========== ==================================================================


Orion
=====
`↑ <table-of-contents-excomm_>`_

=========== ==================================================================
Title       *Orion Game Board*
----------- ------------------------------------------------------------------
Script      `orion_game_board.py <https://github.com/gamesbook/protograf/blob/master/examples/boards/commercial/orion_game_board.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a board for the commercial
            board game "Orion".  It is a fairly simple script, as the board
            is similar to many abstract boards; a so-called "hexhex" shape.

            The background is just stacked ``Circle`` s of differing fill colors
            and the main board is a ``HexagonalGrid`` of ``circular`` shape.
            Of interest is that the "corner" hexagons are not displayed because
            they are listed as *masked*.
----------- ------------------------------------------------------------------
Screenshot  .. image:: images/boards/commercial/orion_game_board.png
               :width: 80%
=========== ==================================================================


Adventurer Conqueror King
=========================
`↑ <table-of-contents-excomm_>`_

=========== ==================================================================
Title       *Adventurer Conqueror King RPG Blank Map*
----------- ------------------------------------------------------------------
Script      `ack_map.py <https://github.com/gamesbook/protograf/blob/master/examples/boards/commercial/ack_map.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a blank map for the
            "Adventurer Conqueror King" roleplaying game.

            The map is constructed of two hexagonal grids; the larger hexes
            have fill set to ``None`` so that the small hexes are visible
            through it. The use of white rectangles enables the  "half-hex"
            effect at the lower edge of the board.
----------- ------------------------------------------------------------------
Screenshot  .. image:: images/boards/commercial/ack_map.png
               :width: 90%
=========== ==================================================================


Traveller: Draft
================
`↑ <table-of-contents-excomm_>`_

=========== ==================================================================
Title       *Traveller RPG Map*
----------- ------------------------------------------------------------------
Script      `traveller_draft.py <https://github.com/gamesbook/protograf/blob/master/examples/boards/commercial/traveller_draft.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a blank sector map for the
            "Traveller" science fiction roleplaying game.

            Its a simple hexagonal grid, with a numeric coordinate system.
            The "edges" are just drawn with lines.

            It might be possible, in future, to expand this to show how star
            systems could be depicted on it; something along the lines of the
            Warp War`_ example.
----------- ------------------------------------------------------------------
Screenshot  .. image:: images/boards/commercial/traveller_draft.png
               :width: 80%
=========== ==================================================================


Traveller: Black
================
`↑ <table-of-contents-excomm_>`_

=========== ==================================================================
Title       *Traveller RPG Map*
----------- ------------------------------------------------------------------
Script      `<https://github.com/gamesbook/protograf/blob/master/examples/boards/commercial/traveller_black.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a blank sector map for the
            "Traveller" scifi roleplaying game.

            Its a simple hexagonal grid, with a numeric coordinate system.
            The "edges" are just drawn with lines. The styling is black because
            of the fill used for the hexagons; when testing, however, it could
            be better to use a lighter color as this using much black is not
            very "printer friendly".

            It might be possible, in future, to expand this to show how star
            systems could be depicted on it; something along the lines of the
            `Warp War`_ example.
----------- ------------------------------------------------------------------
Screenshot  .. image:: images/boards/commercial/traveller_black.png
               :width: 80%
=========== ==================================================================


Warp War
========
`↑ <table-of-contents-excomm_>`_

=========== ==================================================================
Title       *Warp War Map*
----------- ------------------------------------------------------------------
Script      `warpwar.py <https://github.com/gamesbook/protograf/blob/master/examples/boards/commercial/warpwar.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a map for the "Warp War" game.

            The example based off an image created by Rick Smith and posted to
            the https://groups.io/g/warpwar/ forum on 3 June 2024.  This is
            *not* a complete copy of that map - it just serves to illustrate
            how elements of such a map could be created.

            This is a fairly complex layout as most items need to be placed
            with millimetre accuracy using the ``Location()`` command to detail
            which shapes go into which hexagon grid location.

            The green lines joining hexagons are created with the ``LinkLine()``
            command; by default this joins the centres of two locations in the
            hexagon grid; but use of the optional "move x" and "move y"
            settings allows the line endpoints to be adjusted within their
            respective hexagons.

            The use of hexagon ``borders`` enables the drawing of purple lines
            which represent the edges of a nebula; unfortunately, its quite
            tedious to define all of these one-by-one!

            The hexagon numbering for this game, which **protograf** terms
            ``diagonal`` is fairly unusual.  It also uses ``upper-multiple``
            for the *coord_type_y* property, as opposed to the more
            conventional spreadsheet alphanumeric style.

            The hexagon identifers across the top and side are created with a
            ``Sequence(`` command; they are not "built-in" to the grid.  Not
            many games seem to use these, or else they use them in a wide
            variety of ways, so there is currently no automated way of
            achieving this.

            .. HINT::

                The full map script can be found at
                `warpwar_full.py <https://github.com/gamesbook/protograf/blob/master/examples/boards/commercial/warpwar_full.py>`_
                but it uses various :ref:`Python Commands <table-of-contents-pyc>`
                in order to simplify the map generation; it may be of interest
                if you want to see how **protograf** can pull in such commands.

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/boards/commercial/warpwar.png
               :width: 95%
=========== ==================================================================


Underwater Cities
=================
`↑ <table-of-contents-excomm_>`_

=========== ==================================================================
Title       *Underwater Cities Game Board*
----------- ------------------------------------------------------------------
Script      `underwater_cities.py <https://github.com/gamesbook/protograf/blob/master/examples/boards/commercial/underwater_cities.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct the board for the commercial
            board game "Underwater Cities". This is *not* a complete copy of
            that board - it just serves to illustrate how elements of it could
            be created during the prototyping stage.

            The script for this example is one of the longest but it is not
            really that complex, as most shapes are simple rectangles stacked
            in the correct order, with the right fill and line color & styling.

            Some items of interest:

            - Extensive use of the ``Common()`` command to avoid duplication
              between similar items
            - Use of an SVG world map to create the background layer
            - Mix of custom images, free icons and **protograf** to create
              the smaller graphic elements, such as the locks and wreaths
            - Use of the ``RectangularLocation()`` command to lay out the
              primary scoring track; the ``Layout()`` command makes use of multiple
              repeating shapes for the color changes at different intervals
            - Use of ``Sequence()`` command to create the player order track,
              (in the middle) as well as the different rounds (the dark,
              vertical track on the right)
----------- ------------------------------------------------------------------
Screenshot  .. image:: images/boards/commercial/underwater_cities.png
               :width: 90%
=========== ==================================================================


The Honorverse
==============
`↑ <table-of-contents-excomm_>`_

=========== ==================================================================
Title       *The Honorverse Star Map*
----------- ------------------------------------------------------------------
Script      `honorverse.py <https://github.com/gamesbook/protograf/blob/master/examples/boards/maps/honorverse.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows a map with the locations of stars described in the
            "Honor Harrington" science fiction series, written by David Weber, and
            sometimes termed the `Honorverse <https://en.wikipedia.org/wiki/Honorverse>`_

            The backdrop to the series is that FTL travel is possible; both with
            spaceships travelling through hyperspace as well as through wormholes.
            However wormholes are very limited in number, and so the stars that have
            both habitable planets, as well as multiple wormhole junctions, become
            obvious focal points for development and expansion. The main character
            in the series is from such a star system called "Manticore"; the
            centre of a "kingdom" of planets loosely modelled after the British
            Empire in the nineteenth century.

            The data is sourced from:

            * https://www.gotshifted.com/honorverseglossary/MAPS.html
            * https://www.gotshifted.com/honorverseglossary/Book%20Originals.html

            Any errors in transcription are mine |dash| *NOT* the original
            sources!

            Some items of interest:

            * The "stars" are just point locations on the grid; a Python loop
              processes them and styles each according to its information; using
              ``if`` and ``else``, while the ZapfDingbats font provides icons
              used to show the star.
            * The names of stars allow their point locations to be "looked" up
              in the list, and the stars locations form the start and end points
              of lines showing the connecting wormholes.
            * The script has a boolean "toggle" (called ``DARK_MODE``) which can
              be set to change the background color of the map to black and
              the stars to white.

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/boards/maps/honorverse.png
               :width: 90%

----------- ------------------------------------------------------------------
"Zoomed"    .. image:: images/boards/maps/manticore.png
               :width: 90%

=========== ==================================================================
