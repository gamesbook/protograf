"""
Purpose: BoardGameGeek.com API wrapper for protograf
Written by: Derek Hohls
Created on: 21 May 2016
Updated on: 16 January 2024

Notes:

* BGG() uses the `bgg-api` Python library (https://github.com/SukiCZ/boardgamegeek)
* Code is based off of the BGGGame object, for example::

    {'_comments': [],
     '_data': {'accessory': False,
               'alternative_names': ['德国大选', '디 마허'],
               'artists': ['Marcus Gschwendtner', 'Harald Lieske'],
               'categories': ['Economic', 'Negotiation', 'Political'],
               'description': 'Die Macher is a game about seven sequential '
                              'political races in different regions of Germany. '
                              '\n',
               'designers': ['Karl-Heinz Schmiel'],
               'expands': [],
               'expansion': False,
               'expansions': [],
               'families': ['Country: Germany',
                            'Political: Elections',
                            'Series: Classic Line (Valley Games)'],
               'id': 1,
               'image': 'https://cf.geekdo-images.com/rpwCZAjYLD940NWwP3SRoA__original/img/yR0aoBVKNrAmmCuBeSzQnMflLYg=/0x0/filters:format(jpeg)/pic4718279.jpg',
               'implementations': [],
               'maxplayers': 5,
               'maxplaytime': 240,
               'mechanics': ['Alliances',
                             'Area Majority / Influence',
                             'Auction/Bidding',
                             'Dice Rolling',
                             'Hand Management',
                             'Simultaneous Action Selection'],
               'minage': 14,
               'minplayers': 3,
               'minplaytime': 240,
               'name': 'Die Macher',
               'playingtime': 240,
               'publishers': ['Hans im Glück',
                              'Moskito Spiele',
                              'Portal Games',
                              'Spielworxx',
                              'sternenschimmermeer',
                              'Stronghold Games',
                              'Valley Games, Inc.',
                              'YOKA Games'],
               'stats': {'average': 7.61437,
                         'averageweight': 4.3206,
                         'bayesaverage': 7.10354,
                         'median': 0.0,
                         'numcomments': 2011,
                         'numweights': 761,
                         'owned': 7511,
                         'ranks': [{'friendlyname': 'Board Game Rank',
                                    'id': '1',
                                    'name': 'boardgame',
                                    'value': 316},
                                   {'friendlyname': 'Strategy Game Rank',
                                    'id': '5497',
                                    'name': 'strategygames',
                                    'value': 180}],
                         'stddev': 1.58031,
                         'trading': 249,
                         'usersrated': 5356,
                         'wanting': 504,
                         'wishing': 2050},
               'suggested_players': {'results': {
                        '1': {'best_rating': 0,
                              'not_recommended_rating': 83,
                              'recommended_rating': 1},
                        '2': {'best_rating': 0,
                              'not_recommended_rating': 85,
                              'recommended_rating': 1},
                        '3': {'best_rating': 2,
                              'not_recommended_rating': 73,
                              'recommended_rating': 26},
                        '4': {'best_rating': 25,
                              'not_recommended_rating': 9,
                              'recommended_rating': 84},
                        '5': {'best_rating': 111,
                              'not_recommended_rating': 2,
                              'recommended_rating': 12},
                        '5+': {'best_rating': 1,
                               'not_recommended_rating': 59,
                               'recommended_rating': 0}},
                         'total_votes': 132},
               'thumbnail': 'https://cf.geekdo-images.com/rpwCZAjYLD940NWwP3SRoA__thumb/img/YT6svCVsWqLrDitcMEtyazVktbQ=/fit-in/200x150/filters:strip_icc()/pic4718279.jpg',
               'yearpublished': 1986},
     '_expands': [],
     '_expands_set': set(),
     '_expansions': [],
     '_expansions_set': set(),
     '_id': 1,
     '_image': 'https://cf.geekdo-images.com/rpwCZAjYLD940NWwP3SRoA__original/img/yR0aoBVKNrAmmCuBeSzQnMflLYg=/0x0/filters:format(jpeg)/pic4718279.jpg',
     '_name': 'Die Macher',
     '_player_suggestion': [<boardgamegeek.objects.games.PlayerSuggestion>,
                            <boardgamegeek.objects.games.PlayerSuggestion>,
                            <boardgamegeek.objects.games.PlayerSuggestion>,
                            <boardgamegeek.objects.games.PlayerSuggestion>,
                            <boardgamegeek.objects.games.PlayerSuggestion>,
                            <boardgamegeek.objects.games.PlayerSuggestion>],
     '_stats': <boardgamegeek.objects.games.BoardGameStats>,
     '_thumbnail': 'https://cf.geekdo-images.com/rpwCZAjYLD940NWwP3SRoA__thumb/img/YT6svCVsWqLrDitcMEtyazVktbQ=/fit-in/200x150/filters:strip_icc()/pic4718279.jpg',
     '_versions': [],
     '_versions_set': set(),
     '_videos': [],
     '_videos_ids': set(),
     '_year_published': 1986
     }

"""

