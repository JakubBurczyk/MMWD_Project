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

    def __init__(self, size: int, edg: int = 0):
        if edg < size*self.min_edg_factor:
            edg = random.randint(size*self.min_edg_factor, size*self.max_edg_factor)

        self.edg_number = edg
        self.G = nx.gnm_random_graph(size, edg)

        #initialize random weights in range <min_weight, max_weight>

        for (u, v) in self.G.edges():
            e = self.G.edges[u, v]
            self.G.edges[u, v][self.weight] = random.randint(self.min_weight, self.max_weight)

        #intialize charger attribute
        nx.set_node_attributes(self.G, False, self.is_charger)

        #test charger as last node
        self.G.nodes[size-1][self.is_charger] = True

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