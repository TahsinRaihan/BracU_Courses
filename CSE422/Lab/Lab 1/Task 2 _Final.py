from collections import deque

with open("input2a.txt", "r") as file:
    all_input_lines = [line.strip() for line in file if line.strip()]

line_pointer = 0
current_case = 1

while line_pointer < len(all_input_lines):
    
    num_vertices, num_edges = map(int, all_input_lines[line_pointer].split())   #number of vertices and edges
    line_pointer += 1
    entry_node, target_node = map(int, all_input_lines[line_pointer].split())
    line_pointer += 1

    estimated_cost = {}    #  adjacency list
    for i in range(num_vertices):
        node_id, heuristic_val = map(int, all_input_lines[line_pointer].split())
        estimated_cost[node_id] = heuristic_val
        line_pointer += 1


    graph_edges = {node: [] for node in range(1, num_vertices + 1)}  #  adjacency list
    for j in range(num_edges):
        node_u, node_v = map(int, all_input_lines[line_pointer].split())
        graph_edges[node_u].append(node_v)
        graph_edges[node_v].append(node_u)
        line_pointer += 1



    shortest_path_cost = {node: float('inf') for node in range(1, num_vertices + 1)}
    shortest_path_cost[target_node] = 0
    bfs_queue = deque([target_node])

    while bfs_queue:  # Using BFS to compute actual shortest path
        current_node = bfs_queue.popleft()
        for neighbor_node in graph_edges[current_node]:
            if shortest_path_cost[neighbor_node] == float('inf'):
                shortest_path_cost[neighbor_node] = shortest_path_cost[current_node] + 1
                bfs_queue.append(neighbor_node)

    # Check heuristic admissibility
    violating_nodes = []
    for node in range(1, num_vertices + 1):
        if estimated_cost[node] > shortest_path_cost[node]:
            violating_nodes.append(node)

    # Output results for all test case
    print(f"Case {current_case}:")
    if not violating_nodes:
        print(1)
        print("The heuristic values are admissible.")
    else:
        print(0)
        print("Nodes", *violating_nodes, "are inadmissible.")
    print()

    current_case += 1
