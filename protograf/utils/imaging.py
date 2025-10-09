# -*- coding: utf-8 -*-
"""
Image utility functions for protograf
"""
# lib
import io

# third-party
from PIL import (
    Image,
    ImageDraw,
    ImageFilter,
    ImageFont,
)  # , UnidentifiedImageError
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
            name of the image file
        rounding_radius (int):
            corner radius in pixels
    """
    _rad = tools.as_int(rounding_radius, "image operation rounding radius ", minimum=1)

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


def ellipse(the_image: str, bounds: tuple, offset_x: int = 0, offset_y: int = 0):
    """Extract image as ellipse from original.

    Args:
        the_image (str):
            name of the image file
        bounds (tuple):
            x and y in pixels
        offset_x (int):
            x-distance in pixels to shift the ellipse centre
        offset_y (int):
            y-distance in pixels to shift the ellipse centre
    """
    err = f"The (x,y) for extracting an ellipse from {the_image} is not valid"
    if not isinstance(bounds, tuple):
        feedback(err, True)
    else:
        if len(bounds) != 2:
            feedback(err, True)
        else:
            if not isinstance(bounds[0], int) or not isinstance(bounds[1], int):
                feedback(err, True)

    img = Image.open(the_image).convert("RGBA")
    offset_x = offset_x or 0
    offset_y = offset_y or 0
    background = Image.new("RGBA", img.size, (0, 0, 0, 0))

    mask = Image.new("RGBA", img.size, 0)
    draw = ImageDraw.Draw(mask)
    # create square box around (offset) centre of image
    width, height = img.size
    ell_width, ell_height = bounds[0], bounds[1]
    cx, cy = int(width / 2) + offset_x, int(height / 2) + offset_y
    x0, x1 = cx - ell_width / 2, cx + ell_width / 2
    y0, y1 = cx - ell_height / 2, cx + ell_height / 2
    # x1-x0 = y1-y0 when applying the ellipse drawing in this method:
    draw.ellipse((x0, y0, x1, y1), fill="green", outline=None)
    new_img = Image.composite(img, background, mask)
    # new_img.show()
    return in_memory(new_img)


def circle(the_image: str, radius: int, offset_x: int = 0, offset_y: int = 0):
    """Extract image as a circle from original.

    Args:
        the_image (str):
            name of the image file
        radius (int):
            circle radius in pixels
        offset_x (int):
            x-distance in pixels to shift the ellipse centre
        offset_y (int):
            y-distance in pixels to shift the ellipse centre

    """
    img = Image.open(the_image).convert("RGBA")
    offset_x = offset_x or 0
    offset_y = offset_y or 0
    background = Image.new("RGBA", img.size, (0, 0, 0, 0))
    mask = Image.new("RGBA", img.size, 0)
    draw = ImageDraw.Draw(mask)
    # create square box around (offset) centre of image
    width, height = img.size
    cx, cy = int(width / 2) + offset_x, int(height / 2) + offset_y
    x0, x1 = cx - radius, cx + radius
    y0, y1 = cy - radius, cy + radius
    # x1-x0 = y1-y0 when applying the ellipse drawing in this method:
    draw.ellipse((x0, y0, x1, y1), fill="green", outline=None)
    new_img = Image.composite(img, background, mask)
    # new_img.show()
    return in_memory(new_img)


def polygon(
    the_image: str, radius: int, sides: int = 6, offset_x: int = 0, offset_y: int = 0
):
    """Extract image as polygon from original.

    Args:
        the_image (str):
            name of the image file
        radius (int):
            polygon radius in pixels
        sides (int):
            number of sides of the polygon
        offset_x (int):
            x-distance in pixels to shift the ellipse centre
        offset_y (int):
            y-distance in pixels to shift the ellipse centre

    Notes:
        the regular_polygon method from ImageDraw module
        takes 3 key arguments; bounding_circle, n_sides, rotation
        - first is the circle that will be used to fit the polygon
          in which takes 3 parameters (x, y, radius)
        - second is number of sides
        - third is rotation in degrees

    """
    img = Image.open(the_image)
    offset_x = offset_x or 0
    offset_y = offset_y or 0
    sides = sides or 6
    background = Image.new("RGBA", img.size, (0, 0, 0, 0))
    mask = Image.new("RGBA", img.size, 0)
    draw = ImageDraw.Draw(mask)
    # create square box around (offset) centre of image
    width, height = img.size
    cx, cy = int(width / 2) + offset_x, int(height / 2) + offset_y
    draw.regular_polygon(
        (cx, cy, radius), sides, rotation=360, fill="green", outline=None
    )
    new_img = Image.composite(img, background, mask)
    width, height = img.size
    base_img = Image.new("RGBA", (width, height))
    # base_img.paste(new_img, (cx, cy), new_img)
    base_img.paste(new_img, (0, 0), new_img)
    # base_img.show()
    return in_memory(base_img)


def blur(the_image: str, radius: int = 10):
    """Blur the outline of an image.

    Args:
        the_image (str):
            name of the image file
        radius (int):
            blur radius in pixels

    """
    bradius = radius
    im = Image.open(the_image)
    # paste image on white background
    diam = 2 * bradius
    back = Image.new("RGB", (im.size[0] + diam, im.size[1] + diam), (255, 255, 255))
    back.paste(im, (bradius, bradius))
    # create paste mask
    mask = Image.new("L", back.size, 0)
    draw = ImageDraw.Draw(mask)
    x0, y0 = 0, 0
    x1, y1 = back.size
    for d in range(diam + bradius):
        x1, y1 = x1 - 1, y1 - 1
        alpha = 255 if d < bradius else int(255 * (diam + bradius - d) / diam)
        draw.rectangle([x0, y0, x1, y1], outline=alpha)
        x0, y0 = x0 + 1, y0 + 1
    # blur image and paste blurred edge according to mask
    blur = back.filter(ImageFilter.GaussianBlur(bradius / 2))
    back.paste(blur, mask=mask)
    # back.show()
    return in_memory(back)


# TODO
"""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
img = Image.open('my-image.jpg').convert("RGBA")

background = Image.new("RGBA", img.size, (0,0,0,0))
mask = Image.new("RGBA", img.size, 0)
draw = ImageDraw.Draw(mask)

font = ImageFont.truetype('Arial_Bold.ttf', 200)  # font size in pixels
draw.text((10,10), "PROTOGRAF", fill='blue', font=font)

new_img = Image.composite(img, background, mask)
new_img.show()
"""
