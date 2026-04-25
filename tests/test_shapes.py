from protograf.proto import (
    Create,
    Arc, Arrow, Bezier, Chord, chord, Circle, Cross, Dot, Ellipse, Hexagon, Line,
    Pod, Polygon, Rhombus, Rectangle, Polyshape, QRCode, Sector, Square, Stadium,
    Star, StarLine, Text, Trapezoid, Triangle,)

def test_arc():
    Create(globals_reset=True)
    s = Arc()
    assert s.x == 1
    assert s.y == 1

def test_arrow():
    Create(globals_reset=True)
    s = Arrow()
    assert s.x == 1
    assert s.y == 1

def test_bezier():
    Create(globals_reset=True)
    s = Bezier()
    assert s.x == 1
    assert s.y == 1

def test_chord():
    Create(globals_reset=True)
    s = chord()
    assert s.x == 1
    assert s.y == 1

def test_circle():
    Create(globals_reset=True)
    s = Circle()
    assert s.x == 1
    assert s.y == 1

def test_cross():
    Create(globals_reset=True)
    s = Cross()
    assert s.x == 1
    assert s.y == 1

def test_dot():
    Create(globals_reset=True)
    s = Dot()
    assert s.x == 1
    assert s.y == 1

def test_ellipse():
    Create(globals_reset=True)
    s = Ellipse()
    assert s.x == 1
    assert s.y == 1

def test_hexagon():
    Create(globals_reset=True)
    s = Hexagon()
    assert s.x == 1
    assert s.y == 1

def test_line():
    Create(globals_reset=True)
    s = Line()
    assert s.x == 1
    assert s.y == 1

def test_pod():
    Create(globals_reset=True)
    s = Pod()
    assert s.x == 1
    assert s.y == 1

def test_polygon():
    Create(globals_reset=True)
    s = Polygon()
    assert s.x == 1
    assert s.y == 1

def test_polyshape():
    Create(globals_reset=True)
    s = Polyshape()
    assert s.x == 0.0
    assert s.y == 0.0

def test_rhombus():
    Create(globals_reset=True)
    s = Rhombus()
    assert s.x == 1
    assert s.y == 1

def test_rectangle():
    Create(globals_reset=True)
    s = Rectangle()
    assert s.x == 1
    assert s.y == 1

def test_qrcode():
    Create(globals_reset=True)
    s = QRCode()
    assert s.x == 1
    assert s.y == 1

def test_sector():
    Create(globals_reset=True)
    s = Sector()
    assert s.x == 1
    assert s.y == 1

def test_square():
    Create(globals_reset=True)
    s = Square()
    assert s.x == 1
    assert s.y == 1

def test_stadium():
    Create(globals_reset=True)
    s = Stadium()
    assert s.x == 1
    assert s.y == 1

def test_star():
    Create(globals_reset=True)
    s = Star()
    assert s.x == 1
    assert s.y == 1

def test_starline():
    Create(globals_reset=True)
    s = StarLine()
    assert s.x == 1
    assert s.y == 1

def test_text():
    Create(globals_reset=True)
    s = Text()
    assert s.x == 1
    assert s.y == 1

def test_trapezoid():
    Create(globals_reset=True)
    s = Trapezoid()
    assert s.x == 1
    assert s.y == 1

def test_triangle():
    Create(globals_reset=True)
    s = Triangle()
    assert s.x == 1
    assert s.y == 1
