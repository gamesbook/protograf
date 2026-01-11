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
that you do for a PG script |dash| see
:ref:`Run a file with Python <runWithPython>`.

For example, to run the counters extraction script::

    python -m protograf.scripts.counter_extraction

Some scripts may require additional information to work properly e.g.
the name of a configuation file.


Available Scripts
=================

Extracting counters
-------------------

Extraction of individual rectangular counter images, as might be found on a
scan of a full set of counters on a wargame's countersheet |dash| typically
an A4 or Letter-sized card |dash| is useful to provide images to programs
such as `VASSAL <https://vassalengine.org/>`_

For details, refer to :doc:`Counter Extraction <counter_extraction>`
reference.
