import random
import math
grid_size = 25
blocks = [('ALU', 5, 5),('Cache', 7, 4),('Control Unit', 4, 4),('Register File', 6, 6),('Decoder', 5, 3),('Floating Unit', 5, 5),]

nets = [
    (3, 0),  # Register File to ALU
    (2, 0),  # Control Unit to ALU
    (0, 1),  # ALU to Cache
    (3, 5),  # Register File to Floating Unit
    (1, 4),  # Cache To Decoder
    (4, 5),  # Decoder to Floating Unit
]

pop_size = 6
alpha= 1000  #bigger value because we dont want any Overlaps
beta = 2    # smaller valu for wire length
gamma = 1
mutation_rate = 0.1
generations = 15
elitism_count = 2

#random.seed(42) #For testing

def center(cord, w, h): # To get cnter of a block
    x, y = cord
    return x + w / 2, y + h / 2

def count_overlaps(chrom):
    overlaps = 0
    for i in range(len(blocks)):
        xi, yi = chrom[i]
        wi, hi = blocks[i][1], blocks[i][2]
        for j in range(i+1, len(blocks)):
            xj, yj = chrom[j]
            wj, hj = blocks[j][1], blocks[j][2]
            # if they overlap
            if not (xi + wi <= xj or xj + wj <= xi or yi + hi <= yj or yj + hj <= yi):
                overlaps += 1
    return overlaps

def total_wire_length(chrom):
    length = 0
    for a, b in nets:
        ca = center(chrom[a], blocks[a][1], blocks[a][2])
        cb = center(chrom[b], blocks[b][1], blocks[b][2])
        length += math.hypot(ca[0] - cb[0], ca[1] - cb[1])
    return length

def bounding_box_area(chrom): #, calculate area of bounding box
    x_min = min(x for x, y in chrom)
    y_min = min(y for x, y in chrom)
    x_max = max(x + blocks[i][1] for i, (x, y) in enumerate(chrom))
    y_max = max(y + blocks[i][2] for i, (x, y) in enumerate(chrom))
    return (x_max - x_min) * (y_max - y_min)

def fitness(chrom):
    ov = count_overlaps(chrom)
    wire = total_wire_length(chrom)
    area = bounding_box_area(chrom)
    score = -(alpha * ov + beta * wire + gamma * area) # negative because  minimizing overlaps, wire, area
    return score, ov, wire, area

def random_chromosome(): #generating a random chromosome
    chrom = []
    for name, weidth, height in blocks:
        x = random.randint(0, grid_size - weidth)
        y = random.randint(0, grid_size - height)
        chrom.append((x, y))
    return chrom

#genetic algo

population = [random_chromosome() for i in range(pop_size)] # 15 iterations
best_score = -math.inf
best_solution = None

for gen in range(1, generations + 1): # Evaluate fitness
    scored = [(fitness(ch), ch) for ch in population]
    scored.sort(key=lambda item: item[0][0], reverse=True)  # sort by fitness desc

    if scored[0][0][0] > best_score: # if Its better then update
        best_score = scored[0][0][0]
        best_solution = scored[0]

    next_gen = [ch for (j, ch) in scored[:elitism_count]]  #top 2 layouts goes into the next generation

    while len(next_gen) < pop_size: #geneate child until populaton
        p1 = random.choice(population)
        p2 = random.choice(population) # 2 random parent

        flat1 = sum(p1, ())  #Crossover
        flat2 = sum(p2, ())

        point = random.randint(1, len(flat1) - 1)
        child_flat = flat1[:point] + flat2[point:]

        child = [(child_flat[i], child_flat[i+1]) for i in range(0, len(child_flat), 2)] # Re bulding the chuld into 6 point pair

        if random.random() < mutation_rate: #mutation
            bi = random.randrange(len(child))
            weidth, height = blocks[bi][1], blocks[bi][2]
            child[bi] = (random.randint(0, grid_size - weidth), random.randint(0, grid_size - height))
        next_gen.append(child)

    population = next_gen



(best_fit, best_ov, best_wire, best_area), best_chrom = best_solution # best solution

print("Best Fitness       :", best_fit)
print("Overlap Count      :", best_ov)
print("Total Wire Length  :", round(best_wire, 2))
print("Bounding Box Area  :", best_area)
print("\nBest Placement (bottom-left coordinates): ")
for (name, weidth, height), (x, y) in zip(blocks, best_chrom):
    print(f"  {name:15} -> ({x:2}, {y:2})")
