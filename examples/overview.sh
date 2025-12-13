echo -e "\nCreating and assembling a PDF for the overview"
echo " (NOTE: this script requires pdftk to be installed)"
echo -e "\nAll output will be saved to /tmp/demo"
mkdir -p /tmp/demo
# ---- examples: core
echo -e "Creating core..."
python demo/overview.py --no-png -d /tmp/demo
# ---- examples:games
echo -e "Creating basic examples..."
python objects/pentominoes.py --no-png -d /tmp/demo
echo -e "Creating commercial boards..."
python boards/commercial/underwater_cities.py --no-png -d /tmp/demo
python boards/commercial/warpwar.py --no-png -d /tmp/demo
echo -e "Creating counters and money..."
python counters/counters_doagc.py --no-png -d /tmp/demo
python play_money/supreme.py --no-png -d /tmp/demo
echo -e "Creating playing cards..."
python cards/cards_standard.py --no-png -d /tmp/demo
echo -e "Creating BGG game cards..."
python bgg/cards_bgg_thumb.py --no-png -d /tmp/demo
# ---- extract pages
echo -e "Extracting subsets..."
cd /tmp/demo
pdftk underwater_cities.pdf cat 1left output uw_eg.pdf
pdftk pentominoes.pdf cat 2 output pent_eg.pdf
pdftk cards_standard.pdf cat 1 output cs_eg.pdf
pdftk supreme.pdf cat 7 output su_eg.pdf
pdftk doagc.pdf cat 1left output doagc_eg.pdf
# ---- assemble pages
echo -e "Assembling pages..."
pdftk overview.pdf \
  pent_eg.pdf \
  uw_eg.pdf warpwar.pdf \
  cs_eg.pdf su_eg.pdf doagc_eg.pdf cards_bgg_thumb.pdf \
  cat output pg_overview.pdf
echo -e "\nDone!"
# ---- show PDF
xreader pg_overview.pdf
