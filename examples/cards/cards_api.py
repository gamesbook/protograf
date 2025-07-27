"""
Deck and Card example using API data for protograf

Written by: Derek Hohls
Created on: 27 July 2025

Font: https://fonts.google.com/specimen/Yanone+Kaffeesatz
"""
from protograf import *
import requests


def get_api_data():
    # TEST data for changing/developing cards
    # countries = [
    #     {'name': "South Africa",
    #      'area': 235549,
    #      'pop': 61393894,
    #      'fifa': "ARA",
    #      'continent': 'Africa'},
    #     {'name': "South Sudan",
    #      'area': 335549,
    #      'pop': 12393894,
    #      'fifa': "SST",
    #      'continent': 'Africa'},
    #     {'name': "Brazil",
    #      'area': 985549,
    #      'pop': 83399194,
    #      'fifa': "BRZ",
    #      'continent': 'South America'},
    #     {'name': "St Georges",
    #      'area': 949,
    #      'pop': 2194,
    #      'fifa': "",
    #      'continent': 'Oceania'},
    # ]
    result = requests.get(
        'https://restcountries.com/v3.1/all?fields=name,area,population,fifa,continents')
    data = result.json()
    countries = [
        {'name': d['name']['common'],
         'area': d['area'],
         'pop': d['population'],
         'fifa': d['fifa'],
         'continent': d['continents'][0]}
        for d in data]
    return countries


def continent_color(data):
    """Use Parker Bros 1960's Risk! board colors"""
    strip_color = "white"
    if data.continent == 'Africa':
        strip_color = '#FD9F85'
    elif data.continent == 'Asia':
        strip_color = '#CDC03D'
    elif data.continent == 'Europe':
        strip_color = '#8AB4CE'
    elif data.continent == 'South America':
        strip_color = '#6FA045'
    elif data.continent == 'Oceania':
        strip_color = '#B0AB8D'
    elif data.continent == 'North America':
        strip_color = '#E7B522'
    elif data.continent == 'Australia':
        strip_color = '#96707F'
    return rectangle(x=0, y=0, width=8.89, height=2, fill_stroke=strip_color)


Create(filename='cards_countries.pdf', margin=1.5, margin_bottom=0.5)
# deck data from API
Data(source=get_api_data(), filters=[('fifa', '', 'ne')])
# design the deck
Deck(
    cards=9,
    card_size="business",
    grid_marks=True,
    fill=None,
)
# design cards
Font('Yanone Kaffeesatz')
Card('all', continent_color)
small_text = Common(x=1, align="left", font_size=18)
Card('all',
     text(text=T('{{ name }}'), x=4.44, y=1.25, font_size=24))
Card('all',
     text(common=small_text, text=T('Population: {{ "{:,}".format(pop) }}'), y=3))
Card('all',
     text(common=small_text, text=T('Area: {{ "{:,}".format(area) }} km²'), y=3.75))
Card('all',
     text(common=small_text, text=T('FIFA: {{ fifa  }}'), y=4.5))
Save()
