"""
Deck and hexagonal Card example using list data for protograf

Written by: Derek Hohls
Created on: 21 December 2024
"""
from protograf import *

Create(filename='cards_hexagonal.pdf', paper="A4-l")

# deck data
Data(filename="lotr.csv")

# design deck
Deck(frame='hexagon', copy='Copies', height=6, stroke="darkgray")

# background color per Race
back_race = Common(x=0.5, y=0.4, radius=3, label_size=18)
back_hum = hexagon(common=back_race, fill_stroke="tomato")
back_elf = hexagon(common=back_race, fill_stroke="gold")
back_dwa = hexagon(common=back_race, fill_stroke="turquoise")
back_hob = hexagon(common=back_race, fill_stroke="chartreuse")
back_naz = hexagon(common=back_race, fill_stroke="gray")
Card("all", S("{{ Race == 'Human' }}", back_hum))
Card("all", S("{{ Race == 'Elf' }}", back_elf))
Card("all", S("{{ Race == 'Dwarf' }}", back_dwa))
Card("all", S("{{ Race == 'Hobbit' }}", back_hob))
Card("all", S("{{ Race == 'Nazgul' }}", back_naz))

# character Name
name_box = rectangle(x=1.9, y=4.3, width=3.2, height=1,
                     notch_style='snip', notch_x=0.1, notch_y=0.2)
Card("*", name_box)
Card("all", text(text=T("{{ Name }}"), x=3.5, y=5, font_size=18))

# character Age
power = text(
    text=T("""
       <p style="text-align:center; font-family:Helvetica; color:red; font-size:30px">
         <i>Long-lived:</i> <b>{{ Age or '\u221E' }}</b>
       </p>"""),
    x=1.7, y=0.2, width=3.5, font_size=12,
    html=True, fill=None)
Card("all", S("{{ Race == 'Elf' }}", power))
Card("all", S("{{ Race == 'Maia' }}", power))
Card("all", S("{{ Race == 'Nazgul' }}", power))

# no effect!
Card("all", S("{{ foo == 'Orc' }}", power))

Save()
