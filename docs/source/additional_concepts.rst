===================
Additional Concepts
===================

This section assumes you are familiar with the concepts, terms and ideas
for :doc:`protograf <index>` as presented in
:doc:`Basic Concepts <basic_concepts>`, have looked through the
:doc:`Core Shapes <core_shapes>`, and that perhaps you have created one
or two basic scripts on your own, along the lines described in the
:doc:`Script Anatomy <script_anatomy>`.

.. _table-of-contents:

Table of Contents
=================

-  `Names and Naming`_
-  `Values: Text, Numbers and Booleans`_
-  `Assigned Names`_
-  `Case-sensitivity`_
-  `Calculations`_
-  `Changeable Values`_
-  `Quotes in Text`_
-  `Properties and Short-cuts`_
-  `Lists`_
-  `Errors`_


Names and Naming
================
`↑ <table-of-contents_>`_

Naming of things is supposed to be one of the harder aspects of programming!

If you work with the built-in commands and and their properties, the set
of names to use is already chosen for you. However, if you want to start
using some additional options, such as giving `assigned names`_ to reuse
items in multiple places, then you need to be aware of the wider set of
so-called "reserved" names that are available as part of Python.

.. WARNING::

   If your assigned name is the same as a reserved name, then you’ll
   overwite it and your scripts may fail in *very* strange ways!!

Reserved Names
--------------

Basic built-in names include: False, None, True, and, as, assert, async,
await, break, class, continue, def, del, elif, else, except, finally,
for, from, global, if, import, in, is, lambda, nonlocal,
not, or, pass, raise, return, try, while, with, yield

Python also has a number of built-in functions, used to carry out common
operations.

Function names include: abs, aiter, all, anext, any, ascii, bin, bool,
breakpoint, bytearray, bytes, callable, chr, classmethod, compile,
complex, delattr, dict, dir, enumerate, eval, exec, filter, float,
format, frozenset, getattr, globals, hasattr, hash, help, hex, id,
input, int, isinstance, issubclass, iter, len, list, locals, map, max,
memoryview, min, next, object, oct, open, ord, pow, print, property,
range, repr, reversed, round, set, setattr, slice, sorted, staticmethod,
str, sum, super, tuple, type, vars, zip

If you’re interested in what all these functions do, there is a very
readable guide available at:
https://www.mattlayman.com/blog/2024/layman-guide-python-built-in-functions/


Values: Text, Numbers and Booleans
==================================
`↑ <table-of-contents_>`_

An important concept in **protograf** is understanding the different types
of values and how they are used.

Values are typically associated with a property, and affect how a shape
appears, as discussed in :doc:`Basic Concepts <basic_concepts>`.

Text - whether individual letters or words - is often called a *string*, and
is wrapped in quotes - ``"`` - at the start and end of the string.
The string can contain numbers as well - ``"ABC 123"``. Strings are usually
**not** used for calculations, although some can be converted into numbers.
Also see below on `using quotes in text <Quotes in Text>`_.

Numbers are either *integers* - "whole" or "counting" numbers, such as ``21``
or ``100``, or *floats* which are numbers with fractions - ``3.141``.  In most
cases,  **protograf** will handle these differences for you.

Booleans are commonly referred to a "true or false" values. In Python, the
reserved names ``True`` and ``False`` can be used whenever such values are
required.  Some of the properties for some commands require a ``True`` value
to be activated.


Assigned Names
==============
`↑ <table-of-contents_>`_

A very likely usage for assigned names, is when the ``Common`` command is in
use.  This command stores a number of properties that need to be used across
multiple shapes or commands.

Giving this command an *assigned name* enables its result, or value, to be
referred to, and used or reused, later in the script.  For example:

.. code:: python

   green_dots = Common(fill=lime, dot=0.1)
   Circle(common=green_dots)
   Rectangle(common=green_dots)

Both the ``Circle`` and ``Rectangle`` share common properties |dash| ``fill``
and ``dot``|dash| which are assigned to each of their ``common`` property value.
This value |dash| ``green_dots`` |dash| is in turn created when is assigned
to the ``Common`` command.


