from protograf.proto import (
    Arc, Arrow, Bezier, Chord, chord, Circle, Cross, Dot, Ellipse, Hexagon, Line,
    Pod, Polygon, Rhombus, Rectangle, Polyshape, QRCode, Sector, Square, Stadium,
    Star, StarLine, Text, Trapezoid, Triangle,)

def test_arc():
    s = Arc()
    assert s.x == 1
    assert s.y == 1

def test_arrow():
    s = Arrow()
    assert s.x == 1
    assert s.y == 1

def test_bezier():
    s = Bezier()
    assert s.x == 1
    assert s.y == 1

def test_chord():
    s = chord()
    assert s.x == 1
    assert s.y == 1

def test_circle():
    s = Circle()
    assert s.x == 1
    assert s.y == 1

def test_cross():
    s = Cross()
    assert s.x == 1
    assert s.y == 1

def test_dot():
    s = Dot()
    assert s.x == 1
    assert s.y == 1

def test_ellipse():
    s = Ellipse()
    assert s.x == 1
    assert s.y == 1

def test_hexagon():
    s = Hexagon()
    assert s.x == 1
    assert s.y == 1

def test_line():
    s = Line()
    assert s.x == 1
    assert s.y == 1

def test_pod():
    s = Pod()
    assert s.x == 1
    assert s.y == 1

def test_polygon():
    s = Polygon()
    assert s.x == 1
    assert s.y == 1

def test_polyshape():
    s = Polyshape()
    assert s.x == 0.0
    assert s.y == 0.0

def test_rhombus():
    s = Rhombus()
    assert s.x == 1
    assert s.y == 1

def test_rectangle():
    s = Rectangle()
    assert s.x == 1
    assert s.y == 1

def test_qrcode():
    s = QRCode()
    assert s.x == 1
    assert s.y == 1

def test_sector():
    s = Sector()
    assert s.x == 1
    assert s.y == 1

def test_square():
    s = Square()
    assert s.x == 1
    assert s.y == 1

def test_stadium():
    s = Stadium()
    assert s.x == 1
    assert s.y == 1

def test_star():
    s = Star()
    assert s.x == 1
    assert s.y == 1

def test_starline():
    s = StarLine()
    assert s.x == 1
    assert s.y == 1

def test_text():
    s = Text()
    assert s.x == 1
    assert s.y == 1

def test_trapezoid():
    s = Trapezoid()
    assert s.x == 1
    assert s.y == 1

def test_triangle():
    s = Triangle()
    assert s.x == 1
    assert s.y == 1
