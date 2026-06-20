inp=open('input.txt','r')
out=open('output.txt','w')

ver,edge=map(int,inp.readline().split())

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

def DFS(graph,start,visited=None,path=None):
    if visited==None:
        visited=set()
    if path==None:
        path=[]
    visited.add(start)
    path.append(start)
    for neighbour in graph.adj_list[start]:
        if neighbour not in visited:
            DFS(graph,neighbour,visited,path)
    return path


graph=Graph()

for i in range(edge):
    u,v=map(int,inp.readline().split())
    graph.add_edge(u,v)

x=DFS(graph,1)

out.write(" ".join(map(str,x)))