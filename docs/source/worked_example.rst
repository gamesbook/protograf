==================================
Worked Example for a Deck of Cards
==================================

.. |dash| unicode:: U+2014 .. EM DASH SIGN

These examples assumes that you have set-up your computer with Python and
have tested to **check that you can create a test file which generates a
blank PDF**. If not, please first see the :doc:`Setting Up <setting_up>`
document.

It will also be helpful if you have read the
:doc:`Basic Concepts <basic_concepts>` section.  However, do note that
not all aspects of the examples shown here are described in depth, and
many of these will only become clear once you have read other parts of
the full documentation.

.. HINT::

   **Remember** when you create and edit your files, do **not** use a
   word processor such as "Word", "Pages" or "LibreOffice" - but a text
   file editor instead e.g. on Windows, use *NotePad* or
   `NotePad++ <https://notepad-plus-plus.org/>`_; and on OS X, use
   *TextEdit* or `CotEditor <https://coteditor.com/>`_.  A useful editor
   should be able to color-code your file to make it easier to work with.

A simple card deck example: Take 1
----------------------------------

Open up a new text file |dash| referred to as a **script** |dash|
with your text file editor and type the following, making sure that
each line starts **without** any blank spaces!

.. code:: python

   from protograf import *
   Create()
   Deck()
   Save()

As can be seen there are four lines in the file:

-  *Line 1* - this tells Python to access the functionality in
   **protograf**; every script you write **must** start with this line
-  *Line 2* - ``Create()`` tells **protograf** to setup an output PDF
   file in which this design of will be saved. Because no further
   information is given, the default values for sizes and colours will
   used, as well as the default page dimensions.
   Every script you write **must** have this line before *any* further
   **protograf** instructions/commands are supplied.
-  *Line 3* - ``Deck()`` means that **protograf** is defining a deck.
   Because there is no other information given, it will create the default
   number of cards |dash| *9* |dash| with each card having the same default size
   i.e. a "Poker" card size of 8.8 cm high and 6.3 cm wide.
-  *Line 4* - ``Save()`` gives the go-ahead to create the output file on
   disc. Usually, every script you write will have this as the last
   line.  If you don't have it, no file will be created.  The output file
   will be a PDF with the same name as your script (although with ``.pdf``
   extension instead.)

Now save the text file, for example, as ``cards1.py``. Then open a
command-line window (as described in :doc:`Setting Up <setting_up>`)
and change to the directory where the file is saved.

Type the following::

   python cards1.py

The output PDF file should now have been created, in the same directory
as your ``cards1.py`` file, called ``cards1.pdf``. If you open this in a
PDF reader program, you should see that it contains a set of 9 blank,
Poker-card sized, rectangular outlines (which we are calling "cards")
laid out in a grid on an A4-sized page.

.. NOTE::

    The default paper size for **protograf** is *A4* which is a standard
    ISO paper size of about 21 x 30 centimetres (approximately 8.3 x 11.7
    inches), chosen because this is most common type of paper encountered
    globally.


A simple card deck example: Take 2
----------------------------------

Open up a new text file with your text file editor and type in the
following (again, remember to start each line with **NO** blank
spaces):

.. code:: python

   from protograf import *

   Create(paper="A3", filename="example2.pdf")
   Deck()
   Save()

You can see that the ``Create()`` instruction has now been expanded with
a list of new details appearing inside the brackets. These items are
called *properties* and each property is separated by a ",". Each
**property** is defined by a name, followed by an "=" (equals) sign, and
then a value of some kind.

In this case, the ``paper`` property has been set equal to a value of
*"A3"* which is a standard ISO paper size of about 30 x 42 centimetres
(approximately 11.7 x 16.5 inches).  Also, a specific file name has been
chosen for the PDF that will be created for the script; in this case
it is ``example2.pdf``.

A blank line has been added before the ``Create()`` instruction. Adding
blank lines helps make your file more readable, but **protograf** does
*not* use or require them.

Now save this new file, for example, as ``cards2.py``. Open a
command-line window and change to the directory where the file has been
saved.

Type the following::

   python cards2.py

An output PDF file should now have been created in the same directory as
your ``cards2.py`` file - it will be called ``example2.pdf``. It should
contain a set of 9 blank cards appearing in the top half of an A3-sized
page.

.. NOTE::

    Drawing in **protograf** always starts at the top-left
    corner and proceeds left-to-right and then downwards on the page.

A simple card deck example: Take 3
----------------------------------

