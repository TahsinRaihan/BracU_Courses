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

        print(self.adj_list)




graph=Graph()

for i in range(edge):
    u,v=map(int,inp.readline().split())
    graph.add_edge(u,v)

