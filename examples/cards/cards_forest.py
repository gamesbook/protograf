"""
Deck and Card example using list data for protograf

Written by: Derek Hohls
Created on: 12 July 2025

Sources:
    * Images extracted from https://picjumbo.com/mysterious-fantasy-forest-with-old-bridges/
    * Quotes from "Walden or, Life in the Woods", by Henry David Thoreau
"""
from protograf import *

Create(filename='cards_forest.pdf', margin_left=0.9, margin_top=1.5)

# deck data
the_forest = [
    ['No', 'Title', 'Class', 'Value', 'Image', 'Pentomino', 'Quote', 'Copies'],
    [1, "Shadows...", "OTHER", '*', "shadows.png", "X",
     "The question is not what you look at but what you see", 2],
    [2, "Still, Pond", "BIOTA", 3, "pond.png", "P",
     "Its smooth reflecting surface was revealed", 1],
    [3, "Its Moss", "BIOTA", 2, "moss.png", "F",
     "Let us spend one day as deliberately as Nature", 2],
    [4, "Wrapped Up", "BIOTA", 2, "vines.png", "Z",
     "We can never have enough of nature", 2],
    [5, "Going Up", "MINERAL", 2, "stairs.png", "W",
     "...the pleasure of construction...", 2],
    [6, "More Trees", "BIOTA", 1, "trees.png", "Y",
     "I went to the woods because I wished to live", 3],
    [7, "Over And", "MINERAL", 3, "bridge.png", "U",
     "Meet with a success unexpected in common hours", 1],
    [8, "Solid As A", "MINERAL", 2, "rock.png", "V",
     "Things do not change; we change", 2],
    [9, "The Grey Path", "MINERAL", 1, "stone.png", "T",
    "Heaven is under our feet as well as over our heads", 3],
]
Data(data_list=the_forest)

# design the deck
Deck(
    cards=1,
    grid_marks=True,
    rounding=0.3,
    fill="black",
    stroke="gray",
    copy='Copies')

# card Frame
Card("all",
     rectangle(x=0.4, y=4.75, width=5.5, height=3.5,
               stroke="darkred", fill=None,
               stroke_width=3, rounding=0.1)
)
# card Image
Card("all",
     image(T("pictures/{{ Image }}"), x=0.2, y=0.4, width=6, height=3.8,
           rounding=10)
)
# card Value
Card("all",
     circle(x=0.4, y=0.3, radius=0.5, fill="#11341D", stroke="sienna",
            label=T("{{ Value }}"),
            label_stroke="white", label_size=18, label_face="Times-Roman")
)
# card Name
Card("all",
     text(text=T('<div style="text-align: center;">{{ Title }}</div>'),
          css="font-family:Times-Roman; color:white; font-size:14px",
          x=1.5, y=4.5, width=3.5, height=1.25, block_fill="black")
)
# card Type
Card("all",
     stadium(x=2.2, y=8, width=2, height=0.5,
             stroke="darkred", stroke_width=3, fill="black",
             label=T("{{ Class }}"), label_stroke="white", label_size=8)

)
# card Symbol
Card("all",
     pentomino(x=2.5, y=5.7, side=0.5,
               fill="darkslategrey", stroke="sienna",
               # letter=T("{{ Pentomino }}"))
               letter="F")
)
# card ID
Card("all",
     text(x=0.15, y=7.5, width=6, height=1,
          wrap=True,
          text=T('"{{ Quote }}"'),
          stroke="silver", font_size=7, font_name="Times-Roman")
)
# card ID
Card("all",
     text(x=5.7, y=8.6,
          text=T("{{ No }}"), stroke="white", font_size=6)
)

Save()
