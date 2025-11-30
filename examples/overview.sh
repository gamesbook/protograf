echo -e "\nCreating and assembling a PDF for the overview"
echo " (NOTE that this script requires pdftk to be installed)"
echo ""
mkdir -p /tmp/demo
echo -e "\nAll output is saved to /tmp/demo"
# ---- examples: core
python demo/overview.py --no-png -d /tmp/demo

# examples:games
python objects/pentominoes.py --no-png -d /tmp/demo
python boards/abstract/octagons.py --no-png -d /tmp/demo
python boards/commercial/underwater_cities.py --no-png -d /tmp/demo
python boards/commercial/tm_player_board.py --no-png -d /tmp/demo
python boards/commercial/warpwar.py --no-png -d /tmp/demo
python counters/counters_doagc.py --no-png -d /tmp/demo
python cards/cards_standard.py --no-png -d /tmp/demo
python play_money/supreme.py --no-png -d /tmp/demo
python bgg/cards_bgg_thumb.py --no-png -d /tmp/demo
# extract pages
cd /tmp/demo
pdftk underwater_cities.pdf cat 1left output uw_eg.pdf
pdftk pentominoes.pdf cat 2 output pent_eg.pdf
pdftk cards_standard.pdf cat 1 output cs_eg.pdf
pdftk supreme.pdf cat 7 output su_eg.pdf
pdftk doagc.pdf cat 1left output doagc_eg.pdf
# assemble pages
pdftk overview.pdf octagons.pdf pent_eg.pdf \
  uw_eg.pdf tm_player_board.pdf warpwar.pdf \
  cs_eg.pdf su_eg.pdf  doagc_eg.pdf cards_bgg_thumb.pdf \
  cat output pg_overview.pdf
echo -e "\nDone!"
