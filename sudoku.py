z = 9 #your signature

grid = [[0 for i in range(z)] for j in range(z)]
with open("sudoku.txt", "r") as f:
    c = 0
    for i in range(z):
        row = f.readline().split()
        for j in range(z):
            grid[i][j] = int(row[j])
            if grid[i][j] == 0:
                c += 1


grid_2 = []
for j in range(9):
    row = []
    for i in range(9):
        row.append(grid[j][i])
    grid_2.append(row)


def check_duplicates(lst):
    for sub_list in lst:
        seen = set()
        for item in sub_list:
            if item != 0:
                if item in seen:
                    return True
                seen.add(item)
    return False


grid3 = []
for i in range(0, len(grid), 3):
    temp_lists = [[], [], []]
    for j in range(i, i + 3):
        sublist = grid[j]

        for k in range(3):
            start_index = k * 3
            end_index = start_index + 3
            temp_lists[k] += sublist[start_index:end_index]

    grid3.extend(temp_lists)


def dis(a):
    print("The solution is!")
    for i in range(z):
        for j in range(z):
            print(a[i][j], end="   ")
        print("\n")
        print()


def check(a, l):
    zero = 1
    for i in range(z):
        for j in range(z):
            if a[i][j] == 0:
                l[0] = i
                l[1] = j
                return True
    return False


def correct(grids, rows, col, num):
    # Check if 'num' is not in the current row, column, or 3x3 box
    for i in range(9):
        if (grids[rows][i] == num) or (grids[i][col] == num) or (grids[rows - rows % 3 + i // 3][col - col % 3 + i % 3]
                                                                 == num):
            return False
    return True


def sudoku(grids):
    pairs = [0, 0]
    if not check(grids, pairs):
        return True
    rows = pairs[0]
    cols = pairs[1]

    for num in range(1, 10):
        if correct(grid, rows, cols, num):
            grid[rows][cols] = num
            if sudoku(grid):
                return True

            grid[rows][cols] = 0
    return False


if check_duplicates(grid) or check_duplicates(grid_2) or check_duplicates(grid3):
    print("The puzzle cannot be solved!!\nThe Question is wrong!")
elif sudoku(grid):
    dis(grid)
