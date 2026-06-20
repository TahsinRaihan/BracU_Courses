inp=open("input3_1.txt","r")
out=open("output3_1.txt","w")


ver,edge=map(int,inp.readline().split(" "))

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

def dfs(graph,start,visited=None,path=None):
  if visited is None:
    visited=set()
  if path is None:
    path=[]
  visited.add(start)
  path.append(start)
  for neighbour in graph.adj_list[start]:
    if neighbour not in visited:
      dfs(graph,neighbour,visited,path)

  return path


graphh=Graph()
for _ in range(edge):
  u, v = map(int, inp.readline().split())
  graphh.add_edge(u,v)

p=dfs(graphh,1)
out.write(" ".join(map(str,p)))


inp.close()
out.close()

