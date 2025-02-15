# -*- coding: utf-8 -*-
"""
General purpose utility functions for protograf
"""
# lib
from collections import namedtuple
import cmath
import csv
import collections
from enum import Enum
from itertools import zip_longest
import jinja2
import logging
import math
import os
import pathlib
import string
import sys
from urllib.parse import urlparse
import xlrd

# third party
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont, TTFError
from reportlab.pdfbase.pdfmetrics import registerFontFamily

# local
from protograf.utils.support import numbers, feedback

log = logging.getLogger(__name__)
DEBUG = False
MIN_ATTRIBUTES = ("scheme", "netloc")
BUILTIN_FONTS = ["Times-Roman", "Courier", "Helvetica"]


class FontStyleType(Enum):
    REGULAR = 1
    BOLD = 2
    ITALIC = 3
    BOLDITALIC = 4


class DatasetType(Enum):
    FILE = 1
    DICT = 2
    MATRIX = 3
    IMAGE = 4


class DirectionGroup(Enum):
    CARDINAL = 1
    COMPASS = 2
    HEX_FLAT = 3  # vertex
    HEX_POINTY = 4
    HEX_FLAT_EDGE = 4  # edge
    HEX_POINTY_EDGE = 5
    CIRCULAR = 6


class CardFrame(Enum):
    RECTANGLE = 1
    HEXAGON = 2
    CIRCLE = 3


class HexOrientation(Enum):
    FLAT = 1
    POINTY = 2


def script_path():
    """Get the path for a script being called from command line."""
    fname = os.path.abspath(sys.argv[0])
    if fname:
        return pathlib.Path(fname).resolve().parent


def load_data(datasource=None, **kwargs):
    """
    Load data from a 'tabular' source (CSV, XLS) into a dict
    """
    dataset = {}
    log.debug("Load data from a 'tabular' source (CSV, XLS) %s", datasource)
    if datasource:
        filename, file_ext = os.path.splitext(datasource)
        if file_ext.lower() == ".csv":
            headers = kwargs.get("headers", None)
            selected = kwargs.get("selected", None)
            dataset = open_csv(datasource, headers=headers, selected=selected)
        elif file_ext.lower() == ".xls":
            headers = kwargs.get("headers", None)
            selected = kwargs.get("selected", None)
            sheet = kwargs.get("sheet", 0)
            sheetname = kwargs.get("sheetname", None)
            dataset = open_xls(
                datasource,
                sheet=sheet,
                sheetname=sheetname,
                headers=headers,
                selected=selected,
            )
        else:
            feedback('Unable to process a file %s of type "%s"' % (filename, file_ext))
    return dataset


def grouper(n, iterable, fillvalue=None):
    """group and return sets

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
    """Create a result from boolean concatenation

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


def as_int(value, label, maximum=None, minimum=None, allow_none=False) -> int:
    """Set a value to an int; or stop if an invalid value

    Doc Test:

    >>> as_int(value='3', label='N')
    3

    # below cannot be tested because of sys.exit() in feedback()
    # >>> as_int(value='3', label='N', minimum=4)
    # FEEDBACK:: z is
    # >>> as_int(value='3', label='N', maximum=2)
    # FEEDBACK:: z is
    # >>> as_int(value='z', label='N')
    # FEEDBACK:: z is not a valid N integer!
    # >>> as_int(value='3.1', label='N')
    # FEEDBACK:: 3.1 is not a valid N integer!
    """
    if value is None or value == "" and allow_none:
        return value
    _label = f" for {label}" if label else " of"
    try:
        the_value = int(value)
        if minimum and the_value < minimum:
            feedback(
                f"The value{_label} integer is less than the minimum of {minimum}!",
                True,
            )
        if maximum and the_value > maximum:
            feedback(
                f"The value{_label} integer is more than the maximum of {maximum}!",
                True,
            )
        return the_value
    except (ValueError, Exception):
        feedback(f"The {value}{label} is not a valid integer!", True)


