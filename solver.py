import json
import numpy as np
import itertools

class Solver:
    def __init__(self, data_path) -> None:

        with open(data_path, 'r') as file:
            data = json.load(file)

        self.load = data['load']
        self.fuels = data['fuels']
        self.powerplants = data['powerplants']
        self.response = [{"name": plant['name'], "p": float('inf')} for plant in self.powerplants]

        print(self.powerplants)

        return
    
    def preprocess(self):
        for i, plant in enumerate(self.powerplants):
            if self.is_wind(plant):
                max_p = plant['pmax']*self.fuels["wind(%)"]/100
                if max_p <= self.load:
                    self.load = self.load - max_p
                    self.response[i]['p'] = max_p
                    continue
                self.load = 0
                self.response[i]['p'] = self.load
        return self.response

    def solve(self):
        return
    
    def is_wind(self, powerplant: dict):
        return powerplant["type"] == "windturbine"
    
    def power_range(self, powerplant):
        min_p = powerplant['pmin']
        max_p = powerplant['pmax']
        return np.arange(min_p, max_p + 0.1, 0.1)
    
if __name__ == "__main__":
    response = []

    dir = 'example_payloads/payload3.json'
    solver = Solver(dir)
    print(solver.preprocess())
    solver.solve()

    # with open(dir + '/payload3.json', 'r') as file:
    #     data = json.load(file)

    # load = data['load']
    # fuels = data['fuels']
    # powerplants = data['powerplants']
    # thermalplants = powerplants.copy()
    # windparks = []

    # for i, plant in enumerate(powerplants):
    #     if is_wind(plant):
    #         thermalplants.remove(plant)
    #         windparks.append(plant)

    # response = [{"name": plant['name'], "p": float('inf')} for plant in powerplants]
    # print(response)

    # for i, plant in enumerate(powerplants):
    #     if is_wind(plant):
    #         max_p = plant['pmax']*fuels["wind(%)"]/100
    #         if max_p <= load:
    #             load = load - max_p
    #             response[i]['p'] = max_p
    #             continue
    #         load = 0
    #         response[i]['p'] = load
    # print(response)