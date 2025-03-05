# -*- coding: utf-8 -*-
"""
Support utilities for draw module
"""
# lib
from collections import namedtuple
import itertools
import os
import math
import sys
import string
from typing import Any

# third-party
import imageio
import pymupdf

LookupType = namedtuple("LookupType", ["column", "lookups"])


def feedback(item, stop=False, warn=False):
    """Placeholder for more complete feedback."""
    if warn:
        print("WARNING:: %s" % item)
    else:
        print("FEEDBACK:: %s" % item)
    if stop:
        print("FEEDBACK:: Could not continue with program.\n")
        # sys.exit()
        quit()


def numbers(*args):
    """Float range generator.

    'frange6' from http://code.activestate.com/recipes/\
                   66472-frange-a-range-function-with-float-increments/

    Doc Test:

    >>> dg = numbers(5.0, 10.0, 0.5)
    >>> assert next(dg) == 5.0
    >>> assert next(dg) == 5.5
    """
    start = 0.0
    step = 1.0
    l = len(args)
    if l == 1:
        end = args[0]
    elif l == 2:
        start, end = args
    elif l == 3:
        start, end, step = args
        if step == 0.0:
            raise ValueError("frange step must not be zero")
    else:
        raise TypeError("frange expects 1-3 arguments, got %d" % l)

    v = start
    while True:
        if (step > 0 and v >= end) or (step < 0 and v <= end):
            raise StopIteration
        yield v
        v += step


def letters(start: str = "a", stop: str = "z"):
    """Return list of characters between two letters.

    Doc Test:

    >>> letters('b', 'd')
    ['b', 'c', 'd']
    """

    def gen():
        for c in range(ord(start), ord(stop) + 1):
            yield chr(c)

    return list(gen())


