from typing import List

import matplotlib.pyplot as plt
import map
import vehicle
import random
from operator import attrgetter
from enum import Enum


class SlicingType(Enum):
    VISITED_EPSILON = 0
    START_TO_RANDOM = 1


class Genetics:

    def __init__(self, nodes: int = 0, edges: int = 0, mapa: map.Map = None, vehicles_no: int = 100,cycles_number = 100, slicing_type = SlicingType.VISITED_EPSILON):
        self.cycles_number = cycles_number
        self.avgerage_ages = []
        self.done_cycles = 0
        self.charger_nums_of_best = []
        self.kilometrages_of_best = []
        self.visited_nodes_num_of_best = []
        self.nodes_to_chargers_ratios_of_best = []
        self.slicing_type = slicing_type

        if mapa is None:
            self.mapa = map.Map(nodes, edges, as_complete=False, tries=10000)
        else:
            self.mapa = mapa

        self.vehicles = []

        for i in range(vehicles_no):
            self.vehicles.append(vehicle.Vehicle(self.mapa))

        while self.get_vehicles_number() % 4:
            self.vehicles.append(vehicle.Vehicle(self.mapa))

        self.compute_solution(show_best=True,show_progress=True,plot_all=False)

    def compute_solution(self, show_best = True,show_progress = False, plot_all = False):
        print("----START----")
        for i in range(self.cycles_number):
            self.cycle()

            if show_progress and i % int(self.cycles_number/3) == 0:
                print("Cycle: ", i+1, " out of: ", self.cycles_number)

        # self.charger_nums_of_best .append(len(self.vehicles[0].chargers))

        if show_best:
            self.vehicles[0].print_status()

        if plot_all:
            self.plot_avg_age()
            self.plot_charger_nums_of_best()
            self.plot_kilometrages_of_best()
            self.plot_visited_nodes_num_of_best()
            self.plot_nodes_to_chargers_ratios_of_best()

        print("----DONE----\n\n")
    def cycle(self):
        #FIXME
        self.QUICKFIX_visited_and_chargers_doubles()
        self.return_to_start()

        for v in self.vehicles:
            v.charge()
            v.age = v.age + 1
            # print("ID: ",v.ID,"  AGE: ", v.age)
            while True:

                result = self.move_to_random_neighbour(v)
                if result:
                    break



        self.rank()

        # self.charger_nums_of_best.append(len(self.vehicles[0].chargers))
        # self.kilometrages_of_best.append(self.vehicles[0].kilometrage)
        # self.visited_nodes_num_of_best.append(self.vehicles[0].visited_nodes_num)
        # self.nodes_to_chargers_ratios_of_best.append(self.vehicles[0].nodes_to_chargers_ratio)
        #
        # self.avgerage_ages.append(self.get_avg_age())

        self.hunger_games()
        self.crossing()

        #FIXME
        self.QUICKFIX_visited_and_chargers_doubles()

        self.rank()
        self.charger_nums_of_best.append(len(self.vehicles[0].chargers))
        self.kilometrages_of_best.append(self.vehicles[0].kilometrage)
        self.visited_nodes_num_of_best.append(self.vehicles[0].visited_nodes_num)
        self.nodes_to_chargers_ratios_of_best.append(self.vehicles[0].nodes_to_chargers_ratio)

        self.avgerage_ages.append(self.get_avg_age())

        self.done_cycles = self.done_cycles + 1
        # self.return_to_start() MOVED UP

        # print("VEHICLE NUM:", len(self.vehicles))
        # print("AVERAGE AGE:", self.get_avg_age())

    def return_to_start(self):

        def probability(age, max_age):
            if age >= max_age:
                return 1
            else:
                return 1.5**(age-max_age)

        for v in self.vehicles:
            # v.current_node = v.start_node
            # v.kilometrage = 0
            # v.visited_nodes = [v.current_node]
            # if v.age % random.randint(5,30) == 0:
            #     v.visited_nodes = random.sample(v.visited_nodes,int(len(v.visited_nodes)*0.5))
            #     v.chargers = random.sample(v.chargers, int(len(v.chargers) * 1))

            if random.uniform(0, 1) < probability(v.age,30):
                v.visited_nodes = random.sample(v.visited_nodes, int(len(v.visited_nodes) * 0.2))
            # pass
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
        for v in self.vehicles:
            v.visited_nodes_num = len(v.visited_nodes)
            # v.nodes_to_chargers_ratio = v.visited_nodes_num/len(v.chargers)
            v.nodes_to_chargers_ratio = len(v.chargers) / v.visited_nodes_num

        # self.vehicles.sort(key=attrgetter('kilometrage'), reverse=True)
        # self.vehicles.sort(key=attrgetter('visited_nodes_num'), reverse=True)
        self.vehicles.sort(key=attrgetter('nodes_to_chargers_ratio'), reverse=False)

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

        if self.slicing_type == SlicingType.VISITED_EPSILON:
            slice_epsilon = 2
            for i in range(self.mapa.size):
                if i in v.visited_nodes:
                    gene_nodes[i] = 1
                    if i >= slice_epsilon:
                        for j in range(1,slice_epsilon+1):
                            gene_nodes[i - j] = 1
                    if i < self.mapa.size - slice_epsilon:
                        for j in range(1, slice_epsilon + 1):
                            gene_nodes[i + j] = 1

        elif self.slicing_type == SlicingType.START_TO_RANDOM:
            slice_point = random.randint(0,len(gene_nodes))
            for i in range(0,slice_point):
                gene_nodes[i]= 1

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

    def plot_visited_nodes_num_of_best(self):
        cycles = [i for i in range(1, self.done_cycles + 1)]
        plt.plot(cycles, self.visited_nodes_num_of_best)
        plt.title("Top vis nodes num")
        plt.show()

    def plot_nodes_to_chargers_ratios_of_best(self):
        cycles = [i for i in range(1, self.done_cycles + 1)]
        plt.plot(cycles, self.nodes_to_chargers_ratios_of_best)
        plt.title("Top ratio")
        plt.show()

    def QUICKFIX_visited_and_chargers_doubles(self):
        for v in self.vehicles:
            v.chargers = list(set(v.chargers))
            v.visited_nodes = list(set(v.visited_nodes))
