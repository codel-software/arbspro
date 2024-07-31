from scraping.scrapingTeams import scrape_teams
from scraping.scrapingMatches import scrape_matches
import json

def run():
    list_house = ['unibet', 'bet365']
    data = []
    for house in list_house:
        print(">>>>> Processing sportRadar", house)
        teams_json_path = scrape_teams(house)
        matches_json_path = scrape_matches(house)
        
        with open(teams_json_path, 'r') as teams_file: # type: ignore
            teams_data = json.load(teams_file)
        with open(matches_json_path, 'r') as matches_file: # type: ignore
            matches_data = json.load(matches_file)
        odds = []
        for team in teams_data:
            partida_id = team['_id']
            partida_id_str = str(partida_id)
            try:
                team_odd = {
                    'date': team['time']['date'],
                    'home': team['teams']['home']['name'],
                    'home_odds': float(matches_data['fetchedData']['stats_season_odds/113943']['data']['odds'][partida_id_str][0]['home']['odds']),
                    'away': team['teams']['away']['name'],
                    'away_odds': float(matches_data['fetchedData']['stats_season_odds/113943']['data']['odds'][partida_id_str][0]['away']['odds']),
                    'draw_odds': float(matches_data['fetchedData']['stats_season_odds/113943']['data']['odds'][partida_id_str][0]['draw']['odds']),
                }
            except KeyError as e:
                continue
            odds.append(team_odd)
            data_to_save = {
                    "house": house,
                    "data": odds
                    }
            caminho_arquivo = "./json/teamsMatches-"+house+".json"
            with open(caminho_arquivo, "w") as arquivo_saida:
                json.dump(data_to_save, arquivo_saida)
    return list_house
