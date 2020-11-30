from typing import List

import map
import vehicle
import random
from operator import attrgetter


class Genetics:

    def __init__(self, nodes: int = 0, edges: int = 0, vehicles_no: int = 99):

        self.mapa = map.Map(nodes, edges, as_complete=False, tries=100)
        self.vehicles = []

        for i in range(vehicles_no):
            self.vehicles.append(vehicle.Vehicle(self.mapa))

        while self.get_vehicles_number() % 4:
            self.vehicles.append(vehicle.Vehicle(self.mapa))

    def cycle(self):

        for v in self.vehicles:
            v.charge()
            while True:

                result = self.move_to_random_neighbour(v)
                if result:
                    break

        self.rank()
        self.hunger_games()
        print("VEHICLE NUM:",len(self.vehicles))
        self.crossing()

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
        del self.vehicles[int(self.get_vehicles_number()/2)-1:-1]
        pass

    def crossing(self):

        for i in range(0, int(self.get_vehicles_number()/2)-1):
            v1 = self.vehicles[i*2]
            v2 = self.vehicles[i*2+1]

            v3 = vehicle.Vehicle(self.mapa)
            v4 = vehicle.Vehicle(self.mapa)

            self.offspring(v1,v2,v3)
            self.offspring(v2,v1,v4)

            self.vehicles.append(v3)
            self.vehicles.append(v4)
        pass

    def offspring(self,v1,v2,v_out):

        v1_bin_chargers = self.chargers_to_binary_gene(v1)
        gene = self.chargers_to_binary_gene(v2)
        v1_gene_bin_slice = self.get_gene_binary_slice(v1)

        for i in range(len(v_out.chargers)):
            if v1_gene_bin_slice == 1:
                gene[i] = v1_bin_chargers[i]

        v_out.chargers = self.binary_gene_to_chargers(gene)

    def chargers_to_binary_gene(self, v: vehicle.Vehicle):
        gene = [0]*self.mapa.size
        for i in range(self.mapa.size-1):
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
        gene_nodes = [0]*(self.mapa.size)

        for i in range(self.mapa.size-1):
            if i in v.visited_nodes:
                gene_nodes[i] = 1
                if i > 0:
                    gene_nodes[i-1] = 1

                if i < self.mapa.size:
                    gene_nodes[i+1] = 1

        return gene_nodes



    def mutate(self):
        pass
