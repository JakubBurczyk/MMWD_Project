import map
import random


class Vehicle:
    occupied_IDs = []
    battery_capacity = 1000
    battery_life_loss = 0
    km_per_unit_energy = 0.02
    starting_capacity = 1

    def __init__(self, m: map.Map):
        self.map = m
        self.battery_life = 1
        self.battery = self.battery_capacity * self.starting_capacity
        self.start_node = random.randint(0, m.size - 1)
        self.current_node = self.start_node
        self.chargers = []
        self.visited_nodes = [self.current_node]
        self.kilometrage = 0

        if self.occupied_IDs == []:
            self.ID = 0
        else:
            self.ID = max(self.occupied_IDs) + 1

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
        print("Start: ", self.start_node)
        print("Current node: ", self.current_node)
        print("Battery: ", self.battery, " / ", self.battery_capacity)
        print("Range: ", self.calculate_range(), "[km]")
        print("Kilometrage: ", self.kilometrage, "[km]")
        print("Battery life: ", self.battery_life * 100, "%")
        print("---------------")
        print("Gene: ", self.chargers)
        print("---------------")

    def calculate_range(self) -> float:
        return self.battery * self.km_per_unit_energy * self.battery_life

    def charge(self) -> None:
        self.battery = self.battery + self.map.charger_energy

        if self.battery > self.battery_capacity:
            self.battery = self.battery_capacity

        self.battery_life = self.battery_life - self.battery_life_loss

    def reduce_current_range(self, distance):
        self.battery = self.battery - distance / self.km_per_unit_energy

    def can_move_to(self, destination) -> bool:
        return self.calculate_range() >= self.map.get_distance_between(self.current_node, destination)

    def move(self, destination) -> bool:
        can_move = self.can_move_to(destination)
        if can_move:
            distance = self.map.get_distance_between(self.current_node, destination)
            self.reduce_current_range(distance)
            self.current_node = destination
            self.kilometrage += distance
        return can_move
