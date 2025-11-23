# -*- coding: utf-8 -*-
"""
Messaging utilities for protograf
"""
# third party
from rich.console import Console

# local
from protograf import globals
import traceback


def feedback(item, stop=False, warn=False, alert=False):
    """Placeholder for more complete feedback."""
    console = Console()
    if hasattr(globals, "pargs"):
        no_warning = globals.pargs.nowarning
    else:
        no_warning = False
    if warn and not no_warning:
        console.print("[bold magenta]WARNING::[/bold magenta] %s" % item)
    elif alert:
        console.print("[bold yellow]FEEDBACK::[/bold yellow] %s" % item)
    elif not warn:
        console.print("[bold green]FEEDBACK::[/bold green] %s" % item)
    if stop:
        console.print(
            "[bold red]FEEDBACK::[/bold red] Could not continue with script.\n"
        )
        if globals.pargs.trace:
            traceback.print_stack()
        quit()
