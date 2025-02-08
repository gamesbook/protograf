# -*- coding: utf-8 -*-
"""
Dice functions for protograf
"""
# lib
import random

# third party
# project


class Dice:
    """Base class for a dice."""

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.rolls = []
        self.dice_count = 1
        self.roll_count = 1

    def roll(self, count=None):
        """Implement in sub-class"""
        raise NotImplementedError

    def set_rolls(self, rolls):
        """Set number of rolls to be used."""
        try:
            self.roll_count = int(rolls)
        except (ValueError, TypeError):
            self.roll_count = 1

    def set_dice(self, dice):
        """Set number of dice to be used."""
        try:
            self.dice_count = int(dice)
        except (ValueError, TypeError):
            self.dice_count = 1

    def do_roll(self, count=None, pips=6):
        """Generate a list with count values."""
        self.set_rolls(rolls=count)
        self.rolls = [random.randint(1, pips) for rll in range(0, self.roll_count)]
        return self.rolls

    def multi_roll(self, count=None, pips=6, dice=None):
        """Generate a list with count values, summed for the number of dice."""
        self.set_rolls(rolls=count)
        self.set_dice(dice=dice)
        for rll in range(0, self.roll_count):
            total = 0
            for dce in range(0, self.dice_count):
                total += random.randint(1, pips)
            self.rolls.append(total)
        return self.rolls


class DiceD4(Dice):
    """Class for a 4-sided die."""

    def roll(self, count=None):
        return self.do_roll(count=count, pips=4)


class DiceD6(Dice):
    """Class for a 6-sided die."""

    def roll(self, count=None):
        return self.do_roll(count=count, pips=6)


class DiceD8(Dice):
    """Class for a 8-sided die."""

    def roll(self, count=None):
        return self.do_roll(count=count, pips=8)


class DiceD10(Dice):
    """Class for a 10-sided die."""

    def roll(self, count=None):
        return self.do_roll(count=count, pips=10)


class DiceD12(Dice):
    """Class for a 12-sided die."""

    def roll(self, count=None):
        return self.do_roll(count=count, pips=12)


class DiceD20(Dice):
    """Class for a 20-sided die."""

    def roll(self, count=None):
        return self.do_roll(count=count, pips=20)


class DiceD100(Dice):
    """Class for a 100-sided die."""

    def roll(self, count=None):
        return self.do_roll(count=count, pips=100)
