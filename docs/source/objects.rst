==============
Custom Objects
==============

.. |dash| unicode:: U+2014 .. EM DASH SIGN

This section assumes you are very familiar with the concepts, terms and ideas
for :doc:`protograf <index>`  as presented in the
:doc:`Basic Concepts <basic_concepts>` , that you understand all of the
:doc:`Additional Concepts <additional_concepts>` and that you've created some
basic scripts of your own using the :doc:`Core Shapes <core_shapes>`. You also
be familiar with the various types of shape's properties described in the
:doc:`Customised Shapes <customised_shapes>`

Overview
========

:doc:`protograf <index>` provides additional objects that can be drawn, along
with customised properties, in addition to the basic set of
:doc:`core shapes <core_shapes>`.

In many cases, these are constructed out of one or more of the core shapes;
for example, `polyominoes`_ are composed of one or more
:ref:`squares <square-command>`. Thus they are able to use, or reference, the
properties of these shapes, in addition to their own particular properties.

Polyominoes
===========

These are shapes constructed out of a pattern of one or more squares.

Normally, polyominoes are made up of squares that touch other squares
along one or more sides, but the ``pattern`` property approach used by
:doc:`protograf <index>` means that any kind of arrangement can be
constructed.

For more details, see the section on :doc:`Polyominoes <polyominoes>`.

Pentominoes
===========

These are one of the most popular and well-known types of polyominoes;
and each one is composed of **5** squares in one of 12 unique patterns.

They can referred to by their shortcut ``letter`` property which has been
assigned to each of the 12 shapes, based on their similarity to letters in
the Roman alphabet.

For more details, see the section on :doc:`Pentominoes <pentominoes>`.

Tetrominoes
===========

Similar to Pentominoes, these are each composed of **4** squares in one of 5
unique patterns. They can also referred to by their shortcut ``letter``
property.

For more details, see the section on :doc:`Tetrominoes <tetrominoes>`.
