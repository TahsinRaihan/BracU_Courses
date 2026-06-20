
import random
import math

## -----------------------------------------------------------------------------
## Global Parameters
## -----------------------------------------------------------------------------
GRID_DIMENSION = 25
POPULATION_SIZE = 6
MAX_ITERATIONS = 15
MUTATION_RATE = 0.08 # 8% mutation rate
NUM_ELITES = 1 # Number of elites to carry forward

# [cite_start]Component dimensions [cite: 8, 9]
COMPONENTS = {
    "ALU": {"width": 5, "height": 5},
    "Cache": {"width": 7, "height": 4},
    "Control Unit": {"width": 4, "height": 4},
    "Register File": {"width": 6, "height": 6},
    "Decoder": {"width": 5, "height": 3},
    "Floating Unit": {"width": 5, "height": 5},
}

COMPONENT_NAMES_ORDERED = [
    "ALU",
    "Cache",
    "Control Unit",
    "Register File",
    "Decoder",
    "Floating Unit",
]

# [cite_start]Required interconnections [cite: 11, 12, 13, 14, 15, 16]
INTERCONNECTIONS = [
    ("Register File", "ALU"),
    ("Control Unit", "ALU"),
    ("ALU", "Cache"),
    ("Register File", "Floating Unit"),
    ("Cache", "Decoder"),
    ("Decoder", "Floating Unit"),
]

# Fitness function weights
ALPHA = 1000  # Overlap penalty
BETA = 2    # Wiring length penalty
GAMMA = 1   # Bounding area penalty

## -----------------------------------------------------------------------------
## 1. Chromosome Representation / Encoding
## -----------------------------------------------------------------------------

def generate_random_chromosome():
    """
    Generates a single chromosome (a candidate layout) with random bottom-left coordinates.
    [cite_start]Each chromosome is a list of (x, y) tuples for the 6 components in the predefined order[cite: 86, 87].
    [cite_start]Coordinates are in the range [0, GRID_DIMENSION - component_dimension][cite: 91].
    """
    chromosome = []
    for comp_name in COMPONENT_NAMES_ORDERED:
        comp_info = COMPONENTS[comp_name]
        max_x = GRID_DIMENSION - comp_info["width"]
        max_y = GRID_DIMENSION - comp_info["height"]
        x = random.randint(0, max_x)
        y = random.randint(0, max_y)
        chromosome.append((x, y))
    return tuple(chromosome) # Ensure chromosome is a tuple

def generate_initial_population(size=POPULATION_SIZE):
    """
    [cite_start]Generates an initial population of chromosomes[cite: 93].
    """
    return [generate_random_chromosome() for _ in range(size)]

## -----------------------------------------------------------------------------
## Helper Functions for Fitness Calculation
## -----------------------------------------------------------------------------

def calculate_overlap(block1_coords, block1_dims, block2_coords, block2_dims):
    """
    Calculates the overlap between two blocks.
    [cite_start]Returns 1 if there's an overlap, 0 otherwise for penalty calculation[cite: 79].
    """
    x1, y1 = block1_coords
    w1, h1 = block1_dims["width"], block1_dims["height"]
    x2, y2 = block2_coords
    w2, h2 = block2_dims["width"], block2_dims["height"]

    # [cite_start]Calculate right, left, top, bottom for both blocks [cite: 83]
    A_left, A_bottom = x1, y1
    A_right, A_top = x1 + w1, y1 + h1
    B_left, B_bottom = x2, y2
    B_right, B_top = x2 + w2, y2 + h2

    # [cite_start]Check for overlap condition [cite: 80, 81, 82, 84]
    overlap = not (
        A_right <= B_left or
        A_left >= B_right or
        A_bottom >= B_top or
        A_top <= B_bottom
    )
    return 1 if overlap else 0

def calculate_total_overlaps(chromosome):
    """
    [cite_start]Calculates the total number of overlapping pairs in a given chromosome[cite: 76, 77].
    """
    total_overlaps = 0
    num_components = len(chromosome)
    for i in range(num_components):
        for j in range(i + 1, num_components):
            block1_name = COMPONENT_NAMES_ORDERED[i]
            block2_name = COMPONENT_NAMES_ORDERED[j]
            block1_coords = chromosome[i]
            block2_coords = chromosome[j]
            block1_dims = COMPONENTS[block1_name]
            block2_dims = COMPONENTS[block2_name]
            total_overlaps += calculate_overlap(
                block1_coords, block1_dims, block2_coords, block2_dims
            )
    return total_overlaps

