from datetime import datetime, timedelta
class CalculoCustos:
    def __init__(self):
        pass
    def process_surebets(self, lista_possiveis_surebets):
        possible_surebets_list = lista_possiveis_surebets
        list_surebet = []
        hoje = datetime.now().date()
        amanha = hoje + timedelta(days=1)
        for surebet_key in possible_surebets_list:
            try:
                data_surebet = datetime.strptime(surebet_key['data'], '%d/%m/%y').date()
            except:
                data_surebet = datetime.strptime(surebet_key['data'], '%d/%m/%Y').date()
            if data_surebet == hoje or data_surebet == amanha:
                if surebet_key['aposta_11_22'] < 1:
                    surebet = {
                        'data' : surebet_key['data'],
                        'casa_a': surebet_key['casa_a'],
                        'casa_b': surebet_key['casa_b'],
                        'time_a': surebet_key['time_a'],
                        'time_b': surebet_key['time_b'],
                        'odds_a_time_a': surebet_key['odds_a_time_a'],
                        'odds_b_time_a': surebet_key['odds_b_time_a'],
                        'odds_a_time_b': surebet_key['odds_a_time_b'],
                        'odds_b_time_b': surebet_key['odds_b_time_b'],
                        'surebet_total': surebet_key['aposta_11_22'],
                        'retorno_esperado': surebet_key['retorno_esperado_aposta_11_22'],
                        'media_odds': surebet_key['media_odds'],
                        'volatilidade': surebet_key['volatilidade'],
                        'surebet':surebet_key['casa_a']+ '-' + surebet_key['time_a']+'|'+surebet_key['casa_b']+'-'+surebet_key['time_b']
                    }
                    list_surebet.append(surebet)
                if surebet_key['aposta_21_12'] < 1:
                    surebet = {
                        'data' : surebet_key['data'],
                        'casa_a': surebet_key['casa_a'],
                        'casa_b': surebet_key['casa_b'],
                        'time_a': surebet_key['time_a'],
                        'time_b': surebet_key['time_b'],
                        'odds_a_time_a': surebet_key['odds_a_time_a'],
                        'odds_b_time_a': surebet_key['odds_b_time_a'],
                        'odds_a_time_b': surebet_key['odds_a_time_b'],
                        'odds_b_time_b': surebet_key['odds_b_time_b'],
                        'surebet_total': surebet_key['aposta_21_12'],
                        'retorno_esperado': surebet_key['retorno_esperado_aposta_21_12'],
                        'media_odds': surebet_key['media_odds'],
                        'volatilidade': surebet_key['volatilidade'],
                        'surebet':surebet_key['casa_a']+ '-' + surebet_key['time_b']+'|'+surebet_key['casa_b']+'-'+surebet_key['time_a']
                    }
                    list_surebet.append(surebet)
        return list_surebet
    
    
