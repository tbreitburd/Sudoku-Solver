"""!@file solver_tools.py
@brief Module containing tools for solving the sudoku.

@details This module contains tools to solve the sudoku.
One of them is a function that creates a markup of possible values,
for the sudoku cells.
@author Created by T.Breitburd on 19/11/2023
"""
import numpy as np
from . import preprocessing as pp
import pandas as pd


def markup(sudoku):
    """!@brief Create a markup for the sudoku.

    @details This function takes in a sudoku.
    And for each empty cell of that sudoku,
    lists the possible values for that cell.
    And it returns all these possible values in a dataframe,
    with corresponding row and column indexes.
    """
    if all(x == 0 for x in np.ravel(sudoku[:][:])):
        raise ValueError("The sudoku is empty")
    if all(x != 0 for x in np.ravel(sudoku[:][:])):
        raise ValueError("All cells are filled, the sudoku is already solved")

    markup = pd.DataFrame(index=range(9), columns=range(9))
    for row in range(9):
        for col in range(9):
            if sudoku[row][col] == 0:
                cell_markup = [
                    i
                    for i in range(1, 10)
                    if i not in sudoku[row, :]
                    and i not in sudoku[:, col]
                    and i not in (np.ravel(pp.box(sudoku, row, col)))
                ]
                if cell_markup == []:
                    raise ValueError(
                        "There is no possible value for cell "
                        + "({},{})".format(row, col)
                        + ", hence the sudoku is not solvable"
                    )
                markup[col][row] = cell_markup
            else:
                markup[col][row] = [sudoku[row][col]]

    return markup
