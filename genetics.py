from typing import List
from termcolor import colored
import matplotlib.pyplot as plt
import map
import vehicle
import random
from operator import attrgetter
from enum import Enum
import copy
import time

class SlicingType(Enum):
    MULTI_POINT_VISITED_EPSILON = 0
    ONE_POINT_RAND = 1


class Genetics:

    def __init__(self, nodes: int = 0, edges: int = 0, mapa: map.Map = None, vehicles_no: int = 100, cycles_number=100,

                 slicing_type=SlicingType.MULTI_POINT_VISITED_EPSILON):

        self.avgerage_ages = []
        self.done_cycles = 0
        self.charger_nums_of_best = []
        self.kilometrages_of_best = []
        self.visited_nodes_num_of_best = []
        self.nodes_to_chargers_ratios_of_best = []

        self.cycles_number = cycles_number
        self.slicing_type = slicing_type

        self.best_vehicle = None

        self.slice_epsilon = 2

        if mapa is None:
            self.mapa = map.Map(nodes, edges, as_complete=False, tries=10000)
        else:
            self.mapa = copy.deepcopy(mapa)

        self.map_solution = self.mapa
        self.map_binary = None
        self.vehicles = []


        for i in range(vehicles_no):
            self.vehicles.append(vehicle.Vehicle(self.mapa))

        while self.get_vehicles_number() % 4:
            self.vehicles.append(vehicle.Vehicle(self.mapa))

    def solve(self):
        start = time.time()
        for i in range(self.cycles_number):
            self.cycle()

            progress = int((i + 1) / self.cycles_number * 100)
            print("\rProgress: " + colored(str(progress) + "% ",'blue') + "[" + colored("#" * progress, 'green') + colored("." * (100 - progress),'red') + "] "
                  + colored(format(time.time()-start,'.1f'), 'blue') + " seconds elapsed", end="")
            if i == self.cycles_number - 1:
                print("")

        self.rank()
        self.best_vehicle = self.vehicles[0]
        self.map_solution = self.mapa
        for c in self.best_vehicle.chargers:
            self.map_solution.set_as_charger(c)

        self.map_conversion()

        # self.best_vehicle.print_status()
        #
        # self.plot_avg_age()
        # self.plot_charger_nums_of_best()
        # self.plot_kilometrages_of_best()
        # self.plot_visited_nodes_num_of_best()
        # self.plot_nodes_to_chargers_ratios_of_best()
        #
        # self.show_map_solution()

    def cycle(self):
        # FIXME
        self.QUICKFIX_visited_and_chargers_doubles()
        self.alzheimer()

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

        # FIXME
        self.QUICKFIX_visited_and_chargers_doubles()

        self.rank()

        self.best_vehicle = self.vehicles[0]

        self.charger_nums_of_best.append(len(self.best_vehicle.chargers))
        self.kilometrages_of_best.append(self.best_vehicle.kilometrage)
        self.visited_nodes_num_of_best.append(self.best_vehicle.visited_nodes_num)
        self.nodes_to_chargers_ratios_of_best.append(self.best_vehicle.nodes_to_chargers_ratio)

        self.avgerage_ages.append(self.get_avg_age())

        self.done_cycles = self.done_cycles + 1

        # print("VEHICLE NUM:", len(self.vehicles))
        # print("AVERAGE AGE:", self.get_avg_age())

    def alzheimer(self):
        def probability(age, max_age):
            if age >= max_age:
                return 1
            else:
                return 1.5 ** (age - max_age)

        for v in self.vehicles:
            if random.uniform(0, 1) < probability(v.age, 30):
                all_nodes = [i for i in range(self.mapa.size)]
                nodes_to_remember = random.sample(all_nodes, int(len(all_nodes) * 0.8))

                for i in nodes_to_remember:
                    v.visited_nodes = list(filter(lambda n: n != i, v.visited_nodes))
                    # v.chargers = list(filter(lambda n: n != i, v.chargers))
                # v.visited_nodes = random.sample(v.visited_nodes, int(len(v.visited_nodes) * 0.1))
                # v.chargers = random.sample(v.chargers, int(len(v.chargers) * 0.5))

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
            if v.visited_nodes_num==0:
                v.nodes_to_chargers_ratio=1
            else:
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

        if self.slicing_type == SlicingType.MULTI_POINT_VISITED_EPSILON:

            for i in range(self.mapa.size):
                if i in v.visited_nodes:
                    gene_nodes[i] = 1
                    if i >= self.slice_epsilon:
                        for j in range(1, self.slice_epsilon + 1):
                            gene_nodes[i - j] = 1
                    if i < self.mapa.size - self.slice_epsilon:
                        for j in range(1, self.slice_epsilon + 1):
                            gene_nodes[i + j] = 1

        elif self.slicing_type == SlicingType.ONE_POINT_RAND:
            slice_point = random.randint(0, len(gene_nodes))
            for i in range(0, slice_point):
                gene_nodes[i] = 1

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
        plt.title("Średnia wieku populacji")
        plt.xlabel("Cykl")
        plt.ylabel("Wiek (cykle)")
        plt.show()

    def plot_charger_nums_of_best(self):
        cycles = [i for i in range(1, self.done_cycles + 1)]
        plt.plot(cycles, self.charger_nums_of_best)
        plt.title("Ilość ładowarek w genomie najlepszego osobnika")
        plt.xlabel("Cykl")
        plt.ylabel("Ilość ładowarek")
        plt.show()

    def plot_kilometrages_of_best(self):
        cycles = [i for i in range(1, self.done_cycles + 1)]
        plt.plot(cycles, self.kilometrages_of_best)
        plt.title("Przebieg najlepszego osobnika")
        plt.xlabel("Cykl")
        plt.ylabel("Przebieg [km]")
        plt.show()

    def plot_visited_nodes_num_of_best(self):
        cycles = [i for i in range(1, self.done_cycles + 1)]
        plt.plot(cycles, self.visited_nodes_num_of_best)
        plt.title("Ilość odwiedzonych wierzchołków najlepszego osobnika")
        plt.xlabel("Cykl")
        plt.ylabel("Odwiedzone wierzchołki")
        plt.show()

    def plot_nodes_to_chargers_ratios_of_best(self):
        cycles = [i for i in range(1, self.done_cycles + 1)]
        plt.plot(cycles, self.nodes_to_chargers_ratios_of_best)
        plt.title("Stosunek ilości ładowarek do odwiedzonych wierzchołków najlepszego osobnika")
        plt.xlabel("Cykl")
        plt.ylabel("Ładowarki/odwiedzone wierzchołki")
        plt.show()

    def QUICKFIX_visited_and_chargers_doubles(self):
        for v in self.vehicles:
            v.chargers = list(set(v.chargers))
            v.visited_nodes = list(set(v.visited_nodes))

    def show_map_solution(self):
        self.map_solution.print()

    def print_best_vehicle(self):
        self.best_vehicle.print_status()

    def plot(self):
        self.plot_avg_age()
        self.plot_charger_nums_of_best()
        self.plot_kilometrages_of_best()
        self.plot_visited_nodes_num_of_best()
        self.plot_nodes_to_chargers_ratios_of_best()
        self.show_map_solution()

    def map_conversion(self):
        self.map_binary = list()
        binary = [list()] * self.map_solution.size
        for i in range(self.map_solution.size):
            binary[i] = [0] * self.map_solution.size

        for edge in self.map_solution.G.edges:
            binary[edge[0]][edge[1]] = 1
            binary[edge[1]][edge[0]] = 1

        for i in range(self.map_solution.size):
            list_to_append = []
            for j in range(self.map_solution.size):
                if binary[i][j]:
                    list_to_append.append(j)
            if list_to_append:
                self.map_binary.append(list_to_append)
            else:
                self.map_binary.append(None)

    def check_available_paths(self, current_node, stop_node, visited_nodes=[]):
        copyofvisited = visited_nodes.copy()
        copyofvisited.append(current_node)
        if current_node == stop_node:
            self.available_paths.append(copyofvisited)
        else:
            for neighbor in self.map_binary[current_node]:
                if neighbor not in copyofvisited:
                    self.check_available_paths(neighbor, stop_node, copyofvisited)

    def test_iterate(self):
        self.available_paths = []

        start_node, stop_node = random.sample(range(0, self.map_solution.size - 1), 2)
        print("Checking for available paths...")
        self.check_available_paths(start_node, stop_node)
        print("Paths found! Starting test...")
        for path in self.available_paths:
            veh_checker = vehicle.Vehicle(self.mapa)
            veh_checker.start_node = path[0]
            veh_checker.current_node = path[0]
            veh_checker.chargers=self.map_solution.chargers


            for i in range(1, len(path)):
                if veh_checker.current_node in veh_checker.chargers:
                    veh_checker.charge()
                if veh_checker.can_move_to(path[i]):
                    if path[i] == stop_node:
                        return True
                    veh_checker.move(path[i])

                else:
                    break

        return False

    def test(self,tests_number=3):
        print(colored("\n\n-------------BEGINNING TESTS-------------\n", 'green'))

        final_result = 0
        for i in range(tests_number):
            print(colored("-------------Test number", 'yellow'), colored(i + 1,'blue'), colored("--------------",'yellow'))
            result = self.test_iterate()
            if result:
                print("test number", i + 1, ":",colored("ACCEPTED",'green'))
                final_result+=1
            else:
                print("test number", i + 1, ":",colored("REJECTED",'red'))
        print("\n")
        print(colored("-----------------RESULTS-----------------", 'red'))
        print(colored(final_result, 'red'), colored("out of", 'red'), colored(tests_number, 'red'),
              colored("=", 'red'), colored(100 * final_result / tests_number, 'blue'), colored("%", 'blue'),
              colored("passed", 'red'))
        print(colored("-----------------------------------------", 'red'))

    def get_vis_to_size_ratio(self):
        return len(self.best_vehicle.visited_nodes) / self.mapa.size

    def get_chargers_to_size_ratio(self):
        return len(self.best_vehicle.chargers) / self.mapa.size