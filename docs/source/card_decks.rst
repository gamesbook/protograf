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

.. _table-of-contents-crddk:

Table of Contents
=================

- `Introduction`_
- `Basic Concepts`_
- `The Deck Command`_

  - `Deck Example 1. Defaults`_
  - `Deck Example 2. Copy & Mask`_
- `The Card Command`_
- `The CardBack Command`_
- `The Data Command`_

  - `Data Sources`_
  - `Data Properties`_
  - `Data Example 1. CSV`_
  - `Data Example 2. Excel`_
  - `Data Example 3. Matrix`_
  - `Data Example 4. Images`_
  - `Data Example 5. Lists`_
  - `Data Example 6. Google Sheets`_
  - `Data Example 7. BoardGameGeek API`_
- `The Matrix Command`_
- `Countersheet and Counter Commands`_
- `Supporting Commands`_

  - `group function`_
  - `T(emplate) command`_
  - `S(election) command`_
  - `L(ookup) command`_
- `Other Resources`_


Introduction
============
`↑ <table-of-contents-crddk_>`_

Cards are a common and widely used method of storing and displaying
small sets of related data.

Scientists have used index cards since the 17th century and, of course,
libraries have long-used card catalogues as a way to track information
about books. Businesses in the 20th century used Rolodexes and business
cards as means to track and exchange information about individuals. Early
computers used perforated cards called "punch" cards to store their
data. In gaming, playing cards have been popular both in China and
Europe, coming into more widespread use somewhere in the 9th and 14th
centuries respectively.

The massive rise in popularity of a game like
`Magic the Gathering <https://en.wikipedia.org/wiki/Magic:_The_Gathering>`_,
from the early 1990s onwards, has inspired the much greater use of cards in
all aspects of the modern board gaming experience, with cards or tiles
taking the predominant role in many of them.


Basic Concepts
==============
`↑ <table-of-contents-crddk_>`_

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
settings for the properties of the elements appearing on a card from another
source; for example, an Excel or CSV file.  This will typically be text that
needs to appear, but could also include colors and links to images.

In some cases, the ``Matrix()`` command will be needed. This is an alternate
method of providing the settings for the properties of the elements appearing
on a card.

These commands, and the ones supporting them, are described in detail below.

For additional examples that illustrate the use of some of these commands,
see the :doc:`card and deck examples <examples/cards>` section.

.. _the-deck-command:

The Deck Command
================
`↑ <table-of-contents-crddk_>`_

This command provides the overall "framework" for the cards that are defined
in the script.  It's primary purpose is to set the card size, and then
calculate how many cards appear on a page.  It manages the "flow" of cards as
they get drawn.

The following are key properties that will usually need to be set for a
``Deck``:

- **cards** - this is the number of cards appearing in the deck. It defaults
  to ``9``. (**Note** that other commands such as ``Data()`` and ``Matrix()``
  will alter this value.)
- **height** - this is the card height; it defaults to 8.89 cm / 3.5"
- **width** - this is the card width. It defaults to 6.35 cm / 2.5"

.. IMPORTANT::

  The ``Deck`` command is covered in detail, with examples of all of its
  properties, in `The Deck Command <deck_command.html>`_ section.


Deck Example 1. Defaults
------------------------
`↑ <table-of-contents-crddk_>`_

This example shows the definition of a simple deck for cards that are a
commonly-used size (with the default units of centimetres in place).
The card size means that there will be 9 rectangular cards on each
of two A4, portait-mode, pages:

    .. code:: python

      Deck(cards=18)

Note that these rectangular cards have a default height (``8.89`` cm) and
width (``6.35`` cm).

The **actual** number of cards may be changed by `the Data Command`_ or
`the Matrix Command`.


Deck Example 2. Copy & Mask
---------------------------
`↑ <table-of-contents-crddk_>`_

This example shows the definition of a deck of 27 cards that are a
default size and type (rectangular). This  means that there will be
9 cards on each A4 page:

    .. code:: python

      Deck(
        cards=27,
        copy="Copies",
        mask="{{ Race == 'Hobbit' }}")

For the **copy** property to work, it is expected that there is a column
with the label **Copies** available in the Deck's dataset (which is created
by `the Data Command`_); in this case, the number in that column will be
used to make that many copies of the card (unless it has a **mask**).
id
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
`Data Example 5. Lists`_.

