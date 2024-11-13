import json
import numpy as np
import itertools

class Solver:
    def __init__(self, data_path) -> None:

        with open(data_path, 'r') as file:
            data = json.load(file)

        self.load = data['load']
        print(self.load)
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
        ranges = [self.power_range(plant) for plant in self.powerplants if not self.is_wind(plant)]
        best_solution = None
        min_cost = float('inf')
        # a=1
        # for range in ranges:
        #     a = a * len(range)
        # print(a)
        # i = 0
        # # Brute force
        # for power_combination in itertools.product(*ranges):
        #     print(i)
        #     i = i + 1
        #     total_power = sum(power_combination)
        #     total_cost = sum(3 * power_combination[i] for i in range(len(ranges)))
            
        #     # Check if this combination meets the target energy requirement
        #     if total_power == self.load:
        #         # Update if we found a cheaper solution
        #         if total_cost < min_cost:
        #             min_cost = total_cost
        #             best_solution = power_combination
        #             print(best_solution)
        
        # return best_solution, min_cost
    
    def is_wind(self, powerplant: dict):
        return powerplant["type"] == "windturbine"
    
    def power_range(self, powerplant):
        epsilon = 1
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
    solver.preprocess()
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