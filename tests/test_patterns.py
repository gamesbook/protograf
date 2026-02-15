import pytest
from protograf.proto import (
    Grid, HexHex, Blueprint, Repeat, Lines, Sequence, Hexagons, Rectangles,
    Squares, Locations, Location, LinkLine, Layout, Track, )
from protograf.utils.structures import Locale, GridShape
# from protograf.layouts import GridShape

def test_grid():
    s = Grid()
    assert s.x == 0.0
    assert s.y == 0.0

def test_hexhex():
    s = HexHex()
    assert s.x == 1
    assert s.y == 1

def test_blueprint():
    s = Blueprint()
    assert s.x == 0.0
    assert s.y == 0.0

def test_repeat():
    with pytest.raises(SystemExit):
        Repeat()

def test_lines():
    s = Lines()
    assert s is None

def test_sequence():
    s = Sequence()
    assert s is None

def test_hexagons():
    s = Hexagons()
    assert isinstance(s[0], Locale)

def test_rectangles():
    s = Rectangles()
    assert isinstance(s[0], Locale)

def test_squares():
    s = Squares()
    assert isinstance(s[0], GridShape)

def test_locations():
    with pytest.raises(TypeError):
        Locations()

def test_location():
    with pytest.raises(TypeError):
        Location()

def test_linkline():
    with pytest.raises(TypeError):
        LinkLine()

def test_layout():
    with pytest.raises(TypeError):
        Layout()

def test_track():
    s = Track()
    assert s is None