def calculate_center(coords, dims):
    """
    Calculates the center (x, y) coordinates of a block.
    """
    x, y = coords
    width, height = dims["width"], dims["height"]
    center_x = x + width / 2
    center_y = y + height / 2
    return center_x, center_y

def calculate_euclidean_distance(point1, point2):
    """
    [cite_start]Calculates the Euclidean distance between two points[cite: 21, 35].
    """
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def calculate_total_wiring_distance(chromosome):
    """
    Calculates the total wiring distance for all specified interconnections.
    [cite_start]Wires run center-to-center between components[cite: 17, 34].
    """
    total_distance = 0.0
    component_positions = {
        name: chromosome[i] for i, name in enumerate(COMPONENT_NAMES_ORDERED)
    }

    for comp1_name, comp2_name in INTERCONNECTIONS:
        coords1 = component_positions[comp1_name]
        dims1 = COMPONENTS[comp1_name]
        coords2 = component_positions[comp2_name]
        dims2 = COMPONENTS[comp2_name]

        center1 = calculate_center(coords1, dims1)
        center2 = calculate_center(coords2, dims2)

        total_distance += calculate_euclidean_distance(center1, center2)
    return total_distance

def calculate_bounding_box_area(chromosome):
    """
    [cite_start]Calculates the area of the smallest bounding box enclosing all components[cite: 55, 56, 57].
    """
    min_x, min_y = GRID_DIMENSION, GRID_DIMENSION
    max_x, max_y = 0, 0

    for i, coords in enumerate(chromosome):
        block_name = COMPONENT_NAMES_ORDERED[i]
        dims = COMPONENTS[block_name]
        x, y = coords
        width, height = dims["width"], dims["height"]

        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x + width)
        max_y = max(max_y, y + height)

    bounding_box_width = max_x - min_x
    bounding_box_height = max_y - min_y
    return bounding_box_width * bounding_box_height

## -----------------------------------------------------------------------------
## 2. Fitness Function Implementation
## -----------------------------------------------------------------------------

def calculate_fitness(chromosome):
    """
    [cite_start]Calculates the fitness score for a given chromosome (layout) based on three objectives[cite: 95].
    A higher fitness value is better.
    Penalties are applied for overlaps, wiring distance, and bounding box area.
    [cite_start]Overlap counts are considered the least desirable and are penalized way more[cite: 97, 99].
    [cite_start]The total wiring distance and total bounding area are considered next[cite: 100].
    [cite_start]A weighted sum is used[cite: 102].
    """
    overlap_count = calculate_total_overlaps(chromosome)
    wiring_distance = calculate_total_wiring_distance(chromosome)
    bounding_area = calculate_bounding_box_area(chromosome)

    # Fitness is negatively proportional to penalties.
    # We negate the sum of weighted penalties because we want to maximize fitness,
    # but the objectives are to minimize these values.
    fitness_value = - (ALPHA * overlap_count + BETA * wiring_distance + GAMMA * bounding_area)
    return fitness_value, overlap_count, wiring_distance, bounding_area

## -----------------------------------------------------------------------------
## 3. Parent Selection
## -----------------------------------------------------------------------------

def select_parents(population):
    """
    [cite_start]Selects two parents randomly from the population[cite: 105].
    """
    parent1 = random.choice(population)
    parent2 = random.choice(population)
    return parent1, parent2

## -----------------------------------------------------------------------------
## 4. Crossover
## -----------------------------------------------------------------------------

def single_point_crossover(parent1, parent2):
    """
    [cite_start]Performs single-point crossover on two parents to create two offspring[cite: 108, 109].
    """
    # [cite_start]Pick a random split point [cite: 109]
    crossover_point = random.randint(1, len(parent1) - 1)

    # Convert to list for concatenation, then back to tuple
    offspring1 = tuple(list(parent1[:crossover_point]) + list(parent2[crossover_point:]))
    offspring2 = tuple(list(parent2[:crossover_point]) + list(parent1[crossover_point:]))
    return offspring1, offspring2

## -----------------------------------------------------------------------------
## 5. Mutation
## -----------------------------------------------------------------------------

def mutate(chromosome):
    """
    [cite_start]Applies mutation to a chromosome with a given probability[cite: 111, 112].
    [cite_start]Picks any arbitrary component block and introduces random coordinate (x, y) changes to that single particular block with a low probability (5-10% mutation rate)[cite: 113].
    """
    if random.random() < MUTATION_RATE:
        # [cite_start]Pick a random component block to mutate [cite: 113]
        component_index = random.randint(0, len(chromosome) - 1)
        component_name = COMPONENT_NAMES_ORDERED[component_index]
        comp_info = COMPONENTS[component_name]

        # [cite_start]Introduce random coordinate (x, y) changes [cite: 113]
        max_x = GRID_DIMENSION - comp_info["width"]
        max_y = GRID_DIMENSION - comp_info["height"]
        new_x = random.randint(0, max_x)
        new_y = random.randint(0, max_y)

        mutated_chromosome = list(chromosome) # Convert to list to modify
        mutated_chromosome[component_index] = (new_x, new_y)
        return tuple(mutated_chromosome) # Convert back to tuple
    return chromosome

