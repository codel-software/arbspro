import json
from core.match import Match
class House:
    def __init__(self):
        self.name = ''
        self.match_list = []
    def loadJson(self,pathJson,model):
        with open("../scriptJson/teamsMatches-"+pathJson+".json", 'r') as arquivo:
            jsonMatches = json.load(arquivo)
            self.name = jsonMatches['house']
            match = Match()
            match.house = self.name
            for house_match in jsonMatches['data']:
                match.match_date = house_match['date']
                match.odds_a = house_match['home_odds']
                match.odds_b = house_match['away_odds']
                match.time_a = house_match['home']
                match.time_b = house_match['away']
                self.match_list.append(match)   
        # carregar o patchjson, a partir do caminho 
        # verificar se ele é do model 1 ou 2
        # instanciar a partida e adicionar na lista