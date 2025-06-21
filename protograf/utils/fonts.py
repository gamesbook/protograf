# -*- coding: utf-8 -*-
"""
Font utility functions for protograf

Notes:
    There is a noticable "startup"" cost to gather details of all fonts on a
    machine; a cached file is then created and stored in a temp direcory which
    makes this faster in subsequent iterations. Restarting the machine or
    clearing the temp/cache directory will cause this delay again.

Example usage:

from fonts import FontInterface
fi = FontInterface()
fi.load_font_families(cached=False)  # reset cache
print(fi.font_file_css('Bookerly'))
print(fi.font_families.keys()

"""
# lib
from functools import lru_cache
import logging
import os
from pathlib import Path
import pickle
import re
import tempfile
from typing import List, Union
import unicodedata

# third party
from find_system_fonts_filename import (
    get_system_fonts_filename,
    FindSystemFontsFilenameException,
)
from fontTools.ttLib import TTFont, TTLibFileIsCollectionError

# raise log level for fontTools
package_logger = logging.getLogger("fontTools")
package_logger.setLevel(logging.ERROR)

# local
from .support import BUILT_IN_FONTS
from .messaging import feedback


def builtin_font(name: str) -> Union[str, None]:
    """Return a built-in name if it exists."""
    if not name:
        return None
    for available in BUILT_IN_FONTS:
        if str(name).strip().lower() == available.lower():
            return available
    return None


