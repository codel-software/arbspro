class CalculoCustos:
    def __init__(self):
        pass
    def process_surebets(self, lista_possiveis_surebets):
        possible_surebets_list = lista_possiveis_surebets
        list_surebet = []
        for surebet_key in possible_surebets_list:
            print(surebet_key)
            if surebet_key['aposta_11_22'] < 1:
                surebet = {
                    'casa_a': surebet_key['casa_a'],
                    'casa_b': surebet_key['casa_b'],
                    'time_a': surebet_key['time_a'],
                    'time_b': surebet_key['time_b'],
                    'odds_a_time_a': surebet_key['odds_a_time_a'],
                    'odds_b_time_a': surebet_key['odds_b_time_a'],
                    'odds_a_time_b': surebet_key['odds_a_time_b'],
                    'odds_b_time_b': surebet_key['odds_b_time_b'],
                    'retorno_esperado': surebet_key['retorno_esperado_aposta_11_22'],
                    'media_odds': surebet_key['media_odds'],
                    'volatilidade': surebet_key['volatilidade'],
                }
                list_surebet.append(surebet)
            if surebet_key['aposta_21_12'] < 1:
                surebet = {
                    'casa_a': surebet_key['casa_a'],
                    'casa_b': surebet_key['casa_b'],
                    'time_a': surebet_key['time_a'],
                    'time_b': surebet_key['time_b'],
                    'odds_a_time_a': surebet_key['odds_a_time_a'],
                    'odds_b_time_a': surebet_key['odds_b_time_a'],
                    'odds_a_time_b': surebet_key['odds_a_time_b'],
                    'odds_b_time_b': surebet_key['odds_b_time_b'],
                    'retorno_esperado': surebet_key['retorno_esperado_aposta_21_12'],
                    'media_odds': surebet_key['media_odds'],
                    'volatilidade': surebet_key['volatilidade'],
                }
                list_surebet.append(surebet)
        return list_surebet
    
    
