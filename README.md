# protograf

![protograf](logo.png "protograf logo")

__protograf__ is a utility written in Python for designing and creating
simple, regular, graphical outputs in PDF (or PNG/GIF/SVG) format via a script.

__protograf__  has been primarily created to handle the prototyping of cards,
counters, tiles and boards for board games, including hexagonal grids, but can
also be used for creating any simple design that has regular or repetitive
elements; typically a mix of graphics and text.

> You do not need to know the Python language to be able to use __protograf__
> but you do need Python installed on your machine!

## :notebook: Documentation

The online documentation for __protograf__ is available at
[Read the Docs](https://protograf.readthedocs.io/);
its highly recommended to read the sections in the order presented in the
[Guide](https://protograf.readthedocs.io/en/latest/guide.html).

If you're not familiar with any kind of programming or scripting, you should
at least read some of the introductory sections, and especially the
[installation](https://protograf.readthedocs.io/en/latest/setting_up.html)
before proceeding...

## :hammer_and_wrench: Requirements

__protograf__ requires Python (version of 3.13 or higher) to be installed
and running on your machine.

If this is **not** your current Python version, or Python is not installed on
your machine, may want to [install uv](https://docs.astral.sh/uv/getting-started/installation/)
which is a cross-platform tool able to [install Python](https://docs.astral.sh/uv/guides/install-python).

If using [uv](https://docs.astral.sh/uv/), it is recommended to also create and use a
[virtual environment](https://docs.astral.sh/uv/pip/environments/#creating-a-virtual-environment).

## :toolbox: Quick Start (for the impatient)

Assuming that Python 3.13 or higher is installed on your machine, you can then
install __protograf__ via:
```
pip install protograf
```
or, if using [uv](https://docs.astral.sh/uv/):
```
uv pip install protograf
```
To check that __protograf__ is working, you can use one (or more) of
the files from any of the various
[examples](https://github.com/gamesbook/protograf/blob/master/examples/)
sub-directories.

As a quick test, make a copy of `example1.py` script from the `examples/manual`
directory. To do so, open the
[example1.py](https://github.com/gamesbook/protograf/blob/master/examples/manual/example1.py)
link in your browser, click on the `Raw` button (near the top right), and then
save the web page as a file into a local directory on your machine.

Open a command-line window (also known as a  *terminal* or a *console*), change to the
directory where you saved the above file and type:
```
python example1.py
```
and press the `Enter` key.

This script is very simple - it just contains these lines:
```
# `example1` script for protograf
# Written by: Derek Hohls
# Created on: 29 February 2016
from protograf import *
Create()
Save()
```
and is designed to produce a single, blank, A4-sized page in a PDF file.

It should create an output file called `example1.pdf`, which will appear in the
same directory as the script. You should be able to open and view this file using
any PDF-capable program or application. (If you run the script in a Python shell,
the output file will be called `test.pdf`.)

If this works, then download and try out other scripts from any of the `examples`
sub-directories (**note** some examples may require additional files such as
images, CSV files, or spreadsheets). You can download all the examples in a single
[ZIP file](https://github.com/gamesbook/protograf/blob/master/examples.zip).

If it does not work, you may want to look at more detail provided in the
[installation](https://protograf.readthedocs.io/en/latest/setting_up.html)
guide.

## :handshake: Contributions

Please see the [list of contributors](CONTRIBUTORS.txt).

## :game_die: Potential Features

These features are **not** guaranteed to be implemented; they just represent
current / potential areas of work or idea development.

* [ ] New Shapes:
    * [ ] Diamond shape
    * [ ] Parallelogram shape
    * [ ] Cross shape
    * [ ] Pod shape
* [ ] Common objects:
    * [ ] CompassRose (replace Compass Shape)
    * [ ] Cube (Rhombus composite; "3D")
    * [ ] Domino (DotGrid inside Rectangle outline)
    * [ ] Die (Rectangle with DotGrid)
    * [ ] Meeple (Polyshape with Arcs)
    * [ ] Picture Frame (Trapezoid composite)
* [ ] Hexagons: 18xx tile example (requires `Arcs` below!)
* [ ] Hexagon Grid: better hexhex creation with notations
* [ ] Polyline: define arcs along the path
* [ ] Arcs (pathways) inside a hexagon (**in progress**)
* [ ] Shortcut notation for styling of a Shape
* [ ] Stripes: interior "areas" for a Rectangle
* [ ] Cards:
    * [ ] support card-back designs
    * [ ] grid lines for hexagonal cards
    * [ ] multiple custom bleed areas
    * [x] access to Google Sheets
    * [x] extract rectangular cards as PNG files
    * [ ] page annotations
* [ ] Color:
    * [ ] add support for CYMK

## :jigsaw: Potential Examples

These are possible examples to show board creation based on existing games:

* [ ] Extra abstract game boards: Ludo, Wari, Mu Torere
* [ ] Wargame board: Squad Leader with full terrain features (vector and bitmap)
* [ ] Traveller board: show a fully-styled Star System
* [x] WarpWar board: show a fully-styled example
* [ ] 18xx board: show a basic map with tracks, towns, cities and off-map areas

## :mega: Acknowledgements

> *The world is full of power and energy and a person can go far by just
> skimming off a tiny bit of it.*
> "[Snow Crash](https://en.wikipedia.org/wiki/Snow_Crash)", Neal Stephenson, 1992.

As always, with Python, you are building "on the shoulders of giants".
In this case, the [pyMuPDF](https://pymupdf.io/) library provides all of the
core infrastructure used to do the underlying graphics processing, PDF file
creation and images exports; __protograf__ is effectively a highly customised
wrapper to simplify common uses around its existing and extensive capabilities.

Earlier versions of  __protograf__  used the *ReportLab PDF Toolkit*, which is
also a very powerful library for supporting this type of application. Internal
terminology, such as `shapes`, was developed before the adoption of *pyMuPDF*
and it is coincidental that these are similar!

### :books: Additional Libraries

* `cairoSVG` https://pypi.org/project/cairosvg/ - support for drawing SVG images
* `bgg-api` https://pypi.org/project/bgg-api/ - support for access to the
  [BoardGameGeek](https://boardgamegeek.com) API
* `xlrd` https://pypi.org/project/xlrd/ - support for access to Excel `.xls` files
* `openpyxl` https://pypi.org/project/openpyxl/ - support for access to Excel files
* `imageio` https://pypi.org/project/imageio/- support for compiling PNGs into a GIF
* `jinja` https://jinja.palletsprojects.com - template logic with variables
* `pillow` https://github.com/python-pillow/Pillow - support for image processing
* `segno` https://github.com/heuer/segno/ - support for QRCode creation

## :scroll: License

__protograf__ is licensed under the GNU General Public License.
