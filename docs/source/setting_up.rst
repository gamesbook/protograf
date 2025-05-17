==========
Setting Up
==========

.. |dash| unicode:: U+2014 .. EM DASH SIGN

.. _table-of-contents-setup:

Table of Contents
=================

- `Outline`_
- `Python in 1 minute`_
- `Opening a Terminal`_
- `Installing Python`_

  - `Linux Users`_
  - `Windows Users`_
  - `Mac Users`_
- `Testing that Python is installed`_
- `Other Software Installs`_
- `Installing protograf`_
- `Checking that protograf works`_
- `Python in the cloud`_


Outline
=======
`↑ <table-of-contents-setup_>`_

There are four parts to being able to use :doc:`protograf <index>`
on your own machine:

1. Install the correct version of `Python <http://www.python.org>`_
2. Install and set-up **protograf**
3. Install a text editing program
4. Install a PDF viewer

Its possible that you may already have one or more of these programs installed,
but please follow the documentation here to ensure they will work with/for
**protograf**.


Python in 1 minute
==================
`↑ <table-of-contents-setup_>`_

Why do you need Python before starting?

When you work with Python, you do not create executable files, such as the
typical ``.exe`` ones you find on Windows (or ``.app`` on macOS). Instead,
Python itself is loaded and then it "runs" your Python file/script on your
behalf. So, running any Python scripts requires that you first install
Python itself.

Python is composed of many built-in libaries, or *packages*, each of which
handles some aspect of a program. Python also is designed to be extended by
adding-on additional packages written by other programmers; *PyMuPDF*, for
example, is one of those, as is **protograf**.  Python does not come with those
packages built-in |dash| you need to install them after Python itself has been
installed.

Installing Python packages is handled by a tool called ``pip`` |dash| the
Python Installation Package |dash| which is typically installed at the same
time as Python itself.

Opening a Terminal
==================
`↑ <table-of-contents-setup_>`_

In order to install Python and use **protograf**, you will need to use
a **command-line window** or **Terminal**.

The way that you open a terminal window depends on your operating system:

-  For Windows users - go to "Start -> Run" (On Windows 7 to 10, press
   "WindowsKey+R"), or use the search box at the bottom of the Start menu,
   and then enter ``cmd`` |dash| Windows should now show you the option to
   run a ``Command Prompt`` window.
-  For Mac OS X users - go to your Applications/Utilities folder and
   choose "Terminal".
-  For Linux users; you should already know how to open a Terminal!


Installing Python
=================
`↑ <table-of-contents-setup_>`_

**protograf** requires a device e.g. laptop or desktop |dash| but
probably not a smart phone |dash| that already has the correct version
of Python (version 3.13 or higher) installed.  This section guides you
through such an install.

.. NOTE::

    These are minimal guidelines; in case of any doubt or confusion, please
    refer to the documentation of the tools that are referenced here!


Linux users
-----------

You likely already have a version of Python installed.

To setup a new virtual environment to work with **protograf**, you can use
a modern tool such as ``uv``; see
https://ubuntushell.com/install-uv-python-package-manager/

You can then use ``uv`` to install an updated version of Python into a
virtual environment. After `opening a Terminal`_::

    uv venv --python 3.13

``uv`` has extensive documentation at https://docs.astral.sh/uv/

Windows Users
-------------

Option 1: uv
~~~~~~~~~~~~

If you do not already have Python installed, then a quick and easy way to
get going is to use ``uv``.

Follow the install guide ``uv`` |dash| see for example
https://docs.astral.sh/uv/getting-started/installation/#standalone-installer

After `opening a Terminal`_ use ``uv`` to install the right version of
Python in a virtual environment.

The example below assumes you are working as the user "Sam".

In the terminal window you have opened, you will see a prompt i.e.
text followed by small ``_``::

    c:\Users\Sam>

Now install Python by entering::

    uv venv --python 3.13

After a successful install, you will be prompted with::

    Activate with: .venv\Scripts\activate

You can activate the virtual environment by typing::

    .venv\Scripts\activate

And the prompt should change to::

    (Sam) C:\Users\Sam>

which indicates that the virtual environment is now ready for you to
install software and run Python scripts.

``uv`` has extensive documentation at https://docs.astral.sh/uv/

Option 2: miniconda
~~~~~~~~~~~~~~~~~~~

The *miniconda* software is also a fairly simple way of starting to use Python.

Follow https://docs.anaconda.com/miniconda/miniconda-install/ for instructions
on downloading and running the installer.

