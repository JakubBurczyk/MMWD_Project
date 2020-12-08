import networkx as nx
import matplotlib.pyplot as plt
import random


class Map:
    min_edg_factor = 3 / 2
    max_edg_factor = 5 / 2
    is_charger = 'is_charger'
    weight = 'weight'

    min_weight = 3
    max_weight = 8

    charger_energy = 500

    def __init__(self, size: int, edg: int = 0, as_complete=False, tries: int = 100):
        if edg < size * self.min_edg_factor:
            edg = random.randint(size * self.min_edg_factor, size * self.max_edg_factor)

        self.edg_number = edg
        self.size = size

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
        # self.set_as_charger(size - 1)

    def delete_doubled_edges(self, Graph):
        to_be_removed = []
        for (u, v) in Graph.edges:
            counter = 0
            for (x, y) in Graph.edges:
                if x == u and y == v:
                    counter += 1

                elif x == v and y == u:
                    counter += 1
            if counter > 1:
                if (u, v) not in to_be_removed and (v, u) not in to_be_removed:
                    to_be_removed.append((u, v))

        for el in to_be_removed:
            if el in Graph.edges:
                Graph.remove_edge(el[0], el[1])
                print("removed")
        return Graph

    def connectivity_check(self, Graph, size):
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

        def check_for_singles():
            for n in Graph.nodes:
                counter = 0
                for (u, v) in Graph.edges:
                    if u == n:
                        counter += 1
                    elif v == n:
                        counter += 1
                if counter < 3:
                    listofothernodes = []
                    print("adasdasd ",n)
                    for i in range(size):
                        if i != n:
                            listofothernodes.append(i)
                    choosen_ones = random.choices(listofothernodes, k=3)
                    Graph.add_edge(n, choosen_ones[0])
                    Graph.add_edge(n, choosen_ones[1])
                    Graph.add_edge(n, choosen_ones[2])

        check_for_singles()

        check_edges(0)
        print(visited_nodes)
        if 0 in visited_nodes:
            good_island = []
            overboard = []
            for i in range(size):
                if visited_nodes[i]:
                    good_island.append(i)
                else:
                    overboard.append(i)
            for node in overboard:
                print("node to: ", node, "\n")
                choosen_ones = random.choices(good_island, k=2)
                print("lacze z: ", choosen_ones, "\n")
                Graph.add_edge(node, choosen_ones[0])
                Graph.add_edge(node, choosen_ones[1])
            # print(visited_nodes)
        return True

    def graph_generator(self, size: int, edg: int, tries):
        for i in range(tries):

            # Graph = self.delete_doubled_edges(nx.gnm_random_graph(size, edg))
            Graph = nx.gnm_random_graph(size, edg)
            if self.connectivity_check(Graph, size):
                print("Tries: ", i + 1)
                return Graph
        print("whaat")
        return None

    def print(self, edge_filter=0):
        if edge_filter < self.min_weight:
            edge_filter = self.min_weight

        e = [(u, v) for (u, v, d) in self.G.edges(data=True) if d[self.weight] >= edge_filter]

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

    def neighbours(self, node) -> list:
        neighbours = []
        for (u, v) in self.G.edges:
            if u == node:
                neighbours.append(v)
            elif v == node:
                neighbours.append(u)
        return neighbours