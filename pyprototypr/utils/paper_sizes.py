#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Also see: http://resources.printhandbook.com/pages/paper-size-chart.php 
#   http://www.printernational.org/american-paper-sizes.php

paper_sizes = {
    '4A0': {'mm': (1682, 2378), 'pt': (4768, 6741)},
    '2A0': {'mm': (1189, 1682), 'pt': (3370, 4768)},
    'A0': {'mm': (841, 1189), 'pt': (2384, 3370)},
    'A1': {'mm': (594, 841), 'pt': (1684, 2384)},
    'A2': {'mm': (420, 594), 'pt': (1191, 1684)},
    'A3': {'mm': (297, 420), 'pt': (842, 1191)},
    'A4': {'mm': (210, 297), 'pt': (595, 842), 'in': (8.27, 11.69)},
    'A5': {'mm': (148, 210), 'pt': (420, 595)},
    'A6': {'mm': (105, 148), 'pt': (298, 420)},
    'A7': {'mm': (74, 105), 'pt': (210, 298)},
    'A8': {'mm': (52, 74), 'pt': (147, 210)},
    'A9': {'mm': (37, 52), 'pt': (105, 147)},
    'A10': {'mm': (26, 37), 'pt': (74, 105)},
    'B0': {'mm': (1000, 1414), 'pt': (2835, 4008)},
    'B1': {'mm': (707, 1000), 'pt': (2004, 2835)},
    'B2': {'mm': (500, 707), 'pt': (1417, 2004)},
    'B3': {'mm': (353, 500), 'pt': (1001, 1417)},
    'B4': {'mm': (250, 353), 'pt': (709, 1001)},
    'B5': {'mm': (176, 250), 'pt': (499, 709)},
    'B6': {'mm': (125, 176), 'pt': (354, 499)},
    'B7': {'mm': (88, 125), 'pt': (249, 354)},
    'B8': {'mm': (62, 88), 'pt': (176, 249)},
    'B9': {'mm': (44, 62), 'pt': (125, 176)},
    'B10': {'mm': (31, 44), 'pt': (88, 125)},
    'C0': {'mm': (917, 1297), 'pt': (2599, 3677)},
    'C1': {'mm': (648, 917), 'pt': (1837, 2599)},
    'C2': {'mm': (458, 648), 'pt': (1298, 1837)},
    'C3': {'mm': (324, 458), 'pt': (918, 1298)},
    'C4': {'mm': (229, 324), 'pt': (649, 918)},
    'C5': {'mm': (162, 229), 'pt': (459, 649)},
    'C6': {'mm': (114, 162), 'pt': (323, 459)},
    'C7': {'mm': (81, 114), 'pt': (230, 323)},
    'C8': {'mm': (57, 81), 'pt': (162, 230)},
    'C9': {'mm': (40, 57), 'pt': (113, 162)},
    'C10': {'mm': (28, 40), 'pt': (79, 113)},
    'Letter': {'pt': (612, 792), 'mm': (215.9, 279.4), 'in': (8.5, 11)},
    'Tabloid': {'pt': (792, 1224), 'mm': (279.4, 431.8), 'in': (11, 17)},
    'Ledger': {'pt': (1224, 792), 'mm': (431.8, 279.4), 'in': (17, 11)},
    'Legal': {'pt': (612, 1008), 'mm': (215.9, 355.6), 'in': (8.5, 14)},
    'JuniorLegal': {'pt': (360, 576), 'mm': (127, 203.2), 'in': (5, 8)},
    'Statement': {'pt': (396, 612),  'mm': (139.7, 215.9), 'in': (5.5, 8.5)},
    'Executive': {'pt': (522, 756),  'mm': (184.2, 266.7), 'in': (7.25, 10.5)},
    'Folio': {'pt': (612, 936), 'mm': (215.9, 330.2), 'in': (8.5, 13)},
    'Quarto': {'pt': (648, 792), 'mm': (228.6, 279.4), 'in': (9, 11)},
    'BusinessCard': {'pt': (252, 144), 'mm': (88.9, 50.8), 'in': (3.5, 2)},
}
