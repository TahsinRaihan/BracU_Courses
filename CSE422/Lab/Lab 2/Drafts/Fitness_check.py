import math

# ── 1) Block specs and netlist from the question ────────────
blocks = [
    ('ALU', 5, 5),
    ('Cache', 7, 4),
    ('Control Unit', 4, 4),
    ('Register File', 6, 6),
    ('Decoder', 5, 3),
    ('Floating Unit', 5, 5),
]
wired_pairs = [
    (3, 0),  # Register File ↔ ALU
    (2, 0),  # Control Unit ↔ ALU
    (0, 1),  # ALU ↔ Cache
    (3, 5),  # Register File ↔ Floating Unit
    (1, 4),  # Cache ↔ Decoder
    (4, 5),  # Decoder ↔ Floating Unit
]

# Penalty weights
ALPHA, BETA, GAMMA = 1000, 2, 1

# ── 2) Helper functions ────────────────────────────────────

def block_center(x, y, w, h):
    """Center point of a block from its bottom-left."""
    return (x + w/2, y + h/2)

def count_overlaps(layout):
    """Count how many block‐pairs overlap."""
    ov = 0
    for i in range(len(blocks)):
        x1, y1 = layout[i]
        w1, h1 = blocks[i][1], blocks[i][2]
        for j in range(i+1, len(blocks)):
            x2, y2 = layout[j]
            w2, h2 = blocks[j][1], blocks[j][2]
            # If rectangles intersect
            if not (x1+w1 <= x2 or x2+w2 <= x1 or y1+h1 <= y2 or y2+h2 <= y1):
                ov += 1
    return ov

def total_wire_length(layout):
    """Sum of distances between each wired pair’s centers."""
    total = 0.0
    for a, b in wired_pairs:
        cx1, cy1 = block_center(layout[a][0], layout[a][1], *blocks[a][1:])
        cx2, cy2 = block_center(layout[b][0], layout[b][1], *blocks[b][1:])
        total += math.hypot(cx1-cx2, cy1-cy2)
    return total

def bounding_box_area(layout):
    """Area of the smallest rectangle enclosing all blocks."""
    xs = [p[0] for p in layout]
    ys = [p[1] for p in layout]
    min_x, min_y = min(xs), min(ys)
    max_x = max(xs[i] + blocks[i][1] for i in range(len(layout)))
    max_y = max(ys[i] + blocks[i][2] for i in range(len(layout)))
    return (max_x - min_x) * (max_y - min_y)

def evaluate_fitness(layout):
    """
    Compute (fitness, overlaps, wire_length, area).
    Fitness = –(ALPHA*ov + BETA*wire + GAMMA*area)
    """
    ov   = count_overlaps(layout)
    wire = total_wire_length(layout)
    area = bounding_box_area(layout)
    score = -(ALPHA*ov + BETA*wire + GAMMA*area)
    return score, ov, wire, area

# ── 3) Sample layout P1 (from the PDF) ─────────────────────
P1 = [
    ( 9,  3),
    (12, 15),
    (13, 16),
    ( 1, 13),
    ( 4, 15),
    ( 9,  6),
]

# ── 4) Evaluate and print the Task 2 sample output ────────
fitness, overlaps, wiring, area = evaluate_fitness(P1)

print(f"Overlap count = {overlaps}")
print(f"Total wiring distance = {wiring:.1f}")
print(f"Bounding box area = {area}")
print(f"Fitness = {fitness:.2f}")
