import json
from os.path import join
from match import Match  # Certifique-se de que Match esteja importado corretamente


class House:
    def __init__(self):
        self.name = ''
        self.match_list = []

    def loadJson(self, pathJson, model):
        json_path = join("../scriptJson", f"teamsMatches-{pathJson}.json")

        with open(json_path, 'r') as arquivo:
            jsonMatches = json.load(arquivo)

        self.name = jsonMatches['house']
        self.load_matches(jsonMatches['data'])

    def load_matches(self, matches_data):
        for house_match in matches_data:
            match = Match()
            match.house = self.name
            match.match_date = house_match['date']
            match.odds_a = house_match['home_odds']
            match.odds_b = house_match['away_odds']
            match.time_a = house_match['home']
            match.time_b = house_match['away']
            self.match_list.append(match)
