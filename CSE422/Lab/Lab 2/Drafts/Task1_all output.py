import random
import math

grid_size = 25
blocks = [
    ('ALU', 5, 5),
    ('Cache', 7, 4),
    ('Control Unit', 4, 4),
    ('Register File', 6, 6),
    ('Decoder', 5, 3),
    ('Floating Unit', 5, 5),
]

# Required interconnections (nets)
nets = [
    (3, 0),  # Register File → ALU
    (2, 0),  # Control Unit → ALU
    (0, 1),  # ALU → Cache
    (3, 5),  # Register File → Floating Unit
    (1, 4),  # Cache → Decoder
    (4, 5),  # Decoder → Floating Unit
]

# GA parameters
pop_size       = 6
alpha, beta, gamma = 1000, 2, 1    # fitness weights
mutation_rate  = 0.1
generations    = 15
elitism_count  = 2

random.seed(42)

def center(coord, w, h):
    return (coord[0] + w/2, coord[1] + h/2)

def count_overlaps(chrom):
    overlaps = 0
    for i in range(len(blocks)):
        xi, yi = chrom[i]
        wi, hi = blocks[i][1], blocks[i][2]
        for j in range(i+1, len(blocks)):
            xj, yj = chrom[j]
            wj, hj = blocks[j][1], blocks[j][2]
            if not (xi+wi <= xj or xj+wj <= xi or yi+hi <= yj or yj+hj <= yi):
                overlaps += 1
    return overlaps

def total_wire_length(chrom):
    length = 0
    for a, b in nets:
        ca = center(chrom[a], blocks[a][1], blocks[a][2])
        cb = center(chrom[b], blocks[b][1], blocks[b][2])
        length += math.hypot(ca[0]-cb[0], ca[1]-cb[1])
    return length

def bounding_box_area(chrom):
    xs = [c[0] for c in chrom]
    ys = [c[1] for c in chrom]
    x_max = max(xs[i] + blocks[i][1] for i in range(len(chrom)))
    y_max = max(ys[i] + blocks[i][2] for i in range(len(chrom)))
    return (x_max - min(xs)) * (y_max - min(ys))

def fitness(chrom):
    ov   = count_overlaps(chrom)
    wire = total_wire_length(chrom)
    area = bounding_box_area(chrom)
    score = -(alpha*ov + beta*wire + gamma*area)
    return score, ov, wire, area

def random_chromosome():
    return [(random.randint(0, grid_size-w),
             random.randint(0, grid_size-h))
            for (_, w, h) in blocks]

# Initialize
population = [random_chromosome() for _ in range(pop_size)]
best_score = -math.inf
best_solution = None

for gen in range(1, generations+1):
    # Evaluate & sort
    scored = [(fitness(ch), ch) for ch in population]
    scored.sort(key=lambda x: x[0][0], reverse=True)
    
    # Print every candidate this generation
    print(f"\n=== Generation {gen} Candidates ===")
    for rank,( (sc, ov, wi, ar), ch ) in enumerate(scored, start=1):
        print(f"#{rank:>2}  fitness={sc:8.2f} | overlaps={ov:1d} | wire={wi:6.2f} | area={ar:4d} | coords={ch}")
    
    # Track overall best
    top_score, top_ov, top_wire, top_area = scored[0][0]
    if top_score > best_score:
        best_score = top_score
        best_solution = scored[0]
        print(f"--> New overall best at Gen {gen}: fitness={top_score:.2f}, overlaps={top_ov}, wire={top_wire:.2f}, area={top_area}")
    
    # Elitism
    next_gen = [ch for (_,ch) in scored[:elitism_count]]
    # Offspring
    while len(next_gen) < pop_size:
        p1 = random.choice(population)
        p2 = random.choice(population)
        flat1, flat2 = sum(p1,()), sum(p2,())
        pt = random.randint(1, len(flat1)-1)
        child_flat = flat1[:pt] + flat2[pt:]
        child = [(child_flat[i], child_flat[i+1]) 
                 for i in range(0, len(child_flat), 2)]
        if random.random() < mutation_rate:
            bi = random.randrange(len(child))
            w, h = blocks[bi][1], blocks[bi][2]
            child[bi] = (random.randint(0, grid_size-w),
                         random.randint(0, grid_size-h))
        next_gen.append(child)
    
    population = next_gen

# Final report
(score, ov, wi, ar), best_chrom = best_solution
print("\n" + "="*40)
print(" FINAL BEST SOLUTION")
print("="*40)
print(f"Fitness: {score:.2f} | Overlaps: {ov} | Wire: {wi:.2f} | Area: {ar}")
for (name, w, h), (x, y) in zip(blocks, best_chrom):
    print(f"  {name:15} -> ({x:2},{y:2})")
