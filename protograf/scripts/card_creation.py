#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
protograf script: generate a basic template for a set of cards
"""

# lib
from dataclasses import dataclass
from datetime import datetime

# third party
from rich.console import Console


@dataclass
class Options:
    script: str = ""
    paper_size: str = "A4"
    units: str = "cm"
    margins: float = 0.5
    gap: float = 0
    cards: int = 9
    grid_marks: bool = True
    card_size: str = "Poker"
    excel: str = ""


paper_size = {
    "1": "A4 - portrait",
    "2": "A4 - landscape",
    "3": "Letter - portrait",
    "4": "Letter - landscape",
}
units = {
    "1": "cm",
    "2": "mm",
    "3": "in",
}
t_f = {
    "1": "True",
    "2": "False",
}
card_size = {
    "1": "Poker",
    "2": "Bridge",
    "3": "Tarot",
    "4": "Skat",
}

gs = "[bold green]"
ge = "[/bold green]"
rs = "[bold red]"
re = "[/bold red]"
ms = "[bold magenta]"
me = "[/bold magenta]"
qs = "[bold blue]"
qe = "[/bold blue]"

now = datetime.now()
dstring = f"{now:%Y%m%d%H%M%S}"
created = f"{now:%Y-%m-%d %H:%M:%S}"
created_usa = f"{now:%m-%d-%Y %H:%M:%S}"
_input = 0.0
x_size = 1

console = Console()
console.print(f"{qs}Welcome to the Card Creation assistant!{qe}\n")
console.print(f"{qs}Please provide responses to the series of prompts below.{qe}")
console.print(f"{qs}Afterwards, a script will be generated that can used as{qe}")
console.print(f"{qs}a starting point for your card prototype.{qe}\n")
console.print(f"{qs}* Pressing Enter will accept the default option or value.{qe}")
console.print(f"{qs}* Pressing ? will take you back to the previous prompt.{qe}")
# console.print(f"{qs}{qe}")

prompt = f"{gs}Enter the number of your choice:{ge} "
invalid = f"{ms}Invalid selection. Please choose a number from those shown.{me}"
invalid_number = f"{ms}The value {_input} is not a valid number. Please try again.{me}"

opts = Options()
step = 0
# ---- data gather process
while step < 9:

    if step == 0:
        name_input = console.input(
            f"\n{gs}Enter your own script name (no spaces or extension):{ge} "
        )
        if name_input:
            _name = str(name_input).strip().replace(" ", "_")
            if len(_name) > 0:
                opts.script = _name
        if not opts.script:
            opts.script = f"cards_{dstring}"
        step += 1

    elif step == 1:
        options = paper_size
        console.print(f"\n{ms}What is your paper size?{me}")
        for key, value in options.items():
            print(f"{key}. {value}")
        choice = console.input(prompt)

        if choice == "?":
            step -= 1
        else:
            if choice:
                if choice in options:
                    match options[choice]:
                        case 1:
                            opts.paper_size = "A4"
                        case 2:
                            opts.paper_size = "A4-l"
                        case 3:
                            opts.paper_size = "Letter"
                        case 4:
                            opts.paper_size = "Letter-l"
                    step += 1
                else:
                    console.print(invalid)
            else:
                step += 1

    elif step == 2:
        options = units
        console.print(f"\n{ms}What are your units?{me}")
        for key, value in options.items():
            print(f"{key}. {value}")
        choice = console.input(prompt)

        if choice == "?":
            step -= 1
        else:
            if choice:
                if choice in options:
                    opts.units = options[choice]
                    match opts.units:
                        case "cm":
                            x_size = 1
                        case "mm":
                            x_size = 10
                        case "in":
                            x_size = 0.5
                    step += 1
                else:
                    console.print(invalid)
            else:
                step += 1

    elif step == 3:
        _input = console.input(f"\n{gs}Enter the page margin ({opts.units}):{ge} ")
        if _input == "?":
            step -= 1
        else:
            if _input:
                try:
                    _val = float(_input)
                    if _val < 0:
                        console.print(invalid_number)
                    else:
                        opts.margins = _val
                        step += 1
                except:
                    console.print(invalid_number)
            else:
                if opts.units == "in":
                    opts.margins = 0.33
                if opts.units == "mm":
                    opts.margins = 10
                step += 1

    elif step == 4:
        options = card_size
        console.print(f"\n{ms}What is your card size?{me}")
        for key, value in options.items():
            print(f"{key}. {value}")
        choice = console.input(prompt)

        if choice == "?":
            step -= 1
        else:
            if choice:
                if choice in options:
                    opts.card_size = options[choice]
                    step += 1
                else:
                    console.print(invalid)
            else:
                step += 1

    elif step == 5:
        _input = console.input(
            f"\n{gs}Enter the number of {opts.card_size} cards:{ge} "
        )
        if _input == "?":
            step -= 1
        else:
            if _input:
                try:
                    _val = int(_input)
                    if _val <= 0:
                        console.print(invalid_number)
                    else:
                        opts.cards = _val
                        step += 1
                except:
                    console.print(invalid_number)
            else:
                step += 1

    elif step == 6:
        options = t_f
        _input = console.print(f"\n{ms}Do you want grid marks displayed?{me} ")
        for key, value in options.items():
            print(f"{key}. {value}")
        choice = console.input(prompt)

        if choice == "?":
            step -= 1
        else:
            if choice:
                if choice in options:
                    opts.grid_marks = True if choice == "1" else False
                    step += 1
                else:
                    console.print(invalid)
            else:
                step += 1

    elif step == 7:
        _input = console.input(
            f"\n{gs}Enter the spacing size between cards ({opts.units}):{ge} "
        )
        if _input == "?":
            step -= 1
        else:
            if _input:
                try:
                    _val = float(_input)
                    if _val < 0:
                        console.print(invalid_number)
                    else:
                        opts.gap = _val
                        step += 1
                except:
                    console.print(invalid_number)
            else:
                step += 1

    elif step == 8:
        name_input = console.input(
            f"\n{gs}Enter the name of an Excel file (if any) containing card data:{ge} "
        )
        if name_input == "?":
            step -= 1
        else:
            if name_input:
                _name = str(name_input).strip()
                if len(_name) > 0:
                    opts.excel = _name
            step += 1


# ---- data write process
# print(opts)
fname = opts.script + ".py" if ".py" not in opts.script else opts.script
cdate = created if "A4" in opts.paper_size else created_usa

with open(f"{fname}", "w") as foo:
    foo.write(f"'''\nprotograf script\nCreated on: {cdate}\n'''")
    foo.write("\nfrom protograf import *")
    foo.write(
        f'\nCreate(\n    filename="{opts.script}.pdf",'
        f'\n    paper="{opts.paper_size}",'
        f'\n    units="{opts.units}",'
        f"\n    margin={opts.margins},"
        "\n)"
    )
    if opts.excel:
        foo.write(f'\nData(filename="{opts.excel}")')
    foo.write("\nDeck(")
    foo.write(f"\n    cards={opts.cards},")
    foo.write(f'\n    card_size="{opts.card_size}",')
    if opts.grid_marks:
        gml = opts.margins / 2.0
        foo.write("\n    grid_marks=True,")
        foo.write(f"\n    grid_marks_length={gml},")
        foo.write('\n    grid_marks_stroke="black",')
        foo.write("\n    grid_marks_stroke_width=0.1,")
    if opts.gap:
        foo.write(f"\n    spacing_x={opts.gap},")
        foo.write(f"\n    spacing_y={opts.gap},")
    foo.write("\n)")
    foo.write(f'\nCard("*", circle(x={x_size}, y={x_size}, label="{{{{sequence}}}}"))')
    foo.write("\nSave()")

console.print(f'\n{qs}Your choices have been used to create "{fname}" {qe}')
