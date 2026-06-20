from collections import deque

# Open and read the input2.txt file
try:
    file = open('input2.txt', 'r')
    lines = file.readlines()
    file.close()
except FileNotFoundError:
    print("❌ Error: 'input2.txt' not found.")
    exit()

# Strip lines and prepare data list
data = []
for line in lines:
    if line.strip() != "":
        parts = line.strip().split()
        for item in parts:
            data.append(item)

# Use index-based parsing
index = 0

# Read number of nodes and edges
n = int(data[index])
index += 1
m = int(data[index])
index += 1

# Read start and goal nodes
start = int(data[index])
index += 1
goal = int(data[index])
index += 1

# Read heuristics
heuristics = {}
for i in range(n):
    node = int(data[index])
    index += 1
    h_val = int(data[index])
    index += 1
    heuristics[node] = h_val

# Create adjacency list
adj = {}
for i in range(1, n + 1):
    adj[i] = []

# Read edges
for i in range(m):
    u = int(data[index])
    index += 1
    v = int(data[index])
    index += 1
    adj[u].append(v)
    adj[v].append(u)  # undirected

# BFS to find shortest path from each node to goal
distances = {}
for i in range(1, n + 1):
    distances[i] = float('inf')

queue = deque()
queue.append(goal)
distances[goal] = 0

while len(queue) > 0:
    current = queue.popleft()
    for neighbor in adj[current]:
        if distances[neighbor] == float('inf'):
            distances[neighbor] = distances[current] + 1
            queue.append(neighbor)

# Check for admissible heuristics
inadmissible_nodes = []

for node in range(1, n + 1):
    heuristic_value = heuristics[node]
    true_cost = distances[node]
    if heuristic_value > true_cost:
        inadmissible_nodes.append(node)

# Print output
if len(inadmissible_nodes) == 0:
    print(1)
else:
    print(0)
    for node in inadmissible_nodes:
        print(node, end=' ')
    print()
