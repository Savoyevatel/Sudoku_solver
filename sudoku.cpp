#include <iostream>
#include <fstream>
#include<math.h>
#include <vector>
#include <set>
//using namespace std;
#define z 9

bool dis(std::vector<std::vector<int>> & a) {
    std::cout << " The solution is! - " << std::endl;
    for (int i = 0; i < z; i++) {
        for (int j = 0; j < z; j++) {
            std::cout << a[i][j] << "   ";
        }
        std::cout << std::endl << std::endl;
    }
}


bool checkduplicates(const std::vector<std::vector<int>>& lst) {
    for (const auto& subList : lst) {
        std::set<int> seen;
        for (int item : subList) {
            if (item != 0) {
                if (seen.count(item) > 0) {
                    return true;
                }
                seen.insert(item);
            }
        }
    }
    return false;
}


bool check(std::vector<std::vector<int>>& a, std::vector<int>& pair) {
    for (int row = 0; row < z; row++) {
        for (int col = 0; col < z; col++) {
            if (a[row][col] == 0) {
                pair[0] = row;
                pair[1] = col;
                return true;
            }
        }
    }
    return false;
}

bool correct(std::vector<std::vector<int>>& grid, int row, int col, int num) {
    for (int i = 0; i < 9; i++) {
        if (grid[row][i] == num || grid[i][col] == num ||
            grid[row - row % 3 + i / 3][col - col % 3 + i % 3] == num) {
            return false;
        }
    }
    return true;
}

bool sudoku(std::vector<std::vector<int>>& grid) {
    std::vector<int> pairs(2, 0);
    if (!check(grid, pairs)) {
        return true;
    }
    int rows = pairs[0];
    int cols = pairs[1];

    for (int num = 1; num <= 9; num++) {
        if (correct(grid, rows, cols, num)) {
            grid[rows][cols] = num;
            if (sudoku(grid)) {
                return true;
            }

            grid[rows][cols] = 0;
        }
    }
    return false;
}

int main() 
{
	
    std::vector<std::vector<int>> grid(z, std::vector<int>(z, 0));

    std::ifstream file("sudoku.txt");
    if (file.is_open()) {
        int c = 0;
        for (int i = 0; i < z; i++) {
            std::vector<int> row(z, 0);
            for (int j = 0; j < z; j++) {
                file >> row[j];
                grid[i][j] = row[j];
                if (grid[i][j] == 0) {
                    c++;
                }
            }
        }
        file.close();
    }
    
    
    std::vector<std::vector<int>> grid2;
    
    for (int j = 0; j < 9; j++) {
        std::vector<int> row;
        for (int i = 0; i < 9; i++) {
            row.push_back(grid[j][i]);
        }
        grid2.push_back(row);
    }

    
    std::vector<std::vector<int>> grid3;

    for (int i = 0; i < grid.size(); i += 3) {
        std::vector<std::vector<int>> temp_lists = {{}, {}, {}};

        for (int j = i; j < i + 3; j++) {
            std::vector<int> sublist = grid[j];

            for (int k = 0; k < 3; k++) {
                int start_index = k * 3;
                int end_index = start_index + 3;
                temp_lists[k].insert(temp_lists[k].end(), sublist.begin() + start_index, sublist.begin() + end_index);
            }
        }

        grid3.insert(grid3.end(), temp_lists.begin(), temp_lists.end());
    }


    if (checkduplicates(grid) || checkduplicates(grid2) || checkduplicates(grid3)) {
        std::cout << "The puzzle cannot be solved!!\nThe Question is wrong!" << std::endl;
    }
	if (sudoku(grid)) {
        dis(grid);
    } else {
        std::cout << " The puzzle cannot be solved!!\nThe Question is wrong!" << std::endl;
    }

    return 0;
}
