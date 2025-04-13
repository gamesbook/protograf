"""
Retrieve a game image from boardgamegeek.com, and display this in cards via protograf

Written by: Derek Hohls
Created on: 22 January 2025

Notes:
    * BGG() uses the `bgg-api` Python library (https://github.com/SukiCZ/boardgamegeek)
    * Inspired by https://www.myboardgamecollection.com/ (cover page)
"""
from protograf import *

Create(filename="cards_bgg_image.pdf", margin_top=2.5, margin_left=3)

# ID numbers of games to retrieve
choices = [1, 2, 3, 4, 5, 6, 7, 391163, 121921, 28143]
#choices = [1, 2, 3, 4, 5, 7, 8, 9, 10]

# BGG game data -> progress is True to check the rate of retrieval
bgames = BGG(ids=choices, progress=True, short=750)  # characters in DESCRIPTION_SHORT
Data(data_list=bgames.data_list)

Deck(
     cards=8,
     width=15,
     height=5,
     margin=1,
     stroke="white"
)

# create image and QR for the card
img = image(T('{{ IMAGE }}'), x=0., y=0., width=15, height=5, sliced='m')
qr = qrcode(
    T('bgg-{{ ID }}-qr.png'),
    text=T("https://boardgamegeek.com/boardgame/{{ ID }}"),
    x=12.5, y=2.5,
    width=2, height=2,
    fill="#FF5100",
    stroke="#3F3A60")
rct = rectangle(border=None)

# final layout
layout = group(rct, img, qr)
Card('*', layout)

Save()
