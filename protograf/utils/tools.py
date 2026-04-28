# -*- coding: utf-8 -*-
"""
General purpose utility functions for protograf
"""

# lib
from collections.abc import Iterable
import collections
import copy
from functools import lru_cache
from itertools import zip_longest
import logging
import os
import pathlib
from pathlib import Path
import re
import string
from string import ascii_uppercase, digits
import sys
from typing import Any, LiteralString, cast, Dict
from urllib.parse import urlparse

# third-party
import jinja2
from pymupdf import Point as muPoint, Matrix, Font as muFont

# local
from protograf.utils import colrs
from protograf.utils.constants import (
    CACHE_DIRECTORY,
    DEFAULT_FONT,
    STANDARD_CARD_SIZES,
    PAPER_SIZES,
)
from protograf.utils.fonts import builtin_font, FontInterface
from protograf.utils.messaging import feedback
from protograf.utils.support import to_units
from protograf.utils.structures import (
    DirectionGroup,
    GlobalDocument,
    Point,
    ShapeProperties,
    TemplatingType,
)
from protograf import globals

log = logging.getLogger(__name__)
DEBUG = False
MIN_ATTRIBUTES = ("scheme", "netloc")
BUILTIN_FONTS = ["Times-Roman", "Courier", "Helvetica"]


__alpha_to_decimal = {letter: pos for pos, letter in enumerate(ascii_uppercase, 1)}
__powers = (1, 26, 676)


def script_path() -> str | Path:
    """Get the path for a script being called from command line.

    Doc Test:

    >>> R = script_path()
    >>> len(str(R)) > 1
    True
    """
    fname = os.path.abspath(sys.argv[0])
    if fname:
        return pathlib.Path(fname).resolve().parent
    return ""


def grouper(n, iterable, fillvalue=None):
    """Group and return sets

    See:
        http://stackoverflow.com/questions/2990121/~
        how-do-i-loop-through-a-python-list-by-twos

    Use:
        for item1, item2, item3 in grouper(3, 'ABCDEFG', 'x'):

    Doc Test:

    >>> list(grouper(3, 'ABCDEFG', 'x'))
    [('A', 'B', 'C'), ('D', 'E', 'F'), ('G', 'x', 'x')]
    """

    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


def boolean_join(items):
    """Create a result from a Boolean concatenation

    Doc Test:

    >>> items = [True, '+', False]
    >>> boolean_join(items)
    False
    >>> items = [True, '|', False]
    >>> boolean_join(items)
    True
    >>> items = [True, None]
    >>> boolean_join(items)
    True
    """
    if not items or len(items) == 0:
        return None
    expr = ""
    for item in items:
        if item == "&" or item == "and" or item == "+":
            expr += " and "
        elif item == "|" or item == "or":
            expr += " or "
        elif item is not None:
            expr += "%s" % item
        else:
            pass  # ignore nones
    try:
        result = eval(expr)
    except NameError:
        return None
    return result


def _vprint(poynts: list, decimals: int = 2) -> str:
    """Return a user-units, truncated number, version of a list of points."""
    upoints = [Point(pt.x / globals.units, pt.y / globals.units) for pt in poynts]
    rpoints = [
        Point("%.2f" % round(pt.x, decimals), "%.1f" % round(pt.y, decimals))
        for pt in upoints
    ]
    result = ""
    for key, pt in enumerate(rpoints):
        result += f"{key}:({pt.x},{pt.y}), "
    return result.strip(", ")


def _lower(value) -> str | None:
    """Convert value into a lowercase string without any space around it

    Doc Test:

    >>> _lower(None)

    >>> _lower(1)
    '1'
    >>> _lower('a')
    'a'
    >>> _lower('AbA')
    'aba'
    >>> _lower( 'aB ')
    'ab'
    """
    if value is None:
        return None
    try:
        return str(value).lower().strip()
    except Exception:
        raise ValueError(f"Cannot convert {value} into a string!")


def _p2v(value: Point, decimals: int = 4) -> tuple:
    """Convert Point values to a rounded, units-based values using current units.

    Doc Test:

    >>> _p2v(Point(28, 56))
    (0.9878, 1.9756)
    """
    try:
        _units = globals.units
    except:
        _units = 28.3465
    try:
        return (
            round(float(value.x) / _units, decimals),
            round(float(value.y) / _units, decimals),
        )
    except Exception as err:
        log.exception(err)
        feedback(
            f'Unable to do units conversion from "{value}" using {globals.units}!',
            True,
        )
    return (0.0, 0.0)


def _u2p(value: Point) -> tuple:
    """Convert Point values, in user-units, to a Point with point-based values.

    Doc Test:

    >>> _u2p(Point(0.9878, 1.9756))
    Point(x=28.0006727, y=56.0013454)

    """
    try:
        _units = globals.units
    except:
        _units = 28.3465
    try:
        return Point(float(value.x) * _units, float(value.y) * _units)
    except Exception as err:
        log.exception(err)
        feedback(
            f'Unable to do units conversion from "{value}" using {globals.units}!',
            True,
        )
    return (0.0, 0.0)


def as_int(
    value,
    label: str | None = None,
    maximum: int | None = None,
    minimum: int | None = None,
    allow_none: bool = False,
) -> int | None:
    """Convert a value to an int

    Args:

    - value (Any): the value to be converted to a float
    - label (str): assigned as part of the error message to ID the type of value
    - maximum (int): the upper allowed value for the conversion
    - lower (int): the lower allowed value for the conversion
    - allow_none (bool): if True, return None if value is None

    Doc Test:

    >>> as_int(value='3', label='N')
    3

    # below cannot be tested because of sys.exit() in feedback()
    # >>> as_int(value='3', label='N', minimum=4)
    # FEEDBACK:: z is
    # >>> as_int(value='3', label='N', maximum=2)
    # FEEDBACK:: z is
    # >>> as_int(value='z', label='N')
    # FEEDBACK:: The N value "z" is not a valid integer!
    # >>> as_int(value='3.1', label='N')
    # FEEDBACK:: The N value "3.1" is not a valid integer!
    """
    if value is None or value == "" and allow_none:
        return None
    _label = f"{label} value " if label else "value "
    try:
        the_value = int(value)
        if minimum and the_value < minimum:
            feedback(
                f'The {_label}"{value}" is less than the integer minimum of {minimum}!',
                True,
            )
        if maximum and the_value > maximum:
            feedback(
                f'The {_label}"{value}" is more than the integer maximum of {maximum}!',
                True,
            )
        return the_value
    except (ValueError, Exception):
        feedback(f'The {_label}"{value}" is not a valid integer!!', True)


def as_bool(value, allow_none: bool = True) -> bool | None:
    """Convert a value to a Boolean

    Args:

    - value (Any): the value to be converted to a float
    - allow_none (bool): if True, return None if value is None

    Doc Test:

    >>> as_bool(value='3')
    False
    >>> as_bool(value=None)
    >>> as_bool(value=None, allow_none=True)
    >>> as_bool(value=None, allow_none=False)
    False
    >>> as_bool(value='1')
    True
    >>> as_bool(value='Y')
    True
    """
    trues = ["yes", "y", "ya", "yep", "yeah", "ja", "oui", "si", "true", "t", "1"]
    if value is None and allow_none:
        return value
    # _label = f" for {label}" if label else " of"
    result = str(value).lower() in trues
    return result


def as_float(
    value,
    label: str,
    maximum: float | None = None,
    minimum: float | None = None,
    stop: bool = True,
    default: float = 0.0,
) -> float:
    """Set a value to an float; or end program if an invalid value and stop is True

    Args:

    - value (Any): the value to be converted to a float
    - label (str): assigned as part of the error message to ID the type of value
    - maximum (float): the upper allowed value for the conversion
    - lower (float): the lower allowed value for the conversion
    - stop (bool): if True, halt program and display error message
    - default (float): default value to return

    Doc Test:

    >>> as_float(value='3', label='N')
    3.0

    # below cannot be tested because of sys.exit() in feedback()
    # >>> as_float(value='3', label='N', minimum=4)
    # FEEDBACK:: z is
    # >>> as_float(value='3', label='N', maximum=2)
    # FEEDBACK:: z is
    # >>> as_float(value='z', label='N')
    # FEEDBACK:: z is not a valid N integer!
    # >>> as_float(value='3.1', label='N')
    # FEEDBACK:: The value "3.1" for N is not a valid integer!
    """
    _label = f" for {label}" if label else " "
    try:
        the_value = float(value)
        if minimum and the_value < minimum:
            feedback(
                f'The "{value}"{_label} float value is less than the minimum of {minimum}!',
                stop,
            )
        if maximum and the_value > maximum:
            feedback(
                f'The "{value}"{_label} float value is more than the maximum of {maximum}!',
                stop,
            )
        return the_value
    except (ValueError, Exception):
        if stop:
            feedback(f'The value "{value}"{_label} is not a valid float number!', True)
    return default


