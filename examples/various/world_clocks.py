# -*- coding: utf-8 -*-
"""
Example code showing use of functions to create customised shapes for protograf

Written by: Derek Hohls
Created on: 20 August 2024

GMT Time :
    gmtime() =>
    time.struct_time(
        tm_year=2024, tm_mon=8, tm_mday=31, tm_hour=10, tm_min=52, tm_sec=46,
        tm_wday=5, tm_yday=244, tm_isdst=0)

TODO:
    * replace fixed header with random quote from https://api.quotable.io/quotes/random
"""
from protograf import *
from datetime import datetime, timedelta
from time import gmtime, mktime
import argparse

Create(filename="world_clocks.pdf",
        paper="A5-l",
        margin_top=0.5,
        margin_left=1,
        margin_bottom=1,
        margin_right=0.5)


def the_clock(
        x: float = 3,
        y: float = 3.5,
        hours: int = 12,
        minutes: int = 0,
        gmt: int = 0,
        label: str = "PROTO",
        numbers: bool = True):
    """Draw and label a clock shape for a specific time and time zone (GMT offset)
    """
    def hour_to_angle(hour: int):
        rot = (hour - 3) * 30
        if hour <= 3:
            return 270 + hour * 30
        return rot

    # get face and hand color (if "daytime")
    detail = is_day(gmt)
    if detail[0]:
        face = "white"
    else:
        face = "darkgray"
    hand = "red" if detail[1] == 'AM' else "black"
    # adjust hours for GMT
    hours = hours + gmt
    hours = hours if hours <= 12 else hours - 12
    # basic clock frame
    Circle(cx=x, cy=y, radius=2.5, fill=face, stroke_width=6,
           label_size=7, label_my=1, label=label.upper())
    # minutes
    Circle(cx=x, cy=y, radius=2.3, radii=steps(0,360,6), stroke=face, fill=None,
           radii_length=0.15, radii_offset=2.2, radii_stroke_width=0.5, radii_stroke="black")
    # hours
    Circle(cx=x, cy=y, radius=2.3, radii=steps(0,360,30), stroke=face, fill=None,
           radii_length=0.3, radii_offset=2.2, radii_stroke_width=1.5, radii_stroke="black")
    # centre
    Circle(cx=x, cy=y, radius=.13, stroke=hand, fill=hand)
    # hour hand
    hr_angle = hour_to_angle(hours) + minutes * 0.5
    Circle(cx=x, cy=y, radius=1.8, radii=[hr_angle], stroke=face, fill=None,
           radii_length=2, radii_offset=-.5, radii_stroke=hand, radii_stroke_width=4)
    # minute hand
    if minutes >= 15:
        min_angle = (minutes - 15) * 6
    else:
        min_angle = 270 + minutes * 6
    # print(f"{hours=} {minutes=} // {hr_angle=} {min_angle=}")
    Circle(cx=x, cy=y, radius=1.8, radii=[min_angle], stroke=face, fill=None,
           radii_length=2.3, radii_offset=-.5, radii_stroke=hand, radii_stroke_width=3)


def is_day(offset: int = 0):
    """Define "daytime" according to AM/PM and actual hour."""
    gmt_now = datetime.fromtimestamp(mktime(gmtime()))
    current = gmt_now + timedelta(hours=offset)
    if current.strftime('%p') == 'AM':
        day = True if current.hour > 6 else False
        period = 'AM'
    else:
        day = True if current.hour < 18 else False
        period = 'PM'
    return day, period


def main(
        offset: int = 2,
        quote: str = '...everybody talk about pop music!',
        hours: int = None,
        minutes: int = None):
    """Main entry into script.

    Args
        * offset: hours relative (+/-) to GMT used for the 'Home' city
        * quote: text at the top of the page
        * hours: absolute value for hours (1 to 12)
        * minutes: absolute value for minutes (0 to 60)

    """
    now = gmtime()
    # Set page header
    Text(x=14, y=0.5, font_size=24, align="centre",
         text=f"{quote} \n                (GMT {now.tm_hour}:{now.tm_min:>02})")
    # Set time
    _hours = hours or now.tm_hour
    _minutes = minutes or now.tm_min
    # Create a clock for each city
    the_clock(x=4, y=11, hours=_hours, minutes=_minutes, gmt=1, label="London")
    the_clock(x=14, y=11, hours=_hours, minutes=_minutes, gmt=2, label="Munich")
    the_clock(x=9, y=7.5, hours=_hours, minutes=_minutes, gmt=offset, label="Home")
    the_clock(x=4, y=4, hours=_hours, minutes=_minutes, gmt=-4, label="New York")
    the_clock(x=14, y=4, hours=_hours, minutes=_minutes, gmt=8, label="Hong Kong")
    # create PDF and png
    Save(output='png', dpi=300)

    # code below displays examples of times across all hours
    '''
    for i,hr in enumerate([5, 4, 3, 2, 1, 12]):
        y = i * 4.9 + 1.6
        the_clock(x=2, y=y, hours=hr, minutes=0, gmt=0, label=f"{hr}:00")
        the_clock(x=8, y=y, hours=hr, minutes=20, gmt=0, label=f"{hr}:20")
        the_clock(x=14, y=y, hours=hr, minutes=40, gmt=0, label=f"{hr}:40")
    PageBreak()
    for i,hr in enumerate([11, 10, 9, 8, 7, 6]):
        y = i * 4.9 + 1.6
        the_clock(x=2, y=y, hours=hr, minutes=0, gmt=0, label=f"{hr}:00")
        the_clock(x=8, y=y, hours=hr, minutes=20, gmt=0, label=f"{hr}:20")
        the_clock(x=14, y=y, hours=hr, minutes=40, gmt=0, label=f"{hr}:40")
    Save()
    '''

if __name__ == "__main__":
    #main(offset=0, hours=3, minutes=30)
    main()
