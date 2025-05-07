==============
Decks of Cards
==============

.. |dash| unicode:: U+2014 .. EM DASH SIGN

This section assumes you are very familiar with the concepts, terms and
ideas for :doc:`protograf <index>` as presented in the
:doc:`Basic Concepts <basic_concepts>` , that you understand all of the
:doc:`Additional Concepts <additional_concepts>`
and that you've created some basic scripts of your own using the
:doc:`Core Shapes <core_shapes>`.

.. _table-of-contents:

Table of Contents
=================

- `Introduction`_
- `Basic Concepts`_
- `The Deck Command`_

  - `Deck Example #1 Defaults`_
  - `Deck Example #2 Copies`_
- `The Card Command`_
- `The Data Command`_

  - `Data Sources`_
  - `Data Properties`_
  - `Data Example #1 CSV`_
  - `Data Example #2 Excel`_
  - `Data Example #3 Matrix`_
  - `Data Example #4 Images`_
  - `Data Example #5 Lists`_
  - `Data Example #6 BoardGameGeek API`_
- `The Matrix Command`_
- `Countersheet and Counter Commands`_
- `Supporting Commands`_

  - `group command`_
  - `T(emplate) command`_
  - `S(election) command`_
  - `L(ookup) command`_
- `Other Resources`_


Introduction
============
`↑ <table-of-contents_>`_

Cards are a common and widely used method of storing and displaying
small sets of related data.

Scientists have used index cards since the 17th century and, of course,
libraries have long-used card catalogues as a way to track information
about books. Businesses in the 20th century used Rolodexes and business
cards as means to track and exchange information about individuals. Early
computers used a form of index cards called "punch" cards to store their
data. Playing cards, of course, have been popular both in China and
Europe, coming into more widespread use somewhere in the 9th and 14th
centuries respectively.

The massive rise in popularity of a game like *Magic the Gathering*, from
the 1990s onwards, has inspired the much greater use of cards in all aspects of
the modern board gaming experience, with cards or tiles taking the predominant
role in many of them.


Basic Concepts
==============
`↑ <table-of-contents_>`_

Unlike some other designs, where you are specifying exactly where to locate
elements on a page, **protograf** is designed to handle the flow of placing
cards onto multiple pages, based on their size and the size of paper chosen.
Then, for a card, you will set out elements exactly as you want them to appear.

There are two core commands needed; the ``Card()`` and the ``Deck()``:

-  A ``Card()`` command is used to specify the design for a card, or range
   of cards, typically using elements that have already been defined.
   The patterns or designs can be set to appear on single or multiple cards.
-  A ``Deck()`` command is used to specify type, size and number of cards,
   as well as any spacing between them, that will be used to create "frames"
   for all of the cards in the deck and then lay them out on one or more pages.

.. NOTE::

    **protograf** also considers items such tiles or counters to be "cards" as
    they are really just "shapes containing other shapes". See the section
    on `Countersheet and Counter Commands`_

In many cases, the ``Data()`` command will be needed in order to provide
settings for the properties of the elements appearing on a card, from another
source; for example, an Excel or CSV file.  This will typically be text that
needs to appear, but could also include colors and links to images.

In some cases, the ``Matrix()`` command will be needed. This is an alternate
method of providing the settings for the properties of the elements appearing
on a card.

These commands, and the ones supporting them, are described in detail below.

For additional examples that illustrate some of these, see the
:doc:`card and deck examples <examples/cards>` section.

.. _the-deck-command:

The Deck Command
================
`↑ <table-of-contents_>`_

This command provides the overall "framework" for the cards that are defined
in the script.  It's primary purpose is to set the card size, and then
calculate how many cards appear on a page.  It manages the "flow" of cards as
they get drawn.

The following are key properties that will usually need to be set for a
``Deck``:

- **cards** - this is the number of cards appearing in the deck. It defaults
  to ``9``. Note that other commands such as ``Data()`` and ``Matrix()`` will
  alter this value
- **height** - this is the card height; it defaults to ``8.8`` cm
- **width** - this is the card width. It defaults to ``6.3`` cm

