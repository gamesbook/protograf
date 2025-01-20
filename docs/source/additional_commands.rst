===================
Additional Commands
===================

This section deals with some of the additional commands available in
:doc:`protograf <index>` that are not covered elsewhere. You should
already be familiar with all of the :doc:`Basic Concepts <basic_concepts>`,
and have looked through the section on :doc:`Core Shapes <core_shapes>`.

.. _table-of-contents:

Table of Contents
=================

-  `BGG Command`_
-  `Font Command`_
-  `Today Command`_

.. _the-bgg-command:

BGG Command
===========
`↑ <table-of-contents_>`_

**To Be Done**

You will get the following feedback::

    FEEDBACK:: All board game data accessed via this tool is owned by BoardGameGeek and provided through their XML API

Usable Fields
-------------

These are:

- **AVERAGEWEIGHT** -
- **BAYESAVERAGE** -
- **BGG** -
- **CATEGORIES** -
- **DESCRIPTION** -
- **DESCRIPTION_SHORT** -
- **DESIGNERS** -
- **DISPLAY** -
- **EXPANDS** -
- **EXPANSION** -
- **EXPANSIONS** -
- **FAMILIES** -
- **ID** -
- **IMAGE** -
- **IMPLEMENTATIONS** -
- **MAXPLAYERS** -
- **MECHANICS** -
- **MEDIAN** -
- **MINAGE** -
- **MINPLAYERS** -
- **NAME** -
- **NUMCOMMENTS** -
- **NUMWEIGHTS** -
- **OWNED** -
- **PLAYERS** -
- **PLAYINGTIME** -
- **PROPERTIES** -
- **PUBLISHERS** -
- **RANKS** -
- **SET_PROPERTIES** -
- **SHORT** -
- **STDDEV** -
- **THUMBNAIL** -
- **TRADING** -
- **USERSRATED** -
- **WANTING** -
- **WISHING** -
- **YEARPUBLISHED** -

Subsets of Games
----------------

You can retrieve a subset of games by providing one or more items to match on.

These are:

- *own* -  include (if ``True``) or exclude (if ``False``) owned items
- *rated* -  include (if ``True``) or exclude (if ``False``) rated items
- *played* -  include (if ``True``) or exclude (if ``False``) played items
- *commented* -  include (if ``True``) or exclude (if ``False``) items commented on
- *trade* -  include (if ``True``) or exclude (if ``False``) items for trade
- *want* -  include (if ``True``) or exclude (if ``False``) items wanted in trade
- *wishlist* -  include (if ``True``) or exclude (if ``False``) items in the wishlist
- *preordered* -  include (if ``True``) or exclude (if ``False``) preordered items
- *want_to_play* -  include (if ``True``) or exclude (if ``False``) items wanting to play
- *want_to_buy* -  include (if ``True``) or exclude (if ``False``) items wanting to buy
- *prev_owned* -  include (if ``True``) or exclude (if ``False``) previously owned items
- *has_parts* -  include (if ``True``) or exclude (if ``False``) items for which there is a comment in the "Has parts" field
- *want_parts* -  include (if ``True``) or exclude (if ``False``) items for which there is a comment in the "Want parts" field

These are added as properties to the ``BGG()`` command. For example:

.. code:: python

    bgames = BGG(
        user='BenKenobi1976',
        own=True,
        want_to_play=True,
    )

In this example, games must be marked both as "want to play" items **and**
items that are "own"ed for the user ``BenKenobi1976``.


.. _the-font-command:

Font Command
============
`↑ <table-of-contents_>`_

**To Be Done**

.. _the-today-command:

Today Command
============
`↑ <table-of-contents_>`_

**To Be Done**
