==============
Decks of Cards
==============

.. |dash| unicode:: U+2014 .. EM DASH SIGN

These examples are meant to demonstrate the type of output you can expect
to create with **protograf**.  They are *not* meant to be exhaustive or
fully comprehensive!

Bear in mind that the images shown in these examples are lower-resolution
screenshots; the original PDFs that can be generated from the source scripts
will demonstrate full scalability.

.. _table-of-contents-excards:

- `Simple`_
- `Matrix Generated`_
- `Standard Playing Cards`_
- `Image-only Cards`_
- `Hexagonal Cards`_
- `Circular Cards`_
- `Play Money`_
- `Access to an API`_

.. _simple-cards:

Simple
======
`↑ <table-of-contents-excards_>`_

=========== ==================================================================
Title       *Simple set of Cards*
----------- ------------------------------------------------------------------
Script      `cards_design.py <https://github.com/gamesbook/protograf/blob/master/examples/cards/cards_design.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a deck of cards using these
            commands (only an extract of the code is shown here):

              .. code:: python

                l1 = line(
                    x=0.8, x1=5.6, y=7.1, y1=8.4,
                    stroke="gold", stroke_width=2)
                r1 = rectangle(
                    x=0.7, y=7.0, width=5, height=1.5,
                    stroke_width=1, rounding=0.2)
                low = group(r1, l1)

                Card([1,2,3], low)
                Card("4-6", r1)
                Card("7,8,9", l1)

            This is a simple design of lines and rectangles. These are
            assigned names which can be used directly; or indirectly as part
            of a ``group``.

            The assignment as to which card (``Card``) can either be done via
            a string e.g. ``"4-6"`` or a list of numbers e.g. ``[1,2,3]``.

            To set changes for cards at intervals; for example, a set of even
            cards |dash| as defined by their sequence number |dash| or a set
            odd cards:

              .. code:: python

                # element added to every odd card in the range
                Card(steps(1,9,2), rectangle())
                # element added to every even card in the range
                Card(steps(2,10,2), circle())

            An alternate way to set changes for cards, specifically for odd
            and even cards:

              .. code:: python

                # element added to every odd card in the deck
                Card("odd", rectangle())
                # element added to every even card in the deck
                Card("even", circle())

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/cards/cards_simple.png
               :width: 90%
=========== ==================================================================

.. _matrix-generated-cards:

Matrix Generated
================
`↑ <table-of-contents-excards_>`_

=========== ==================================================================
Title       *Cards generated from a Matrix*
----------- ------------------------------------------------------------------
Script      `cards_matrix_one.py <https://github.com/gamesbook/protograf/blob/master/examples/cards/cards_matrix_one.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a deck of cards using these
            commands (only an extract of the code is shown here):

              .. code:: python

                combos = Matrix(
                    labels=['SUIT', 'VALUE', 'IMAGE'],
                    data=[
                        # tomato, lime, aqua, gold, hotpink
                        ['#FF6347', '#00FF00','#00FFFF', '#FFD700', '#FF69B4'],
                        ['5', '3', '1'],
                        # tapedrive, heart, snowflake
                        ['\U+2707', '\U+2766', '\U+2745']
                    ])
                Data(matrix=combos)

            The use of the ``Matrix`` command is helpful for a design that is
            a combination/permutation scenario.

            In this example each card will display a unique combination of a
            *SUIT* - these are hexadecimal colors in the first list that
            appears in ``data`` |dash| plus a *VALUE* |dash| these are the
            numbers in the second list appearing in ``data`` |dash| and also
            an *IMAGE* |dash| these are the Unicode symbols shown in the
            third list of ``data``.

            .. HINT::

                As can be seen, a Unicode symbol is shown by 4-characters
                prefixed by the ``\U+`` (For more, see
                :ref:`Unicode <unicode-characters>` character resources.)

                The Unicode symbols available are specific to the font
                being used.

            Once defined in the ``Matrix``, the results will be generated and
            stored via the ``Data`` command's **matrix** property.
