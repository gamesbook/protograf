"""
Deck and Card example using list data for protograf

Written by: Derek Hohls
Created on: 12 July 2025

Sources:
    * Images extracted from https://picjumbo.com/mysterious-fantasy-forest-with-old-bridges/
    * Quotes from "Walden or, Life in the Woods", by Henry David Thoreau
    * Font used is https://fonts.google.com/specimen/Quintessential
"""
from protograf import *

Create(filename='cards_forest.pdf', margin_left=1, margin_top=1.5)
# deck data
the_forest = [
    ['ID', 'Title', 'Class', 'Value', 'Image', 'Pentomino', 'Invert', 'Quote', 'Copies'],
    [1, "Shadows...", "OTHER", '*', "shadows", "X", 0,
     "... not what you look at but what you see", 2],
    [2, "Still, Pond", "BIOTA", 3, "pond", "P", 0,
     "Its smooth reflecting surface was revealed", 1],
    [3, "It's Moss", "BIOTA", 2, "moss", "F", 0,
     "Spend one day as deliberately as Nature", 2],
    [4, "Wrapped Up", "BIOTA", 2, "vines", "Z", 0,
     "We can never have enough of nature", 2],
    [5, "Going Places", "MINERAL", 2, "stairs", "W", 0,
     "...the pleasure of construction...", 2],
    [6, "More Trees", "BIOTA", 1, "trees", "T", 0,
     "I went to the woods because I wished to live", 3],
    [7, "Over And", "MINERAL", 3, "bridge", "U", 1,
     "Meet with a success unexpected in common hours", 1],
    [8, "Solid As", "MINERAL", 2, "rock", "V", 0,
     "Things do not change; we change", 2],
    [9, "Greyer Path", "MINERAL", 1, "stone", "Y", 0,
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
    copy='Copies',
    card_name="Image"
)
# default Font
Font("Quintessential")
# card Frame
Card("all",
     rectangle(x=0.4, y=4.75, width=5.5, height=3.5,
               stroke="saddlebrown", fill=None,
               stroke_width=3, rounding=0.1))
# card Image
Card("all",
     image(T("pictures/{{ Image }}.png"),
           x=0.2, y=0.4, width=6, height=3.8, rounding=10))
# card Value
Card("all",
     circle(x=0.4, y=0.3, radius=0.5, fill="#11341D", stroke="sienna",
            label=T("{{ Value }}"),
            label_stroke="white", label_size=18, label_font="Quintessential"))
# card Title
Card("all",
     text(text=T('{{ Title }}'),
          #text="look",
          style='font-family:Quintessential; color:white; font-size:15px; text-align:center;',
          x=1.5, y=4.5, width=3.5, height=1.25, box_fill="black"))
# card Class
Card("all",
     stadium(x=2.2, y=8, width=2, height=0.5,
             stroke="saddlebrown", stroke_width=3, fill="black",
             label=T("{{ Class }}"),
             label_stroke="white", label_size=8, label_font="Helvetica"))
# card Symbol
pent_normal = pentomino(x=2.5, y=5.4, side=0.5,
          fill="darkslategrey", stroke="sienna", stroke_width=0.5,
          letter=T("{{ Pentomino }}"))
pent_invert = pentomino(x=2.5, y=5.4, side=0.5,
          fill="darkslategrey", stroke="sienna",
          invert="tb",
          letter=T("{{ Pentomino }}"))
Card("all", S("{{ Invert != 1 }}", pent_normal))
Card("all", S("{{ Invert == 1 }}", pent_invert))
# card Quote
Card("all",
     text(x=0.15, y=7.5, width=6, height=1,
          wrap=True,
          text=T('"{{ Quote }}"'),
          stroke="silver", font_size=7, font_name="Quintessential"))
# card ID
Card("all",
     text(x=5.7, y=8.8, font_name="Helvetica",
          text=T("{{ ID }}"), stroke="dimgray", font_size=6))
# card Attribution
Card("all",
     text(x=0.5, y=8.8, align="left", font_name="Helvetica",
          text="protograf // out of the woods", stroke="dimgray", font_size=6))
Save(cards=True)
