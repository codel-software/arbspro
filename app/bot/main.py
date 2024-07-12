import calculo
from bet import Bet
from scrapingMatchesOdds import getOldds
import os
from search import search

# Define o caminho do diretório
caminho_do_diretorio = "../scriptJson"

# Cria o diretório se ele não existir
os.makedirs(caminho_do_diretorio, exist_ok=True)

# Busca no modelo 1
bet = Bet()
bet.run()

# Busca no modelo de API
getOldds()

# Busca oportunidades
# search()
calculo.run()