----------- ------------------------------------------------------------------
Screenshot  .. image:: images/cards/cards_matrix.png
               :width: 90%
=========== ==================================================================

.. _standard-playing-cards:

Standard Playing Cards
======================
`↑ <table-of-contents-excards_>`_

=========== ==================================================================
Title       *Standard Playing Cards generated from a Matrix & Images*
----------- ------------------------------------------------------------------
Script      `cards_standard.py <https://github.com/gamesbook/protograf/blob/master/examples/cards/cards_standard.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a deck of cards using these
            commands (only an extract of the code is shown here).

            The bulk of the cards are generated via a ``Matrix`` (see the
            **Matrix** example above), also using Unicode symbols for the
            **SUIT** and a list of the standard card **VALUE** letters and
            numbers:

              .. code:: python

                combos = Matrix(
                    labels=['SUIT', 'VALUE'],
                    data=[
                        # spade, club, heart, diamond
                        ['\u2660', '\u2663', '\u2665', '\u2666'],
                        ['K','Q','J','10','9','8','7','6','5','4','3','2','A'],
                    ])
                Data(matrix=combos, extra=2)

            The **extra** property for the ``Data`` command allows the deck to
            consist of more more cards than those generated by the ``Matrix``;
            so, in this case, 4 suits multiplied by 13 values is 52 cards. The
            two Jokers are the 2 "extras" (card numbers 53 and 54).

            The Number cards consist of text and a colored suit - because
            the suit is created from a Unicode symbol it is also text; the
            locations of these are set via common properties; and the color
            is set via a **stroke** property.

            The Royalty cards require an image, whose settings are created via
            a ``Common`` command:

              .. code:: python

                royals = Common(x=1.5, y=1.8, width=3.5, height=5)
                Card("14", image("images/king_c.png", common=royals))
                Card("15", image("images/queen_c.png", common=royals))

            The Ace of Spades is often specially demarcated in a deck via a
            more elaborate design. In this case, the design is simply two
            large spades symbols, of different colors, superimposed:

              .. code:: python

                Card("13",
                     text(x=3.15, y=2.6, font_size=180, stroke="black",
                          text='\u2660'),
                     text(x=3.15, y=3.8, font_size=60, stroke="white",
                          text='\u2660'))

            The Jokers (not shown in the screenshot) are the **extra** 2
            cards needed for a standard deck. In this case they also require
            an image, as well as text whose properties are created via the
            same ``Common`` command used for number cards:

              .. code:: python

                jok_pic = Common(x=0.8, y=1.9, width=5, height=5)
                Card("53",
                     text(common=value_top, stroke="black", text='J'),
                     text(common=value_low, stroke="black", text='J'),
                     image("images/joker_black.png", common=jok_pic))

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/cards/cards_standard.png
               :width: 90%
=========== ==================================================================

.. _image-only-cards:

Image-Only Cards
================
`↑ <table-of-contents-excards_>`_

=========== ==================================================================
Title       *Cards generated from a directory of images*
----------- ------------------------------------------------------------------
Script      `cards_images.py <https://github.com/gamesbook/protograf/blob/master/examples/cards/cards_images.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a deck of cards using these
            commands (only an extract of the code is shown here):

              .. code:: python

                Data(images="pictures", images_filter=".png,.jpg")
                # add an image from Data to each card
                Card("*", image("*", x=0, y=0, width=6.3, height=8.8))

            The commands for generating cards that just consist of an image
            are simple.  the ``Data`` command's **images** property points to
            a directory containing all the images.

            It can be helpful to ensure that any non-image files stored in
            that images directory are ignored; for this purpose the
            **images_filter** property can be set to contain a comma-delimited
            list of allowable file extensions.

            The ``Card`` command sets all cards in the deck (via ``*``) to
            each use an image; but in thise case no ``Image`` name is set
            as this will be "filled in" with the names from the ``Data``.

            *Credits:* the original image that was "chopped up" to form the
            set of images used for these example cards was sourced from:
            https://picjumbo.com/mysterious-fantasy-forest-with-old-bridges/

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/cards/cards_images.png
               :width: 90%
