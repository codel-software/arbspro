from house import House
from scraping import sportRadar
from scraping import scrapingMatchesOdds

def calculate_surebet(odds_a, odds_b, draw_odds):
    return (1 / odds_a) + (1 / odds_b) + (1 / draw_odds)
def identify_surebets(matches):
    surebets = []
    n = len(matches)
    
    for i in range(n):
        for j in range(n):
            if j == i:
                continue
            for k in range(n):
                if k == i or k == j:
                    continue
                # Combinações distintas
                print(n)
                odds_a = matches[i].odds_a
                odds_b = matches[j].odds_b
                draw_odds = matches[k].draw_odds
                surebet_value = calculate_surebet(odds_a, odds_b, draw_odds)
                if surebet_value < 1:
                    surebets.append({
                        'combination': f"{matches[i].house} (A) - {matches[j].house} (B) - {matches[k].house} (Draw)",
                        'value': surebet_value,
                        'odds': (odds_a, odds_b, draw_odds)
                    })
    return surebets

call_sport_radar = sportRadar.run()
call_odds_api = scrapingMatchesOdds.getOddsApi()

houses = []
for return_house in call_sport_radar:
    houses.append(return_house)
for return_house in call_odds_api:
    houses.append(return_house)

list_house_odds = []
for house in houses:
    h = House()
    h.loadJson(pathJson=house)
    for i in h.match_list:
        list_house_odds.append(i)
surebets = identify_surebets(list_house_odds)
print(surebets)
    