If you have followed the above examples, you will know how to create the
cards file, and how to generate and display the output PDF file. This
script example will therefore *only* show the text in the file you create,
and discuss what the resulting output should look like.

Create this text in a file called ``cards3.py``:

.. code:: python

   from protograf import *

   Create(filename='example3.pdf', offset=0.5)

   # deck design: a "template" that all cards will use
   Deck(
       cards=50,
       height=5,
       width=3.8,
       fill="#702EB0")

   # create the output card file, using the card 'deck'
   Save()

A ``Deck()`` instruction allows you to define the details for every card
that will appear in the deck, such as its height, width and the colour
to fill it in.

Because there are many properties in it, the ``Deck()`` instruction has
been split over multiple lines to make it easier to read |dash| you need
to make sure that such a split happens directly *after a comma*, and
**not** in the middle of a word or a property setting.

When you split an instruction, make sure that there are one or more
spaces at the start of the continuation lines; it's often helpful to
start the next line indented by four (4) spaces.

In this ``Deck``, the number of cards has been set to 50. The size of
the cards in the deck have been changed to be 5cm high and 3.8cm wide.
The fill color is defined by a **hexadecimal** value - this sets the
red, green and blue components that make up a color. In this case, we
might see the color as a shade of "purple".

In this script, the lines shown starting with a ``#`` are called
**comments** |dash| these will be ignored by **protograf** but are included
to provide some more explanation as to what the next line, or lines, are
doing. You could also add lines at the start of a script to define
what its purpose is.

The resulting ``example3.pdf`` will show two pages of small, blank,
purple cards, each card being approximately 2 inches by 1.5 inches,
with 25 cards per page, for a total of 50 cards.

.. NOTE::

   **protograf** will do the calculation for you on how
   many cards will fit on page to make up the total number of cards
   for the deck, based on the size of cards you want and how large
   the page is.

A simple card deck example: Take 4
----------------------------------

This example will only show the text in the file you create, and then
discuss the new kinds of details added to it, as well as what the
resulting output should be.

Here we are now providing information to actually display on the cards.

Create this text in a file called ``cards4.py``:

.. code:: python

   from protograf import *

   # create the output card file and page details
   Create(filename='example4.pdf', offset=0.5)

   # set deck design; use a white border instead of default black
   Deck(cards=25,
        height=5,
        width=3.8,
        fill="skyblue",
        stroke="white")

   # customize a single card (number 25) in the deck with text;
   # the text is 1.9cm from the card left & 3cm from its top;
   # the font size has been set to 28pt
   Card("25", text(text="25!", x=1.9, y=3.0, font_size=28))

   # switch the font in use; set it's face, size and stroke color
   Font("Times-Roman", size=14, stroke="red")

   # create more text; display it using the new font
   mytext = text(text="I'm on cards 1-9", x=1.9)

   # specify a range of cards that will contain 'mytext'
   Card("1-9", mytext)

   # save to file
   Save()

For this deck we are are setting card colors by choosing their names
from a a set of pre-defined colors available in **protograf** |dash|
these might be useful if they match your needs.

A new instruction, called ``Card()``, has been added. As might be
expected, this specifies what will actually appear on a given card or
cards apart from just the color. The number just after the ``(`` bracket
is the card number or, if there are multiple cards, then the first and
last card number separated by a dash ("-").

In the line starting ``Card("25"``, you can see that Card#25 will
contains the text ``25!`` in a large font size, using the default
font face of ``Helvetica``.

You can change the default **Font** in use by setting the properties of a
``Font``. This can include its name |dash| here it is ``Times-Roman`` |dash|
its size in *points*, and its color |dash| set by the **stroke** property.

This script also shows the use of a **reference** |dash| a reference is
just a name, followed by an "=" sign, and then an instruction of some kind;
in this script the reference is named ``mytext`` and it is referring to
text placed at a location.

You can also see that the ``mytext`` reference is used further on when
specifying the design for cards numbered ``1`` to ``9`` (``Card("1-9"``).

The resulting ``example4.pdf`` file will show a page of small,
white-bordered, light-blue cards - with the same text appearing on cards
one to nine, but with different text on the last card (number ``25``).

Continuing on …
---------------

If you are interested in carrying on with design of card decks, then the
section on :doc:`Card Decks <card_decks>` will be helpful for you.
Please bear in mind that that section assumes you are familiar with **all**
the :doc:`basic concepts <basic_concepts>` and program usage described in
earlier sections.

There are also card-related examples in the
:doc:`Available Examples <examples/index>` section.
