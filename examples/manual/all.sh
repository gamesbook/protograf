#!/bin/bash
# CHANGE LINE BELOW AS NEEDED!
#export PYTHONPATH="${PYTHONPATH}:/path/to/"  # parent of proto
rm *.pdf
echo "Creating cards1.pdf..."
python cards1.py
echo "Creating cards2.pdf..."
python cards2.py
echo "Creating cards3.pdf..."
python cards3.py
echo "Creating cards4.pdf..."
python cards4.py
echo "Creating cards5.pdf..."
python cards5.py
echo "Creating cards6.pdf..."
python cards6.py
echo "Creating cards7.pdf..."
python cards7.py
echo "Creating example1.pdf..."
python example1.py
echo "Creating example2.pdf..."
python example2.py
echo "Showing faulty example3.py..."
python example3.py
