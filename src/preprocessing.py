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

    # Check that the sudoku file has the correct format
    if len(sudoku_rows) != 11:
        raise ValueError("The sudoku file has an incorrect number of rows")

    len_rows = [len(char) for char in sudoku_rows]
    if not all(x == 12 for x in len_rows[:10]):
        raise ValueError("The sudoku file has an incorrect number of columns")

    if sudoku_rows[3] != "---+---+---\n" and sudoku_rows[7] != "---+---+---\n":
        raise ValueError("The sudoku file has incorrect separators")

    # Drop the separator lines
    sudoku_rows = sudoku_rows[0:3] + sudoku_rows[4:7] + sudoku_rows[8:11]

    # Check that the sudoku rows have the correct format
    InRowSep = [char[3] for char in sudoku_rows]
    InRowSep2 = [char[7] for char in sudoku_rows]
    if not all(x == "|" for x in InRowSep + InRowSep2):
        raise ValueError("The sudoku file has incorrect separators")

    # Initialize the sudoku array
    sudoku = np.zeros((9, 9), dtype=int)

    # Remove the newlines and the vertical lines,
    # and add the rows to the sudoku array
    for row_num, row in enumerate(sudoku_rows, 1):
        row = [x for x in row if x != "\n" and x != "|"]
        sudoku[row_num - 1] = row
    return sudoku


def box(sudoku, row, col):
    """!@brief This function takes in a sudoku,
    and returns a 3x3 array of the sudoku boxes.
    @details The function takes in a sudoku,
    and returns a 3x3 array of the sudoku boxes.
    @param sudoku The sudoku to extract the boxes from.
    @return A 3x3 array of all the boxes in the sudoku.
    """
    # Initialize the list of boxes
    box = np.zeros((3, 3))
    # Get the box values
    row_start = int(3 * (row - 1))
    row_end = int(row_start + 3)

    col_start = int(3 * (col - 1))
    col_end = int(col_start + 3)

    # fmt: off
    # This line caused black/flake8 conflicts
    box = [sudoku[i][col_start:col_end] for i in range(row_start, row_end)]
    # fmt: on

    return box
