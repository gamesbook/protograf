=========================
A Rationale for protograf
=========================

.. |dash| unicode:: U+2014 .. EM DASH SIGN
.. |check| unicode:: U+2610 .. BALLOT BOX

Why do this?
============

I realize that there are many software programs out there that are used for
creating graphics and layouts for games, some of which are very sophisticated
indeed; for example, Photoshop, Inkscape as well as various ones designed for
the Mac which obviously excels in this field.

However for someone like myself, who is not a graphics designer and doesn't
want to spend time learning all the ins-and-outs of these programs, I wanted
a tool that was fairly flexible but still in line with my own capabilities
and ambitions.

To be clear: *protograf* is not a tool that in any way competes with
full-scale graphics or art programs, and if you already know and use such
programs, you may just want to skip this one...

How does this work?
===================

As a programmer, I'm used to the idea of writing scripts to generate an output
and so, given my familiarity with Python, a language which has access to
numerous libraries covering a wide range of domains, it made sense for me to
pick this tool to undertake the task.

The code is publicly available on GitHub
(https://github.com/gamesbook/protograf) and so can be used (or reused)
by anyone with Internet access.

If something happens to me such that I cannot work on it any more, anyone
else is welcome to continue with it.

What does it do?
================

*protograf* is essentially a Python package that allows you to write a script
that can generate components of a game's graphical components, layer by layer.

*protograf* is built on top of the PyMuPDF Python library which provides the
underlying routines that allows a Python program to draw vector graphics and
generate a PDF output (or export to PNG/SVG/GIF images).

*protograf* provides a set of commands that will draw graphics - these are
shapes such as circles, rectangles, stars etc. - as well as lines and text.
Each of these can be customized in terms of their color, size, shape etc.
From these primitive graphics, more complex ones can be built up.

*protograf* provides acommands to allow to layout shapes onto various
"virtual" grids.

*protograf* can also generate cards, using data from Excel or CSV files,
or other sources such Google Sheets or the BGG API. There is a strong emphasis
on hexagons and hexagonal grids, as I just really like working with this
particular shape.

*protograf* is not in any way at a "professional software level" for creating
production-ready graphics and does *NOT* handle "special effects" such kerning,
skewing, image tiling, gradient colors, text-effects (e.g. drop shadows; 3D),
 etc. etc.
