import random
import math

# ── 1) Make randomness repeatable ────────────────────────────
random.seed(42)

# ── 2) Define the chip layout problem ───────────────────────
GRID_SIZE = 25

# Each block: (name, width, height)
block_defs = [
    ('ALU',          5, 5),
    ('Cache',        7, 4),
    ('Control Unit', 4, 4),
    ('Register File',6, 6),
    ('Decoder',      5, 3),
    ('Floating Unit',5, 5),
]

# Which pairs of block‐indices need wires between them
net_connections = [
    (3, 0),  # Register File ↔ ALU
    (2, 0),  # Control Unit ↔ ALU
    (0, 1),  # ALU ↔ Cache
    (3, 5),  # Register File ↔ Floating Unit
    (1, 4),  # Cache ↔ Decoder
    (4, 5),  # Decoder ↔ Floating Unit
]

# ── 3) GA parameters ─────────────────────────────────────────
population_size = 6
num_elites      = 2     # how many top layouts to carry over
mutation_rate   = 0.10  # 10% chance per child
generations     = 15

# Fitness penalty weights
alpha = 1000
beta    = 2
gamma  = 1

# ── 4) Helper functions ─────────────────────────────────────

def block_center(x, y, w, h):
    """Return the center (cx, cy) of a block from its bottom-left (x,y)."""
    return (x + w/2, y + h/2)

def compute_overlaps(layout):
    """Count how many block-pairs overlap in this layout."""
    count = 0
    for i in range(len(block_defs)):
        x1, y1 = layout[i]
        w1, h1 = block_defs[i][1], block_defs[i][2]
        for j in range(i+1, len(block_defs)):
            x2, y2 = layout[j]
            w2, h2 = block_defs[j][1], block_defs[j][2]
            if not (x1+w1 <= x2 or x2+w2 <= x1 or y1+h1 <= y2 or y2+h2 <= y1):
                count += 1
    return count

def compute_wire_length(layout):
    """Sum Euclidean distances between centers of each wired pair."""
    total = 0.0
    for a, b in net_connections:
        cx1, cy1 = block_center(layout[a][0], layout[a][1], *block_defs[a][1:])
        cx2, cy2 = block_center(layout[b][0], layout[b][1], *block_defs[b][1:])
        total += math.hypot(cx1 - cx2, cy1 - cy2)
    return total

def compute_bounding_area(layout):
    """Compute the area of the smallest rectangle enclosing all blocks."""
    xs = [pos[0] for pos in layout]
    ys = [pos[1] for pos in layout]
    min_x, min_y = min(xs), min(ys)
    max_x = max(xs[i] + block_defs[i][1] for i in range(len(layout)))
    max_y = max(ys[i] + block_defs[i][2] for i in range(len(layout)))
    return (max_x - min_x) * (max_y - min_y)

def compute_fitness(layout):
    """
    Return (score, overlaps, wire_length, area).
    Score is negative weighted sum, so higher is better.
    """
    ov  = compute_overlaps(layout)
    wl  = compute_wire_length(layout)
    ar  = compute_bounding_area(layout)
    score = -(alpha*ov + beta*wl + gamma*ar)
    return (score, ov, wl, ar)

def random_layout():
    """Generate a random layout: bottom-left (x,y) for each block."""
    layout = []
    for _, w, h in block_defs:
        x = random.randint(0, GRID_SIZE - w)
        y = random.randint(0, GRID_SIZE - h)
        layout.append((x, y))
    return layout

def two_point_crossover(parent1, parent2):
    """
    Perform two-point crossover on two parents.
    Returns two children.
    """
    flat1 = sum(parent1, ())
    flat2 = sum(parent2, ())
    cut1, cut2 = sorted(random.sample(range(1, len(flat1)), 2))
    child1_flat = flat1[:cut1] + flat2[cut1:cut2] + flat1[cut2:]
    child2_flat = flat2[:cut1] + flat1[cut1:cut2] + flat2[cut2:]
    def rebuild(flat):
        return [(flat[i], flat[i+1]) for i in range(0, len(flat), 2)]
    return rebuild(child1_flat), rebuild(child2_flat)

# ── 5) Initialize with a random population ─────────────────
population = [random_layout() for _ in range(population_size)]
best_overall = None  # will hold ((score,ov,wl,ar), layout)

# ── 6) GA main loop ─────────────────────────────────────────
for _ in range(generations):
    # a) Evaluate fitness of each individual
    scored = [(compute_fitness(layout), layout) for layout in population]
    # b) Sort by score descending
    scored.sort(key=lambda x: x[0][0], reverse=True)
    # c) Track the best ever
    if best_overall is None or scored[0][0][0] > best_overall[0][0]:
        best_overall = scored[0]
    # d) Elitism: carry over top num_elites layouts
    next_pop = [layout for (_, layout) in scored[:num_elites]]
    # e) Fill the rest with two-point offspring and mutation
    while len(next_pop) < population_size:
        mom = random.choice(population)
        dad = random.choice(population)
        child1, child2 = two_point_crossover(mom, dad)
        # mutate child1
        if random.random() < mutation_rate:
            idx = random.randrange(len(child1))
            w, h = block_defs[idx][1], block_defs[idx][2]
            child1[idx] = (
                random.randint(0, GRID_SIZE - w),
                random.randint(0, GRID_SIZE - h)
            )
        # mutate child2
        if len(next_pop) + 1 < population_size and random.random() < mutation_rate:
            idx = random.randrange(len(child2))
            w, h = block_defs[idx][1], block_defs[idx][2]
            child2[idx] = (
                random.randint(0, GRID_SIZE - w),
                random.randint(0, GRID_SIZE - h)
            )
        next_pop.append(child1)
        if len(next_pop) < population_size:
            next_pop.append(child2)
    population = next_pop

# ── 7) Final best solution report ───────────────────────────
(score, overlaps, wire_len, area), best_layout = best_overall

print("Best Fitness       :", score)
print("Overlap Count      :", overlaps)
print("Total Wire Length  :", round(wire_len, 2))
print("Bounding Box Area  :", area)
print("\nBest Placement (bottom-left coordinates):")
for (name, _, _), (x, y) in zip(block_defs, best_layout):
    print(f"  {name:15} -> ({x:2}, {y:2})")
