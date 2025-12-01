# csp.py
from itertools import product, combinations
from typing import List, Sequence

class SudokuCSP:
    """
    Tạo CNF clauses cho Sudoku 9x9 theo biểu diễn propositional:
    biến (r,c,v) -> số nguyên: 1..729
    """

    def __init__(self, N: int = 9):
        self.N = N
        self.block = 3  # kích thước block = 3 cho Sudoku chuẩn

    def varnum(self, r: int, c: int, v: int) -> int:
        """Mã hóa (r,c,v) về biến nguyên (1..N*N*N). r,c,v đều 1-based."""
        return self.N * self.N * (r - 1) + self.N * (c - 1) + v

    def _at_least_one(self, literals: Sequence[int]) -> List[List[int]]:
        """Trả về clause đại diện cho 'ít nhất một' (OR trên literals)."""
        return [list(literals)]

    def _at_most_one(self, literals: Sequence[int]) -> List[List[int]]:
        """Sinh các clause pairwise cho 'tối đa một' (¬xi ∨ ¬xj)."""
        clauses = []
        for a, b in combinations(literals, 2):
            clauses.append([-a, -b])
        return clauses

    def _exactly_one(self, literals: Sequence[int]) -> List[List[int]]:
        """Kết hợp 'ít nhất một' và 'tối đa một' => 'chính xác một'."""
        clauses = []
        clauses += self._at_least_one(literals)
        clauses += self._at_most_one(literals)
        return clauses

    def generate_clauses(self, puzzle: Sequence[Sequence[int]]) -> List[List[int]]:
        """
        Sinh tất cả CNF clauses từ puzzle.
        puzzle: danh sách 9 hàng, mỗi hàng 9 số (0 nếu blank).
        Trả về list các clauses (mỗi clause là list các int).
        """
        # kiểm tra kích thước
        if len(puzzle) != self.N or any(len(row) != self.N for row in puzzle):
            raise ValueError("Puzzle phải là ma trận 9x9 (dùng 0 cho ô trống).")

        clauses: List[List[int]] = []

        # 1) Cell constraints: mỗi ô chính xác một giá trị
        for r, c in product(range(1, self.N + 1), repeat=2):
            literals = [self.varnum(r, c, v) for v in range(1, self.N + 1)]
            clauses += self._exactly_one(literals)

        # 2) Row constraints: mỗi giá trị xuất hiện đúng 1 lần trên mỗi hàng
        for r in range(1, self.N + 1):
            for v in range(1, self.N + 1):
                literals = [self.varnum(r, c, v) for c in range(1, self.N + 1)]
                clauses += self._exactly_one(literals)

        # 3) Column constraints: mỗi giá trị xuất hiện đúng 1 lần trên mỗi cột
        for c in range(1, self.N + 1):
            for v in range(1, self.N + 1):
                literals = [self.varnum(r, c, v) for r in range(1, self.N + 1)]
                clauses += self._exactly_one(literals)

        # 4) Block constraints: mỗi giá trị xuất hiện đúng 1 lần trong mỗi block 3x3
        for br in range(0, self.block):
            for bc in range(0, self.block):
                rows = range(1 + br * self.block, 1 + br * self.block + self.block)
                cols = range(1 + bc * self.block, 1 + bc * self.block + self.block)
                for v in range(1, self.N + 1):
                    literals = [self.varnum(r, c, v) for r in rows for c in cols]
                    clauses += self._exactly_one(literals)

        # 5) Clues (gợi ý ban đầu): cố định giá trị tại ô có sẵn
        for r in range(1, self.N + 1):
            for c in range(1, self.N + 1):
                val = puzzle[r - 1][c - 1]
                if val != 0:
                    clauses.append([self.varnum(r, c, val)])  # clause unit

        return clauses
