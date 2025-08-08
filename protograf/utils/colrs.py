# -*- coding: utf-8 -*-
"""
Color-specific utility functions for protograf
"""
# lib
from colorsys import rgb_to_hls, hls_to_rgb

# third-party
from pymupdf.utils import getColor

# local
from protograf.utils.constants import COLOR_NAMES
from protograf.utils.messaging import feedback


def get_color(name: str = None, is_rgb: bool = True) -> tuple:
    """Get a color tuple; by name from a pre-defined dictionary or as a RGB tuple."""
    if name is None:
        return None  # it IS valid to say that NO color has been set
    if isinstance(name, tuple) and len(name) == 3:  # RGB color tuple
        if (
            (name[0] >= 0 and name[0] <= 255)
            and (name[1] >= 0 and name[0] <= 255)
            and (name[2] >= 0 and name[0] <= 255)
        ):
            return name
        else:
            feedback(f'The color tuple "{name}" is invalid!')
    elif isinstance(name, str) and len(name) == 7 and name[0] == "#":  # hexadecimal
        _rgb = tuple(int(name[i : i + 2], 16) for i in (1, 3, 5))
        rgb = tuple(i / 255 for i in _rgb)
        return rgb
    else:
        pass  # unknown format
    try:
        if name.upper() not in COLOR_NAMES:
            feedback(f'The color name "{name}" is not pre-defined!', True)
        color = getColor(name)
        return color
    except (AttributeError, ValueError):
        feedback(f'The color name "{name}" cannot be converted to RGB!', True)


def get_opacity(transparency: float = 0) -> float:
    """Convert from '100% is fully transparent' to '0 is not opaque'."""
    if transparency is None:
        return 1.0
    try:
        return float(1.0 - transparency / 100.0)
    except (ValueError, TypeError):
        feedback(
            f'The transparency of "{transparency}" is not valid (use 0 to 100)', True
        )


def color_to_hex(name):
    """Convert a named color (Color class) to a hexadecimal string"""
    if isinstance(name, str):
        return name
    _tuple = (int(name.red * 255), int(name.green * 255), int(name.blue * 255))
    _string = "#%02x%02x%02x" % _tuple
    return _string.upper()


def rgb_to_hex(color: tuple) -> str:
    """Convert a RGB tuple color to a hexadecimal string

    Doc Test:

    >>> rgb_to_hex((123,45,6))
    '#7A852CD35FA'
    """
    if color is None:
        return color
    _tuple = (int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))
    _string = "#%02x%02x%02x" % _tuple
    return _string.upper()


def adjust_color_brightness(red, grn, blu, factor, as_hex=True):
    """Alter brightness of a RGB colour - lighter or darker.

    Args:

    - red (int): red color channel value; ranging from 0 to 255
    - grn (int): green color channel value; ranging from 0 to 255
    - blu (int): blue color channel value; ranging from 0 to 255
    - factor (float): amount of change to brightness
    - as_hex (bool): if True, return value as a Hexadecimal color string
    """
    h, l_t, s = rgb_to_hls(red / 255.0, grn / 255.0, blu / 255.0)
    l_t = max(min(l_t * factor, 1.0), 0.0)
    red, grn, blu = hls_to_rgb(h, l_t, s)
    _r, _g, _b = int(red * 255), int(grn * 255), int(blu * 255)
    if as_hex:
        return "#%02x%02x%02x" % (_r, _g, _b)
    else:
        return _r, _g, _b


def lighten_color(red, grn, blu, factor=0.1, as_hex=True):
    """Increase brightness of a RGB colour

    Args:

    - red (int): red color channel value; ranging from 0 to 255
    - grn (int): green color channel value; ranging from 0 to 255
    - blu (int): blue color channel value; ranging from 0 to 255
    - factor (float): amount of change to brightness
    - as_hex (bool): if True, return value as a Hexadecimal color string
    """
    return adjust_color_brightness(red, grn, blu, 1 + factor, as_hex)


def darken_color(red, grn, blu, factor=0.1, as_hex=True):
    """Decrease brightness of a RGB colour

    Args:

    - red (int): red color channel value; ranging from 0 to 255
    - grn (int): green color channel value; ranging from 0 to 255
    - blu (int): blue color channel value; ranging from 0 to 255
    - factor (float): amount of change to brightness
    - as_hex (bool): if True, return value as a Hexadecimal color string
    """
    return adjust_color_brightness(red, grn, blu, 1 - factor, as_hex)


def lighten_pymu(color, factor=0.1) -> tuple:
    """Increase brightness of a PyMuPDF colour tuple

    Args:

    - color (tuple): a (red, green, blue) fractional color channel tuple; from 0 to 1
    - factor (float): amount of change to brightness

    Returns:
        tuple: fractional R, G, B colors
    """
    red = color[0] * 255
    grn = color[1] * 255
    blu = color[2] * 255
    result = adjust_color_brightness(red, grn, blu, 1 + factor, False)
    return result[0] / 255, result[1] / 255, result[2] / 255


def darken_pymu(color, factor=0.1) -> tuple:
    """Decrease brightness of a PyMuPDF colour tuple

    Args:

    - color (tuple): a (red, green, blue) fractional color channel tuple; from 0 to 1
    - factor (float): amount of change to brightness

    Returns:
        tuple: fractional R, G, B colors
    """
    red = color[0] * 255
    grn = color[1] * 255
    blu = color[2] * 255
    result = adjust_color_brightness(red, grn, blu, 1 - factor, False)
    return result[0] / 255, result[1] / 255, result[2] / 255


def lighten(hex_color, factor=0.2, as_hex=True):
    """Increase brightness of a hexadecimal colour

    Args:

    - hex_color (str): Hexadecimal color string
    - factor (float): amount of change to brightness
    - as_hex (bool): if True, return value as a Hexadecimal color string

    Notes:

        Factor set to 0.2 for use in Cube shades
    """
    if not hex_color:
        return None
    if hex_color[0] != "#":
        feedback(f'"{hex_color}" is not a valid hexadecimal color', True)
    try:
        red, grn, blu = tuple(int(hex_color[i : i + 2], 16) for i in (1, 3, 5))
        return lighten_color(red, grn, blu, factor, as_hex)
    except (ValueError, TypeError):
        feedback(
            f'Unable to lighten "{hex_color}"; please check it is a valid color', True
        )


def darken(hex_color, factor=0.2, as_hex=True):
    """Decrease brightness of a Hexadecimal colour

    Args:

    - hex_color (str): Hexadecimal color string
    - factor (float): amount of change to brightness
    - as_hex (bool): if True, return value as a Hexadecimal color string

    Notes:

        Factor set to 0.2 for use in Cube shades
    """
    if not hex_color:
        return None
    if hex_color[0] != "#":
        feedback(f'"{hex_color}" is not a valid hexadecimal color', True)
    try:
        red, grn, blu = tuple(int(hex_color[i : i + 2], 16) for i in (1, 3, 5))
        return darken_color(red, grn, blu, factor, as_hex)
    except (ValueError, TypeError):
        feedback(
            f'Unable to darken "{hex_color}"; please check it is a valid color', True
        )


if __name__ == "__main__":
    import doctest

    doctest.testmod()
