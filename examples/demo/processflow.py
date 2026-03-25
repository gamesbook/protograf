# -*- coding: utf-8 -*-
"""
A process flow diagram using protograf

Written by: Derek Hohls
Created on: 23 January 2026
"""
from protograf import *


def draw_step(x, y, title, detail):
    box = Rectangle(
        x=x, y=y,
        width=5, height=4,
        stroke_width=1, rounded=True)
    Text(
        title,
        x=x + 2.5, y=y + 0.75,
        font_size=16)
    Text(
        "<ul>" + detail + "</ul>",
        html=True, align="left",
        x=x, y=y + 1,
        width=5, height=3,
        font_size=12)
    Line(x=x, y=y + 1, length=5, stroke_width=1)
    return box


Create(filename="process_flow.pdf", margin=1)

Blueprint(edges="n,w")

step1 = draw_step(
    x=1, y=5,
    title="User Details",
    detail="<li>Fill out form</li><li>Submit form</li>")
step2 = draw_step(
    x=7, y=5,
    title="User Validation",
    detail="<li>Check required fields</li><li>Clean & format data</li>")
step3 = draw_step(
    x=13, y=5,
    title="Data Storage",
    detail="<li>Save form data to database table</li>")
step4 = draw_step(
    x=7, y=11,
    title="Trigger Workflow",
    detail="<li>Send out emails</li><li>Message sysadmin</li><li>Notify the API</li>")

Line(links=[
        (step1, "p", "e"),
        (step2, "p", "w")],
     stroke_width=1,
     arrow=True)
Line(links=[
        (step2, "p", "e"),
        (step3, "p", "w")],
     stroke_width=1,
     arrow=True)
Polyline(
    links=[
        (step3, "p", "s"),
        (step4, "p", "n")],
     snail="s 1 w 6",
     stroke_width=1,
     arrow=True)

Save()
