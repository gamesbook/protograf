"""
Deck and Card example using list data for protograf

Written by: Derek Hohls
Created on: 21 December 2024
"""
from protograf import *

Create(filename='cards_lotr.pdf', margin_bottom=1.9)

# deck data
lotr = [
    ['ID', 'Name', 'Age', 'Race', 'Copies'],
    [1, "Gimli", 140, "Dwarf", 1],
    [2, "Legolas", 656, "Elf", 1],
    [3, "Aragorn", 88, "Human", 1],
    [4, "Frodo", 51, "Hobbit", 1],
    [5, "Pippin", 29, "Hobbit", 1],
    [6, "Merry", 37, "Hobbit", 1],
    [7, "Samwise", 39, "Hobbit", 1],
    [8, "Boromir", 41, "Human", 1],
    [9, "Gandalf", None, "Maia", 1],
    [10, "RingWraith", 4300, "Nazgul", 9],
]
Data(data_list=lotr)
# Data(filename="lotr.csv")  # matches other examples ...

# design the deck
Deck(
    cards=1,
    grid_marks=True,
    rounding=0.3,
    fill=None,
    stroke="gray",
    mask="{{ Race == 'Hobbit' }}",
    copy='Copies')

# background color per Race
back_race = Common(x=0.5, y=0.5, width=5.3, height=7.9, rounded=0.2)
back_hum = rectangle(common=back_race, fill_stroke="tomato")
back_elf = rectangle(common=back_race, fill_stroke="gold")
back_dwa = hexagon(common=back_race, fill_stroke="turquoise")
back_hob = hexagon(common=back_race, fill_stroke="chartreuse")
back_naz = rectangle(common=back_race, fill_stroke="gray")
Card("all", S("{{ Race == 'Human' }}", back_hum))
Card("all", S("{{ Race == 'Elf' }}", back_elf))
Card("all", S("{{ Race == 'Dwarf' }}", back_dwa))
Card("all", S("{{ Race == 'Hobbit' }}", back_hob))
Card("all", S("{{ Race == 'Nazgul' }}", back_naz))

# character Name
name_box = rectangle(x=0.75, y=6.6, width=4.8, height=1.5, rounding=0.3)
Card("*", name_box)
Card("all", text(text=T("{{ Name }}"), x=3.3, y=7.3, font_size=18))

# character Age
Card("all",
     text(
         text=T("""
            <p style="text-align:center; font-family:Helvetica; color:red; font-size:30px">
              <i>Long-lived</i> <b>({{ Age or '\u221E' }})</b>
            </p>"""),
         x=0.75, y=7.1,
         height=1, width=4.8,
         html=True, fill=None))

Save()
