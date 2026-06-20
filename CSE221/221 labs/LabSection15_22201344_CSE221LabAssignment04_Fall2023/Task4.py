inp = open("input4_1.txt", "r")
out = open("output4_1.txt", "w")
ver, edge = map(int, inp.readline().strip().split(" "))


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


graph = Graph()
for _ in range(edge):
    u, v = map(int, inp.readline().strip().split())
    graph.add_edge(u, v)

if graph.has_cycle():
    out.write("YES")
else:
    out.write("NO")

inp.close()
out.close()
