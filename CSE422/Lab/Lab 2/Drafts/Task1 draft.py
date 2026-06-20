import random
import math

# Make random choices repeatable
random.seed(42)

# --- Problem setup ---
grid_size = 25

# Each block is (name, width, height)
blocks = [
    ('ALU', 5, 5),
    ('Cache', 7, 4),
    ('Control Unit', 4, 4),
    ('Register File', 6, 6),
    ('Decoder', 5, 3),
    ('Floating Unit', 5, 5),
]

# Which blocks should be connected by wires (by index in blocks)
net_pairs = [
    (3, 0),  # Register File ↔ ALU
    (2, 0),  # Control Unit ↔ ALU
    (0, 1),  # ALU ↔ Cache
    (3, 5),  # Register File ↔ Floating Unit
    (1, 4),  # Cache ↔ Decoder
    (4, 5),  # Decoder ↔ Floating Unit
]

# --- GA parameters ---
population_size   = 6
elite_count       = 2
mutation_probability = 0.10
num_generations   = 15

# Fitness penalties
alpha = 1000
beta  = 2
gamma  = 1


# --- Helper functions ---

def block_center(position, width, height):
    """Return the (x,y) center point of a block."""
    x, y = position
    return (x + width / 2, y + height / 2)

def count_overlaps(layout):
    """Count how many pairs of blocks overlap in this layout."""
    overlaps = 0
    for i in range(len(blocks)):
        xi, yi = layout[i]
        wi, hi = blocks[i][1], blocks[i][2]
        for j in range(i + 1, len(blocks)):
            xj, yj = layout[j]
            wj, hj = blocks[j][1], blocks[j][2]
            # Check rectangle overlap
            if not (xi + wi <= xj or xj + wj <= xi or
                    yi + hi <= yj or yj + hj <= yi):
                overlaps += 1
    return overlaps

def total_wire_length(layout):
    """Sum of straight-line distances between required block centers."""
    total = 0.0
    for a, b in net_pairs:
        ca = block_center(layout[a], blocks[a][1], blocks[a][2])
        cb = block_center(layout[b], blocks[b][1], blocks[b][2])
        dx = ca[0] - cb[0]
        dy = ca[1] - cb[1]
        total += math.hypot(dx, dy)
    return total

def bounding_box_area(layout):
    """Area of the smallest rectangle enclosing all blocks."""
    xs = [pos[0] for pos in layout]
    ys = [pos[1] for pos in layout]
    min_x = min(xs)
    min_y = min(ys)
    max_x = max(xs[i] + blocks[i][1] for i in range(len(layout)))
    max_y = max(ys[i] + blocks[i][2] for i in range(len(layout)))
    return (max_x - min_x) * (max_y - min_y)

def evaluate_fitness(layout):
    """
    Return a tuple (score, overlaps, wire_length, area).
    Higher score is better, so we negate the weighted penalties.
    """
    ov  = count_overlaps(layout)
    wl  = total_wire_length(layout)
    ar  = bounding_box_area(layout)
    penalty = alpha * ov + beta* wl + gamma * ar
    return -penalty, ov, wl, ar

def make_random_layout():
    """Generate one random layout of all blocks."""
    positions = []
    for _, w, h in blocks:
        x = random.randint(0, grid_size - w)
        y = random.randint(0, grid_size - h)
        positions.append((x, y))
    return positions


# --- Initialize population ---
population = [make_random_layout() for _ in range(population_size)]
best_score    = -math.inf
best_solution = None

# --- Run GA ---
for _ in range(num_generations):
    # Score all layouts
    scored = [(evaluate_fitness(layout), layout) for layout in population]
    # Keep best-ever
    scored.sort(key=lambda x: x[0][0], reverse=True)
    if scored[0][0][0] > best_score:
        best_score = scored[0][0][0]
        best_solution = scored[0]
    # Elitism: carry top layouts forward
    next_pop = [layout for (_, layout) in scored[:elite_count]]
    # Fill rest by crossover + mutation
    while len(next_pop) < population_size:
        p1 = random.choice(population)
        p2 = random.choice(population)
        flat1 = sum(p1, ())
        flat2 = sum(p2, ())
        split = random.randint(1, len(flat1) - 1)
        child_flat = flat1[:split] + flat2[split:]
        child = [(child_flat[i], child_flat[i+1])
                 for i in range(0, len(child_flat), 2)]
        if random.random() < mutation_probability:
            idx = random.randrange(len(child))
            w, h = blocks[idx][1], blocks[idx][2]
            child[idx] = (random.randint(0, grid_size - w),
                          random.randint(0, grid_size - h))
        next_pop.append(child)
    population = next_pop

# --- Print only the final best result ---
(final_score, final_overlaps, final_wire, final_area), final_layout = best_solution

print("Best Fitness       :", final_score)
print("Overlap Count      :", final_overlaps)
print("Total Wire Length  :", round(final_wire, 2))
print("Bounding Box Area  :", final_area)
print("\nBest Placement (bottom-left coordinates):")
for (name, w, h), (x, y) in zip(blocks, final_layout):
    print(f"  {name:15} -> ({x:2}, {y:2})")
