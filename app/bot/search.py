import json
from datetime import datetime, timedelta


def search_match_id(id, home):
    for odd in home['data']:
        if odd['match_id'] == id:
            return odd
    return None


def calcular_probabilidade_implicita(odds):
    return 1 / float(odds)


def verificar_surebet(odds1, odds2):
    prob1 = calcular_probabilidade_implicita(odds1)
    prob2 = calcular_probabilidade_implicita(odds2)
    return (prob1 + prob2) < 1


def odds_validas(*odds):
    try:
        for odd in odds:
            if odd == 'n/a':
                return False
            float(odd)
        return True
    except ValueError:
        return False


def search():
    # Abre o arquivo JSON e carrega os dados
    with open("all.json", 'r') as arquivo:
        liest_home = json.load(arquivo)

    a_odd_name = liest_home[0]['house']
    b_odd_name = liest_home[1]['house']

    surebets = []

    for a in liest_home[0]['data']:
        b = search_match_id(a['match_id'], liest_home[1])
        if b:
            # Verificar se as odds são válidas antes de calcular
            if odds_validas(a['home_odds'], a['away_odds'], a['draw_odds'], b['home_odds'], b['away_odds'], b['draw_odds']):
                # Calcular probabilidades implícitas para todos os resultados possíveis
                home_odds_a = float(a['home_odds'])
                away_odds_a = float(a['away_odds'])
                draw_odds_a = float(a['draw_odds'])

                home_odds_b = float(b['home_odds'])
                away_odds_b = float(b['away_odds'])
                draw_odds_b = float(b['draw_odds'])

                # Verificar oportunidades de Surebet
                surebet_home = verificar_surebet(home_odds_a, away_odds_b)
                surebet_away = verificar_surebet(away_odds_a, home_odds_b)
                surebet_draw = verificar_surebet(draw_odds_a, draw_odds_b)

                if surebet_home:
                    # Calcular o lucro com um investimento de 10 reais
                    investimento_total = 10
                    prob_home = 1 / home_odds_a
                    prob_away = 1 / away_odds_b
                    lucro = investimento_total * \
                        (prob_home - 1) / (prob_home + prob_away)
                    surebets.append({
                        'date': a['date'],
                        'match': f"{a['home']} vs {a['away']}",
                        'tipo': 'Casa',
                        'odds_a': home_odds_a,
                        'odds_b': away_odds_b,
                        'lucro': lucro
                    })

                if surebet_away:
                    # Calcular o lucro com um investimento de 10 reais
                    investimento_total = 10
                    prob_away = 1 / away_odds_a
                    prob_home = 1 / home_odds_b
                    lucro = investimento_total * \
                        (prob_away - 1) / (prob_away + prob_home)
                    surebets.append({
                        'date': a['date'],
                        'match': f"{a['home']} vs {a['away']}",
                        'tipo': 'Fora',
                        'odds_a': away_odds_a,
                        'odds_b': home_odds_b,
                        'lucro': lucro
                    })

                if surebet_draw:
                    # Calcular o lucro com um investimento de 10 reais
                    investimento_total = 10
                    prob_draw_a = 1 / draw_odds_a
                    prob_draw_b = 1 / draw_odds_b
                    lucro = investimento_total * \
                        (prob_draw_a - 1) / (prob_draw_a + prob_draw_b)
                    surebets.append({
                        'date': a['date'],
                        'match': f"{a['home']} vs {a['away']}",
                        'tipo': 'Empate',
                        'odds_a': draw_odds_a,
                        'odds_b': draw_odds_b,
                        'lucro': lucro
                    })
    hoje = datetime.now().date()
    amanha = hoje + timedelta(days=1)
    ontem = hoje + timedelta(days=-1)

    # Imprimir as oportunidades de Surebet com exemplo de investimento de 10 reais
    if surebets:
        for sb in surebets:
            data_surebet = datetime.strptime(sb['date'], '%d/%m/%y').date()
            if data_surebet == hoje or data_surebet == amanha:
                # print("Oportunidade de Surebet encontrada:")
                # print(f"Data: {sb['date']}")
                # print(f"Partida: {sb['match']}")
                # print(f"Tipo de Surebet: {sb['tipo']}")
                # print(f"Odds {a_odd_name}: {sb['odds_a']} | Odds {b_odd_name}: {sb['odds_b']}")
                # print(f"Lucro com investimento de R$ 10,00: R$ {sb['lucro']:.2f}")
                # print()
                message = (
                    "**Oportunidade de Surebet encontrada:**\n"
                    f"**Data:** {sb['date']}\n"
                    f"**Partida:** {sb['match']}\n"
                    f"**Tipo de Surebet:** {sb['tipo']}\n"
                    f"**Odds {a_odd_name}:** {sb['odds_a']} | **Odds {b_odd_name}:** {sb['odds_b']}\n"
                    f"**Lucro com investimento de R$ 10,00:** R$ {sb['lucro']:.2f}\n"
                )
                # Chame a função da sua API do Telegram para enviar a mensagem
                from telegramApi import enviar_mensagem_telegram
                enviar_mensagem_telegram(message)
