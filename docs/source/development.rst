===========
Development
===========

.. |dash| unicode:: U+2014 .. EM DASH SIGN

These notes are aimed at those who might be developing the code further,
or who want to use :doc:`protograf <index>` as part of other Python
projects.


Coding
======

In general, follow the `Zen of Python <https://peps.python.org/pep-0020/>`_
|dash| which is much easier to say than do |dash| but also try to follow
the style of the code in the rest of the project.

Note, however, that this project "breaks" a few normal conventions:

- Use of ``global`` variables in the ``proto.py`` file
- Extensive use of ``**kwargs**`` for the various shapes which means that a user
  could pass in a key+value setting that simply gets ignored without raising an
  error; this could be improved by creating numerous subclasses with a more
  extensive inheritance framework, but these soon start getting tricky to
  juggle...
- Use of ``from protograf import *`` for running scripts; you could force a
  user to import only what they need but that makes it really tedious for them,
  and much harder to do if you're not a programmer!  If you are using this as
  part of another Python project, then of course you should follow the normal
  approach of only importing exactly what you need!

Code is formatted using ``black`` (https://black.readthedocs.io/) which is
triggered as a GitHub action  |dash| see the ``.github/workflows/`` directory.


Package Management
==================

Project packaging is handling via *poetry* (https://python-poetry.org/).  You
must have installed this before starting development. Follow the guides to
setup a virtual environment in which to work.

As you work, you can update the changes locally by running::

    poetry install

New package dependencies should be added via::

    poetry add MyNewPackage

Or perhaps with finer control over versions::

    poetry add MyNewPackage^3.1.4

Check existing dependencies via::

    poetry show

Update a patch version via::

    poetry version patch

Update a minor version via::

    poetry version minor


Releases on pypi
----------------

The software includes a GitHub workflow |dash| see the
``.github/workflows/`` directory |dash| which handles pushing new releases  onto pypi.

To trigger such an update, add a new version as above, and then tag and push::

    git tag 0.1.1
    git push origin --tags

If you check the *Actions* tab on the GitHub project page, you should now see
the workflow in action.

When complete, there should now be an updated version showing if you refresh
the home page of the project on https://pypi.org/.


Documentation
=============

Documentation is written in reStructuredText. Some helpful web resources:

- https://github.com/DevDungeon/reStructuredText-Documentation-Reference - guide
- https://docutils.sourceforge.io/docs/user/rst/quickstart.html - quick start
- https://docutils.sourceforge.io/docs/user/rst/quickref.html - detailed summary
- https://jwodder.github.io/kbits/posts/rst-hyperlinks/ - all about links
- https://docutils.sourceforge.io/docs/ref/rst/directives.html - directives

Some useful tools:

- https://github.com/retext-project/retext - a reStructuredText editor
- https://github.com/mgedmin/restview - a reStructuredText viewer in your browser
  (but currently does not support Sphinx directives)
- https://pypi.org/project/sphinx-view/ - a reStructuredText viewer in your browser
  that *does* support Sphinx directives (but is quite dated)
