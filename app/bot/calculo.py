from operator import truediv
from calculoCustos import CalculoCustos
from match import Match
from data_house.odds_api import odds_api
from data_house.sport_radar import sport_radar
from house import House
from datetime import datetime, timedelta
from telegramApi import enviar_mensagem_telegram
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
                    "data": match_odd_1.match_date,
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
            parte_1 = (real_surebet['retorno_esperado']/soma_totais['total_retorno']) 
            parte_2 = (1-(soma_totais['custo_transacao']/soma_totais['total_c'])) 
            parte_3 = (1-(real_surebet['volatilidade']/soma_totais['total_volatilidade']))
            locacao = parte_1 * parte_2 * parte_3
            real_surebet['locacao'] = locacao
            locacao_time_1 = ((1/real_surebet['odds_a_time_b'])/real_surebet['surebet_total'])*locacao
            real_surebet['locacao_proporcional_1'] = locacao_time_1
            locacao_time_2 = ((1/real_surebet['odds_b_time_a'])/real_surebet['surebet_total'])*locacao
            real_surebet['locacao_proporcional_2'] = locacao_time_2
        if real_surebets:
            for sb in real_surebets:
                    message = (
                        "**Oportunidade de Surebet encontrada:**\n"
                        f"**Data:** {sb['data']}\n"
                        f"**Partida:** {sb['time_a']} x {sb['time_b']}\n"
                        f"**Tipo de Surebet:** {sb['surebet']}\n"
                        f"**Retorno Esperado - R (%):** {sb['retorno_esperado']}\n"
                        f"**Média das Odds:** {sb['media_odds']}\n"
                        f"**Volatilidade - V:** {sb['volatilidade']}\n"
                        f"**Alocação Surebets:** {sb['locacao']}\n"
                        f"**Alocação Proporcional - Time 1:** {sb['locacao_proporcional_1']}\n"
                        f"**Alocação Proporcional - Time 2:** {sb['locacao_proporcional_2']}\n"
                        # f"**Lucro com investimento de R$ 10,00:** R$ {sb['lucro']:.2f}\n"
                    )
                    print(message)
                    # Chame a função da sua API do Telegram para enviar a mensagem
                    # enviar_mensagem_telegram(message)
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



# 1º a função calculate_real_surebet() deve somar apenas com as surbets do dia que vai ser enviados no grupo, dia atual e o proximo ou so dia atual
# 2º Inclusão da comparação de empate
# casa 1 TIME 1 casa 2 TIME 2 OU EMPATE
# casa 1 TIME 2 casa 2 TIME 1 OU EMPATE
# casa 1 TIME 1 OU EMPATE casa 2 TIME 2 
# casa 1 TIME 2 u empate casa 2 time 1 