The full code - including the data - for this example is available as
`cards_lotr.py <https://github.com/gamesbook/protograf/blob/master/examples/cards/cards_lotr.py>`_


.. _the-card-command:

The Card Command
================
`↑ <table-of-contents-crddk_>`_

This command is both simple and flexible. It allows for a complex design, with
many elements, to be added to any |dash| or all |dash| of the cards in a deck.

The **key concept** to note about a card is that its essentially a "small page".
Any x- and y-locations are therefore defined relative to the card
and **not** to the page.

A Card is defined slightly differently from other shapes in **protograf**
in that the properties are not named.

The **first value** supplied to the ``Card()`` command must be one or more
sequence numbers of the relevant cards.  This value can be supplied either
as a *string*, or a *list* (numbers between square brackets ``[`` and ``]``).

.. NOTE::

   A Card's sequence number depends on how the data for the Deck is sourced;
   usually it will correspond to the order that it is read from an Excel or
   CSV file.

Examples of Card sequence numbers supplied as *strings*:

- ``"10"`` - a single number; card number 10
- ``"10-20"`` - a range of numbers; in this case the cards numbered 10 through
  to 20 inclusive
- ``"5,10-20,23-27"`` - multiple ranges of numbers; in this card number 5,
  cards numbered 10 through to 20 and cards numbered 23 through to 27
- ``"*"`` - means any and all cards (the term ``"all"`` can also be used)

Examples of Card sequence numbers supplied as a *list*:

- ``[10]`` -  a single number; card number 10
- ``[10,11,12,13,15]`` - a set of numbers; in this case the cards numbered
  10 through to 15, but not number 14

The **second value**, and **all further values**, supplied to the ``Card()``
command must be a :doc:`core shape <core_shapes>` or a
:ref:`group <group-function>`.

There can be any number of ``Card()`` commands; and the same output card could
be targeted by multiple ``Card()`` commands, each affecting some aspect of its
appearance; as elsewhere in **protograf** the order of commands matter in
the sense that later commands may overwrite any elements created by earlier
ones.

Card Creation Example 1.
------------------------

This example shows how different shapes can be assigned to cards:

    .. code:: python

        Deck(cards=9)

        text1 = text(
            text='proto',
            x=3.1, y=4.4, font_size=18)
        rect1 = rectangle(
            x=0.7, y=7.0, width=5, height=1.5)
        line1 = line(
            x=0.8, y=7.1, x1=5.6, y1=8.4,
            stroke="red")

        line_in_rect = group(rect1, line1)

        Card('*', text1)
        Card("1-3", rect1)
        Card([7,8,9], line_in_rect)

Here:

- *all* (the ``*``) cards get assigned the same text (in the card centre)
- cards 1, 2 and 3 are assigned a rectangle
- cards 7, 8 and 9 are assigned a *group* (named ``line_in_rect``); this
  group consists of a rectangle (``rect1``) overdrawn by a red, diagonal line
  (``line1``). The line is superimposed on the rectangle because it appears
  after it in the group list (see below for how the
  `group <group-function_>`_ function works.)


.. _the-cardback-command:

The CardBack Command
====================
`↑ <table-of-contents-crddk_>`_

This command mirrors its counterpart |dash| :ref:`Card Command <the-card-command>`.

Any element or option that is applicable to that command can be used; for
example; adding shapes or setting ranges.

There are a few differences.  Any numeric range for a CardBack cannot exceed
the number of cards |dash| so if there were 9 Cards in the Deck, you cannot
set a range of ``"1-10"`` for a CardBack.

The default location for CardBacks to be drawn is on alternating pages on the
assumption that cards will be printed back-to-back and that there are matchiing
card backs for every front.  The offsets for CardBack positions are changed so
that the images line-up "behind" the Cards drawn on the front.

Both front and back can be drawn on the same page by using a **gutter**. For
details on this property, see the `Deck Command <deck_command.html>`_.


.. _the-data-command:

The Data Command
================
`↑ <table-of-contents-crddk_>`_

This command allows for a dataset |dash| for example, a CSV file or an Excel
spreadsheet |dash| to be used as the source for values or properties of
commands making the cards.

.. IMPORTANT::

   The number of cards that are listd in the dataset |dash| CSV file; Excel
   spreadsheetl; ect. |dash| will **always** take priority over the number
   of cards specified in  `The Deck Command <deck_command.html>`.

