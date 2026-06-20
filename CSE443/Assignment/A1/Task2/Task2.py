with open('Task2.txt', 'r') as f:
    lines = [line.strip() for line in f if line.strip()]

k = int(lines[0])
kmers = lines[1:]

graph = {}
in_degree = {}
out_degree = {}

for kmer in kmers:
    prefix = kmer[:-1]
    suffix = kmer[1:]
    
    if prefix not in graph:
        graph[prefix] = []
    if suffix not in graph:
        graph[suffix] = []
        
    graph[prefix].append(suffix)
    
    out_degree[prefix] = out_degree.get(prefix, 0) + 1
    in_degree[suffix] = in_degree.get(suffix, 0) + 1
    
    if prefix not in in_degree:
        in_degree[prefix] = 0
    if suffix not in out_degree:
        out_degree[suffix] = 0

start_node = kmers[0][:-1]
for node in graph:
    if out_degree[node] - in_degree[node] == 1:
        start_node = node
        break

stack = [start_node]
path = []

while stack:
    curr = stack[-1]
    if graph[curr]:
        stack.append(graph[curr].pop())
    else:
        path.append(stack.pop())

path.reverse()
text = path[0] + "".join([node[-1] for node in path[1:]])

with open('Task2_output.txt', 'w') as out:
    out.write(text + '\n')