## -----------------------------------------------------------------------------
## 6. New Generation Creation
## -----------------------------------------------------------------------------

def create_new_generation(population, fitness_scores):
    """
    Creates a new generation using elitism and selecting from offspring.
    [cite_start]The population size should be the same for all generations[cite: 115].
    """
    # Sort population by fitness in descending order
    sorted_population = sorted(
        zip(population, fitness_scores), key=lambda x: x[1][0], reverse=True
    )

    new_population = []

    # [cite_start]Apply elitism: carry forward the best individuals [cite: 116]
    for i in range(NUM_ELITES):
        new_population.append(sorted_population[i][0])

    # [cite_start]Fill the rest of the population with offspring [cite: 117]
    num_offspring_needed = POPULATION_SIZE - NUM_ELITES
    offspring = []

    while len(offspring) < num_offspring_needed:
        parent1, parent2 = select_parents([chromo for chromo, _ in sorted_population])
        child1, child2 = single_point_crossover(parent1, parent2)

        child1 = mutate(child1)
        child2 = mutate(child2)

        offspring.append(child1)
        if len(offspring) < num_offspring_needed:
            offspring.append(child2)

    new_population.extend(offspring)
    return new_population

## -----------------------------------------------------------------------------
## 7. GA Loop
## -----------------------------------------------------------------------------

def run_genetic_algorithm():
    """
    [cite_start]Runs the genetic algorithm simulation until the best fitness (a plateau) is achieved or the maximum number of 15 iterations is reached[cite: 120].
    """
    population = generate_initial_population()
    best_overall_fitness = float('-inf')
    best_overall_chromosome = None
    best_overall_metrics = None

    print("Starting Genetic Algorithm...\n")

    for generation in range(MAX_ITERATIONS): # Run for a maximum number of iterations
        # Calculate fitness for the current population
        fitness_results = [calculate_fitness(chromo) for chromo in population]

        # Find the best chromosome in the current generation
        current_best_fitness_idx = 0
        for i, result in enumerate(fitness_results):
            if result[0] > fitness_results[current_best_fitness_idx][0]:
                current_best_fitness_idx = i

        current_best_chromosome = population[current_best_fitness_idx]
        current_best_fitness, current_overlap, current_wiring, current_bounding = fitness_results[current_best_fitness_idx]

        print(f"--- Generation {generation + 1} ---")
        print(f"Current Best Fitness: {current_best_fitness:.2f}")
        print(f"  Overlaps: {current_overlap}")
        print(f"  Wiring Distance: {current_wiring:.2f}")
        print(f"  Bounding Area: {current_bounding}")
        print(f"  Chromosome: {current_best_chromosome}")
        print("-" * 30)

        # Update overall best
        if current_best_fitness > best_overall_fitness:
            best_overall_fitness = current_best_fitness
            best_overall_chromosome = current_best_chromosome
            best_overall_metrics = (current_overlap, current_wiring, current_bounding)

        # Create new generation
        population = create_new_generation(population, fitness_results)

    print("\nGenetic Algorithm Finished.")
    return best_overall_chromosome, best_overall_fitness, best_overall_metrics

## -----------------------------------------------------------------------------
## 8. Required Output
## -----------------------------------------------------------------------------

if __name__ == "__main__":
    best_chromosome, best_fitness, best_metrics = run_genetic_algorithm()

    print("\n" + "="*40)
    print("Optimal Placement Strategy Found:")
    print("="*40)
    print(f"Best Total Fitness Value: {best_fitness:.2f}")
    if best_metrics:
        total_overlap_counts, total_wiring_length, total_bounding_box_area = best_metrics
        print(f"Total Overlap Counts: {total_overlap_counts}")
        print(f"Total Wiring Length: {total_wiring_length:.2f}")
        print(f"Total Bounding Box Area: {total_bounding_box_area}")

    print("\nOptimal Placement (Bottom-Left Coordinates):")
    if best_chromosome:
        for i, comp_name in enumerate(COMPONENT_NAMES_ORDERED):
            print(f"  {comp_name}: {best_chromosome[i]}")
