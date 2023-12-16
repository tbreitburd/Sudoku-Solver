"""!@file preprocessing.py
@brief Module containing tools for preprocessing adn post_processing the sudoku

@details This module contains tools to process the sudokus. One function is to
load the sudoku txt file information into a useable array.
The other is a function to extract the 3x3 box of a cell,
and finally a function to convert the sudoku array back into the .txt file
format, for printing and saving the sudoku once solved.

@author Created by T.Breitburd on 19/11/2023
"""
import os
import numpy as np
import sys
import traceback


def load_sudoku(path):
    """!@brief Load the sudoku .txt file into a useable Numpy array.

    @details This function takes in a path to a sudoku .txt file,
    reads the file into a series of strings for each row,
    checks that the file has the correct format,
    then picks out the numbers from the strings, dropping the separators,
    and returns a 9x9 numpy array of the sudoku.

    @param path Path to the sudoku txt file

    @return A 9x9 numpy array containing the sudoku numbers
    """
    # We use os to have relative paths be portable
    proj_dir = os.getcwd()
    sudoku_path = os.path.join(proj_dir, path)

    # Read the sudoku file, and drop the separator lines
    try:
        f = open(sudoku_path, "r")
    except FileNotFoundError:
        raise FileNotFoundError(
            "The sudoku file was not found at the path: " + sudoku_path
        )

    try:
        sudoku_rows = f.readlines()

        # Check that the sudoku file has the correct format:
        # There should be 11 rows
        if len(sudoku_rows) != 11:
            raise ValueError(
                "The sudoku in text form has an incorrect number "
                + "of rows, should be 11 but is "
                + str(len(sudoku_rows))
            )
        # 12 columns for the first 9 rows
        # (9 + 2 separators + new line character)
        len_rows = [len(char) for char in sudoku_rows]
        if not all(x == 12 for x in len_rows[:10]):
            raise ValueError(
                "The sudoku in text form has an incorrect number "
                + "of columns, should be 12 but is "
                + str(len_rows[:10])
            )
        # horizontal separators should be "---+---+---\n"
        hor_sep = "---+---+---\n"
        if sudoku_rows[3] != hor_sep and sudoku_rows[7] != hor_sep:
            raise ValueError(
                "The sudoku file has incorrect "
                + "horizontal separators, must be ---+---+---"
            )
    except ValueError as e:
        print("Traceback: ")
        traceback.print_stack()
        print("Error: ")
        print(e)
        print("Exiting program")
        sys.exit(1)

    # Drop the horizontal separator lines
    sudoku_rows = sudoku_rows[0:3] + sudoku_rows[4:7] + sudoku_rows[8:11]

    # Check that the sudoku rows have the correct format,
    # with vertical separators at specific positions
    # fmt: off
    try:
        InRowSep = [char[3] for char in sudoku_rows]
        InRowSep2 = [char[7] for char in sudoku_rows]
        if not all(x == "|" for x in InRowSep + InRowSep2):
            raise ValueError(
                "The sudoku file has incorrect vertical separators"
                + ", must be |"
            )
    # fmt: on
    except ValueError as e:
        print("Traceback: ")
        traceback.print_stack()
        print("Error: ")
        print(e)
        print("Exiting program")
        sys.exit(1)

    # Initialize the sudoku array
    sudoku = np.zeros((9, 9), dtype=int)

    # Remove the "new line" characters and the vertical separators,
    # and add those rows to the sudoku array
    for row_num, row in enumerate(sudoku_rows, 1):
        row = [x for x in row if x != "\n" and x != "|"]
        sudoku[row_num - 1] = row
    return sudoku


def box(sudoku, row, col):
    """!@brief This function takes in a sudoku and a cell's row and column,
    and returns a 3x3 array of the sudoku box that cell is in.

    @details The function takes in a sudoku and a cell's row and column,
    and returns a 3x3 array of the sudoku box that cell is in.

    @param sudoku The sudoku to extract the box from
    @param row The row of the cell, 0 based index
    @param col The column of the cell, 0 based index

    @return A 3x3 array of the corresponding box.
    """
    # Check that the cell coordinates are valid
    try:
        if row < 0 or row > 8 or col < 0 or col > 8:
            raise ValueError(
                "The cell coordinates are not valid, "
                + "must be between 0 and 8 inclusive but:"
                + "Row: "
                + str(row)
                + ", Col: "
                + str(col)
            )
    except ValueError as e:
        print("Traceback: ")
        traceback.print_stack()
        print("Error: ")
        print(e)
        print("Exiting program")
        sys.exit(1)

    # Initialize box array
    box = np.zeros((3, 3))
    # Identify the box's box-coordinates (tuples of 1, 2 or 3)
    box_row = int((row + 3) // 3)
    box_col = int((col + 3) // 3)

    # Get the box values
    row_start = int(3 * (box_row - 1))
    row_end = int(row_start + 3)

    col_start = int(3 * (box_col - 1))
    col_end = int(col_start + 3)

    # fmt: off
    # This line caused black/flake8 conflicts
    box = sudoku[row_start:row_end, col_start:col_end]
    # fmt: on

    return box


def sudoku_to_output_format(sudoku):
    """!@brief This function takes in a sudoku array,
    and returns a string in the specific format of the output file.

    @details This function takes in a sudoku numpy array, and adds each cell to
    a string, adding in separators, vertical and horizontal
    and newlines where necessary, returning a string which when printed will
    be in the desired sudoku format for the output file.

    @param sudoku The sudoku numpy array to convert to a string

    @return A string in the format of the output file.
    """
    # Initialize the output string
    sudoku_str = ""

    for row in range(9):
        for col in range(9):
            # Add each cell to the output string
            sudoku_str += str(sudoku[row][col])

            # Add a vertical separator if at the end of a box
            if col == 2 or col == 5:
                sudoku_str += "|"

            # Add a newline if at the end of a row,
            # except at the end of the sudoku
            elif col == 8 and row != 8:
                sudoku_str += "\n"

        # Add a horizontal separator if at the end of row 3 or 6
        if row == 2 or row == 5:
            sudoku_str += "---+---+---\n"

    return sudoku_str