Because values now have "names" they can be
referenced and used by the `Supporting Commands`_ - this is usually the primary
reason to supply a data source in this way.

.. NOTE::

   A dataset that the script must use should be defined **before** a ``Deck``
   or ``Countersheet`` command is used; otherwise you will get this error:

   .. code::

     FEEDBACK:: Cannot use T() or S() command without Data already defined!


Data Sources
------------
`↑ <table-of-contents-crddk_>`_

There are six possible types of data sources to create a dataset:

1. A CSV file
2. An Excel file
3. A ``Matrix`` command
4. A directory (containing images)
5. A "list of lists" (included in the script)
6. A Google Sheet
7. The :ref:`BoardGameGeek API <the-bgg-command>` (available as a list-of-lists)

Apart from the images directory, each data source is essentially a set of rows
and columns.  Each **row** represents data that must appear on a card.
Each **column** must be named so that the data can be referenced and used,
in some way, for a card:

- the names for a CSV file must appear in the first line of the file
- the names for a Excel file, or Google Sheet, must appear in the columns of
  the first row of the spreadsheet
- the names for `the Matrix Command`_ must appear as a list assigned
  to the *labels* property of the command
- the names for a "list of lists" must appear in the first list in the lists

.. IMPORTANT::

    The names used must **only** consist of normal alphabetical characters
    |dash| upper- or lower-case |dash| and **not** other numbers, symbols,
    punctuation marks, spaces etc. except for an underscore (``_``).

The ``Data`` command uses different property names to refer to these
different types of data sources:

- **filename** - the full path to the name (including extension) of the
  CSV or Excel file being used; if no directory is supplied in the path,
  then it is assumed to be the same one in which the script is located
- **sheet** - refers to the ID of the Google Sheet being accessed (see
  the example below for more details)
- **matrix** - refers to the name assigned to the ``Matrix`` being used
- **images** - refers to the directory in which the images are located; if
  a full path is not given, its assumed to be directly under the one in which
  the script is located
- **images_list** - is used in conjunction with *images* to provide a list of
  file extensions which filter which type of files will be loaded from the
  directory e.g. ``.png`` or ``.jpg``; this is important to set if the
  directory contains files of a type that are not, or cannot be, used
- **data_list** refers to the name assigned to the "list of lists" being used;
  this property is also used when linked to data being sources from the
  :ref:`BoardGameGeek API <the-bgg-command>`

.. HINT::

   If you are a Python programmer, there is a final way to provide data.

   Internally, all of these data sources are converted to a list of
   *dictionaries*, whose keys all match and correspond to the column names,
   so if you have this available, through any means, it can be supplied
   directly to ``Data`` via a **source** property.  The onus is on *you*
   to ensure that the dictionary is correctly formatted.

Data Properties
---------------
`↑ <table-of-contents-crddk_>`_

The other property that can be used for the ``Data`` command is:

- **extra** - if additional cards need to be manually created for a Deck,
  that are *not* part of the data source, then the number of those cards
  can be specified here. See the
  :ref:`standard playing cards <standard-playing-cards>`
  example, where the primary cards are created through `the Matrix Command`_
  and the two Jokers are the "extras".

.. _deck-data-csv:

Data Example 1. CSV
-------------------
`↑ <table-of-contents-crddk_>`_

This example shows how data is sourced from a CSV file:

    .. code:: python

       Data(filename="card_data.csv")

.. _deck-data-excel:

Data Example 2. Excel
---------------------
`↑ <table-of-contents-crddk_>`_

This example shows how data is sourced from an Excel file:

    .. code:: python

       Data(filename="card_data.xls")

.. _deck-data-matrix:

Data Example 3. Matrix
----------------------
`↑ <table-of-contents-crddk_>`_

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

Data Example 4. Images
----------------------
`↑ <table-of-contents-crddk_>`_

This example shows how data is sourced from an image directory:

    .. code:: python

       Data(
           images="pictures", images_filter=".png,.jpg")

Here the script will look for all images with a ``png`` or ``jpg`` extension,
located in the ``pictures`` subdirectory.

.. _deck-data-lists:

Data Example 5. Lists
---------------------
`↑ <table-of-contents-crddk_>`_

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

