"""!@file preprocessing.py
@brief Module containing tools for preprocessing
the sudoku txt file into a useable array

@details This module contains tools to load
the sudoku txt file information into a useable array.
@author Created by T.Breitburd on 19/11/2023
"""
import os
import numpy as np


def test(x):
    return x + 1


def load_sudoku(path):
    """!@brief Load the sudoku txt file into a useable array

    @param path Path to the sudoku txt file
    @return A 9x9 numpy array containing the sudoku numbers
    """
    # We use os to have relative paths be portable
    proj_dir = os.getcwd()
    sudoku_path = os.path.join(proj_dir, path)

    # Read the sudoku file, and drop the separator lines
    with open(sudoku_path, "r") as f:
        sudoku_rows = f.readlines()
    sudoku_rows = sudoku_rows[0:3] + sudoku_rows[4:7] + sudoku_rows[8:11]

    # Initialize the sudoku array
    sudoku = np.zeros((9, 9), dtype=int)

    # Remove the newlines and the vertical lines,
    # and add the rows to the sudoku array
    for row_num, row in enumerate(sudoku_rows, 1):
        row = [x for x in row if x != "\n" and x != "|"]
        sudoku[row_num - 1] = row
    return sudoku
