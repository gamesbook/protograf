# -*- coding: utf-8 -*-
"""
protograf Abstract games pieces shape definitions
"""

# lib

# third party

# module
from protograf.utils.messaging import feedback


def piece_shape(key: str, name: str = "") -> object:
    """Return the shape matching a named piece."""
    from protograf.protos import image, circle

    all_pieces = {
        "B": circle(fill_stroke="black"),
        "W": circle(fill="white", stroke="black"),
        "z": image(
            "test.png",
        ),  # TODO - load ALL images from resources
    }
    the_shape = all_pieces.get(key, None)
    if the_shape is None:
        feedback(f"Unable to locate piece {name} ({key})", False, True)
        return None
    return the_shape
