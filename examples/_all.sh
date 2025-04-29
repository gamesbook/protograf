echo -e "\nCreating PDFs and PNGs for all examples (except those in manual)"
echo ""
mkdir -p /tmp/demo
echo -e "\nAll examples outputs are saved to /tmp/demo"
# ---- examples: simple
echo -e "\nCreating basic examples..."
python core/demo.py -d /tmp/demo
python core/diagram.py -d /tmp/demo
python core/default_shapes.py -d /tmp/demo
# ----  examples: customised
echo -e "\nCreating customised examples..."
python core/customised_blueprint.py -d /tmp/demo
python core/customised_circle.py -d /tmp/demo
python core/customised_commands.py -d /tmp/demo
python core/customised_hexagon.py -d /tmp/demo
python core/customised_hexagonal_grid.py -d /tmp/demo
python core/customised_hexagonal_grid_locations.py -d /tmp/demo
python core/customised_rectangle.py -d /tmp/demo
python core/customised_shapes.py -d /tmp/demo
# ---- examples: simple: layouts
echo -e "\nCreating customised layouts..."
python core/layouts/layouts_basic.py -d /tmp/demo
python core/layouts/layouts_rectangular.py -d /tmp/demo
python core/layouts/layouts_triangular.py -d /tmp/demo
python core/layouts/layouts_shapes_outer.py -d /tmp/demo
python core/layouts/layouts_sequence.py -d /tmp/demo
python core/layouts/layouts_tracks.py -d /tmp/demo
python core/layouts/layouts_repeat.py -d /tmp/demo
# ---- boards: abstract
echo -e "\nCreating abstract boards..."
python boards/abstract/chessboard.py -d /tmp/demo
python boards/abstract/chessboard_brown.py -d /tmp/demo
python boards/abstract/go.py -d /tmp/demo
python boards/abstract/hex_game.py -d /tmp/demo
python boards/abstract/hexhex.py -d /tmp/demo
python boards/abstract/hexhex_circles.py -d /tmp/demo
python boards/abstract/hexhex_dots.py -d /tmp/demo
python boards/abstract/hexhex_hexagons.py -d /tmp/demo
python boards/abstract/hexhex_rectangles.py -d /tmp/demo
python boards/abstract/octagons.py -d /tmp/demo
python boards/abstract/tictactoe.py -d /tmp/demo
# ---- boards: commercial
echo -e "\nCreating commercial boards..."
python boards/commercial/ack_map.py -d /tmp/demo
python boards/commercial/orion_game_board.py -d /tmp/demo
python boards/commercial/squadleader.py -d /tmp/demo
python boards/commercial/traveller_draft.py -d /tmp/demo
python boards/commercial/traveller_black.py -d /tmp/demo
python boards/commercial/underwater_cities.py -d /tmp/demo
python boards/commercial/warpwar.py -d /tmp/demo
# ---- boards: maps
echo -e "\nCreating maps..."
python boards/map/honorverse.py -d /tmp/demo
# ---- counters
echo -e "\nCreating counters..."
python counters/counters.py -d /tmp/demo
python counters/counters_excel.py -d /tmp/demo
python counters/counters_csv.py -d /tmp/demo
python counters/blocks_csv.py -d /tmp/demo
# ---- cards
echo -e "\nCreating cards..."
python cards/cards_design.py -d /tmp/demo
python cards/cards_hexagonal.py -d /tmp/demo
python cards/cards_circular.py -d /tmp/demo
python cards/cards_lotr.py -d /tmp/demo
python cards/cards_images.py -d /tmp/demo
python cards/cards_matrix_one.py -d /tmp/demo
python cards/cards_matrix_two.py -d /tmp/demo
python cards/cards_standard.py -d /tmp/demo
# ---- play_money
echo -e "\nCreating play money..."
python play_money/supreme.py -d /tmp/demo
# ---- decks
echo -e "\nCreating decks..."
python cards/cards_deck_01.py -d /tmp/demo
python cards/cards_deck_02.py -d /tmp/demo
python cards/cards_deck_03.py -d /tmp/demo
python cards/cards_deck_04.py -d /tmp/demo
python cards/cards_deck_05.py -d /tmp/demo
python cards/cards_deck_06.py -d /tmp/demo
python cards/cards_deck_07.py -d /tmp/demo
python cards/cards_deck_08.py -d /tmp/demo
python cards/cards_deck_09.py -d /tmp/demo
python cards/cards_deck_10.py -d /tmp/demo
# -- various
echo -e "\nCreating various..."
python various/clock.py -d /tmp/demo
python various/logo.py -d /tmp/demo
python various/large_objects.py -d /tmp/demo
python various/objects.py -d /tmp/demo
python various/rolling.py -d /tmp/demo
python various/unicode.py -d /tmp/demo
python various/world_clocks.py -d /tmp/demo
# -- Board Game Geek
echo -e "\nCreating BGG game cards..."
python bgg/cards_bgg_basic.py -d /tmp/demo
python bgg/cards_bgg_thumb.py -d /tmp/demo
python bgg/cards_bgg_image.py -d /tmp/demo

echo -e "\nDone!"