def as_bool(value, label=None, allow_none=True) -> bool:
    """Convert a value to a boolean

    Doc Test:

    >>> as_bool(value='3', label='N')
    False
    >>> as_bool(value='Y', label='Y')
    True
    """
    if value is None and allow_none:
        return value
    _label = f" for {label}" if label else " of"
    result = str(value).lower() in ("yes", "ja", "oui", "y", "true", "t", "1")
    return result


def as_float(value, label, maximum=None, minimum=None, stop=True, default=None) -> int:
    """Set a value to an float; or end program if an invalid value and stop is True

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
            feedback(f'The value "{value}"{label} is not a valid float number!', True)
        else:
            return None


def tuple_split(
    string: str, label: str = "list", pairs_list: bool = False, all_ints: bool = False
) -> list:
    """
    Split a string into a list of tuple numbers

    Doc Test:

    >>> print(tuple_split(''))
    []
    >>> print(tuple_split('3'))
    [(3.0,)]
    >>> print(tuple_split('3,4'))
    [(3.0, 4.0)]
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
    if string:
        try:
            _string_list = string.strip(" ").replace(";", ",").split(" ")
            for _str in _string_list:
                items = _str.split(",")
                if all_ints:
                    _items = [int(itm) for itm in items]
                else:
                    _items = [float(itm) for itm in items]
                values.append(tuple(_items))
            if pairs_list:
                for value in values:
                    if len(value) != 2:
                        feedback(
                            f"Values of {label} must be pairs of integers!",
                            f' Check if all values in "{string}" are integer pairs.',
                            True,
                        )
            return values
        except ValueError:
            if all_ints:
                feedback(
                    f"Cannot convert {label} into a list of integer sets!"
                    f' Check if all values in "{string}" are integers.',
                    True,
                )
            else:
                feedback(f"Cannot convert {label} into a list of numeric sets!", True)
            return values

        except Exception:
            return values
    else:
        return values


def sequence_split(
    string: str, as_int: bool = True, unique: bool = True, sep: str = ","
):
    """
    Split a string into a list of individual values

    Note:
        * If `unique` is True, order will NOT be maintained!

    Doc Test:

    >>> sequence_split('')
    []
    >>> sequence_split('3')
    [3]
    >>> sequence_split('3', False)
    ['3']
    >>> sequence_split('3,4,5')
    [3, 4, 5]
    >>> sequence_split('3,4,5', False, False)
    ['3', '4', '5']
    >>> x = sequence_split('3,4,5', False)
    >>> assert '5' in x
    >>> sequence_split('3-5,6,1-4')
    [1, 2, 3, 4, 5, 6]
    >>> sequence_split('A,1,B', False, False)
    ['A', '1', 'B']
    """
    values = []
    if string:
        try:
            if sep == ",":
                _string = (
                    string.replace(" ", "")
                    .replace('"', "")
                    .replace("'", "")
                    .replace(";", ",")
                )
            else:
                _string = string
        except Exception:
            return values
    else:
        return values
    # simple single value
    try:
        if as_int:
            values.append(int(_string))
            return values
    except Exception:
        pass
    # multi-values
    _strings = _string.split(sep)
    # log.debug('strings:%s', _strings)
    for item in _strings:
        if "-" in item:
            _strs = item.split("-")
            seq_range = list(range(int(_strs[0]), int(_strs[1]) + 1))
            if not as_int:
                seq_range = [str(val) for val in seq_range]
            values = values + seq_range
        else:
            if as_int:
                values.append(int(item))
            else:
                values.append(item)

    if unique:
        return list(set(values))  # unique
    return values


def split(string: str):
    """
    Split a string into a list of individual characters

    Doc test:
    >>> split('A,1,B')
    ['A', '1', 'B']
    >>> split('A 1 B')
    ['A', '1', 'B']
    """
    if isinstance(string, (list, tuple)):
        return string
    sep = " " if string and "," not in string else ","
    return sequence_split(string, False, False, sep)


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