def as_point(value) -> list | Point:
    """Convert one or more tuples to a Point or list of Points

    Doc Test:

    >>> as_point((1,2))
    Point(x=1, y=2)
    >>> as_point([(1,2), (3,4)])
    [Point(x=1, y=2), Point(x=3, y=4)]
    """
    if value is None:
        return []
    if isinstance(value, tuple):
        return Point(value[0], value[1])
    if isinstance(value, list):
        items = []
        for item in value:
            if isinstance(item, tuple):
                items.append(Point(item[0], item[1]))
            else:
                raise ValueError(f"Cannot convert {item} into a Point!")
        return items
    raise ValueError(f"Cannot convert {value} into a Point!")


def compass_to_rotation(value: str) -> float:
    """Convert a compass direction to a rotation number.

    Doc Test:

    >>> compass_to_rotation('n')
    90
    >>> compass_to_rotation('s')
    270
    """
    _value = _lower(value)
    match _value:
        case "n":
            return 90
        case "e":
            return 0
        case "w":
            return 180
        case "s":
            return 270
        case "ne":
            return 45
        case "nw":
            return 135
        case "sw":
            return 225
        case "se":
            return 315
        case _:
            feedback(f'Compass direction "{value}" is not valid!', True)
            return 0


def tuple_split(
    strng: str, label: str = "list", pairs_list: bool = False, all_ints: bool = False
) -> list:
    """Split a string into a list of tuple numbers

    Doc Test:

    >>> print(tuple_split(''))
    []
    >>> print(tuple_split('3'))
    [(3.0,)]
    >>> print(tuple_split('3,4'))
    [(3.0, 4.0)]
    >>> print(tuple_split('  3,4  5.1,6.2   -7,8.1'))
    [(3.0, 4.0), (5.1, 6.2), (-7.0, 8.1)]
    >>> print(tuple_split('3,5 6,1 4,2'))
    [(3.0, 5.0), (6.0, 1.0), (4.0, 2.0)]
    >>> print(tuple_split('3,5 6,1 4,2', all_ints=True))
    [(3, 5), (6, 1), (4, 2)]

    # below cannot be tested because of sys.exit() in feedback()
    # print(tuple_split('a,5 6,1 4,2', all_ints=True))
    # FEEDBACK:: Cannot convert list into a list of integer sets!
    # print(tuple_split('3,5 6,1 4', pairs_list=True))
    # Values of list must be pairs of integers!
    """
    values = []
    if strng:
        try:
            _string_list = strng.strip(" ").replace(";", ",").split(" ")
            for _str in _string_list:
                items = _str.split(",")
                _items = []
                for itm in items:
                    _itm = itm.strip(" ")
                    if _itm:
                        if all_ints:
                            _items.append(int(_itm))
                        else:
                            _items.append(float(_itm))
                if _items:
                    values.append(tuple(_items))
            if pairs_list:
                for value in values:
                    if len(value) != 2:
                        feedback(
                            f"Values of {label} must be pairs of integers!",
                            f' Check if all values in "{strng}" are integer pairs.',
                            True,
                        )
            return values
        except ValueError as err:
            if all_ints:
                feedback(
                    f"Cannot convert {label} into a list of integer sets!"
                    f' Check if all values in "{strng}" are integers.',
                    True,
                )
            else:
                feedback(
                    f"Cannot convert {label} into a list of numeric sets ({err})!", True
                )
            return values

        except Exception:
            return values
    else:
        return values


def sequence_split(
    strng: str,
    to_int: bool = True,
    unique: bool = True,
    sep: str = ",",
    to_float: bool = False,
    msg: str = "",
    clean: bool = False,
    star: bool = False,
) -> list:
    """
    Split a string into a list of individual values

    Args:

    - strng: the item to be split
    - to_int (bool): if True, convert values to integers
    - unique (bool): if True, create a list of unique
    - sep (str): expected delimiter between values - defaults to ","
    - to_float (bool): if True, convert values to floats
    - msg (str): return as part of the error
    - clean (bool): if True, strip any surrounding spaces
    - star (bool): if True, allow for "all" or "*" as the only list value

    Note:
        * If `unique` is True, order will NOT be maintained!

    Doc Test:

    >>> sequence_split('*', star=True)
    ['*']
    >>> sequence_split('')
    []
    >>> sequence_split('3')
    [3]
    >>> sequence_split('3', to_int=False)
    ['3']
    >>> sequence_split('3,4,5')
    [3, 4, 5]
    >>> sequence_split('3,4,5', to_int=False, unique=False)
    ['3', '4', '5']
    >>> x = sequence_split('3,4,5', to_int=False)
    >>> assert '5' in x
    >>> sequence_split('3-5,6,1-4')
    [1, 2, 3, 4, 5, 6]
    >>> sequence_split('A,1,B', to_int=False, unique=False)
    ['A', '1', 'B']
    >>> sequence_split('3.1,4.2,5.3', unique=False, to_int=False, to_float=True)
    [3.1, 4.2, 5.3]
    >>> sequence_split([3.1,4.2,5.3], unique=False, to_int=False, to_float=True)
    [3.1, 4.2, 5.3]
    >>> sequence_split(3)
    [3]
    >>> sequence_split(3.1)
    [3.1]
    """
    values = []
    if isinstance(strng, list):
        return strng
    if isinstance(strng, (int, float)):
        return [strng]
    if strng:
        try:
            if sep == ",":
                _string = strng.replace('"', "").replace("'", "").strip()
            else:
                _string = strng
                if clean or star:
                    _string = _string.strip()
        except Exception:
            return values
    else:
        return values

    # simple single value
    try:
        if to_int:
            values.append(int(_string))
            return values
    except Exception:
        pass

    # multi-values
    _strings = []
    try:
        _strings = _string.split(sep)
    except AttributeError:
        feedback(
            f'Unable to split "{_string}" - please check that its a valid candidate!',
            False,
        )
        if isinstance(_string, TemplatingType):
            feedback("The script may not be using T() correctly", True)
        else:
            feedback("", True)

    # star test
    if star and len(_strings) == 1:
        if _strings[0] == "*" or _strings[0] == "all":
            return ["*"]

    # log.debug('strings:%s', _strings)
    for item in _strings:
        if "-" in item:
            _strs = item.split("-")
            seq_range = [str(val) for val in _strs]
            if to_int:
                seq_range = list(range(int(_strs[0]), int(_strs[1]) + 1))
            values = values + seq_range
            if to_float:
                feedback(f'Cannot set a range of decimal numbers ("{item}"){msg}', True)
        else:
            if to_int:
                try:
                    values.append(int(item))
                except ValueError:
                    feedback(
                        f'Unable to use "{item}"; check for whole numbers (with a {sep} between each)',
                        True,
                    )
            elif to_float:
                try:
                    values.append(float(item))
                except ValueError:
                    feedback(
                        f'Unable to use "{item}"; check for numbers (with a {sep} between each)',
                        True,
                    )
            else:
                _item = str(item).strip() if clean else str(item)
                values.append(_item)

    if unique:
        return list(set(values))  # unique
    return values


