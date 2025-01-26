=========================
Appendix III: Using Fonts
=========================

.. IMPORTANT::

   This section represents the **very** limited understanding of the program's
   author - certainly any feedback to help correct and make it clearer will be
   more than welcome!

The Basics
==========

Apart from the `Built-In Fonts`_, each time you want to use a different font
in your script, you first need to declare it.

If you are using the ``Text`` command, the font can be setup as follows:

.. code:: python

    Text("Hello World!", font_face="Arial", font_size=48, stroke=red)


If you want to set the font for a whole section of script, then using the
``Font`` command, you can setup as follows:

.. code:: python

    Font(face="Arial", size=48, stroke=red)

In this case, the properties are similar but the "*font_*" prefix is not
needed.

.. NOTE::

    Font face names, and their associated file names, should be considered
    as **case-sensitive**!


Built-In Fonts
==============

Because :doc:`protograf <index>` uses *ReportLab* to generate the PDF output,
it has access to the three "built-in" fonts supplied by it.

These are:

- *Times-Roman* - a basic serif font
- *Helvetica* - a basic sanserif font
- *Courier* - a basic fixed-width font

As far as possible, all examples supplied with :doc:`protograf <index>` make
use of these fonts, so that they can run anywhere.


Supplementary Fonts
===================

As suggested in :doc:`Setting Up <setting_up>` , if you're running on a Linux
operating system, you can consider using a command such as:

    sudo apt-get install ttf-mscorefonts-installer

In this case, when the ``Create`` command runs, it will automatically try to
register the following fonts:

- *Ubuntu*
- *Arial*
- *Verdana*
- *Courier New*
- *Times New Roman*
- *Trebuchet_MS*
- *Georgia*
- *Webdings*

If you are running on a Windows operating system, these fonts should already
be installed and usable.


Using Additional Fonts
======================

It is possible to install additional fonts into an operating system. Once
installed, these could be used in a :doc:`protograf <index>` script.

However, there are some limitations:

- The font **MUST** be a TrueType font, which will have a filename with a
  ``.ttf`` extension
- The font must be installed into the standard location for that operating
  system, so that it can be "discovered"
- The font must be referred to correctly; for example, the ``Ubuntu`` font is
  not actually available as ``Ubuntu`` but rather as ``Ubuntu-L``, ``Ubuntu-R``
  and ``Ubuntu-M`` for the light, regular and medium varieties.

It should also be noted that the ability of a font to display bold and italic
(or, for serif fonts, oblique) styles require additional font files to be
installed.  These files usually have an appended suffix like *Bold* or *B*.
:doc:`protograf <index>` will attempt to discover and install those extra
files, to create what is termed a "font family" but there is no guarantee it
will be able to do so!


Font Resources
==============