def splitq(seq, sep=None, pairs=("()", "[]", "{}"), quote="\"'"):
    """Split sequence by separator but considering parts inside pairs or quoted
       as unbreakable pairs have different start and end value, quote have same
       symbol in beginning and end.

    Notes:
        * Use itertools.islice if only part of splits is needed

    Source:
        https://www.daniweb.com/programming/software-development/code/426990/\
        split-string-except-inside-brackets-or-quotes
    """
    if not seq:
        yield []
    else:
        lsep = len(sep) if sep is not None else 1
        lpair, _ = zip(*pairs)
        pairs = dict(pairs)
        start = index = 0
        while 0 <= index < len(seq):
            c = seq[index]
            if (sep and seq[index:].startswith(sep)) or (sep is None and c.isspace()):
                yield seq[start:index]
                # pass multiple separators as single one
                if sep is None:
                    index = len(seq) - len(seq[index:].lstrip())
                else:
                    while sep and seq[index:].startswith(sep):
                        index = index + lsep
                start = index
            elif c in quote:
                index += 1
                p, index = index, seq.find(c, index) + 1
                if not index:
                    raise IndexError("Unmatched quote %r\n%i:%s" % (c, p, seq[:p]))
            elif c in lpair:
                nesting = 1
                while True:
                    index += 1
                    p, index = index, seq.find(pairs[c], index)
                    if index < 0:
                        raise IndexError(
                            "Did not find end of pair for %r: %r\n%i:%s"
                            % (c, pairs[c], p, seq[:p])
                        )
                    nesting += "{lpair}({inner})".format(
                        lpair=c, inner=splitq(seq[p:index].count(c) - 2)
                    )
                    if not nesting:
                        break
            else:
                index += 1
        if seq[start:]:
            yield seq[start:]


def open_csv(filename, headers=None, selected=None):
    """Read data from CSV file into a list of dictionaries

    Supply:

      * headers is a list of strings to use instead of the first row
      * selected is a list of desired rows e.g. [2,4,7]
    """
    if not filename:
        feedback("A valid CSV filename must be supplied!")

    dict_list = []
    _file_with_path = None
    norm_filename = os.path.normpath(filename)
    if not os.path.exists(norm_filename):
        filepath = script_path()
        _file_with_path = os.path.join(filepath, norm_filename)
        if not os.path.exists(_file_with_path):
            feedback(f'Unable to find CSV "{filename}", including in {filepath}')

    try:
        csv_filename = _file_with_path or norm_filename
        if headers:
            reader = csv.DictReader(open(csv_filename), fieldnames=headers)
        else:
            reader = csv.DictReader(open(csv_filename))
        for key, item in enumerate(reader):
            if not selected:
                dict_list.append(item)
            else:
                if key + 1 in selected:
                    dict_list.append(item)
    except IOError:
        feedback('Unable to find or open CSV "%s"' % csv_filename)
    return dict_list


def open_xls(filename, sheet=0, sheetname=None, headers=None, selected=None):
    """Read data from XLS file into a list of dictionaries

    Supply:

      * sheet to select a sheet number (otherwise first is used)
      * sheetname to select a sheet by name (otherwise first is used)
      * headers is a list of strings to use instead of the first row
      * selected is a list of desired rows e.g. [2,4,7]
    """

    def cleaned(value):
        if isinstance(value, float):
            if float(value) == float(int(value)):
                return int(value)
        # if isinstance(value, str):
        #     return value.encode('utf8')
        return value

    if not filename:
        feedback("A valid Excel filename must be supplied!")

    dict_list = []

    _file_with_path = None
    norm_filename = os.path.normpath(filename)
    if not os.path.exists(norm_filename):
        filepath = script_path()
        _file_with_path = os.path.join(filepath, norm_filename)
        if not os.path.exists(_file_with_path):
            feedback(f'Unable to find "{filename}", including in {filepath}')

    try:
        excel_filename = _file_with_path or norm_filename
        book = xlrd.open_workbook(excel_filename)
        if sheet:
            sheet = sheet - 1
            sheet = book.sheet_by_index(sheet)
        elif sheetname:
            sheet = book.sheet_by_name(sheetname)
        else:
            sheet = book.sheet_by_index(0)
        start = 1
        if not headers:
            keys = [sheet.cell(0, col_index).value for col_index in range(sheet.ncols)]
        else:
            start = 0
            keys = headers
        if len(keys) < sheet.ncols:
            feedback(
                'Too few headers supplied for the existing columns in "%s"' % filename
            )
        else:
            dict_list = []
            for row_index in range(start, sheet.nrows):
                item = {
                    keys[col_index]: cleaned(sheet.cell(row_index, col_index).value)
                    for col_index in range(sheet.ncols)
                }
                if not selected:
                    dict_list.append(item)
                else:
                    if row_index + 1 in selected:
                        dict_list.append(item)
    except IOError:
        feedback('Unable to find or open Excel "%s"' % excel_filename)
    except IndexError:
        feedback('Unable to open sheet "%s"' % (sheet or sheetname))
    except xlrd.biffh.XLRDError:
        feedback('Unable to open sheet "%s"' % sheetname)
    return dict_list


