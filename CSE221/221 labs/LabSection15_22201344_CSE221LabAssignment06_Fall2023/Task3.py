from queue import PriorityQueue

inp= open("input3.txt", "r")
out= open('output3.txt', 'w')


num_nodes, num_edges = map(int, inp.readline().split())
graph = [[] for _ in range(num_nodes)]

for i in range(num_edges):
    u, v, w = map(int, inp.readline().split())
    graph[u - 1].append((v - 1, w))
    graph[v - 1].append((u - 1, w))


def dijkstra(graph, start):
    num_nodes = len(graph)
    distances = [float('inf')] * num_nodes
    visited = [False] * num_nodes
    distances[start] = 0
    pq = PriorityQueue()
    pq.put((0, start))

    while not pq.empty():
        current_node = pq.get()[1]
        visited[current_node] = True

        for neighbor, weight in graph[current_node]:
            if not visited[neighbor]:
                new_distance = max(distances[current_node], weight)
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    pq.put((distances[neighbor], neighbor))

    return distances

distances = dijkstra(graph, 0)

if distances[num_nodes - 1] == float('inf'):
    out.write("Impossible")
else:
    out.write(f"{distances[num_nodes - 1]}")
