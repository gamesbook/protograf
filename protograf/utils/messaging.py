# -*- coding: utf-8 -*-
"""
Messaging utilities for protograf
"""
# lib
import sys
import traceback

# third party
from rich.console import Console

# local
from protograf import globals


def feedback(item, stop=False, warn=False, alert=False):
    """Placeholder for more complete feedback."""
    console = Console()
    if hasattr(globals, "pargs"):
        no_warning = globals.pargs.nowarning
    else:
        no_warning = False
    if warn and not no_warning:
        console.print(f"[bold magenta]WARNING::[/bold magenta] {item}")
    elif alert:
        console.print(f"[bold yellow]FEEDBACK::[/bold yellow] {item}")
    elif not warn:
        console.print(f"[bold green]FEEDBACK::[/bold green] {item}")
    if stop:
        console.print(
            "[bold red]FEEDBACK::[/bold red] Could not continue with script.\n"
        )
        if globals.pargs.trace:
            traceback.print_stack()
        sys.exit()
