================
Sequence Command
================

.. |dash| unicode:: U+2014 .. EM DASH SIGN

This section assumes you are very familiar with the concepts, terms and
ideas for :doc:`protograf <index>` as presented in the
:doc:`Basic Concepts <basic_concepts>` , that you understand all of the
:doc:`Additional Concepts <additional_concepts>`
and that you've created some basic scripts of your own using the
:doc:`Core Shapes <core_shapes>`.

This is part of the set of commands use for :doc:`Layouts <layouts>`.

Overview
========

The `Sequence()` command is designed to lay out a number of values - letters or
numbers, or shapes - in a straight line.

Apart from the ``Sequence()`` command described here, there are also these
other commands which allow you to layout elements in a more repetitive or
regular way within a page:

- :doc:`Repeat <layouts_repeat>`
- :doc:`Track <layouts_track>`
- :doc:`RectangularLocations <layouts_rectangular>`
- :doc:`TriangularLocations <layouts_triangular>`

.. _the-sequence-command:

Usage
=====

The ``Sequence()`` command accepts the following properties:

- **shape** - this is one of the core shapes available, for example, a circle
  or rectangle; the properties of that shape will determine where the first one
  in the sequence is drawn; the shape should always be specified with a
  lowercase initial so that the ``Sequence()`` can handle the drawing.
- **setting** - [1] this can be a *set* i.e. a number of values enclosed in
  `(...)` round brackets; representing these attributes required to construct
  the sequence:

  - *start* - the value the sequence starts with
  - *end* - the value the sequence ends with
  - *increment* - the difference between one value and next |dash| if negative,
    the values decrease
  - *type* - the sequence can be `letter`, `number`, `roman`, or `excel`
- **setting** - [2] alternatively, the setting can be specified by providing a
  list of values (using square ``[...]`` brackets); these are drawn in the order
  provided and can be a mix of letters or numbers
- **interval_x** and **interval_y** - [1] the distance between the centre of
  each shape that is drawn, starting from the location of the first as the
  reference point; negative numbers means the distances are to the left and up
  (rather than to the right and down)
- **interval_x** and **interval_y** - [2] a list of values representing the
  incremental distance between the centre of each shape that is drawn, starting
  from the location of the first as the reference point; negative numbers means
  the distances are to the left and up (rather than to the right and down)


Example 1. Sequence Values #1
-----------------------------
`↑ <the-sequence-command_>`_

.. |sv1| image:: images/layouts/sequence_values1.png
   :width: 330

===== ======
|sv1| This example shows how the ``Text()`` shape is used to display the
      values in the sequence; the values are automatically assigned to its
      **text** property.

      This example with **normal integer numbers** is created by:

      .. code:: python

          Sequence(
              text(x=1, y=3),
              setting=(10, 0, -2, 'number'),
              interval_x=0.5,
          )

      Here the progression is one of numbers.

      The range starts at ``10`` and the sequence will use every second number
      because the interval is ``-2``.

      The first shape is drawn at ``1.5`` cm and the ``interval_x`` property
      means that each shape will be ``0.5`` cm to the right (positive ``x``
      direction) of the previous one.

      The shapes drawn will be in a level line, because the default
      ``interval_y`` value is zero.

===== ======

Example 2. Sequence Values #2
-----------------------------
`↑ <the-sequence-command_>`_

.. |sv2| image:: images/layouts/sequence_values2.png
   :width: 330

===== ======
|sv2| This example shows how the ``Text()`` shape is used to display the
      values in the sequence; the values are automatically assigned to its
      **text** property.

      This example with **lowercase letters** is created by:

      .. code:: python

          Sequence(
              text(x=1, y=2.5),
              setting=('h', 'b', -2, 'letter'),
              interval_y=0.5,
              interval_x=0.5,
          )

      Here the progression is one of letters.

      The letters will be lowercase because the start letter |dash| ``h``
      |dash| is lowercase.

      The sequence ends with a ``b``.

      The sequence will use every second letter because the interval value
      is set to ``-2``.

      After the first shape is drawn, each following shape will
      be ``0.5`` cm to the right (``interval_x``) and ``0.5`` cm
      above (``interval_y``) the previous one.

