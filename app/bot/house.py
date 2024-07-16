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
            if house_match['home_odds']>0 and house_match['away_odds']>0:
                match = Match()
                match.house = self.name
                match.match_date = house_match['date']
                match.odds_a = house_match['home_odds']
                match.odds_b = house_match['away_odds']
                match.time_a = house_match['home']
                match.time_b = house_match['away']
                match.draw_odds = house_match['draw_odds']
                self.match_list.append(match)
