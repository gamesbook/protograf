# -*- coding: utf-8 -*-
"""
A process flow diagram using protograf

Written by: Derek Hohls
Created on: 23 January 2026
"""
from protograf import *


def draw_box(x, y, title, detail):
    box = Rectangle(x=x, y=y, height=4, width=5, stroke_width=1, rounded=True)
    Text(title, x=x + 2.5, y=y + 0.75, font_size=16)
    Text(
        "<ul>" + detail + "</ul>",
        html=True, align="left",
        x=x, y=y + 1,
        width=5,
        height=3,
    )
    Line(x=x, y=y + 1, length=5, stroke_width=1)
    return box


Create(filename="process_flow.pdf", margin=1, page_grid=2)

b1 = draw_box(
    x=1, y=5,
    title="User Details",
    detail="<li>Fill out form</li><li>Submit form</li>")
b2 = draw_box(
    x=7, y=5,
    title="User Validation",
    detail="<li>Check required fields</li><li>Clean & format data</li>")
b3 = draw_box(
    x=13, y=5,
    title="Data Storage",
    detail="<li>Save form data to database table</li>")
b4 = draw_box(
    x=7, y=11,
    title="Trigger Workflow",
    detail="<li>Send an email</li><li>Message sysadmin</li><li>Notify external API</li>")

Line(connections=[(b1, "p", "e"), (b2, "p", "w")],
     stroke_width=1, arrow=True)
Line(connections=[(b2, "p", "e"), (b3, "p", "w")],
     stroke_width=1, arrow=True)
# TODO - use polyline + snail!
Line(connections=[(b3, "p", "s"), (b4, "p", "n")],
     stroke_width=1, arrow=True)

Save()
