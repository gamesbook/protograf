import pytest
from protograf.proto import (
    Create,
    Grid, HexHex, Blueprint, Repeat, Lines, Sequence, Hexagons, Rectangles,
    Squares, Locations, Location, GridLine, Layout, Track, )
from protograf.utils.structures import Locale, GridShape
# from protograf.layouts import GridShape

def test_grid():
    Create(globals_reset=True)
    s = Grid()
    assert s.x == 0.0
    assert s.y == 0.0

def test_hexhex():
    Create(globals_reset=True)
    s = HexHex()
    assert s.x == 1
    assert s.y == 1

def test_blueprint():
    Create(globals_reset=True)
    s = Blueprint()
    assert s.x == 0.0
    assert s.y == 0.0

def test_repeat():
    Create(globals_reset=True)
    with pytest.raises(SystemExit):
        Repeat()

def test_lines():
    Create(globals_reset=True)
    s = Lines()
    assert s is None

def test_sequence():
    Create(globals_reset=True)
    s = Sequence()
    assert s is None

def test_hexagons():
    Create(globals_reset=True)
    s = Hexagons()
    assert isinstance(s[0], Locale)

def test_rectangles():
    Create(globals_reset=True)
    s = Rectangles()
    assert isinstance(s[0], Locale)

def test_squares():
    Create(globals_reset=True)
    s = Squares()
    assert isinstance(s[0], GridShape)

def test_locations():
    Create(globals_reset=True)
    with pytest.raises(TypeError):
        Locations()

def test_location():
    Create(globals_reset=True)
    with pytest.raises(TypeError):
        Location()

def test_gridline():
    Create(globals_reset=True)
    with pytest.raises(TypeError):
        GridLine()

def test_layout():
    Create(globals_reset=True)
    with pytest.raises(TypeError):
        Layout()

def test_track():
    Create(globals_reset=True)
    s = Track()
    assert s is None
