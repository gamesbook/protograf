"""
Standard playing cards script for protograf

Written by: Derek Hohls
Created on: 12 August 2024

Note:
    Characters from the ZapfDingbats font are described using their hex code; see:
    https://help.adobe.com/en_US/framemaker/2015/using/using-framemaker-2015/Appendix/frm_character_sets_cs/frm_character_sets_cs-5.htm
"""
from protograf import *

# create deck
Create(filename='cards_standard.pdf', margin=1, margin_bottom=1.9)

# generate data for cards
combos = Matrix(
    labels=['SUIT', 'VALUE'],
    data=[
        #['\u2660', '\u2663', '\u2665', '\u2666'],  # spade, club, heart, diamond
        ['\xab', '\xa8', '\xaa', ' \xa9'],  # spade, club, heart, diamond
        ['K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2', 'A'],
    ])
Data(matrix=combos, extra=2)  # will (re)set no. of cards based on length

# deck design
Deck(cards=54,
     height=8.8,
     width=6.3,
     rounding=0.5,
     grid_marks=True)

gred = '#BD0000'  # Guardsman Red

# card layout elements
value_top = Common(x=1.0, y=1.4, font_size=40)
value_black = text(common=value_top, stroke="black", text=T('{{VALUE}}'))
value_red = text(common=value_top, stroke=gred, text=T('{{VALUE}}'))

value_low = Common(x=5.85, y=7.4, font_size=40, rotation=180)
value_low_black = text(common=value_low, stroke="black", text=T('{{VALUE}}'))
value_low_red = text(common=value_low, stroke=gred, text=T('{{VALUE}}'))

marker_base = Common(x=0.9, y=2.6, font_size=42, font_name="zapfdingbats", align="centre")
marker_black = text(common=marker_base, stroke="black", text=T('{{SUIT}}'))
marker_red = text(common=marker_base, stroke=gred, text=T('{{SUIT}}'))

marker_low = Common(x=5.5, y=6.2, font_size=42, rotation=180, font_name="zapfdingbats")
marker_low_black = text(common=marker_low, stroke="black", text=T('{{SUIT}}'))
marker_low_red = text(common=marker_low, stroke=gred, text=T('{{SUIT}}'))

# cards setup
Card("1-26", value_black, value_low_black, marker_black, marker_low_black)
Card("27-52", value_red, value_low_red, marker_red, marker_low_red)

# royalty
royals = Common(x=1.55, y=1.9, width=3.3, height=5)
# royalty - SPADES
Card( "1", image("images/king_s.png", common=royals))
Card( "2", image("images/queen_s.png", common=royals))
Card( "3", image("images/jack_s.png", common=royals))
# royalty - CLUBS
Card("14", image("images/king_c.png", common=royals))
Card("15", image("images/queen_c.png", common=royals))
Card("16", image("images/jack_c.png", common=royals))
# royalty - HEARTS
Card("27", image("images/king_h.png", common=royals))
Card("28", image("images/queen_h.png", common=royals))
Card("29", image("images/jack_h.png", common=royals))
# royalty - DIAMONDS
Card("40", image("images/king_d.png", common=royals))
Card("41", image("images/queen_d.png", common=royals))
Card("42", image("images/jack_d.png", common=royals))

# ace
Card("13",
     text(x=2.8, y=6.6, font_size=180, stroke="black", text='\xab', font_name="zapfdingbats"),
     text(x=3.05, y=5, font_size=60, stroke="white", fill="white", text='\xab', font_name="zapfdingbats"))

# jokers (2 extra cards)
jok_pic = Common(x=0.8, y=1.9, width=5, height=5)
Card("53",
     text(common=value_top, stroke="black", text='J'),
     text(common=value_low, stroke="black", text='J'),
     image("images/joker_black.png", common=jok_pic))
Card("54",
     text(common=value_top, stroke=gred, text='J'),
     text(common=value_low, stroke=gred, text='J'),
     image("images/joker_red.png", common=jok_pic))

Save()