It can be seen that using ``None`` in the "list of lists" is equivalent
to missing item in the CSV file (for Gandalf's age).

See below under the `T(emplate) command`_ and also under the
`S(election) command`_ for examples how this data could be used.


Data Example 6. Google Sheets
-----------------------------
`↑ <table-of-contents-crddk_>`_

There are three properties needed to gain access to data from a Google Sheet:

- *google_key* - an API Key that you can request from Google
- *google_sheet* - the unique ID (a mix of numbers and letters) which is randomly
  assigned by Google to your Google Sheet
- *google_name* - the name of the tab in the Google Sheet housing your data

The API Key
+++++++++++

Getting a Google API Key is beyond the scope of this document; one method is
provided by Google https://support.google.com/googleapi/answer/6158862?hl=en
but be aware that such documentation may quickly get out of date.

The end result of the process should provide you a key like this:
``A1_izC00Lbut2001askHAL4aPodd00rsys3rr0r``

You may also need to follow the ``+ Enable APIs and services`` on the Google
Cloud Dashboard (https://console.cloud.google.com/apis/dashboard) and then
select/enable the Google Sheets API from the list of services.

The Sheet ID
++++++++++++

A Google Sheet is only accessible by you when first created. To make it
allow **protograf** code access to the data, you **must** share the
Google Sheet publicly.

Navigate to your Google Sheet and click on the ``Share`` button. Then ensure
that you choose ``Anyone with the link`` and set the access to ``View``.

Click on the ``Copy link`` and save this in a document; the result should look like:

https://docs.google.com/spreadsheets/d/1vRfwxVjafnZVmgjazQKr2UQDyGYYK8GXJhQAPlzJ03o/edit

The string of characters between the ``/d/`` and the ``/edit`` is the **sheet ID**.

The Sheet Name
++++++++++++++

The name of the sheet you want to access is displayed in the bottom section of
display on a tab.  The default name of the first sheet is ``Sheet1``.


This next example shows how data is sourced from a Google Sheet, once you have
all the information described above:

    .. code:: python

        Data(
            google_sheet="1vRfwxVjafnZVmgjazQKr2UQDyGYYK8GXJhQAPlzJ03o",
            google_key="A1_izC00Lbut2001askHAL4aPodd00rsys3rr0r",
            google_name="Characters")

If the sheet cannot be reached, or access permissions are not correct,
or the API key is invalid, then you will get an error.

Solving access errors to a Google Sheet is beyond the scope of **protograf**
and its developers!

.. NOTE::

    There are limits to how many requests you can make to Google; please
    be aware of what your usage rights and limits are!


.. _deck-data-bgg:

Data Example 7. BoardGameGeek API
---------------------------------
`↑ <table-of-contents-crddk_>`_

This example shows how data is loaded for boardgame details obtained from the
:ref:`BoardGameGeek API <the-bgg-command>`.

.. code:: python

    boardgames = BGG(ids=[1, 2, 3], progress=True)
    Data(data_list=boardgames.data_list)

If access to the BoardGameGeek API works, then it returns the game data
|dash| in this case games with ID's ``1``, ``2``, and ``3`` |dash|
and these data are assigned to the name ``boardgames``.

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
`↑ <table-of-contents-crddk_>`_

The ``Matrix`` command uses these properties to create data:

- **data** - these are all relevant data that needs to appear on the cards;
  specified as a "list of lists"; where each nested list contains all data of
  a specific type of value
- **labels** - a list with one label for each of the other nested lists

This command will generate a dataset for the cards, based on all combinations
of values in a "list of lists"; so for this Matrix' set of *data*:

.. code:: python

    Matrix(
        labels=['INITIAL', 'NUMBER', 'LETTER'],
        data=[
            ['A', 'B', ],
            ['1', '2', ],
            ['x', 'y', ],
         ])

There are 8 possible *data* combinations:  A-1-x, A-1-y, A-2-x, A-2-y,
B-1-x,  B-1-y, B-2-x, and B-2-y and therefore eight cards in the deck.

See the `Data Example 3. Matrix`_ above for a full Matrix.

.. _the-countersheet-command:

Countersheet and Counter Commands
=================================
`↑ <table-of-contents-crddk_>`_

These commands are effectively "wrappers" around the Deck and Card commands
(respectively) so all of the properties and abilities of those commands can
be used via these instead.  The only real difference is that the default size
of a Counter is 1" square (2.54 cm x 2.54 cm).

The aim of having these commands is to allow the script to be more informative
as to its purpose and use.

.. HINT::

    For an excellent guide on how to create counters for a "traditional"
    hex-and-counter wargame, see *"Creating Wargames Counters with Inkscape"*
    at https://github.com/jzedwards/creating-wargames-counters-with-inkscape ;
    although its "grammar" is specific to Inkscape, the principle and approach
    can be adapted to **protograf**


Supporting Commands
===================
`↑ <table-of-contents-crddk_>`_

The following commands are helpful in terms of increased flexibilty and
reduced repetition when designing a deck of cards.

- `group function`_
- `T(emplate) command`_
- `S(election) command`_
- `L(ookup) command`_

.. _group-function:

group function
--------------
`↑ <table-of-contents-crddk_>`_

The ``group()`` function provides a "shortcut" way to reference a set of
shapes that all need to be drawn together.

Add the shapes to a set i.e. comma-separated names wrapped in curved
brackets |dash| ``(..., ...)`` |dash| and assign the set to a name.

The shapes are drawn in the order listed in the set (**not** the order
in which they appear in the script!).

For example:

    .. code:: python

      line1 = line(x=0.8, x1=5.6, y=7.1, y1=8.4)
      rect1 = rectangle(x=0.7, y=7.0, width=5, height=1.5)
      stack = group(rect1, line1)

When this group named *stack* is assigned to a card and then drawn,
the Rectangle will be drawn first, followed by the Line, following the
order in which these appear in the group's set.

This approach is somewhat similar to the
:ref:`Common command <the-common-command>`, which provides a way to
group commonly used *properties*, except that for that command, the
order of items does not matter.

.. _the-template-command:

T(emplate) command
------------------
`↑ <table-of-contents-crddk_>`_

The ``T()`` command causes the name of a :ref:`Data() <the-data-command>`
column to be replaced by its equivalent value for that card.

To use this command, simply enclose the name of the data column in curly
brackets - ``"{{...}}"``. Remember that this name **is** case-sensitive.

This example shows how to use the command, with reference to the ``Data``
from `Data Example 5. Lists`_.

The text, which will appear at the bottom of all of the cards,
is derived from the *Name* column:

.. code:: python

    Card("all", text(text=T('{{Name}}', x=3.3, y=7.5, font_size=18))

Data from the column can also be mixed in with other text or values,
for example:

.. code:: python

    power = text(
        text=T("""
           <p style="text-align:center; font-family:Helvetica">
           <i>Long-lived</i> <b>({{ Age or '\u221E' }})</b>
           </p>"""),
        x=1.4, y=0.7,
        height=1, width=3.5,
        html=True, fill=None)

Here the *text* incoporating the value of the *Age* column uses the
capabilities supported via ``html=True`` to style the text - italic and bold.

The **or** option is used inside of the ``T()`` command ``{{ }}`` to provide
an alternate value |dash| in this case the infinity sign |dash| for use when
there is no *Age* value (for example, for the "Gandalf" row).

The full code for this example is available as
`cards_lotr.py <https://github.com/gamesbook/protograf/blob/master/examples/cards/cards_lotr.py>`_

.. HINT::

    If the column name you use in the ``T()`` command does **not** appear in
    any the actual column names, you will get an error such as:

    .. code::

        FEEDBACK:: Unable to process data with this template ('Ag' is undefined)

Template functions
~~~~~~~~~~~~~~~~~~

It could that you need to perform a more complex operation, or validation,
on the data returned by the template from the :ref:`Data() <the-data-command>`.

In this case, you can write a :ref:`Python function <python-function>` which
can be used to generate one or more shapes to be drawn on the card.

The function should accept one incoming value; this incoming data for this
value will be that created by the ``T()`` command.

The function should **return** one or more shapes; anything else will trigger
this error::

    FEEDBACK:: Check that all elements created by 'icon_list' are shapes.

The name of the function is then passed to the ``T()`` command by that
command's *function* property.

Template Function Example 1.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this example, the function is called ``greet``, and is assigned and used
by the ``T()`` command as follows:

.. code:: python

    def greet(data):
        greeting = 'Hi ' + data
        return text(greeting, x=1, y=1)

    greetings = T('{{Name}}', function=greet)
    Card("*", greetings)

Here the value extracted from the ``Name`` column of your data file is
provided to the function you have called ``greet`` and assigned to it's
``data`` property.

The function simply creates a new text value called ``greeting`` and uses
that in a Text() shape which is then returned by the function.

The Text() shape is then assigned, via ``greetings`` to one more cards in
the usual way.

Template Function Example 2.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is a more complex example involving deeper knowledge of
:doc:`Python Commands <python_commands>`; please skip it if the terminology
or grammar makes no sense!

If you had a data value containing a list of image names (say they are
separated by commas) that need to be drawn in a line on the card, then
you will need a function that will *split* those
names and create a list of Image() shapes laid out in a line.

The approach could be:

.. code:: python

    def make_images(data):
        all_icons = split(data)  # create a list of individual icons
        icon_list = []  # create a place (a list) to store Images
        start = 0  # set distance away from start
        for icon in all_icons:  # step through icon list
            icon_image = image(icon, x=0.5 + start, y=2)  # create Image
            icon_list.append(icon_image)  # add image to the list
            start = start + 0.5  # increase distance for next icon
        return icon_list

    icons = T('{{Icons}}', function=make_images)
    Card("*", icons)

The key point here is that the ``make_images`` function generates a list of
shapes that are provided for use in the script by the **return**.


.. _the-selection-command:

S(election) command
-------------------
`↑ <table-of-contents-crddk_>`_

The ``S()`` command causes a shape to be added to a card, or set of cards,
for a matching condition.

There are two properties required:

1. the first is the **condition** that must matched, enclosed in curly brackets
   ``"{{...}}"``
2. the second is the **shape** that will be drawn if the condition is matched

The match **condition** contains three parts, all separated by spaces:

1. the *column* name being checked |dash| this **is** case-sensitive
2. the test *comparison* being used, e.g.:

   - ``==`` for equal to;
   - ``!=`` for not equal to;
   - ``>`` for greater than;
   - ``<`` for less than;
   - ``in`` to check if text is contained in other text (see example below)
3. the *value* being checked - for example, a number or some text |dash| this
   **is** also case-sensitive

This example shows how to use the command, with reference to the ``Data``
from `Data Example 5. Lists`_:

.. code:: python

    back_race = Common(
        x=0.5, y=0.5, width=5.3, height=7.9, rounded=0.2)
    back_hum = rectangle(
        common=back_race, fill_stroke="tomato")
    Card("all", S("{{ Race == 'Human' }}", back_hum))

In this example, for any/all cards for which the **Race** column is equal
to |dash| the double equals (``==``) comparison |dash| the value **Human**,
a red rectangle, named ``back_hum``, will be drawn on that card(s).

**Note** that the ``in`` check can be used in reverse. So:

.. code:: python

    back_race = Common(
        x=0.5, y=0.5, width=5.3, height=7.9, rounded=0.2)
    back_hum = rectangle(
        common=back_race, fill_stroke="tomato")
    Card("all", S("{{ 'H' in Race }}", back_hum))

Here any/all cards for which the **Race** column contains a capital "H"
will have a red rectangle, named ``back_hum``, drawn on them.

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

It takes three properties which correspond to the names of the three columns
(remember that these names **are** case-sensitive):

- the *first* column name is one that must contain a value for the current
  card;
- the *second* column name is one that is used to find a matching card whose
  column must contain a value that matches that of the one appearing in the
  current Card
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
a Card whose **NAME** column contains a matching value |dash| in this case,
the card with **ID** of ``1``; and then returns the value from that card's
**IMAGE** column |dash| in this case, the value **wire.png**.

.. _other-card-resources:

Other Resources
===============
`↑ <table-of-contents-crddk_>`_

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
CardFoldr          Multi   JavaScript https://foosel.github.io/cardfoldr/
CardMaker          Multi   C#         https://github.com/nhmkdev/cardmaker
DeCard64           Windows Delphi     https://github.com/Dimon-II/DeCard64
Forge of Cards     Online  JavaScript https://forgeofcards.com/#/
NanDeck            Windows ?          https://www.nandeck.com/
Paperize           Online  JavaScript https://beta.editor.paperize.io/#/
Strange Eons       Multi   Java       https://strangeeons.cgjennings.ca/index.html
Squib              Multi   Ruby       https://github.com/andymeneely/squib
================== ======= ========== =========================================================
