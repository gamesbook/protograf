"""
Deck and circular Card example using list data for protograf

Written by: Derek Hohls
Created on: 22 December 2024
"""
from protograf import *

Create(filename='cards_circular.pdf', paper="A4-l")

# deck data
Data(filename="lotr.csv")

# design deck
Deck(
     cards=1,
     frame='circle',
     stroke="darkgray",
     radius=3.15,
     copy='Copies',
     grid_marks=True)

# background color per Race
race = Common(x=0.35, y=0.35,radius=2.8)
Card("all", S("{{ Race == 'Human' }}", circle(common=race, fill_stroke="tomato")))
Card("all", S("{{ Race == 'Elf' }}", circle(common=race, fill_stroke="gold")))
Card("all", S("{{ Race == 'Dwarf' }}", circle(common=race, fill_stroke="turquoise")))
Card("all", S("{{ Race == 'Hobbit' }}", circle(common=race, fill_stroke="chartreuse")))
Card("all", S("{{ Race == 'Nazgul' }}", circle(common=race, fill_stroke="gray")))

# # character Name
Card("*", rectangle(x=1.5, y=4.2, width=3.4, height=1, rounding=0.4))
Card("all", text(text=T("{{ Name }}"), x=3.2, y=4.9, font_size=18))

# # character Age
power = text(
    text=T("""
       <p style="text-align:center; font-family:Helvetica; color:red; font-size:30px">
       <i>Long-lived</i> <b>({{ Age or '\u221E' }})</b>
       </p>"""),
    x=1.4, y=0.7, width=3.5, font_size=12,
    html=True, fill=None)
Card("all", S("{{ Race == 'Dwarf' }}", power))
Card("all", S("{{ Race == 'Elf' }}", power))
Card("all", S("{{ Race == 'Maia' }}", power))
Card("all", S("{{ Race == 'Nazgul' }}", power))

# no effect!
Card("all", S("{{ foo == 'Orc' }}", power))

Save()
