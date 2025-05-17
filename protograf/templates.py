"""
Pre-defined templates for protograf
"""

# lib
# third party
from reportlab.lib.units import cm, inch

# project


CARDS = [
    {"poker": {"height": 8.8, "width": 6.3, "units": cm}},
    {"tarot": {"height": 13.0, "width": 7.5, "units": cm}},
]
TILES = [
    {"catan": {"height": 4.5, "width": 4.5, "units": cm}},
    {"bluemoon": {"height": 5.0, "width": 5.0, "units": cm}},
]
COUNTERS = [
    {"AH": {"height": 0.5, "width": 0.5, "units": inch}},
    {"SPI": {"height": 0.5, "width": 0.5, "units": inch}},
]
