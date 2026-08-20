=========================
Compound Objects Overview
=========================

.. |dash| unicode:: U+2014 .. EM DASH SIGN

This section assumes you are very familiar with the concepts, terms and ideas
for :doc:`protograf <../index>`  as presented in the
:doc:`Basic Concepts <../basic_concepts>` , that you understand all of the
:doc:`Additional Concepts <../additional_concepts>` and that you've created some
basic scripts of your own using the :doc:`Core Shapes <../core_shapes>`. You also
be familiar with the various types of shapes' properties described in the
:doc:`Customised Shapes <../customised_shapes>`

.. _objects-overview:

Summary
=======

In many cases, compound objects are constructed |dash| compounded |dash| out
of one or more of the :doc:`core shapes <../core_shapes>`; for example,
a `polyomino`_ is composed of one or more :ref:`squares <square-command>` and
simple `dice`_ are also a single square. Thus these objects are able to use,
or reference, many of the properties of these core shapes, in addition to their
own particular properties.

The compound objects available are:

- `CardBox`_ - a template to be cut-out and folded to create a box
- `Cube`_ - a 3D depiction of a shaded cube
- `Dice`_ - a top-down view of a "square" with dice pips
- `Domino`_ - a top-down view of a "double-square" with dice pips
- `Polyomino`_ - a pattern of one or more squares touching on their edges
- `Pentomino`_ - a well-known type of polyomino; each is composed of 5 squares
  in one of 12 unique patterns
- `Tetromino`_ - another type of polyomino; each is composed of 4 squares
  in one of 5 unique patterns
- `RaceTrack`_ - a pathway composed of Rectangles and Bands


CardBox
=======
`^ <objects-overview_>`_

A CardBox can be used to generate a template, or outline, of a shape
that is designed to be cut-out and folded to create a box |dash| for
boardgames, such a box is often referred to as a **tuckbox**.

For more details, see the :doc:`CardBox <cardbox>` section.


Cube
====
`^ <objects-overview_>`_

Cubes are used in many games, and being able to readily create a basic
depiction of them can be useful.

For more details, see the section on :doc:`Cubes <cubes>`.


Dice
====
`^ <objects-overview_>`_

Dice are used in many games, and being able to readily create a basic
depiction of them can be useful.

For more details, see the section on :doc:`Dice <dice>`.


Domino
======
`^ <objects-overview_>`_

Dominoes, like cards, are playing pieces used in a number of games, so being
able to readily create a basic depiction of them can be useful.

For more details, see the section on :doc:`Dominoes <dominos>`.


Polyomino
=========
`^ <objects-overview_>`_

A Polyomino is a shape constructed out of a pattern of one or more squares.

Normally, polyominoes are made up of squares that touch other squares
along one or more sides, but the ``pattern`` property approach used by
:doc:`protograf <index>` means that any kind of arrangement can be
constructed.

For more details, see the section on :doc:`Polyominoes <polyominoes>`.


Pentomino
=========
`^ <objects-overview_>`_

A Pentomino is one of the most popular and well-known types of polyominoes;
and each one is composed of **5** squares in one of 12 unique patterns.

They can referred to by their shortcut ``letter`` property which has been
assigned to each of the 12 shapes, based on their similarity to letters in
the Roman alphabet.

For more details, see the section on :doc:`Pentominoes <pentominoes>`.


Tetromino
=========
`^ <objects-overview_>`_

Similar to Pentominoes, these are each composed of **4** squares in one of 5
unique patterns. They can also referred to by their shortcut ``letter``
property.

For more details, see the section on :doc:`Tetrominoes <tetrominoes>`.


RaceTrack
=========
`^ <objects-overview_>`_

A RaceTrack is a composite shape, used in some games, that is composed of
a series of Bands and Rectangle shapes.  It can be useful to readily create
basic tracks, or pathways, making use of the specialised properties of its
component shapes.

For more details, see the :doc:`RaceTrack <racetracks>` section.
