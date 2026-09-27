# -*- coding: utf-8 -*-
"""
Example code for protograf

Written by: Derek Hohls
Created on: 27 September 2026

NOTE:
    * This requires python-chess to be installed e.g.
      uv pip install chess
      See https://github.com/niklasf/python-chess
    * Any valid PGN game file can be used; the one here
      was sourced from https://www.pgnmentor.com/files.html
"""
from protograf import *
import chess.pgn

# Setup the document
Create(
    filename="chess_game.pdf",
    paper_height=10,
    paper_width=10,
    margin=1)

# Open and read a game's PGN file
pgn_file = open("game.pgn")
game = chess.pgn.read_game(pgn_file)
hdr = game.headers
title = f"{hdr['Event']}; {hdr['Date']}; {hdr['White']} (W) vs {hdr['Black']} (B)"

# Setup the board
the_board = AbstractGame(name="chess")

# Setup start of game with a title
AbstractState(board=the_board, setup=True)
Text(title, x=0, y=0, font_size=7, align="left")
PageBreak()

# Create a new page for every move in the game
pgn_board = game.board()
for move in game.mainline_moves():
    pgn_board.push(move)
    fen = pgn_board.fen()  # Forsyth-Edwards Notation
    _fen = fen.split(' ')
    positions = _fen[0]
    AbstractState(board=the_board, positions=positions)
    move = floor(pgn_board.ply() / 2 + 0.5)
    Text(f"Move {move}.", x=4, y=8.5, font_size=7)
    PageBreak()

# Save as an animation
Save(
    output='gif',
    dpi='300',
    framerate=1)
