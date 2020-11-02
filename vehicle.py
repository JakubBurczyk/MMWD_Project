import map


class Vehicle:
    occupied_IDs = []
    battery_capacity = 1000
    battery_life_loss = 0
    km_per_unit_energy = 0.02
    starting_capacity = 1

    def __init__(self, m: map.Map):

        self.map = m
        self.battery_life = 1
        self.battery = self.battery_capacity*self.starting_capacity
        self.current_node = 1

        if self.occupied_IDs == []:
            self.ID = 0
        else:
            self.ID = max(self.occupied_IDs)+1

        self.occupied_IDs.append(self.ID)

    def __del__(self):
        self.occupied_IDs.remove(self.ID)

    def print_occupied_IDs(self):
        print(self.occupied_IDs)

    def print_ID(self):
        print(self.ID)

    def print_status(self):
        print("----VEHICLE----")
        print("ID: ", self.ID)
        print("Current node: ", self.current_node)
        print("Battery: ", self.battery," / ", self.battery_capacity)
        print("Range: ", self.calculate_range(), "[km]")
        print("Battery life: ", self.battery_life*100, "%")
        print("---------------")

    def calculate_range(self) -> float:
        return self.battery*self.km_per_unit_energy*self.battery_life

    def charge(self) -> None:
        self.battery = self.battery + self.map.charger_energy

        if self.battery > self.battery_capacity:
            self.battery = self.battery_capacity

        self.battery_life = self.battery_life - self.battery_life_loss

    def can_traverse_to(self,destination) -> bool:
        return self.calculate_range() >= self.map.get_distance_between(self.current_node, destination)
