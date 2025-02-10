@echo off
ECHO "Please ensure the virtual environment is active"

md C:\Users\%USERNAME%\AppData\Local\Temp\protograf
SET "location=C:\Users\%USERNAME%\AppData\Local\Temp\protograf"

ECHO "All examples ouput is saved to: %location%"

REM ----  examples: basic
ECHO "Creating basic examples..."
python core\demo.py -d %location%
python core\default_shapes.py -d %location%
python core\diagram.py -d %location%"
python core\default_shapes.py -d %location%"

REM ----  examples: customised
ECHO "Creating customised examples..."
python core\customised_blueprint.py -d %location%"
python core\customised_circle.py -d %location%"
python core\customised_commands.py -d %location%"
python core\customised_hexagon.py -d %location%"
python core\customised_hexagonal_grid.py -d %location%"
python core\customised_hexagonal_grid_locations.py -d %location%"
python core\customised_rectangle.py -d %location%"
python core\customised_shapes.py -d %location%"

REM ---- examples: simple: layouts
ECHO "Creating customised layouts..."
python core\layouts\layouts_basic.py -d %location%"
python core\layouts\layouts_rectangular.py -d %location%"
python core\layouts\layouts_triangular.py -d %location%"
python core\layouts\layouts_shapes_outer.py -d %location%"
python core\layouts\layouts_sequence.py -d %location%"
python core\layouts\layouts_tracks.py -d %location%"
python core\layouts\layouts_repeat.py -d %location%"

REM ---- boards: abstract
ECHO "Creating abstract boards..."
python boards\abstract\chessboard.py -d %location%"
python boards\abstract\chessboard_brown.py -d %location%"
python boards\abstract\go.py -d %location%"
python boards\abstract\hex_game.py -d %location%"
python boards\abstract\hexhex.py -d %location%"
python boards\abstract\hexhex_circles.py -d %location%"
python boards\abstract\hexhex_dots.py -d %location%"
python boards\abstract\hexhex_hexagons.py -d %location%"
python boards\abstract\hexhex_rectangles.py -d %location%"
python boards\abstract\octagons.py -d %location%"
python boards\abstract\tictactoe.py -d %location%"

REM ---- boards: commercial
ECHO "Creating commercial boards..."
python boards\commercial\ack_map.py -d %location%"
python boards\commercial\orion_game_board.py -d %location%"
python boards\commercial\squadleader.py -d %location%"
python boards\commercial\traveller_draft.py -d %location%"
python boards\commercial\traveller_black.py -d %location%"
python boards\commercial\underwater_cities.py -d %location%"
python boards\commercial\warpwar.py -d %location%"

REM ---- counters
ECHO "Creating counters..."
python counters\counters.py -d %location%"
python counters\counters_excel.py -d %location%"
python counters\counters_csv.py -d %location%"
python counters\blocks_csv.py -d %location%"

REM ---- cards
ECHO "Creating cards..."
python cards\cards_design.py -d %location%"
python cards\cards_hexagonal.py -d %location%"
python cards\cards_circular.py -d %location%"
python cards\cards_lotr.py -d %location%"
python cards\cards_images.py -d %location%"
python cards\cards_matrix_one.py -d %location%"
python cards\cards_matrix_two.py -d %location%"
python cards\cards_standard.py -d %location%"

REM ---- decks
ECHO "Creating decks..."
python cards\cards_deck_01.py -d %location%"
python cards\cards_deck_02.py -d %location%"
python cards\cards_deck_03.py -d %location%"
python cards\cards_deck_04.py -d %location%"
python cards\cards_deck_05.py -d %location%"
python cards\cards_deck_06.py -d %location%"
python cards\cards_deck_07.py -d %location%"
python cards\cards_deck_08.py -d %location%"
python cards\cards_deck_09.py -d %location%"
python cards\cards_deck_10.py -d %location%"

REM ---- various
ECHO "Creating various..."
python various\chords.py -d %location%"
python various\clock.py -d %location%"
python various\logo.py -d %location%"
python various\objects.py -d %location%"
python various\rolling.py -d %location%"
python various\unicode.py -d %location%"
python various\world_clocks.py -d %location%"

REM ---- Board Game Geek
ECHO "Creating BGG game cards..."
python bgg\cards_bgg_basic.py -d %location%"
python bgg\cards_bgg_thumb.py -d %location%"
python bgg\cards_bgg_image.py -d %location%"

ECHO "Done!"
