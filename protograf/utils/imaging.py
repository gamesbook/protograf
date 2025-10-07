# -*- coding: utf-8 -*-
"""
Image utility functions for protograf
"""
# lib
import io
# third-party
from PIL import Image, ImageDraw, ImageOps, ImageChops  # , UnidentifiedImageError
import pymupdf
# local
from protograf.utils.messaging import feedback
from protograf.utils import tools


def in_memory(the_image):
    """Return an in-memory instance of an image as a PNG."""
    membuf = io.BytesIO()
    the_image.save(membuf, format="png")
    png_data = membuf.getvalue()
    imgdoc = pymupdf.open(stream=png_data)  # in-memory image document
    return imgdoc


def rounding(the_image: str, rounding_radius):
    """Apply rounded corners to the image.

    Args:
        the_image (str):
            name of the image
        rounding (int):
            corner radius in pixels
    """
    _rad = tools.as_int(rounding_radius, 'image operation rounding radius ', mimimum=1)

    image_in = Image.open(the_image)
    mask = Image.new("L", image_in.size, 0)
    draw = ImageDraw.Draw(mask)
    # draw.ellipse((0, 0, image_in.size[0], image_in.size[1]), fill=255)
    draw.rounded_rectangle(
        ((0, 0), (image_in.size[0], image_in.size[1])),
        _rad,
        fill=255,
    )
    rounded_image = Image.composite(
        image_in, Image.new("RGBA", image_in.size, (0, 0, 0, 0)), mask
    )
    # rounded_image.show()
    return in_memory(rounded_image)


def ellipse(the_image: str, bounds: tuple):
    """Extract image as ellipse from original.

    Args:
        the_image (str):
            name of the image
        bounds (tuple):
            x and y in pixels
    """
    err = f'The (x,y) for extracting an ellipse from {the_image} is not valid'
    if not isinstance(bounds, tuple):
        feedback(err, True)
    else:
        if len(bounds) != 2:
            feedback(err, True)
        else:
            if not isinstance(bounds[0], int) or not isinstance(bounds[1], int):
                feedback(err, True)

    mask = Image.new("L", bounds, 0)  # e.g. (128, 128)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bounds, fill=255)

    image_in = Image.open(the_image)
    ell_image = ImageOps.fit(image_in, mask.size, centering=(0.5, 0.5))
    ell_image.putalpha(mask)
    # ell_image.show()
    return in_memory(ell_image)


def circle(the_image: str, radius: int):
    """Extract image as a circle from original.

    Args:
        the_image (str):
            name of the image
        radius (int):
            circle radius in pixels

    """
   # err = f'The radius for extracting a circle from {the_image} is not valid'
    _rad = tools.as_int(radius, 'Image operation circle radius', minimum=1)

    image_in = Image.open(the_image)  # .convert("RGBA")

    circle = Image.new("L", (_rad * 2, _rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, _rad * 2, _rad * 2), fill=255)
    alpha = Image.new("L", image_in.size, "white")
    w, h = image_in.size
    alpha.paste(circle.crop((0, 0, _rad, _rad)), (0, 0))
    alpha.paste(circle.crop((0, _rad, _rad, _rad * 2)), (0, h - _rad))
    alpha.paste(circle.crop((_rad, 0, _rad * 2, _rad)), (w - _rad, 0))
    alpha.paste(
        circle.crop((_rad, _rad, _rad * 2, _rad * 2)), (w - _rad, h - _rad)
    )
    alpha = ImageChops.darker(alpha, image_in.split()[-1])

    image_in.putalpha(alpha)
    # image_in.show()
    return in_memory(image_in)


def polygon(the_image: str, vertices: list):
    """Extract image as polygon from original.

    Args:
        the_image (str):
            name of the image
        vertices (list):
            list of (x, y) tuples in pixels e.g.
            [(100, 100), (1000, 100), (1000, 800), (100, 800)]
    """
    err = f'The vertices for extracting a polygon from {the_image} are not valid'
    if not isinstance(vertices, list):
        feedback(err, True)
    for item in vertices:
        if not isinstance(item, tuple):
            feedback(err, True)
        else:
            if len(item) != 2:
                feedback(err, True)
            else:
                if not isinstance(item[0], int) or not isinstance(item[1], int):
                    feedback(err, True)

    image_in = Image.open(the_image)

    mask = Image.new("L", image_in.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.polygon(vertices, fill=255, outline=None)
    black = Image.new("L", image_in.size, 0)

    poly_image = Image.composite(image_in, black, mask)
    # poly_image.show()
    return in_memory(poly_image)
