import random
population_size = 100
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

origin_grid = grid
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
    grid_copy = [row[:] for row in grid] # Create a copy of the original grid
    grid_1, grid_2, grid_3 = change(grid_copy)
    pop.append(grid_1)
    pop2.append(grid_2)
    pop3.append(grid_3)
#print("########")
#print(pop[0])
#print("########")
def calculate_fitness(pop):
    fitness_values = []
    rows = [[len(set(x)) for x in subset] for subset in pop]
    columns = [[len(set(x)) for x in subset] for subset in pop2]
    box_grid = [[len(set(x)) for x in subset] for subset in pop3]
    #rows = [[len(set(x))/len(x) for x in subset] for subset in pop]
    #print(rows)
    rows = [sum(x)/len(x) for x in rows]
    #rows = [sum(x) for x in rows]
    columns = [sum(x)/len(x) for x in columns]
    box_grid = [sum(x)/len(x) for x in box_grid]

    for i in range(len(pop)):
        d = 3 * 9 # Sum of numbers from 1 to 9
        f = abs(rows[i] + columns[i] + box_grid[i])/d
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
    fitness_values = sorted(fitness_values, reverse=True)
    indices = sorted(range(len(fitness_values)), key=lambda i: fitness_values[i])[:10]
    selected_pop = [pop[i] for i in indices]
    selected_10 = selected_pop.copy()
    mate1 = selected_10[random.randint(0, 9)]
    mate2 = selected_10[random.randint(0, 9)]
    print(mate1,mate2)
    return mate1, mate2

def crossover(parent1, parent2):
    n = 4
    c_point = sorted(random.sample(range(1, 9), 4))
    c_point2 = sorted(random.sample(range(1, 9), 4))
    c_point3 = sorted(random.sample(range(1, 9), 4))

    gridc1 = [[parent2[i][j] if j in c_point else parent1[i][j] for j in range(len(parent1[i]))] for i in
                  range(len(parent1))]

    gridc2 = [[parent2[i][j] if j in c_point2 else parent1[i][j] for j in range(len(parent1[i]))] for i in
                  range(len(parent1))]
    gridc3 = [[parent2[i][j] if j in c_point3 else parent1[i][j] for j in range(len(parent1[i]))] for i in
                  range(len(parent1))]
    return gridc1, gridc2, gridc3

def mutate(list1):#changes the position of only 1 value
    if random.random() < 0.02:
        # Randomly select two different indices
        i1, j1, i2, j2 = random.sample(range(len(list1)), 4)

        # Swap the values at the selected indices
        list1[i1][j1], list1[i2][j2] = list1[i2][j2], list1[i1][j1]

    return list1


population = pop

for generation in range(generations):
    fitness_values = calculate_fitness(population)
    print(f"The average fitness value is {sum(fitness_values)/len(fitness_values)}!")
    if any(fit == 1 for fit in fitness_values):
        print(f"Solution found in generation {generation}!")
        dis(pop[fitness_values.index(0)])
        break

    new_population = []
    for _ in range(population_size // 3):
        parent1, parent2 = select_parents(pop, fitness_values)
        child1, child2, child3 = crossover(parent2, parent1)
        mutate(child1)
        mutate(child2)
        mutate(child3)
        new_population.extend([child1, child2,child3])

    population = new_population
