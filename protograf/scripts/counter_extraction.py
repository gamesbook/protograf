# -*- coding: utf-8 -*-
"""
protograf script: extract rectangular counters as invididual images
"""
# lib
import configparser
from collections import namedtuple
import os
import sys

# third party
from wand.image import Image


def failure(message):
    """End the program with a message."""
    print(message)
    sys.exit(0) # Exit with status code 0 (success)


def as_int(
    value,
    label: str = None,
) -> int:
    """Convert a value to an int

    Args:

    - value (Any): the value to be converted to a float
    - label (str): assigned as part of the error message to ID the type of value
    """
    _label = f"{label} value " if label else "value "
    if value is None:
        failure(f'The {_label}"{value}" is not a valid integer!!')
    try:
        the_value = int(value)
        return the_value
    except (ValueError, Exception):
        failure(f'The {_label}"{value}" is not a valid integer!!')


def extract_section(config, img, extract_filename: str, left: int = 0, top: int = 0):
    # region to extract (e.g. top-left corner at (top, left) with width & height)
    width = as_int(config.counter['width'], 'counter width')
    height = as_int(config.counter['height'], 'counter height')
    # ---- clone() and crop() create the extracted image
    with img.clone() as extracted_region:
        extracted_region.crop(left, top, width=width, height=height)
        extracted_region.save(filename=extract_filename)
        # print(f'Extracted region size: {extracted_region.size}')


def process_image(config = None):
    fname = config.file['name']
    if not os.path.exists(fname):
        print(f'Cannot locate image file: {fname}')
        sys.exit(0) # Exit with status code 0 (success)
    base_dir = config.file['output']
    if not os.path.exists(base_dir):
        try:
            os.makedirs(base_dir)
        except OSError as err:
            failure(f'Unable to create "{base_dir}" - please check permissions and try again (Error: {err}).')

    prefix = config.counter["prefix"].strip('"')
    top = as_int(config.counter['top'], 'top-most y position')
    left = as_int(config.counter['left'], 'left-most x position')
    rows, cols = as_int(config.group['rows'], 'rows'), as_int(config.group['cols'], 'cols')
    gap_x = as_int(config.counter['gap_x'], 'gap_x')
    gap_col = as_int(config.counter['gap_col'], 'gap_col')
    gap_y = as_int(config.counter['gap_y'], 'gap_y')
    gap_row = as_int(config.counter['gap_col'], 'gap_row')
    height = as_int(config.counter['height'], 'height')
    width = as_int(config.counter['width'], 'width')

    _sets = config.group['sets']
    if 'x' not in _sets:
        failure('Set must contain a "NxM" setting - please check and try again.')
    _set_1, _set_2 = _sets.split('x')
    set_x, set_y = as_int(_set_1, 'first value of set'), as_int(_set_2, 'second value of set')
    # print('sets', set_x, set_y, _sets)

    the_set = 1
    with Image(filename=fname) as img:
        for x in range(0, set_x):
            for y in range(0, set_y):
                offset_y = y * (rows * (gap_y + height) + gap_row)
                offset_x = x * (cols * (gap_x + width) + gap_col)
                # print(f'Original size: {img.size}')
                for row in range(0, rows):
                    for col in range(0, cols):
                        # print(x, y, the_set, row, col)
                        ctop = top + row * (gap_x + height) + offset_y
                        cleft = left + col * (gap_x + width) + offset_x
                        _file = f'{prefix}_{the_set}_{row + 1}_{col + 1}' + '.png'
                        extract_filename = os.path.join(base_dir, _file)
                        # print(extract_filename)
                        extract_section(config, img, extract_filename, cleft, ctop)
                the_set += 1
            the_set += 1


def load_config(filename: str = 'config.ini'):

    # ---- default values in a dictionary
    default_settings = {
        'name': 'counters.png',
        'prefix': 'counter',
        'width': '100',
        'height': '100',
        'top': '0',
        'left': '0',
        'gap_x': '0',
        'gap_y': '0',
        'cols': '1',
        'rows': '1',
        'gap_col': '0',
        'gap_row': '0',
        'sets': '1x1'
    }
    config = configparser.ConfigParser(defaults=default_settings)
    config.read(filename)
    AllConfig = namedtuple('AllConfig', config.keys())
    all_items = dict(config.items())
    all_config = AllConfig(**all_items)
    # print(f"{all_config}")
    return all_config


def main():
    config = load_config('sample.ini')
    process_image(config)


if __name__ == "__main__":
    main()
