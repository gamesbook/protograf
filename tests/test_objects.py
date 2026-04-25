from protograf.proto import (
    Create,
    Cube, D6, Domino, Polyomino, Pentomino, Tetromino, StarField)

def test_cube():
    Create(globals_reset=True)
    s = Cube()
    assert s.x == 1
    assert s.y == 1

def test_d6():
    Create(globals_reset=True)
    s = D6()
    assert s.x == 1
    assert s.y == 1

def test_domino():
    Create(globals_reset=True)
    s = Domino()
    assert s.x == 1
    assert s.y == 1

def test_polyomino():
    Create(globals_reset=True)
    s = Polyomino()
    assert s.x == 1
    assert s.y == 1

def test_pentomino():
    Create(globals_reset=True)
    s = Pentomino()
    assert s.x == 1
    assert s.y == 1

def test_tetromino():
    Create(globals_reset=True)
    s = Tetromino()
    assert s.x == 1
    assert s.y == 1

def test_starfield():
    Create(globals_reset=True)
    s = StarField()
    assert s.x == 1
    assert s.y == 1
