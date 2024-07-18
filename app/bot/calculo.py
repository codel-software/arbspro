from operator import truediv
from calculoCustos import CalculoCustos
from match import Match
from data_house.odds_api import odds_api
from data_house.sport_radar import sport_radar
from house import House
import math


def process_odd(odd_1, odd_2):
    surebets = []  # Usando um conjunto para garantir que cada surebet seja único

    for match_odd_1 in odd_1.match_list:
        for match_odd_2 in odd_2.match_list:
            if match_odd_1.time_a == match_odd_2.time_a and \
               match_odd_1.time_b == match_odd_2.time_b and \
               match_odd_1.match_date == match_odd_2.match_date:
                aposta_11_22 = (1 / match_odd_1.odds_a) + \
                    (1 / match_odd_2.odds_b)
                aposta_21_12 = (1 / match_odd_2.odds_a) + \
                    (1 / match_odd_1.odds_b)
                surebet = aposta_11_22 < 1 or aposta_21_12 < 1

                all_odds = [match_odd_1.odds_a,match_odd_1.odds_b,match_odd_2.odds_a,match_odd_2.odds_b]
                check_surebet = {
                    "casa_a": match_odd_1.house,
                    "casa_b": match_odd_2.house,
                    "time_a": match_odd_1.time_a,
                    "time_b": match_odd_1.time_b,
                    "odds_a_time_a": match_odd_1.odds_a,
                    "odds_b_time_a": match_odd_1.odds_b,
                    "odds_a_time_b": match_odd_2.odds_a,
                    "odds_b_time_b": match_odd_2.odds_b,
                    "aposta_11_22": aposta_11_22,
                    "aposta_21_12": aposta_21_12,
                    "retorno_esperado_aposta_11_22": (1-aposta_11_22)*100,
                    "retorno_esperado_aposta_21_12": (1-aposta_21_12)*100,
                    "media_odds": (sum(all_odds)/len(all_odds)),
                    "volatilidade": math.sqrt(((match_odd_1.odds_a - (sum(all_odds)/len(all_odds))) ** 2 + \
                    (match_odd_1.odds_b - (sum(all_odds)/len(all_odds))) ** 2 + \
                    (match_odd_2.odds_a - (sum(all_odds)/len(all_odds))) ** 2 + \
                    (match_odd_2.odds_b - (sum(all_odds)/len(all_odds))) ** 2) / 4),
                    "surebet": surebet
                }

                # Convertendo para tuple para usar como chave única
                surebets.append(check_surebet)

    return surebets


def run():
    # Aqui você pode adicionar mais fontes de dados, se necessário
    data_base = [odds_api,sport_radar]

    # Percorre os modelos
    for data in data_base:
        list_house_odds = []
        houses = data.getHouse()
        # Percorre as casa de cada modelo
        for house in houses:
            h = House()
            h.loadJson(pathJson=house, model=data.model)
            list_house_odds.append(h)

        lista_possiveis_surebets = []
        # Pega as partidas e compara 1 com a outra
        for i, odd_1 in enumerate(list_house_odds):
            # Evita comparar um objeto com ele mesmo e comparações duplicadas
            for odd_2 in list_house_odds[i+1:]:
                possivel_surebets = process_odd(odd_1, odd_2)
                for possivel_surebet in possivel_surebets:
                    lista_possiveis_surebets.append(possivel_surebet)
        # Imprimir os resultados ou realizar outras operações com as surebets
        surebet_calculate = CalculoCustos()
        real_surebets = surebet_calculate.process_surebets(lista_possiveis_surebets)
        soma_totais = calculate_real_surebets(real_surebets)
        for real_surebet in real_surebets:
            # Estou neste momento, faço os calculos da função abaixo calculate_real_surebets
            # Após o calculo verificar se o calculo de locao esta correto e salvar os dados
            # enviar para o telegram.
            # locacao = (26.38/40.89)*(1-(0.17/1.66))*(1-(0.07/1.36))*100
            locacao = (real_surebet['retorno_esperado']/soma_totais['total_retorno'])*(1-(soma_totais['total_c']/soma_totais['custo_transacao']))*(1-real_surebet['volatilidade']/soma_totais['total_volatilidade'])*100
            print(locacao)
def calculate_real_surebets(surebet_calculate):
    custo_transacao = (49.9/30)/10
    total_retorno = 0
    total_volatilidade = 0
    total_c = 10 * custo_transacao
    for surebet_real in surebet_calculate:
        total_retorno += surebet_real['retorno_esperado']
        total_volatilidade += surebet_real['volatilidade']
    resultado = {
        'total_retorno': total_retorno,
        'total_volatilidade': total_volatilidade,
        'total_c': total_c,
        'custo_transacao':custo_transacao
    }
    return resultado
        


# Exemplo de utilização:
if __name__ == "__main__":
    run()
