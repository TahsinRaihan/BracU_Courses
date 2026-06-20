import heapq


inp = open("input1.txt", "r")
out = open("output1.txt", "w")
vertices, edges = [int(i) for i in inp.readline().split()]


def length(graph, u, v):
    for x in graph[u]['Adj']:
        if x == v:
            return int(x[1])

def dijkstra(graph, start):
    dist = [float("inf")] * len(graph)
    prev = [None] * len(graph)
    dist[start - 1] = 0
    q = [(0, start)]
    visited = [False] * len(graph)
    while q:
        cost, vertice = heapq.heappop(q)
        if visited[vertice - 1]:
            continue
        visited[vertice - 1] = True
        for v in graph[vertice]['Adj']:
            alt = dist[vertice - 1] + length(graph, vertice, v)

            if alt < dist[v[0] - 1]:
                dist[v[0] - 1] = alt
                prev[v[0] - 1] = vertice
                heapq.heappush(q, [alt, v[0]])
    return dist


graph = {}
for i in range(1, vertices + 1):
    graph[i] = {"Adj": []}


for i in range(edges):
    u, v, cost = [int(i) for i in inp.readline().split()]
    graph[u]["Adj"].append((v, cost))


start = int(inp.readline())

for i in dijkstra(graph, start):
    if i == float('inf'):
        out.write('-1' + " ")
    else:
        out.write(str(i) + " ")


inp.close()
out.close()






