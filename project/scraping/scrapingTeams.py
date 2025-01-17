import requests
import json


def scrape_teams(houseBet, game_type, type_name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36'
    }

    url = 'https://stats.fn.sportradar.com/'+houseBet + \
        '/br/America:Montevideo/gismo/stats_season_fixtures2/'+game_type+'/1'

    response = requests.get(url, headers=headers)

    print(str(response.status_code))
    print(url)

    html_content = response.text
    objeto_python = json.loads(html_content)

    # Verificar e acessar o valor da chave 'data'
    if 'doc' in objeto_python and isinstance(objeto_python['doc'], list):
        # Acessar o primeiro item da lista 'doc'
        primeiro_item = objeto_python['doc'][0]

        # Verificar se 'data' está presente no primeiro item
        if 'data' in primeiro_item:
            dados = primeiro_item['data']
            matches = dados['matches']
            caminho_arquivo = "./json/teams-"+houseBet+"-"+type_name+".json"
            with open(caminho_arquivo, "w") as arquivo_saida:
                json.dump(matches, arquivo_saida)

            return caminho_arquivo
        else:
            print("'data' não encontrada no primeiro item de 'doc'.")
    else:
        print("'doc' não encontrada ou não é uma lista.")
