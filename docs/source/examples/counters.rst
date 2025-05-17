==================
Examples: Counters
==================

.. |dash| unicode:: U+2014 .. EM DASH SIGN

These examples are meant to demonstrate the type of output you can expect
to create with **protograf**.  They are *not* meant to be exhaustive or
comprehensive!

Bear in mind that the images shown in these examples are lower-resolution
screenshots; the original PDFs that can be generated from the source scripts
will demonstrate full scalability.

.. _table-of-contents-excntr:

Table of Contents
=================

- `Wargame - Basic Counters`_
- `Wargame - Counters from CSV`_
- `Wargame - Counters from Excel`_
- `Wargame - Blocks from CSV`_


Wargame - Basic Counters
========================
`↑ <table-of-contents-excntr_>`_

=========== ==================================================================
Title       *Basic Wargame Counters*
----------- ------------------------------------------------------------------
Source Code `counters.py <https://github.com/gamesbook/protograf/blob/master/examples/counters/counters.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a set of counters.

            The "placeholder" for the counters is the ``CounterSheet``; here
            it defines how many are needed and what their basic size and
            default color is, as well the grouping and spacing between the
            groups:

              .. code:: python

                CounterSheet(
                    counters=18,
                    width=2.6, height=2.6,
                    fill="yellow",
                    grouping_cols=3, grouping_rows=2,
                    spacing_x=2.6, spacing_y=1.3
                    )

            The layouts for the counters are constructed from a series of a
            basic shapes. Intermediate steps are stored via assigned names;
            this allows them to be reused in different places, for different
            counters that share common elements.

            Remember that using lowercase names for the shape commands means
            that they will **not** be drawn immediately, but only when the
            card itself is drawn.

            Following is "walkthrough" on how some (*not* all) of the counters
            from this example are created.

            First, the shapes forming the conventional symbol for an
            infantry unit ('X' in a box) are assigned names and then combined
            with a :ref:`group function <group-function>`:

              .. code:: python

                out = rectangle(
                  x=0.8, y=1.2, width=1.0, height=0.6,
                  stroke_width=0.5, fill=None)
                lu = line(
                  x=0.8, y=1.2, x1=1.8, y1=1.8,
                  stroke="black", stroke_width=1.5)
                ld = line(
                  x=0.8, y=1.8, x1=1.8, y1=1.2,
                  stroke="black", stroke_width=1.5)
                inf = group(out, lu, ld)

            Then text and color (for one of the country's armies) are defined:

              .. code:: python

                brown = "#B6A378"
                inf_A = text(
                  font_name="Helvetica", font_size=18,
                  x=1.3, y=0.5, text="2-3-4")
                division = text(
                  font_name="Helvetica", font_size=12,
                  x=1.3, y=1.9, text="XX")

            Now the counter outline is defined:

              .. code:: python

                russian = rectangle(
                   x=0, y=0, width=2.6, height=2.6,
                   stroke_width=1, fill=brown)

            And finally the complete counter itself is defined in a two step
            process, also using the :ref:`group function <group-function>`
            to combine different, previously-defined elements:

               .. code:: python

                inf_russian = group(russian, inf)
                inf_russian_A = group(inf_russian, inf_A, division)

            Finally, the counter, or counters, can be drawn in one or more
            positions on the countersheet:

               .. code:: python

                Counter("13-15", inf_russian_A)

            These counters are shown outlined in blue in the screenshot. Note
            that the blue line was *not* created as part of the script but
            just added in with a graphics editor.

            Bear in mind that counters are drawn in order, starting from the
            top-left, then moving across to the right to complete a row,
            then moving down to the next row - so in this example, counters 1
            to 6 are drawn along the top row |dash| in two groups of 3
            each |dash| followed by 7 to 12 on the next row down, and so on.

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/counters/counters_basic.png
               :width: 100%
=========== ==================================================================


Wargame - Counters from CSV
===========================
`↑ <table-of-contents-excntr_>`_

=========== ==================================================================
Title       *Wargame Counters from a CSV file*
----------- ------------------------------------------------------------------
Source Code `counters_csv.py <https://github.com/gamesbook/protograf/blob/master/examples/counters/counters_csv.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a set of counters using data
            from a plain text CSV (comma-separated values) file.

            The CSV file contains data such as::

                NATION,TYPE,SIZE,VALUE,ID
                ...
                rus,INF,XX,2-3-4,55R/1
                rus,INF,XX,2-3-4,57R/1
                rus,INF,XX,2-3-4,72R/1
                ...
                ger,MARKER,,,
                ger,MARKER,,,

            The data is loaded into the script via the ``Data`` command, for
            which only the filename is needed:

              .. code:: python

                Data(filename="counters.csv")

            Using this command means that the number of counters in the
            ``CounterSheet`` will be based the number of rows in the file.

            In general, every line in the file corresponds to a counter that
            will be drawn, and defines key values that will determine how that
            counter will be drawn.

            Elements that should appear on a counter, and whose values or
            settings should be derived from data in the file, can now refer
            to the headings appearing at the start of the file; for example:

              .. code:: python

                ident = text(
                    text=T('{{ID}}'),
                    font_name="Helvetica", font_size=12,
                    x=0.25, y=0.7,
                    width=0.8, height=1.4,
                    wrap=True, align='centre',


            Here the text that will be used depends on data in the **ID**
            column. This can be accessed by the ``T({{ID}})`` (template
            command). So, in the first row of data, shown in the file snippet
            above, contains an **ID** value of ``55R/1``.

            When this is referenced by a Counter in the script:

              .. code:: python

                Counter("all", value, size, ident)

            ``ident`` will use the text in the  **ID** column and assign it
            to the counter being drawn.  You can see the values from the
            snippet of CSV shown above on the left side of the counters
            outlined in blue in the screenshot.

            It is possible to do *conditional* assignment using an ``S`` (for
            **Select**) command;  for example:

              .. code:: python

                Counter(
                  "all",
                  S("{{ TYPE == 'MARKER' and NATION == 'ger' }}",
                  marker_german))

            Here, the ``marker_german`` element (which happens to link to an
            image) will *only* be drawn if the row in the CSV file meets both
            of **two** conditions, using the
            :ref:`S() command <the-selection-command>`:

            1. it has a **TYPE** value equal to *MARKER*, ``and``
            2. it has a  **NATION** value equal to *ger*

            Note that both examples ensure that the *case* (upper or lower)
            is being matched correctly.

            An example of this is last two rows from the snippet of CSV shown
            above.  The resulting counters are outlined in yellow in the
            screenshot.

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/counters/counters_csv.png
               :width: 100%
=========== ==================================================================


Wargame - Counters from Excel
=============================
`↑ <table-of-contents-excntr_>`_

=========== ==================================================================
Title       *Wargame Counters from an Excel file*
----------- ------------------------------------------------------------------
Source Code `counters_excel.py <https://github.com/gamesbook/protograf/blob/master/examples/counters/counters_excel.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a set of counters using data
            from an Excel file.

            This example is effectively exactly the same as the ones above,
            with the only difference being the data source file:

              .. code:: python

                Data(filename="counters.xls")

            .. HINT::

                It is possible - maybe even preferable! - to use a font for
                common/standard military unit icons; see, for example,
                the *JZNATO v11* font available from:
                https://github.com/jzedwards/jzfonts

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/counters/counters_excel.png
               :width: 100%
=========== ==================================================================


Wargame - Blocks from CSV
=========================
`↑ <table-of-contents-excntr_>`_

=========== ==================================================================
Title       *Wargame Block Labels from a CSV file*
----------- ------------------------------------------------------------------
Source Code `blocks_csv.py <https://github.com/gamesbook/protograf/blob/master/examples/counters/blocks_csv.py>`_
----------- ------------------------------------------------------------------
Discussion  This example shows how to construct a set of labels, designed to
            be attached to small wooden blocks, using data from a plain text
            CSV (comma-separated values) file.

            The same basic approach that is described in previous examples
            applies here.  The CSV looks like::

                SIDE,TITLE,MOVE,STRENGTH,DOTS,SHIELD,BORDER,IMAGE
                English,DURHAM,2,B2,4,red,#57762C,
                ...
                English,NORSE, ,A2,3,1,#416E83,viking.png

            Of interest, is that second-last column in each row defines a
            hexadecimal color (see :ref:`colors <basic-color>`) which can
            used, for example, via:

              .. code:: python

                outline = rectangle(
                  x=0.45, y=0.45,
                  width=2.0, height=2.0,
                  stroke_width=1,
                  stroke=T('{{BORDER}}'), fill=None)

            As described previously, the ``T()`` command allows the hexadecimal
            color value from the **BORDER** column to be used for the ``stroke``
            property of the Rectangle.

            These counters can also contain images, for example:

              .. code:: python

                pic = image(
                    T('images/{{IMAGE}}'),
                    x=0.7, y=0.95, width=1.5, height=1.1)

            This references the last column, called **IMAGE** of the CSV.
            If the column is empty, then no image is drawn.

            Another item of interest is the use of the ``Sequence`` command
            to create the small squares that run along the edge of each
            counter/label:

              .. code:: python

                lbrown = "#F1D7B5"
                top4 = sequence(
                     square(
                       x=0.9, y=2.35, side=0.25,
                       stroke=lbrown, stroke_width=1,
                       fill=T('{{BORDER}}')),
                     setting=(1, 4),
                     gap_x=0.29)

            Because its known that a counter/label always has a set of
            sequences that proceed, with decreasing length, in clockwise order,
            its possible to use ``group()`` commands to create all possible
            combinations of such sets of sequences.

----------- ------------------------------------------------------------------
Screenshot  .. image:: images/counters/blocks_csv.png
               :width: 100%
=========== ==================================================================
