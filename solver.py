import json

RATE = 0.3

class Solver:
    
    def __init__(self, data) -> None:
        self.load = data['load']
        self.fuels = data['fuels']
        self.powerplants = data['powerplants']
        self.response = [{"name": plant['name'], "p": float('inf')} for plant in self.powerplants]
        return

    def solve(self):
        """
        Solve the problem with an heuristic that dispatches power plants based on their ranking.

        Returns:
            dict: A dictionary containing the power output assigned to each plant, indexed by the plant's ID.
        """
        rank = self.ranking()

        # Iterate through the power plants in order of their rank.
        for index in rank:

            plant = self.powerplants[index]
            max_p = plant['pmax']
            min_p = plant['pmin']

            if self.is_wind(plant):
                max_p = max_p*self.fuels["wind(%)"]/100
                min_p = min_p*self.fuels["wind(%)"]/100

            # If the plant's maximum power is less than or equal to the remaining load, dispatch its full capacity.
            if max_p <= self.load:
                self.load = self.load - max_p
                self.response[index]['p'] = max_p
                continue

            # If the load is less than or equal to the plant's minimum power, do not dispatch any power from this plant.
            if self.load <= min_p:
                self.response[index]['p'] = 0.0
                continue

            # If the load is in between the plant's minimum and maximum capacity, dispatch only the remaining load.
            self.response[index]['p'] = self.load
            self.load = 0.0
            
        return self.response
    
    def ranking(self):
        """
        Calculate the ranking of power plants based on their fuel cost.

        This method calculates the fuel cost for each power plant in the `self.powerplants` list,
        based on whether the plant uses gas or kerosine.

        Returns:
            list[int]: A list of indices representing the power plants sorted by fuel cost 
            in ascending order.
        """
        ranks = []
        for plant in self.powerplants:

            cost = 0.0

            # Compute the cost for one unit of power generated
            if self.is_gas(plant):
                cost += self.gas_cost(1, plant)

            if self.is_kerosine(plant):
                cost += self.kerosine_cost(1, plant)

            ranks.append(cost)

        sorted_indexes = sorted(range(len(ranks)), key=lambda i: ranks[i])
        return sorted_indexes
    
    def gas_cost(self, power, plant):
        """
        Calculate the cost of the energy production for a gas power plant.

        Args:
            power (float): The amount of power to be generated, in MWh.
            plant (dict): A dictionary representing the power plant.

        Returns:
            float: The calculated gas fuel cost for the given power and plant, in euros.
        """
        return (self.fuels["gas(euro/MWh)"]*power + self.fuels["co2(euro/ton)"]*RATE*power)/plant['efficiency']

    def kerosine_cost(self, power, plant):
        """
        Calculate the cost of the energy production for a kerosine power plant.

        Args:
            power (float): The amount of power to be generated, in MWh.
            plant (dict): A dictionary representing the power plant.

        Returns:
            float: The calculated gas fuel cost for the given power and plant, in euros.
        """
        return self.fuels["kerosine(euro/MWh)"]*power/plant['efficiency']
    
    def is_gas(self, powerplant: dict):
        return powerplant["type"] == "gasfired"

    def is_kerosine(self, powerplant: dict):
        return powerplant["type"] == "turbojet"

    def is_wind(self, powerplant: dict):
        return powerplant["type"] == "windturbine"
    
if __name__ == "__main__":
    response = []

    dir = 'example_payloads/payload3.json'
    with open(dir, 'r') as file:
        data = json.load(file)
    solver = Solver(data)
    response = solver.solve()
    print(response)

    with open('result.json', 'w') as fp:
        json.dump(response, fp)