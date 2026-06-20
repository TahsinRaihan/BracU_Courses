from collections import deque

# Read all lines from the input file
with open("input2a.txt", "r") as file:
    lines = [line.strip() for line in file if line.strip() != ""]

i = 0
case_number = 1

while i < len(lines):
    # Read n and m
    n, m = map(int, lines[i].split())
    i += 1

    # Read start and goal
    start, goal = map(int, lines[i].split())
    i += 1

    # Read heuristic values
    heuristics = {}
    for _ in range(n):
        node, h_val = map(int, lines[i].split())
        heuristics[node] = h_val
        i += 1

    # Build adjacency list
    adj = {node: [] for node in range(1, n + 1)}
    for _ in range(m):
        u, v = map(int, lines[i].split())
        adj[u].append(v)
        adj[v].append(u)
        i += 1

    # Compute true distances from each node to goal using BFS
    distances = {node: float('inf') for node in range(1, n + 1)}
    distances[goal] = 0
    queue = deque([goal])

    while queue:
        current = queue.popleft()
        for neighbor in adj[current]:
            if distances[neighbor] == float('inf'):
                distances[neighbor] = distances[current] + 1
                queue.append(neighbor)

    # Check for admissibility
    inadmissible = []
    for node in range(1, n + 1):
        if heuristics[node] > distances[node]:
            inadmissible.append(node)

    # Output result for this case
    print(f"Case {case_number}:")
    if not inadmissible:
        print(1)
        print("The heuristic values are admissible.")
    else:
        print(0)
        print("Nodes", *inadmissible, "are inadmissible.")
    print()

    case_number += 1