def roman(value: int, REAL=True) -> str:
    """Convert an integer to a Roman number

    Source:
        https://www.geeksforgeeks.org/converting-decimal-number-lying-between-1-to-3999-to-roman-numerals/

    Note:
        REAL is only used for doctest, to bypass sys.exist() problem

    Doc Test:

    >>> roman(5)
    'V'
    >>> roman(50)
    'L'
    >>> roman(55)
    'LV'
    >>> roman(555)
    'DLV'
    >>> roman(5555, False)
    FEEDBACK:: Cannot convert a number above 3999 to Roman
    >>> roman('a', False)
    FEEDBACK:: The value "a" is not a valid integer
    """
    try:
        num = abs(int(value))
    except Exception:
        feedback(f'The value "{value}" is not a valid integer', REAL)
        return
    if num > 3999:
        feedback("Cannot convert a number above 3999 to Roman", REAL)
        return None

    # Store Roman values of digits from 0-9 at different places
    m = ["", "M", "MM", "MMM"]
    c = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM "]
    x = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]
    i = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]

    # Converting to Roman
    thousands = m[num // 1000]
    hundreds = c[(num % 1000) // 100]
    tens = x[(num % 100) // 10]
    ones = i[num % 10]
    ans = thousands + hundreds + tens + ones
    return ans


def steps(start, end, step=1, REAL=True):
    """Return a list of numbers from start to end, at step intervals.

    Note:
        REAL is only used for doctest, to bypass sys.exist() problem

    Doc Test:

    >>> steps('a', 'b', REAL=False)
    FEEDBACK:: A start value of "a" is not a valid number
    >>> steps(1, 'b', REAL=False)
    FEEDBACK:: An end value of "b" is not a valid number
    >>> steps(1, 2, 'c', REAL=False)
    FEEDBACK:: A step value of "c" is not a valid number
    >>> steps(2, 1, REAL=False)
    FEEDBACK:: End value of "1" must be greater than start value of "2"
    >>> steps(1, 2, -1, REAL=False)
    FEEDBACK:: End value of "2" must be less than start value of "1"
    >>> steps(2, 1, 0, REAL=False)
    FEEDBACK:: An step value of "0" is not valid
    >>> steps(1, 3, REAL=False)
    [1, 2, 3]
    >>> steps(1, 3, 2, REAL=False)
    [1, 3]
    >>> steps(3, 1, -2, REAL=False)
    [3, 1]
    >>> steps(1, 5, 1.5, REAL=False)
    [1, 2.5, 4.0]
    """
    try:
        _start = float(start)
    except Exception:
        feedback(f'A start value of "{start}" is not a valid number', REAL)
        return
    try:
        _end = float(end)
    except Exception:
        feedback(f'An end value of "{end}" is not a valid number', REAL)
        return
    try:
        _step = float(step)
    except Exception:
        feedback(f'A step value of "{step}" is not a valid number', REAL)
        return
    if step == 0:
        feedback(f'An step value of "{step}" is not valid', REAL)
        return
    if end < start and step > 0:
        feedback(
            f'End value of "{end}" must be greater than start value of "{start}"', REAL
        )
        return
    if start < end and step < 0:
        feedback(
            f'End value of "{end}" must be less than start value of "{start}"', REAL
        )
        return

    result, current = [], start
    while True:
        result.append(current)
        current += step
        if current > end and step > 0:
            break
        if current < end and step < 0:
            break
    return result


def split(string, delim=" "):
    """Split a string on the delim.

    Doc Test:

    >>> split('a b')
    ['a', 'b']
    >>> split('a,b', ',')
    ['a', 'b']
    """
    return string.split(delim)


def combinations(_object, size=2, repeat=1, delimiter=","):
    """Create a list of combinations.

    Args:
        _object: list OR delimited string
        size: int
            how many items to take from list to create a combo
        repeat: int
            how many times to repeat item in original list

    Doc Test:

    >>> combinations([1,2,3])
    ['12', '13', '23']
    >>> combinations('1,2,3')
    ['12', '13', '23']

    """
    try:
        size = int(size)
    except (TypeError, AttributeError):
        feedback(f'Unable to use a size of "{size}"', False, True)
        return []
    try:
        repeat = int(repeat)
    except (TypeError, AttributeError):
        feedback(f'Unable to use a repeat of "{repeat}"', False, True)
        return []
    try:
        items = _object.split(delimiter)
    except AttributeError:
        items = _object
    try:
        for item in items:
            pass
        items = items * repeat
        combo = itertools.combinations(items, size)
        full_list = []
        while True:
            try:
                comb = next(combo)
                sub = [str(cmb) for cmb in comb]
                full_list.append("".join(sub))
            except StopIteration:
                break
        new_list = list(set(full_list))
        new_list.sort()
        return new_list
    except (TypeError, AttributeError):
        feedback(f'Unable to create combinations from "{_object}"', False, True)
        return []


def to_int(value: Any, name: str = "", fail: bool = True) -> int:
    """Convert value to an integer.

    Doc Test:

    >>> to_int('3')
    3
    >>> to_int('a', fail=False)
    FEEDBACK:: Unable to convert "a" into a whole number!
    >>> to_int('a', name="foo", fail=False)
    FEEDBACK:: Unable to use foo value of "a" - needs to be a whole number!
    """
    try:
        return int(value)
    except Exception as err:
        if name:
            feedback(
                f'Unable to use {name} value of "{value}" - needs to be a whole number!',
                fail,
            )
        else:
            feedback(f'Unable to convert "{value}" into a whole number!', fail)


def to_float(value: Any, name: str = "", fail: bool = True) -> float:
    """Convert value to a float.ccto_float('3')
    3.0
    >>> to_float('a', fail=False)
    FEEDBACK:: Unable to convert "a" into a floating point number!
    >>> to_float('a', name="foo", fail=False)
    FEEDBACK:: Unable to use foo value of "a" - needs to be a floating point number!
    """
    try:
        return float(value)
    except Exception as err:
        if name:
            feedback(
                f'Unable to use {name} value of "{value}" - needs to be a floating point number!',
                fail,
            )
        else:
            feedback(f'Unable to convert "{value}" into a floating point number!', fail)


def excel_column(value: int = 1):
    """Convert a number into an Excel column letter.

    Ref:
        https://stackoverflow.com/questions/23861680/

    Doc Test:

    >>> excel_column(1)
    'A'
    >>> excel_column(27)
    'AA'
    """

    def converter(num):
        return (
            ""
            if num == 0
            else converter((num - 1) // 26) + string.ascii_uppercase[(num - 1) % 26]
        )

    num = to_int(value)
    return converter(num)


def excels(start, end, step=1, REAL=True):
    """Return a list of Excel col numbers from start to end, at step intervals.

    Doc Test:

    >>> excels(1, 2)
    ['A', 'B']
    >>> excels(27, 29)
    ['AA', 'AB', 'AC']
    """
    nums = steps(start, end, step=step, REAL=REAL)
    result = [excel_column(num) for num in nums]
    return result


def pdf_to_png(
    filename: str,
    fformat: str = "png",
    dpi: int = 300,
    names: list = None,
    directory: str = None,
    framerate: float = 1.0,
):
    """Extract pages from PDF as PNG image(s).  Optionally, assemble into a GIF.

    Uses:
        * https://pymupdf.io/
        * https://pypi.org/project/imageio/
    """
    feedback(f'Saving page(s) from "{filename}" as image file(s)...', False)
    _filename = os.path.basename(filename)
    basename = os.path.splitext(_filename)[0]
    dirname = directory or os.path.dirname(filename)
    # validate directory
    if not os.path.exists(dirname):
        feedback(
            f'Cannot find the directory "{dirname}" - please create this first.', True
        )
    # validate names list
    if names is not None:
        if isinstance(names, list):
            for name in names:
                if not (isinstance(name, str) or name is None):
                    feedback(
                        f'Each item in names settings "{names}" must be text or None.',
                        True,
                    )
        else:
            feedback(
                f'The names setting "{names}" must be a list of names.', False, True
            )
            names = None
        _names = [name in names if name is not None else name]
        if len(_names) != len(list(set(_names))):
            feedback(
                f'The names setting "{names}" does not contain a unique list of names.',
                False,
                True,
            )
    try:
        doc = pymupdf.open(filename)
        pages = doc.page_count
        all_pngs = []  # track full and final name of each saved .png
        # save pages as .png files
        for pg_number, page in enumerate(doc):
            pix = page.get_pixmap(dpi=dpi)
            if names and pg_number < len(names):
                if names[pg_number] is not None:
                    iname = os.path.join(dirname, f"{names[pg_number]}.png")
                    pix.save(iname)
                    all_pngs.append(iname)  # track for GIF creation
            else:
                if pages > 1:
                    iname = os.path.join(dirname, f"{basename}-{page.number + 1}.png")
                    all_pngs.append(iname)  # track for GIF creation
                else:
                    iname = os.path.join(dirname, f"{basename}.png")
                    all_pngs.append(iname)  # track for GIF creation
                pix.save(iname)
        # assemble .png files into a .gif
        if fformat == "gif" and framerate > 0:
            feedback(
                f'Converting PNG image file(s) from "{filename}" into a GIF...', False
            )
            images = []
            gif_name = os.path.join(dirname, f"{basename}.gif")
            for filename in all_pngs:
                images.append(imageio.imread(filename))
                imageio.mimsave(
                    gif_name, images, duration=framerate * 1000
                )  # ms -> sec
            for filename in all_pngs:
                if os.path.isfile(filename):
                    os.remove(filename)
    except Exception as err:
        feedback(f"Unable to extract images for {filename} - {err}!")


def pdf_cards_to_png(
    filename: str,
    fformat: str = "png",
    dpi: int = 300,
    directory: str = None,
    card_frames: dict = None,
    page_height: float = 0,
):
    """Extract individual cards from PDF as PNG image(s).

    Args:
        * card_frames - dict key is page number; value is a list of lists;
          each item in the nested list is a Bounding Box (bottom-left and
          top-right x,y coordinates)
        * page_height - in MuPDF's coordinate system, the y-axis is oriented
          from top to bottom, so ReportLab y-coordinates must be "inverted"

    Uses:
        * https://pymupdf.io/
        * https://pypi.org/project/imageio/
    """
    feedback(f'Saving card(s) from "{filename}" as image file(s)...', False)
    _filename = os.path.basename(filename)
    basename = os.path.splitext(_filename)[0]
    dirname = directory or os.path.dirname(filename)
    # validate directory
    if not os.path.exists(dirname):
        feedback(
            f'Cannot find the directory "{dirname}" - please create this first.', True
        )
    try:
        doc = pymupdf.open(filename)
        page_num = 0
        for page in doc:
            outlines = card_frames.get(page_num, [])
            for key, outline in enumerate(outlines):
                iname = os.path.join(
                    dirname, f"{basename}-{page_num + 1}-{key + 1}.png"
                )
                # https://pymupdf.readthedocs.io/en/latest/rect.html
                # Rect represents a rectangle defined by four floating point numbers
                # x0, y0, x1, y1. They are coordinates of diagonally opposite points.
                # The first two numbers are regarded as the “top left” corner P(x0,y0)
                # and second two are regarded P(x1,y1) as the “bottom right” one.
                rect = pymupdf.Rect(
                    outline.bl.x,  # top-left x0
                    page_height - outline.tr.y,  # top-left y0
                    outline.tr.x,  # bottom-right x1
                    page_height - outline.bl.y,  # bottom-right y1
                )
                pix = page.get_pixmap(clip=rect, dpi=dpi)  # page fragment as an image
                pix.save(iname)  # store image as a PNG
            page_num += 1
    except Exception as err:
        feedback(f"Unable to extract card images for {filename} - {err}!")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
