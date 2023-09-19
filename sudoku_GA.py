import random
population_size = 100
#mutation_rate = 0.01 no longer used
generations = 1000

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


def change(list1):
    for sublist in list1:
        list2 = [x + 1 for x in range(z) if x + 1 not in sublist]
        random.shuffle(list2)

        for i in range(len(sublist)):
            if sublist[i] == 0 and list2:
                sublist[i] = list2.pop()
    grid_1 = list1
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

    return grid_1, grid_2, grid_3

pop = []
pop2 = []
pop3 = []
for i in range(population_size):
    grid_copy = [row[:] for row in grid]  # Create a copy of the original grid
    grid_1, grid_2, grid_3 = change(grid_copy)
    pop.append(grid_1)
    pop2.append(grid_2)
    pop3.append(grid_3)

def calculate_fitness(pop):
    fitness_values = []
    rows = [[sum(subsublist) for subsublist in sublist] for sublist in pop]
    columns = [[sum(subsublist) for subsublist in sublist] for sublist in pop2]
    box_grid = [[sum(subsublist) for subsublist in sublist] for sublist in pop3]
    print(rows[0])
    print(columns[0])
    print(box_grid[0])

    for i in range(len(pop)):
        d = 3 * 45 # Sum of numbers from 1 to 9
        f = abs(rows[i] + columns[i] + box_grid[i] - d)
        fitness_values.append(f)
    return fitness_values
fitness_values = (calculate_fitness(pop))

def correct(grids, rows, col, num):
    # Check if 'num' is not in the current row, column, or 3x3 box
    for i in range(z):
        if (grids[rows][i] == num) or (grids[i][col] == num) or (grids[rows - rows % 3 + i // 3][col - col % 3 + i % 3]
                                                                 == num):
            return False
    return True

def select_parents(pop, fitness_values):
    fitness_values = sorted(fitness_values)
    pop = fitness_values[:10]
    selected_pop = [pop[i] for i in pop]
    selected_pop = selected_pop.copy()
    for x in selected_pop:
        mate1 = selected_pop[random.randint(0, len(selected_pop) - 1)]
        mate2 = selected_pop[random.randint(0, len(selected_pop) - 1)]
    return mate1, mate2

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

population = pop

for generation in range(generations):
    fitness_values = [calculate_fitness(ind) for ind in pop]
    print(f"The average fitness value is {sum(fitness_values)}!")
    if any(fit == 0 for fit in fitness_values):
        print(f"Solution found in generation {generation}!")
        dis(pop[fitness_values.index(0)])
        break

    new_population = []
    for _ in range(population_size // 2):
        parent1, parent2 = select_parents(pop, fitness_values)
        child1, child2, child3 = crossover(parent2, parent1)
        print(child1)
        print(child1)
        mutate(child1)
        mutate(child2)
        mutate(child3)
        new_population.extend([child1, child2])

    population = new_population
