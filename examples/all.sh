echo -e "\nCreating PDFs for all examples (except those in manual)"
echo ""
mkdir -p /tmp/demo
echo -e "\nAll examples output is saved to /tmp/demo"
# ---- examples: simple
echo -e "\nCreating basic examples..."
python core/demo.py --no-png -d /tmp/demo
python core/blank.py --no-png -d /tmp/demo
python core/diagram.py --no-png -d /tmp/demo
python core/default_shapes.py --no-png -d /tmp/demo
# ----  examples: customised
echo -e "\nCreating customised examples..."
python core/customised_blueprint.py --no-png -d /tmp/demo
python core/customised_circle.py --no-png -d /tmp/demo
python core/customised_commands.py --no-png -d /tmp/demo
python core/customised_hexagon.py --no-png -d /tmp/demo
python core/customised_hexagonal_grid.py --no-png -d /tmp/demo
python core/customised_hexagonal_grid_locations.py --no-png -d /tmp/demo
python core/customised_rectangle.py --no-png -d /tmp/demo
python core/customised_shapes.py --no-png -d /tmp/demo
python core/customised_text.py --no-png -d /tmp/demo
# ---- examples: simple: layouts
echo -e "\nCreating customised layouts..."
python core/layouts/layouts_basic.py --no-png -d /tmp/demo
python core/layouts/layouts_rectangular.py --no-png -d /tmp/demo
python core/layouts/layouts_triangular.py --no-png -d /tmp/demo
python core/layouts/layouts_shapes_outer.py --no-png -d /tmp/demo
python core/layouts/layouts_sequence.py --no-png -d /tmp/demo
python core/layouts/layouts_tracks.py --no-png -d /tmp/demo
python core/layouts/layouts_repeat.py --no-png -d /tmp/demo
# ---- examples: objects
python objects/polyominoes.py --no-png -d /tmp/demo
python objects/pentominoes.py --no-png -d /tmp/demo
python objects/dice_d6.py --no-png -d /tmp/demo
# ---- boards: abstract
echo -e "\nCreating abstract boards..."
python boards/abstract/chessboard.py --no-png -d /tmp/demo
python boards/abstract/chessboard_brown.py --no-png -d /tmp/demo
python boards/abstract/go.py --no-png -d /tmp/demo
python boards/abstract/hex_game.py --no-png -d /tmp/demo
python boards/abstract/hexhex.py --no-png -d /tmp/demo
python boards/abstract/hexhex_circles.py --no-png -d /tmp/demo
python boards/abstract/hexhex_dots.py --no-png -d /tmp/demo
python boards/abstract/hexhex_hexagons.py --no-png -d /tmp/demo
python boards/abstract/hexhex_rectangles.py --no-png -d /tmp/demo
python boards/abstract/morabaraba.py --no-png -d /tmp/demo
python boards/abstract/octagons.py --no-png -d /tmp/demo
python boards/abstract/tictactoe.py --no-png -d /tmp/demo
# ---- boards: commercial
echo -e "\nCreating commercial boards..."
python boards/commercial/ack_map.py --no-png -d /tmp/demo
python boards/commercial/orion_game_board.py --no-png -d /tmp/demo
python boards/commercial/squadleader.py --no-png -d /tmp/demo
python boards/commercial/traveller_draft.py --no-png -d /tmp/demo
python boards/commercial/traveller_black.py --no-png -d /tmp/demo
python boards/commercial/underwater_cities.py --no-png -d /tmp/demo
python boards/commercial/warpwar.py --no-png -d /tmp/demo
# ---- boards: maps
echo -e "\nCreating maps..."
python boards/maps/honorverse.py --no-png -d /tmp/demo
# ---- counters
echo -e "\nCreating counters..."
python counters/counters.py --no-png -d /tmp/demo
python counters/counters_excel.py --no-png -d /tmp/demo
python counters/counters_csv.py --no-png -d /tmp/demo
python counters/blocks_csv.py --no-png -d /tmp/demo
# ---- cards
echo -e "\nCreating cards..."
python cards/cards_design.py --no-png -d /tmp/demo
python cards/cards_hexagonal.py --no-png -d /tmp/demo
python cards/cards_circular.py --no-png -d /tmp/demo
python cards/cards_rectangular.py --no-png -d /tmp/demo
python cards/cards_images.py --no-png -d /tmp/demo
python cards/cards_matrix_one.py --no-png -d /tmp/demo
python cards/cards_matrix_two.py --no-png -d /tmp/demo
python cards/cards_standard.py --no-png -d /tmp/demo
# ---- play_money
echo -e "\nCreating play money..."
python play_money/supreme.py --no-png -d /tmp/demo
# ---- decks
echo -e "\nCreating decks..."
python cards/cards_deck_01.py --no-png -d /tmp/demo
python cards/cards_deck_02.py --no-png -d /tmp/demo
python cards/cards_deck_03.py --no-png -d /tmp/demo
python cards/cards_deck_04.py --no-png -d /tmp/demo
python cards/cards_deck_05.py --no-png -d /tmp/demo
python cards/cards_deck_06.py --no-png -d /tmp/demo
python cards/cards_deck_07.py --no-png -d /tmp/demo
python cards/cards_deck_08.py --no-png -d /tmp/demo
python cards/cards_deck_09.py --no-png -d /tmp/demo
python cards/cards_deck_10.py --no-png -d /tmp/demo
python cards/cards_deck_11.py --no-png -d /tmp/demo
python cards/cards_deck_12.py --no-png -d /tmp/demo
python cards/cards_deck_13.py --no-png -d /tmp/demo
python cards/cards_deck_14.py --no-png -d /tmp/demo
python cards/cards_deck_15.py --no-png -d /tmp/demo
# -- various
echo -e "\nCreating various..."
python various/clock.py --no-png -d /tmp/demo
python various/logo.py --no-png -d /tmp/demo
python various/large_objects.py --no-png -d /tmp/demo
python various/objects.py --no-png -d /tmp/demo
python various/rolling.py --no-png -d /tmp/demo
python various/unicode.py --no-png -d /tmp/demo
python various/world_clocks.py --no-png -d /tmp/demo
# -- Board Game Geek
echo -e "\nCreating BGG game cards..."
python bgg/cards_bgg_basic.py --no-png -d /tmp/demo
python bgg/cards_bgg_thumb.py --no-png -d /tmp/demo
python bgg/cards_bgg_image.py --no-png -d /tmp/demo

echo -e "\nDone!"
