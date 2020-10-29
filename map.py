import networkx as nx
import matplotlib.pyplot as plt
import random


class Map:

    def __init__(self, size: int, edg: int = 0):
        if edg < size*3/2:
            edg = random.randrange(int(size*3/2), size*2)

        self.G = nx.gnm_random_graph(size,edg)
        self.chargers = [size-1]

    def print(self):
        e = [(u, v) for (u, v, d) in self.G.edges(data=True)]

        pos = nx.spring_layout(self.G)  # positions for all nodes

        # nodes
        color_map = []
        for node in self.G:
            if node in self.chargers:
                color_map.append('lightblue')
            else:
                color_map.append('lightgreen')

        nx.draw_networkx_nodes(self.G, pos, node_size=200, node_color = color_map)

        # edges
        nx.draw_networkx_edges(self.G, pos, edgelist=e, width=1)

        # labels
        nx.draw_networkx_labels(self.G, pos, font_size=10, font_family="sans-serif")

        plt.axis("on")
        plt.show()