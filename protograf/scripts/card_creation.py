#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
protograf script: generate a basic template for a set of cards
"""
# lib
from datetime import datetime
from rich.console import Console

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
created = f"{now:%Y-%m-%d %H:%M:%S}"
created_usa = f"{now:%m-%d-%Y %H:%M:%S}"
_input = 0.0

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


step = 0
params = {}
params["script"] = "cards_" + f"{now:%Y%m%d%H%M%S}"
params["paper_size"] = "A4"
params["units"] = "cm"
params["margins"] = 0.5
params["gap"] = 0
params["cards"] = 9
params["grid_marks"] = True
params["card_size"] = "Poker"
uunits = params["units"]

# ---- data gather process
while step < 8:

    if step == 0:
        name_input = console.input(
            f"\n{ms}Enter your own script name (no spaces):{me} "
        )
        if name_input:
            _name = str(name_input).replace(" ", "_")
            if len(_name) > 0:
                params["script"] = _name
        step += 1

    elif step == 1:
        options = paper_size
        console.print(f"\n{ms}Select your paper size:{me}")
        for key, value in options.items():
            print(f"{key}. {value}")
        choice = console.input(prompt)

        if choice == "?":
            step -= 1
        else:
            if choice:
                if choice in options:
                    params["paper_size"] = options[choice]
                    step += 1
                else:
                    console.print(invalid)
            else:
                step += 1

    elif step == 2:
        options = units
        console.print(f"\n{ms}Select your units:{me}")
        for key, value in options.items():
            print(f"{key}. {value}")
        choice = console.input(prompt)

        if choice == "?":
            step -= 1
        else:
            if choice:
                if choice in options:
                    params["units"] = options[choice]
                    step += 1
                else:
                    console.print(invalid)
            else:
                step += 1
            uunits = params["units"]

    elif step == 3:
        _input = console.input(f"\n{gs}Enter the page margin [{uunits}]:{ge} ")
        if _input == "?":
            step -= 1
        else:
            if _input:
                try:
                    _val = float(_input)
                    if _val < 0:
                        console.print(invalid_number)
                    else:
                        params["margins"] = _val
                        step += 1
                except:
                    console.print(invalid_number)
            else:
                step += 1

    elif step == 4:
        options = card_size
        console.print(f"\n{ms}Select your card size:{me}")
        for key, value in options.items():
            print(f"{key}. {value}")
        choice = console.input(prompt)

        if choice == "?":
            step -= 1
        else:
            if choice:
                if choice in options:
                    params["card_size"] = options[choice]
                    step += 1
                else:
                    console.print(invalid)
            else:
                step += 1

    elif step == 5:
        _input = console.input(
            f'\n{gs}Enter the number of {params["card_size"]} cards:{ge} '
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
                        params["cards"] = _val
                        step += 1
                except:
                    console.print(invalid_number)
            else:
                step += 1

    elif step == 6:
        options = t_f
        _input = console.print(f"\n{gs}Do you want grid marks displayed?{ge} ")
        for key, value in options.items():
            print(f"{key}. {value}")
        choice = console.input(prompt)

        if choice == "?":
            step -= 1
        else:
            if choice:
                if choice in options:
                    params["grid_marks"] = True if choice == "1" else False
                    step += 1
                else:
                    console.print(invalid)
            else:
                step += 1

    elif step == 7:
        _input = console.input(
            f"\n{gs}Enter the spacing size between cards [{uunits}]:{ge} "
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
                        params["gap"] = _val
                        step += 1
                except:
                    console.print(invalid_number)
            else:
                step += 1

# ---- data write process
# print(params)
fname = params["script"] + ".py" if ".py" not in params["script"] else params["script"]
cdate = created if "A4" in params["paper_size"] else created_usa
with open(f"{fname}", "w") as foo:
    foo.write(f"'''\nprotograf script\nCreated on: {cdate}\n'''\n")
    foo.write("from protograf import *\n")
    foo.write(
        f"Create(\n    filename=\"{params['script']}.pdf\","
        f"\n    margin={params['margins']},"
        f"\n    paper=\"{params['paper_size']}\""
        ")"
    )
    foo.write("\nDeck(")
    foo.write(f"\n    cards={params['cards']},")
    foo.write(f"\n    card_size=\"{params['card_size']}\",")
    if params["grid_marks"]:
        gml = params["margins"] / 2.0
        foo.write("\n    grid_marks=True,")
        foo.write(f"\n    grid_marks_length={gml},")
        foo.write('\n    grid_marks_stroke="black",')
        foo.write("\n    grid_marks_stroke_width=0.1,")
    if params["gap"]:
        foo.write(f"\n    spacing_x={params['gap']},")
        foo.write(f"\n    spacing_y={params['gap']},")
    foo.write("\n)")
    foo.write("\nCard('*', circle(label=\"{{sequence}}\"))")
    foo.write("\nSave()")

console.print(f'\n{qs}Your choices have been used to create "{fname}" {qe}')
