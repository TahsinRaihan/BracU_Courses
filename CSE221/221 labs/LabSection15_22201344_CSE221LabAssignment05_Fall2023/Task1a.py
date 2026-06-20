inp = open("input1a_3.txt", "r")
out = open("output1a_3.txt", "w")

ver, edge = map(int, inp.readline().split())


class Graph:
    def __init__(self):
        self.adj_list = {}

    def add_edge(self, u, v):
        if u not in self.adj_list:
            self.adj_list[u] = []
        if v not in self.adj_list:
            self.adj_list[v] = []
        self.adj_list[u].append(v)

    def has_cycle(self):
        visited = set()
        stack = set()

        def dfs(node):
            if node in stack:
                return True
            if node in visited:
                return False
            visited.add(node)
            stack.add(node)
            for neighbor in self.adj_list[node]:
                if dfs(neighbor):
                    return True
            stack.remove(node)
            return False

        for node in self.adj_list:
            if dfs(node):
                return True
        return False

def topologicalDFS(G, s, visited, path, stack, flag):
    visited[s] = 1
    path[s] = 1
    for i in G[s]:
        if visited[i] == 0:
            topologicalDFS(G, i, visited, path, stack, flag)
        elif path[i] == 1:
            flag = True
            
    path[s] = 0
    stack.append(s)


def topological_sort(graph):
    visited = [0] * (len(graph) + 1)
    path = [0] * (len(graph) + 1)
    stack = []
    flag = False

    for node in graph.keys():
        if visited[node] == 0:
            topologicalDFS(graph, node, visited, path, stack, flag)

    if flag:
        return "IMPOSSIBLE"
    else:
        return stack[::-1]


graph = Graph()
for _ in range(edge):
    u, v = map(int, inp.readline().split())
    graph.add_edge(u, v)

if graph.has_cycle():
    out.write("IMPOSSIBLE")
else:
    order = topological_sort(graph.adj_list)
    out.write(" ".join(map(str, order)))


inp.close()
out.close()