def flatten(lst):
    """Flatten nested lists into a single list of lists.

    >>> list(flatten([[1, 2], [3,4, [5,6]]]))
    [1, 2, 3, 4, 5, 6]
    """
    try:
        for ele in lst:
            if isinstance(ele, collections.abc.Iterable) and not isinstance(ele, str):
                for sub in flatten(ele):
                    yield sub
            else:
                yield ele
    except TypeError:
        yield lst


def flatten_keys(d: dict):
    """Flatten nested dicts into a single dict.

    NOTE:
        * values for keys in nested dict will override those in parent(s)!
        * See: https://www.geeksforgeeks.org/python-flatten-nested-keys/

    >>> flatten_keys({'height': 8, 'cards': 1, 'image': None, 'kwargs': {'kwargs': {'image': 'FOO', 'kwargs': {'cards': 9}}}})
    {'height': 8, 'cards': 9, 'image': 'FOO'}
    """
    result = {}
    for k, v in d.items():
        if isinstance(v, dict):
            flat_v = flatten_keys(v)
            for flat_k, flat_v in flat_v.items():
                # result[k + '.' + flat_k] = flat_v
                result[flat_k] = flat_v
        elif isinstance(v, list):
            for i, item in enumerate(v):
                try:
                    flat_item = flatten_keys(item)
                except AttributeError:
                    flat_item = item
                if isinstance(flat_item, dict):
                    for flat_k, flat_v in flat_item.items():
                        # result[f"{k}.{i}.{flat_k}"] = flat_v
                        result[f"{flat_k}"] = flat_v
        else:
            result[k] = v
    return result


def comparer(val, operator, target):
    """target could be list?? - split a string by , or ~

    >>> comparer(None, None, None)
    True
    >>> comparer("1", '*', "1")
    FEEDBACK:: Unknown operator: * (1.0 and 1.0)
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
    False
    >>> comparer("a", '~', "aa")
    True
    >>> comparer("True", '~', "True")
    False
    >>> comparer("False", '~', "False")
    False
    >>> comparer("1", '~', [1,2,3])
    True
    """

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

    if target == "T" or target == "True":
        target = True
    if target == "F" or target == "False":
        target = False
    if val == "T" or val == "True":
        val = True
    if val == "F" or val == "False":
        val = False

    if not operator:
        operator = "="
    if operator in ["<", "<=", ">", ">="]:
        val, target = to_length(val, target)

    try:
        val = float(val)
    except Exception:
        pass
    try:
        target = float(target)
    except Exception:
        pass
    if operator == "=":
        if val == target:
            return True
    elif operator == "~" or operator == "in":
        try:
            if val in target:
                return True
        except TypeError:
            pass
    elif operator == "!=":
        if val != target:
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
    else:
        feedback("Unknown operator: %s (%s and %s)" % (operator, val, target))
    return False


def color_to_hex(name):
    """Convert a named ReportLab color (Color class) to a hexadecimal string"""
    if isinstance(name, str):
        return name
    _tuple = (int(name.red * 255), int(name.green * 255), int(name.blue * 255))
    _string = "#%02x%02x%02x" % _tuple
    return _string.upper()


