# -*- coding: utf-8 -*-
"""
Messaging utilities for protograf
"""
# local
from protograf import globals


def feedback(item, stop=False, warn=False):
    """Placeholder for more complete feedback."""
    if warn and not globals.pargs.nowarning:
        print("WARNING:: %s" % item)
    elif not warn:
        print("FEEDBACK:: %s" % item)
    if stop:
        print("FEEDBACK:: Could not continue with program.\n")
        # sys.exit()
        quit()
