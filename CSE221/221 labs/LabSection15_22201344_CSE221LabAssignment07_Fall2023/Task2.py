inp = open('input_2a.txt', 'r')
out = open('output_2a.txt', 'w')

city, road = map(int, inp.readline().split())

adj_list = [[] for _ in range(city + 1)]
visited = [0 for _ in range(city + 1)]

for _ in range(road):
    f, t, w = map(int, inp.readline().split())
    adj_list[f].append((t, w))
    adj_list[t].append((f, w))

def minimum_cost(adj_list, visited):
    pq = []
    cost = 0
    visited[1] = 1
    for i in adj_list[1]:
        pq.append(i)
    while pq:
        pq.sort(key=lambda x: x[1])
        u, w = pq.pop(0)
        if visited[u] == 0:
            visited[u] = 1
            cost += w
            for i in adj_list[u]:
                pq.append(i)
    return cost

print(minimum_cost(adj_list, visited), file=out)

inp.close()
out.close()
