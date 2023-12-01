"""!@file solver_tools.py
@brief Module containing tools for solving the sudoku.

@details This module contains tools to solve the sudoku.
One of them is
@author Created by T.Breitburd on 19/11/2023
"""
import numpy as np
from src import preprocessing as pp
import pandas as pd


def markup(sudoku):
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
                markup[col][row] = cell_markup
    return markup
