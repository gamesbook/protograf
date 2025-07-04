=========================
Examples: Board Game Geek
=========================

.. _BGG-Examples:

.. |dash| unicode:: U+2014 .. EM DASH SIGN

These examples are meant to demonstrate the type of output you can expect
to create with **protograf**.  They are *not* meant to be exhaustive or
comprehensive!

Bear in mind that the images shown in these examples are lower-resolution
screenshots; the original PDFs that can be generated from the source scripts
will demonstrate full scalability.

.. _table-of-contents-exbgg:

Table of Contents
=================

- `Basic`_
- `Image-based`_
- `Images and QR`_


Basic
=====
`↑ <table-of-contents-exbgg_>`_

=========== ==================================================================
Title       *Basic BoardGameGeek Example*
----------- ------------------------------------------------------------------
Script      `cards_bgg_basic.py <https://github.com/gamesbook/protograf/blob/master/examples/bgg/cards_bgg_basic.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a set of cards |dash| one per game
            |dash| using the BoardGameGeek API (BGG API), accessed via the
            https://github.com/SukiCZ/boardgamegeek Python library.

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/bgg/bgg_cards_basic.png
               :width: 90%
=========== ==================================================================


Image-based
===========
`↑ <table-of-contents-exbgg_>`_

=========== ==================================================================
Title       *BoardGameGeek Example with Thumbnails and Custom Values*
----------- ------------------------------------------------------------------
Script      `cards_bgg_thumb.py <https://github.com/gamesbook/protograf/blob/master/examples/bgg/cards_bgg_thumb.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a set of cards |dash| one per game
            |dash| using the BoardGameGeek API (BGG API), accessed via the
            https://github.com/SukiCZ/boardgamegeek Python library.

            This example was inspired by https://www.myboardgamecollection.com/ -
            a simple way to create a PDF file with all your collection data!

            This example uses games' "thumbnails" sourced from the BGG API,
            and also makes use of the :ref:`Selection <the-selection-command>`
            command to change the color of the third panel, based on how well
            the game is rated.

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/bgg/bgg_cards_thumb.png
               :width: 90%
=========== ==================================================================


Images and QR
=============
`↑ <table-of-contents-exbgg_>`_

=========== ==================================================================
Title       *BoardGameGeek Example with Images and QRCodes*
----------- ------------------------------------------------------------------
Script      `cards_bgg_image.py <https://github.com/gamesbook/protograf/blob/master/examples/bgg/cards_bgg_image.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a set of cards |dash| one per game
            |dash| using the BoardGameGeek API (BGG API), accessed via the
            https://github.com/SukiCZ/boardgamegeek Python library.

            This example was inspired by https://www.myboardgamecollection.com/ -
            a simple way to create a PDF file with all your collection data!

            This example uses games' full-sized images sourced from the BGG API,
            which are "sliced" to show the middle-third of the image.

            It also makes use of the :ref:`QRCode command <qrcode-command>`
            to generate a QRCode based on a hyperlink for the games' URLs on
            the BGG website.

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/bgg/bgg_cards_image.png
               :width: 90%
=========== ==================================================================
