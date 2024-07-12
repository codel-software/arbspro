import json
from match import Match


class House:
    def __init__(self):
        self.name = ''
        self.match_list = []

    def loadJson(self, pathJson, model):
        with open("../scriptJson/teamsMatches-"+pathJson+".json", 'r') as arquivo:
            jsonMatches = json.load(arquivo)
            self.name = jsonMatches['house']
            for house_match in jsonMatches['data']:
                match = Match()
                match.house = self.name
                match.match_date = house_match['date']
                match.odds_a = house_match['home_odds']
                match.odds_b = house_match['away_odds']
                match.time_a = house_match['home']
                match.time_b = house_match['away']
                self.match_list.append(match)
