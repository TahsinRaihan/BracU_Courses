inp = open("input5_1.txt", "r")
out = open("output5_1.txt", "w")
n, m, end = map(int, inp.readline().strip().split())

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

def bfs(Graph, start, end):
    visited = set()
    queue = deque([(start, [start])])
    while queue:
        current_city, path = queue.popleft()
        visited.add(current_city)
        if current_city==end:
            return path
        for neighbour in Graph.adj_list[current_city]:
            if neighbour not in visited:
                queue.append((neighbour, path + [neighbour]))
    return None


graph = Graph()
for _ in range(m):
    u, v = map(int, inp.readline().split())
    graph.add_edge(u, v)

path = bfs(graph, 1, end)
if path is not None:
    out.write(f"Time: {len(path) - 1}\n")
    out.write(f"Shortest Path: {' '.join(map(str, path))}\n")
else:
    out.write("Time: 0\n")
    out.write("Shortest Path: 1\n")


inp.close()
out.close()

