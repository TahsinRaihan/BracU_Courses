inp = open("input3_1.txt", "r")
out = open("output3_1.txt", "w")

vertices, edges = [int(i) for i in inp.readline().split()]

class Tracker:
    def __init__(self):
        self.time = 0
        self.scc = []

def dfs_first_pass(graph, tracker):
    for u in graph:
        graph[u]['color'] = 'white'
        graph[u]['transpose'] = []
    tracker.time = 0
    for u in graph:
        if graph[u]['color'] == 'white':
            dfs_visit_first_pass(graph, u, tracker)


def dfs_visit_first_pass(graph, u, tracker):
    graph[u]['color'] = 'gray'
    tracker.time += 1
    for v in graph[u]["Adj"]:
        if graph[v]['color'] == 'white':
            dfs_visit_first_pass(graph, v, tracker)
    graph[u]['color'] = 'black'
    tracker.time += 1
    finish_time[u] = tracker.time


def transpose(graph):
    for i in graph:
        for x in graph[i]['Adj']:
            graph[x]['transpose'].append(i)


def dfs_second_pass(graph, tracker, top_ord):
    for u in graph:
        graph[u]['visited'] = False
    tracker.time = 0
    for u in top_ord:
        temp = [u]
        if graph[u]['visited'] == False:
            graph[u]['visited'] = True
            dfs_visit_second_pass(graph, u, tracker, temp)
            tracker.scc.append(temp)

def dfs_visit_second_pass(graph, u, tracker, temp):
    tracker.time += 1
    for v in graph[u]["transpose"]:
        if graph[v]['visited'] == False:
            temp.append(v)
            graph[v]['visited'] = True
            dfs_visit_second_pass(graph, v, tracker, temp)
    tracker.time += 1
    finished_time[u] = tracker.time

finish_time = {}
finished_time = {}

graph = {}
for i in range(1, vertices + 1):
    graph[i] = {'color': None, "Adj": []}


for i in range(edges):
    u, v = [int(i) for i in inp.readline().split()]
    graph[u]["Adj"].append(v)


t1 = Tracker()
t2 = Tracker()

dfs_first_pass(graph, t1)
top_ord = sorted(finish_time, key=finish_time.get, reverse=True)
transpose(graph)
dfs_second_pass(graph, t2, top_ord)

for i in t2.scc:
    for j in sorted(i):
        out.write(str(j) + " ")
    out.write("\n")

inp.close()
out.close()
