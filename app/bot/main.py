import os
import shutil
import calculo
from bet import Bet
from scrapingMatchesOdds import getOldds
from datetime import datetime


def main():
    # Define o caminho do diretório 'scriptJson'
    caminho_do_diretorio = "../scriptJson"

    # Cria o diretório 'scriptJson' se ele não existir
    os.makedirs(caminho_do_diretorio, exist_ok=True)

    try:
        # Busca no modelo 1
        bet = Bet()
        bet.run()

        # Busca no modelo de API
        getOldds()

        # Busca oportunidades
        calculo.run()

        # Copiar diretório 'scriptJson' para pasta 'data'
        copiar_diretorio_scriptjson_para_data(caminho_do_diretorio)

        print("Processo concluído com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro durante a execução: {str(e)}")
        # Aqui você pode adicionar um registro de log do erro, se desejar


def copiar_diretorio_scriptjson_para_data(caminho_do_diretorio):
    # Caminho para o diretório 'data' (um nível acima do diretório 'scriptJson')
    caminho_do_diretorio_data = os.path.abspath(
        os.path.join(caminho_do_diretorio, "..", "data"))

    # Cria o diretório 'data' se ele não existir
    os.makedirs(caminho_do_diretorio_data, exist_ok=True)

    # Criar um nome de pasta com base na data e hora atual
    data_hora_atual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    pasta_destino = os.path.join(caminho_do_diretorio_data, data_hora_atual)

    # Copiar 'scriptJson' para o diretório de destino
    shutil.copytree(caminho_do_diretorio, pasta_destino)

    print(f"Diretório 'scriptJson' copiado para: {pasta_destino}")


if __name__ == "__main__":
    main()