.. IMPORTANT::

  The ``Deck`` command is covered in detail, with examples of all of its
  properties, in `The Deck Command <deck_command.html>`_ section.


Deck Example #1 Defaults
------------------------

This example shows the definition of a simple deck for cards that are a
commonly-used size (with the default units of centimetres in place).
The card size means that there will be 9 rectangular cards on each
A4 page (in default portrait mode):

    .. code:: python

      Deck(cards=18)

Note that height (``8.8`` cm) and width (``6.3`` cm) are the default values
for rectangular cards.


Deck Example #2 Copies
----------------------

This example shows the definition of a deck of 27 cards that are a
default size and type (rectangular). This  means that there will be
9 cards on each A4 page (in default portrait mode):

    .. code:: python

      Deck(
        cards=27,
        copy="Copies",
        mask="{{ Race == 'Hobbit' }}")

For the **copy** property to work, it is expected that there is a column
with the label **Copies** available in the Deck's dataset (which is created
by `the Data Command`_); in this case, the number in that column will be
used to make that many copies of the card (unless it has a **mask**).

For the **mask** property to work, it is expected that there is a column
with the label **Race** available in the Deck's dataset (which is created
by `the Data Command`_); in this case, any card with data matching the
value ``Hobbit`` will be masked (ignored and not drawn).

If you need to match any of multiple *mask* conditions, use an **or**:

    .. code:: python

        mask="{{ Race == 'Hobbit' or Race == 'Dwarf' }}")

If you need to match all of multiple *mask* conditions, use an **and**:

    .. code:: python

        mask="{{ Race == 'Hobbit' and Age < 39 }}")

If you need multiple *mask* conditions, these can be combined using an
**and** or an **or**, with each grouped condition in round brackets:

    .. code:: python

        mask="{{(Race == 'Hobbit' and Age < 39) or (Race == 'Human' and Age < 80)}}")

The dataset that could be used with the above Deck is shown in
`Data Example #5`_.

The full code - including the data - for this example is available as
`cards_lotr.py <https://github.com/gamesbook/protograf/blob/master/examples/cards/cards_lotr.py>`_

.. _the-card-command:

The Card Command
================
`↑ <table-of-contents_>`_

This command is both simple and flexible. It allows for a complex design, with
many elements, to be added to any - or all - of the cards in a deck.

The **key concept** to note about a card is that its essentially a "small page".
Any x- and y-locations are defined relative to the lower left of the card
and **not** that of the page.

A Card is defined slightly differently from other shapes in **protograf**
in that the properties are not named.

The **first value** supplied to the ``Card()`` command must be one or more
sequence numbers of the relevant cards.  This value can be supplied either
as a *string*, or a *list* (numbers between square brackets ``[`` and ``]``).

.. NOTE::

   A Card's sequence number depends on how the data for the Deck is sourced;
   usually it will correspond to the order that it is read from the Excel or
   CSV file.

Examples of Card sequence numbers supplied as *strings*:

- ``"10"`` - a single number; card number 10
- ``"10-20"`` - a range of numbers; in this case the cards numbered 10 through
   to 20 inclusive
-  ``"5,10-20,23-27"`` - multiple ranges of numbers; in this card number 5,
   cards numbered 10 through to 20 and cards numbered 23 through to 27
- ``"*"`` - any and all cards (the term ``"all"`` can also be used)

Examples of Card sequence numbers supplied as a *list*:

- ``[10]`` -  a single number; card number 10
- ``[10,11,12,13,14,15]`` - a set of numbers; in this case the cards numbered
  10 through to 15 inclusive

The **second value**, and all further values, supplied to the ``Card()``
command must be a :doc:`core shape <core_shapes>` or a
:ref:`group <group-command>`.

There can be any number of ``Card()`` commands; and the same Card could be
targeted by multiple ``Card()`` commands, each affecting some aspect of its
appearance; as elsewhere in **protograf** the order of commands matter in
the sense that later commands will overwrite any elements created by earlier
ones.

Card Creation Example #1
------------------------

