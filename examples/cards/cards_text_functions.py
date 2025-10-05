"""
Deck and Card example using list data for protograf

Written by: Derek Hohls
Created on: 5 October 2025
"""
from protograf import *

Create(filename='cards_lotr.pdf',
       paper="A6",
       margin=0.75, margin_top=1)

# deck data
lotr = [
    ['ID', 'Name', 'Age', 'Race', 'Copies'],
    [1, "gandalf grey", None, "Maia", 1],
    [2, "LEGOLAS", 656, "Elf", 1],
    [3, "gimli", 140, "Dwarf", 1],
    [4, "aragorn", 88, "Human", 1],
    [5, "frodo  ", 51, "Hobbit", 1],
    [6, "pippin", 29, "Hobbit", 1],
    [7, "merry", 37, "Hobbit", 1],
    [8, "samwise", 39, "Hobbit", 1],
    [9, "boromir", 41, "Human", 1],
]
Data(data_list=lotr)
# design deck
Deck(cards=1, height=4, width=3)

# character name
name_box = rectangle(x=0.25, y=0.25, width=2.5, height=1, rounded=0.1)
chn = Common(x=1.5, y=0.75, font_size=12)
Card("*", name_box)
Card("1", text(text=T("{{ Name.title() }}"), common=chn))
Card("2", text(text=T("{{ Name.lower() }}"), common=chn))
Card("3", text(text=T("{{ Name.upper() }}"), common=chn))
Card("4", text(text=T("{{ Name.capitalize() }}"), common=chn))
Card("5", text(text=T("{{ Name.strip() }}"), common=chn))
Card("6", text(text=T("{{ Name.replace('p', 'm') }}"), common=chn))
Card("7", text(text=T("{{ Name.zfill(7) }}"), common=chn))
Card("8", text(text=T("{{ Name.lstrip('sam') }}"), common=chn))
Card("9", text(text=T("{{ Name.rstrip('mir') }}"), common=chn))

Save(
     output='png',
     dpi=300,
     directory="../docs/source/images/decks",
     names=['cards_text_functions']
)
