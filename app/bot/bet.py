from mainScript import getData
import json
import os


class Bet:
    def __init__(self):
        self.list_house = ['unibet', 'bet365']
        self.output_dir = "../scriptJson"

    def run(self):
        os.makedirs(self.output_dir, exist_ok=True)

        for house in self.list_house:
            print(">>>>> Processing", house)
            try:
                data = getData(house)
                if data:
                    data_to_save = {
                        "house": house,
                        "data": data
                    }
                    file_path = os.path.join(
                        self.output_dir, f"teamsMatches-{house}.json")
                    with open(file_path, "w") as arquivo_saida:
                        json.dump(data_to_save, arquivo_saida)
                    print(f"Data saved to {file_path}")
                else:
                    print(f"No data returned for {house}")
            except Exception as e:
                print(f"Failed to retrieve or save data for {house}: {str(e)}")


# Exemplo de utilização:
if __name__ == "__main__":
    bet = Bet()
    bet.run()
