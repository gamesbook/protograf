from protograf.proto import (
    Cube, D6, Domino, Polyomino, Pentomino, Tetromino, StarField)

def test_cube():
    s = Cube()
    assert s.x == 1
    assert s.y == 1

def test_d6():
    s = D6()
    assert s.x == 1
    assert s.y == 1

def test_domino():
    s = Domino()
    assert s.x == 1
    assert s.y == 1

def test_polyomino():
    s = Polyomino()
    assert s.x == 1
    assert s.y == 1

def test_pentomino():
    s = Pentomino()
    assert s.x == 1
    assert s.y == 1

def test_tetromino():
    s = Tetromino()
    assert s.x == 1
    assert s.y == 1

def test_starfield():
    s = StarField()
    assert s.x == 1
    assert s.y == 1