def alpha_column(num: int, lower: bool = False) -> string:
    """Convert a number to a letter-based notation

    Notes:
        * Encountered on a WarpWar map; numbers below 26 appear sequentially as
          a, b, c, etc, numbers above 26 appear sequentially as aa, bb, cc, etc; if
          above 52 then appear sequentially as aaa, bbb, ccc etc. Add more letters for
          each multiple of 26.
    """
    if lower:
        return string.ascii_lowercase[divmod(num - 1, 26)[1] % 26] * (
            divmod(num - 1, 26)[0] + 1
        )
    else:
        return string.ascii_uppercase[divmod(num - 1, 26)[1] % 26] * (
            divmod(num - 1, 26)[0] + 1
        )


def register_font(
    font_name: str = None,
    style: str = None,
    directory: str = None,
    filename: str = None,
):
    """Use likely combos of name and styles to register font and family styles."""

    def register_font_style(
        font_name: str,
        font_type: FontStyleType,
        style: str = None,
        directory: str = None,
        filename: str = None,
    ):
        """Use pdfmetrics to registerFont, linked to a font file, for a style type.

        Args:
            style
                use the name of a specific style e.g. Light or Thin or Medium
                to register a single specific style; useful when a font does
                not actually have a Regular
            filename
                the actual filename might not be based on the font name;
                supply this instead
        """
        font_name = font_name.strip(" ")
        match font_type:
            case FontStyleType.REGULAR:
                fstyles = [style] if style else ["", "Regular", "R", "Rg"]
                style_name = f"{font_name}"
            case FontStyleType.BOLD:
                fstyles = ["Bold", "Bo", "Bd", "B"]
                style_name = f"{font_name} Bold"
            case FontStyleType.ITALIC:
                fstyles = ["Italic", "It", "I", "Oblique", "Ob", "O"]
                style_name = f"{font_name} Italic"
            case FontStyleType.BOLDITALIC:
                fstyles = ["BoldItalic", "BoIt", "BI", "BoldOblique", "BoOb", "BO", "Z"]
                style_name = f"{font_name} Bold Italic"

        base_names = list(
            set(
                [
                    font_name,
                    str(font_name).replace(" ", "_"),
                    str(font_name).replace(" ", "-"),
                ]
            )
        )
        file_seps = ["", "-", "_", " "]
        directory = "" if directory is None else directory
        path = directory if os.path.exists(directory) else ""
        for base_name in base_names:
            for style in fstyles:
                for sep in file_seps:
                    if filename:
                        _file_name = f"{filename}{sep}{style}.ttf"
                    else:
                        _file_name = f"{base_name}{sep}{style}.ttf"
                    full_file_name = os.path.join(path, _file_name)
                    full_file_name_lower = os.path.join(path, full_file_name.lower())
                    filenames = [full_file_name, full_file_name_lower]
                    for fname in filenames:
                        # print(f'{style_name=} {fname=}')
                        try:
                            pdfmetrics.registerFont(TTFont(style_name, fname))
                            # print(f'Registered:  {style_name} file:{fname}')
                            return style_name
                        except TTFError:
                            pass
        return None

    if not font_name:
        feedback("No font name supplied for registration!", True)
    if font_name in BUILTIN_FONTS:
        return  # font families available in ReportLab without registration

    # get base font
    font_regular = register_font_style(
        font_name, FontStyleType.REGULAR, style, directory, filename
    )
    if not font_regular:
        raise TTFError
    # possble additional styles
    kwargs = {}
    kwargs["bold"] = register_font_style(
        font_name, FontStyleType.BOLD, style, directory, filename
    )
    kwargs["italic"] = register_font_style(
        font_name, FontStyleType.ITALIC, style, directory, filename
    )
    kwargs["boldItalic"] = register_font_style(
        font_name, FontStyleType.BOLDITALIC, style, directory, filename
    )
    # full family
    if font_regular and kwargs:
        # print(f'Register Family! {font_regular=} {kwargs=}')
        registerFontFamily(font_name.strip(" "), normal=font_regular, **kwargs)


