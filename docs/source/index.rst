.. protograf documentation master file, created by
   sphinx-quickstart on Sat Jan 11 20:23:56 2025.

Welcome to protograf's documentation!
=====================================

.. image:: logo.png
  :width: 511
  :alt: protograf logo
  :target: https://github.com/gamesbook/protograf

`protograf <https://github.com/gamesbook/protograf>`_ is a utility written in
Python for designing and creating simple, regular, graphical outputs in PDF
(or PNG/GIF/SVG) format via a script.

**protograf**  has been primarily created to handle the prototyping of cards,
counters, tiles and boards for board games, including hexagonal grids, but can
also be used for creating any simple design that has regular or repetitive
elements; typically a mix of graphics and text.

If it's your first time here, please consult the `guide <guide.html>`_
which presents the sections designed to be read in order; they all contain
useful information but do build on each other.

.. toctree::
   :maxdepth: 2
   :caption: Getting Setup:

   setting_up

.. toctree::
   :maxdepth: 2
   :caption: Introduction:

   overview
   guide

.. toctree::
   :maxdepth: 2
   :caption: Concepts:

   basic_concepts
   script_anatomy
   additional_concepts
   terminology

.. toctree::
   :maxdepth: 2
   :caption: Text & Shapes:

   core_shapes
   customised_shapes
   customised_text

.. toctree::
   :maxdepth: 2
   :caption: Making Cards:

   card_deck_introduction
   card_decks
   worked_example
   deck_command
   card_images

.. toctree::
   :maxdepth: 2
   :caption: Advanced Topics:

   layouts
   hexagonal_grids
   hexhex_grids
   additional_commands
   objects
   functions
   using_fonts
   python_commands

.. toctree::
   :maxdepth: 2
   :caption: Examples:

   examples/index
   examples/abstract
   examples/commercial
   examples/bgg
   examples/cards
   examples/counters
   examples/various

.. toctree::
   :maxdepth: 2
   :caption: References:

   commands
   rationale
   development
   useful_resources


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
