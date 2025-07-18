"""
Show customised texts - and useful overides - for protograf

Written by: Derek Hohls
Created on: 19 July 2025

Font sources:
    *
"""

from protograf import *

Create(filename="customised_text.pdf",
       paper="A8",
       margin_left=0.5,
       margin_right=0.3,
       margin_bottom=0.2,
       margin_top=0.5,
       font_size=8,
       stroke_width=0.5,
       )

Footer(draw=False)

txt = Common(x=0, y=0, font_size=8, align="left")

Text(common=txt, text="Text START...")
Text(x=0, y=6, font_size=8, align="left", text=Today())
PageBreak()

# ---- text styling
Blueprint()
Text(common=txt, text="Text - styling")

Font("Times-Roman", size=11, stroke="tomato")
Text(x=0, y=0.5, align="left", text="Times-Roman 12pt red")

Text(html=True,
     x=0, y=1, width=4, height=2,
     text='<div style="font-family: Helvetica; font-size: 10pt; color: black">'
          'HTML Helvetica 10pt<br/>'
          '<b>bold</b> <i>ital</i> <b><i>bold ital</i></b></div>'
)
Text(html=True,
     x=0, y=2, width=4, height=2,
     text='<div style="font-family: Times-Roman; font-size: 9pt; color: blue">'
          'HTML Times-Roman 9pt<br/>'
          '<b>bold</b> <i>ital</i> <b><i>bold ital</i></b></div>'
)
Text(x=0, y=3, width=4, height=2,
     style="font-family: Courier; font-size: 8pt; color: blue;",
     text='HTML/CSS Courier 8pt<br/>'
          '<b>bold</b> <i>ital</i> <b><i>bold ital</i></b>'
)
Text(x=0, y=4, width=4, height=1,
     block_stroke="red", block_fill="yellow",
     block_dotted=True, block_transparency=50,
     style="font-family: Courier; font-size: 8pt; color: blue;",
     text='HTML/CSS Courier 8pt<br/>'
)
PageBreak()

# ---- text custom
Blueprint()
Text(common=txt, text="Text - font, case & align")
Text(wrap=True,
     x=0, y=1, width=4, height=1,
     font_size=7,  fill="black", stroke="black",
     font_name="Courier", align="right",
     transform='t',
     text="I am Courier in title case to the right")
Text(wrap=True,
     x=0, y=2.5, width=4, height=1,
     font_size=8,  fill="black", stroke="black",
     font_name="Helvetica", align="left",
     transform='upper',
     text="I am Helvetica in upper case to the left")
Text(wrap=True,
     x=0, y=4, width=4, height=1,
     font_size=9,  fill="black", stroke="black",
     font_name="Times-Roman", align="centre",
     transform='lowercase',
     text="I'm lower case Times-Roman in the centre")
PageBreak()

# ---- text outlined
Blueprint()
Text(common=txt, text="Text - font outlined")
basic = Common(
    wrap=True,
    width=5, height=1.5,
    font_size=10,
    stroke="black",
    font_name="Helvetica",
    align="left")
Text(common=basic,
     x=0, y=0.5,
     fill="white",
     text="Default; no outline")
Text(common=basic,
     x=0, y=1.5,
     fill="white",
     outlined=True,
     text="Outlined; white fill")
Text(common=basic,
     x=0, y=2.5,
     fill="red",
     outlined=True,
     text="Outlined; red fill")
Text(common=basic,
     x=0, y=3.5,
     fill=None,
     outlined=True,
     text_stroke_width=0.1,
     text="Outlined; no fill; text_stroke_width=0.1")
Text(common=basic,
     x=0, y=5,
     fill="yellow",
     outlined=True,
     text_stroke_width=0.07,
     text="Outlined; yellow fill; text_stroke_width=0.07")
PageBreak()

# ---- text rotate
Blueprint()
Text(common=txt, text="Text - rotate")
props = Common(font_size=7,  fill="black", stroke="black", font_name="Helvetica")
# line
Text(common=props, x=1, y=1, text="Line text 1,1 - rotate 30", rotation=30)
Text(common=props, x=3, y=1, text="Line text 3,1 - rotate 30\nline break", rotation=30)

Text(common=props, x=0, y=3, width=1, height=3, wrap=True,
     text="Wrap text - 1-by-3 - rotate 90", rotation=90)
Text(common=props, x=1, y=3, width=3, height=1, wrap=True,
     text="Wrap text - 3-by-1 - rotate 90", rotation=90)

Text(common=props, x=3, y=3, width=1, height=3, html=True,
     style="""
         font-family: Helvetica;
         font-size: 7pt;
         color: black;""",
     text="<i>HTML text</i> - 1-by-3 - rotate 90", rotation=90)
PageBreak()


# ---- text fonts
Blueprint(stroke_width=0.5, edges="w")
Text(common=txt, text="Text - fonts")

Font("Eurostar")  #
Font("FreeMono")  #
Font("Quintessential")  #
Font("Eagle Lake")  #

Text(x=0, y=0.5, width=4, height=1.5,
     align="left", font_name="Eurostar",
     text="AbcEJZ?0&")

Text(x=0, y=1, width=4, height=1.25, wrap=True,
     align="right", stroke="green", font_size=14,
     font_name="Eagle Lake", block_fill="lightcyan",
     text="AbcEJZ?0&")

Text(x=0, y=2.5, width=4, height=1.25, html=True,
     align="left", stroke="red", font_size=14,
     font_name="Quintessential", block_fill="pink",
     text="AbcEJZ?0&")

Text(x=0, y=4, width=4, height=1.25,
     block_fill="greenyellow",  # NO html!
     style="""
         font-family: FreeMono;
         font-size: 15.0px;
         color:gray;
         font-weight: bold;""",
     text="AbcEJZ?0&")

Text(x=0, y=5.5, width=4, height=2.5,
     html=True, block_fill="silver",
     text="""
     <div style="
         font-family: Eagle Lake;
         font-size:12.0px;
         color:blue;
         text-align:center;">
     AbcEJZ?0&
     </div>
     <div style="
         font-family: FreeMono;
         font-size:14.0px;
         color:purple;
         text-align:center;">
     AbcEJZ?0&
     </div>"""
     )

PageBreak()

# ---- END
Text(common=txt, text="Text END...")

Save(
     output='png',
     dpi=300,
     directory="../docs/source/images/customised",
     names=[
        None,
        "text_style", "text_custom",
        "text_outlined", "text_rotate",
        "text_fonts",
        None])
