# -*- coding: utf-8 -*-
"""
protograf Abstract games pieces shape definitions
"""

# lib
from importlib.resources import files

# third party

# module
from protograf.utils.messaging import feedback

NAMED_CHESS_BLACK = {
    "pawn": "cp",
    "queen": "cq",
    "king": "ck",
    "rook": "cr",
    "bishop": "cb",
    "knight": "cn",
}
NAMED_CHESS_WHITE = {
    "pawn": "cP",
    "queen": "cQ",
    "king": "cK",
    "rook": "cR",
    "bishop": "cB",
    "knight": "cN",
}
NAMED_SHOGI_BLACK = {
    "osho": "sk",
    "gyokusho": "sj",
    "hisha": "sr",
    "ryuo": "sd",
    "kakugyo": "sb",
    "ryuma": "sh",
    "ryume": "sh",
    "kinsho": "sg",
    "ginsho": "ss",
    "narigin": "sv",
    "keima": "sn",
    "narikei": "st",
    "kyosha": "sl",
    "narikyo": "sa",
    "fuhyo": "sp",
    "tokin": "sw",
}
NAMED_SHOGI_WHITE = {
    "osho": "sK",
    "gyokusho": "sJ",
    "hisha": "sR",
    "ryuo": "sD",
    "kakugyo": "sB",
    "ryuma": "sH",
    "ryume": "sH",
    "kinsho": "sG",
    "ginsho": "sS",
    "narigin": "sV",
    "keima": "sN",
    "narikei": "sT",
    "kyosha": "sL",
    "narikyo": "sA",
    "fuhyo": "sP",
    "tokin": "sW",
}


