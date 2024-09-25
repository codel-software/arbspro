from scraping.scrapingTeams import scrape_teams
from scraping.scrapingMatches import scrape_matches
import json

def run():
    list_house = ['unibet', 'bet365','betclic']
    list_game_type = ['113943','114439']
    for house in list_house:
        for game_type in list_game_type:
            game_text = ''
            if game_type == '113943':
                game_text = 'a'
            else:
                game_text = 'b'
            print(">>>>> Processing sportRadar", house,game_text)
            teams_json_path = scrape_teams(house,game_type,game_text)
            matches_json_path = scrape_matches(house,game_type,game_text)
            
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
                        'home_odds': float(matches_data['fetchedData'][f'stats_season_odds/{game_type}']['data']['odds'][partida_id_str][0]['home']['odds']),
                        'away': team['teams']['away']['name'],
                        'away_odds': float(matches_data['fetchedData'][f'stats_season_odds/{game_type}']['data']['odds'][partida_id_str][0]['away']['odds']),
                        'draw_odds': float(matches_data['fetchedData'][f'stats_season_odds/{game_type}']['data']['odds'][partida_id_str][0]['draw']['odds']),
                    }
                except KeyError as e:
                    continue
                odds.append(team_odd)
                data_to_save = {
                        "house": house,
                        "data": odds
                        }
                caminho_arquivo = "./json/teamsMatches-"+house+'-'+game_text+".json"
                with open(caminho_arquivo, "w") as arquivo_saida:
                    json.dump(data_to_save, arquivo_saida)
            print("<<<<< finish sportRadar", house,game_text)
           
    return ['unibet-a', 'bet365-a','betclic-a','unibet-b', 'bet365-b','betclic-b']
