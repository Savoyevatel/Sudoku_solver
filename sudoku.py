z = 9 #your signature
c= 0 #counting zeros

grid = [[0 for i in range(z)] for j in range(z)]

with open("sudoku.txt", "r") as f:
    c = 0
    for i in range(z):
        row = f.readline().split()
        for j in range(z):
            grid[i][j] = int(row[j])
            if grid[i][j] == 0:
                c += 1
#print(a)

pair = [[0, 0] for i in range(c)]

def dis(a):
    print("The solution is!")
    for i in range(z):
        for j in range(z):
            print(a[i][j], end="   ")
        print("\n")
        print()

#print(dis())
def check(a, l):
    zero = 1
    for i in range(z):
        for j in range(z):
            if a[i][j] == 0:
                l[0] = i #row
                l[1] = j #column
                return True
    return False
#print(check(i,j))
def correct(grid, row, col, num):
    # Check if 'num' is not in the current row, column, or 3x3 box
    for i in range(9):
        if (grid[row][i] == num) or (grid[i][col] == num) or (grid[row - row % 3 + i // 3][col - col % 3 + i % 3] == num):
            return False
    return True

def sudoku(grid):
    l = [0, 0]
    if (not check(grid, l)):
        return True
    row = l[0]
    col = l[1]

    for num in range(1, 10):
        if correct(grid, row, col, num):
            grid[row][col] = num
            if (sudoku(grid)):
                return True

            grid[row][col] = 0
    return False

if (sudoku(grid)):
    dis(grid)
else:
    print("The puzzle cannot be solved!!\nThe Question is wrong!")