===== ======

Example 3. Sequence Values #3
-----------------------------
`↑ <the-sequence-command_>`_

.. |sv3| image:: images/layouts/sequence_values3.png
   :width: 330

===== ======
|sv3| This example shows how the ``Text()`` shape is used to display the
      values in the sequence; the values are automatically assigned to its
      **text** property.

      This example with **uppercase letters** is created by:

      .. code:: python

          Sequence(
              text(x=1, y=4),
              setting=('B', 'J', 2, 'letter'),
              interval_y=-0.5,
              interval_x=0.5,
          )

      Here the progression is one of uppercase letters because the start letter
      is ``B``.

      After the first shape is drawn, each following shape will be
      ``0.5`` cm to the right and above |dash| because ``interval_y`` is
      negative |dash| the previous one.

===== ======

Example 4. Sequence Values #4
-----------------------------
`↑ <the-sequence-command_>`_

.. |sv4| image:: images/layouts/sequence_values4.png
   :width: 330

===== ======
|sv4| This example shows how the ``Text()`` shape is used to display the
      values in the sequence; the values are automatically assigned to its
      **text** property.

      This example with **Roman numerals** is created by:

      .. code:: python

          Sequence(
              text(x=0.5, y=3),
              setting=(5, 11, 1, 'roman'),
              interval_x=0.5,
          )

      Here the progression is one of Roman numbers.

      The range starts at ``5``, which is a ``V`` in Roman, and ends at
      ``11`` which is a ``XI`` in Roman.

===== ======

Example 5. Sequence Values #5
-----------------------------
`↑ <the-sequence-command_>`_

.. |sv5| image:: images/layouts/sequence_values5.png
   :width: 330

===== ======
|sv5| This example shows how the ``Text()`` shape is used to display the
      values in the sequence; the values are automatically assigned to its
      **text** property.

      This example with **Excel columns** is created by:

      .. code:: python

          Sequence(
              text(x=0.5, y=3),
              setting=(27, 52, 5, 'excel'),
              interval_x=0.5,
          )

      Here the progression is one of Excel column headers.

      The value ranges from:

      -  ``AA`` for the first value, which corresponds to column number 27

      to:

      - ``BE`` for the last value, which corresponds to column number 52

      The values make use of letter pairs from every ``5`` th column.

===== ======

Example 6. Sequence Shapes #1
-----------------------------
`↑ <the-sequence-command_>`_

.. |sq1| image:: images/layouts/sequence_shape2.png
   :width: 330

===== ======
|sq1| In this example, values in the sequence are being assigned
      to a text-based property using the special ``{{sequence}}`` keyword.

      The keyword is replaced by the **actual** value of the sequence number
      for the item.

      This example with **rectangles** is created by:

      .. code:: python

          Sequence(
              rectangle(
                  x=0.25, y=0.25, height=0.75, width=1,
                  label_size=8, label="${{sequence}}"),
              setting=(1, 3, 1, 'number'),
              interval_x=1.2,
          )

      Here the progression is one of numbers.

      Each number in the sequence is assigned to the ``{{sequence}}`` keyword
      and substituted into the text as part of the ``Rectangle`` 's label;
      the ``$`` is just a normal character.

===== ======

Example 7. Sequence Shapes #2
-----------------------------
`↑ <the-sequence-command_>`_

.. |sq2| image:: images/layouts/sequence_shape3.png
   :width: 330

