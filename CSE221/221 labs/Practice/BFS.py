inp=open('input.txt','r')
out=open('output.txt','w')

ver,edge=map(int,inp.readline().split())

from collections import deque

class Graph:
    def __init__(self):
        self.adj_list={}
    def add_edge(self,u,v):
        if u not in self.adj_list:
            self.adj_list[u]=[]
        if v not in self.adj_list:
            self.adj_list[v]=[]
        
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)

def BFS(graph,start):
    visited=set()
    path=[]
    queue= deque([start])

    while queue:
        curr=queue.popleft()
        if curr not in visited:
            path.append(curr)
            visited.add(curr)
        for neighbour in graph.adj_list[curr]:
            if neighbour not in visited:
                queue.append(neighbour)

    return path





graph=Graph()

for i in range(edge):
    u,v=map(int,inp.readline().split())
    graph.add_edge(u,v)

x=BFS(graph,1)

out.write(" ".join(map(str,x)))