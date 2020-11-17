import map
import vehicle
import random
from operator import attrgetter


class Genetics:

    def __init__(self, nodes: int = 0, edges: int = 0, vehicles_no: int = 100):

        self.mapa = map.Map(nodes, edges, as_complete=False, tries=100)
        self.vehicles = []

        for i in range(vehicles_no):
            self.vehicles.append(vehicle.Vehicle(self.mapa))

    def cycle(self):

        for v in self.vehicles:
            while True:

                result = self.move_to_random_neighbour(v)
                if result:
                    break

        self.rank()

    def move_to_random_neighbour(self, v: vehicle.Vehicle) -> bool:
        # TODO:sprawdzac czy wierzcholek odwiedzany jest ladowarka -> podladowac

        neighbours = v.map.neighbours(v.current_node)
        to_be_removed = []
        for n in neighbours:
            if not v.can_move_to(n):
                to_be_removed.append(n)

        for n in to_be_removed:
            neighbours.remove(n)

        if not neighbours:
            v.chargers.append(v.current_node)
            return True
        to_be_removed_2 = []
        for n in neighbours:
            if n in v.visited_nodes:
                to_be_removed_2.append(n)

        for n in to_be_removed_2:
            neighbours.remove(n)

        if neighbours:
            destination = neighbours[random.randint(0, len(neighbours) - 1)]
            v.move(destination)
            v.visited_nodes.append(destination)

            return False
        else:
            return True

    def rank(self):
        self.vehicles.sort(key=attrgetter('kilometrage'), reverse=True)

    def hunger_games(self):
        pass

    def crossing(self):
        pass

    def mutate(self):
        pass