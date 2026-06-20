import heapq

# Calculate Manhattan distance between two points
def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

# Solve one maze test case using A* Search
def solve_case(n, m, start_x, start_y, goal_x, goal_y, maze):
    directions = [(1, 0, 'D'), (0, -1, 'L'), (0, 1, 'R'), (-1, 0, 'U')]  # down, left, right, up
    open_set = []
    g_cost = {}
    g_cost[(start_x, start_y)] = 0
    parent = {}
    visited = set()

    start_h = manhattan_distance(start_x, start_y, goal_x, goal_y)
    heapq.heappush(open_set, (start_h, 0, (start_x, start_y)))

    while len(open_set) > 0:
        current_f, current_g, (x, y) = heapq.heappop(open_set)

        if (x, y) == (goal_x, goal_y):
            path = []
            current = (x, y)
            while current != (start_x, start_y):
                previous, move_char = parent[current]
                path.append(move_char)
                current = previous
            path.reverse()
            return str(len(path)) + "\n" + ''.join(path)

        if (x, y) in visited:
            continue

        visited.add((x, y))

        for direction in directions:
            dx = direction[0]
            dy = direction[1]
            move_char = direction[2]
            nx = x + dx
            ny = y + dy

            if nx >= 0 and nx < n and ny >= 0 and ny < m:
                if maze[nx][ny] == '0':
                    new_g = current_g + 1
                    if (nx, ny) not in g_cost or new_g < g_cost[(nx, ny)]:
                        g_cost[(nx, ny)] = new_g
                        h = manhattan_distance(nx, ny, goal_x, goal_y)
                        f = new_g + h
                        parent[(nx, ny)] = ((x, y), move_char)
                        heapq.heappush(open_set, (f, new_g, (nx, ny)))

    return "-1"

# === Start of program ===

# Read from input file
try:
    file = open("input1a.txt", "r")
    lines = file.readlines()
    file.close()
except FileNotFoundError:
    print("❌ Error: 'input1a.txt' not found.")
    exit()

# Remove empty lines and strip each line
clean_lines = []
for line in lines:
    line = line.strip()
    if line != "":
        clean_lines.append(line)

# Process each test case
i = 0
results = []

while i < len(clean_lines):
    # Maze dimensions
    size_line = clean_lines[i]
    n, m = map(int, size_line.split())
    i += 1

    # Start position
    start_line = clean_lines[i]
    a, b = map(int, start_line.split())
    i += 1

    # Goal position
    goal_line = clean_lines[i]
    c, d = map(int, goal_line.split())
    i += 1

    # Maze grid
    maze = []
    for row in range(n):
        maze.append(clean_lines[i])
        i += 1

    # Solve the maze
    result = solve_case(n, m, a, b, c, d, maze)
    results.append(result)

# Print the results
print("=== RESULTS ===")
for res in results:
    print(res)
    print()
