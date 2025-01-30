=======================
Appendix I: Using Fonts
=======================

.. |dash| unicode:: U+2014 .. EM DASH SIGN

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

- *Ubuntu*  (technically, *Ubuntu Regular*)
- *Arial*
- *Verdana*
- *Courier New*
- *Times New Roman*
- *Trebuchet_MS*
- *Georgia*
- *Webdings*

If you are running on a Windows operating system, these fonts should already
be installed and usable.

On Ubuntu Linux these font files are typically installed into ``/usr/share/fonts``.


Using Additional Fonts
======================

It is possible to install additional fonts into an operating system. Once
installed, these could then be used in a :doc:`protograf <index>` script.

However, there are some limitations:

- The font **MUST** be a *TrueType* font, which will have a filename with a
  ``.ttf`` extension
- The font must be installed into the standard location for that operating
  system, so that it can be "auto-discovered"
- The font must be referred to correctly; for example, the ``Ubuntu`` font is
  not actually available as ``Ubuntu`` but rather as ``Ubuntu-L``, ``Ubuntu-R``
  and ``Ubuntu-M`` for the light, regular and medium styles. By default,
  :doc:`protograf <index>` will attempt to find and use the *regular* style
  if no plain version is available.

On an Ubuntu Linux machine, your new font file could be installed into
``./home/USERNAME/.local/share/fonts``.

Font Styles
-----------

Fonts can be created with a number of styles, including:

- light
- thin
- regular (the "default")
- medium
- black
- bold
- italic
- oblique (italic equivalent for sanserif fonts)

All of these styles require additional font files to be installed.

The style files usually have an appended suffix like *-Bold* or *B*.
:doc:`protograf <index>` will attempt to discover and install those extra
files, to create what is termed a "font family", but there is no guarantee it
will be able to do so!

Font Style Combinations
-----------------------

It is common for two of the styles - bold and italic - to be used together
with the default, or plain, version of the font.  There can also be a combined
version of these styles |dash| *BoldItalic* or *BoldOblique* |dash| that is
useful when both styles are applied.

When all these styles are available, they will be registered as being part of
the same family; internally the program's command to do so is:

    registerFontFamily(
        'Merriweather',
        normal='Merriweather-Regular',
        bold='Merriweather-Bold',
        italic='Merriweather-Italic',
        boldItalic='Merriweather-BoldItalic')

(This example assumes you would have downloaded and installed the font files
for the *Merriweather* font from https://fonts.google.com/specimen/Merriweather )

Font Filename
-------------

If :doc:`protograf <index>` is unable to "auto-discover" the font, but
you know the name, including the full path, of the font file, then you can
supply this directly to the ``Font`` command:

.. code:: python

    Font(face="BenKenobi", size=48, stroke=red, filename="/tmp/BKenobi.ttf")

Be aware that doing this makes your script less portable between machines,
as that same file may not be present on a different machine.


Font Resources
==============

Additional fonts are available from:

- https://www.dafont.com/
- https://fonts.google.com/ - also very useful explanations about fonts, and
  how to choose them
