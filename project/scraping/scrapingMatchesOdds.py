import requests
import json
from datetime import datetime

team_mapping = {
    "Vasco da Gama": "Vasco Gama",
    "Bragantino-SP": "Bragantino",
    "Cuiabá": "Cuiabá EC"
}


def normalize_team_name(name):
    return team_mapping.get(name, name)


def getOddsApi():
    key = '9c448318f44a5d30f12fe7fbb2e1cf3a'
    url = 'https://api.the-odds-api.com/v4/sports/soccer_brazil_campeonato/odds/?apiKey=' + \
        key+'&regions=us&markets=h2h,spreads&oddsFormat=american'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.json() == []:
        return []
    if response.status_code == 200:
        # html_content = response.text.split("window.__INITIAL_STATE__=", 1)[-1]
        data = response.json()
        organized_data = []

        for odd in data:
            date_obj = datetime.strptime(
                odd['commence_time'], "%Y-%m-%dT%H:%M:%SZ")
            format_date = date_obj.strftime("%d/%m/%Y")

            home_team = odd['home_team']
            away_team = odd['away_team']
            date = format_date
            odds_list = []

            for bet in odd['bookmakers']:
                house_name = bet['title']
                home_odds = None
                away_odds = None
                draw_odds = None

                for market in bet['markets']:
                    if market['key'] == 'h2h':
                        for outcome in market['outcomes']:
                            if outcome['name'] == home_team:
                                if outcome['price'] < 0:
                                    home_odds = 1 + \
                                        (100 / abs(outcome['price']))
                                else:
                                    home_odds = 1 + (outcome['price'] / 100)
                            elif outcome['name'] == away_team:
                                if outcome['price'] < 0:
                                    away_odds = 1 + \
                                        (100 / abs(outcome['price']))
                                else:
                                    away_odds = 1 + (outcome['price'] / 100)
                            elif outcome['name'] == "Draw":
                                if outcome['price'] < 0:
                                    draw_odds = 1 + \
                                        (100 / abs(outcome['price']))
                                else:
                                    draw_odds = 1 + (outcome['price'] / 100)
                normalized_home_team = normalize_team_name(home_team)
                normalized_away_team = normalize_team_name(away_team)
                organized_data.append({
                    "house_name": house_name,
                    "date": date,
                    "home": normalized_home_team,
                    "home_odds": home_odds,
                    "away": normalized_away_team,
                    "away_odds": away_odds,
                    "draw_odds": draw_odds
                })
    unique_house_names = set()
    for bet in organized_data:
        unique_house_names.add(bet['house_name'])
        unique_house_names_list = list(unique_house_names)
    for house in unique_house_names_list:
        data_list = []
        for bet in organized_data:
            if bet['house_name'] == house:
                data_list.append({
                    "date": bet['date'],
                    "home": bet['home'],
                    "home_odds": bet['home_odds'],
                    "away": bet['away'],
                    "away_odds": bet['away_odds'],
                    "draw_odds": bet['draw_odds']
                })
        house_data = {
            "house": house,
            "data": data_list
        }
        caminho_arquivo = "./json/teamsMatches-"+house+".json"
        with open(caminho_arquivo, "w") as arquivo_saida:
            json.dump(house_data, arquivo_saida)
    return unique_house_names_list
