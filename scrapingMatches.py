import requests
import json

def scrape_matches():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36'
    }
    houseBet = 'unibet'

    url = 'https://s5.sir.sportradar.com/'+houseBet+'/br/1/season/113943/fixtures/full'

    response = requests.get(url, headers=headers)

    # Verificar se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Obter o conteúdo HTML da página
        html_content = response.text.split("window.__INITIAL_STATE__=", 1)[-1]
        html_content = html_content.split("window.__TRANSLATIONS_FILE__", 1)[0]
        # print(html_content)
        objeto_python = json.loads(html_content)
        # print(objeto_python)
        # Caminho para o arquivo de saída JSON
        caminho_arquivo = "matches-"+houseBet+".json"

        # Salvar o objeto Python como JSON em um arquivo
        with open(caminho_arquivo, "w") as arquivo_saida:
            json.dump(objeto_python, arquivo_saida)
        return caminho_arquivo
    else:
        print(f"Falha na requisição: {response.status_code}")
