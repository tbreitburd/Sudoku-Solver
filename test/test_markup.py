from src import solver_tools, preprocessing
import unittest
import numpy as np


def test_markup():
    markup_tester = solver_tools.markup(
        preprocessing.load_sudoku("sudokus/sudoku1.txt")
    )
    assert markup_tester[3][4] == [1, 3, 4, 8]
    assert markup_tester[6][0] == [8]


empty_sudoku = np.zeros((9, 9), dtype=int)


def test_markup_2():
    with unittest.TestCase().assertRaises(ValueError):
        solver_tools.markup(empty_sudoku)
