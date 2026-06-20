inp=open('input1.txt','r')
out=open('output1.txt','w')

ver,edge=map(int,inp.readline().split())

from collections import deque

class Graph:
    def __init__(self):
        self.adj_list={}
    def add_edge(self,u,v,w):
        if u not in self.adj_list:
            self.adj_list[u]=[]
        if v  not in self.adj_list:
            self.adj_list[v]=[]
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)


def print_list(graph):
    x=graph.adj_list
    concat=''
    for key, val in x.items():
        print(key,':', val,file=out)



graph=Graph()

for i in range(edge):
    u,v,w=map(int,inp.readline().split())
    graph.add_edge(u,v,w)


s,d=map(int,inp.readline().split())

def BFS(graph,start,end):
    visited=set()
    path=[]
    current=deque([start])
    queue=current.popleft()
    while queue:
        if current not in visited:
            visited.add(current)
            path.append[current]

        for neighbour in graph.adj_list[current]:
            if neighbour not in visited:
                queue.append(current)

        return path
    


print_list(graph)
BFS(graph,s,d)