def split(
    strng: str,
    tuple_to_list: bool = False,
    separator: str | None = None,
    clean: bool = False,
):
    """
    Split a string into a list of individual characters

    Doc Test:

    >>> split('A,1,B')
    ['A', '1', 'B']
    >>> split('A 1 B')
    ['A', '1', 'B']
    >>> split((1, 2, 3), True)
    [(1, 2, 3)]
    >>> split("1;2;3", separator=';')
    ['1', '2', '3']
    >>> split("1; 2; 3", separator=';', clean=True)
    ['1', '2', '3']
    >>> split("A,b B, C")
    ['A', 'b B', ' C']
    >>> split("A,b B, C", clean=True)
    ['A', 'b B', 'C']
    """
    if isinstance(strng, list):
        return strng
    if isinstance(strng, tuple):
        if tuple_to_list:
            return [strng]
        return strng
    if separator:
        sep = separator
    else:
        sep = " " if strng and "," not in strng else ","
    return sequence_split(strng, to_int=False, unique=False, sep=sep, clean=clean)


def separate(
    strng: str,
    tuple_to_list: bool = False,
    separator: str | None = None,
    clean: bool = False,
):
    """
    Split a string into a list of individual items

    Doc Test:

    >>> separate('A,1,B')
    ['A', '1', 'B']
    >>> separate('A 1 B')
    ['A', '1', 'B']
    >>> separate((1, 2, 3), True)
    [(1, 2, 3)]
    >>> separate("1;2;3", separator=';')
    ['1', '2', '3']
    >>> separate("1; 2; 3", separator=';', clean=True)
    ['1', '2', '3']
    >>> separate("A,b B, C")
    ['A', 'b B', ' C']
    >>> separate("A,b B, C", clean=True)
    ['A', 'b B', 'C']
    >>> separate("A,1-3, C, 1:1-3", separator=',', clean=True)
    ['A', '1-3', 'C', '1:1-3']
    >>> separate("A b C d:1,6", separator=' ', clean=True)
    ['A', 'b', 'C', 'd:1,6']

    """
    if isinstance(strng, list):
        return strng
    if isinstance(strng, tuple):
        if tuple_to_list:
            return [strng]
        return strng
    if separator:
        sep = separator
    else:
        sep = " " if (strng and "," not in strng) else ","
    result = strng.split(sep)
    if clean:
        outcome = [item.strip() for item in result if item.strip() != ""]
        return outcome
    return result


def integer_pairs(pairs, label: str = "list") -> list:
    """Convert a list or string into a list of tuples; each with a pair of integers.

    Doc Test:

    >>> integer_pairs(pairs=[(1,2), (3,4)])
    [(1, 2), (3, 4)]
    >>> integer_pairs(pairs="1,2 3,4")
    [(1, 2), (3, 4)]
    """
    if pairs:
        if isinstance(pairs, str):
            pairs = tuple_split(pairs, label=label, all_ints=True, pairs_list=True)
        if not isinstance(pairs, list):
            feedback(f"The {label} value '{pairs}' is not valid list!", True)
        for item in pairs:
            if not isinstance(item, tuple):
                feedback(
                    f'{label} must only contain a list of integers pairs (not "{pairs}")!',
                    True,
                )
            if len(item) != 2:
                feedback(
                    f'{label} must only contain a list of paired integers (not "{pairs}")!',
                    True,
                )
            for val in item:
                if not isinstance(val, int):
                    feedback(
                        f"{label} must only contain integers "
                        f' ("{val}" in "{pairs}" is not an integer)!',
                        True,
                    )
        return pairs
    return []


def splitq(seq, seps: str | None = None, pairs: str = "()[]{}<>", quotes: str = "'\""):
    """
    Split sequence by separator but considering parts inside pairs or quoted
    as unbreakable; ppairs have different start and end value; quote has same
    symbol in beginning and end.

    Notes:
        * Use itertools.islice if only part of splits is needed

    Source:
        https://www.daniweb.com/programming/software-development/code/426990/\
        split-string-except-inside-brackets-or-quotes
        -> but using the split_outside() function NOT the original with errors

    Doc Test:

    >>> result = splitq("Hello, (Tony Jarkko) This ('is') quoted Great to 'split'   {this split}'Also Quoted part' [test test] end ")
    >>> print(list(result))
    ['Hello,', '(Tony Jarkko)', 'This', "('is')", 'quoted', 'Great', 'to', "'split'", "{this split}'Also Quoted part'", '[test test]', 'end']
    """
    closers = {pairs[i + 1]: pairs[i] for i in range(0, len(pairs), 2)}
    openers = set(closers.values())
    sep = None if seps is None else set(seps)
    stack, buf, q = [], [], None
    for i, ch in enumerate(seq):
        if q:
            buf.append(ch)
            if ch == q and (i == 0 or seq[i - 1] != "\\"):
                q = None
        elif ch in quotes:
            q = ch
            buf.append(ch)
        elif ch in openers:
            stack.append(ch)
            buf.append(ch)
        elif ch in closers:
            if not stack or stack.pop() != closers[ch]:
                raise ValueError(
                    f"Did not find end of pair for '{closers.get(ch, '?')}': '{ch}'"
                )
            buf.append(ch)
        else:
            is_sep = (sep is None and ch.isspace()) or (sep is not None and ch in sep)
            if is_sep and not stack:
                if buf:
                    yield "".join(buf).strip()
                    buf = []
            else:
                buf.append(ch)
    if q:
        raise ValueError("Did not find end of quote.")
    if stack:
        opener = stack[-1]
        expected = next(c for c, o in closers.items() if o == opener)
        raise ValueError(f"Did not find end of pair for '{opener}': '{expected}'")
    if buf:
        yield "".join(buf).strip()


def flatten(lst: Iterable):
    """Flatten nested lists into a single list

    Doc Test:

    >>> list(flatten([0, [1, 2], [3,4, [5,6]]]))
    [0, 1, 2, 3, 4, 5, 6]
    """
    try:
        for ele in lst:
            if isinstance(ele, Iterable) and not isinstance(ele, str):
                for sub in flatten(ele):
                    yield sub
            else:
                yield ele
    except TypeError:
        yield lst


def flatten_keys(dictionary: dict):
    """Flatten nested dicts into a single dict.

    NOTE:
        * values for keys in nested dict will override those in parent(s)!
        * See: https://www.geeksforgeeks.org/python-flatten-nested-keys/

    Doc Test:

    >>> flatten_keys({'height': 8, 'cards': 1, 'image': None, 'kwargs': {'kwargs': {'image': 'FOO', 'kwargs': {'cards': 9}}}})
    {'height': 8, 'cards': 9, 'image': 'FOO'}
    """
    result = {}
    for key, val in dictionary.items():
        if isinstance(val, dict):
            flat_v = flatten_keys(val)
            for flat_k, flat_v in flat_v.items():
                # result[key + '.' + flat_k] = flat_v
                result[flat_k] = flat_v
        elif isinstance(val, list):
            for item in val:
                try:
                    flat_item = flatten_keys(item)
                except AttributeError:
                    flat_item = item
                if isinstance(flat_item, dict):
                    for flat_k, flat_v in flat_item.items():
                        result[f"{flat_k}"] = flat_v
        else:
            result[key] = val
    return result


def list_ordering(
    base: list,
    changes: list,
    start: bool = False,
    end: bool = False,
    only: bool = False,
) -> list:
    """Alter ordering in base list to match order in changes.

    Args:
        base (list): canonical list of all values with default order
        changes (list): selected values in required order
        start (bool): changes must appear at the start of the altered list
        end (bool): changes must appear at the end of the altered list
        only (bool): return only values in changes

    Returns:
        list

    Doc Test:

    >>> list_ordering([1], [1], False, False)
    [1]
    >>> list_ordering([1, 2, 3, 4, 5, 6, 7], [4, 5, 6], True, False)
    [4, 5, 6, 1, 2, 3, 7]
    >>> list_ordering([1, 2, 3, 4, 5, 6, 7], [2, 3, 4], False, True)
    [1, 5, 6, 7, 2, 3, 4]
    >>> list_ordering([1, 2, 3, 4, 5, 6, 7], [2, 3, 4], False, False, True)
    [2, 3, 4]
    """
    if not changes:
        return base
    if not isinstance(changes, list):
        feedback("Ordering values must be in a list", True)
    # validate changes
    for item in changes:
        if item not in base:
            allowed = ", ".join(base)
            feedback(
                f'Ordering values must be any of: "{allowed}" - not "{item}"', True
            )
    # first
    if start:
        combined_list = changes + base
        result_list = list(dict.fromkeys(combined_list))
        return result_list
    if end:
        result_list = [item for item in base if item not in changes]
        combined_list = result_list + changes
        final_list = list(dict.fromkeys(combined_list))
        return final_list
    if only:
        return changes
    return base


