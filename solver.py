import json
import numpy as np
import itertools

RATE = 0.3

class Solver:
    def __init__(self, data_path) -> None:

        with open(data_path, 'r') as file:
            data = json.load(file)

        self.load = data['load']
        self.fuels = data['fuels']
        self.powerplants = data['powerplants']
        self.response = [{"name": plant['name'], "p": float('inf')} for plant in self.powerplants]

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
        rank = self.ranking()
        for index in rank:
            plant = self.powerplants[index]
            max_p = plant['pmax']
            min_p = plant['pmin']
            if self.is_wind(plant):
                max_p = max_p*self.fuels["wind(%)"]/100
                min_p = min_p*self.fuels["wind(%)"]/100
            if max_p <= self.load:
                self.load = self.load - max_p
                self.response[index]['p'] = max_p
                continue
            if self.load <= min_p:
                self.response[index]['p'] = 0.0
                continue
            self.response[index]['p'] = self.load
            self.load = 0.0
        return self.response
    
    def ranking(self):
        ranks = []
        for plant in self.powerplants:
            cost = 0.0
            if self.is_gas(plant):
                cost += self.gas_cost(1, plant)
            if self.is_kerosine(plant):
                cost += self.kerosine_cost(1, plant)
            ranks.append(cost)
        sorted_indexes = sorted(range(len(ranks)), key=lambda i: ranks[i])
        print(ranks)
        return sorted_indexes
    
    def gas_cost(self, power, plant):
        return (self.fuels["gas(euro/MWh)"]*power + self.fuels["co2(euro/ton)"]*RATE*power)/plant['efficiency']

    def kerosine_cost(self, power, plant):
        return self.fuels["kerosine(euro/MWh)"]*power/plant['efficiency']

    # def solve(self):
    #     ranges = {index: self.power_range(plant) for index, plant in enumerate(self.powerplants) if not self.is_wind(plant)}
    #     best_solution = None
    #     min_cost = float('inf')
    #     # Brute force
    #     for power_combination in itertools.product(*ranges.values()):
    #         total_power = sum(power_combination)
    #         if total_power == self.load:
    #             print("yes: ", power_combination)
    #             total_cost = 0.0
    #             for power, index in zip(power_combination, ranges.keys()):
    #                 plant = self.powerplants[index]
    #                 if plant['type'] == "gasfired":
    #                     total_cost += (self.fuels["gas(euro/MWh)"]*power + self.fuels["co2(euro/ton)"]*RATE*power)/plant['efficiency']
    #                 if plant['type'] == "turbojet":
    #                     total_cost += self.fuels["kerosine(euro/MWh)"]*power/plant['efficiency']
    #             if total_cost < min_cost:
    #                 min_cost = total_cost
    #                 best_solution = power_combination
    #                 print(best_solution)
        
    #     return best_solution, min_cost
    
    def is_gas(self, powerplant: dict):
        return powerplant["type"] == "gasfired"

    def is_kerosine(self, powerplant: dict):
        return powerplant["type"] == "turbojet"

    def is_wind(self, powerplant: dict):
        return powerplant["type"] == "windturbine"
    
    def power_range(self, powerplant):
        epsilon = 0.1
        min_p = powerplant['pmin']
        max_p = powerplant['pmax']
        if self.load <= max_p:
            max_p = self.load
        if min_p == 0:
            return np.arange(min_p, max_p + 0.1, epsilon)
        return np.insert(np.arange(min_p, max_p + 0.1, epsilon), 0, 0.0)
    
if __name__ == "__main__":
    response = []

    dir = 'example_payloads/payload3.json'
    solver = Solver(dir)
    response = solver.solve()

    with open('result.json', 'w') as fp:
        json.dump(response, fp)

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