"""
Retrieve a game image from boardgamegeek.com, and display this in cards via protograf

Written by: Derek Hohls
Created on: 22 January 2025

Notes:
    * BGG() uses the `bgg-api` Python library (https://github.com/SukiCZ/boardgamegeek)
    * Inspired by https://www.myboardgamecollection.com/ (cover page)
"""
from protograf import *

Create(filename="cards_bgg_image.pdf", margin_bottom=1.75)

# ID numbers of games to retrieve
choices = [1, 2, 3, 4, 5, 6, 7, 391163, 121921]
choices = [1, 2, 3]

# BGG game data -> progress is True to check the rate of retrieval
bgames = BGG(ids=choices, progress=True, short=750)  # short: characters in DESCRIPTION_SHORT
Data(data_list=bgames.data_list)

Deck(
     cards=1,
     width=15,
     height=3,
     grid_marks=True, stroke=None)  # number of cards reset by Data()

# create image for the card
img = image(T('{{ IMAGE }}'), x=0, y=0, width=15, height=3, sliced='top')

# final layout
Card("*", img)

Save()