def comparer(val: Any, operator: str, target: Any) -> bool:
    """Compare value with a target.

    Args:

    - val (str): the value to be checked
    - operator (str): one of - < | > | ~ | *
    - target: a single value or a list of values; for a list the operator must be a ~

    Doc Test:

    >>> comparer(None, None, None)
    True
    >>> comparer("1", '*', "1")
    FEEDBACK:: Unknown operator: * (1 and 1)
    False
    >>> comparer("1", None, "1")
    True
    >>> comparer("a", None, "a")
    True
    >>> comparer("True", None, "True")
    True
    >>> comparer("False", None, "False")
    True
    >>> comparer("1", '<', "1.1")
    True
    >>> comparer("a", '<', "aa")
    True
    >>> comparer("True", '<', "True")
    False
    >>> comparer("False", '<', "False")
    False
    >>> comparer("1", '~', "1.1")
    FEEDBACK:: Invalid operator for numbers: ~ (1.0 and 1.1)
    False
    >>> comparer("a", '~', "aa")
    True
    >>> comparer("True", '~', "True")
    FEEDBACK:: Invalid operator for numbers: ~ (1.0 and 1.0)
    False
    >>> comparer("False", '~', "False")
    FEEDBACK:: Invalid operator for numbers: ~ (0.0 and 0.0)
    False
    >>> comparer("1", '~', [1,2,3])
    True
    >>> comparer("1.1", '~', [1.1,2,3])
    True
    """

    def compare_numbers(val: int | float, target: int | float, operator: str) -> bool:
        if operator == "=":
            if val == target:
                return True
        elif operator == "<":
            if val < target:
                return True
        elif operator == ">":
            if val > target:
                return True
        elif operator == ">=":
            if val >= target:
                return True
        elif operator == "<=":
            if val <= target:
                return True
        elif operator == "!=":
            if val != target:
                return True
        else:
            feedback(f"Invalid operator for numbers: {operator} ({val} and {target})")
            return False
        return False

    def to_length(val, target):
        """Get length of object."""
        try:
            val = len(val)
        except Exception:
            pass
        try:
            target = len(target)
        except Exception:
            pass
        return val, target

    if target in ["T", "True"]:
        target = True
    if target in ["F", "False"]:
        target = False
    if val in ["T", "True"]:
        val = True
    if val in ["F", "False"]:
        val = False

    if not operator:
        operator = "="
    if operator in ["<", "<=", ">", ">="]:
        val, target = to_length(val, target)
    elif operator not in ["=", "~"]:
        feedback(f"Unknown operator: {operator} ({val} and {target})")
        return False

    try:
        _val = float(val)
        _target = float(target)
        result = compare_numbers(_val, _target, operator)
        return result
    except Exception:
        pass

    if operator == "=":
        if val == target:
            return True
    elif operator == "!=":
        if val != target:
            return True
    elif operator in ["~", "in"]:
        try:
            if val in target:
                return True
            if float(val) in target:
                return True
            if int(val) in target:
                return True
        except (ValueError, TypeError):
            pass
    else:
        pass

    return False


def alpha_column(num: int, lower: bool = False) -> str:
    """Convert a number to a letter-based notation

    Notes:
        * Encountered on a WarpWar map; numbers below 26 appear sequentially as
          a, b, c, etc, numbers above 26 appear sequentially as aa, bb, cc, etc; if
          above 52 then appear sequentially as aaa, bbb, ccc etc. Add more letters for
          each multiple of 26.

    Doc Test:

    >>> alpha_column(1)
    'A'
    >>> alpha_column(26, lower=True)
    'z'
    >>> alpha_column(27)
    'AA'
    """
    if lower:
        return string.ascii_lowercase[divmod(num - 1, 26)[1] % 26] * (
            divmod(num - 1, 26)[0] + 1
        )
    return string.ascii_uppercase[divmod(num - 1, 26)[1] % 26] * (
        divmod(num - 1, 26)[0] + 1
    )


@lru_cache(maxsize=None)
def integer_pair_to_cell(row: int, col: int) -> str:
    """Convert 0-indexed (row, col) to A1-style spreadsheet ID.

    Doc Test:

    >>> print(integer_pair_to_cell(0, 0))
    A1
    >>> print(integer_pair_to_cell(10, 27))
    AB11
    """
    column_str = ""
    while col >= 0:
        col, remainder = divmod(col, 26)
        column_str = chr(65 + remainder) + column_str
        if col == 0:
            break
        col -= 1
    return f"{column_str}{row + 1}"


@lru_cache(maxsize=None)
def column_from_string(col: str) -> int:
    """Convert ASCII column name (base 26) to decimal with 1-based index

    Characters represent descending multiples of powers of 26

    "AFZ" == 26 * pow(26, 0) + 6 * pow(26, 1) + 1 * pow(26, 2)

    Doc Test:

    >>> column_from_string('A')
    1
    >>> column_from_string('AA')
    27
    """
    error_msg = f"'{col}' is not a valid column name. Column names are from A to ZZZ"
    if len(col) > 3:
        raise ValueError(error_msg)
    idx = 0
    _col = reversed(col.upper())
    for letter, power in zip(list(_col), __powers):
        try:
            pos = __alpha_to_decimal.get(cast(LiteralString, letter))
        except KeyError:
            raise ValueError(error_msg)
        if pos is not None:
            idx += pos * power
    if not 0 < idx < 18279:
        raise ValueError(error_msg)
    return idx


def coordinate_to_tuple(coordinate: str, zeroed: bool = False) -> tuple | None:
    """Convert Excel style coordinate to 1-based (column, row) tuple

    Args:
        zeroed (bool): if True, use zero base

    Doc Test:

    >>> coordinate_to_tuple('A1')
    (1, 1)
    >>> coordinate_to_tuple('AB31')
    (28, 31)
    >>> coordinate_to_tuple('A1', True)
    (0, 0)
    >>> coordinate_to_tuple('AB31', True)
    (27, 30)
    >>> coordinate_to_tuple('')
    """
    idx = None
    for idx, c in enumerate(coordinate):
        if c in digits:
            break
    if idx:
        col = coordinate[:idx]
        row = coordinate[idx:]
        if zeroed:
            return column_from_string(col) - 1, int(row) - 1
        return column_from_string(col), int(row)


