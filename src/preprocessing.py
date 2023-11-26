"""!@file preprocessing.py
@brief Module containing tools for preprocessing
the sudoku txt file into a useable array

@details This module contains tools to load
the sudoku txt file information into a useable array.
@author Created by T.Breitburd on 19/11/2023
"""


def test(x):
    return x + 1


def load_sudoku(path):
    """!@brief Load the sudoku txt file into a useable array

    @param path Path to the sudoku txt file
    @return A 9x9 numpy array containing the sudoku numbers
    """
    with open(path, "r") as f:
        sudoku = [[int(x) for x in line.split()] for line in f]
    return sudoku
