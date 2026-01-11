# -*- coding: utf-8 -*-
"""
protograf script: common utils

Notes:
    * Dyanamic* classes derived from code at:
      https://alexandra-zaharia.github.io/posts/python-configuration-and-dataclasses/
"""
# lib
import configparser
import sys


def failure(message: str):
    """End the program with a message."""
    print(message)
    sys.exit(0)  # Exit with status code 0 (success)


def as_int(value, label: str = None) -> int:
    """Convert a value to an int

    Args:

    - value (Any): the value to be converted to a float
    - label (str): assigned as part of the error message to ID the type of value
    """
    _label = f"{label} value " if label else "value "
    if value is None:
        failure(f'The {_label}"{value}" is not a valid integer!')
    try:
        the_value = int(value)
        return the_value
    except (ValueError, Exception):
        failure(f'The {_label}"{value}" is not a valid integer!')
    return None


class DynamicConfig:
    """Store dict key-values as class attributes."""

    def __init__(self, conf):
        if not isinstance(conf, dict):
            raise TypeError(f"dict expected, found {type(conf).__name__}")

        self._raw = conf
        for key, value in self._raw.items():
            setattr(self, key, value)


class DynamicConfigIni:
    """Store dict key-values from configparser objects as class attributes."""

    def __init__(self, conf, defs):
        if not isinstance(conf, configparser.ConfigParser):
            raise TypeError(f"ConfigParser expected, found {type(conf).__name__}")

        if not isinstance(defs, configparser.ConfigParser):
            raise TypeError(f"ConfigParser expected, found {type(defs).__name__}")

        # merge default and file-based
        for section in conf.sections():
            if not defs.has_section(section):
                defs.add_section(section)
            for key, value in conf.items(section):
                defs.set(section, key, value)

        # set attrs
        self._raw = defs
        for key, value in self._raw.items():
            setattr(self, key, DynamicConfig(dict(value.items())))
