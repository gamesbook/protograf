# -*- coding: utf-8 -*-
"""
Font utility functions for protograf
"""
from functools import lru_cache
from pathlib import Path
import re
from typing import List, Union
import unicodedata

from find_system_fonts_filename import (
    get_system_fonts_filename, FindSystemFontsFilenameException)
from fontTools.ttLib import TTFont, TTLibFileIsCollectionError


class FontInterface:

    def __init__(self):
        self.name_table = {}
        self.name_table_readable = {}
        self.post_table = {}
        self.os2_table = {}
        self.font_files = []
        self.font_families = {}

    @lru_cache(maxsize=256)  # limits cache
    def load_font_files(self):
        """Track all files from default locations used by an OS."""
        font_filenames = get_system_fonts_filename()
        self.font_files = sorted(list(font_filenames))

    @lru_cache(maxsize=256)  # limits cache
    def load_font_families(self):
        """Track family data across all files from default locations used by an OS."""
        self.load_font_files()
        for ffile in self.font_files:
            fdt = self.extract_font_summary(ffile)
            if fdt:
                family = fdt['fontFamily']
                if family not in list(self.font_families.keys()):
                    self.font_families[family] = []
                self.font_families[family].append(
                    {'file': fdt['fileName'],
                     'name': fdt['fullName'],
                     'italic': fdt['isItalic'],
                     'class': fdt['fontSubfamily']
                })

    @lru_cache(maxsize=256)  # limits cache
    def font_file_css(self, font_family: str):
        """Create a CSS string to be used by PyMuPDF."""

    def get_ttfont(self, file_path: str):
        """."""
        try:
            font = TTFont(file_path)
            return font
        except TTLibFileIsCollectionError as err:
            print(f'Cannot load font from: {file_path} - {err}')
        return None

    def extract_font_summary(
        self,
        font_path: Union[str, Path],
        normalize: bool = True
    ) -> dict:
        """Extract basic metadata and structural information from a font file.

        Args:
            font_path (Union[str, Path]): Path to the font file.

        Returns:
            dict: A dictionary containing high-level font summary with keys:
                * fontFamily (str): Font family name.
                * fontSubfamily (str): Font subfamily name.
                * fileName (str): Font file path
                * uniqueID (str): Unique identifier for the font.
                * fullName (str): Full font name.
                * version (str): Font version.
                * postScriptName (str): PostScript name.
                * weightClass (int): Weight class.
                * isItalic (bool): Whether the font is italic.
        """
        if isinstance(font_path, Path):
            font_path = str(font_path)

        font_info = {}
        font = self.get_ttfont(font_path)
        if not font:
            return font_info

        self.extract_font_details(font_path, normalize)

        font_info = {
            'fontFamily': self.name_table_readable.get('fontFamily'),
            'fontSubfamily': self.name_table_readable.get('fontSubfamily'),
            'fileName': font_path,
            'uniqueID': self.name_table.get(3, ''),
            'fullName': self.name_table.get(4, ''),
            'version': self.name_table_readable.get('version'),
            'postScriptName': self.name_table.get(6, ''),
            'weightClass': self.os2_table.get('usWeightClass'),
            'isItalic': self.post_table.get('italicAngle') != 0
        }
        return font_info

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
        sanitized = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)
        # Remove specific Unicode control and invisible formatting characters
        sanitized = re.sub(
            r'[\u200B-\u200F\u2028-\u202F\u2060-\u206F]', '', sanitized)
        # Remove directional formatting characters (optional, adjust if needed)
        sanitized = re.sub(r'[\u202A-\u202E]', '', sanitized)
        # Optionally, normalize the text to remove any leftover inconsistencies
        if normalize:
            sanitized = unicodedata.normalize('NFKC', sanitized)
        return sanitized

    def extract_font_details(
        self,
        font_path: Union[str, Path],
        normalize: bool = True
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
        font_info['fileName'] = font_path
        font_info['tables'] = list(font.keys())

        # Parse name table
        self.name_table = {}
        for record in font['name'].names:
            try:
                raw_string = record.string.decode('utf-16-be').strip()
                clean_string = self.remove_control_characters(raw_string, normalize)
                self.name_table[record.nameID] = clean_string
            except UnicodeDecodeError:
                self.name_table[record.nameID] = self.remove_control_characters(
                    record.string.decode(errors='ignore'), normalize)
        font_info['nameTable'] = self.name_table

        # Readable name table for common nameIDs
        self.name_table_readable = {
            'copyright': self.name_table.get(0, ''),
            'fontFamily': self.name_table.get(1, ''),
            'fontSubfamily': self.name_table.get(2, ''),
            'uniqueID': self.name_table.get(3, ''),
            'fullName': self.name_table.get(4, ''),
            'version': self.name_table.get(5, ''),
            'postScriptName': self.name_table.get(6, ''),
        }
        font_info['nameTableReadable'] = {
            k: self.remove_control_characters(v, normalize)
            for k, v in self.name_table_readable.items()
        }

        # Parse cmap table
        cmap_table = {}
        cmap_table_index = []

        for cmap in font['cmap'].tables:
            platform_name = {
                0: 'Unicode',
                1: 'Macintosh',
                3: 'Windows'
            }.get(cmap.platformID, f"Platform {cmap.platformID}")

            encoding_name = {
                (0, 0): 'Unicode 1.0',
                (0, 3): 'Unicode 2.0+',
                (0, 4): 'Unicode 2.0+ with BMP',
                (1, 0): 'Mac Roman',
                (3, 1): 'Windows Unicode BMP',
                (3, 10): 'Windows Unicode Full'
            }.get((cmap.platformID, cmap.platEncID), f"Encoding {cmap.platEncID}")

            cmap_entries = {}
            for codepoint, glyph_name in cmap.cmap.items():
                char = chr(codepoint)
                cmap_entries[self.remove_control_characters(char, normalize)] = \
                    self.remove_control_characters(glyph_name, normalize)

            key = f"{platform_name}, {encoding_name}"
            cmap_table[key] = cmap_entries
            cmap_table_index.append(key)

        font_info['cmapTable'] = cmap_table
        font_info['cmapTableIndex'] = cmap_table_index

        # Parse head table
        head = font['head']
        head_table = {
            'unitsPerEm': head.unitsPerEm,
            'xMin': head.xMin,
            'yMin': head.yMin,
            'xMax': head.xMax,
            'yMax': head.yMax,
        }
        font_info['headTable'] = head_table

        # Parse hhea table
        hhea = font['hhea']
        hhea_table = {
            'ascent': hhea.ascent,
            'descent': hhea.descent,
            'lineGap': hhea.lineGap,
        }
        font_info['hheaTable'] = hhea_table

        # Parse OS/2 table
        os2 = font['OS/2']
        self.os2_table = {
            'usWeightClass': os2.usWeightClass,
            'usWidthClass': os2.usWidthClass,
            'fsType': os2.fsType,
        }
        font_info['OS2Table'] = self.os2_table

        # Parse post table
        post = font['post']
        self.post_table = {
            'isFixedPitch': post.isFixedPitch,
            'italicAngle': post.italicAngle,
        }
        font_info['postTable'] = self.post_table

        # Combine layout-related metrics
        font_info['layoutMetrics'] = {
            'unitsPerEm': head_table['unitsPerEm'],
            'boundingBox': {
                'xMin': head_table['xMin'],
                'yMin': head_table['yMin'],
                'xMax': head_table['xMax'],
                'yMax': head_table['yMax']
            },
            'ascent': hhea_table['ascent'],
            'descent': hhea_table['descent'],
            'lineGap': hhea_table['lineGap']
        }

        # Font summary
        font_info['summary'] = {
            'fontFamily': self.name_table_readable['fontFamily'],
            'fontSubfamily': self.name_table_readable['fontSubfamily'],
            'uniqueID': self.name_table.get(3, ''),
            'fullName': self.name_table.get(4, ''),
            'version': self.name_table_readable['version'],
            'postScriptName': self.name_table.get(6, ''),
            'weightClass': os2.usWeightClass,
            'isItalic': self.post_table['italicAngle'] != 0
        }

        return font_info


# fi = FontInterface()
# summ = fi.extract_font_summary(
#     '/home/derek/.local/share/fonts/Adobe/TrueType/Univers LT Std/Univers_LT_Std_65_Bold.ttf')
# pprint.pprint(summ)

"""
import pprint
from fonts import FontInterface
fi = FontInterface()
fi.load_font_files()
len(fi.font_files)
fi.load_font_families()
print(fi.font_families.keys()
"""