This example shows how different shapes can be assigned to cards:

    .. code:: python

        Deck(cards=9)

        line1 = line(
            x=0.8, y=7.1, x1=5.6, y1=8.4,
            stroke="red")
        rect1 = rectangle(
            x=0.7, y=7.0, width=5, height=1.5)
        text1 = text(
            text='proto',
            x=3.1, y=4.4, font_size=18)
        line_in_rect = group(rect1, line1)

        Card('*', text1)
        Card("1-3", rect1)
        Card([7,8,9], line_in_rect)

Here:

- *all* (the ``*``) cards get assigned the same text (in the card centre)
- cards 1, 2 and 3 are assigned a rectangle
- cards 7, 8 and 9 are assigned a group (assigned to ``line_in_rect``); this
  group contains a rectangle with a red, diagonal line - the line is
  superimposed on the rectangle because it appears after it in the group list
  (see below for how the `group <group-command_>`_ command works.)

.. _the-data-command:

The Data Command
================
`↑ <table-of-contents_>`_

This command allows for a dataset to be used as the source for values or
properties making up a Card. Because values now have "names" they can be
accessed and used in the `Supporting Commands`_ - this is usually the primary
reason to supply a data source in this way.

.. NOTE::

   A dataset that the script must use should be defined **before** a ``Deck``
   or ``Countersheet`` command is used; otherwise you will get this error:

   .. code::

     FEEDBACK:: Cannot use T() or S() command without Data already defined!


Data Sources
------------
`↑ <table-of-contents_>`_

There are six possible types of data sources to create a dataset:

1. A CSV file
2. An Excel file
3. A ``Matrix`` command
4. A directory (containing images)
5. A "list of lists" (included in the script)
6. The BoardGameGeek API (available as a list-of-lists)

Apart from the images directory, each data source is essentially a set of rows
and columns.  Each **row** represents data that must appear on a card.
Each **column** must be named so that the data can be referenced and used:

- the names for a CSV file must appear in the first line of the file
- the names for a Excel file must appear in the columns of the first row of
  the spreadsheet
- the names for `the Matrix Command`_ command must appear as a list assigned
  to the *labels* property of the command
- the names for a "list of lists" must appear in the first list in the lists

.. IMPORTANT::

    The names used must **only** consist of normal alphabetical characters
    |dash| upper- or lower-case |dash| and **not** other numbers, symbols,
    punctuation marks, spaces etc. except for an underscore (``_``).

The ``Data`` command uses different properties to access these different
types of sources:

- **filename** - the full path to the name (including extension) of the
  CSV or Excel file being used; if no directory is supplied in the path,
  then it is assumed to be the same one in which the script is located
- **matrix** - refers to the name assigned to the ``Matrix`` being used
- **images** - refers to the directory in which the images are located; if
  a full path is not given, its assumed to be directly under the one in which
  the script is located
- **images_list** - is used in conjunction with *images* to provide a list of
  file extensions which filter which type of files will be loaded from the
  directory e.g. ``.png`` or ``.jpg``; this is important to set if the
  directory contains files of a type that are not, or cannot be, used
- **data_list** refers to the name assigned to the "list of lists" being used

.. HINT::

   If you are a Python programmer, there is a final way to provide data.

   Internally, all of these data sources are converted to a list of
   *dictionarie*, whose keys all match and correspond to the column names,
   so if you have this available, through any means, it can be supplied
   directly to ``Data`` via a **source** property.  The onus is on *you*
   to ensure that the dictionary is correctly formatted.

Data Properties
---------------
`↑ <table-of-contents_>`_

The other property that can be used for the ``Data`` command is:

- **extra** - if additional cards need to be manually created for a Deck,
  that are *not* part of the data source, then the number of those cards
  can be specified here. See the
  :ref:`standard playing cards <standard-playing-cards>`
  example, where the primary cards are created through `the Matrix Command`_
  and the two Jokers are the "extras".

.. _deck-data-csv:

Data Example #1 CSV
-------------------
`↑ <table-of-contents_>`_