=========== ==================================================================

.. _hexagonal-cards:

Hexagonal Cards
================
`↑ <table-of-contents-excards_>`_

=========== ==================================================================
Title       *Hexagonal-shaped Cards*
----------- ------------------------------------------------------------------
Script      `cards_hexagonal.py <https://github.com/gamesbook/protograf/blob/master/examples/cards/cards_hexagonal.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a deck of cards/tiles using
            these commands (only an extract of the code is shown here):

              .. code:: python

                Data(filename="lotr.csv")
                Deck(
                    cards=6,
                    shape='hexagon',
                    height=6.3,
                    copy='Copies')

            It can be seen that each alternate row is offset from the ones on
            either side of it; this is to make cutting such cards/tiles much
            easier.

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/cards/cards_hexagonal.png
               :width: 90%
=========== ==================================================================

.. _circular-cards:

Circular Cards
==============
`↑ <table-of-contents-excards_>`_

=========== ==================================================================
Title       *Circular-shaped Cards*
----------- ------------------------------------------------------------------
Script      `cards_circular.py <https://github.com/gamesbook/protograf/blob/master/examples/cards/cards_circular.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a deck of cards using these
            commands (only an extract of the code is shown here):

              .. code:: python

                Data(filename="lotr.csv")
                Deck(
                    cards=1,
                    shape='circle',
                    radius=3.15,
                    copy='Copies')

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/cards/cards_circular.png
               :width: 90%
=========== ==================================================================

.. _play-money:

Play Money
==========
`↑ <table-of-contents-excards_>`_

=========== ==================================================================
Title       *Play Money* (using Cards)
----------- ------------------------------------------------------------------
Script      `supreme.py <https://github.com/gamesbook/protograf/blob/master/examples/play_money/supreme.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a set of play money using
            ``Deck()`` and ``Card()`` commands.  This example was inspired by
            the money found in the game "Supremacy" (Supremacy Games, 1984).

            Of interest is the use of ``PolyLine()`` command to create the logo
            at the centre, with the ``Repeat()`` command used to create the set
            of lines that forms the background to the logo.

            The data used to set the various denomination values and their
            colors is "baked into" the script using the list-of-lists
            approach.

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/play_money/supreme.png
               :width: 95%
=========== ==================================================================


.. _access-api:

Access to an API
================
`↑ <table-of-contents-excards_>`_

=========== ==================================================================
Title       *Data Accessed from an API*
----------- ------------------------------------------------------------------
Script      `cards_api.py <https://github.com/gamesbook/protograf/blob/master/examples/cards/cards_api.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a deck of cards using data
            obtained from an API (only an extract of the code is shown here):

            .. code:: python

              import requests

                def get_api_data():
                    result = requests.get(
                        'https://restcountries.com/v3.1/all?'
                        'fields=name,area,population,fifa,continents')
                    data = result.json()
                    countries = []
                    for d in data:
                        countries.append(
                            {'name': d['name']['common'],
                             'area': d['area'],
                             'pop': d['population'],
                             'fifa': d['fifa'],
                             'continent': d['continents'][0]}
                        )
                    return countries

                Data(
                    source=get_api_data(),
                    filters=[('fifa', '', 'ne')])

            This example makes use of the following Python features:

            - ``def`` to create a new function
            - ``import`` to load another library
            - ``for`` to create a loop
            - ``append`` to add items to a list

            In this example, an API is called.  This is a web site that is
            able to provide a data set in a structured format.  The Python
            ``requests`` library makes this very straightforward to do.

            A loop allows each item of data in the data set to be accessed.
            Columns from each item can then be accessed using the ``[]``
            notation.  This allows the chosen columns to be added as a set
            of key/value of pairs using the ``{}`` notation to a list.

            The ``Data()`` command allows the new function, which creates
            the dataset in format usuable by **protograf**, to be accessed
            via the *source* property.

            Use of the *filters* property allows a subset of the data to be
            chosen for the Cards.

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/cards/countries_cards.png
               :width: 90%
=========== ==================================================================