# lib
import os
import pickle
from pathlib import Path

# third party
from boardgamegeek import BGGClient
from boardgamegeek.objects.things import Thing
from boardgamegeek.exceptions import BGGApiError
from boardgamegeek.objects.games import CollectionBoardGame
from boardgamegeek.objects.games import BoardGame

# local
from protograf.utils.messaging import feedback
from protograf.utils.support import CACHE_DIRECTORY
from protograf.utils import tools


class BGGGame:
    """Wrapper around the `game` object from boardgamegeek.api"""

    def __init__(
        self,
        game_id: int = None,
        user: str = None,
        user_game: CollectionBoardGame = None,
        short: int = 500,
    ):
        """
        Args:
            user_game: obj
                a boardgamegeek.game.CollectionBoardGame object
            game_id: int
                Unique BGG number for a boardgame
            short: int
                number of characters to use for short description
        """
        self._game = None
        self.user_game = user_game
        self.user = user or ""
        self.short = int(short) or 500
        self.bgg = BGGClient()
        self.cache_directory = Path(Path.home() / CACHE_DIRECTORY / "bgg")
        self.cache_directory.mkdir(parents=True, exist_ok=True)
        # load and cache game
        local_cache = False
        if not self._game:
            game_id = tools.as_int(game_id, "game ID", minimum=1)
            self._game, local_cache = self.load_game(game_id)
        if self._game:
            self.set_properties()
            if not local_cache:
                self.save_game()  # do cache

    def load_game(self, game_id: int) -> (BoardGame, bool):
        """Retrieve and save boardgame; from BGG or local cache.

        Returns:
            tuple (boardgamegeek.objects.games.BoardGame object, bool):
                bool is True if loaded from file; False if from API
        """
        the_game = None
        game_file = f"{game_id}_{self.user}.pck" if self.user_game else f"{game_id}.pck"
        try:
            filename = Path(self.cache_directory / game_file)
            with open(str(filename), "rb") as filehandler:
                the_game = pickle.load(filehandler)
                return the_game, True
                # print(f' !!! loaded {game_file} for GameID#{game_id}')
        except:
            try:
                the_game = self.bgg.game(game_id=game_id)
                if not the_game:
                    feedback(f"Unable to load Game #{game_id} from BGG", False, True)
                return the_game, False
            except BGGApiError as err:
                if "Failed to resolve 'boardgamegeek.com'" in str(err):
                    msg = "Test if your internet connection reaches boardgamegeek.com"
                else:
                    msg = err
                feedback(f"Unable to access boardgamegeek API ({msg})", True)
            except Exception as err:
                feedback(f"Unable to create game: {game_id} ({err})", True)
        return the_game, None

    def save_game(self):
        """Retrieve game from BGG or local cache.

        Notes:
            * Base game filename is the ID of the game
            * Game files where user's collection data are available and stored
              are appended with the user's name.
        """
        game_id = f"{self._game.id}"
        game_file = f"{game_id}_{self.user}.pck" if self.user_game else f"{game_id}.pck"
        filename = Path(self.cache_directory / game_file)
        with open(str(filename), "wb") as file_pickle:
            pickle.dump(self._game, file_pickle)
        # print(f' !!! saved {game_file} for GameID#{game_id}')

    def get_description_short(self):
        """Create an abbreviated description for a game."""
        if self._game:
            desc = self._game.description[0 : self.short]
            _cut = int(
                (
                    len(desc)
                    - len(desc.replace(",", "").replace(".", "").replace(":", ""))
                )
                / 2
                + self.short
            )
            desc = self._game.description[0:_cut]
            return desc[0:-3] + "..."

    def set_properties(self):
        """Create both raw (_ prefix) and string formatted versions of props"""
        if not self._game:
            return
        self._alternative_names = self._game.alternative_names
        self.alternative_names = ", ".join(self._game.alternative_names)
        self._artists = self._game.artists
        self.artists = ", ".join(self._game.artists)
        self._average = self._game.stats["average"]
        self.average = "%.3f" % self._game.stats["average"]
        self._averageweight = self._game.stats["averageweight"]
        self.averageweight = "%.3f" % self._game.stats["averageweight"]
        self._bayesaverage = self._game.stats["bayesaverage"]
        self.bayesaverage = "%.3f" % self._game.stats["bayesaverage"]
        self._categories = self._game.categories
        self.categories = ", ".join(self._game.categories)
        self._description = self._game.description
        self.description = f"{self._game.description}"
        self._designers = self._game.designers
        self.designers = ", ".join(self._game.designers)
        self._expands = self._game.expands
        try:
            self.expands = ", ".join(self._game.expands)
        except TypeError:
            self.expands = ""
            for item in self._game.expands:
                if isinstance(item, Thing):
                    new_game, from_file = self.load_game(item.id)
                    if new_game:
                        self.expands += new_game.name + ","
            if len(self.expands) > 0:
                self.expands = self.expands[:-1]
            # print(f'Cannot turn {self._game.expands} into a list from type '
            #       f'{type(self._game.expands)} for ID#{self._game.id}')
        self._expansion = self._game.expansion
        if self._game.expansion is True:
            self.expansion = "Yes"
        else:
            self.expansion = "False"
        self._expansions = self._game.expansions
        if self._expansions:
            names = []
            for exp in self._expansions:
                names.append(exp.name)
            self.expansions = ", ".join(names)
        else:
            self.expansions = ""
        self._families = self._game.families
        self.families = ", ".join(self._game.families)
        self._id = self._game.id
        self.id = f"{self._game.id}"
        self._image = self._game.image
        self.image = f"{self._game.image}"
        self._implementations = self._game.implementations
        self.implementations = ", ".join(self._game.implementations)
        self._maxplayers = self._game.maxplayers
        self.maxplayers = f"{self._game.maxplayers}"
        self._mechanics = self._game.mechanics
        self.mechanics = ", ".join(self._game.mechanics)
        self._median = self._game.stats["median"]
        self.median = "%.3f" % self._game.stats["median"]
        self._minage = self._game.minage
        self.minage = f"{self._game.minage}"
        self._minplayers = self._game.minplayers
        self.minplayers = f"{self._game.minplayers}"
        self._name = self._game.name
        self.name = f"{self._game.name}"
        self._numcomments = self._game.stats["numcomments"]
        self.numcomments = f"{self._game.stats['numcomments']}"
        self._numweights = self._game.stats["numweights"]
        self.numweights = f"{self._game.stats['numweights']}"
        self._owned = self._game.stats["owned"]
        self.owned = f"{self._game.stats['owned']}"
        self._playingtime = self._game.playingtime
        self.playingtime = f"{self._game.playingtime}"
        self._publishers = self._game.publishers
        self.publishers = ", ".join(self._game.publishers)
        self._ranks = self._game.stats["ranks"]
        self.ranks = f"{self._game.stats['ranks']}"
        self._stddev = self._game.stats["stddev"]
        self.stddev = "%.3f" % self._game.stats["stddev"]
        self._thumbnail = self._game.thumbnail
        self.thumbnail = f"{self._game.thumbnail}"
        self._trading = self._game.stats["trading"]
        self.trading = f"{self._game.stats['trading']}"
        self._usersrated = self._game.stats["usersrated"]
        self.usersrated = f"{self._game.stats['usersrated']}"
        self._wanting = self._game.stats["wanting"]
        self.wanting = f"{self._game.stats['wanting']}"
        self._wishing = self._game.stats["wishing"]
        self.wishing = f"{self._game.stats['wishing']}"
        self._yearpublished = self._game.yearpublished
        self.yearpublished = f"{self._game.yearpublished}"
        # custom fields
        self.description_short = self.get_description_short()
        self._description_short = self.description_short
        if self._game.minplayers == self._game.maxplayers:
            self.players = f"{self._game.maxplayers}"
        else:
            self.players = f"{self._game.minplayers}-{self._game.maxplayers}"
        self._players = (self._game.minplayers, self._game.maxplayers)
        self.age = f"{self._game.minage}+"
        self._age = self._game.minage
        if self.user_game:
            self.user_rating = tools.as_float(
                self.user_game.rating, "BGG user rating", stop=False
            )
            self.user_own = tools.as_bool(self.user_game.own)
            self.user_preordered = tools.as_bool(self.user_game.preordered)
            self.user_prevowned = tools.as_bool(self.user_game.prevowned)
            self.user_want = tools.as_bool(self.user_game.want)
            self.user_wanttobuy = tools.as_bool(self.user_game.wanttobuy)
            self.user_wanttoplay = tools.as_bool(self.user_game.wanttoplay)
            self.user_fortrade = tools.as_bool(self.user_game.fortrade)
            self.user_wishlist = tools.as_bool(self.user_game.wishlist)
            self.user_wishlistpriority = tools.as_int(
                self.user_game.wishlistpriority, "BGG user wishlist priority"
            )

    def display(self):
        """Display all properties and values of a BGGGame."""
        for attr in dir(self):
            if "__" not in attr:
                print("%s: %r" % (attr, getattr(self, attr)))

    def properties(self):
        """Return all properties of a BGGGame as list."""
        props = []
        for attr in dir(self):
            if "__" not in attr:
                props.append(attr)
        return props


