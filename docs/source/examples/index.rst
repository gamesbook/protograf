========================
Overview of the Examples
========================

.. |dash| unicode:: U+2014 .. EM DASH SIGN

The examples supplied with :doc:`protograf <../index>` attempt to highlight
or demonstrate how different functions or features can be used. They do
**not** attempt to be comprehensive and cover all features, but they
**do** give some ideas as to what can be done |dash| and how.

In most cases, you will need to look at the example script itself to
understand how the output has been created.

1. There is a somewhat random tour of various elements in **protograf**
   available as a `PDF file <https://github.com/gamesbook/protograf/blob/master/docs/source/examples/demo.pdf>`_ - it is based on the
   `demo script <https://github.com/gamesbook/protograf/blob/master/examples/core/demo.py>`_
2. :doc:`Abstract Boards <abstract>` and
   :doc:`Commercial Boards <commercial>` - construction examples for games
3. :doc:`Counters <counters>` - counters are really just "tiny square
   cards"!
4. :doc:`Cards <cards>` - different kinds of decks that can be
   constructed
5. :doc:`BGG <bgg>` - how to retrieve and display data that can be
   accessed from the BoardGameGeek API
6. :doc:`Assorted <various>` - examples of various "real world" things;
   usually constructed using multiple different elements of **protograf**
   to give ideas of how these can be used together in a game design

.. HINT::

   All the examples are stored into a single
   `ZIP file <https://github.com/gamesbook/protograf/blob/master/examples.zip>`_
   which can be downloaded and extracted.

   If, in a Terminal, you navigate to the ``examples`` directory, you will
   find two batch files:

   - For Windows, you can run the ``all.bat`` file
   - For Linux, you can run the ``all.sh`` file

   These batch files process each example script in turn and save the
   output from each as a PDF file:

   - In Windows, to a subdirectory ``Temp\protograf`` under your home directory
   - In Linux, to the ``tmp/demo`` subdirectory

   You may notice that each file is called with the ``--no-png`` option.
   This is prevent PNG images being created; the reason for this is because
   the directory names in some of the example files will likely not exist
   on your machine.
