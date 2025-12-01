# visualizer.py
import matplotlib.pyplot as plt
import numpy as np
from typing import List

def visualize_sudoku(puzzle: List[List[int]], solution: List[List[int]], title: str = "Sudoku"):
    """
    Hiển thị puzzle (đầu vào) và solution (kết quả) trên cùng một bảng 9x9.
    - puzzle: ma trận 9x9 với 0 cho ô trống
    - solution: ma trận 9x9 là lời giải (hoặc None)
    """
    N = 9
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, N)
    ax.set_ylim(0, N)
    ax.set_xticks(np.arange(0, N+1, 1))
    ax.set_yticks(np.arange(0, N+1, 1))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_aspect('equal')
    ax.invert_yaxis()
    ax.grid(True, which='both', linewidth=1)

    # kẻ đường viền block dày hơn
    for i in range(0, N+1, 3):
        ax.axhline(i, linewidth=2)
        ax.axvline(i, linewidth=2)

    # in số: giữ số gốc đậm hơn để phân biệt
    for r in range(N):
        for c in range(N):
            num = solution[r][c] if solution is not None else puzzle[r][c]
            if num == 0:
                continue
            weight = 'bold' if puzzle[r][c] != 0 else 'normal'
            ax.text(c + 0.5, r + 0.5, str(num),
                    va='center', ha='center', fontsize=14, fontweight=weight)

    plt.title(title, pad=12)
    plt.show()