def piece_shape(key: str, game: str, name: str = "") -> object:
    """Return the shape matching a named piece."""
    from protograf.protos import image, circle

    # TODO - load ALL images from resources
    all_pieces = {
        # ---- generic
        "B": circle(fill_stroke="black"),
        "W": circle(fill="white", stroke="black"),
        # ---- checkers
        # colors contrast with black squares
        "kR": circle(fill_stroke="red"),
        "kW": circle(fill_stroke="white"),
        # ---- chess
        "cK": image(
            files("protograf").joinpath("resources/abstracts/chess/Chess_klt45.svg")
        ),
        "cQ": image(
            files("protograf").joinpath("resources/abstracts/chess/Chess_qlt45.svg")
        ),
        "cB": image(
            files("protograf").joinpath("resources/abstracts/chess/Chess_blt45.svg")
        ),
        "cN": image(
            files("protograf").joinpath("resources/abstracts/chess/Chess_nlt45.svg")
        ),
        "cR": image(
            files("protograf").joinpath("resources/abstracts/chess/Chess_rlt45.svg")
        ),
        "cP": image(
            files("protograf").joinpath("resources/abstracts/chess/Chess_plt45.svg")
        ),
        "ck": image(
            files("protograf").joinpath("resources/abstracts/chess/Chess_kdk45.svg")
        ),
        "cq": image(
            files("protograf").joinpath("resources/abstracts/chess/Chess_qdk45.svg")
        ),
        "cb": image(
            files("protograf").joinpath("resources/abstracts/chess/Chess_bdk45.svg")
        ),
        "cn": image(
            files("protograf").joinpath("resources/abstracts/chess/Chess_ndk45.svg")
        ),
        "cr": image(
            files("protograf").joinpath("resources/abstracts/chess/Chess_rdk45.svg")
        ),
        "cp": image(
            files("protograf").joinpath("resources/abstracts/chess/Chess_pdk45.svg")
        ),
        # ---- shogi
        # ---- * black/lowercase - pointing up - Lower side of board)
        "sk": image(
            files("protograf").joinpath("resources/abstracts/shogi/Shogi_osho(svg).svg")
        ),
        "sj": image(
            files("protograf").joinpath(
                "resources/abstracts/shogi/Shogi_gyokusho(svg).svg"
            )
        ),
        "sr": image(
            files("protograf").joinpath(
                "resources/abstracts/shogi/Shogi_hisha(svg).svg"
            )
        ),
        "sd": image(
            files("protograf").joinpath("resources/abstracts/shogi/Shogi_ryuo(svg).svg")
        ),
        "sb": image(
            files("protograf").joinpath(
                "resources/abstracts/shogi/Shogi_kakugyo(svg).svg"
            )
        ),
        "sh": image(
            files("protograf").joinpath(
                "resources/abstracts/shogi/Shogi_ryuma(svg).svg"
            )
        ),
        "sg": image(
            files("protograf").joinpath(
                "resources/abstracts/shogi/Shogi_kinsho(svg).svg"
            )
        ),
        "ss": image(
            files("protograf").joinpath(
                "resources/abstracts/shogi/Shogi_ginsho(svg).svg"
            )
        ),
        "sv": image(
            files("protograf").joinpath(
                "resources/abstracts/shogi/Shogi_narigin(svg).svg"
            )
        ),
        "sn": image(
            files("protograf").joinpath(
                "resources/abstracts/shogi/Shogi_keima(svg).svg"
            )
        ),
        "st": image(
            files("protograf").joinpath(
                "resources/abstracts/shogi/Shogi_narikei(svg).svg"
            )
        ),
        "sl": image(
            files("protograf").joinpath(
                "resources/abstracts/shogi/Shogi_kyosha(svg).svg"
            )
        ),
        "sa": image(
            files("protograf").joinpath(
                "resources/abstracts/shogi/Shogi_narikyo(svg).svg"
            )
        ),
        "sp": image(
            files("protograf").joinpath(
                "resources/abstracts/shogi/Shogi_fuhyo(svg).svg"
            )
        ),
        "sw": image(
            files("protograf").joinpath(
                "resources/abstracts/shogi/Shogi_tokin(svg).svg"
            )
        ),
        # ---- * white/uppercase - pointing down - Upper side of board)
        # white image is rotated by 180 degrees
        "sK": image(
            files("protograf").joinpath(
                "resources/abstracts/shogi/Shogi_osho(svg).svg"
            ),
            rotation=180,
        ),
        "sJ": image(
            files("protograf").joinpath(
                "resources/abstracts/shogi/Shogi_gyokusho(svg).svg"
            ),
            rotation=180,
        ),
        "sR": image(
            files("protograf").joinpath(
                "resources/abstracts/shogi/Shogi_hisha(svg).svg"
            ),
            rotation=180,
        ),
        "sD": image(
            files("protograf").joinpath(
                "resources/abstracts/shogi/Shogi_ryuo(svg).svg"
            ),
            rotation=180,
        ),
        "sB": image(
            files("protograf").joinpath(
                "resources/abstracts/shogi/Shogi_kakugyo(svg).svg"
            ),
            rotation=180,
        ),
        "sH": image(
            files("protograf").joinpath(
                "resources/abstracts/shogi/Shogi_ryuma(svg).svg"
            ),
            rotation=180,
        ),
        "sG": image(
            files("protograf").joinpath(
                "resources/abstracts/shogi/Shogi_kinsho(svg).svg"
            ),
            rotation=180,
        ),
        "sS": image(
            files("protograf").joinpath(
                "resources/abstracts/shogi/Shogi_ginsho(svg).svg"
            ),
            rotation=180,
        ),
        "sV": image(
            files("protograf").joinpath(
                "resources/abstracts/shogi/Shogi_narigin(svg).svg"
            ),
            rotation=180,
        ),
        "sN": image(
            files("protograf").joinpath(
                "resources/abstracts/shogi/Shogi_keima(svg).svg"
            ),
            rotation=180,
        ),
        "sT": image(
            files("protograf").joinpath(
                "resources/abstracts/shogi/Shogi_narikei(svg).svg"
            ),
            rotation=180,
        ),
        "sL": image(
            files("protograf").joinpath(
                "resources/abstracts/shogi/Shogi_kyosha(svg).svg"
            ),
            rotation=180,
        ),
        "sA": image(
            files("protograf").joinpath(
                "resources/abstracts/shogi/Shogi_narikyo(svg).svg"
            ),
            rotation=180,
        ),
        "sP": image(
            files("protograf").joinpath(
                "resources/abstracts/shogi/Shogi_fuhyo(svg).svg"
            ),
            rotation=180,
        ),
        "sW": image(
            files("protograf").joinpath(
                "resources/abstracts/shogi/Shogi_tokin(svg).svg"
            ),
            rotation=180,
        ),
        # ---- test
        "z": image(files("protograf").joinpath("resources/abstracts/test/black.png")),
        "Z": image(files("protograf").joinpath("resources/abstracts/test/white.png")),
    }
    the_shape = all_pieces.get(key, None)
    if the_shape is None:
        feedback(f"Unable to locate piece {name} ({key})", False, True)
        return None
    return the_shape