===== ======
|sq2| In this example, values in the sequence are being assigned
      to a text-based property using the special ``{{sequence}}`` keyword.

      The keyword is replaced by the **actual** value of the sequence number
      for the item.

      This example with **hexagons** and **circles** is
      created by:

      .. code:: python

          Sequence(
              [hexagon(
                  cx=1, cy=1, radius=0.5,
                  title_size=8,
                  title="Fig. {{sequence}}"),
               circle(
                   cx=1, cy=1, radius=0.2,
                   fill="gray")],
              setting=('A', 'C', 1),
              interval_y=1.5,
              interval_x=0.5,
          )

      Here the progression is one of uppercase letters (start letter is ``A``).

      Note that the *letter* value is missing from the setting; this is because
      the type of value can be inferred from the start and end values.

      Each letter in the sequence is assigned to the ``{{sequence}}`` keyword and
      so that sequence value becomes part of the ``Hexagon`` 's title text.

      This example also shows how multiple shapes can be drawn at the same time
      with a single ``Sequence`` command.

      Instead of supplying a single shape, provide two or more in a list
      (enclosed with square brackets ``[...]``).

      As always the shapes are drawn in order |dash| the hexagon first and then
      the grey circle |dash| downwards and to the right (positive intervals).

===== ======

Example 8. Sequence Shapes #3
-----------------------------
`↑ <the-sequence-command_>`_

.. |sq3| image:: images/layouts/sequence_shape1.png
   :width: 330

===== ======
|sq3| In this example, values in the sequence are being assigned
      to a text-based property using the special ``{{sequence}}`` keyword.

      The keyword is replaced by the **actual** value of the sequence number
      for the item.

      This example with **circles** is created by:

      .. code:: python

          Sequence(
              circle(
                  cx=2, cy=4, radius=0.3,
                  label="{{sequence}}"),
              setting=[4, 'B?', '', 10, 'VI'],
              interval_y=-0.7,
          )

      Here the **setting** is a *specific list of values*.

      The settings items are separated by commas between the square brackets
      from ``[`` to ``]``.

      In this case, the list is a mixture of letters and numbers; which are
      assigned as part of the ``Cirle``'s label via the ``{{sequence}}``
      keyword.

      .. NOTE::

          The ``''`` (empty quotes) for the third item in the
          ``setting`` mean that nothing is assigned to the ``{{sequence}}``
          but that the ``Cirle`` itself is still drawn!

===== ======

Example 9. Sequence Shapes #4
-----------------------------
`↑ <the-sequence-command_>`_

.. |sq4| image:: images/layouts/sequence_shape4.png
   :width: 330

===== ======
|sq4| In this example, values in the sequence are being assigned
      to a text-based property using the special ``{{sequence}}`` keyword.

      The keyword is replaced by the **actual** value of the sequence number
      for the item.

      This example with **squares** is created by:

      .. code:: python

        Sequence(
            [square(
                x=1.5, y=1, side=0.5,
                rounded=True,
                label_size=8, label ="{{sequence}}")],
            setting=list('DIANA'),
            interval_y=0.6,
            interval_x=0.0,
        )

      Here the **setting** values are generated by a Python function called
      ``list()`` which splits the word into a list of single letters; these
      5 letters are assigned in turn to the ``{{sequence}}`` to use for the
      Squares' labels.

===== ======

Example 10. Sequence Shapes #5
------------------------------
`↑ <the-sequence-command_>`_

.. |sq5| image:: images/layouts/sequence_shape5.png
   :width: 330

===== ======
|sq5| In this example, values in the sequence are being assigned
      to a text-based property using the special ``{{sequence}}`` keyword.

      The keyword is replaced by the **actual** value of the sequence number
      for the item.

      This example with **polygons** is created by:

      .. code:: python

        Sequence(
            [polygon(
                cx=2, cy=0.5,
                sides=7, radius=0.5,
                label_size=7,
                label="{{sequence}}")],
            setting=[
                "red", "orange", "yellow",
                "green", "blue"],
            interval_y=[1.25, 1.5, 1, 1.25, 0.75],
            interval_x=0.0,
        )

      Here the **setting** is a list of words; these are assigned to the
      ``{{sequence}}`` to use for the Polygon's label.

      The *interval_y* property is a list of incremental values; these can be
      used to position the shape at any y-position on a page.  This can be
      combined, if needed, with a list of any incremental *interval_x* values.
      The result is to allow complete flexibility over where items in the
      sequence can be placed.

===== ======