This example shows how data is sourced from a CSV file:

    .. code:: python

       Data(filename="card_data.csv")

.. _deck-data-excel:

Data Example #2 Excel
---------------------
`↑ <table-of-contents_>`_

This example shows how data is sourced from an Excel file:

    .. code:: python

       Data(filename="card_data.xls")

.. _deck-data-matrix:

Data Example #3 Matrix
----------------------
`↑ <table-of-contents_>`_

This example shows how data is sourced from a Matrix; in this case the data
represents possible combinations for a standard deck of playing cards:

    .. code:: python

        combos = Matrix(
            labels=['SUIT', 'VALUE'],
            data=[
                ['\xab', '\xa8', '\xaa', ' \xa9'],  # spade, club, heart, diamond
                ['K','Q','J','10','9','8','7','6','5','4','3','2','A'],
            ])
        Data(matrix=combos)

The dataset will contain a combination of every item in the first list of
*data* - representing the **SUIT** - with every item in the second list of
*data* - representing the **VALUE**; so 4 suits, multiplied by 13 values,
results in 52 dataset items.

For more detail on these properties see `The Matrix Command`_.

.. _deck-data-images:

Data Example #4 Images
----------------------
`↑ <table-of-contents_>`_

This example shows how data is sourced from an image directory:

    .. code:: python

       Data(
           images="pictures", images_filter=".png,.jpg")

.. _deck-data-lists:

Data Example #5 Lists
---------------------
`↑ <table-of-contents_>`_

This example shows how data is sourced from a "list of lists":

    .. code:: python

       lotr = [
           ['ID', 'Name', 'Age', 'Race', 'Copies'],
           [1, "Gimli", 140, "Dwarf", 1],
           [2, "Legolas", 656, "Elf", 1],
           [3, "Aragorn", 88, "Human", 1],
           [4, "Frodo", 51, "Hobbit", 1],
           [5, "Pippin", 29, "Hobbit", 1],
           [6, "Merry", 37, "Hobbit", 1],
           [7, "Samwise", 39, "Hobbit", 1],
           [8, "Boromir", 41, "Human", 1],
           [9, "Gandalf", None, "Maia", 1],
           [10, "RingWraith", 4300, "Nazgul", 9],
       ]
       Data(data_list=lotr)

This list above is equivalent to a CSV file containing:

    .. code:: text

        ID,Name,Age,Race,Copies
        1,Gimli,140,Dwarf,1
        2,Legolas,656,Elf,1
        3,Aragorn,88,Human,1
        4,Frodo,51,Hobbit,1
        5,Pippin,29,Hobbit,1
        6,Merry,37,Hobbit,1
        7,Samwise,39,Hobbit,1
        8,Boromir,41,Human,1
        9,Gandalf,,Maia,1
        10,RingWraith,4300,Nazgul,9

It can be seen that using ``None`` is the same as the missing item for
Gandalf's age.

See below under the `T(emplate) command`_ and also under the
`S(election) command`_ for examples how this data could be used.

.. _deck-data-bgg:

Data Example #6 BoardGameGeek API
---------------------------------
`↑ <table-of-contents_>`_

This example shows how data is loaded for boardgame details obtained from the
:ref:`BoardGameGeek API <the-bgg-command>`.

.. code:: python

    boardgames = BGG(ids=[1, 2, 3], progress=True)
    Data(data_list=boardgames.data_list)

Assuming access to the BoardGameGeek API works and returns the game data
required |dash| in this case games with ID's ``1``, ``2``, and ``3`` |dash|
which in turn, in this case, are assigned to the name ``boardgames``.

The ``data_list`` required for Data can be obtained from the stored set of
games  |dash| in this case ``boardgames`` |dash| by appending the term
``.data_list`` to it.

The game information can then be used as it would for other data sources.

A collection of games, linked to a BoardGameGeek user, can also be retrieved
by supplying their username, for example:

.. code:: python

    boardgames = BGG(user='BenKenobi1976', progress=True)
    Data(data_list=boardgames.data_list)


.. _the-matrix-command:

The Matrix Command
==================
`↑ <table-of-contents_>`_

The ``Matrix`` command uses these properties to create data:

- **data** - these are all relevant data that needs to appear on the acards;
  specified as a "list of lists"; where each nested list contains all data of
  a given type of value
- **labels** - there should be one label for each nested list i.e. per each
  type of value

This command will generate a dataset for the cards, based on all combinations
of values in a "list of lists"; so for this set of *data*:

.. code:: python

    data=[
        ['A', 'B', ],
        ['1', '2', ],
        ['x', 'y', ],
     ])

There are 8 combinations:  A-1-x, A-1-y, A-2-x, A-2-y, B-1-x, B-1-y, B-2-x,
and B-2-y and therefore eight cards in the deck.

See the `Data Example #3 Matrix`_ above for a full Matrix.

.. _the-countersheet-command:

Countersheet and Counter Commands
=================================
`↑ <table-of-contents_>`_

These commands are effectively "wrappers" around the Deck and Card commands
(respectively) so all of the properties and abilities of those commands can
be used via these instead.  The only real difference is that the default size
of a Counter is 1" square (2.54 cm x 2.54 cm).

The aim of having these commands is to allow the script to be more informative
as to its purpose and use.

For an excellent guide on how to create counters for a "traditional"
hex-and-counter wargame, see *"Creating Wargames Counters with Inkscape"*
at https://github.com/jzedwards/creating-wargames-counters-with-inkscape ;
although its "grammar" is specific to Inkscape, the principle and approach
can be adapted to **protograf**


Supporting Commands
===================
`↑ <table-of-contents_>`_

The following commands are helpful in terms of increased flexibilty and
reduced repetition when designing a deck of cards.

- `group command`_
- `T(emplate) command`_
- `S(election) command`_
- `L(ookup) command`_

.. _group-command:

group command
-------------
`↑ <table-of-contents_>`_

The ``group()`` command provides a "shortcut" way to reference a stack of shapes
that all need to be drawn together. Add the shapes to a set - comma-separated
names wrapped in curved brackets (``(..., ...)``) - and assign the set to a
name.  The shapes are drawn in the order listed.

For example:

    .. code:: python

      line1 = line(x=0.8, x1=5.6, y=7.1, y1=8.4)
      rect1 = rectangle(x=0.7, y=7.0, width=5, height=1.5)
      stack = group(rect1, line1)

When this group named *stack* is assigned to a card and then drawn,
the Rectangle will be drawn first, followed by the Line, following the
order in which the appear in the group's listing.

This command is somewhat similar to the
:ref:`Common command <the-common-command>`, which also provides a way to
group commonly used properties.

.. _the-template-command:

T(emplate) command
------------------
`↑ <table-of-contents_>`_

The ``T()`` command causes the name of a column to be replaced by its equivalent
value for that card.

To use this command, simply enclose the name of the data column in curly
brackets - ``"{{...}}"`` - remember that this **is** case-sensitive.

This example shows how to use the command, with reference to the ``Data``
from `Data Example #5 Lists`_.  The text appearing at the top of all cards
is derived from the **Name** column:

.. code:: python

    Card("all", text(text=T("{{ Name }}"), x=3.3, y=7.5, font_size=18))

Data from the column can also be mixed in with other text or values:

.. code:: python

    power = text(
        text=T("<i>Long-lived</i> <b>({{ Age or '\u221E' }})</b>"),
        x=0.5, y=1.2, width=5, font_size=18,
        align="centre", wrap=True, fill=None)

Here the Text assigned to the name *power* uses the full text capability to
style the text - italic and bold - and also uses the **or** option in the
``T()`` command to provide an alternate value - in this case the infinity
sign - to use when there no *Age* value (for example, for the "Gandalf" row).

The full code for this example is available as
`cards_lotr.py <https://github.com/gamesbook/protograf/blob/master/examples/cards/cards_lotr.py>`_

.. HINT::

    If the column name you use in the ``T()`` command does **not** appear in
    any the actual column names, you will get an error such as:

    .. code::

        FEEDBACK:: Unable to process data with this template ('Ag' is undefined)


