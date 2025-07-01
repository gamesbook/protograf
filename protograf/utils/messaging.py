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
    if warn and not globals.pargs.nowarning:
        console.print("[bold magenta]WARNING::[/bold magenta] %s" % item)
    elif not warn:
        console.print("[bold green]FEEDBACK::[/bold green] %s" % item)
    if stop:
        console.print(
            "[bold red]FEEDBACK::[/bold red] Could not continue with program.\n"
        )
        # sys.exit()
        quit()
