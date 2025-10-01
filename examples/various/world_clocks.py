# -*- coding: utf-8 -*-
"""
Example code showing use of functions to create customised shapes for protograf

Written by: Derek Hohls
Created on: 20 August 2024
Updated on: 22 September 2025

Notes:

*  Additional, standard Python libraries for date & time are required
*  GMT Time :
        gmtime() =>
        time.struct_time(
            tm_year=2024, tm_mon=8, tm_mday=31, tm_hour=10, tm_min=52, tm_sec=46,
            tm_wday=5, tm_yday=244, tm_isdst=0)

TODO:

* replace fixed header with random quote from https://api.quotable.io/quotes/random
"""
from protograf import Create, Circle, Text, Save, steps
from datetime import datetime, timedelta
from time import gmtime, mktime


Create(
    filename="world_clocks.pdf",
    paper="A5-l",
    margin_top=0.5,
    margin_left=1,
    margin_bottom=1,
    margin_right=0.5,
)


def clock_angles(hours: int, minutes: int) -> tuple:
    """Convert analogue clock time to angles measured counterclockwise

    Args:
        hours (int):
            Hour value (0–23)
        minutes (int):
            Minute value (0–59)

    Returns:
        tuple: (hour_angle, minute_angle) in degrees from "east"

    Example usage:

        ```
        times = [
            (10, 00), (10, 15), (10, 30), (10, 45),
            (9, 00), (9, 15), (9, 30), (9, 45),
            (1, 30), (3, 00), (12, 00), (2, 15), (6, 30)]
        for item in times:
            h, m = item[0], item[1]
            hour_angle, minute_angle = clock_angles(h, m)
            print(f"At {h}:{m:02d}, hour hand angle: {hour_angle:.2f}°, "
                  f"minute hand angle: {minute_angle:.2f}°")
    ```
    """

    def counter(angle):
        return (450 - angle) % 360

    try:
        int(hours)
        int(minutes)
    except Exception:
        raise ValueError("Invalid hours or minutes!")
    if hours < 0 or hours > 23:
        raise ValueError(f"Invalid hours - {hours}!")
    if minutes < 0 or minutes > 59:
        raise ValueError(f"Invalid minutes- {minutes}!")

    hours = hours % 12  # 12-hour format
    # minute hand: 360° in 60 minutes → 6° per minute
    minute_angle = (minutes * 6) % 360
    # hour hand: 360° in 12 hours → 30° per hour + 0.5° per minute
    hour_angle = (hours * 30 + minutes * 0.5) % 360
    # convert to counterclockwise from horizontal (3 o'clock)
    # 3 o'clock is 0°, 12 o'clock is 90°, 9 o'clock is 180°, 6 o'clock is 270°
    return (counter(hour_angle), counter(minute_angle))


def the_clock(
    x: float = 3,
    y: float = 3.5,
    hours: int = 12,
    minutes: int = 0,
    gmt: int = 0,
    label: str = "PROTO",
    numbers: bool = True,
):
    """Draw and label a clock shape for a specific time and time zone (GMT offset)"""
    # ---- get face and hand color (if "daytime")
    detail = is_day(gmt)
    if detail[0]:
        face = "white"
    else:
        face = "darkgray"
    hand = "red" if detail[1] == "AM" else "black"
    # ---- adjust hours for GMT
    hours = hours + gmt
    if hours < 0:
        hours = 24 - hours
    hours = hours if hours <= 12 else hours - 12
    # ---- draw basic clock frame
    Circle(
        cx=x,
        cy=y,
        radius=2.5,
        fill=face,
        stroke_width=6,
        label_size=7,
        label_my=1,
        label=label.upper(),
    )
    # ---- draw minutes labels
    Circle(
        cx=x,
        cy=y,
        radius=2.3,
        stroke=face,
        fill=None,
        radii=steps(0, 360, 6),
        radii_length=0.15,
        radii_offset=2.2,
        radii_stroke_width=0.5,
        radii_stroke="black",
    )
    # ---- draw hours labels
    Circle(
        cx=x,
        cy=y,
        radius=2.3,
        stroke=face,
        fill=None,
        radii=steps(0, 360, 30),
        radii_length=0.3,
        radii_offset=2.2,
        radii_stroke_width=1.5,
        radii_stroke="black",
    )
    # ---- draw centre
    Circle(cx=x, cy=y, radius=0.13, stroke=hand, fill=hand)
    # ---- angles for hands
    hr_angle, min_angle = clock_angles(hours, minutes)
    # ---- draw hour hand
    Circle(
        cx=x,
        cy=y,
        radius=1.8,
        stroke=face,
        fill=None,
        radii=[hr_angle],
        radii_length=2,
        radii_offset=-0.5,
        radii_stroke=hand,
        radii_stroke_width=4,
    )
    # ---- draw minute hand
    Circle(
        cx=x,
        cy=y,
        radius=1.8,
        stroke=face,
        fill=None,
        radii=[min_angle],
        radii_length=2.3,
        radii_offset=-0.5,
        radii_stroke=hand,
        radii_stroke_width=3,
    )


def is_day(offset: int = 0):
    """Define "daytime" according to AM/PM and actual hour."""
    gmt_now = datetime.fromtimestamp(mktime(gmtime()))
    current = gmt_now + timedelta(hours=offset)
    if current.strftime("%p") == "AM":
        day = True if current.hour > 6 else False
        period = "AM"
    else:
        day = True if current.hour < 18 else False
        period = "PM"
    return day, period


def main(
    offset: int = 2,
    quote: str = "...everybody talk about pop music!",
    label: str = "Home",
    hours: int = None,
    minutes: int = None,
):
    """Main entry into script.

    Args:
        offset (int):
            hours relative (+/-) to GMT used for the 'Home' city
        quote (str):
            text at the top of the page
        label (str):
            label for Home clock in the centre
        hours (int):
            absolute value for hours (1 to 24)
        minutes (int):
            absolute value for minutes (0 to 60)

    """
    now = gmtime()
    # ----  Set time if not provided
    _hours = hours or now.tm_hour
    _minutes = minutes or now.tm_min
    # ---- Set page header
    Text(
        x=14,
        y=0.5,
        font_size=24,
        align="centre",
        text=f"{quote} \n                (GMT {_hours}:{_minutes:>02})",
    )
    # ---- Create a clock for each city
    the_clock(x=4, y=11, hours=_hours, minutes=_minutes, gmt=1, label="London")
    the_clock(x=14, y=11, hours=_hours, minutes=_minutes, gmt=2, label="Munich")
    the_clock(x=9, y=7.5, hours=_hours, minutes=_minutes, gmt=offset, label=label)
    the_clock(x=4, y=4, hours=_hours, minutes=_minutes, gmt=-4, label="New York")
    the_clock(x=14, y=4, hours=_hours, minutes=_minutes, gmt=8, label="Hong Kong")
    # ---- create PDF and png
    Save(output="png", dpi=300)

    # code below displays examples of times across all hours
    """
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
    """


if __name__ == "__main__":
    main(offset=-8, label="San Francisco")
