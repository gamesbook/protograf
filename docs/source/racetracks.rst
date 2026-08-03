=========
RaceTrack
=========

.. |dash| unicode:: U+2014 .. EM DASH SIGN

This section assumes you are very familiar with the concepts, terms and ideas
for :doc:`protograf <index>`  as presented in the
:doc:`Basic Concepts <basic_concepts>` , that you understand all of the
:doc:`Additional Concepts <additional_concepts>` and that you've created some
basic scripts of your own using the :doc:`Core Shapes <core_shapes>`. You also
be familiar with the various types of shape's properties described in the
:doc:`Customised Shapes <customised_shapes>`

.. _racetrackOver:

Overview
========

A number of games make use of a RaceTrack, so being able to readily add
one to a graphic, or game board layout, can be useful.

It should be noted that while the object's name is "RaceTrack" it is really
more of a pathway, to which can be added styling by means of the properties
of the shapes that compose it.

.. _racetrack-object:

RaceTrack Properties
====================

A ``RaceTrack`` is effectively a pathway; and, if the end of the pathway
aligns with the start, it becomes what can be perceived as a "racetrack".

The ``RaceTrack`` does not really have the basic properties common to many
other :doc:`shapes <core_shapes>`; instead it derives its appearance from
the Bands and/or Rectangles which compose it.

The ``RaceTrack`` command only has one property:

- **stages** - this is a list (inside ``[``..``]`` brackets) of one or more
  :ref:`Rectangles <rectangle-command>` and/or :ref:`Bands <band-command>`

Starting with the first shape, and proceeding **counter-clockwise**, each shape
is laid-out, its end aligned with the start of the previous one.  This means
that the position of all shapes, except the first, is overridden by the
``RaceTrack`` construction.

.. NOTE::

    The "width" of the ``RaceTrack`` is determined by the *height* of the first
    shape in the **stages** list.  All other subsequent shapes have their height
    set to match.


RaceTrack Examples
==================

The examples below show how Bands and/or Rectangles are used to create a
RaceTrack.


Example 1. Simple Track
------------------------
`^ <racetrack-object_>`_

.. |rt1| image:: images/objects/racetrack_simple.png
   :width: 330

===== ======
|rt1| This example shows a RaceTrack constructed using commands like:

      .. code:: python

         basics = Common(
           width=1.0,
           stroke="black")

         rect1 = rectangle(
           common=basics, fill="gold",
           height=0.5, x=2)
         rect2 = rectangle(
           common=basics, fill="aqua",
           height=1.0)

         RaceTrack(stages=[rect1, rect2])

        styles = Common(
          stroke="black",
          radius=1,
          angle_width=60)

        band1 = band(
          common=styles, fill="gold",
          height=0.5, cx=2, cy=4,
          angle_start=30)
        band2 = band(
          common=styles, fill="aqua",
          height=0.25)

        RaceTrack(stages=[band1, band2])

      The start of the RaceTrack is determined by the position of ``rect1``
      as it is first in the *stages* list.

      The top example shows a RaceTrack composed of Rectangles.

      The position and height of ``rect2`` are both changed; the *height* is
      set to match that of ``rect1``, while its position is changed so that its
      right-edge aligns with the left-edge of of ``rect1``.

      The middle example shows a RaceTrack composed of Bands.

      The position and height of ``band2`` are both changed; the *height* is
      set to match that of ``band1``, while its position is changed so that its
      right-edge aligns with the left-edge of of ``band1``.

===== ======