Case-sensitivity
================
`↑ <table-of-contents_>`_

**protograf**, like Python, is case-sensitive - unlike some computer
languages or, for example, the file names that are used in Windows; so a
lowercase name is **NOT** the same as an uppercase version of it.

For example:

.. code:: python

    Rectangle()

will create and draw a ``Rectangle`` shape on the page; but:

.. code:: python

    area = rectangle()

will create a ``Rectangle`` shape, and assign a reference to it in the
property named ``area`` |dash| for use later on in the script |dash| but
will **not** draw the Rectangle on the page.


Calculations
============
`↑ <table-of-contents_>`_

Because **protograf** is able to use any of Python's built-in functionality,
your script can make use of tools such as the ability to perform calculations.

Basic arithmetic includes *addition* (``1+1``), *subtraction* (``1-1``),
*multiplication* (``1*1``), and *division* (``1/1``).  The ability to raise
a number to a given power is included (``2**3``).

Even though its not essential to use them, adding calculations can make a
script easier to read. For example, if working with *inches* as units, then a
fractional value can be set like this: ``x=5/16`` - while this is numerically
the same as ``x=0.3125`` its probably easier to understand the intent of the
calculation.


Changeable Values
=================
`↑ <table-of-contents_>`_

**protograf** comes with a number of "built-in" names that can be used in
some circumstances.  There are represented by the name enclosed in a pair of
quotes *and* a pair of double curly brackets: ``"{{name}}"``

Specifically, when working with grids, the ``row``, ``col`` (column) and
``sequence`` number are all available as changeable, named values; that is
to say, the value of that name will replace its appearance in the script.
For example, if a shape has this property ``label="{{row}}"`` when it is
drawn as part of a grid, the value of ``{{row}}`` will be replaced by the row
number in which it appears - say ``2``.  Because the values are numeric, it
is also possible to perform `calculations`_ with them; so an entry such as
``{{2 * row}}`` will produce values that are double that of the  row number.

When working with ``Deck()`` commands, the data source will contain named
columns with multiple values; again the use of a ``{{name}}`` - where *name*
is replaced by the column name - is possible.

.. NOTE::

    Changeable value names **are** case-sensitive!


Quotes in Text
==============
`↑ <table-of-contents_>`_

Using quotes - ``'`` or ``"`` - inside a string of letters can be tricky.

If you have a Text shape, for example, like this:

.. code:: python

   Text(x=1, y=1, text="Something interesting")

You can easily add single quotes as part of the text e.g. for ``isn't``::

   Text(x=1, y=1, text="Something isn't interesting")

However, if you want to use double quotes inside the text, then you’ll
need to change the outer ones to singles:

.. code:: python

   Text(x=1, y=1, text='Something "interesting"!')

What if you want to use single and double quotes in the text? In this
case, you’ll need to add a special marker character - a backslash - before
the quote that is matched by the outer one:

.. code:: python

   Text(x=1, y=1, text='Something isn\'t "interesting"!')

Here the ``\'`` in front of the ``t`` in ``isn't`` shows that the single
quote is **not** the end of the string, but simply a symbol that must be
displayed "as is".


Properties and Short-cuts
=========================
`↑ <table-of-contents_>`_

In general, **protograf** tries to avoid the use of short-cuts and instead
relies on short, but hopefully memorable, names for things, although there
are some exceptions,

Many properties are set with *directions* matching those shown on a compass,
and although you could want write these names out in full, it can be very
tedious  to type, for example, ``southeast`` or ``northwest`` and so
``se`` and ``nw`` are used instead.

The other exceptions are the location names.

- Instead of "across" and "up", **protograf** uses ``x`` and ``y`` because
  of their common usage in geometry.
- Similarly, ``cx`` and ``cy`` are used instead of "centre from left"
  or "centre from bottom".
- Also, ``mx`` and ``my`` are used instead of "move horizontally" or
  "move vertically".

Hopefully, these "short-cut" names will become memorable after working with
the program for a while.

Some of the other proprerties can be *optionally* abbreviated to use just their
first letter; so, for example, using ``d`` for a ``diamond`` layout of a
``Hexagons`` grid.


