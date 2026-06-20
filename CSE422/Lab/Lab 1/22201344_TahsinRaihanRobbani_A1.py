####Part---1####

import heapq

with open('input1a.txt', 'r') as file: 
    input_lines = [line.strip() for line in file if line.strip()]

def input():
    return input_lines.pop(0)

def manhattan_distance(x1, y1, x2, y2):   
    return abs(x1 - x2) + abs(y1 - y2)

def solve_maze():

    rows, cols = map(int, input().split())  
    start_row, start_col = map(int, input().split())
    goal_row, goal_col   = map(int, input().split())
    maze_grid = [input() for i in range(rows)]

    # A* setup
    directions = [
        ( 1,  0, 'D'),
        ( 0, -1, 'L'),
        ( 0,  1, 'R'),
        (-1,  0, 'U'),
    ]
    visited_nodes = set()
    came_from     = {}
    g_score_map   = {(start_row, start_col): 0}


    priority_queue = []
    start_h = manhattan_distance(start_row, start_col, goal_row, goal_col)
    heapq.heappush(priority_queue, (start_h, 0, (start_row, start_col)))


    while priority_queue:
        f_score, current_g, (r, c) = heapq.heappop(priority_queue)

        # Check goal
        if (r, c) == (goal_row, goal_col):

            moves = []
            node = (r, c)
            while node != (start_row, start_col):
                node, move_char = came_from[node]
                moves.append(move_char)
            moves.reverse()

            print(len(moves))
            print(''.join(moves))
            return

        if (r, c) in visited_nodes:
            continue
        visited_nodes.add((r, c))

        # Explore neighbors
        for dr, dc, move_char in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze_grid[nr][nc] == '0': #ensure it is within the maze
                tentative_g = current_g + 1
                prev_g = g_score_map.get((nr, nc), float('inf'))
                if tentative_g < prev_g:
                    g_score_map[(nr, nc)] = tentative_g
                    came_from[(nr, nc)] = ((r, c), move_char)
                    h = manhattan_distance(nr, nc, goal_row, goal_col)
                    heapq.heappush(priority_queue, (tentative_g + h, tentative_g, (nr, nc)))


    print(-1) # IF No path found

first_case = True
while input_lines: #Read input from all the folowing cases
    if not first_case:
        print()  
    first_case = False
    solve_maze()



####Part---2####




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

    # CHECk heuristic admissibility
    violating_nodes = []
    for node in range(1, num_vertices + 1):
        if estimated_cost[node] > shortest_path_cost[node]:
            violating_nodes.append(node)

    # cHecking  for all test case
    print(f"Case {current_case}:")
    if not violating_nodes:
        print(1)
        print("The heuristic values are admissible.")
    else:
        print(0)
        print("Nodes", *violating_nodes, "are inadmissible.")
    print()

    current_case += 1

