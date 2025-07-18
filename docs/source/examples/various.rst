=================
Examples: Various
=================

.. |dash| unicode:: U+2014 .. EM DASH SIGN

These examples are meant to demonstrate the type of output you can expect
to create with **protograf**.  They are *not* meant to be exhaustive or
comprehensive!

Bear in mind that the images shown in these examples are lower-resolution
screenshots; the original PDFs that can be generated from the source scripts
will demonstrate full scalability.

.. _table-of-contents-exvar:

- `A Clock`_
- `Chords`_
- `Rondel`_
- `Miscellaneous Objects 1`_
- `Miscellaneous Objects 2`_
- `World Clocks`_

A Clock
=======
`↑ <table-of-contents-exvar_>`_

=========== ==================================================================
Title       *A Wall Clock*
----------- ------------------------------------------------------------------
Script      `clock.py <https://github.com/gamesbook/protograf/blob/master/examples/various/clock.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to create a complex element - a clock - by
            combining :ref:`multiple Circles <circleIndex>`, each
            with different properties.

            Only the first circle |dash| the clock's outline border and its
            title |dash| has a *fill* color set but the rest do not:

              .. code:: python

                Circle(
                    cx=3, cy=4.5, radius=2.5,
                    stroke_width=6,
                    label="PROTO", label_size=6, label_my=1)

            The other circles - which each have a *fill* color of ``None`` so
            as to be transparent - make use of the *radii* property to draw
            some aspect of the clock, for example the hour marks:

              .. code:: python

                Circle(
                   cx=3, cy=4.5, radius=2.3,
                   stroke="white", fill=None,
                   radii=steps(0, 360, 30),
                   radii_stroke_width=1.5,
                   radii_length=0.3,
                   radii_offset=2.2)

            Here the setting of various *radii_* properties allows the marks
            to be generated.

            Of interest is the use of the :ref:`steps() <steps-function>`
            function to create the list of angles needed to specify where
            the offset radii used for the hours are to be drawn.

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/various/clock.png
               :width: 50%
=========== ==================================================================

Miscellaneous Objects 1
=======================
`↑ <table-of-contents-exvar_>`_

=========== ==================================================================
Title       *Miscellaneous Objects #1*
----------- ------------------------------------------------------------------
Script      `objects.py <https://github.com/gamesbook/protograf/blob/master/examples/various/objects.py>`_
----------- ------------------------------------------------------------------
Discussion  The first page of this set of examples shows how to construct
            various "compound" shapes by making use of various properties of
            different shapes.
----------- ------------------------------------------------------------------
Screenshot  .. image:: images/various/objects_1.png
               :width: 80%
=========== ==================================================================


Miscellaneous Objects 2
=======================
`↑ <table-of-contents-exvar_>`_

=========== ==================================================================
Title       *Miscellaneous Objects #2*
----------- ------------------------------------------------------------------
Script      `objects.py <https://github.com/gamesbook/protograf/blob/master/examples/various/objects.py>`_
----------- ------------------------------------------------------------------
Discussion  The second page of this set of examples shows how to construct
            various "compound" shapes by making use of various properties of
            different shapes.
----------- ------------------------------------------------------------------
Screenshot  .. image:: images/various/objects_2.png
               :width: 80%
=========== ==================================================================


Chords
======
`↑ <table-of-contents-exvar_>`_

=========== ==================================================================
Title       *Chords (in a circle)*
----------- ------------------------------------------------------------------
Script      `large_objects.py <https://github.com/gamesbook/protograf/blob/master/examples/various/large_objects.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a simple effect by combining
            a basic shape |dash| a :ref:`Chord <chord-command>` |dash| with a
            Python loop:

              .. code:: python

               for i in range(0, 200):
                   Chord(shape=Circle(
                           cx=2, cy=2, radius=2, fill=None),
                         angle=Random(360),
                         angle1=Random(360))

            Here the ``for`` loop runs for 200 times. Each time it does so,
            the :ref:`Random() <random-command>`  command generates a random
            value between 1 and 360 i.e. corresponding to degrees around a
            circle, to assign to the Chord's start and end points; then each
            Chord is drawn as usual.

            Also see :ref:`Python loops <python-loop>` for more details.
----------- ------------------------------------------------------------------
Screenshot  .. image:: images/various/chords.png
               :width: 40%
=========== ==================================================================


Rondel
======
`↑ <table-of-contents-exvar_>`_

=========== ==================================================================
Title       *Rondel (circle radii and sectors)*
----------- ------------------------------------------------------------------
Script      `large_objects.py <https://github.com/gamesbook/protograf/blob/master/examples/various/large_objects.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a simple effect by using
            data from a Python loop combined with *radii labels*:

              .. code:: python

                circ = Common(cx=2, cy=3, radius=2)

                # information needed
                radii = list(range(0, 360, 60))
                colrs = [
                    "lightsteelblue", "cyan", "gold",
                    "chartreuse", "tomato", "white", ]
                labels = [
                    'Build', 'Trade', 'Income',
                    'Plant', 'Explore', 'Harvest']

                # rondel colors
                for colr, angle in zip(colrs, radii):
                    Sector(
                        common=circ,
                        fill=colr,
                        stroke="sienna", stroke_width=2,
                        angle_start=angle - 30,
                        angle_width=60)
                # rondel text
                Circle(
                    common=circ,
                    stroke="#A0522D",
                    stroke_width=3,
                    fill=None,
                    radii=radii,
                    radii_offset=0.75,
                    radii_length=1,
                    radii_stroke_width=0.01,
                    radii_labels=labels,
                    radii_labels_font="Times-Roman",
                    dot=0.2)

            In this example, using the "offset" for the radii allows the
            label |dash| which is centred on the radius line |dash| to
            be moved further outward.

            Also see :ref:`Python loops <python-loop>` for more
            details.
----------- ------------------------------------------------------------------
Screenshot  .. image:: images/various/rondel.png
               :width: 50%
=========== ==================================================================


World Clocks
============
`↑ <table-of-contents-exvar_>`_

=========== ==================================================================
Title       *World Clocks*
----------- ------------------------------------------------------------------
Script      `world_clocks.py <https://github.com/gamesbook/protograf/blob/master/examples/various/world_clocks.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to reuse a complex element |dash| a clock
            |dash| by means of a set of Python functions; see
            :ref:`Python functions <python-function>` for more
            details.

            This is a fairly complex script |dash| a mini program really |dash|
            which is likely only to be legible to a Python programmer! It's
            probably far beyond the scope of this library's intended use...

            The script essentially "wraps" the clock creation approach
            described above into a function which is accessed for each city,
            or place, whose clock should be displayed.

            The script also uses other functions to calculate the position
            of the clock hands based on the current time of the day; this is
            a bit fiddly because the hour hand angle changes in relation to
            the number of minutes. The clock face and the hand colors are
            changed depending on the day/night and light/dark cycles.

            Further ideas:

            -  Wrap a call to this script via a command that gets runs each
               minute e.g. via ``cron`` on Linux; this will produce an updated
               image of times which could be displayed automatically on screen
               by a suitable viewer.
            -  Add a link to an API that generates quotes; use this quote for
               the header text so that a new quote appears each time the script
               is run.
----------- ------------------------------------------------------------------
Screenshot  .. image:: images/various/world_clocks.png
               :width: 90%
=========== ==================================================================
