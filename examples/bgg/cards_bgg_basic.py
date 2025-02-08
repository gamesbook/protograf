"""
Retrieve game info from boardgamegeek.com, and display this in cards via protograf

Written by: Derek Hohls
Created on: 21 May 2016

Notes:
    BGG() uses the `bgg-api` Python library (https://github.com/SukiCZ/boardgamegeek)
"""
from protograf import *

Create(filename="cards_bgg_basic.pdf", margin_bottom=1.75)

# ID numbers of games to retrieve
choice = range(1, 10)

# BGG game data -> progress is True so we can see the rate of retrieval
bgames = BGG(ids=choice, progress=True, short=610)  # short: characters in DESCRIPTION_SHORT
Data(data_list=bgames.data_list)

Deck(cards=1, grid_marks=True, stroke=None)  # number of cards reset by Data()

# format of text used
numbers = Common(font_name="Helvetica", font_size=9, stroke=black)
title = Common(font_name="Times-Roman", font_size=12, stroke=black)

# source and location of images
time_img = image('time.png', x=0.2, y=6.8, width=1.8, height=1.8)
players_img = image('players.png', x=2.2, y=6.8, width=1.8, height=1.8)
age_img = image('age.png', x=4.2, y=6.8, width=1.8, height=1.8)

# create a list of text elements for the cards
time = text(common=numbers, x=1.1, y=6.9, text=T('{{ PLAYINGTIME }}'))
players = text(common=numbers, x=3.1, y=6.9, text=T('{{ PLAYERS }}'))
minage = text(common=numbers, x=5.1, y=6.9, text=T('{{ AGE }}'))
name = text(common=title, x=3.15, y=6.4, text=T('{{ NAME[:32] }}'))
desc = text(
    font_name="Times-Roman", font_size=9, stroke="#808080",
    leading=11, x=0.075, y=6.35, width=6.125, height=4.8,
    wrap=True, align="centre", text=T('{{ DESCRIPTION_SHORT }}'))
foot = text(
    font_name="Helvetica", font_size=7, stroke=black, leading=8,
    x=0.1, y=1.67, width=6.1, height=1.6,
    wrap=True, align="centre", text=T('{{ MECHANICS }}'))

# final layout
layout = group(time, players, minage, name, desc, foot)
Card("*", layout)
Card("*", time_img, age_img, players_img)

Save()
