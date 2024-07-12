from mainScript import getData
import json


class Bet:

    def __init__(self) -> None:
        self.list_house = ['unibet', "bet365"]

    def run(self, ):
        for house in self.list_house:
            list_data_house = []
            print(">>>>>")
            print(house)
            data = getData(house)
            data = {
                "house": house,
                "data": data
            }
            with open("../scriptJson/teamsMatches-"+house+".json", "w") as arquivo_saida:
                json.dump(data, arquivo_saida)


# with open("./all.json", "w") as arquivo_saida:
#     json.dump(list_data_house, arquivo_saida)
