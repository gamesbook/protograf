# -*- coding: utf-8 -*-
"""
Show default fonts that are built-into PyMuPDF

Written by: Derek Hohls
Created on: 24 April 2025

Notes:
    * CJK fonts are NOT automatically built-in to some operating systems.
    * For Ubuntu/Debian alternatives, see:
        https://help.accusoft.com/PrizmDoc/v12.2/HTML/Installing_Asian_Fonts_on_Ubuntu_and_Debian.html
    * For Windows, see:
        https://helpx.adobe.com/acrobat/kb/font-pack-spelling-dictionary-64-bit-windows.html
"""

from protograf import *

Create(filename="default_fonts.pdf",
       paper="A7",
       margin=0.75,
       margin_right=0.2,
       margin_top=0.5,
       margin_bottom=0.2,
       font_size=8,
       stroke_width=0.5)

header = Common(x=0, y=0, font_size=8, align="left")
sample = Common(x=0, font_size=7.5, align="left")
fox = 'A quick brown fox jumps over the lazy dog'
abc = "A  B  C  D  E  F  G  H  I  J  K  L  M  N  O  P"
blue_width = 0.33

Blueprint(stroke_width=blue_width)
Text(common=header, text="Built-in Fonts: Western")

Text(common=sample, y=0.5, text="Helvetica (helv)", font_name="Helvetica")
Text(common=sample, y=1.0, text=fox, font_name="Helvetica")
Text(common=sample, y=1.5, text="Times-Roman (tiro)", font_name="Times-Roman")
Text(common=sample, y=2.0, text=fox, font_name="Times-Roman")
Text(common=sample, y=2.5, text="Courier (cour)", font_name="Courier")
Text(common=sample, y=3.0, text=fox, font_name="Courier")
Text(common=sample, y=3.5, text="Symbol (symb)", font_name="Helvetica")
Text(common=sample, y=4.0, text=abc, font_name="Symbol")
Text(common=sample, y=4.5, text="ZapfDingbats (zadb)", font_name="Helvetica")
Text(common=sample, y=5.0, text=abc, font_name="ZapfDingbats")
PageBreak()


Blueprint(stroke_width=blue_width)
Text(common=header, text="Built-in Fonts: Western Stylised")

Text(common=sample, y=0.5, text="Helvetica-Bold (hebo)", font_name="Helvetica-Bold")
Text(common=sample, y=1.0, text=fox, font_name="Helvetica-Bold")
Text(common=sample, y=1.5, text="Helvetica-Oblique (heit)", font_name="Helvetica-Oblique")
Text(common=sample, y=2.0, text=fox, font_name="Helvetica-Oblique")
Text(common=sample, y=2.5, text="Helvetica-BoldOblique (hebi)", font_name="Helvetica-BoldOblique")
Text(common=sample, y=3.0, text=fox, font_name="Helvetica-BoldOblique")
Text(common=sample, y=3.5, text="Times-Bold (tibo)", font_name="Times-Bold")
Text(common=sample, y=4.0, text=fox, font_name="Times-Bold")
Text(common=sample, y=4.5, text="Times-Italic (tiit)", font_name="Times-Italic")
Text(common=sample, y=5.0, text=fox, font_name="Times-Italic")
Text(common=sample, y=5.5, text="Times-BoldItalic (tibi)", font_name="Times-BoldItalic")
Text(common=sample, y=6.0, text=fox, font_name="Times-BoldItalic")
Text(common=sample, y=6.5, text="Courier-Bold (cobo)", font_name="Courier-Bold")
Text(common=sample, y=7.0, text=fox, font_name="Courier-Bold")
Text(common=sample, y=7.5, text="Courier-Oblique (coit)", font_name="Courier-Oblique")
Text(common=sample, y=8.0, text=fox, font_name="Courier-Oblique")
Text(common=sample, y=8.5, text="Courier-BoldOblique (cobi)", font_name="Courier-BoldOblique")
Text(common=sample, y=9.0, text=fox, font_name="Courier-BoldOblique")

PageBreak()


Blueprint(stroke_width=blue_width)
Text(common=header, text="Fonts: CJK (if installed)")

Text(common=sample, y=0.5, text="Heiti (china-s)", font_name="Helvetica")
Text(common=sample, y=1.0, text=fox, font_name="china-s")
Text(common=sample, y=1.5, text="Song (china-ss)", font_name="Helvetica")
Text(common=sample, y=2.0, text=fox, font_name="china-ss")
Text(common=sample, y=2.5, text="Fangti (china-t)", font_name="Helvetica")
Text(common=sample, y=3.0, text=fox, font_name="china-t")
Text(common=sample, y=3.5, text="Ming (china-ts)", font_name="Helvetica")
Text(common=sample, y=4.0, text=fox, font_name="china-ts")
Text(common=sample, y=4.5, text="Gothic (japan)", font_name="Helvetica")
Text(common=sample, y=5.0, text=fox, font_name="japan")
Text(common=sample, y=5.5, text="Mincho (japan-s)", font_name="Helvetica")
Text(common=sample, y=6.0, text=fox, font_name="japan-s")
Text(common=sample, y=6.5, text="Dotum (korea)", font_name="Helvetica")
Text(common=sample, y=7.0, text=fox, font_name="korea")
Text(common=sample, y=7.5, text="Batang (korea-s)", font_name="Helvetica")
Text(common=sample, y=8.0, text=fox, font_name="korea-s")

Save(output='png',
     dpi=300,
     directory="../docs/source/images/defaults",
     names=[
        'default_fonts_western',
        'default_fonts_western_stylised',
        'default_fonts_cjk'
     ])
