from pysat.solvers import Glucose3
from problem import SudokuCSP
from typing import List, Optional

class SudokuSolver:

    def __init__(self, puzzle: List[List[int]]):
        self.puzzle = puzzle
        self.csp = SudokuCSP()
        self.solver = None  

    def _add_clauses(self, clauses: List[List[int]]) -> None:
        self.solver = Glucose3()
        for clause in clauses:
            self.solver.add_clause(clause)

    def _model_to_grid(self, model: List[int]) -> List[List[int]]:
        N = self.csp.N
        grid = [[0 for _ in range(N)] for _ in range(N)]
        for lit in model:
            if lit > 0:
                v = lit % N
                if v == 0:
                    v = N
                idx = (lit - 1)
                r = idx // (N * N) + 1
                c = (idx % (N * N)) // N + 1
                grid[r - 1][c - 1] = v
        return grid

    def solve(self) -> Optional[List[List[int]]]:
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
