# main.py
from SAT_solver import SudokuSolver
from visualizer import visualize_sudoku

def read_sudoku_from_file(filename):
    """Đọc file Sudoku, '.' sẽ được chuyển thành 0"""
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
    # 1) Đọc puzzle từ file
    puzzle = read_sudoku_from_file("input.txt")

    # 2) Giải bằng SAT solver
    solver = SudokuSolver(puzzle)
    solution = solver.solve()

    # 3) Hiển thị kết quả
    if solution is None:
        print("Không tìm thấy nghiệm hợp lệ.")
    else:
        visualize_sudoku(puzzle, solution, title="Sudoku Solution")
