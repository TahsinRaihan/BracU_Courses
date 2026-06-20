inp = open("input6_1.txt", "r")
out = open("output6_1.txt", "w")


node, edge = map(int, inp.readline().split())
grid = [list(inp.readline().strip()) for _ in range(node)]


def dfs(grid, row, col, visited):
    if row < 0 or col < 0 or row >= len(grid) or col >= len(grid[0]):
        return 0
    
    if grid[row][col]=='#' or visited[row][col]:
        return 0
    
    if grid[row][col] == 'D':
        visited[row][col] = 1
        diamonds = 1
        
    else:
        diamonds = 0

    visited[row][col] = 1

    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        new_row, new_col = row + dr, col + dc
        diamonds += dfs(grid, new_row, new_col, visited)

    return diamonds


def max_diamonds(grid):
    rows = len(grid)
    cols = len(grid[0])
    visited = []
    for _ in range(rows):
        visited.append([0] * cols)

    max_diamond_count = 0

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == '.' and not visited[i][j]:
                diamonds_collected = dfs(grid, i, j, visited)
                max_diamond_count = max(max_diamond_count, diamonds_collected)

    return max_diamond_count



result = max_diamonds(grid)


out.write(f"{result}")


inp.close()
out.close()