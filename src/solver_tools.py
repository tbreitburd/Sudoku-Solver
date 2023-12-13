"""!@file solver_tools.py
@brief Module containing tools for solving the sudoku.

@details This module contains tools to solve the sudoku.
One of them is a function that creates a markup of possible values,
for each remaining empty cell in the sudoku.
The other is a backtracking algorithm that uses a recursive function
to solve the sudoku.

@author Created by T.Breitburd on 19/11/2023
"""
import numpy as np
import warnings
from . import preprocessing as pp
import pandas as pd


def check_sudoku(sudoku):
    """!@brief Check if the sudoku is valid.

    @details This function takes in a sudoku,
    and checks if it is valid, i.e. only values in between 1 and 9,
    and maximum one of each per row, column and box

    @param sudoku A 9x9 numpy array containing the sudoku numbers

    @return A boolean, True if the sudoku is valid, False if it is not.
    """

    # Check if the sudoku only contains numbers between 0 and 9
    if any(x not in range(10) for x in np.ravel(sudoku)):
        return False

    # Check if there are no duplicates in each row

    # Check if there are no duplicates in each column

    # Check if there are no duplicates in each box

    return True


def markup(sudoku):
    """!@brief Create a markup for the sudoku.

    @details This function takes in a sudoku.
    And for each empty cell of that sudoku,
    lists the possible values for that cell, by checking the row, column, and
    box that cell is in for values that are already present.
    And it returns all these possible values in a dataframe,
    with corresponding row and column indexes.

    @param sudoku A 9x9 numpy array containing the sudoku numbers

    @return A 9x9 dataframe containing lists of possible values for each cell.
    """

    # Check if the sudoku might have multiple solutions, if yes, give a warning
    if np.count_nonzero(sudoku) < 16:
        message = (
            "This sudoku may have multiple solutions,"
            + " and the backtracking algorithm will"
            + " return the first it finds."
        )
        warnings.warn(message, UserWarning)

    # Check if the sudoku is already solved, if yes, raise an error
    if all(x != 0 for x in np.ravel(sudoku[:][:])):
        # fmt: off
        raise RuntimeError("All cells are filled, " +
                           "the sudoku is already solved")
        # fmt: on

    # Create a dataframe to store the markup
    markup = pd.DataFrame(index=range(9), columns=range(9))

    # Loop through the sudoku, and for each empty cell,
    # check the row, column, and box that cell is in for values that are
    # already present, then list the possible values for that cell.
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

                # If there are no possible values for the cell, raise an error
                if cell_markup == []:
                    raise RuntimeError(
                        "There is no possible value for cell "
                        + "({},{})".format(row, col)
                        + ", hence the sudoku is not solvable"
                    )

                # Put the possible values in the markup dataframe
                markup[col][row] = cell_markup
            else:
                # If the cell is not empty, put the cell value in the markup
                # This is to avoid having NaN values in the markup dataframe.
                markup[col][row] = [sudoku[row][col]]

    return markup


def backtrack_alg(sudoku, markup_, backtrack_cells, cell_num):
    """!@brief Backtracking algorithm to solve the sudoku,
    using a recursive function.

    @details This function takes a sudoku in array form,
    the associated markup dataframe of possible values for the sudoku cells,
    a list of the cells that we need to backtrack through from that markup,
    the cell number we are currently looking at within that list,
    and returns a solved sudoku, if possible.

    @param sudoku A 9x9 numpy array containing the sudoku numbers
    @param markup_ A 9x9 dataframe containing lists of possible values
    for each cell.
    @param backtrack_cells A numpy array containing the indexes of the cells
    that still have more than one possible value, in that markup file.
    @param cell_num The index of the current cell we are looking at,
    within the backtrack_cells list.

    @return A boolean, True if the sudoku is solved,
    False if it is still not solved.
    """
    # The recursive function method was used from this webpage,
    # as well as the subapges linked to it:
    # https://www.geeksforgeeks.org/introduction-to-recursion-data-structure
    # -and-algorithm-tutorials/?ref=lbp

    # Base case of the recursion, we have reached the end of the sudoku if:
    if cell_num == len(backtrack_cells):
        return True  # Returning true will end the recursion,
        # however deep the level of recursion is.

    # Get the markup values of the current cell, from the markup dataframe
    backtrack_cell_vals = markup_[backtrack_cells[cell_num][0]][
        backtrack_cells[cell_num][1]
    ]

    # Get the sudoku-valid values for the current cell, from the sudoku array,
    # using the same conditions as in the markup function
    # fmt: off
    valid_cell_vals = [
        x
        for x in backtrack_cell_vals
        if x not in sudoku[backtrack_cells[cell_num][1], :]
        and x not in sudoku[:, backtrack_cells[cell_num][0]]
        and x not in (
                    np.ravel(
                            pp.box(
                                    sudoku,
                                    backtrack_cells[cell_num][1],
                                    backtrack_cells[cell_num][0]
                                    )
                            )
                    )
        # fmt: on
    ]

    # If there are no valid values for the current cell, return False
    # This will trigger the backtracking, when at a level cell_num + 1.
    # If this happens at cell_num = 0, then the sudoku is not solvable.
    if valid_cell_vals == []:
        if cell_num == 0:
            raise RuntimeError(
                "The sudoku is not solvable, already solved, or there may "
                + "be a disagreement between the arguments, i.e. not being "
                + "associated, check the arguments are from the same sudoku."
            )
        return False

    # Now we loop through those valid values, and trying them in the sudoku.
    # It is within this loop that the recursion happens. The within loop
    # placement is what permits us to backtrack to the previous cell's next
    # value, if the current cell value is not valid.
    for val_num in range(len(valid_cell_vals)):
        # Assign the trial value to the current cell
        cell_trial = valid_cell_vals[val_num]
        # fmt: off
        sudoku[
            backtrack_cells[cell_num][1]
            ][
                backtrack_cells[cell_num][0]] = cell_trial
        # fmt: on

        # From this current cell and trial value, we move on to the next cell
        # and implicitly the ones after that, using the recursive call, to see
        # if the sudoku can be solved with this current cell's trial value.
        # If this line fails at cell_num + 1, we will simply "come back" to
        # this loop, and try the next value in the list of valid values.
        if backtrack_alg(sudoku, markup_, backtrack_cells, cell_num + 1):
            return True

        # If the recursive call returns False, then we need to backtrack as
        # described above.
        # And before doing that we need to reset the current cell to 0,
        # so that the valid_cell_vals definition above works correctly.
        sudoku[backtrack_cells[cell_num][1]][backtrack_cells[cell_num][0]] = 0

    # If we have tried all the valid values for the current cell,
    # and none of them worked, then we need to backtrack. This line is
    # what makes the if statement in the loop above work as intended.
    return False
