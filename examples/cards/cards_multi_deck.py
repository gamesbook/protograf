"""
Multi-Deck example using LOTR sample data for protograf

Written by: Derek Hohls
Created on: 26 July 2025

Notes:
    * `uniques` function extract unique values from a column
    * Filters work regardless if original file contains sorted data

"""
from protograf import *

Create(filename='cards_multi_deck.pdf', margin=0.75)

lotr = [
    ['ID', 'Name', 'Age', 'Race', 'Stage'],
    [2, "Legolas", 656, "Elf", 3],
    [1, "Galadriel", 8372, "Elf", 3],
    [3, "Aragorn", 88, "Human", 2],
    [10, "Barliman", 62, "Human", 2],
    [4, "Frodo", 51, "Hobbit", 1],
    [5, "Pippin", 29, "Hobbit", 2],
    [6, "Merry", 37, "Hobbit", 2],
    [7, "Samwise", 39, "Hobbit", 1],
    [8, "Boromir", 41, "Human", 3],
    [9, "Arwen", 2778, "Elf", 2],]

Data(data_list=lotr)
races = uniques('Race')
stages = uniques('Stage')

for race in races:
    for stage in stages:
        dd = Data(
            data_list=lotr,
            filters=[('Race', race), ('Stage', stage)])
        if dd:  # NOTE: some Races do not appear in some Stages
            Deck(grid_marks=True, rounded=True)
            Card("*", circle(cx=3.2, cy=4.4, radius=2, label=T("{{ Name }}")))
            Card("*", text(x=3.2, y=5, text=T("{{ Race }}")))
            Save(filename=f'cards_{race}-{stage}.pdf')
