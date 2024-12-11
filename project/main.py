from house import House
from scraping import sportRadar
from calculo import getSurebets
from scraping import scrapingMatchesOdds
from datetime import datetime, timedelta
from telegramApi import enviar_mensagem_telegram
import math
import time
import json


def calculate_surebet(odds_a, odds_b, draw_odds):
    return (1 / odds_a) + (1 / odds_b) + (1 / draw_odds)


def identify_surebets(matches):
    surebets = []
    combinations = []
    count = []
    today = datetime.now().date()
    end_date = today + timedelta(days=4)

    # Filtrar partidas para o intervalo de datas desejado
    filtered_matches = [match for match in matches if today <= datetime.strptime(
        match.match_date, '%d-%m-%Y').date() <= end_date]

    grouped_matches = {}
    for match in filtered_matches:
        # print(match.match_date,'-',match.time_a,'-',match.time_b,'-',match.house)
        key = (match.match_date, match.time_a, match.time_b)
        if key not in grouped_matches:
            grouped_matches[key] = []
        grouped_matches[key].append(match)
    # Identificar surebets

    for key, match_list in grouped_matches.items():
        n = len(match_list)
        for i in range(n):
            for j in range(n):
                if j == i:
                    continue
                for k in range(n):
                    if k == i or k == j:
                        continue
                    count = count + 1
                    # Combinações distintas
                    odds_a = match_list[i].odds_a
                    odds_b = match_list[j].odds_b
                    draw_odds = match_list[k].draw_odds
                    surebet_value = calculate_surebet(
                        odds_a, odds_b, draw_odds)
                    combinations.append({
                        'combination': f"{match_list[i].house} ({match_list[i].time_a}) - {match_list[j].house} ({match_list[j].time_b}) - {match_list[k].house} (Draw)",
                        'implied_probability': surebet_value,
                        'odds': (odds_a, odds_b, draw_odds),
                        'date': key[0],
                        'teams': (key[1], key[2])
                    })
                    if surebet_value < 1:
                        average_odds = (match_list[i].odds_a + match_list[i].odds_b + match_list[i].draw_odds +
                                        match_list[j].odds_a + match_list[j].odds_b + match_list[j].draw_odds +
                                        match_list[k].odds_a + match_list[k].odds_b + match_list[k].draw_odds) / 9

                        volatility = math.sqrt(((match_list[i].odds_a - average_odds) ** 2 +
                                                (match_list[i].odds_b - average_odds) ** 2 +
                                                (match_list[i].draw_odds - average_odds) ** 2 +
                                                (match_list[j].odds_a - average_odds) ** 2 +
                                                (match_list[j].odds_b - average_odds) ** 2 +
                                                (match_list[j].draw_odds - average_odds) ** 2 +
                                                (match_list[k].odds_a - average_odds) ** 2 +
                                                (match_list[k].odds_b - average_odds) ** 2 +
                                                (match_list[k].draw_odds - average_odds) ** 2) / 9)

                        surebets.append({
                            'combination': f"{match_list[i].house} ({match_list[i].time_a}) - {match_list[j].house} ({match_list[j].time_b}) - {match_list[k].house} (Draw)",
                            'implied_probability': surebet_value,
                            'odds': (odds_a, odds_b, draw_odds),
                            'date': key[0],
                            'teams': (key[1], key[2]),
                            'expected_return': (1 - surebet_value) * 100,
                            'average_odds': average_odds,
                            'volatility': volatility,
                            'house_odds': {
                                match_list[i].house: {
                                    'odd_a': match_list[i].odds_a,
                                    'odd_b': match_list[i].odds_b,
                                    'draw': match_list[i].draw_odds
                                },
                                match_list[j].house: {
                                    'odd_a': match_list[j].odds_a,
                                    'odd_b': match_list[j].odds_b,
                                    'draw': match_list[j].draw_odds
                                },
                                match_list[k].house: {
                                    'odd_a': match_list[k].odds_a,
                                    'odd_b': match_list[k].odds_b,
                                    'draw': match_list[k].draw_odds
                                }
                            }
                        })
    # Calcula o retorno mínimo e máximo
    if surebets:
        retorno_minimo = min([surebet['expected_return']
                             for surebet in surebets])
        retorno_maximo = max([surebet['expected_return']
                             for surebet in surebets])
    else:
        retorno_minimo = 0
        retorno_maximo = 0
    # Criando a mensagem no formato desejado
    hora_atual = datetime.now().hour
    if 6 <= hora_atual < 12:
        periodo = "Manhã"
    elif 12 <= hora_atual < 18:
        periodo = "Tarde"
    else:
        periodo = "Noite"

    # Criar a mensagem com o período dinâmico
    message = (
        "📝 *Relatório Diário | Surebets Pre-match*\n\n"
        f"📊 *Total de Surebets Analisadas:* {len(count)}\n"
        f"📈 *Retorno Mínimo Identificado:* {retorno_minimo:.2f}%\n"
        f"📉 *Retorno Máximo Identificado:* {retorno_maximo:.2f}%\n"
        f"⏰ *Período:* {periodo}\n\n"
        "🔗 [Clique aqui para acessar sua lista personalizada.](http://app.referee.bet/)\n"
    )
    enviar_mensagem_telegram(message)
    # Converte para JSON com indentação
    surebets_json = json.dumps(surebets, indent=4)
    timestamp = str(int(time.time()))
    with open('./surebetsJson/'+timestamp+'-surebets.json', 'w') as json_file:
        json_file.write(surebets_json)
    return surebets


def main():
    call_sport_radar = sportRadar.run()
    call_odds_api = scrapingMatchesOdds.getOddsApi()

    houses = []
    for return_house in call_sport_radar:
        houses.append(return_house)
    for return_house in call_odds_api:
        houses.append(return_house)

    list_house_odds = []
    for house in houses:
        h = House()
        h.loadJson(pathJson=house)
        for i in h.match_list:
            list_house_odds.append(i)
    surebets = identify_surebets(list_house_odds)
    calculo = getSurebets(surebets)

    # Salvar o resultado em public/data.json
    with open('public/data.json', 'w') as json_file:
        json.dump(calculo, json_file, indent=4)

    return calculo


def tempo_ate_proximo_horario():
    agora = datetime.now()
    horarios = [6, 12, 18]

    for hora in horarios:
        proximo_horario = agora.replace(
            hour=hora, minute=0, second=0, microsecond=0)
        if proximo_horario > agora:
            return (proximo_horario - agora).total_seconds()

    proximo_horario = agora.replace(
        day=agora.day + 1, hour=6, minute=0, second=0, microsecond=0)
    return (proximo_horario - agora).total_seconds()


while True:

    get_surebets = main()
    tempo_de_espera = tempo_ate_proximo_horario()
    time.sleep(tempo_de_espera)
