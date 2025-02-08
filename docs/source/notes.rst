===========
protograf
===========

.. _table-of-contents:

Table of Contents
=================

- `Overview`_
- `Concept`_
- `Elements`_


Overview
========
`↑ <table-of-contents_>`_

**protograf** is a simple Python utility for fast creation of elements needed for
prototype board or card games or other creative endevours requiring regular, simple
output.

**protograf** is *not* a graphic design program, nor even at the level of tools such
as nanDeck (see http://www.nand.it/nandeck/), or MultiDeck
(https://www.semicolon.com/multideck/multideck.html),  both of which have support for
fairly complex designs.


Concept
=======
`↑ <table-of-contents_>`_

The program should be reasonably simple, quick and useful.

- *Simple* in that names and shortcuts make sense; defaults are sensible;
  common things are fairly easy
- *Quick* in that commands should be simple and easy things should take a few lines
- *Useful* for common scenarios but not at the level of complex graphic design
- *Readable* in that commands use common names rather than quirky abbreviations
  or special characters.

The assumption is that a user of this tool wants to rapidly develop a prototype in
digital form, and is expecting to iterate over numerous versions in the course of a
design process.

For rapid design changes, a clean and simple layout is better than getting
bogged down in the complexities of, for example, graduated shading, font kerning
or intricate interdependant layouts.

The underlying availability of Python means that more complex scenarios can,
if needs be, be catered for by a programmer with knowledge of the langauge.


Elements
========
`↑ <table-of-contents_>`_

.. table::
    :width: 100
    :widths: 30, 50, 20

    ========== ========== ========
    Properties Shapes     Layouts
    ========== ========== ========
    stroke     line       card
    x, y       hexagon    deck
    cx,cy      circle     grid
    rotation   rectangle  tile
    height     ellipse    sequence
    width      polygon    track
    label      image
    angle      text
    ========== ========== ========

All elements have default properties; sizes are based on 1cm (centimeter) as a default;
the default foreground color, used for drawing lines, is ``black`` and the default
background color, used for filling in areas, is ``white``.
