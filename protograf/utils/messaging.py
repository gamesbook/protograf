# -*- coding: utf-8 -*-
"""
Messaging utilities for protograf
"""
# third party
from rich.console import Console

# local
from protograf import globals


def feedback(item, stop=False, warn=False):
    """Placeholder for more complete feedback."""
    console = Console()
    if hasattr(globals, "pargs"):
        no_warning = globals.pargs.nowarning
    else:
        no_warning = False
    if warn and not no_warning:
        console.print("[bold magenta]WARNING::[/bold magenta] %s" % item)
    elif not warn:
        console.print("[bold green]FEEDBACK::[/bold green] %s" % item)
    if stop:
        console.print(
            "[bold red]FEEDBACK::[/bold red] Could not continue with program.\n"
        )
        quit()
