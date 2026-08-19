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
PageBreak()

name = Common(text="Norsemen: The Cards", font_size=14, stroke="white")
cbx = Common(font_size=14, stroke="white")
name_up = text(common=name)
name_front = text(common=name)
name_top = text(common=name)
name_btm = text("NtG:Bottom", common=cbx, rotation=180)
name_lft = text("NtG:Left", common=cbx, rotation=-90)
name_rgh = text("NtG:Right", common=cbx, rotation=90)
name_bck = text("NtG:Back", common=cbx)

# Photo by <a href="https://unsplash.com/@rogueli?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Rogue Li</a> on <a href="https://unsplash.com/photos/dark-stormy-clouds-over-a-calm-blue-ocean-_bO-Wa0DHaU?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
# Original is 640x426
wrapper = image(
    "images/rogue-li-unsplash.jpg",
    width=14, height=7,
    fit="width")

CardBox(
    x=0, y=0,
    thumb=1.25,
    card_size="Mini",  #44.5, 63.5
    fold=True,
    fold_stroke="yellow",
    fill="#61778F",
    padding_width=0.8,
    padding_height=0.8,
    rounded=True,
    flap=1,
    flap_glue=0.25,
    flap_inner=0.5,
    shapes_wrap=wrapper,
    shapes_front=name_front,
    shapes_back=name_bck,
    shapes_top=name_top,
    shapes_bottom=name_btm,
    shapes_left=name_lft,
    shapes_right=name_rgh,
)
Text("Photo by https://unsplash.com/@rogueli", y=13, x=0, align="left")

Save(
    output='png',
    dpi=300,
    directory="../docs/source/images/objects",
    names=[
        'cardbox_default',
        'cardbox_custom',
        'cardbox_shapes',
        'cardbox_wrap',
    ]
)
