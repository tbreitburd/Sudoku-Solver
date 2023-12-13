"""!@file test_check_sudoku.py
@brief Module containing tests for the check_sudoku function of the
solver_tools module.

@details This module contains tests for the check_sudoku function of the
solver_tools module. The check_sudoku function is used to check whether a
given sudoku is valid or not. The function returns a tuple containing a
boolean value and a string. The boolean value is True if the sudoku is valid
and False if it is not. The string is empty if the sudoku is valid and
contains an error message if it is not.

@author Created by T.Breitburd on 13/12/2023
"""

import numpy as np
from src import solver_tools as st


sudoku_bad_row = np.array(
    [
        [0, 0, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 0, 9, 5, 0, 4],
        [0, 0, 0, 0, 5, 0, 1, 6, 9],
        [0, 8, 0, 0, 0, 0, 3, 0, 5],
        [0, 7, 5, 0, 0, 2, 2, 9, 0],
        [4, 0, 6, 0, 0, 0, 0, 8, 0],
        [7, 6, 2, 0, 8, 0, 0, 0, 0],
        [1, 0, 3, 9, 0, 0, 0, 0, 0],
        [0, 0, 0, 6, 0, 0, 0, 0, 0],
    ]
)


def test_check_sudoku():
    assert st.check_sudoku(sudoku_bad_row) == (
        False,
        "There are too many 2's in row 5",
    )


sudoku_bad_col = np.array(
    [
        [0, 0, 0, 0, 0, 7, 5, 0, 0],
        [0, 0, 0, 0, 0, 9, 0, 0, 4],
        [0, 0, 0, 0, 5, 0, 1, 6, 9],
        [0, 8, 0, 0, 0, 0, 3, 0, 5],
        [0, 7, 5, 0, 0, 0, 2, 9, 0],
        [4, 0, 6, 0, 0, 0, 0, 8, 0],
        [7, 6, 2, 0, 8, 0, 0, 0, 0],
        [1, 0, 3, 9, 0, 0, 5, 0, 0],
        [0, 0, 0, 6, 0, 0, 0, 0, 0],
    ]
)


def test_check_sudoku2():
    assert st.check_sudoku(sudoku_bad_col) == (
        False,
        "There are too many 5's in column 7",
    )


sudoku_bad_box = np.array(
    [
        [0, 0, 0, 0, 0, 7, 5, 0, 0],
        [0, 0, 0, 0, 0, 9, 0, 5, 4],
        [0, 0, 0, 0, 5, 0, 1, 6, 9],
        [0, 8, 0, 0, 0, 0, 3, 0, 5],
        [0, 7, 5, 0, 0, 0, 2, 9, 0],
        [4, 0, 6, 0, 0, 0, 0, 8, 0],
        [7, 6, 2, 0, 8, 0, 0, 0, 0],
        [1, 0, 3, 9, 0, 0, 0, 0, 0],
        [0, 0, 0, 6, 0, 0, 0, 0, 0],
    ]
)


def test_check_sudoku3():
    assert st.check_sudoku(sudoku_bad_box) == (
        False,
        "There are too many 5's in box [1,3]",
    )


sudoku_good = np.array(
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


def test_check_sudoku5():
    assert st.check_sudoku(sudoku_good) == (True, "_")
