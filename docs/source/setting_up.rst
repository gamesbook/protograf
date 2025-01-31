==========
Setting Up
==========

.. |dash| unicode:: U+2014 .. EM DASH SIGN

.. _table-of-contents:

Table of Contents
=================

- `Outline`_
- `Python in 1 minute`_
- `Installing Python`_
- `Other Software Installs`_
- `Installing protograf`_
- `Checking if protograf works`_
- `Python in the cloud`_


Outline
=======
`↑ <table-of-contents_>`_

There are four parts to being able to use :doc:`protograf <index>`
on your own machine:

1. Install the correct version of `Python <http://www.python.org>`_
2. Install and set-up **protograf**
3. Install a text editing program
4. Install a PDF viewer (e.g. *Adobe Acrobat*)

Its possible that you may already have one or more of these programs installed.


Python in 1 minute
==================
`↑ <table-of-contents_>`_

Why do you need Python before starting?

When you work with Python, you do not create executable files, such as the
typical `.exe` ones you find on Windows (or `.app` on macOS). Instead, Python
itself is loaded and then it "runs" your Python file/script (the `.py` ones)
on your behalf.  So, running any Python scripts requires that you first install
Python itself.

Python is composed of many built-in libaries, or *packages*, each of which
handles some aspect of a program. Python is designed to be extended by adding
on additional packages written by other programmers; ``ReportLab``, for example,
is one of those, as is **protograf**.  Python does not come with those packages
built-in |dash| you need to install them after Python itself has been installed.

Installing Python packages is handled by a tool called ``pip`` |dash| the
Python Installation Package |dash| which is typically installed at the same
time as Python itself.


Installing Python
=================
`↑ <table-of-contents_>`_

**protograf** requires a device e.g. laptop or desktop (but probably
not a smart phone) that already has the correct version of Python
(version 3.13 or higher) installed.

Linux users
-----------

You likely already have a version of Python installed.

To setup a new virtual environment to work with **protograf**, you can use
a modern tool such as ``uv``; see
https://ubuntushell.com/install-uv-python-package-manager/

You can then use ``uv`` to install an updated version of Python as well as this
virtual environment; for example::

    uv venv --python 3.13

New packages can be installed using ``uv`` with ``pip``::

    uv pip install reportlab

``uv`` has extensive documentation at https://docs.astral.sh/uv/

Windows and mac Users
---------------------

If you have no experience of working with Python, then "miniconda" is a fairly
simple way of using Python; follow
https://docs.anaconda.com/miniconda/miniconda-install/ for instructions on
downloading and running the installer. Make sure you choose a version that will
install Python 3.13 or higher (3.13, 3.14, etc.).  Again, follow the
documentation there to ensure that Python is working after the installation
is complete.

Alternatively, install ``uv`` |dash| see for example
https://docs.astral.sh/uv/getting-started/installation/#standalone-installer

and then use ``uv`` to install the right version of Python in a
virtual environment; for example::

    uv venv --python 3.13

New packages can be installed using ``uv`` with ``pip``::

    uv pip install reportlab


Once Python is installed and working, you can install new packages for it using
``pip``.

Alternative Options
~~~~~~~~~~~~~~~~~~~
Another very detailed and useful guide to installing Python on Windows is at:
https://www.tomshardware.com/how-to/install-python-on-windows-10-and-11

This guide will also take you through installing
`NotePad++ <https://notepad-plus-plus.org/>`_ which is the recommended
Windows editor for creating **protograf** scripts.

For MacOS, there is a helpful guide on working with Python from
*pyLadies*; see:
http://www.pyladies.com/blog/Get-Your-Mac-Ready-for-Python-Programming/

Test that Python is installed
-----------------------------

In order to test that Python is installed, start a **command-line
window**. The way you do this depends on your operating system.

-  For Windows users - go to "Start -> Run" (On Windows 7 to 10, press
   "WindowsKey+R" or use the search box at the bottom of the Start menu)

-  For Mac OS X users - go to your Applications/Utilities folder and
   choose "Terminal".

-  For Linux users; you should already know how to open a Terminal!

When the command-line window appears, type::

   python --version

You should see something like::

   Python 3.13.1

The exact number after the "13" does not matter.

You can now close the command-line window.


Other Software Installs
=======================
`↑ <table-of-contents_>`_

PDF Viewer
----------

You will also need a program that can display PDF files; for example,
*Adobe Acrobat* (cross-platform), or **Evince** (Linux), or **Preview**
(Mac), or **Foxit** (Windows). Most modern web browsers should also be
able to open and display PDF files.

Core Fonts (optional)
---------------------

For Linux users, it is recommended that you install Microsoft’s Core
Fonts - see http://mscorefonts2.sourceforge.net/ |dash| Ubuntu users
can install these via::

   sudo apt-get install ttf-mscorefonts-installer


Installing **protograf**
==========================
`↑ <table-of-contents_>`_

The simplest way to install **protograf** itself is via ``pip``.

Open a command-line window (see the section `Test that Python is installed`_)
and::

   pip install protograf

If you are using ``uv``::

   uv pip install protograf


Checking if **protograf** works
=================================
`↑ <table-of-contents_>`_

To now check that ``protograf`` works, you should create a small test
file.

Open your text editor and type |dash| or copy and paste |dash| the following,
making sure you do not start any line with spaces!::

   from protograf import *
   Create()
   Text(text="Hello World")
   Save()

Save the file; call it *test.py*. The ".py" indicates that this a Python
file |dash| this is useful but not essential!

Now use Python to "run" this file.

By "run", its meant that you open a command-line window and change to the
directory in which the test file was created, for example on Windows::

   cd C:/

If you're not sure about the "command-line" part, then see the section
`Test that Python is installed`_.

Now type::

   python test.py

and press the *Enter* key.

There should now be a new file called ``test.pdf`` in the same
directory.

You should be able to open and view this PDF file via your PDF viewer.
It should be a mostly blank, A4-sized page with the phrase *Hello World*
in a Helvetica font near the bottom-left.


Python in the cloud
===================
`↑ <table-of-contents_>`_

If you do not want to install Python, you can try a cloud-based version.

You will need to register on this site: https://www.pythonanywhere.com/ and
use the tools and infrastructure they provide.

.. HINT::

    The environment used for `pythonanywhere` is a Linux-based one
    and likely to be unfamiliar if you're a Windows user |dash| especially
    if you're not used to working via a "shell" in a terminal, or
    command-line, interface.

*pythonanywhere* provides a terminal (`bash`) that you can use to install Python
packages via `pip` and the option to upload files - such as **protograf**
scripts. Once scripts are uploaded there, they can be run in the terminal.

*pythonanywhere* has its own documentation to help you work further with it.
