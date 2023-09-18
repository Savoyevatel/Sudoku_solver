import random

z = 9
grid = [[0 for i in range(z)] for j in range(z)]
with open("sudoku.txt", "r") as f:
    c = 0
    for i in range(z):
        row = f.readline().split()
        for j in range(z):
            grid[i][j] = int(row[j])
            if grid[i][j] == 0:
                c += 1

def dis(a):
    print("The solution is!")
    for i in range(z):
        for j in range(z):
            print(a[i][j], end="   ")
        print("\n")
        print()

def change(grid): #randomizes new values for each epoch grid1 is row, grid2 is column and grid 3 is 3x3 grid
    grid_1 = [row[:] for row in grid] 
    grid_2 = [[grid_1[j][i] for j in range(z)] for i in range(z)]
    grid_3 = []
    for i in range(0, len(grid_1), 3):
        temp_lists = [[], [], []]
        for j in range(i, i + 3):
            sublist = grid_1[j]

            for k in range(3):
                start_index = k * 3
                end_index = start_index + 3
                temp_lists[k] += sublist[start_index:end_index]

        grid_3.extend(temp_lists)
    for row in grid_1:
        empty_cells = [i for i, cell in enumerate(row) if cell == 0]
        random.shuffle(empty_cells)
        values = list(range(1, 10))
        for cell_index in empty_cells:
            value = random.choice(values)
            row[cell_index] = value
            values.remove(value)
    return grid_1, grid_2, grid_3
def calculate_fitness(grid):
    grid_1, grid_2, grid_3 = change(grid)
    a = [sum(row) for row in grid_1] 
    b = [sum(col) for col in grid_2] 
    c = [sum(col) for col in grid_3]
    d = 3 * 45 # Sum of numbers from 1 to 9
    fitness_values = [abs(a[i] + b[i] + c[i] - d) for i in range(z)]
    return sum(fitness_values)/z

def generate_individual():
    return grid

def correct(grids, rows, col, num):
    # Check if 'num' is not in the current row, column, or 3x3 box
    for i in range(z):
        if (grids[rows][i] == num) or (grids[i][col] == num) or (grids[rows - rows % 3 + i // 3][col - col % 3 + i % 3]
                                                                 == num):
            return False
    return True

def select_parents(population, fitness_values):
    print(fitness_values)
    total_fitness = sum(fitness_values)/population_size
    roulette_value = random.uniform(0, total_fitness)
    cumulative_fitness = 0
    for i, fit in enumerate(fitness_values):
        cumulative_fitness += fit
        if cumulative_fitness >= roulette_value:
            parent1 = population[i]
            break
    while True:
        roulette_value = random.uniform(0, total_fitness)
        cumulative_fitness = 0
        for i, fit in enumerate(fitness_values):
            cumulative_fitness += fit
            if cumulative_fitness >= roulette_value:
                parent2 = population[i]
                break
        if parent1 != parent2:
            return parent1, parent2

def crossover(parent1, parent2):
    half_len = len(parent1) // 2
    gridc1 = parent1[:half_len] + parent2[half_len:]

    random.shuffle(parent1)
    random.shuffle(parent2)
    gridc2 = parent1[:len(parent1) // 2] + parent2[len(parent2) // 2:]
    random.shuffle(parent1)
    random.shuffle(parent2)
    gridc3 = parent1[:len(parent1) // 2] + parent2[len(parent2) // 2:]
    return gridc1, gridc2, gridc3

def mutate(individual):#changes the position of only 1 value
    row1, col1 = random.randint(0, 8), random.randint(0, 8)
    row2, col2 = random.randint(0, 8), random.randint(0, 8)

    # Swap the values at the chosen positions
    individual[row1][col1], individual[row2][col2] = individual[row2][col2], individual[row1][col1]
    return individual

population_size = 100
#mutation_rate = 0.01 no longer used
generations = 1000

population = [generate_individual() for _ in range(population_size)]

for generation in range(generations):
    fitness_values = [calculate_fitness(ind) for ind in population]
    print(fitness_values)
    print(f"The average fitness value is {sum(fitness_values)/population_size}!")
    if any(fit == 0 for fit in fitness_values):
        print(f"Solution found in generation {generation}!")
        dis(population[fitness_values.index(0)])
        break

    new_population = []
    for _ in range(population_size // 2):
        parent1, parent2 = select_parents(population, fitness_values)
        child1, child2, child3 = crossover(parent2, parent1)
        mutate(child1)
        mutate(child2)
        mutate(child3)
        new_population.extend([child1, child2])

    population = new_population
