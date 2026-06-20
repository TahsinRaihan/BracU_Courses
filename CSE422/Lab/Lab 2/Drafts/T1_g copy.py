import random
import math

# Fix the random seed so every run is identical
random.seed(42)

# --- Problem definition ---
GRID_SIZE = 25
BLOCKS = [
    ('ALU', 5, 5),
    ('Cache', 7, 4),
    ('Control Unit', 4, 4),
    ('Register File', 6, 6),
    ('Decoder', 5, 3),
    ('Floating Unit', 5, 5),
]

# Each tuple says “draw a wire between block i and block j”
NET_PAIRS = [
    (3, 0),  # Register File → ALU
    (2, 0),  # Control Unit → ALU
    (0, 1),  # ALU → Cache
    (3, 5),  # Register File → Floating Unit
    (1, 4),  # Cache → Decoder
    (4, 5),  # Decoder → Floating Unit
]

# --- Genetic Algorithm settings ---
POPULATION_SIZE = 6
ELITE_COUNT     = 2     # number of top layouts to carry over each generation
MUTATION_RATE   = 0.10  # 10% chance to mutate a child
GENERATIONS     = 15

# Fitness weights (higher = more important to avoid)
WEIGHT_OVERLAP  = 1000
WEIGHT_WIRE     = 2
WEIGHT_AREA     = 1


# --- Helper functions ---

def block_center(pos, width, height):
    """Return (x,y) center from bottom-left pos and size."""
    return (pos[0] + width/2, pos[1] + height/2)


def count_overlaps(layout):
    """Count how many pairs of blocks overlap."""
    overlaps = 0
    for i in range(len(BLOCKS)):
        xi, yi = layout[i]
        wi, hi = BLOCKS[i][1], BLOCKS[i][2]
        for j in range(i+1, len(BLOCKS)):
            xj, yj = layout[j]
            wj, hj = BLOCKS[j][1], BLOCKS[j][2]
            # check for rectangle overlap
            if not (xi+wi <= xj or xj+wj <= xi or yi+hi <= yj or yj+hj <= yi):
                overlaps += 1
    return overlaps


def total_wire_length(layout):
    """Sum of Euclidean distances between centers of required nets."""
    length = 0.0
    for a, b in NET_PAIRS:
        ca = block_center(layout[a], *BLOCKS[a][1:])
        cb = block_center(layout[b], *BLOCKS[b][1:])
        dx, dy = ca[0] - cb[0], ca[1] - cb[1]
        length += math.hypot(dx, dy)
    return length


def bounding_box_area(layout):
    """Area of smallest rectangle enclosing all blocks."""
    xs = [p[0] for p in layout]
    ys = [p[1] for p in layout]
    max_x = max(xs[i] + BLOCKS[i][1] for i in range(len(layout)))
    max_y = max(ys[i] + BLOCKS[i][2] for i in range(len(layout)))
    min_x = min(xs)
    min_y = min(ys)
    return (max_x - min_x) * (max_y - min_y)


def evaluate_fitness(layout):
    """
    Compute fitness = negative weighted sum of:
      1) number of overlaps
      2) total wire length
      3) bounding-box area
    """
    ov   = count_overlaps(layout)
    wl   = total_wire_length(layout)
    area = bounding_box_area(layout)
    penalty = WEIGHT_OVERLAP * ov + WEIGHT_WIRE * wl + WEIGHT_AREA * area
    return -penalty, ov, wl, area


def random_layout():
    """Generate one layout: random bottom-left (x,y) for each block."""
    layout = []
    for _, w, h in BLOCKS:
        x = random.randint(0, GRID_SIZE - w)
        y = random.randint(0, GRID_SIZE - h)
        layout.append((x, y))
    return layout


# --- Initialize population ---
population = [random_layout() for _ in range(POPULATION_SIZE)]
best_overall_fitness = -math.inf
best_overall_solution = None

# --- Main GA loop ---
for generation in range(1, GENERATIONS + 1):

    # 1) Score and sort the current population
    scored = [(evaluate_fitness(ind), ind) for ind in population]
    scored.sort(key=lambda x: x[0][0], reverse=True)

    # 2) Print this generation’s results
    print(f"\nGeneration {generation}:")
    for rank, ((fit, ov, wl, ar), layout) in enumerate(scored, start=1):
        print(f"  {rank:>2}. fit={fit:8.2f}  overlaps={ov} "
              f"wire={wl:6.2f}  area={ar}")

    # 3) Update all-time best if improved
    top_fit, top_ov, top_wl, top_ar = scored[0][0]
    if top_fit > best_overall_fitness:
        best_overall_fitness = top_fit
        best_overall_solution = scored[0]
        print("    -> New best so far!")

    # 4) Keep the top ELITE_COUNT layouts unchanged
    next_generation = [layout for (_, layout) in scored[:ELITE_COUNT]]

    # 5) Fill the rest of the population with children
    while len(next_generation) < POPULATION_SIZE:
        # pick two parents at random
        p1 = random.choice(population)
        p2 = random.choice(population)

        # flatten and do single-point crossover
        flat1, flat2 = sum(p1, ()), sum(p2, ())
        split = random.randint(1, len(flat1)-1)
        child_flat = flat1[:split] + flat2[split:]

        # rebuild (x,y) pairs
        child = [(child_flat[i], child_flat[i+1])
                 for i in range(0, len(child_flat), 2)]

        # mutation: randomly move one block
        if random.random() < MUTATION_RATE:
            idx = random.randrange(len(child))
            w, h = BLOCKS[idx][1], BLOCKS[idx][2]
            child[idx] = (
                random.randint(0, GRID_SIZE - w),
                random.randint(0, GRID_SIZE - h)
            )

        next_generation.append(child)

    # move to the next generation
    population = next_generation

# --- Final best solution report ---
(fit_score, ov_count, wire_len, box_area), best_layout = best_overall_solution

print("\n" + "="*40)
print("Best layout overall:")
print(f"  Fitness     = {fit_score:.2f}")
print(f"  Overlaps    = {ov_count}")
print(f"  Wire length = {wire_len:.2f}")
print(f"  Area        = {box_area}")
print("  Block positions (bottom-left):")
for (name, w, h), (x, y) in zip(BLOCKS, best_layout):
    print(f"    {name:15} at ({x:2}, {y:2})")