class BGGGameList:
    """Lists which are groups of multiple games' string-based properties."""

    def __init__(self, user=None, **kwargs):
        """create empty lists to hold values"""
        self.bgg = BGGClient(requests_per_minute=120)
        self.user = user
        self.collection = None  # boardgamegeek.collection.Collection
        if self.user:
            self.collection = self.bgg.collection(user_name=user, **kwargs)
        self.game_data = []  # list of games; each as a list of values
        self.games = []  # list of BGGGame objects
        self.alternative_names = []
        self.artists = []
        self.average = []
        self.averageweight = []
        self.bayesaverage = []
        self.categories = []
        self.description = []
        self.designers = []
        self.expands = []
        self.expansion = []
        self.expansions = []
        self.families = []
        self.id = []
        self.image = []
        self.implementations = []
        self.maxplayers = []
        self.mechanics = []
        self.median = []
        self.minage = []
        self.minplayers = []
        self.name = []
        self.numcomments = []
        self.numweights = []
        self.owned = []
        self.playingtime = []
        self.publishers = []
        self.ranks = []
        self.stddev = []
        self.thumbnail = []
        self.trading = []
        self.usersrated = []
        self.wanting = []
        self.wishing = []
        self.yearpublished = []
        # custom fields
        self.players = []
        self.description_short = []
        self.age = []

    def set_values(self, game):
        """Append a game's property to a matching list."""
        self._game = game  # BGGGame object
        if self._game:
            self.games.append(game)
            self.alternative_names.append(self._game.alternative_names)
            self.artists.append(self._game.artists)
            self.average.append(self._game.average)
            self.averageweight.append(self._game.averageweight)
            self.bayesaverage.append(self._game.bayesaverage)
            self.categories.append(self._game.categories)
            self.description.append(self._game.description)
            self.designers.append(self._game.designers)
            self.expands.append(self._game.expands)
            self.expansion.append(self._game.expansion)
            self.expansions.append(self._game.expansions)
            self.families.append(self._game.families)
            self.id.append(self._game.id)
            self.image.append(self._game.image)
            self.implementations.append(self._game.implementations)
            self.maxplayers.append(self._game.maxplayers)
            self.mechanics.append(self._game.mechanics)
            self.median.append(self._game.median)
            self.minage.append(self._game.minage)
            self.minplayers.append(self._game.minplayers)
            self.name.append(self._game.name)
            self.numcomments.append(self._game.numcomments)
            self.numweights.append(self._game.numweights)
            self.owned.append(self._game.owned)
            self.playingtime.append(self._game.playingtime)
            self.publishers.append(self._game.publishers)
            self.ranks.append(self._game.ranks)
            self.stddev.append(self._game.stddev)
            self.thumbnail.append(self._game.thumbnail)
            self.trading.append(self._game.trading)
            self.usersrated.append(self._game.usersrated)
            self.wanting.append(self._game.wanting)
            self.wishing.append(self._game.wishing)
            self.yearpublished.append(self._game.yearpublished)
            # custom fields
            self.players.append(self._game.players)
            self.description_short.append(self._game.description_short)
            self.age.append(self._game.age)

    @property
    def data_list(self) -> list:
        """Return `game_data` - list of game list data."""
        if len(self.games) < 1:
            return []
        properties = self.games[0].properties()
        # append one row per game; data matched to header
        for _game in self.games:
            game_list = []
            for attr in properties:
                game_list.append(getattr(_game, attr))
            self.game_data.append(game_list)
        # TODO sort on a key
        # self.game_data.sort(key=lambda x: x[3])
        # create header row
        headers = [prop.upper() for prop in properties]
        self.game_data.insert(0, headers)
        return self.game_data
