from src import solver_tools
import numpy as np
import unittest


sudoku = np.array(
    [
        [0, 0, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 0, 9, 5, 0, 4],
        [0, 0, 0, 0, 5, 0, 1, 6, 9],
        [0, 8, 0, 0, 0, 0, 3, 0, 5],
        [0, 7, 5, 0, 0, 0, 2, 9, 0],
        [4, 0, 6, 0, 0, 0, 0, 8, 0],
        [7, 6, 2, 0, 8, 0, 0, 0, 0],
        [1, 0, 3, 9, 0, 0, 0, 0, 0],
        [0, 0, 0, 6, 0, 0, 0, 0, 0],
    ],
)

sudoku_solved = np.array(
    [
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [7, 8, 9, 1, 2, 3, 4, 5, 6],
        [4, 5, 6, 7, 8, 9, 1, 2, 3],
        [3, 1, 2, 6, 4, 5, 9, 7, 8],
        [6, 4, 5, 9, 7, 8, 3, 1, 2],
        [9, 7, 8, 3, 1, 2, 6, 4, 5],
        [2, 3, 1, 5, 6, 4, 8, 9, 7],
        [5, 6, 4, 8, 9, 7, 2, 3, 1],
        [8, 9, 7, 2, 3, 1, 5, 6, 4],
    ]
)

markup1 = solver_tools.markup(sudoku)
backtrack_cells = np.where(markup1.map(len) > 1)
backtrack_cells = np.array([backtrack_cells[1], backtrack_cells[0]]).T


def test_backtrack():
    with unittest.TestCase().assertRaises(RuntimeError):
        solver_tools.backtrack_alg(sudoku_solved, markup1, backtrack_cells, 0)


sudoku2 = np.array(
    [
        [0, 0, 0, 0, 0, 0, 1, 2, 3],
        [0, 0, 9, 0, 0, 0, 0, 0, 5],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 8, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 4, 0, 0, 7, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 4, 0, 0, 0, 8, 0, 0],
        [0, 0, 0, 5, 0, 0, 0, 0, 0],
    ]
)


def test_backtrack_2():
    assert not solver_tools.backtrack_alg(sudoku2, markup1, backtrack_cells, 0)


def test_backtrack_3():
    assert solver_tools.backtrack_alg(sudoku, markup1, backtrack_cells, 0)

    assert np.array_equal(
        [
            [5, 9, 4, 1, 6, 7, 0, 2, 3],
            [6, 3, 1, 8, 2, 9, 5, 7, 4],
            [8, 2, 7, 4, 5, 3, 1, 6, 9],
            [2, 8, 9, 7, 4, 6, 3, 1, 5],
            [0, 7, 5, 3, 1, 8, 2, 9, 6],
            [4, 1, 6, 2, 9, 5, 0, 8, 7],
            [7, 6, 2, 5, 8, 4, 9, 3, 1],
            [1, 4, 3, 9, 7, 2, 6, 5, 8],
            [9, 5, 8, 6, 3, 1, 7, 4, 2],
        ],
        sudoku,
    )
