========
Overview
========

.. |dash| unicode:: U+2014 .. EM DASH SIGN

Introduction
============

The aim of :doc:`protograf <index>` is to provide a general purpose
program that allows you to design simple, scalable and reproducible text
and graphics that can be used for prototyping the elements or components
of a project, such as the creation of a board game, including the board,
the tiles, the cards and so on.

.. IMPORTANT::

   **protograf** is *NOT* a full-blown graphics editor |dash| like the
   Adobe Photoshop, GIMP, or Inkscape packages |dash| or a desktop publishing
   tool |dash| like Scribus, InDesign, or Xpress |dash| which allow
   sophisticated creation of complex graphics and text layouts; it does not
   attempt in **any** way to replicate their extensive functionality!


Who might want to use **protograf** ?
=====================================

**protograf** is useful for anyone that needs to work on a design in
an incremental fashion, tweaking and changing as they go along. Doing
this with a regular graphics package can sometimes be tedious;
especially when common changes need to be made across many elements.

Simple designs that make use of regular-shaped objects or fonts,
including fonts that themselves contain symbols or icons, are
straightforward to implement in **protograf**; but more complex
pictures or background images should be made, as usual, in a regular
graphics design package and then added into your script by a link
to the image file.

**protograf** also supports access of data in comma-delimited text files
|dash| often called "CSV" files |dash| and Excel documents; this can help
separate out the design and layout from the content - the text and the
numbers - that appears in the design.


Why not use a professional graphics package?
============================================

Obviously, if you use a graphics package as an everyday tool, that will
probably suit your needs perfectly.

However, there might be a reason to use something simpler. Daniel, of
https://daniel.games/ has this to say about making a prototype:

    The game should be neat. This means it's simple, clear, and not ugly.

    Your layout (of cards and other objects) should just be flat areas of
    muted colour, with text on top of it. It's simple and functional.

    Don't use textures, bevels, gradients, realistic shadows, or other
    embellishments.

    The best design is design done by a professional. The second-best design
    is no design at all, which is what you should do.

    In the same way, icons should just be simple, flat-colour shapes.
    Just go and get free, basic icons from https://thenounproject.com/
    Make better ones later, if you're good with graphic design.

(See more good advice at https://daniel.games/the-work-of-game-design.htm )

So, **protograf** aims to help you achieve the above |dash| the
"second-best design"!


How do I use **protograf**?
===========================

In general, what you do is type a set of instructions |dash| which
**protograf** terms a *script* |dash| into a file. You save that file on
your computer, and then use Python to create your output |dash| a PDF or
PNG file |dash| containing the results of those instructions; hopefully
the design that you intended to make!

As your design changes and evolves, you can add or change instructions and
recreate the output.


How does **protograf** work?
============================

**protograf** is written in Python; the reason being that this is a
relatively easy-to-use programming language that is often used for
scripting or automating routines |dash| both by itself and as part of larger
systems. Python has access to numerous packages that help avoid having
to write code from scratch.

.. NOTE::

   Python is *not* a speedy language, but its still fast enough to
   use for **protograf**

**protograf** uses various supporting Python packages; the most important
of these is *PyMuPDF* which supports the creation of vector graphics in
a PDF document.

**protograf** is designed in such a way that you *don’t* need to know how
to program in Python in order to use it; but if you *are* a Python
programmer then you can certainly treat this as you would any other
package and add in your own additional Python code or logic to your
scripts as needed.


How do I get started?
=====================

Its suggested that you **first** get everything :doc:`set-up <setting_up>`
and tested.

Now read through the :doc:`basic concepts <basic_concepts>`
before trying out a :doc:`worked example <worked_example>`. After that,
browse through the sections listed in the :doc:`Guide <guide>`.