class FontInterface:

    def __init__(self, cache_directory):
        self.name_table = {}
        self.name_table_readable = {}
        self.name_table_summary = {}
        self.post_table = {}
        self.os2_table = {}
        self.font_files = []
        self.font_families = {}
        self.cache_directory = cache_directory or tempfile.gettempdir()

    @lru_cache(maxsize=256)  # limits cache
    def load_font_files(self):
        """Track all font files from the default locations used by the OS."""
        font_filenames = get_system_fonts_filename()
        self.font_files = sorted(list(font_filenames))

    @lru_cache(maxsize=256)  # limits cache
    def load_font_families(self, cached: bool = True, cache_path: str = None):
        """Track family data across all files from default locations used by an OS.

        Args:
            cached (bool): if False, will reload available font_families from the OS
            cache_path (str): location of pickle file; defaults to OS's temp directory
        """
        if not cache_path:
            cache_path = self.cache_directory
        cache_file = os.path.join(cache_path, "font_families.pickle")
        if cached:
            if os.path.exists(cache_file):
                with open(cache_file, "rb") as file:
                    self.font_families = pickle.load(file)
                if self.font_families:
                    return
        feedback("Setting up fonts ... ... ... please be patient!", False)
        self.load_font_files()
        for ffile in self.font_files:
            fdt = self.extract_font_summary(ffile)
            if fdt:
                family = fdt.get("fontFamily")
                # if 'Eagle' in family: breakpoint()
                if family:
                    if family not in list(self.font_families.keys()):
                        self.font_families[family] = []
                    self.font_families[family].append(
                        {
                            "file": fdt["fileName"],
                            "name": fdt["fullName"],
                            "italic": fdt["isItalic"],
                            "class": fdt["fontSubfamily"],
                        }
                    )
                    # register font under alternate (display?) name
                    if fdt["altName"] and fdt["altName"] != fdt["fontFamily"]:
                        family = fdt["altName"]
                        if family not in list(self.font_families.keys()):
                            self.font_families[family] = []
                        self.font_families[family].append(
                            {
                                "file": fdt["fileName"],
                                "name": fdt["fullName"],
                                "italic": fdt["isItalic"],
                                "class": fdt["fontSubfamily"],
                            }
                        )
        if self.font_families:
            with open(cache_file, "wb") as file:
                pickle.dump(self.font_families, file)

    @lru_cache(maxsize=256)  # limits cache
    def get_font_family(self, name: str) -> Union[str, None]:
        """Get proper name for a font family if it exists

        Args:
            name: case-insensitive name of a font family e.g. "bookerly"
        """
        if not name:
            return None
        if not self.font_families:
            self.load_font_families()
        for font_family in list(self.font_families.keys()):
            if str(name).lower() == font_family.lower():
                return font_family
        return None

    @lru_cache(maxsize=256)  # limits cache
    def get_font_file(self, name: str) -> str:
        """Get file name for a specific font style if it exists

        Args:
            name: case-insensitive name of a font style e.g. "bookerly Bold"
        """
        if not name:
            return None
        if not self.font_families:
            self.load_font_families()
        for font_family in list(self.font_families.keys()):
            font_details = self.font_families[font_family]
            for font in font_details:
                if str(name).lower() == font["name"].lower():
                    return font["file"]
                if "Gras" in font["name"]:
                    if (
                        str(name).lower()
                        == font["name"].replace("Gras", "Bold").lower()
                    ):
                        return font["file"]
                if "Italique" in font["name"]:
                    if (
                        str(name).lower()
                        == font["name"].replace("Italique", "Italic").lower()
                    ):
                        return font["file"]

        return None

    @lru_cache(maxsize=256)  # limits cache
    def font_file_css(self, font_family: str) -> Union[str, None]:
        """Create a CSS string to be used by PyMuPDF.

        Args:
            font_family: proper name of a font family

        Returns:
            tuple (str|None, str|None): base file path, CSS styling specification

        Example family entry:
            font_families['Bookerly']:
            [{'file': '/home/user/.local/share/fonts/Bookerly-Bold.ttf',
              'name': 'Bookerly Bold', 'italic': False, 'class': 'Bold'},
             {'file': '/home/user/.local/share/fonts/Bookerly-BoldItalic.ttf',
              'name': 'Bookerly Bold Italic', 'italic': True, 'class': 'Bold Italic'},
             {'file': '/home/user/.local/share/fonts/Bookerly-Regular.ttf',
              'name': 'Bookerly', 'italic': False, 'class': 'Regular'},
             {'file': '/home/user/.local/share/fonts/Bookerly-RegularItalic.ttf',
              'name': 'Bookerly Italic', 'italic': True, 'class': 'Italic'}]

        Example CSS:
            @font-face { font-family: Bookerly;
                         src: url(Bookerly-Bold.ttf);font-weight: bold; }
            @font-face { font-family: Bookerly;
                         src: url(Bookerly-BoldItalic.ttf);font-weight: bold; font-style: italic; }
            @font-face { font-family: Bookerly;
                         src: url(Bookerly-Regular.ttf); }
            @font-face { font-family: Bookerly;
                         src: url(Bookerly-RegularItalic.ttf); font-style: italic; }'
        """
        if not self.font_families:
            self.load_font_families()
        if font_family not in list(self.font_families.keys()):
            return None, None
        styles = self.font_families[font_family]
        css_styles = []
        for style in styles:
            weight = ";"
            if ("Bold" in style["class"] or "Gras" in style["class"]) and (
                "Italic" in style["class"] or "Italique" in style["class"]
            ):
                weight = ";font-weight: bold; font-style: italic;"
            elif "Bold" in style["class"] or "Gras" in style["class"]:
                weight = ";font-weight: bold;"
            elif "Italic" in style["class"] or "Italique" in style["class"]:
                weight = "; font-style: italic;"

            path, url = os.path.split(style["file"])
            css_styles.append(
                f"@font-face {{ font-family: {font_family}; src: url({url}){weight} }}"
            )
        css = " ".join(css_styles)
        return path, css

    def get_ttfont(self, file_path: str):
        """."""
        try:
            font = TTFont(file_path)
            return font
        except TTLibFileIsCollectionError as err:
            if not os.path.exists(file_path):
                print(f"Cannot load font from: {file_path} - {err}")
        return None

    def extract_font_summary(
        self, font_path: Union[str, Path], normalize: bool = True
    ) -> dict:
        """Extract basic metadata from a font file.

        Args:
            font_path (Union[str, Path]): Path to the font file.

        Returns:
            dict: A dictionary containing high-level font summary with keys:
                * fontFamily (str): Font family name.
                * fontSubfamily (str): Font subfamily name.
                * fileName (str): Font file path.
                * uniqueID (str): Unique identifier for the font.
                * fullName (str): Full font name.
                * altName (str): Alternate font name.
                * version (str): Font version.
                * postScriptName (str): PostScript name.
                * weightClass (int): Weight class.
                * isItalic (bool): Whether the font is italic.
        """
        font_info = self.extract_font_details(font_path, normalize)
        result = font_info.get("summary", None) if font_info else None
        return result

    def load_ttfont(self, font_path: Union[str, Path], **kwargs) -> TTFont:
        """Load a TrueType font file."""
        if isinstance(font_path, Path):
            font_path = str(font_path)
        return TTFont(font_path, **kwargs)

    def remove_control_characters(self, text: str, normalize: bool = True) -> str:
        """
        Remove control characters and invisible formatting characters from a string.

        Args:
            text (str): The input string.
            normalize (bool): Whether to normalize the text to remove inconsistencies.

        Returns:
            str: The sanitized string with control and invisible characters removed.
        """
        # Remove basic control characters (C0 and C1 control codes)
        sanitized = re.sub(r"[\x00-\x1F\x7F-\x9F]", "", text)
        # Remove specific Unicode control and invisible formatting characters
        sanitized = re.sub(r"[\u200B-\u200F\u2028-\u202F\u2060-\u206F]", "", sanitized)
        # Remove directional formatting characters (optional, adjust if needed)
        sanitized = re.sub(r"[\u202A-\u202E]", "", sanitized)
        # Optionally, normalize the text to remove any leftover inconsistencies
        if normalize:
            sanitized = unicodedata.normalize("NFKC", sanitized)
        return sanitized

    def extract_font_details(
        self, font_path: Union[str, Path], normalize: bool = True
    ) -> dict:
        """Extract detailed metadata and structural information from a font file.

        Args:
            font_path (Union[str, Path]): Path to the font file.

        Returns:
            dict: A dictionary containing font metadata and tables, including:

                - fileName (str): Path to the font file.
                - tables (list): List of available tables in the font.
                - nameTable (dict): Raw name table values, keyed by nameID.
                - nameTableReadable (dict): Readable name table with keys:
                    * copyright (str): Copyright information.
                    * fontFamily (str): Font family name.
                    * fontSubfamily (str): Font subfamily name.
                    * uniqueID (str): Unique identifier for the font.
                    * fullName (str): Full font name.
                    * version (str): Font version string.
                    * postScriptName (str): PostScript name.
                - cmapTable (dict): Character-to-glyph mappings, keyed by encoding.
                - cmapTableIndex (list): List of encoding descriptions.
                - headTable (dict): Font header table with keys:
                    * unitsPerEm (int): Units per em.
                    * xMin (int): Minimum x-coordinate of the glyph bounding box.
                    * yMin (int): Minimum y-coordinate of the glyph bounding box.
                    * xMax (int): Maximum x-coordinate of the glyph bounding box.
                    * yMax (int): Maximum y-coordinate of the glyph bounding box.
                - hheaTable (dict): Horizontal header table with keys:
                    * ascent (int): Typographic ascent.
                    * descent (int): Typographic descent.
                    * lineGap (int): Line gap.
                - OS2Table (dict): OS/2 table with keys:
                    * usWeightClass (int): Weight class.
                    * usWidthClass (int): Width class.
                    * fsType (int): Embedding restrictions.
                - postTable (dict): PostScript table with keys:
                    * isFixedPitch (bool): Whether the font is monospaced.
                    * italicAngle (float): Italic angle of the font.
                - layoutMetrics (dict): Font layout metrics with keys:
                    * unitsPerEm (int): Units per em.
                    * boundingBox (dict): Bounding box coordinates:
                        - xMin (int): Minimum x-coordinate.
                        - yMin (int): Minimum y-coordinate.
                        - xMax (int): Maximum x-coordinate.
                        - yMax (int): Maximum y-coordinate.
                    * ascent (int): Typographic ascent.
                    * descent (int): Typographic descent.
                    * lineGap (int): Line gap.
                - summary (dict): High-level font summary with keys:
                    * fontFamily (str): Font family name.
                    * fontSubfamily (str): Font subfamily name.
                    * version (str): Font version.
                    * weightClass (int): Weight class.
                    * isItalic (bool): Whether the font is italic.
        """

        if isinstance(font_path, Path):
            font_path = str(font_path)

        font_info = {}
        font = self.get_ttfont(font_path)
        if not font:
            return font_info

        # File name and available tables
        font_info["fileName"] = font_path
        font_info["tables"] = list(font.keys())

        # ---- name table
        self.name_table = {}
        for record in font["name"].names:
            try:
                raw_string = record.string.decode("utf-16-be").strip()
                clean_string = self.remove_control_characters(raw_string, normalize)
                self.name_table[record.nameID] = clean_string
            except UnicodeDecodeError:
                self.name_table[record.nameID] = self.remove_control_characters(
                    record.string.decode(errors="ignore"), normalize
                )
        font_info["nameTable"] = self.name_table

        # ---- Readable name table
        self.name_table_readable = {
            "copyright": self.name_table.get(0, ""),
            "fontFamily": self.name_table.get(1, ""),
            "fontSubfamily": self.name_table.get(2, ""),
            "uniqueID": self.name_table.get(3, ""),
            "fullName": self.name_table.get(4, ""),
            "version": self.name_table.get(5, ""),
            "postScriptName": self.name_table.get(6, ""),
            "altName": self.name_table.get(16, ""),
        }
        font_info["nameTableReadable"] = {
            k: self.remove_control_characters(v, normalize)
            for k, v in self.name_table_readable.items()
        }
        self.name_table_summary = font_info["nameTableReadable"]

        # Parse cmap table
        cmap_table = {}
        cmap_table_index = []

        for cmap in font["cmap"].tables:
            platform_name = {0: "Unicode", 1: "Macintosh", 3: "Windows"}.get(
                cmap.platformID, f"Platform {cmap.platformID}"
            )

            encoding_name = {
                (0, 0): "Unicode 1.0",
                (0, 3): "Unicode 2.0+",
                (0, 4): "Unicode 2.0+ with BMP",
                (1, 0): "Mac Roman",
                (3, 1): "Windows Unicode BMP",
                (3, 10): "Windows Unicode Full",
            }.get((cmap.platformID, cmap.platEncID), f"Encoding {cmap.platEncID}")

            cmap_entries = {}
            for codepoint, glyph_name in cmap.cmap.items():
                char = chr(codepoint)
                cmap_entries[self.remove_control_characters(char, normalize)] = (
                    self.remove_control_characters(glyph_name, normalize)
                )

            key = f"{platform_name}, {encoding_name}"
            cmap_table[key] = cmap_entries
            cmap_table_index.append(key)

        font_info["cmapTable"] = cmap_table
        font_info["cmapTableIndex"] = cmap_table_index

        # Parse head table
        head = font["head"]
        head_table = {
            "unitsPerEm": head.unitsPerEm,
            "xMin": head.xMin,
            "yMin": head.yMin,
            "xMax": head.xMax,
            "yMax": head.yMax,
        }
        font_info["headTable"] = head_table

        # ---- hhea table
        hhea = font["hhea"]
        hhea_table = {
            "ascent": hhea.ascent,
            "descent": hhea.descent,
            "lineGap": hhea.lineGap,
        }
        font_info["hheaTable"] = hhea_table

        # ---- OS/2 table
        os2 = font["OS/2"]
        self.os2_table = {
            "usWeightClass": os2.usWeightClass,
            "usWidthClass": os2.usWidthClass,
            "fsType": os2.fsType,
        }
        font_info["OS2Table"] = self.os2_table

        # ----  post table
        post = font["post"]
        self.post_table = {
            "isFixedPitch": post.isFixedPitch,
            "italicAngle": post.italicAngle,
        }
        font_info["postTable"] = self.post_table

        # Combine layout-related metrics
        font_info["layoutMetrics"] = {
            "unitsPerEm": head_table["unitsPerEm"],
            "boundingBox": {
                "xMin": head_table["xMin"],
                "yMin": head_table["yMin"],
                "xMax": head_table["xMax"],
                "yMax": head_table["yMax"],
            },
            "ascent": hhea_table["ascent"],
            "descent": hhea_table["descent"],
            "lineGap": hhea_table["lineGap"],
        }

        # ----  Font summary
        font_info["summary"] = {
            "fontFamily": self.name_table_summary["fontFamily"],
            "fontSubfamily": self.name_table_summary["fontSubfamily"],
            "fileName": font_path,
            "uniqueID": self.name_table_summary["uniqueID"],
            "fullName": self.name_table_summary["fullName"],
            "altName": self.name_table_summary["altName"],
            "version": self.name_table_summary["version"],
            "postScriptName": self.name_table_summary["postScriptName"],
            "weightClass": os2.usWeightClass if os2 else None,
            "isItalic": self.post_table.get("italicAngle") != 0,
        }

        return font_info
