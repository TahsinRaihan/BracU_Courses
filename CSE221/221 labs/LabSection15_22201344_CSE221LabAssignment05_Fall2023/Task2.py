from collections import defaultdict
import heapq


inp = open("input2_1.txt", "r")
out = open("output2_1.txt", "w")

vertices, edges = map(int, inp.readline().split())


class Graph:
    def __init__(self):
        self.vertices = 0
        self.graph = defaultdict(list)
        self.indegree = defaultdict(int)

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.indegree[v] += 1


    def initialize_indegree(self):
        for u in self.graph:
            for v in self.graph[u]:
                self.indegree[v] += 0


    def topological_sort(self):
        heap = []  
        result = []

        for u in range(1, self.vertices + 1):
            if self.indegree[u] == 0:
                heapq.heappush(heap, u)

        while heap:
            u = heapq.heappop(heap)  
            result.append(u)

            for v in self.graph[u]:
                self.indegree[v] -= 1
                if self.indegree[v] == 0:
                    heapq.heappush(heap, v)

        if len(result) != self.vertices:
            return "IMPOSSIBLE"
        return result




graph = Graph()
graph.vertices = vertices

for _ in range(edges):
    u, v = map(int, inp.readline().split())
    graph.add_edge(u, v)

graph.initialize_indegree()
result = graph.topological_sort()

if result == "IMPOSSIBLE":
    out.write("IMPOSSIBLE")
else:
    for i in result:
        out.write(str(i) + " ")

inp.close()
out.close()
