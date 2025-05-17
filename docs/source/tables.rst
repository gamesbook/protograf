======
Tables
======

Elements
========

.. table::
    :width: 100
    :widths: 30, 50, 20

    ========== ========== ========
    Properties Shapes     Layouts
    ========== ========== ========
    stroke     line       card
    x,y        hexagon    deck
    location   circle     grid
    size       rectangle  tile
    height     ellipse    sequence
    width      polygon    track
    cx,cy      image
    angle      text
    ========== ========== ========


.. table::
    :width: 100
    :widths: 30, 50, 20

    +------------+-----------+----------+
    | Header 1   | Header 2  | Header 3 |
    |            |           |          |
    +============+===========+==========+
    |stroke      |line       |card      |
    +------------+-----------+----------+
    |x,y         |hexagon    |deck      |
    +------------+-----------+----------+
    |location    |circle     |grid      |
    +------------+-----------+----------+
    |size        |rectangle  |tile      |
    +------------+-----------+----------+
    |cx, cy      |arc        |          |
    +------------+-----------+----------+
    |angle       |image      |          |
    +------------+-----------+----------+

.. |rpk| image:: images/custom/rectangle/peak.png
   :width: 330

.. table::
    :width: 100
    :widths: 30, 70

    ===== ======
    |rpk| This example shows a Rectangle constructed using these properties below::

            Rectangle(
                x=1, y=4, width=2, height=1.5,
                font_size=6, label="points = s",
                peaks=[("s", 1), ("e", 0.25)]
            )

          Notes:

          - *peaks* - the value(s) used to create the peak; this is a list, shown
            by the square brackets (``[`` to ``]``), of one or more sets, each
            enclosed by the round brackets, consisting of a *directions* and a peak
            *size*.  Directions are the primary compass directions - (n)orth,
            (s)outh, (e)ast and (w)est, and sizes are the distances of the centre
            of the peak from the edge of the Rectangle.  If the value ``*``` is used
            for a direction, its short-cut meaning that peaks myst drawn in all four
            directions.
    ===== ======
