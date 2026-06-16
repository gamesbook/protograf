# -*- coding: utf-8 -*-
"""
Example code for protograf

Written by: Derek Hohls
Created on: 16 June 2026
"""
from protograf import *

Create(
    filename="cardbox.pdf",
    paper="A5-l",
    margin=0.25,
    page_grid=1,
)

title = Common(x=1, y=18, font_size=16, align="left")

CardBox(stroke_width=3)
Text(common=title, text="CardBox: Default")
PageBreak()


CardBox(
    card_size="Mini",
    stroke_width=3,
    fold=True,
    fold_stroke_width=1,
    rounded=True,
    thumb=1.25,
)
Text(common=title, text="CardBox: Size, Folds, Rounded, Thumb")
PageBreak()


front = image(
    "images/mysterious-fantasy-forest-with-old-bridges-crop.jpg",
    height=6.35, width=4.45)
back = rectangle(
    stroke="maroon", fill="yellowgreen",
    height=6.35, width=4.45,
    hatches='d', hatches_count=50, hatches_stroke="maroon")

name = Common(text="A Game of Cards", font_size=14)
name_up = text(common=name)
name_front = text(common=name, stroke="white")
name_top = text(common=name)
name_btm = text(common=name, rotation=180)
name_lft = text(common=name, rotation=-90)
name_rgh = text(common=name, rotation=90)

CardBox(
    card_size="Mini",
    fold=True,
    rounded=True,
    thumb=1.25,

    fold_stroke="red",
    fill="wheat",
    padding_width=0.8,
    padding_height=0.8,

    flap=1,
    flap_glue=0.25,
    flap_inner=0.5,

    shapes_front=[front, name_front],
    shapes_back=back,
    shapes_top=name_top,
    shapes_bottom=name_btm,
    shapes_left=name_lft,
    shapes_right=name_rgh,
)
Text(common=title, text="CardBox: Customised with Text, Shapes and Image")

Save(
    output='png',
    dpi=300,
    directory="../docs/source/images/objects",
    names=[
        'cardbox_default',
        'cardbox_custom',
        'cardbox_shapes',
    ]
)