def sheet_column(num: int, lower: bool = False) -> string:
    """Convert a spreadsheet number to a column letter

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
        else:
            return (
                ""
                if num == 0
                else converter((num - 1) // 26, lower)
                + string.ascii_uppercase[(num - 1) % 26]
            )

    return converter(num, lower)


def base_fonts():
    """Register MS Core Fonts

    NOTES:
        * On Ubuntu: sudo apt-get install ttf-mscorefonts-installer
        * The Windows filenames are 'truncated' versions, hence the use
          of an alternate
    """
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
        try:
            name = ffont["name"]
            register_font(name)
        except TTFError:
            try:
                alt = ffont.get("alternate")
                register_font(name, filename=alt)
            except TTFError:
                missing.append(name)
    if missing:
        names = ", ".join(missing)
        feedback(f"Unable to register the MS font(s): {names}", False, True)


def eval_template(string: str, data: dict = None, label: str = ""):
    """Process data dict via jinja2 template in source.

    Doc Test:
    >>> eval_template("2+{{x}}", {'x': 2})
    '2+2'
    >>> eval_template("2+{{x}}", {'y': 2})
    '2+'
    """
    if data is None or not data:
        return string
    if isinstance(data, tuple):
        try:
            data = data._asdict()
        except Exception:
            pass
    if not isinstance(data, dict):
        feedback("The data must be in the form of a dictionary", True)
    try:
        environment = jinja2.Environment()
        template = environment.from_string(str(string))
        custom_value = template.render(data)
        return custom_value
    except jinja2.exceptions.TemplateSyntaxError:
        feedback(
            f'Unable to create the text or value - check the grammar for "{string}"',
            True,
        )
    except (ValueError, jinja2.exceptions.UndefinedError):
        feedback(f'Unable to process "{string}" data with this template', True)


def validated_directions(
    value: list | str, direction_group: DirectionGroup, label: str = ""
) -> list:
    """Check and return a list of lowercase, direction abbreviations.

    Doc Test:
    # >>> validated_directions('', DirectionGroup.CARDINAL)
    # []
    # >>> validated_directions([], DirectionGroup.CARDINAL)
    # []
    # >>> validated_directions(['n', 's'], DirectionGroup.CARDINAL)
    # ['n', 's']
    # >>> validated_directions('n s', DirectionGroup.CARDINAL)
    # ['n', 's']
    # >>> validated_directions('n s', DirectionGroup.HEX_FLAT)
    # ['w', 'e']
    # >>> validated_directions('w e', DirectionGroup.HEX_POINTY)
    # ['n', 's']
    # >>> validated_directions('w e n s ne', DirectionGroup.COMPASS)
    # ['w', 'e', 'n', 's', 'ne']
    """
    if not value:
        return []
    if isinstance(value, str):
        values = split(value.lower())
    else:
        if not isinstance(value, list):
            feedback(f"Cannot handle {label}value - must be a string or a list!", True)
        values = [str(val).lower().strip() for val in value]
    values_set = set(values)
    match direction_group:
        case DirectionGroup.CARDINAL:
            valid = {"n", "e", "w", "s"}
        case DirectionGroup.COMPASS:
            valid = {"n", "e", "w", "s", "ne", "se", "sw", "nw"}
        case DirectionGroup.HEX_FLAT:
            valid = {"e", "se", "sw", "w", "ne", "nw"}
        case DirectionGroup.HEX_POINTY:
            valid = {"s", "se", "sw", "n", "ne", "nw"}
        case DirectionGroup.HEX_FLAT_EDGE:  # perbis
            valid = {"s", "se", "sw", "n", "ne", "nw"}
        case DirectionGroup.HEX_POINTY_EDGE:  # perbis
            valid = {"e", "se", "sw", "w", "ne", "nw"}
        case DirectionGroup.CIRCULAR:
            valid = {"n", "e", "w", "s", "ne", "se", "sw", "nw", "o", "d"}
        case _:
            raise NotImplementedError("Cannot handle {direction_group} type!")
    if "all" in values or "*" in values:
        values = list(valid)
        values_set = set(values)
    if values_set.issubset(valid):
        return values
    _label = f"the {label} value" if label else f'"{value}"'
    feedback(f"Cannot use {_label} - it must contain valid directions {valid}!", True)


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


if __name__ == "__main__":
    import doctest

    doctest.testmod()
