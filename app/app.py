from mainScript import getData
import json


list_house = ['unibet', "bet365"]
list_data_house = []


for house in list_house:
    print(">>>>>")
    print(house)
    print(type(house))
    data = getData(house)
    data = {
        "house": house,
        "data": data
    }
    list_data_house.append(data)


with open("./all.json", "w") as arquivo_saida:
    json.dump(list_data_house, arquivo_saida)