def sheet_column(num: int, lower: bool = False) -> str:
    """Convert a number to a spreadsheet-styled character string

    Ref:
        https://stackoverflow.com/questions/23861680/

    Doc Test:

    >>> sheet_column(num=3, lower=True)
    'c'
    >>> sheet_column(num=27, lower=False)
    'AA'
    """

    def converter(num, lower):
        if lower:
            return (
                ""
                if num == 0
                else converter((num - 1) // 26, lower)
                + string.ascii_lowercase[(num - 1) % 26]
            )
        return (
            ""
            if num == 0
            else converter((num - 1) // 26, lower)
            + string.ascii_uppercase[(num - 1) % 26]
        )

    return converter(num, lower)


@lru_cache(maxsize=256)
def get_font_by_name(fonts_name: object) -> tuple:
    """Get font details by name - built-in OR system installed.

    Args:
        fonts_name: expected name of font or fonts

    Returns:

    - font (pymupdf.Font): the Font object
    - font_file (str): path to the font's file
    - font_name (str): actual font name to be used
    - mu_font_name (str): font name to be used for HTML Text

    Doc Test:

    >>> get_font_by_name('foo')
    WARNING:: Cannot find or load the font(s) `foo`. Defaulting to "Helvetica".
    (Font('Helvetica'), None, 'Helvetica', 'Helvetica')
    >>> get_font_by_name('Helvetica')
    (Font('Helvetica'), None, 'Helvetica', 'Helvetica')
    >>> get_font_by_name(tuple(['foo', 'Times-Roman']))
    (Font('Times-Roman'), None, 'Times-Roman', 'Times-Roman')

    #get_font_by_name('Arial')
    #(Font('Arial Regular'), '/usr/share/fonts/truetype/msttcorefonts/Arial.ttf', 'Arial')
    """

    font, font_file = None, None
    if fonts_name is None:
        font_name = DEFAULT_FONT
    elif isinstance(fonts_name, str):
        font_names = [fonts_name]
    elif isinstance(fonts_name, (tuple, list)):
        font_names = fonts_name
    else:
        font_names = []
        feedback("Font name must be a string or a list of strings!", True)

    for font_name in font_names:
        if not builtin_font(font_name):
            cache_directory = pathlib.Path(pathlib.Path.home() / CACHE_DIRECTORY)
            fi = FontInterface(cache_directory=cache_directory)
            font_file = fi.get_font_file(name=font_name)
            if font_file:
                font = muFont(font_name, font_file)
                break  # stop after first one found
        else:
            font = muFont(font_name)  # built-in
            break

    if not font:
        feedback(
            f"Cannot find or load the font(s) `{fonts_name}`."
            f' Defaulting to "{DEFAULT_FONT}".',
            False,
            True,
        )
        font_name = DEFAULT_FONT
        font = muFont(DEFAULT_FONT)  # built-in

    mu_font_name = font_name.replace(" ", "-")
    return font, font_file, font_name, mu_font_name


def base_fonts():
    """Register MS Core Fonts

    NOTES:
        * On Ubuntu: sudo apt-get install ttf-mscorefonts-installer
        * The Windows filenames are 'truncated' versions, hence the use
          of an alternate
    """

    def register_font(name: str, filename: str | None = None):
        """Register a font."""
        log.debug("register_font: %s %s", name, filename)

    fonts = [
        {
            "name": "Arial",
            "alternate": "Arial",
        },
        {
            "name": "Verdana",
            "alternate": "Verda",
        },
        {
            "name": "Courier New",
            "alternate": "Cour",
        },
        {
            "name": "Times New Roman",
            "alternate": "Times",
        },
        {
            "name": "Trebuchet MS",
            "alternate": "Trebuc",
        },
        {
            "name": "Georgia",
            "alternate": "Georg",
        },
        {
            "name": "Webdings",
            "alternate": "Webd",
        },
        # {'name': 'ObiWan', 'alternate': 'benK'},  # dummy to check failure
    ]
    missing = []
    for ffont in fonts:
        name = ""
        try:
            name = ffont["name"]
            register_font(name)
        except Exception:
            try:
                alt = ffont.get("alternate")
                register_font(name, filename=alt)
            except Exception:
                missing.append(name)
    if missing:
        names = ", ".join(missing)
        feedback(f"Unable to register the MS font(s): {names}", False, True)


def eval_template(strng: str, data: dict | None = None, label: str = ""):
    """Process data dict via jinja2 template in source.

    Doc Test:

    >>> eval_template("2+{{x}}", {'x': 2})
    '2+2'
    >>> eval_template("2+{{x}}", {'y': 2})
    '2+'
    """
    if data is None or not data:
        return strng
    if isinstance(data, tuple):
        try:
            data = data._asdict()
        except Exception:
            pass
    if not isinstance(data, dict):
        feedback("The data must be in the form of a dictionary", True)
    try:
        environment = jinja2.Environment()
        template = environment.from_string(str(strng))
        custom_value = template.render(data)
        return custom_value
    except jinja2.exceptions.TemplateSyntaxError:
        feedback(
            f'Unable to create the text or value - check the grammar for "{strng}"',
            True,
        )
    except (ValueError, jinja2.exceptions.UndefinedError):
        feedback(f'Unable to process "{strng}" data with this template', True)


def valid_directions(
    direction_group: DirectionGroup,
    label: str = "",
    vertex_count: int = 0,
) -> dict | set:
    """."""
    match direction_group:
        case DirectionGroup.CARDINAL:
            valid = {"n", "e", "w", "s"}
        case DirectionGroup.ORDINAL:
            valid = {"ne", "se", "sw", "nw"}
        case DirectionGroup.COMPASS:
            valid = {"n", "e", "w", "s", "ne", "se", "sw", "nw"}
        case DirectionGroup.HEX_FLAT:  # radii
            valid = {"e", "se", "sw", "w", "ne", "nw"}
        case DirectionGroup.HEX_POINTY:  # radii
            valid = {"s", "se", "sw", "n", "ne", "nw"}
        case DirectionGroup.HEX_FLAT_EDGE:  # perbii
            valid = {"s", "se", "sw", "n", "ne", "nw"}
        case DirectionGroup.HEX_POINTY_EDGE:  # perbii
            valid = {"e", "se", "sw", "w", "ne", "nw"}
        case DirectionGroup.CIRCULAR:
            valid = {"n", "e", "w", "s", "ne", "se", "sw", "nw", "o", "d"}
        case DirectionGroup.TRIANGULAR:  # equilateral triangle VERTICES
            valid = {"se", "sw", "n"}
        case DirectionGroup.TRIANGULAR_EDGE:  # equilateral triangle
            valid = {"ne", "nw", "s"}
        case DirectionGroup.TRIANGULAR_HATCH:  # equilateral triangle HATCH
            valid = {"ne", "sw", "e", "w", "nw", "se"}
        case DirectionGroup.POLYGONAL:  # polygon
            valid = set(range(1, vertex_count + 1))
        case DirectionGroup.STAR:  # star
            valid = set(range(1, vertex_count + 1))
        case _:
            raise NotImplementedError(f"Cannot handle {direction_group} type!")
    return valid


def validated_gridlines(
    value: list | str,
    direction_group: DirectionGroup = DirectionGroup.COMPASS,
    label: str = "",
) -> list:
    """Check and return a list of lowercase, direction abbreviations for a grid.

    Doc Test:

    >>> validated_gridlines('n s')
    ['n', 's']
    >>> validated_gridlines('ne se')
    ['ne', 'se']
    >>> validated_gridlines('d se')
    ['ne', 'nw', 'se']
    >>> validated_gridlines('e w', DirectionGroup.HEX_POINTY_EDGE)
    ['e', 'w']
    >>> validated_gridlines('o', DirectionGroup.HEX_POINTY_EDGE)
    ['e', 'w']
    >>> validated_gridlines('n s', DirectionGroup.HEX_FLAT_EDGE)
    ['n', 's']
    >>> validated_gridlines('o', DirectionGroup.HEX_FLAT_EDGE)
    ['n', 's']
    """
    _value = value
    # ---- pre-flight checks
    if not value:
        return []
    if isinstance(value, int):
        value = str(value)
    if isinstance(value, str):
        value = value.strip().split(" ")
    else:
        if not isinstance(value, list):
            feedback(
                f"Cannot handle {label}{_value} - must be a string or a list!", True
            )
    values = [str(val).lower().strip() for val in value]
    # ---- replace generic directions
    clean_values = []
    for val in values:
        match val:
            case "all" | "*":
                if direction_group == DirectionGroup.HEX_FLAT_EDGE:
                    clean_values += ["n", "s", "ne", "sw"]
                elif direction_group == DirectionGroup.HEX_POINTY_EDGE:
                    clean_values += ["e", "w", "ne", "sw"]
                elif direction_group == DirectionGroup.TRIANGULAR_HATCH:
                    clean_values += ["e", "ne", "sw"]
                else:
                    clean_values += ["n", "s", "e", "w", "ne", "nw", "se", "sw"]
            case "d" | "diag" | "diagonal":
                if direction_group == DirectionGroup.HEX_FLAT_EDGE:
                    clean_values += ["ne", "nw"]
                elif direction_group == DirectionGroup.HEX_POINTY_EDGE:
                    clean_values += ["ne", "nw"]
                elif direction_group == DirectionGroup.TRIANGULAR_HATCH:
                    clean_values += ["ne", "nw"]
                else:
                    clean_values += ["ne", "nw"]
            case "o" | "ortho" | "orthogonal":
                if direction_group == DirectionGroup.HEX_FLAT_EDGE:
                    clean_values += ["n", "s"]
                elif direction_group == DirectionGroup.HEX_POINTY_EDGE:
                    clean_values += ["e", "w"]
                elif direction_group == DirectionGroup.TRIANGULAR_HATCH:
                    clean_values += ["e", "w"]
                else:
                    clean_values += ["n", "s", "e", "w"]
            case "n" | "s" | "e" | "w" | "ne" | "nw" | "se" | "sw":
                clean_values += [val]
            case _:
                _label = f'the {label} "{val}"' if label else f'"{val}"'
                feedback(
                    f"Cannot use {_label} - this must correspond with "
                    "one of the valid directions!",
                    True,
                )
    # ---- validate all directions
    values_set = set(clean_values)
    valid = valid_directions(direction_group, label, 0)
    if values_set.issubset(valid):
        # NOTE in some cases, we need to ignore `vertex_count` because not yet known...
        return clean_values
    _label = f'{label} "{_value}"' if label else f'"{_value}"'
    feedback(
        f"Cannot use {_label} - this must correspond with "
        f"one of the valid directions {valid}!",
        True,
    )
    return []


def validated_directions(
    value: list | str,
    direction_group: DirectionGroup,
    label: str = "",
    vertex_count: int = 0,
) -> list:
    """Check and return a list of lowercase, direction abbreviations.

    Doc Test:

    >>> validated_directions('n s', DirectionGroup.CARDINAL)
    ['n', 's']
    >>> validated_directions('ne se', DirectionGroup.HEX_FLAT)
    ['ne', 'se']
    >>> validated_directions('n s', DirectionGroup.HEX_POINTY)
    ['n', 's']
    >>> validated_directions('w e n s ne', DirectionGroup.COMPASS)
    ['w', 'e', 'n', 's', 'ne']
    >>> validated_directions(' w e n s ne ', DirectionGroup.COMPASS)  # spaces at ends
    ['w', 'e', 'n', 's', 'ne']
    >>> validated_directions('  1 4 7 ', DirectionGroup.STAR, vertex_count=8)  # spaces at ends
    [1, 4, 7]
    >>> validated_directions('1 9 17 ', DirectionGroup.POLYGONAL, vertex_count=20)
    [1, 9, 17]
    >>> validated_directions(1, DirectionGroup.POLYGONAL, vertex_count=20)
    [1]
    """
    if not value:
        return []
    if isinstance(value, int):
        value = str(value)
    if isinstance(value, str):
        value = value.strip()
        values = split(value.lower())
    else:
        if not isinstance(value, list):
            feedback(
                f"Cannot handle {label}{value} - must be a string or a list!", True
            )
        values = [str(val).lower().strip() for val in value]
    values_set = set(values)
    valid = valid_directions(direction_group, label, vertex_count)
    if "all" in values or "*" in values:
        values = list(valid)
        if direction_group in [DirectionGroup.POLYGONAL, DirectionGroup.STAR]:
            values = range(1, vertex_count + 1)
        values_set = set(values)
    else:
        if direction_group in [DirectionGroup.POLYGONAL, DirectionGroup.STAR]:
            shname = "Star" if direction_group == DirectionGroup.STAR else "Polygon"
            try:
                values = [int(val) for val in values]
            except (NameError, TypeError, ValueError):
                feedback(
                    f'Unable to use "{value}" as direction(s) for a {shname}.', False
                )
                vrange = f"to {vertex_count}" if vertex_count else "onwards"
                feedback(
                    f"The {shname} directions must be whole numbers from 1 {vrange}.",
                    True,
                )
            values_set = set(values)
    if values_set.issubset(valid) or not vertex_count:
        # NOTE in some cases, we need to ignore `vertex_count` because not yet known...
        return list(values)
    _label = f"the {label} value" if label else f'"{value}"'
    feedback(
        f'Cannot use {_label} "{value}" - it must correspond with '
        f"the valid directions {valid}!",
        True,
    )
    return []


def transpose_lists(
    original_list: list, direction: str | None = None, invert: str | None = None
) -> list:
    """Reorientate a list-of-lists

    Args:
        original_list (list)
            a list of lists
        direction (str)
            'south' / 's' / '-90' or  'north' / 'n' / '90' to swop rows with columns
        invert (str)
            'lr' or 'tb' to reverse order of sub-lists within outer list

    Doc Test:

    >>> transpose_lists([[1, 2, 3], [4, 5, 6]], direction=None, invert=None)
    [[1, 2, 3], [4, 5, 6]]
    >>> transpose_lists([[1, 2, 3], [4, 5, 6]], direction=None, invert='LR')
    [[3, 2, 1], [6, 5, 4]]
    >>> transpose_lists([[1, 2, 3], [4, 5, 6]], direction=None, invert='TB')
    [[4, 5, 6], [1, 2, 3]]
    >>> transpose_lists([[1, 2, 3], [4, 5, 6]], direction=90, invert=None)
    [[3, 6], [2, 5], [1, 4]]
    >>> transpose_lists([[1, 2, 3], [4, 5, 6]], direction=270, invert=None)
    [[4, 1], [5, 2], [6, 3]]
    >>> transpose_lists([[1, 2, 3], [4, 5, 6]], direction=90, invert='LR')
    [[1, 4], [2, 5], [3, 6]]
    >>> transpose_lists([[1, 2, 3], [4, 5, 6]], direction=270, invert='LR')
    [[6, 3], [5, 2], [4, 1]]
    >>> transpose_lists([[1, 2, 3], [4, 5, 6]], direction=90, invert='TB')
    [[6, 3], [5, 2], [4, 1]]
    >>> transpose_lists([[1, 2, 3], [4, 5, 6]], direction=270, invert='TB')
    [[1, 4], [2, 5], [3, 6]]
    >>> transpose_lists([[1,0], [1,0], [1,0], [1,1], ], direction=90, invert='TB')
    [[1, 0, 0, 0], [1, 1, 1, 1]]
    """

    def row_col_swop(matrix):
        num_cols = len(matrix[0])
        swopped_matrix = [[row[i] for row in matrix] for i in range(num_cols)]
        return swopped_matrix

    transpose_copy = copy.copy(original_list)
    match str(invert).lower():
        case "lr" | "leftright" | "rl" | "rightleft":
            for al in transpose_copy:
                al.reverse()
        case "tb" | "topbottom" | "bt" | "bottomtop":
            transpose_copy.reverse()
        case _:
            pass

    match str(direction).lower():
        case "s" | "south" | "-90" | "270":
            transpose_copy = row_col_swop(transpose_copy)
            for al in transpose_copy:
                al.reverse()
        case "n" | "north" | "90":
            transpose_copy = row_col_swop(transpose_copy)
            transpose_copy.reverse()
        case _:
            pass
    return transpose_copy


def is_url_valid(url: str, qualifying=MIN_ATTRIBUTES):
    """Test if a URL is valid.

    See: https://stackoverflow.com/a/36283503/154858

    Doc Test:

    >>> is_url_valid(None)
    False
    >>> is_url_valid('')
    False
    >>> is_url_valid({})
    False
    >>> is_url_valid('naboo')
    False
    >>> is_url_valid('"file:///yoda.txt')
    False
    >>> is_url_valid('httpx://www.google.com')
    False
    >>> is_url_valid('https://https://https://www.foo.bar')
    False

    >>> is_url_valid('https://www.google.com')
    True
    >>> is_url_valid('https://www.tiktok.com/@outlikethevapors')
    True
    >>> is_url_valid('https://-wee.com')
    True
    >>> is_url_valid('http://localhost:8080')
    True
    """
    tokens = urlparse(url)
    if tokens.scheme and tokens.scheme not in ["http", "https"]:
        return False
    if tokens.netloc:
        if tokens.netloc[0:4] == "http" or tokens.netloc[0:5] == "https":
            return False
    return all(getattr(tokens, qualifying_attr) for qualifying_attr in qualifying)


def save_globals() -> GlobalDocument:
    """Create a copy of key globals settings"""
    return GlobalDocument(
        base=globals.base,
        deck=globals.deck,
        card_frames=globals.card_frames,
        filename=globals.filename,
        directory=globals.directory,
        document=globals.document,
        doc_page=globals.doc_page,
        canvas=globals.canvas,
        margins=globals.margins,
        page=globals.page,
        page_fill=globals.page_fill,
        page_width=globals.page_width,
        page_height=globals.page_height,
        page_count=globals.page_count,
        page_grid=globals.page_grid,
    )


def restore_globals(doc: GlobalDocument):
    """Restore key globals settings"""
    globals.base = doc.base
    globals.deck = doc.deck
    globals.card_frames = doc.card_frames
    globals.filename = doc.filename
    globals.directory = doc.directory
    globals.document = doc.document
    globals.doc_page = doc.doc_page
    globals.canvas = doc.canvas
    globals.margins = doc.margins
    globals.page = doc.page
    globals.page_fill = doc.page_fill
    globals.page_width = doc.page_width
    globals.page_height = doc.page_height
    globals.page_count = doc.page_count
    globals.page_grid = doc.page_grid


def unit(
    item, units: str | None = None, skip_none: bool = False, label: str = ""
) -> float:
    """Convert an item into the appropriate unit system."""
    log.debug("units %s :: label: %s", units, label)
    if item is None and skip_none:
        return 0.0
    _units = to_units(units) if units is not None else globals.units
    try:
        _item = as_float(item, label)
        return _item * _units
    except (TypeError, ValueError):
        _label = f" {label}" if label else ""
        feedback(
            f"Unable to set unit value for{_label}: {item}."
            " Please check that this is a valid value.",
            stop=True,
        )
    return 0.0


def points(item, units: str | None = None, skip_none: bool = False, label: str = ""):
    """Convert an item from points into the appropriate unit system."""
    log.debug("units %s :: label: %s", units, label)
    if item is None and skip_none:
        return None
    _units = to_units(units) if units is not None else globals.units
    try:
        _item = as_float(item, label)
        if _item is not None and _units is not None:
            return _item / _units
    except (TypeError, ValueError):
        _label = f" {label}" if label else ""
        feedback(
            f"Unable to set points value for{_label}: {item}."
            " Please check that this is a valid value.",
            stop=True,
        )


def get_pymupdf_props(
    defaults=None,
    index=None,  # extract from list of potential values (usually Card options)
    **kwargs,
):
    """Get pymupdf properties for fill, font, line, line style, colors and rotation

    Notes:
        If letting default a color parameter to None, then no resp. color selection
        command will be generated. If fill and color are both None, then the drawing
        will contain no color specification. But it will still be “stroked”,
        which causes PDF’s default color “black” be used by PDF viewers.

        The default value of width is 1.

        The values width, color and fill have the following relationship:

        - If fill=None, then shape elements will *always* be drawn with a border -
          even if color=None (in which case black is taken) or width=0
          (in which case 1 is taken).
        - Shapes without border can only be achieved if a fill color is specified
          (which may be be white). To achieve this, specify width=0.
          In this case, the color parameter is ignored.
    """

    def ext(prop) -> str:
        if isinstance(prop, str):
            return prop
        try:
            return prop[index]
        except TypeError:
            return prop

    defaults = defaults if defaults else {}
    if "fill" in kwargs:
        fill = kwargs.get("fill", None)  # reserve None for 'no fill at all'
    else:
        fill = defaults.get("fill")
    if "stroke" in kwargs:
        stroke = kwargs.get("stroke", None)  # reserve None for 'no stroke at all'
    else:
        stroke = defaults.get("stroke", None)
    # ---- transparency / opacity
    opacity = 1
    _transparency = kwargs.get("transparency", defaults.get("transparency"))
    if _transparency:
        _transparency = as_float(_transparency, "transparency")
        if _transparency >= 1:
            _transparency = _transparency / 100.0
        opacity = 1 - _transparency
    stroke_width = kwargs.get("stroke_width", None)
    # ---- set line end style
    stroke_cap = 0  # default is "sharp"
    line_join = kwargs.get("lineJoin", 0)  # default is "sharp"
    if kwargs.get("stroke_ends", None):  # shape centered at end-of-line
        ends = _lower(kwargs.get("stroke_ends"))
        if ends in ["rounded", "r", "round"]:
            stroke_cap = 1  # circle; diameter equal to line width
            line_join = 1  # rounded
        elif ends in ["squared", "s", "square"]:
            stroke_cap = 2  # square; side equal to line width
            line_join = 2  # butt; cut-off edge
        else:
            feedback(
                f'The ends value "{kwargs.get("stroke_ends")}" is not valid.', True
            )
    # ---- set rotation
    _rotation = kwargs.get("rotation", None)  # calling Shape must set a tuple!
    _rotation_point = kwargs.get(
        "rotation_point", None
    )  # calling Shape must set a tuple!
    closed = kwargs.get("closed", False)  # whether to connect last and first points
    # ---- set line dots / dashed
    dotted = kwargs.get("dotted", None)
    dashed = kwargs.get("dashed", None)
    _dotted = ext(dotted) or ext(defaults.get("dotted"))
    _dashed = ext(dashed) or ext(defaults.get("dashed"))
    if _dotted:
        the_stwd = (
            round(stroke_width)
            if stroke_width
            else round(defaults.get("stroke_width", 0.1))
        )
        the_stwd = max(the_stwd, 1)
        dashes = f"[{the_stwd} {the_stwd}] 0"
    elif _dashed:
        _dlist = (
            _dashed
            if isinstance(_dashed, (list, tuple))
            else sequence_split(_dashed, to_int=False)
        )
        doffset = round(unit(_dlist[2])) if len(_dlist) >= 3 else 0
        dspaced = round(unit(_dlist[1])) if len(_dlist) >= 2 else ""
        dlength = round(unit(_dlist[0])) if len(_dlist) >= 1 else ""
        dashes = f"[{dlength} {dspaced}] {doffset}"
    else:
        dashes = None
    # ---- check rotation
    morph = None
    if _rotation_point and not isinstance(_rotation_point, (Point, muPoint)):
        feedback(f'Rotation point "{_rotation_point}" is invalid', True)
    if _rotation is not None and not isinstance(_rotation, (float, int)):
        feedback(f'Rotation angle "{_rotation}" is invalid', True)
    if _rotation and _rotation_point:
        # ---- * set rotation matrix
        mtrx = Matrix(1, 1)
        mtrx.prerotate(_rotation)
        morph = (_rotation_point, mtrx)
    # ---- get color tuples
    _color = colrs.get_color(stroke)
    _fill = colrs.get_color(fill)
    # ---- set width
    _width = stroke_width or defaults.get("stroke_width")
    if _color is None and _fill is None:
        # feedback("Cannot have both fill and stroke set to None!", True)
        return None
    # print(f'^^^ SCP {stroke=} {fill=} {_color=} {_fill=} {line_join=}')  # None OR fraction RGB
    # ---- set/apply properties
    pymu_props = ShapeProperties(
        width=_width,
        color=_color,
        fill=_fill,
        lineCap=stroke_cap or 0,
        lineJoin=line_join,
        dashes=dashes,
        fill_opacity=opacity,
        morph=morph,
        closePath=closed,
    )
    return pymu_props


def set_canvas_props(
    cnv=None,
    index=None,  # extract from list of potential values (usually Card options)
    defaults=None,
    **kwargs,
):
    """Set pymupdf Shape properties for fill, font, line, line style and colors"""
    cnv = cnv if cnv else globals.canvas
    defaults = defaults if defaults else {}
    pymu_props = get_pymupdf_props(defaults=defaults, index=index, **kwargs)
    # print(f"--- tools {pymu_props=}")
    if pymu_props:
        try:
            cnv.finish(
                width=as_float(pymu_props.width, "width"),
                color=pymu_props.color,
                fill=pymu_props.fill,
                lineCap=pymu_props.lineCap,
                # FIXME : MuPDF error: syntax error: unknown keyword: 'lineJoin'?
                # lineJoin=pymu_props.lineJoin,
                dashes=pymu_props.dashes,
                fill_opacity=pymu_props.fill_opacity,
                morph=pymu_props.morph,
                closePath=pymu_props.closePath,
            )
        except Exception as err:
            feedback(f"Unexpected Error: {err}", True)
    cnv.commit()


def get_font_file(fonts_name: object) -> tuple:
    """Access and track a font and its file."""
    _name, font_path, _file = None, None, None
    if not fonts_name:
        return _name, font_path, _file
    if isinstance(fonts_name, str):
        font_names = [fonts_name]
    elif isinstance(fonts_name, list):
        font_names = fonts_name
    else:
        font_names = []
        feedback("Font name must be a string or a list of strings!", True)
    for name in font_names:
        _font_name = str(name).strip()
        if _font_name:
            _name = builtin_font(_font_name)
            if not _name:  # check for custom font
                cache_directory = Path(Path.home() / CACHE_DIRECTORY)
                fi = FontInterface(cache_directory=cache_directory)
                _name = fi.get_font_family(fonts_name)
                if not _name:
                    feedback(
                        f'Cannot find or load a Font named "{fonts_name}".',
                        False,
                        True,
                    )
                else:
                    _file = fi.get_font_file(fonts_name, fullpath=False)
                    font_path, css = fi.font_file_css(_name)
                    if css not in globals.css and css is not None:
                        globals.css += css + "\n"
                    globals.archive.add(font_path)
                    return _name, font_path, _file
    return _name, font_path, _file


def card_size(card_size: str, units: str = "pt") -> tuple | None:
    """Return card width and height in requested units for a named size.

    Doc Test:

    >>> card_size('poker')
    (180, 252)
    >>> card_size('poker', 'in')
    (2.5, 3.5)
    >>> card_size('miniamerican', 'mm')
    (41.0, 63.0)
    """
    size = None
    if units not in ["pt", "mm", "in"]:
        feedback(f'Card size units "{units}" is unknown.', True)
    match str(card_size).lower():
        case "bridge" | "b":
            size = STANDARD_CARD_SIZES["bridge"][units]
        case "business" | "u":
            size = STANDARD_CARD_SIZES["business"][units]
        case "flash" | "f":
            size = STANDARD_CARD_SIZES["flash"][units]
        case "mini" | "m":
            size = STANDARD_CARD_SIZES["mini"][units]
        case "miniamerican" | "ma":
            size = STANDARD_CARD_SIZES["miniamerican"][units]
        case "minieuropean" | "me":
            size = STANDARD_CARD_SIZES["minieuropean"][units]
        case "mtg" | "magic":
            size = STANDARD_CARD_SIZES["mtg"][units]
        case "poker" | "p" | "mtg":
            size = STANDARD_CARD_SIZES["poker"][units]
        case "skat" | "s":
            size = STANDARD_CARD_SIZES["skat"][units]
        case "tarot" | "t":
            size = STANDARD_CARD_SIZES["tarot"][units]
        case "":
            pass
        case _:
            feedback(f'Card size "{card_size}" is unknown.', True)
    return size


def paper_size(paper_size: str, units: str = "pt") -> tuple | None:
    """Return paper width and height in requested units for a named size.

    Doc Test:

    >>> paper_size('A4')
    (595, 842)
    >>> paper_size('Legal', 'in')
    (8.5, 14)
    >>> paper_size('Notelet', 'pt')
    (270, 270)

    # >>> paper_size('A5', 'in')
    # (180, 252)
    """
    if units not in ["pt", "mm", "in"]:
        feedback(f'Paper size units "{units}" is unknown.', True)
    try:
        return PAPER_SIZES[paper_size][units]
    except KeyError:
        feedback(f'Paper size "{paper_size}" in "{units}" is unavailable.', True)
    return None


def uniques(key: str) -> list:
    """Unique values in a Data() dataset i.e. a list of equivalent dicts.

    Args:
        key (str): a key in each dict in the list of dicts

    Doc Test:

    >>> uniques(None)
    []
    >>> uniques('')
    []
    >>> uniques('test')
    []
    """
    if not key:
        return []
    unique_values = set()
    try:
        for d in globals.dataset:
            if key in d:
                unique_values.add(d[key])
    except AttributeError:
        pass
    return list(unique_values)


def html_img(text: str) -> str:
    """Replace an image placeholder with an HTML <img> tag.

    Note:
        * placeholder pattern is |:filename.png:| or |:filename.png 00:|
          where 00 will be a number representing the height
        * alternative placeholder pattern for SVG is |;filename.svg;| or
          |;filename 00 name;|
          where 00 will be a number representing the height and the name is
          a hexadecimal color to apply to replace ALL other colors in the SVG
        * the filename for an image must NOT contain spaces!
        * a `.png` will be added to the filename, if there is no extension

    Doc Test:

    >>> html_img('A.png')
    'A.png'
    >>> html_img('|:A.png')
    '|:A.png'
    >>> html_img('A.png:|')
    'A.png:|'
    >>> html_img('|:A.png and |:B:|')  # POOR OUTCOME!
    '<img src="A.png" height=and>'
    >>> html_img(' |:A.png:| and |:B:| ')
    ' <img src="A.png"> and <img src="B.png"> '
    >>> html_img('an |:A:| or')
    'an <img src="A.png"> or'
    >>> html_img('an |: A 20 :| or')
    'an <img src="A.png" height=20> or'
    """
    # ---- PNG
    images = re.findall(r"\|\:(.*?)\:\|", text)
    txt = text
    for img in images:
        _img = img.strip(" ")
        items = _img.split(" ")
        image_name = items[0]
        _, ext = os.path.splitext(image_name)
        if not ext:
            image_name = image_name + ".png"
        if len(items) > 1:
            txt = txt.replace(img, f'<img src="{image_name}" height={items[1]}>')
        else:
            txt = txt.replace(img, f'<img src="{image_name}">')
    if images:
        txt = txt.replace("|:", "").replace(":|", "")
    # ---- SVG
    svg_images = re.findall(r"\|\;(.*?)\;\|", txt)
    for img in svg_images:
        _img = img.strip(" ")
        items = _img.split(" ")
        image_name = items[0]
        _, ext = os.path.splitext(image_name)
        if not ext:
            image_name = image_name + ".svg"
        if len(items) > 1 and len(items) < 3:
            txt = txt.replace(img, f'<img src="{image_name}" height={items[1]}>')
        elif len(items) >= 3:
            txt = txt.replace(img, f'<img src="{image_name}" height={items[1]}>')
        else:
            txt = txt.replace(img, f'<img src="{image_name}">')
    if svg_images:
        txt = txt.replace("|;", "").replace(";|", "")
    return txt


def html_glyph(text: str, font_name: str, font_size: str = "") -> str:
    """Replace a Unicode glyph placeholder with font details in a <span> tag.

    Note:
        * placeholder pattern is |!unicode!| or |!unicode 00!|
          |!unicode 00 #COLOR !|
          where 00 will be a number representing the font size and #COLOR
          is a hexadecimal color for the font color
        * the glyph's unicode MUST appear in the Font matching `font_name`
        * the font_size, if any, will be overridden by any value used in the
          placeholder

    Doc Test:

    >>> html_glyph('E001', "Helvetica")
    'E001'
    >>> html_glyph('|!E001', "Helvetica")
    '|!E001'
    >>> html_glyph('E001!|', "Helvetica")
    'E001!|'
    >>> html_glyph('an |! E001 12 !| or', "Helvetica")
    'an <span style="font-family: Helvetica; font-size: 12px;">E001</span> or'
    >>> html_glyph('an |! E001 12 #000 !| or', "Helvetica")
    'an <span style="font-family: Helvetica; font-size: 12px; color: #000;">E001</span> or'

    """
    glyphs = re.findall(r"\|\!(.*?)\!\|", text)
    txt = text
    for glp in glyphs:
        _glp = glp.strip(" ")
        items = _glp.split(" ")
        glyph_name = items[0]
        # <span style="font-family: sans-serif; font-size: 14px; color: blue;">Hello World!</span>
        if len(items) > 2:
            txt = txt.replace(
                glp,
                f'<span style="font-family: {font_name}; font-size: {items[1]}px; color: {items[2]};">{glyph_name}</span>',
            )
        if len(items) > 1:
            txt = txt.replace(
                glp,
                f'<span style="font-family: {font_name}; font-size: {items[1]}px;">{glyph_name}</span>',
            )
        else:
            if font_size:
                txt = txt.replace(
                    glp,
                    f'<span style="font-family: {font_name}; ; font-size:{font_size}">{glyph_name}</span',
                )
            else:
                txt = txt.replace(
                    glp, f'<span style="font-family: {font_name}">{glyph_name}</span'
                )
    if glyphs:
        txt = txt.replace("|!", "").replace("!|", "")
    return txt


if __name__ == "__main__":
    import doctest

    doctest.testmod()
