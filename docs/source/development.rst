========================
Development of protograf
========================

.. |dash| unicode:: U+2014 .. EM DASH SIGN
.. |check| unicode:: U+2610 .. BALLOT BOX

These notes are aimed at those who might be developing the
`protograf code <https://github.com/gamesbook/protograf>`_ further,
or who just want to use :doc:`protograf <index>` as part of other Python
projects.

.. _table-of-contents-dev:

- `Coding`_
- `Package Management`_
- `Documentation`_

Coding
======
`↑ <table-of-contents-dev_>`_

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
  approach of only importing **exactly** what you need!

Code is formatted using ``black`` (https://black.readthedocs.io/) which is
triggered as a GitHub action |dash| see the ``.github/workflows/`` directory.


Package Management
==================
`↑ <table-of-contents-dev_>`_

Project packaging is handling via *poetry* (https://python-poetry.org/).  You
must have installed this before starting development. Follow the guides to
setup a virtual environment in which to work.

Poetry Workflow
---------------

As you work, you can update the changes locally by running::

    poetry install

New package dependencies should be added via::

    poetry add MyNewPackage

Or perhaps with finer control over versions::

    poetry add MyNewPackage^3.1.4

Check existing dependencies via::

    poetry show

Upgrade a dependency via::

    poetry update MyExistingPackage

Update a patch / feature version (the most common case) via::

    poetry version patch

Update a minor version via::

    poetry version minor

Update a major version via::

    poetry version major


Examples:

======= ======= =======
type 	before 	after
======= ======= =======
patch 	4.1.6 	4.1.7
minor 	2.1.4 	2.2.0
major 	1.3.2 	2.0.0
======= ======= =======

Releases to pypi
----------------

The software includes a GitHub workflow |dash| see the ``.github/workflows/``
directory |dash| which handles pushing new, tagged releases onto
https://pypi.org for distribution.

Once all code changes have been made and tested |dash| all examples must
run as normal |dash| then a new version can be released.

Follow this process:

- |check| Format primary code with black (``black protograf``)
- |check| Finalise release date and notes in ``CHANGES.txt``
- |check| Ensure all the examples can be run by using shell script(s)
- |check| Update the ``examples.zip`` file with latest example code
  (remove all PDF in examples/ except ``colorset`` and ``colorset_svg``;
  and also delete the ``temp`` directory)
- |check| Update the ``release`` in ``docs/source/conf.py``
- |check| Update the ``__version_info__`` in ``_version.py``
- |check| If working in a branch, now merge changes into master
- |check| Ensure you are on the ``master`` branch and pull changes
- |check| Update the version using poetry e.g. ``poetry version patch``
- |check| Git commit and push all these changes to GitHub
- |check| Add a tag that matches the poetry version e.g. ``git tag 0.1.2``
- |check| Push tag to GitHub i.e. ``git push origin --tags``

If you check the *Actions* tab on the GitHub project page, you should now see
the workflow in action.

When complete, there should now be an updated version showing, if you do a
refresh of the home page of the project at https://pypi.org/project/protograf/

Working with latest
-------------------

If you're just interested in installing the latest version via ``pip``,
then use::

    pip install git+https://github.com/gamesbook/protograf

Or ``uv pip install git+https://github.com/gamesbook/protograf`` if using
``uv``.


Documentation
=============
`↑ <table-of-contents-dev_>`_

Documentation is written in reStructuredText and hosted on *ReadTheDocs*
at https://app.readthedocs.org/projects/protograf/

Every time you push a commit to GitHub, the documentation workflow |dash|
see the ``.github/workflows/`` directory |dash| will trigger a build,
which can be accessed here:
https://app.readthedocs.org/projects/protograf/builds/


Documentation Notes
-------------------

Some helpful reStructuredText web resources:

- https://github.com/DevDungeon/reStructuredText-Documentation-Reference - guide
- https://docutils.sourceforge.io/docs/user/rst/quickstart.html - quick start
- https://docutils.sourceforge.io/docs/user/rst/quickref.html - detailed summary
- https://jwodder.github.io/kbits/posts/rst-hyperlinks/ - all about links
- https://docutils.sourceforge.io/docs/ref/rst/directives.html - directives

Some useful tools:

- https://github.com/retext-project/retext - a reStructuredText editor
- https://github.com/mgedmin/restview - a reStructuredText viewer in your browser;
  it currently does **not** support Sphinx directives
- https://pypi.org/project/sphinx-view/ - a reStructuredText viewer in your browser
  that **does** support Sphinx directives (but is quite dated)
