input_file = open("input2_1.txt", "r")
output_file = open("output2_1.txt", "w")


ver, edge = map(int, input_file.readline().split(" "))


from collections import deque

class Graph:
    def __init__(self):
        self.adj_list = {}

    def add_edge(self, u, v):
        if u not in self.adj_list:
            self.adj_list[u] = []
        if v not in self.adj_list:
            self.adj_list[v] = []
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)


def bfs(Graph, start):
    visited = set()
    queue = deque([start])
    path = []

    while queue:
        current_city = queue.popleft()
        if current_city not in visited:
            path.append(current_city)
            visited.add(current_city)
            for neighbour in Graph.adj_list[current_city]:
                if neighbour not in visited:
                    queue.append(neighbour)
    return path



graph = Graph()
for _ in range(edge):
    u, v = map(int, input_file.readline().split())
    graph.add_edge(u, v)


bfs_path = bfs(graph, 1)

output_file.write(" ".join(map(str, bfs_path)))




input_file.close()
output_file.close()

