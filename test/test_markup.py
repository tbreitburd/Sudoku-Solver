"""!@file test_markup.py

@brief Module containing tests for the markup function of the solver_tools
module.

@details This module contains tests for the markup function of the solver_tools
module. The markup function is used to generate a markup of a given sudoku.
The markup is a 3D array of shape (9, 9, number of possible values) where the
first two dimensionsvcorrespond to the rows and columns of the sudoku and
the third dimensioncontains a list of possible values for each cell of the
sudoku.

@author Created by T.Breitburd on 01/12/2023
"""
from src import solver_tools, preprocessing
import unittest
import numpy as np


def test_markup():
    """!@brief Test the markup function on a sudoku.

    @details The markup function should return a 3D array of shape (9, 9, 9)
    where the first two dimensions correspond to the rows and columns of the
    sudoku and the third dimension contains a list of possible values for each
    cell of the sudoku.
    """
    markup_tester = solver_tools.markup(
        preprocessing.load_sudoku("sudokus/sudoku1.txt")
    )
    assert markup_tester[3][4] == [1, 3, 4, 8]
    assert markup_tester[6][0] == [8]


empty_sudoku = np.zeros((9, 9), dtype=int)


unsolvable_sudoku = np.array(
    [
        [0, 0, 0, 0, 0, 0, 1, 2, 3],
        [0, 0, 9, 0, 0, 0, 0, 4, 5],
        [0, 0, 0, 0, 0, 0, 6, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 7, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 8, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
)


solved_sudoku = np.array(
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


class TestMarkup(unittest.TestCase):
    def test_markup_2(self):
        """!@brief Test the markup function on an empty sudoku.

        @details The markup function should return a warning since this sudoku
        has many solutions.
        """
        with self.assertWarns(UserWarning):
            solver_tools.markup(empty_sudoku)

    def test_markup_3(self):
        """!@brief Test the markup function on an unsolvable sudoku.

        @details The markup function should return an error and exit.
        """
        with self.assertRaises(SystemExit) as context:
            solver_tools.markup(unsolvable_sudoku)

        # Check the exit code
        self.assertEqual(context.exception.code, 1)

    def test_markup_4(self):
        """!@brief Test the markup function on a solved sudoku.

        @details The markup function should return an error and exit.
        """
        with self.assertRaises(SystemExit) as context:
            solver_tools.markup(solved_sudoku)

        # Check the exit code
        self.assertEqual(context.exception.code, 1)
