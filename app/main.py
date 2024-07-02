from core.match import Match
from core.data_house.odds_api import odds_api
from core.data_house.sport_radar import sport_radar
from core.house import House

data_base = [sport_radar,odds_api]
for data in data_base:
    model = data.model
    list_house_odds = []
    houses = data.getHouse()
    for house in houses:
        h = House()
        h.loadJson(pathJson=house,model=model)
        list_house_odds.append(h)
    
    print(list_house_odds)
    #percorrer as casas e descobrir as surebets e salvar em outra lista