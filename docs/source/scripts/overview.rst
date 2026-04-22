=======
Scripts
=======

.. |dash| unicode:: U+2014 .. EM DASH SIGN

This section describes add-ons to **protograf** that are not part of the
"core" functionality.


Using Scripts
=============

Scripts are pre-defined sets of code, designed to carry out a specific
functions, or a set of functions.

To use a script, you open a terminal and "run" it with Python in a similar way
that you do for a **protograf** script |dash| see
:ref:`Run a file with Python <runWithPython>`.

For example, to run the counter extraction script (note the extra ``-m``)::

    python -m protograf.scripts.counter_extraction

Some scripts may require additional information to work properly e.g.
the name of a configuration file.


Available Scripts
=================

.. _script-cards:

Creating Cards
--------------

The card creation script, called ``card_creation``, is designed to run a
series of prompts whose answers will be used set up a **protograf** file
for you, containing a basic template for the cards.

To run the card creation script (note the extra ``-m``)::

    python -m protograf.scripts.card_creation

Obviously, card designs vary widely, so this script can only provide a very
basic starter |dash| hopefully enough to see what the structure of such a
script should be...

.. _script-extraction:

Extracting Counters
-------------------

Extracting individual rectangular counter images, as might be found on a
scan of a full set of counters on a wargame's countersheet |dash| typically
an A4 or Letter-sized card |dash|, is useful to provide images to programs
such as `VASSAL <https://vassalengine.org/>`_

For details, refer to :doc:`Counter Extraction <counter_extraction>`
reference.
