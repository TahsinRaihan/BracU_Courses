from collections import deque

inp = open("input1b_1.txt", "r")
out = open("output1b_1.txt", "w")

vertices, edges = map(int, inp.readline().split())
            
class Graph:
    def __init__(self):
        self.vertices = 0
        self.graph = {}
        self.indegree = []

    def add_edge(self, u, v):
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []
        self.graph[u].append(v)


    def initialize_indegree(self):
        self.indegree = [0] * (self.vertices + 1)
        for u in self.graph:
            for v in self.graph[u]:
                self.indegree[v] += 1

    def topological_sort_bfs(self):
        queue = deque()
        result = []

        for v in range(1, self.vertices + 1):
            if self.indegree[v] == 0:
                queue.append(v)

        while queue:
            u = queue.popleft()
            result.append(u)

            for v in self.graph[u]:
                self.indegree[v] -= 1
                if self.indegree[v] == 0:
                    queue.append(v)

        if len(result) != self.vertices:
            return "IMPOSSIBLE"
        return result


graph = Graph()
graph.vertices = vertices

for _ in range(edges):
    u, v = map(int, inp.readline().split())
    graph.add_edge(u, v)

graph.initialize_indegree()
result = graph.topological_sort_bfs()

if result == "IMPOSSIBLE":
    out.write("IMPOSSIBLE")
else:
    out.write(" ".join(map(str, result)))


inp.close()
out.close()

