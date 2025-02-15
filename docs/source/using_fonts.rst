==============================
Appendix I: Working with Fonts
==============================

.. |dash| unicode:: U+2014 .. EM DASH SIGN

.. IMPORTANT::

   This section represents the **very** limited understanding of the program's
   author - certainly any feedback to help correct and make it clearer will be
   more than welcome!

.. _table-of-contents:

Table of Contents
=================

- `The Basics`_
- `Built-In Fonts`_
- `Supplementary Fonts`_
- `Using Additional Fonts`_
- `Word Processor fonts vs protograf`_
- `External Font Resources`_


The Basics
==========
`↑ <table-of-contents_>`_

Apart from the `Built-In Fonts`_, each time you want to use a different font
in your script, you'll first need to declare it.

If you are using the ``Text`` command, the font can be setup as follows:

.. code:: python

    Text("Hello World!", font_name="Arial", font_size=48, stroke=red)

If you want to set the font for a whole section of script, then using the
``Font`` command you can set this up as follows:

.. code:: python

    Font(name="Arial", size=48, stroke=red)

In this case, the properties are similar but the "*font_*" prefix is not
needed. The ``Font()`` command also has some useful extra properties,
which are described below.

.. NOTE::

    Font names, and their associated file names, should be considered
    as **case-sensitive**!


Built-In Fonts
==============
`↑ <table-of-contents_>`_

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
`↑ <table-of-contents_>`_

As suggested in :doc:`Setting Up <setting_up>` , if you're running on a Linux
operating system, you can consider using a command such as:

    sudo apt-get install ttf-mscorefonts-installer

In this case, when the ``Create`` command runs, it will automatically try to
register the following fonts:

- *Arial*
- *Verdana*
- *Courier New*
- *Times New Roman*
- *Trebuchet MS*
- *Georgia*
- *Webdings*

If you are running on a Windows operating system, these fonts should already
be installed and usable.

On Ubuntu Linux these font files are typically installed into the
``/usr/share/fonts`` directory.

If you do not install these fonts, or have them already installed, you may
see a warning message every time you run a script:

    WARNING:: Unable to register the MS font(s): Arial, Verdana, Courier New, Times New Roman, Trebuchet MS, Georgia, Webdings


Using Additional Fonts
======================
`↑ <table-of-contents_>`_

It is possible to install additional fonts into an operating system. Once
installed, these could then be used in a :doc:`protograf <index>` script.

However, there are some limitations:

- The font **MUST** be a *TrueType* font, which will have a filename with a
  ``.ttf`` extension.
- The font should be installed into the standard location for that operating
  system, so that it can be "auto-discovered".
- The font must be referred to correctly; for example, the ``Ubuntu`` font is
  not actually available as ``Ubuntu`` but rather as ``Ubuntu-L``, ``Ubuntu-R``
  and ``Ubuntu-M`` for the light, regular and medium styles.  By default,
  :doc:`protograf <index>` will attempt to find and use the *regular* style
  if no plain version is available.

On an Ubuntu Linux machine, your new font file could be installed into the
``/home/USERNAME/.local/share/fonts`` directory.

.. HINT::

    There are online tools that will convert different font types |dash| for
    example, from OpenType to TrueType font. Please ensure that you adhere to
    the restrictions imposed by the font's license.

Common Font Styles
------------------

In addition to a font default appearance - sometimes termed *Regular* - a
font often has bold or italic styling that can be used together
with this default.

There can also be a combined version of these styles |dash| *BoldItalic* or
*BoldOblique* |dash| that is useful when both styles are applied.

These files for these styles usually have an appended suffix like *-Bold* or
*B*. :doc:`protograf <index>` will attempt to discover and install both bold
and italic files, to create what is termed a "font family", by trying out
different combinations of names and abbreviations, as well as different name
separators, but there is no sure guarantee that it will be able to do so!

When any or all of these styles can be accessed, they will be registered as
being part of the same "font family"; internally the program's command to do
this is:

.. code:: python

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
you know the path where the font file exists, then you can supply the
*directory* property to the ``Font`` command:

.. code:: python

    Font(face="BenKenobi", size=48, stroke=red, directory="/tmp/")

Be aware that doing this makes your script less portable between machines,
as that same file may not be present in the same directory on a different
machine.

Additional Font Styles
----------------------

Fonts can also be created with a number of additional styles, including:

- light
- thin
- medium
- dark
- black

All of these styles require additional font files to be installed.

To use such a style |dash| and its associated file |dash| you need supply
the *style* property to the ``Font`` command:

.. code:: python

    Font(face="Skywalker", size=48, stroke=red, style="Dark")


Word Processor fonts vs protograf
=================================
`↑ <table-of-contents_>`_

In some cases, you'll notice that a font can be displayed with bold or
italic styling in a word processor, even though it cannot be displayed the
same way in :doc:`protograf <index>`.  The reason is that *ReportLab*
does not create an "artificial" font style if it cannot find a matching
file for italic or bold version of the font.

The long answer was supplied in a Reddit post
(https://www.reddit.com/r/fonts/comments/1dzlhl0/) which is
paraphrased below:


*Question:* Why do some fonts have a separate "bold" or "italics" version, when
you can just  format the main font for the same effect? When I download a new
font, there's often a few variants included in the ZIP file, most commonly an
Italic version & Bold version. But whenever I install just the base font and
test if I can italicize/bolden it, it works just fine - and looks the same as
the standalone italic/bold versions.

*Answer:* Depending on the app you’re using, selecting bold or italic will
automatically switch to the bold or italic version of the font. If the app
doesn’t automatically switch it might **artificially** bold the font or slant
it to be italic.  There's also a big difference between a word processor app
putting a generic slant (for italics) or thickness (for bold) on the letters,
and the actual font created by designers having considered and crafted what
the font should look like in various forms. So, they don't look at all the
same. Set them really large, and you'll see the difference.


External Font Resources
=======================
`↑ <table-of-contents_>`_

Additional fonts are available from:

- https://www.dafont.com/
- https://fonts.google.com/ - also has very useful explanations about fonts and
  how to choose them
