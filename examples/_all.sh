echo -e "\nCreating PDFs and PNGs for all examples (except those in manual)"
echo ""
mkdir -p /tmp/demo
echo -e "\nAll examples outputs are saved to directories specified in the scripts"
# ---- examples: simple
echo -e "\nCreating basic examples..."
python core/blank.py
python core/demo.py
python core/diagram.py
python core/default_shapes.py
# ----  examples: customised
echo -e "\nCreating customised examples..."
python core/customised_blueprint.py
python core/customised_circle.py
python core/customised_commands.py
python core/customised_hexagon.py
python core/customised_hexagonal_grid.py
python core/customised_hexagonal_grid_locations.py
python core/customised_rectangle.py
python core/customised_shapes.py
python core/customised_text.py
# ---- examples: simple: layouts
echo -e "\nCreating customised layouts..."
python core/layouts/layouts_basic.py
python core/layouts/layouts_rectangular.py
python core/layouts/layouts_triangular.py
python core/layouts/layouts_shapes_outer.py
python core/layouts/layouts_sequence.py
python core/layouts/layouts_tracks.py
python core/layouts/layouts_repeat.py
# ---- examples: objects
python objects/polyominoes.py
python objects/ominoes_basic.py
python objects/pentominoes.py
python objects/dice_d6.py
# ---- boards: abstract
echo -e "\nCreating abstract boards..."
python boards/abstract/chessboard.py
python boards/abstract/chessboard_brown.py
python boards/abstract/go.py
python boards/abstract/hex_game.py
python boards/abstract/hexhex.py
python boards/abstract/hexhex_circles.py
python boards/abstract/hexhex_dots.py
python boards/abstract/hexhex_hexagons.py
python boards/abstract/hexhex_rectangles.py
python boards/abstract/morabaraba.py
python boards/abstract/octagons.py
python boards/abstract/tictactoe.py
# ---- boards: commercial
echo -e "\nCreating commercial boards..."
python boards/commercial/ack_map.py
python boards/commercial/orion_game_board.py
python boards/commercial/squadleader.py
python boards/commercial/traveller_draft.py
python boards/commercial/traveller_black.py
python boards/commercial/underwater_cities.py
python boards/commercial/warpwar.py
python boards/commercial/tm_player_board.py
# ---- boards: maps
echo -e "\nCreating maps..."
python boards/maps/honorverse.py
# ---- counters
echo -e "\nCreating counters..."
python counters/counters.py
python counters/counters_excel.py
python counters/counters_csv.py
python counters/counters_doagc.py
python counters/blocks_csv.py
# ---- cards
echo -e "\nCreating cards..."
python cards/cards_design.py
python cards/cards_hexagonal.py
python cards/cards_circular.py
python cards/cards_rectangular.py
python cards/cards_images.py
python cards/cards_matrix_one.py
python cards/cards_matrix_two.py
python cards/cards_multi_deck.py
python cards/cards_standard.py
# ---- play_money
echo -e "\nCreating play money..."
python play_money/supreme.py
# ---- decks
echo -e "\nCreating decks..."
python cards/cards_deck_01.py
python cards/cards_deck_02.py
python cards/cards_deck_03.py
python cards/cards_deck_04.py
python cards/cards_deck_05.py
python cards/cards_deck_06.py
python cards/cards_deck_07.py
python cards/cards_deck_08.py
python cards/cards_deck_09.py
python cards/cards_deck_10.py
python cards/cards_deck_11.py
python cards/cards_deck_12.py
python cards/cards_deck_13.py
python cards/cards_deck_14.py
python cards/cards_deck_15.py
# -- various
echo -e "\nCreating various..."
python various/clock.py
python various/logo.py
python various/large_objects.py
python various/objects.py
python various/rolling.py
python various/unicode.py
python various/world_clocks.py
# -- Board Game Geek
echo -e "\nCreating BGG game cards..."
python bgg/cards_bgg_basic.py
python bgg/cards_bgg_thumb.py
python bgg/cards_bgg_image.py

echo -e "\nDone!"
