import heapq
def Dijkstra(G,s):
    dist = [float('inf')]*(len(G))
    dist[s] = 0
    priority_q = []
    heapq.heappush(priority_q,(dist[s],s))
    parent = [-1]*len(G)
    visited = [False]*len(G)

    while len(priority_q) != 0 :
        val,u = heapq.heappop(priority_q)
        if visited[u] == True:
            continue
        visited[u] = True
        for j,w in G[u]:
            n_cost = val + w
            if n_cost < dist[j]:
                dist[j] = n_cost
                parent[j] = u
                heapq.heappush(priority_q,(dist[j],j))
    dist.pop(0)
    for e in range(len(dist)):
        if dist[e] == float('inf'):
            dist[e] = -1            
    return dist          

in_file = open("input.txt","r")
out_file = open("output.txt","w")

N,M = list(map(int,in_file.readline().split(" ")))
dict1 = {}
for i in range (N+1):
    dict1[i] = []
    
for i in range(M):
    x,y,cost = list(map(int,in_file.readline().split(" ")))
    dict1[x].append((y,cost))

for i in range(M+1,M+2,1):
    source = list(map(int,in_file.readline().split(" ")))

weight = Dijkstra(dict1,source[0]) 
for k in weight:
    out_file.write(f"{k} ")
    
in_file.close()
out_file.close()