.. _the-selection-command:

S(election) command
-------------------
`↑ <table-of-contents_>`_

The ``S()``  command causes a shape to be added to a card, or set of cards,
for a matching condition.

There are two properties required:

- the first is the **condition** that must matched, enclosed in curly brackets
  ``"{{...}}"``
- the second is the **shape** that will be drawn if the condition is matched

The match condition contains three parts, all separated by spaces:

- the *column* name being checked - this **is** case-sensitive
- the test *condition* being used; e.g.:

  - ``==`` for equal to;
  - ``!=`` for not equal to;
  - ``>`` for greater than;
  - ``<`` for less than;
  - ``in`` to check if text is contained in other text
- the *value* being checked - for example, a number or some text

This example shows how to use the command, with reference to the ``Data``
from `Data Example #5`_:

    .. code:: python

        back_race = Common(
            x=0.5, y=0.5, width=5.3, height=7.9, rounded=0.2)
        back_hum = rectangle(
            common=back_race, fill_stroke="tomato")
        Card("all", S("{{ Race == 'Human' }}", back_hum))

In this example, any/all cards for which the **Race** column is equal
to -  the double equals ``==`` check  - the value **Human**, a red
rectangle will be drawn on the card (the one named ``back_hum``).

A "nonsense" condition is usually ignored; for example:

    .. code:: python

        Card("all", S("{{ nature == 'Orc' }}", power))

will produce no changes in the cards as there is no **nature** column or
**Orc** value.

The full code for this example is available as
`cards_lotr.py <https://github.com/gamesbook/protograf/blob/master/examples/cards/cards_lotr.py>`_

.. _the-lookup-command:

L(ookup) command
----------------

The ``L()``  command enables the current Card to retrieve data from a named
column corresponding to another Card based on the value of a named column
in the current Card.

It takes three properties; the names of the three columns (remember that
these names **are** case-sensitive):

- the *first* column name is one that must contain a value for the current
  card;
- the *second* column name is one that is used to find a matching card whose
  column must contain a value that mtaches that of the one appearing in the
  the current Card
- the *third* column is the one that will return the value for the matched
  Card.

As an example, suppose a CSV file contains data for these two cards:

    .. code::

       ID, NAME, USES,   IMAGE
       1,  wire, copper, wire.png
       2,  plug, wire,   plug.png

This example shows how to retrieve the **IMAGE** for the *"wire"* card
when working with the second (*"plug"*) card:

    .. code:: python

        Card("2", image(source=L('USES', 'NAME', 'IMAGE')))

The program takes the value from the *plug*'s **USES** column; then finds
a Card whose **NAME** column contains a matching value - in this case, the
first card; and then returns the value from that card's **IMAGE** column - in
this case, the value **wire.png**.

.. _other-card-resources:

Other Resources
===============
`↑ <table-of-contents_>`_

**protograf** is by no means the only tool for creating decks of cards.
Numerous other options exist, both free and commercial.  Some of the free /
open-source ones are listed below.

Inclusion of these links does **not** constitute a recommendation of them or
their use!

================== ======= ========== =========================================================
Title              O/S     Language   Link
================== ======= ========== =========================================================
Batch Card Maker   Multi   Python     https://github.com/p-dimi/Batch-Card-Maker
Card Creatr Studio Multi   Electron   https://cardcreatr.sffc.xyz/
Card Editor        Windows Java       https://bitbucket.org/mattsinger/card-editor/src/release/
CardMaker          Multi   C#         https://github.com/nhmkdev/cardmaker
DeCard64           Windows Delphi     https://github.com/Dimon-II/DeCard64
Forge of Cards     Online  JavaScript https://forgeofcards.com/#/
NanDeck            Windows ?          https://www.nandeck.com/
Paperize           Online  JavaScript https://beta.editor.paperize.io/#/
Strange Eons       Multi   Java       https://strangeeons.cgjennings.ca/index.html
Squib              Multi   Ruby       https://squib.rocks/
================== ======= ========== =========================================================
