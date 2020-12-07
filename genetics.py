from typing import List

import matplotlib.pyplot as plt
import map
import vehicle
import random
from operator import attrgetter


class Genetics:

    def __init__(self, nodes: int = 0, edges: int = 0, mapa: map.Map = None, vehicles_no: int = 99):

        self.avgerage_ages = []
        self.done_cycles = 0
        self.charger_nums_of_best = []
        self.kilometrages_of_best = []
        if mapa is None:
            self.mapa = map.Map(nodes, edges, as_complete=False, tries=10000)
        else:
            self.mapa = mapa

        self.vehicles = []

        for i in range(vehicles_no):
            self.vehicles.append(vehicle.Vehicle(self.mapa))

        while self.get_vehicles_number() % 4:
            self.vehicles.append(vehicle.Vehicle(self.mapa))

    def cycle(self):
        self.QUICKFIX_visited_and_chargers_doubles()

        for v in self.vehicles:
            v.charge()
            v.age = v.age + 1
            # print("ID: ",v.ID,"  AGE: ", v.age)
            while True:

                result = self.move_to_random_neighbour(v)
                if result:
                    break

        self.rank()
        self.hunger_games()
        self.crossing()

        self.rank()
        self.charger_nums_of_best.append(len(self.vehicles[0].chargers))
        self.kilometrages_of_best.append(self.vehicles[0].kilometrage)
        self.avgerage_ages.append(self.get_avg_age())
        self.done_cycles = self.done_cycles + 1
        self.return_to_start()

        # print("VEHICLE NUM:", len(self.vehicles))
        # print("AVERAGE AGE:", self.get_avg_age())

    def return_to_start(self):
        for v in self.vehicles:
            # v.current_node = v.start_node
            v.kilometrage = 0
            v.visited_nodes = [v.current_node]
        pass

    def get_vehicles_number(self):
        return len(self.vehicles)

    def move_to_random_neighbour(self, v: vehicle.Vehicle) -> bool:

        neighbours = v.map.neighbours(v.current_node)

        to_be_removed = []
        for n in neighbours:
            if n in v.visited_nodes:
                to_be_removed.append(n)

        for n in to_be_removed:
            neighbours.remove(n)

        if not neighbours:
            return True

        to_be_removed = []
        for n in neighbours:
            if not v.can_move_to(n):
                to_be_removed.append(n)

        for n in to_be_removed:
            neighbours.remove(n)

        if neighbours:
            destination = neighbours[random.randint(0, len(neighbours) - 1)]
            if destination in v.chargers:
                v.charge()
            v.move(destination)
            v.visited_nodes.append(destination)

            return False
        else:
            v.chargers.append(v.current_node)
            return True

    def rank(self):
        self.vehicles.sort(key=attrgetter('kilometrage'), reverse=True)

    def hunger_games(self):
        del self.vehicles[int(self.get_vehicles_number() / 2) - 1:-1]
        pass

    def crossing(self):

        for i in range(0, int(self.get_vehicles_number() / 2)):
            v1 = self.vehicles[i * 2]
            v2 = self.vehicles[i * 2 + 1]

            v3 = vehicle.Vehicle(self.mapa)
            v4 = vehicle.Vehicle(self.mapa)

            self.offspring(v1, v2, v3)
            self.offspring(v2, v1, v4)

            self.vehicles.append(v3)
            self.vehicles.append(v4)

    def offspring(self, v1, v2, v_out):

        v1_bin_chargers = self.chargers_to_binary_gene(v1)
        gene = self.chargers_to_binary_gene(v2)
        v1_gene_bin_slice = self.get_gene_binary_slice(v1)

        for i in range(len(v1_bin_chargers)):
            if v1_gene_bin_slice[i] == 1:
                # print("Node ",i,"from G1 of value: ",v1_bin_chargers[i], " to G2 of value",gene[i])
                gene[i] = v1_bin_chargers[i]

        v_out.chargers = self.binary_gene_to_chargers(gene)
        # print("V1 vis: ", v1.visited_nodes)
        # print("V1 chrg: ", v1.chargers)
        # print("V2 vis: ", v2.visited_nodes)
        # print("V2 chrg: ", v2.chargers)
        # print("G1 -------: ", v1_bin_chargers)
        # print("G1 slicing: ", v1_gene_bin_slice)
        # print("G2 -------: ", self.chargers_to_binary_gene(v2))
        # print("Out ------: ", gene)
        # print("Out : ", self.binary_gene_to_chargers(gene))
        # print("----------------")

    def chargers_to_binary_gene(self, v: vehicle.Vehicle):
        gene = [0] * self.mapa.size
        for i in range(self.mapa.size):
            if i in v.chargers:
                gene[i] = 1
        return gene

    def binary_gene_to_chargers(self, gene: List):
        chargers = []
        for i in range(len(gene)):
            if gene[i] == 1:
                chargers.append(i)
        return chargers

    def get_gene_binary_slice(self, v: vehicle.Vehicle):
        gene_nodes = [0] * self.mapa.size

        for i in range(self.mapa.size):
            if i in v.visited_nodes:
                gene_nodes[i] = 1
                if i > 0:
                    gene_nodes[i - 1] = 1

                if i < self.mapa.size - 1:
                    gene_nodes[i + 1] = 1

        return gene_nodes

    def mutate(self):
        pass

    def get_avg_age(self):
        age_sum = 0
        for v in self.vehicles:
            age_sum = age_sum + v.age

        avg_age = age_sum / self.get_vehicles_number()
        return avg_age

    def plot_avg_age(self):
        cycles = [i for i in range(1, self.done_cycles + 1)]
        plt.plot(cycles, self.avgerage_ages)
        plt.title("Average age")
        plt.show()

    def plot_charger_nums_of_best(self):
        cycles = [i for i in range(1, self.done_cycles + 1)]
        plt.plot(cycles, self.charger_nums_of_best)
        plt.title("Number of chargers")
        plt.show()

    def plot_kilometrages_of_best(self):
        cycles = [i for i in range(1, self.done_cycles + 1)]
        plt.plot(cycles, self.kilometrages_of_best)
        plt.title("Top kilometrage")
        plt.show()

    def QUICKFIX_visited_and_chargers_doubles(self):
        for v in self.vehicles:
            v.chargers = list(set(v.chargers))
            v.visited_nodes = list(set(v.visited_nodes))
