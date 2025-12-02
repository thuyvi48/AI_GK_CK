from SAT_solver import SudokuSolver
from visualizer import visualize_sudoku

def read_sudoku_from_file(filename):
    # . là 0
    puzzle = []
    with open(filename, "r") as f:
        for line in f:
            row = []
            for val in line.strip().split():
                if val == ".":
                    row.append(0)
                else:
                    row.append(int(val))
            puzzle.append(row)
    return puzzle

if __name__ == "__main__":
    puzzle = read_sudoku_from_file("input.txt")
    solver = SudokuSolver(puzzle)
    solution = solver.solve()
    if solution is None:
        print("Không tìm thấy nghiệm hợp lệ.")
    else:
        visualize_sudoku(puzzle, solution, title="Sudoku Solution")