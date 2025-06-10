@echo off
ECHO "Please ensure the virtual environment is active"

md C:\Users\%USERNAME%\Temp\protograf
SET "location=C:\Users\%USERNAME%\Temp\protograf"

ECHO "All examples ouput is saved to: %location%"

REM ----  examples: basic
ECHO "Creating basic examples..."
python core\demo.py --no-png -d %location%
python core\default_shapes.py --no-png -d %location%
python core\diagram.py --no-png -d %location%
python core\default_shapes.py --no-png -d %location%

REM ----  examples: customised
ECHO "Creating customised examples..."
python core\customised_blueprint.py --no-png -d %location%
python core\customised_circle.py --no-png -d %location%
python core\customised_commands.py --no-png -d %location%
python core\customised_hexagon.py --no-png -d %location%
python core\customised_hexagonal_grid.py --no-png -d %location%
python core\customised_hexagonal_grid_locations.py --no-png -d %location%
python core\customised_rectangle.py --no-png -d %location%
python core\customised_shapes.py --no-png -d %location%

REM ---- examples: simple: layouts
ECHO "Creating customised layouts..."
python core\layouts\layouts_basic.py --no-png -d %location%
python core\layouts\layouts_rectangular.py --no-png -d %location%
python core\layouts\layouts_triangular.py --no-png -d %location%
python core\layouts\layouts_shapes_outer.py --no-png -d %location%
python core\layouts\layouts_sequence.py --no-png -d %location%
python core\layouts\layouts_tracks.py --no-png -d %location%
python core\layouts\layouts_repeat.py --no-png -d %location%

REM ---- boards: abstract
ECHO "Creating abstract boards..."
python boards\abstract\chessboard.py --no-png -d %location%
python boards\abstract\chessboard_brown.py --no-png -d %location%
python boards\abstract\go.py --no-png -d %location%
python boards\abstract\hex_game.py --no-png -d %location%
python boards\abstract\hexhex.py --no-png -d %location%
python boards\abstract\hexhex_circles.py --no-png -d %location%
python boards\abstract\hexhex_dots.py --no-png -d %location%
python boards\abstract\hexhex_hexagons.py --no-png -d %location%
python boards\abstract\hexhex_rectangles.py --no-png -d %location%
python boards\abstract\morabaraba.py --no-png -d %location%
python boards\abstract\octagons.py --no-png -d %location%
python boards\abstract\tictactoe.py --no-png -d %location%

REM ---- boards: commercial
ECHO "Creating commercial boards..."
python boards\commercial\ack_map.py --no-png -d %location%
python boards\commercial\orion_game_board.py --no-png -d %location%
python boards\commercial\squadleader.py --no-png -d %location%
python boards\commercial\traveller_draft.py --no-png -d %location%
python boards\commercial\traveller_black.py --no-png -d %location%
python boards\commercial\underwater_cities.py --no-png -d %location%
python boards\commercial\warpwar.py --no-png -d %location%

REM ---- boards: maps
ECHO "Creating maps..."
python boards\maps\honorverse.py  --no-png -d %location%

REM ---- counters
ECHO "Creating counters..."
python counters\counters.py --no-png -d %location%
python counters\counters_excel.py --no-png -d %location%
python counters\counters_csv.py --no-png -d %location%
python counters\blocks_csv.py --no-png -d %location%

REM ---- cards
ECHO "Creating cards..."
python cards\cards_design.py --no-png -d %location%
python cards\cards_hexagonal.py --no-png -d %location%
python cards\cards_circular.py --no-png -d %location%
python cards\cards_rectangular.py --no-png -d %location%
python cards\cards_images.py --no-png -d %location%
python cards\cards_matrix_one.py --no-png -d %location%
python cards\cards_matrix_two.py --no-png -d %location%
python cards\cards_standard.py --no-png -d %location%

REM ---- play_money
ECHO "Creating play money..."
python play_money\supreme.py --no-png -d %location%

REM ---- decks
ECHO "Creating decks..."
python cards\cards_deck_01.py --no-png -d %location%
python cards\cards_deck_02.py --no-png -d %location%
python cards\cards_deck_03.py --no-png -d %location%
python cards\cards_deck_04.py --no-png -d %location%
python cards\cards_deck_05.py --no-png -d %location%
python cards\cards_deck_06.py --no-png -d %location%
python cards\cards_deck_07.py --no-png -d %location%
python cards\cards_deck_08.py --no-png -d %location%
python cards\cards_deck_09.py --no-png -d %location%
python cards\cards_deck_10.py --no-png -d %location%
python cards\cards_deck_11.py --no-png -d %location%
python cards\cards_deck_12.py --no-png -d %location%
python cards\cards_deck_13.py --no-png -d %location%

REM ---- various
ECHO "Creating various..."
python various\clock.py --no-png -d %location%
python various\logo.py --no-png -d %location%
python various\objects.py --no-png -d %location%
python various\large_objects.py --no-png -d %location%
python various\rolling.py --no-png -d %location%
python various\unicode.py --no-png -d %location%
python various\world_clocks.py --no-png -d %location%

REM ---- Board Game Geek
ECHO "Creating BGG game cards..."
python bgg\cards_bgg_basic.py --no-png -d %location%
python bgg\cards_bgg_thumb.py --no-png -d %location%
python bgg\cards_bgg_image.py --no-png -d %location%

ECHO "Done!"
