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
from wand.drawing import Drawing
from wand.color import Color


def failure(message: str):
    """End the program with a message."""
    print(message)
    sys.exit(0)  # Exit with status code 0 (success)


def as_int(value, label: str = None) -> int:
    """Convert a value to an int

    Args:

    - value (Any): the value to be converted to a float
    - label (str): assigned as part of the error message to ID the type of value
    """
    _label = f"{label} value " if label else "value "
    if value is None:
        failure(f'The {_label}"{value}" is not a valid integer!')
    try:
        the_value = int(value)
        return the_value
    except (ValueError, Exception):
        failure(f'The {_label}"{value}" is not a valid integer!')
    return None


def draw_outline(config, filename: str, rounded: bool = True, aliased: bool = True):
    """Create larger image with rounded rectangular outline

    Args:

    - config (namedtuple): configuration settings
    - filename (str): name of the file to be created
    - rounded (bool): if True, outline is rounded
    - aliased (bool): if True, outline is antialiased
    """
    width = as_int(config.counter["width"], "counter width")
    height = as_int(config.counter["height"], "counter height")
    border = as_int(config.frame["thickness"], "frame thickness")
    # https://imagemagick.org/script/color.php#color_names
    border_color = config.frame["color"]  # 'black'
    new_width = width + border * 2
    new_height = height + border * 2

    with Image(filename=filename) as icon:
        # 1. Make white background transparent
        # icon.transparent_color('white', alpha=0.0) # Sets white to fully transparent
        # 2. Create a new blank transparent background image
        # Adjust width/height to fit. 'RGBA' ensures alpha channel.
        with Image(width=new_width, height=new_height, background=None) as background:
            background.alpha_channel = "set"  # Enable alpha channel
            # 'over' blends icon onto background, 'blend' offers more control.
            background.composite_channel(
                "default_channels", icon, "over", border, border
            )
            # 3. Draw outline
            with Drawing() as draw:
                draw.fill_color = Color("transparent")
                draw.stroke_color = Color(border_color)
                draw.stroke_width = border
                draw.stroke_antialias = aliased
                # -- corner radius (e.g., 20 pixels)
                corner_radius = 2 * border if rounded else 0
                # -- rounded rectangle
                draw.rectangle(
                    left=border / 2,
                    top=border / 2,
                    width=new_width - border,
                    height=new_height - border,
                    radius=corner_radius,
                )
                # 4 .Apply the drawing operations to the image
                draw(background)
            # 5. Save the final image
            background.save(filename=filename)


def extract_section(
    config,
    img: Image,
    extract_filename: str,
    left: int = 0,
    top: int = 0,
    outlined: bool = False,
    aliased: bool = True,
):
    """Save part of an image to a new file.

    Args:

    - config (namedtuple): configuration settings
    - img (wand.image.Image): source image
    - extract_filename (str): name of the file to be created
    - top: top-left y corner of extaction area (pixels)
    - left: top-left x corner of extaction area (pixels)
    - outlined (bool): if True, outline is drawn
    - aliased (bool): if True, outline is antialiased
    """
    # ---- region to extract : top-left corner at (top, left) with width & height
    width = as_int(config.counter["width"], "counter width")
    height = as_int(config.counter["height"], "counter height")
    # ---- clone() and crop() create the extracted image
    btm = top + height
    # print(f"size: {img.size} extract: {top=} {btm=}")
    with img.clone() as extracted_region:
        if btm <= img.size[1]:
            extracted_region.crop(left, top, width=width, height=height)
            extracted_region.save(filename=extract_filename)
            # print(f'Extracted region size: {extracted_region.size}')
            if outlined:
                draw_outline(config, extract_filename, aliased)


def process_image(config=None):
    """Process an image according to configuration settings."""
    fname = config.file["name"]
    if not os.path.exists(fname):
        failure(f"Cannot locate image file: {fname}")
    base_dir = config.file["output"]
    if not os.path.exists(base_dir):
        try:
            os.makedirs(base_dir)
        except OSError as err:
            failure(
                f'Unable to create "{base_dir}"'
                f" - please check permissions and try again (Error: {err})."
            )

    # ---- counter settings
    prefix = config.counter["prefix"].strip('"')
    top = as_int(config.counter["top"], "top-most y position")
    left = as_int(config.counter["left"], "left-most x position")
    gap_x = as_int(config.counter["gap_x"], "gap_x")
    gap_y = as_int(config.counter["gap_y"], "gap_y")
    height = as_int(config.counter["height"], "height")
    width = as_int(config.counter["width"], "width")
    # ---- group settings
    rows = as_int(config.group["rows"], "rows")
    cols = as_int(config.group["cols"], "cols")
    gap_row = as_int(config.group["gap_row"], "gap_row")
    gap_col = as_int(config.group["gap_col"], "gap_col")
    _sets = config.group["sets"]
    # ---- frame settings
    border = as_int(config.frame["thickness"], "frame thickness")
    if border % 2 != 0:
        failure(
            f"Frame thickness must be an even number e.g. 2, 4 or 6 - not {border}."
        )
    outlined = True if border else False
    alias = as_int(config.group["alias"], "alias")
    aliased = True if alias else False

    if "x" not in _sets:
        failure('Set must contain a "NxM" setting - please check and try again.')
    _set_1, _set_2 = _sets.split("x")
    set_x, set_y = as_int(_set_1, "first value of set"), as_int(
        _set_2, "second value of set"
    )
    # print('sets', set_x, set_y, _sets)

    the_set = 1
    the_top, the_left = top, left
    with Image(filename=fname) as img:
        for y in range(0, set_y):
            top = the_top + y * rows * height + y * (rows - 1) * gap_y + y * gap_row
            for x in range(0, set_x):
                left = left + x * cols * width + x * (cols - 1) * gap_x + x * gap_col
                for row in range(0, rows):
                    for col in range(0, cols):
                        # print(x, y, the_set, row, col)
                        ctop = top + row * (gap_x + height)
                        cleft = left + col * (gap_x + width)
                        _file = f"{prefix}_{the_set}_{row + 1}_{col + 1}" + ".png"
                        extract_filename = os.path.join(base_dir, _file)
                        extract_section(
                            config,
                            img,
                            extract_filename,
                            cleft,
                            ctop,
                            outlined,
                            aliased,
                        )
                the_set += 1
            left = the_left


def load_config(filename: str = "config.ini"):
    """Load configuration settings from an .ini file"""
    # ---- default values in a dictionary
    default_settings = {
        "name": "counters.png",
        "prefix": "counter",
        "width": "100",
        "height": "100",
        "top": "0",
        "left": "0",
        "gap_x": "0",
        "gap_y": "0",
        "cols": "1",
        "rows": "1",
        "gap_col": "0",
        "gap_row": "0",
        "sets": "1x1",
        "thickness": "0",
        "color": "black",
        "alias": "1",
    }
    config = configparser.ConfigParser(defaults=default_settings)
    config.read(filename)
    allconfig = namedtuple("allconfig", config.keys())
    all_items = dict(config.items())
    all_config = allconfig(**all_items)
    # print(f"{all_config}")
    return all_config


def main():
    """Script Entry - primary loop."""
    config = load_config("sample.ini")
    process_image(config)


if __name__ == "__main__":
    main()
