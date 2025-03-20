"""
Retrieve game info from boardgamegeek.com, and display this in cards via protograf

Written by: Derek Hohls
Created on: 20 January 2025

Notes:
    * BGG() uses the `bgg-api` Python library (https://github.com/SukiCZ/boardgamegeek)
    * Inspired by https://www.myboardgamecollection.com/
"""
from protograf import *

Create(filename="cards_bgg_thumb.pdf", margin_bottom=1.75)

# ID numbers of games to retrieve
choices = [1, 2, 3, 4, 5, 6, 7, 391163, 121921]

# BGG game data -> progress is True so we can see the rate of retrieval
bgames = BGG(ids=choices, progress=True, short=750)  # short: characters in DESCRIPTION_SHORT
Data(data_list=bgames.data_list)

Deck(cards=1, grid_marks=True, stroke=None)  # number of cards reset by Data()

# format the text and numeric boxes used
numbers = Common(
    font_name="Helvetica", font_size=9, height=0.8, width=2.6, x=0.2,
    notch=0.15, notch_corners="NW SW")
title = Common(font_name="Times-Roman", font_size=12, stroke="red")

# create an image for the card
img = image(T('{{ IMAGE }}'), x=2.8, y=5.45, width=3.25, height=3.25)

# create a list of text elements for the cards
players = rectangle(
    common=numbers, y=7.9, fill_stroke="chartreuse", label_stroke="black",
    label=T('{{ PLAYERS }}'))
time = rectangle(
    common=numbers, y=6.85, fill_stroke="cyan", label_stroke="black",
    label=T('{{ PLAYINGTIME }} min'))
name = text(
    common=title, align="left", x=0.2, y=5.8, width=6, wrap=True,
    text=T('<i>{{ NAME }}</i>'))
desc = text(
    font_name="Helvetica", font_size=7, stroke=dimgray,
    leading=8, x=0.2, y=4.8, width=5.8, height=4.8,
    wrap=True, align="justify", text=T('{{ DESCRIPTION_SHORT }}'))
game_id = circle(
    cx=5.6, cy=0.3, font_size=7, radius=0.2,
    stroke=None, fill=None, label_stroke=gray, label=T('{{ ID }}'))

# create colored ratings based on score
rating_high = rectangle(
    common=numbers, y=5.8, fill_stroke="gold", label_stroke="black",
    label=T('{{ _BAYESAVERAGE|round(2) }}'))
rating_med = rectangle(
    common=numbers, y=5.8, fill_stroke="yellow", label_stroke="black",
    label=T('{{ _BAYESAVERAGE|round(2) }}'))
rating_low = rectangle(
    common=numbers, y=5.8, fill_stroke=khaki, label_stroke="black",
    label=T('{{ _BAYESAVERAGE|round(2) }}'))
Card("all", S("{{ _BAYESAVERAGE >= 7 }}", rating_high))
Card("all", S("{{ _BAYESAVERAGE >=6 and _BAYESAVERAGE < 7 }}", rating_med))
Card("all", S("{{ _BAYESAVERAGE < 6 }}", rating_low))

# final layout
layout = group(time, players, desc, game_id, img, name)
Card("*", layout)

Save()
