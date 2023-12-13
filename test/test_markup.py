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
    markup_tester = solver_tools.markup(
        preprocessing.load_sudoku("sudokus/sudoku1.txt")
    )
    assert markup_tester[3][4] == [1, 3, 4, 8]
    assert markup_tester[6][0] == [8]


empty_sudoku = np.zeros((9, 9), dtype=int)


def test_markup_2():
    with unittest.TestCase().assertWarns(UserWarning):
        solver_tools.markup(empty_sudoku)


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


def test_markup_3():
    with unittest.TestCase().assertRaises(RuntimeError):
        solver_tools.markup(unsolvable_sudoku)


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


def test_markup_4():
    with unittest.TestCase().assertRaises(RuntimeError):
        solver_tools.markup(solved_sudoku)
