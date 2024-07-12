from operator import truediv
from re import split
from pprint import pprint
from match import Match
from data_house.odds_api import odds_api
from data_house.sport_radar import sport_radar
from house import House


def process_odd(odd_1, odd_2, house):
    surebets = []
    for match_odd_1 in odd_1.match_list:
        for match_odd_2 in odd_2.match_list:
            if match_odd_1.time_a == match_odd_2.time_a:
                if match_odd_1.time_b == match_odd_2.time_b:
                    if match_odd_1.match_date == match_odd_2.match_date:
                        aposta_11_22 = (1/match_odd_1.odds_a) + \
                            (1/match_odd_2.odds_b)
                        aposta_21_12 = (1/match_odd_2.odds_a) + \
                            (1/match_odd_1.odds_b)
                        surebet = False
                        if aposta_11_22 < 1:
                            surebet = True
                        if aposta_21_12 < 1:
                            surebet = True
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
                        surebets.append(check_surebet)
    print(surebets)


def run():
    data_base = [odds_api]

    for data in data_base:
        list_odds_process = []

        model = data.model
        list_house_odds = []
        houses = data.getHouse()
        for house in houses:
            h = House()
            h.loadJson(pathJson=house, model=model)
            list_house_odds.append(h)
        # percorrer as casas e descobrir as surebets e salvar em outra lista

        list_surbets = []
        for odd_1 in list_house_odds:
            if len(list_odds_process) == 0:
                list_odds_process.append(odd_1)
                continue
            for odd_2 in list_odds_process:
                process_odd(odd_1=odd_1, odd_2=odd_2, house=house)
            list_odds_process.append(odd_1)