Make sure you choose a version that will install Python 3.13 or higher
(3.13, 3.14, etc.).

Follow their documentation there to ensure that Python is working after the
installation is complete.

Make sure you can use *miniconda* to setup and activate a new virtual environment.

Mac Users
---------

The program author has no access to a MacOS, and so cannot be sure this
software will work there.

It is suggested to follow the approach outlined for Windows and install
``uv``.

There is a helpful guide on working with Python from *pyLadies*; see:
http://www.pyladies.com/blog/Get-Your-Mac-Ready-for-Python-Programming/


Testing that Python is installed
================================

After `opening a Terminal`_, and activating the virtual environment::

   python --version

You should see something like::

   Python 3.13.1

The exact number after the "13" does not matter.

You can now close the command-line window.


Other Software Installs
=======================
`↑ <table-of-contents-setup_>`_

PDF Viewer
----------

You will also need a program that can display PDF files; for example,
*Adobe Acrobat* (cross-platform), or **Evince** (Linux), or **Preview**
(Mac), or **Foxit** (Windows).

Most modern web browsers should also be able to open and display PDF files.

.. HINT::

    While not a requirement, it appears that Sumatra PDF viewer |dash| available
    at https://www.sumatrapdfreader.org/download-free-pdf-viewer |dash|
    is a useful one for Windows users, as it supports "live reloading"
    i.e. each time you make changes to your **protograf** script the PDF
    will automatically refresh.

Core Fonts (optional)
---------------------

For Linux users, it is recommended that you install Microsoft’s Core
Fonts - see http://mscorefonts2.sourceforge.net/ |dash| Ubuntu users
can install these via::

   sudo apt-get install ttf-mscorefonts-installer

Text Editor
-----------

For Windows users, it is suggested that you install
`NotePad++ <https://notepad-plus-plus.org/>`_ which is the recommended
Windows editor for creating **protograf** scripts |dash| if you do not
already have a tool for editing Python scripts.

Installing **protograf**
==========================
`↑ <table-of-contents-setup_>`_

.. IMPORTANT::

    Windows users will need to install an additional program - a "DLL" -
    which is a required dependency.  Download the ``vc_redist.x64.exe`` file from
    https://learn.microsoft.com/en-gb/cpp/windows/latest-supported-vc-redist?view=msvc-170#latest-microsoft-visual-c-redistributable-version
    and do the install!

After `testing that Python is installed`_, you can install **protograf** itself
via ``pip``.

After `opening a Terminal`_, and activating the virtual environment::

   pip install protograf

If you are using ``uv``::

   uv pip install protograf


Checking that protograf works
=============================
`↑ <table-of-contents-setup_>`_

To now check that **protograf** works, you should create a small test
file.

Open your text editor and type |dash| or copy and paste |dash| the following,
making sure you do not have any spaces at the start of any line!::

   from protograf import *
   Create()
   Text(text="Hello World")
   Save()

.. HINT::

  If you're viewing this documentation on the *readthedocs* website, you
  can hover over the top-right corner of any colored block of text and
  click on the icon to automatically copy that block.

Save the file; call it *test.py*. The ``.py`` extension indicates that this
is a Python file |dash| this is useful but not absolutely essential!

Now use Python to "run" this file i.e. after `opening a Terminal`_, and
activating the virtual environment, you will need to change to the
directory in which the test file was created.

For example. on Windows, you may have saved the file in ``Documents``, so::

   (Sam) C:\Users\Sam>cd Documents

Now type::

   python test.py

and press the *Enter* key.

After the program runs, there should now be a new file called ``test.pdf``
that has been created in the same directory.

You should be able to open and view this PDF file via your `PDF viewer`_.
It should be a mostly blank, A4-sized page with the phrase *Hello World*
in a small, Helvetica font near the top-left.


Python in the cloud
===================
`↑ <table-of-contents-setup_>`_

If you do not want to install Python, you can try a cloud-based version.

You will need to register on  https://www.pythonanywhere.com/ and then
use the tools and infrastructure they provide.

.. HINT::

    The environment used for *pythonanywhere* is a Linux-based one
    and likely to be unfamiliar if you're a Windows user |dash| especially
    if you're not used to working via a "shell" in a Terminal, or
    command-line, interface.

*pythonanywhere* provides a terminal (``bash``) that you can use to install
Python packages via ``pip``.

You also have option to edit, or upload files |dash| such as **protograf**
scripts. Once scripts are available there, they can be run in the Terminal.

*pythonanywhere* has its own documentation to help you work further with it.
