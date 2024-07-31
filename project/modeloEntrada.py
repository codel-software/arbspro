from datetime import datetime

class ModeloEntrada:
    def __init__(self, casa, data, time_casa, odds_time_casa, time_visitante, odds_time_visitante, odds_empate):
        self.casa = casa
        self.data = self.formatar_data(data)
        self.time_casa = time_casa
        self.odds_time_casa = odds_time_casa
        self.time_visitante = time_visitante
        self.odds_time_visitante = odds_time_visitante
        self.odds_empate = odds_empate

    def formatar_data(self, data):
        formatos = ["%d-%m-%Y", "%d/%m/%Y", "%d-%m-%y", "%d/%m/%y"]  # Formatos esperados
        for formato in formatos:
            try:
                data_formatada = datetime.strptime(data, formato).strftime("%d-%m-%Y")
                return data_formatada
            except ValueError:
                continue
        raise ValueError(f"Data '{data}' não está em um formato reconhecido.")