Lists
=====
`↑ <table-of-contents_>`_

Lists are a particularly useful way to collate, or group, related items
so that they can be processed together.

You may be familiar with examples such as grocery lists or to-do lists.
A list is normally written as a series of items, each separated with a
comma. For example; apples, oranges, bananas and plums.

A list can also be written vertically in the form of a number of bullets:

-  first,
-  second, and
-  third.

A column in a spreadsheet can be thought of as such a vertical list,
although you would not usually use an "and" in it!

Lists in **protograf** are written in a similar way but they need to
be identified by wrapping them at their start and end by the use of
*brackets*.

The brackets that are used are so-called **square brackets** - ``[`` and
``]``. Items in the list are separated by commas.

-  If they are numbers, then that’s all you need: for example, *[1, 3, 5,
   7]* - this list is a series of odd numbers.
-  If they are words, or strings of text then each item must be wrapped
   in quotes: for example, *['apples', 'oranges', 'bananas', 'plums']*
   or *["apples", "oranges", "bananas", "plums"]* |dash| remember that quotes
   can be single or double but not a mix of both!

.. NOTE::

   Note that there is **no** use of the word "and" in these lists!

A list is normally given an assignment to store it in memory for use by
the script; for example:

.. code:: python

   groceries = ['apples', 'oranges', 'bananas', 'plums']

This is so that the list can be referred to in the script by using the
shorthand reference name |dash| in this case ``groceries``. There are various
examples of the use of lists of elsewhere in these documents and also in
the script examples.

.. _script-errors

Errors
======
`↑ <table-of-contents_>`_

A situation that you will often encounter, especially as your script gets
longer and more complex, is the appearance of errors.

While **protograf** will attempt to check many details of the script,
its very unlikely to be able to catch every mistake that might be made.

It will do some basic error checking as to whether correct values have
been assigned to properties; so:

.. code:: python

    Rectangle(height="a")

will cause this error when the script is run::

    FEEDBACK:: The "a" is not a valid float number!
    FEEDBACK:: Could not continue with program.

because the ``height`` is meant to be a number, not a string.

In some cases, instructions will **not** cause an error, but they will simply
be ignored, for example:

.. code:: python

    Rectangle(corner="a")

will still draw a ``Rectangle``; the meaning of ``corner`` is unknown so it will
simply be skipped.

Python-specific Errors
----------------------

"Under the hood" Python will itself also report on various errors, for example:

.. code:: python

   Arc(x=1, y=1, x=2, y1=3)
                 ^^^
   SyntaxError: keyword argument repeated: x

Python attempts to identify the type and location of the error - a
``SyntaxError`` is just a grammar error of some type - as well as what
the cause *might* be. Here, it found that you have used the property ``x``
twice, so in this case you might need to change the second one to ``x1`` --
which  is probably the intended one:

.. code:: python

   Arc(x=1, y=1, x1=2, y1=3)

Another example:

.. code:: python

   Rectangle(height=1.5, stroke=green, fill=bred)
                                            ^^^^
   NameError: name 'bred' is not defined

In this case, the script uses the name of something - ``bred`` - which
is unknown. It could be a simple spelling mistake e.g. here it should be
``red`` *or* possibly you'd meant to assign the word ``bred`` to a particular
color before using it for the ``Rectangle``:

.. code:: python

   bred = "#A0522D"
   Rectangle(height=1.5, stroke=green, fill=bred)

Another example:

.. code:: python

   paper=A8 cards=9
            ^^
   SyntaxError: invalid syntax. Perhaps you forgot a comma?

Another ``SyntaxError`` where Python tries to assess what the cause
might be. Here, you’d need to add a ``,`` (comma) at the end of setting the
``paper=A8`` property as each property in the list **must** be comma-separated
(a space is not sufficient) as follows:

.. code:: python

   paper=A8, cards=9

.. NOTE::

  Needless to say, many articles and book chapters have been devoted to how
  one goes about finding problems or errors - one example is:
  http://greenteapress.com/thinkpython/html/thinkpython002.html#toc6 (and there
  are other chapters in this same book that may also be of help).
