from operator import truediv
from match import Match
from data_house.odds_api import odds_api
from data_house.sport_radar import sport_radar
from house import House


def process_odd(odd_1, odd_2):
    surebets = set()  # Usando um conjunto para garantir que cada surebet seja único

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
                    "surebet": surebet
                }

                # Convertendo para tuple para usar como chave única
                surebets.add(tuple(check_surebet.items()))

    return surebets


def run():
    # Aqui você pode adicionar mais fontes de dados, se necessário
    data_base = [odds_api]

    for data in data_base:
        list_house_odds = []
        houses = data.getHouse()

        for house in houses:
            h = House()
            h.loadJson(pathJson=house, model=data.model)
            list_house_odds.append(h)

        list_surebets = []
        for i, odd_1 in enumerate(list_house_odds):
            # Evita comparar um objeto com ele mesmo e comparações duplicadas
            for odd_2 in list_house_odds[i+1:]:
                surebets = process_odd(odd_1, odd_2)
                list_surebets.extend(surebets)

        # Imprimir os resultados ou realizar outras operações com as surebets
        for surebet in list_surebets:
            # Convertendo de volta para dicionário para impressão ou manipulação posterior
            print(dict(surebet))


# Exemplo de utilização:
if __name__ == "__main__":
    run()
