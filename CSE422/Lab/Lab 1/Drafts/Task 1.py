
import heapq

with open('input1.txt', 'r') as f:
    lines = f.readlines()

def input():
    return lines.pop(0)
 
def solve():
    # Read maze dimensions
    n, m = map(int, input().split())
    # Read start and goal coordinates
    a, b = map(int, input().split())
    c, d = map(int, input().split())
    # Read maze grid
    maze = [input().rstrip() for _ in range(n)]
    
    # Manhattan-distance heuristic
    def h(x, y):
        return abs(x - c) + abs(y - d)
    
    # Possible moves: (dx, dy, move_char)
    moves = [
        (1, 0, 'D'),
        (0, -1, 'L'),
        (0, 1, 'R'),
        (-1, 0, 'U')
    ]
    
    # A* priority queue holds tuples (f = g + h, g, (x, y))
    open_heap = []
    g_score = {(a, b): 0}
    heapq.heappush(open_heap, (h(a, b), 0, (a, b)))
    parents = {}      # To reconstruct path: child_coord → (parent_coord, move_char)
    closed = set()    # Visited set
    
    while open_heap:
        f, g, (x, y) = heapq.heappop(open_heap)
        if (x, y) == (c, d):
            # Reconstruct path of moves
            path = []
            cur = (x, y)
            while cur != (a, b):
                cur, move = parents[cur]
                path.append(move)
            # Output cost and move sequence
            print(len(path))
            print(''.join(reversed(path)))
            return
        
        if (x, y) in closed:
            continue
        closed.add((x, y))
        
        # Explore neighbors
        for dx, dy, move in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and maze[nx][ny] == '0':
                ng = g + 1
                # If this path to (nx,ny) is better, record it
                if ng < g_score.get((nx, ny), float('inf')):
                    g_score[(nx, ny)] = ng
                    parents[(nx, ny)] = ((x, y), move)
                    heapq.heappush(open_heap, (ng + h(nx, ny), ng, (nx, ny)))
    
    # No path found
    print(-1)

if __name__ == "__main__":
    solve()
