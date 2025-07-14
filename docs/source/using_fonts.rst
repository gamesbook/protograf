==============================
Appendix I: Working with Fonts
==============================

.. |dash| unicode:: U+2014 .. EM DASH SIGN

.. IMPORTANT::

   This section represents the **very** limited understanding of the program's
   author - certainly any feedback to help correct and make it clearer will be
   more than welcome!

.. _table-of-contents-fonts:

- `The Basics`_
- `Built-In Fonts`_
- `Using Additional Fonts`_
- `Supplementary Fonts`_
- `Word Processor fonts vs protograf`_
- `External Font Resources`_


The Basics
==========
`↑ <table-of-contents-fonts_>`_

Apart from the `Built-In Fonts`_, each time you want to use a different font
in your script, you'll first need to declare it.

If you are using the ``Text`` command, the font can be setup as follows:

.. code:: python

    Text("Hello World!", font_name="Arial", font_size=48, stroke="red")

If you do not supply the font properties, they will default to:

- *font_name* - Helvetica
- *font_size* - 12 (points)
- *stroke* - black

If you want to set the font for a whole section of script, then using the
``Font`` command you can set this up as follows:

.. code:: python

    Font(name="Arial", size=48, stroke="red")

In this case, the properties are similar but the "*font_*" prefix is not
needed.

.. NOTE::

    Font names, and their associated file names, should be considered
    as **case-sensitive**!


.. _builtin-fonts:

Built-In Fonts
==============
`↑ <table-of-contents-fonts_>`_

Because :doc:`protograf <index>` uses *PyMuPDF* to generate the PDF output,
it has access to these "built-in" fonts.

These are:

- *Times-Roman* - a basic serif font
- *Helvetica* - a basic sanserif font
- *Courier* - a basic fixed-width font
- *Symbol* - a variety of custom lettering
- *ZapfDingbats* - a variety of "dingbats" (mini-images)

As far as possible, all examples supplied with :doc:`protograf <index>` make
use of these fonts, so that they can be run and used anywhere.

.. NOTE::

    Be aware that some PDF viewers may not render some, or all, of the
    characters when using *Symbol* or *ZapfDingbats*. Also, the glyph
    (visual) images will be specific to every viewer.

CJK Fonts
---------

CJK fonts (China, Japan, Korea) **may** be available and installed on some
machines, depending on the OS and the PDF viwer in use.  If they are, they
can be referred to as follows:

- *Heiti* - simplified Chinese
- *Song* - simplified Chinese (serif)
- *Fangti* - traditional Chinese
- *Ming* - traditional Chinese (serif)
- *Gothic* - Japanese
- *Mincho* - Japanese (serif)
- *Dotum* - Korean
- *Batang* - Korean (serif)


.. _additionalFonts:

Using Additional Fonts
======================
`↑ <table-of-contents-fonts_>`_

It is possible to install additional fonts into an operating system. Once
installed, these could then be used in a :doc:`protograf <index>` script.

However, there are some limitations:

- The font should be installed into the standard location(s) for that operating
  system, so that it can be "auto-discovered".
- The font must be referred to correctly; for example, the ``Ubuntu`` font is
  not actually available as ``Ubuntu`` but rather as ``Ubuntu-L``, ``Ubuntu-R``
  and ``Ubuntu-M`` for the light, regular and medium styles.

On an Ubuntu Linux machine, your new font file could be installed into the
``/home/USERNAME/.local/share/fonts`` directory.


Font Registration
-----------------

The first time that a non-default font |dash| one that is installed specifically
on your machine |dash| is referred to, :doc:`protograf <index>` will need to
check all available font files to find it - this can take some time!

After this, a copy of all the fonts' information is stored in a single file in
the settings location used by  :doc:`protograf <index>` (usually in a
sub-directory called ``.protograph`` located in your home directory). This
will speed up the font checking process significantly for future.

However, if you later on install new font(s) onto your machine, you will need
to force the fonts information file to be recreated so it has access to the
new font(s).

Use the property ``cached_fonts=False`` in the script's ``Create`` command e.g.

.. code:: python

    Create(
        cached_fonts=False
    )

Alternatively, you can also used the ``--fonts`` option when using Python
to process your script:

.. code::

    python --fonts myscript.py

In either case, you should get feedback from the script about this process:

.. code::

    FEEDBACK:: Setting up fonts ... ... ... please be patient!


Common Font Styles
------------------

In addition to a font's default appearance |dash| sometimes termed
*regular* |dash| a font often has bold or italic |dash| sometimes termed
*oblique* |dash| styling that can be used together with this default.

There can also be a combined version of these styles |dash| for example,
*BoldItalic* or *BoldOblique* |dash| that is useful when both styles must be
applied together.

These files for these styles usually have an appended suffix like *-Bold* or
*B*. :doc:`protograf <index>` will attempt to discover and register both bold
and italic files, to create what is termed a "font family", but there is no
guarantee that all these files exist for every family!

When any or all of these styles are accessed, they will be registered as
being part of the same "font family"; and the command to make the family
available is:

.. code:: python

    Font(name='Merriweather')

(This example assumes you would have downloaded and installed the font files
for the *Merriweather* font from https://fonts.google.com/specimen/Merriweather )

If you need to use a specific style for a text box, append the style to the
font's family name; for example:

.. code:: python

    Text(text='Hello World', font_name="Merriweather-Bold")


.. _supplementaryFonts:

Supplementary Fonts
===================
`↑ <table-of-contents-fonts_>`_

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


Word Processor fonts vs protograf
=================================
`↑ <table-of-contents-fonts_>`_

In some cases, you'll notice that a font can be displayed with bold or
italic styling in a word processor, even though it cannot be displayed the
same way in :doc:`protograf <index>`.  The reason is that *PyMuPDF*
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
`↑ <table-of-contents-fonts_>`_

Additional fonts are available from:

- https://www.dafont.com/ - some free to use and some have specific licenses
- https://fonts.google.com/ - licensed under SIL Open Font License (OFL) - see
  https://openfontlicense.org/

As always, please check for yourself the details of licenses and restrictions
associated with any fonts you choose to use.
