import json
from scrapingTeams import scrape_teams
from scrapingMatches import scrape_matches

def main():
    # Chamando as funções de scraping dos dois scripts
    teams_json_path = scrape_teams()
    matches_json_path = scrape_matches()
    
    # Acessando os dados dos arquivos JSON
    with open(teams_json_path, 'r') as teams_file:
        teams_data = json.load(teams_file)
    with open(matches_json_path, 'r') as matches_file:
        matches_data = json.load(matches_file)
    # odds = matches_data['fetchedData']['stats_season_odds/113943']['data']['odds']['48214399']
    # print(odds)
    odds = []
    for team in teams_data:
        partida_id = team['_id']
        # Convertendo o partida_id para string
        partida_id_str = str(partida_id)
        try:
            team_odd ={ 
                'date':team['time']['date'],
                'match_id':partida_id,
                'team_home_id': team['teams']['home']['_id'],
                'home': team['teams']['home']['name'],
                'home_odds': matches_data['fetchedData']['stats_season_odds/113943']['data']['odds'][partida_id_str][0]['home']['odds'],
                'away': team['teams']['away']['name'],
                'team_away_id': team['teams']['away']['_id'],
                'away_odds': matches_data['fetchedData']['stats_season_odds/113943']['data']['odds'][partida_id_str][0]['away']['odds'],
                'draw_odds': matches_data['fetchedData']['stats_season_odds/113943']['data']['odds'][partida_id_str][0]['draw']['odds'],
            }
        except KeyError as e:
            # print(f"Erro ao acessar as odds para a partida {partida_id_str}: {e}")
            # Definindo os valores para 0
            team_odd = {
                'date':team['time']['date'],
                'match_id':partida_id,
                'team_home_id': team['teams']['home']['_id'],
                'home': team['teams']['home']['name'],
                'home_odds': 'n/a',
                'away': team['teams']['away']['name'],
                'team_away_id': team['teams']['away']['_id'],
                'away_odds': 'n/a',
                'draw_odds': 'n/a',
            }
        odds.append(team_odd)
        for odd in odds:
            print(odd)


if __name__ == "__main__":
    main()
