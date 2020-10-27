class Map:
    def __init__(self, size: int):
        self.graph = []
        self.size = size

        for i in range(0, size):
            self.graph.append([0] * size)
            self.graph[i][i] = -1

    def print(self):
        for i in range(0, self.size):
            print(self.graph[i])
