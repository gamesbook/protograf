# -*- coding: utf-8 -*-
"""
protograf Abstract games pieces shape definitions and/files
"""

# lib
from importlib.resources import files

# third party

# module
from protograf.utils.messaging import feedback

RESOURCES = "resources/abstracts/"
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
NAMED_GO = {
    "white": "gW",
    "black": "gB",
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
NAMED_SHOGI_INT_BLACK = {
    "osho": "ik",
    "gyokusho": "ij",
    "hisha": "ir",
    "ryuo": "id",
    "kakugyo": "ib",
    "ryuma": "ih",
    "ryume": "ih",
    "kinsho": "ig",
    "ginsho": "is",
    "narigin": "iv",
    "keima": "in",
    "narikei": "it",
    "kyosha": "il",
    "narikyo": "ia",
    "fuhyo": "ip",
    "tokin": "iw",
}
NAMED_SHOGI_INT_WHITE = {
    "osho": "iK",
    "gyokusho": "iJ",
    "hisha": "iR",
    "ryuo": "iD",
    "kakugyo": "iB",
    "ryuma": "iH",
    "ryume": "iH",
    "kinsho": "iG",
    "ginsho": "iS",
    "narigin": "iV",
    "keima": "iN",
    "narikei": "iT",
    "kyosha": "iL",
    "narikyo": "iA",
    "fuhyo": "iP",
    "tokin": "iW",
}
SHOGI_NAMES = [
    "osho",
    "gyokusho",
    "hisha",
    "ryuo",
    "kakugyo",
    "ryuma",
    "ryume",
    "kinsho",
    "ginsho",
    "narigin",
    "keima",
    "narikei",
    "kyosha",
    "narikyo",
    "fuhyo",
    "tokin",
]


def piece_shape(key: str, name: str = "", **kwargs) -> object:
    """Return the shape matching a named piece."""
    from protograf.protos import image, circle

    all_pieces = {
        # ---- generic
        "B": circle(fill_stroke="black", **kwargs),
        "W": circle(fill="white", stroke="black", **kwargs),
        # ---- checkers
        # colors contrast with black squares
        "kR": circle(fill_stroke="red", **kwargs),
        "kW": circle(fill_stroke="white", **kwargs),
        # ---- go
        "gB": image(files("protograf").joinpath(f"{RESOURCES}/go/black.png"), **kwargs),
        "gW": image(files("protograf").joinpath(f"{RESOURCES}/go/white.png"), **kwargs),
        # ---- chess
        "cK": image(
            files("protograf").joinpath(f"{RESOURCES}/chess/Chess_klt45.svg"), **kwargs
        ),
        "cQ": image(
            files("protograf").joinpath(f"{RESOURCES}/chess/Chess_qlt45.svg"), **kwargs
        ),
        "cB": image(
            files("protograf").joinpath(f"{RESOURCES}/chess/Chess_blt45.svg"), **kwargs
        ),
        "cN": image(
            files("protograf").joinpath(f"{RESOURCES}/chess/Chess_nlt45.svg"), **kwargs
        ),
        "cR": image(
            files("protograf").joinpath(f"{RESOURCES}/chess/Chess_rlt45.svg"), **kwargs
        ),
        "cP": image(
            files("protograf").joinpath(f"{RESOURCES}/chess/Chess_plt45.svg"), **kwargs
        ),
        "ck": image(
            files("protograf").joinpath(f"{RESOURCES}/chess/Chess_kdt45.svg"), **kwargs
        ),
        "cq": image(
            files("protograf").joinpath(f"{RESOURCES}/chess/Chess_qdt45.svg"), **kwargs
        ),
        "cb": image(
            files("protograf").joinpath(f"{RESOURCES}/chess/Chess_bdt45.svg"), **kwargs
        ),
        "cn": image(
            files("protograf").joinpath(f"{RESOURCES}/chess/Chess_ndt45.svg"), **kwargs
        ),
        "cr": image(
            files("protograf").joinpath(f"{RESOURCES}/chess/Chess_rdt45.svg"), **kwargs
        ),
        "cp": image(
            files("protograf").joinpath(f"{RESOURCES}/chess/Chess_pdt45.svg"), **kwargs
        ),
        # ---- shogi
        # ---- * black/lowercase - pointing up - Lower side of board)
        "sk": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi/Shogi_osho(svg).svg"),
            **kwargs,
        ),
        "sj": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi/Shogi_gyokusho(svg).svg"),
            **kwargs,
        ),
        "sr": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi/Shogi_hisha(svg).svg"),
            **kwargs,
        ),
        "sd": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi/Shogi_ryuo(svg).svg"),
            **kwargs,
        ),
        "sb": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi/Shogi_kakugyo(svg).svg"),
            **kwargs,
        ),
        "sh": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi/Shogi_ryuma(svg).svg"),
            **kwargs,
        ),
        "sg": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi/Shogi_kinsho(svg).svg"),
            **kwargs,
        ),
        "ss": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi/Shogi_ginsho(svg).svg"),
            **kwargs,
        ),
        "sv": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi/Shogi_narigin(svg).svg"),
            **kwargs,
        ),
        "sn": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi/Shogi_keima(svg).svg"),
            **kwargs,
        ),
        "st": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi/Shogi_narikei(svg).svg"),
            **kwargs,
        ),
        "sl": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi/Shogi_kyosha(svg).svg"),
            **kwargs,
        ),
        "sa": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi/Shogi_narikyo(svg).svg"),
            **kwargs,
        ),
        "sp": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi/Shogi_fuhyo(svg).svg"),
            **kwargs,
        ),
        "sw": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi/Shogi_tokin(svg).svg"),
            **kwargs,
        ),
        # ---- * white/uppercase - pointing down - Upper side of board)
        # white image is rotated by 180 degrees
        "sK": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi/Shogi_osho(svg).svg"),
            rotation=180,
            **kwargs,
        ),
        "sJ": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi/Shogi_gyokusho(svg).svg"),
            rotation=180,
            **kwargs,
        ),
        "sR": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi/Shogi_hisha(svg).svg"),
            rotation=180,
            **kwargs,
        ),
        "sD": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi/Shogi_ryuo(svg).svg"),
            rotation=180,
            **kwargs,
        ),
        "sB": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi/Shogi_kakugyo(svg).svg"),
            rotation=180,
            **kwargs,
        ),
        "sH": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi/Shogi_ryuma(svg).svg"),
            rotation=180,
            **kwargs,
        ),
        "sG": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi/Shogi_kinsho(svg).svg"),
            rotation=180,
            **kwargs,
        ),
        "sS": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi/Shogi_ginsho(svg).svg"),
            rotation=180,
            **kwargs,
        ),
        "sV": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi/Shogi_narigin(svg).svg"),
            rotation=180,
            **kwargs,
        ),
        "sN": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi/Shogi_keima(svg).svg"),
            rotation=180,
            **kwargs,
        ),
        "sT": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi/Shogi_narikei(svg).svg"),
            rotation=180,
            **kwargs,
        ),
        "sL": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi/Shogi_kyosha(svg).svg"),
            rotation=180,
            **kwargs,
        ),
        "sA": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi/Shogi_narikyo(svg).svg"),
            rotation=180,
            **kwargs,
        ),
        "sP": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi/Shogi_fuhyo(svg).svg"),
            rotation=180,
            **kwargs,
        ),
        "sW": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi/Shogi_tokin(svg).svg"),
            rotation=180,
            **kwargs,
        ),
        # ---- shogi international
        # ---- * black/lowercase - pointing up - Lower side of board)
        "ik": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi_int/0OU.svg"), **kwargs
        ),
        "ij": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi_int/0GY.svg"), **kwargs
        ),
        "ir": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi_int/0HI.svg"), **kwargs
        ),
        "id": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi_int/0RY.svg"), **kwargs
        ),
        "ib": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi_int/0KA.svg"), **kwargs
        ),
        "ih": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi_int/0RY.svg"), **kwargs
        ),
        "ig": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi_int/0KI.svg"), **kwargs
        ),
        "is": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi_int/0GI.svg"), **kwargs
        ),
        "iv": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi_int/0NG.svg"), **kwargs
        ),
        "in": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi_int/0KE.svg"), **kwargs
        ),
        "it": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi_int/0NK.svg"), **kwargs
        ),
        "il": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi_int/0KY.svg"), **kwargs
        ),
        "ia": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi_int/0NY.svg"), **kwargs
        ),
        "ip": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi_int/0FU.svg"), **kwargs
        ),
        "iw": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi_int/0TO.svg"), **kwargs
        ),
        # ---- * white/uppercase - pointing down - Upper side of board)
        "iK": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi_int/1OU.svg"),
            **kwargs,
        ),
        "iJ": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi_int/1GY.svg"),
            **kwargs,
        ),
        "iR": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi_int/1HI.svg"),
            **kwargs,
        ),
        "iD": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi_int/1RY.svg"),
            **kwargs,
        ),
        "iB": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi_int/1KA.svg"),
            **kwargs,
        ),
        "iH": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi_int/1RY.svg"),
            **kwargs,
        ),
        "iG": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi_int/1KI.svg"),
            **kwargs,
        ),
        "iS": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi_int/1GI.svg"),
            **kwargs,
        ),
        "iV": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi_int/1NG.svg"),
            **kwargs,
        ),
        "iN": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi_int/1KE.svg"),
            **kwargs,
        ),
        "iT": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi_int/1NK.svg"),
            **kwargs,
        ),
        "iL": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi_int/1KY.svg"),
            **kwargs,
        ),
        "iA": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi_int/1NY.svg"),
            **kwargs,
        ),
        "iP": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi_int/1FU.svg"),
            **kwargs,
        ),
        "iW": image(
            files("protograf").joinpath(f"{RESOURCES}/shogi_int/1TO.svg"),
            **kwargs,
        ),
        # ---- test
        "z": image(
            files("protograf").joinpath(f"{RESOURCES}/test/black.png"), **kwargs
        ),
        "Z": image(
            files("protograf").joinpath(f"{RESOURCES}/test/white.png"), **kwargs
        ),
    }
    the_shape = all_pieces.get(key, None)
    if the_shape is None:
        feedback(f"Unable to locate piece {name} ({key})", False, True)
        return None
    return the_shape
