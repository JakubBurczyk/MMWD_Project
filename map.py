import networkx as nx
import matplotlib.pyplot as plt
import random


class Map:
    min_edg_factor = 3 / 2
    max_edg_factor = 5 / 2
    is_charger = 'is_charger'
    weight = 'weight'

    min_weight = 10
    max_weight = 20

    charger_energy = 500

    def connectivity_check(self, Graph,size):
        visited_nodes = [0] * size

        def check_edges(node):
            for (u, v) in Graph.edges:
                if u == node:
                    if not visited_nodes[v]:
                        visited_nodes[v] = 1
                        check_edges(v)
                elif v == node:
                    if not visited_nodes[u]:
                        visited_nodes[u] = 1
                        check_edges(u)

        check_edges(0)
        if 0 in visited_nodes:
            print(visited_nodes)
            return False
        else:
            print(visited_nodes)
            return True

    def graph_generator(self, size: int, edg: int, tries):
        for i in range(tries - 1):
            Graph = nx.gnm_random_graph(size, edg)
            if self.connectivity_check(Graph,size):
                print("Tries: ", i + 1)
                return Graph
        print("whaat")
        return None

    def __init__(self, size: int, edg: int = 0, as_complete=False, tries: int = 100):
        if edg < size * self.min_edg_factor:
            edg = random.randint(size * self.min_edg_factor, size * self.max_edg_factor)

        self.edg_number = edg

        if as_complete:
            self.G = nx.complete_graph(size)
        else:
            self.G = self.graph_generator(size, edg, tries)
            print(self.G.edges)
        # initialize random weights in range <min_weight, max_weight>

        for (u, v) in self.G.edges():
            e = self.G.edges[u, v]
            self.G.edges[u, v][self.weight] = random.randint(self.min_weight, self.max_weight)

        # intialize charger attribute
        nx.set_node_attributes(self.G, False, self.is_charger)

        # test charger as last node
        self.set_as_charger(size - 1)

    def print(self, edge_filter=0):
        if edge_filter < self.min_weight:
            edge_filter = self.min_weight

        e = [(u, v) for (u, v, d) in self.G.edges(data=True) if d[self.weight] > edge_filter]

        pos = nx.spring_layout(self.G)  # positions for all nodes

        # nodes
        color_map = []
        for node in self.G.nodes(data=True):
            if node[1][self.is_charger] is True:
                color_map.append('lightgreen')
            else:
                color_map.append('lightblue')

        nx.draw_networkx_nodes(self.G, pos, node_size=200, node_color=color_map)

        # edges
        nx.draw_networkx_edges(self.G, pos, edgelist=e, width=1)

        # labels
        nx.draw_networkx_labels(self.G, pos, font_size=10, font_family="sans-serif")

        plt.axis("on")
        plt.show()

    def count_chargers(self) -> int:
        chargers = 0
        for node in self.G.nodes(data=True):
            if node[1][self.is_charger] is True:
                chargers = chargers + 1

        return chargers

    def set_as_charger(self, node_num) -> None:

        if node_num in self.G.nodes:
            t = self.G.nodes(data=True)[node_num]
            self.G.nodes(data=True)[node_num][self.is_charger] = True

    def get_distance_between(self, n1, n2) -> float:
        if (n1, n2) in self.G.edges:
            return self.G.edges[n1, n2][self.weight]
        else:
            return None
