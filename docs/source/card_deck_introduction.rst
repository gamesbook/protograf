==================
Working with Cards
==================

.. |dash| unicode:: U+2014 .. EM DASH SIGN

This section assumes you are very familiar with the concepts, terms and
ideas for :doc:`protograf <index>` as presented in the
:doc:`Basic Concepts <basic_concepts>` , that you understand all of the
:doc:`Additional Concepts <additional_concepts>`
and that you've created some basic scripts of your own using the
:doc:`Core Shapes <core_shapes>`.

.. _table-of-contents-wwc:

- `Introduction`_
- `Key Concepts and Commands`_
- `Images, Icons and Fonts`_
- `Supporting Commands`_
- `A Simple Deck, Card & Data Example`_
- `Countersheet and Counter Commands`_
- `Other Card Deck Resources`_


.. NOTE::

    This section is a high-level overview; all the key details, along with
    supporting examples can be found in the :doc:`Card Decks <card_decks>`
    section.  Further useful information is in the
    :doc:`Cards: Images, Icons and Font <card_images>` section.


Introduction
============
`↑ <table-of-contents-wwc_>`_

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


Key Concepts and Commands
=========================
`↑ <table-of-contents-wwc_>`_

Unlike the case where you specify where to locate elements on a single page,
you can also use **protograf** to handle the flow of placing cards onto
multiple pages, based on the cards' size and the size of the paper chosen.

In your script, for one or more cards, you will set out the elements exactly
as you want them to appear |dash| in effect, the card becomes a "mini page".

There are two core commands needed; the ``Deck()`` and the ``Card()``; with
supporting commands including the ``Data()`` and ``Matrix()`` commands.

Deck Command
------------

A ``Deck()`` command is used to set up the framework for creating one or more
cards.

Using its properties, you can specify aspects such type, size and the expected
number of cards, as well as any spacing and color swathes between them, that
will be used to create "frames", or placeholders, for each of the cards in the
deck.

All of these properties have defaults; for example, the default card size is
that of a Poker card, and the default number of cards is 9 |dash| the number
that will fit onto one A4-sized page with default margins.

For full details on how to configure a ``Deck``, see the section on the
:ref:`Deck Command <the-deck-command>`.

Card Command
------------

A ``Card()`` command is used to specify the design for a card, or a range
of cards.

A card design typically uses shapes and text elements |dash| some of which
may have already been defined.

Patterns or designs can be used (or re-used) for single or multiple cards.

.. NOTE::

    **protograf** also considers items such tiles or counters to be "cards" as
    they are really just "shapes containing other shapes". See
    `Countersheet and Counter Commands`_.

For full details on how to work with a ``Card``, see the section on the
:ref:`Card Command <the-card-command>`.

Data Command
------------

In many cases, the ``Data()`` command will be needed in order to provide
settings for the properties of the elements appearing on a card.  The source
of this data can be from places such as: an Excel or CSV file; or a Google
sheet.  Data can also be stored directly in the script.

All such data is **column-based** data; the names of the columns will be cross-
referenced by the cards; and each data record (the "row of a spreadsheet")
effectively correponds to one card of your prototype deck.

The data will typically include text that needs to appear on cards, but could
also include names of colors used to draw shapes, or links to images that will
need to be shown on the card.

Data can also be sub-setted by using some simple filter options.

For full details on how to work with ``Data``, see the section on the
:ref:`Data Command <the-data-command>`.

Matrix Command
--------------

In some cases, the ``Matrix()`` command will be needed. This is an alternate
method of providing the settings for the properties of the elements appearing
on a card.

For full details, see the section on the
:ref:`Matrix Command <the-matrix-command>`.


Images, Icons and Fonts
=======================
`↑ <table-of-contents-wwc_>`_

<TBD>


Supporting Commands
===================
`↑ <table-of-contents-wwc_>`_

The following commands are helpful in terms of increased flexibilty and
reduced repetition when designing a deck of cards.

-  The ``group()`` function provides a "shortcut" way to reference a set of
   shapes that all need to be drawn together.
-  The ``T()`` (*Template*) command allows a reference to some data |dash|
   for example, the cell in the named column of a spreadsheet |dash| to
   be substituted by its actual value when the card gets created.
-  The ``T()`` command also supports using a reference to a
   :ref:`Python function <python-function>` which you have created, that
   can be used to generate one or more shapes to be drawn on the card,
   based on value(s) from that card's data record.
-  The ``S()`` (*Selection*) command causes a shape to be added to a card,
   or set of cards, for a matching condition.
-  The ``L()`` (*Lookup*)  command enables the current Card to retrieve data
   from a named column corresponding to another Card based on the value of a
   named column in the current Card (whew!).


A Simple Deck, Card & Data Example
==================================

This script shows a simple script that displays a few cards using some
of the commands discussed briefly above.

Note that the data for these cards is embedded in the script; it looks
similar to a CSV file, but each row of data is "wrapped" in square
brackets with a comma at the end: ``[...],``

.. code:: python

    from protograf import *
    Create()
    card_data = [
        ['ID', 'Name', 'Age'],
        [1, "Gimli", 140],
        [2, "Legolas", 656],
        [3, "Aragorn", 88],
        [4, "Frodo", 51],
        [5, "Pippin", 29],
        [6, "Merry", 37],
        [7, "Samwise", 39],
        [8, "Boromir", 41],
        [9, "RingWraith", 4300],
    ]
    Data(data_list=card_data)
    Deck()
    Card("all",
         circle(x=0.5, y=0.5, radius=0.5, label=T("{{ Age }}")))
    Card("all",
         text(text=T("{{ Name }}"), x=3.3, y=7, font_size=18))
    Save()


Countersheet and Counter Commands
=================================
`↑ <table-of-contents-wwc_>`_

The ``Countersheet()`` and ``Counter()`` commands are effectively "wrappers"
around,  respectively, the Deck and Card commands so that all of the properties
and  abilities of those commands can be used via these instead.

The only *real* difference is that the default size of a ``Counter`` is 1"
square (i.e. 2.54 cm x 2.54 cm) versus that of a ``Card`` |dash|
6.35 cm x 8.89 cm, or 2.5" x 3.5".  On Letter-sized paper, this will result
in a default of 70 counters. You can see this with a short script:

.. code:: python

    from protograf import *
    Create(filename="counters.pdf", paper="letter")
    CounterSheet()
    Save()


.. _other-card-resources:

Other Card Deck Resources
=========================
`↑ <table-of-contents-wwc_>`_

**protograf** is by no means the only tool for creating decks of cards.
Numerous other options exist, both free and commercial.  Some of the free /
open-source ones are listed below.

Note that inclusion of these links does **not** constitute a recommendation of
them or their use!

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
