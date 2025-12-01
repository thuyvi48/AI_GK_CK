# SAT_solver.py
from pysat.solvers import Glucose3
from problem import SudokuCSP
from typing import List, Optional

class SudokuSolver:
    """
    Wrapper OOP cho quá trình:
    - sinh CNF từ Sudoku
    - gọi Glucose3 để tìm model
    - chuyển model -> lưới 9x9
    """

    def __init__(self, puzzle: List[List[int]]):
        self.puzzle = puzzle
        self.csp = SudokuCSP()
        self.solver = None  # sẽ khởi tạo khi cần

    def _add_clauses(self, clauses: List[List[int]]) -> None:
        """Thêm clauses vào solver (không trả về gì)."""
        self.solver = Glucose3()
        for clause in clauses:
            self.solver.add_clause(clause)

    def _model_to_grid(self, model: List[int]) -> List[List[int]]:
        """Chuyển danh sách literal model (int) sang ma trận 9x9 giá trị."""
        N = self.csp.N
        grid = [[0 for _ in range(N)] for _ in range(N)]
        for lit in model:
            if lit > 0:
                v = lit % N
                if v == 0:
                    v = N
                # tính r,c từ lit (1-based)
                idx = (lit - 1)
                r = idx // (N * N) + 1
                c = (idx % (N * N)) // N + 1
                grid[r - 1][c - 1] = v
        return grid

    def solve(self) -> Optional[List[List[int]]]:
        """Giải puzzle, trả về grid 9x9 nếu thành công, ngược lại None."""
        clauses = self.csp.generate_clauses(self.puzzle)
        self._add_clauses(clauses)
        try:
            sat = self.solver.solve()
            if not sat:
                return None
            model = self.solver.get_model()
            return self._model_to_grid(model)
        finally:
            if self.solver is not None:
                self.solver.delete()
                self.solver = None
