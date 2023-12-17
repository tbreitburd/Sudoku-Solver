"""!@file solver_tools.py
@brief Module containing tools for solving the sudoku.

@details This module contains tools to solve the sudoku.
The markup() function creates a markup of possible values,
for each remaining empty cell in the sudoku. It takes in a sudoku, and for each
empty cell, lists the possible values for that cell, by checking the row,
column, and box that cell is in for values that are already present.
The check_sudoku() as its name suggests checks if the sudoku is valid,
and optionally, if it is solved.
The last one is a backtracking algorithm that uses a recursive function
to solve the sudoku. It takes in a sudoku, the associated markup dataframe,
a list of the cells that we need to backtrack through from that markup,
and the cell number we are currently looking at within that list,
and returns a solved sudoku, if possible.

@author Created by T.Breitburd on 19/11/2023
"""
import numpy as np
import warnings
from . import preprocessing as pp
import pandas as pd
import sys
import traceback


def check_sudoku(sudoku, final_check):
    """!@brief Check if the sudoku is valid.

    @details This function takes in a sudoku,
    and checks if it is valid, i.e. a maximum of one of each number
    in each row, column and box. Given the final_check boolean, when True,
    it also checks if the sudoku is solved, i.e. if there are no empty cells.

    @param sudoku A 9x9 numpy array containing the sudoku numbers
    @param final_check A boolean, True if it's to check the sudoku is solved

    @return A boolean, True if the sudoku is valid, False if it is not.
    And a string, containing a message explaining why the sudoku is not valid.

    @example This example describes how to use the check_sudoku function.

    @code
    >>> sudoku = np.array([[0,0,4,0,5,0,0,7,0],
    ...                    [0,0,0,0,0,0,0,0,0],
    ...                    [0,0,0,0,0,8,0,0,0],
    ...                    [0,3,0,0,0,0,0,9,0],
    ...                    [0,0,1,0,0,0,0,9,0],
    ...                    [0,0,0,7,0,0,0,0,0],
    ...                    [0,0,0,4,6,2,0,0,0],
    ...                    [0,8,0,0,0,0,0,0,0],
    ...                    [0,7,0,0,0,0,3,0,0]])
    >>> check, message = check_sudoku(sudoku, False)
    >>> print(check)
    False
    >>> print(message)
    There are too many 9's in column 7
    @endcode
    """
    # Check if the sudoku is filled completely:
    if final_check:
        if not all(x != 0 for x in np.ravel(sudoku[:][:])):
            message = "The sudoku is not solved, there are still empty cells"
            return False, message

    # Check if there are too many of the same number in a row, column or box
    # fmt: off
    for i in range(9):
        for j in range(1, 10):
            if np.count_nonzero((sudoku[i, :] == j)) > 1:
                message = "There are too many {}'s in row {}".format(j, i + 1)
                return False, message
            if np.count_nonzero((sudoku[:, i] == j)) > 1:
                message = ("There are too many"
                           + " {}'s in column {}".format(j, i + 1))
                return False, message
            for k in [1, 5, 8]:
                if np.count_nonzero((np.ravel(pp.box(sudoku, i, k)) == j)) > 1:
                    message = (
                        "There are too many "
                        + "{}'s in box ".format(j)
                        + "[{},{}]".format((i // 3) + 1, (k // 3) + 1)
                    )
                    return False, message
    # fmt: on
    return True, "_"


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

    @exception UserWarning Raised if the sudoku might have multiple solutions,
    and the backtracking algorithm will return the first it finds.
    @exception RuntimeError Raised if the sudoku is not solvable,
    already solved, or there may be a disagreement between the arguments.

    @example This example describes how to use the markup function.

    @code
    >>> sudoku = np.array([[0,0,4,0,5,0,0,7,0],
    ...                   [0,0,0,0,0,0,0,0,0],
    ...                   [0,0,0,0,0,8,0,0,0],
    ...                   [0,3,0,0,0,0,0,9,0],
    ...                   [0,0,1,0,0,0,0,0,0],
    ...                   [0,0,0,7,0,0,0,0,0],
    ...                   [0,0,0,4,6,2,0,0,0],
    ...                   [0,8,0,0,0,0,0,0,0],
    ...                   [0,7,0,0,0,0,3,0,0]])
    >>> markup_ = markup(sudoku)
    >>> print(markup_)
                             0                1                      2  \
    0        [1, 2, 3, 6, 8, 9]     [1, 2, 6, 9]                    [4]
    1  [1, 2, 3, 5, 6, 7, 8, 9]  [1, 2, 5, 6, 9]  [2, 3, 5, 6, 7, 8, 9]
    2     [1, 2, 3, 5, 6, 7, 9]  [1, 2, 5, 6, 9]     [2, 3, 5, 6, 7, 9]
    3        [2, 4, 5, 6, 7, 8]              [3]        [2, 5, 6, 7, 8]
    4     [2, 4, 5, 6, 7, 8, 9]  [2, 4, 5, 6, 9]                    [1]
    5        [2, 4, 5, 6, 8, 9]  [2, 4, 5, 6, 9]        [2, 5, 6, 8, 9]
    6              [1, 3, 5, 9]        [1, 5, 9]              [3, 5, 9]
    7     [1, 2, 3, 4, 5, 6, 9]              [8]        [2, 3, 5, 6, 9]
    8        [1, 2, 4, 5, 6, 9]      ...................................
    @endcode
    """
    try:
        # Check if the sudoku might have multiple solutions,
        # if yes, give a warning
        if np.count_nonzero(sudoku) < 17:
            message = (
                "This sudoku may have multiple solutions,"
                + " and the backtracking algorithm will"
                + " return the first it finds."
            )
            warnings.warn(message, UserWarning)

            # fmt: on
    except UserWarning as e:
        print("Traceback: ")
        traceback.print_exc()
        print("Warning:")
        print(e)

    try:
        # Check if the sudoku is already solved, if yes, raise an error
        if all(x != 0 for x in np.ravel(sudoku[:][:])):
            # fmt: off
            raise RuntimeError("All cells are filled, "
                               + "the sudoku is already solved")
    except RuntimeError as e:
        print("Traceback: ")
        traceback.print_stack()
        print("Error: ")
        print(e)
        print("Exiting program")
        sys.exit(1)

    # Create a dataframe to store the markup
    markup = pd.DataFrame(index=range(9), columns=range(9))

    # Loop through the sudoku, and for each empty cell,
    # check the row, column, and box that cell is in for values that are
    # already present, then list the possible values for that cell.
    for row in range(9):
        for col in range(9):
            if sudoku[row][col] == 0:
                set_row = set(sudoku[row, :])
                set_col = set(sudoku[:, col])
                set_box = set(np.ravel(pp.box(sudoku, row, col)))
                # fmt: off
                cell_markup = [
                    i for i in range(1, 10)
                    if i not in (set_row | set_col | set_box)
                ]
                # fmt: on
                try:
                    # If there are no possible values for the cell,
                    # raise an error
                    if cell_markup == []:
                        raise RuntimeError(
                            "There is no possible value for cell "
                            + "({},{})".format(row, col)
                            + ", hence the sudoku is not solvable"
                        )
                except RuntimeError as e:
                    print("Traceback: ")
                    traceback.print_stack()
                    print("Error: ")
                    print(e)
                    print("Exiting program")
                    sys.exit(1)

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
    and returns a solved sudoku, if possible. Using a recursive function
    structure, it iterates through the backtracking_cells list,
    and for each cell, it tries each of the possible values for that cell,
    and if it fails, it backtracks to the previous cell, and tries the next
    value for that cell, and so on. If it reaches the end of the list,
    then the sudoku is solved. If it fails at cell_num = 0, or technically
    reaches the last cell having tried all possible values for the previous
    cells, then the sudoku is not solvable.

    @param sudoku A 9x9 numpy array containing the sudoku numbers
    @param markup_ A 9x9 dataframe containing lists of possible values
    for each cell.
    @param backtrack_cells A numpy array containing the indexes of the cells
    that still have more than one possible value, in that markup file.
    @param cell_num The index of the current cell we are looking at,
    within the backtrack_cells list.

    @return A boolean, True if the sudoku is solved,
    False if it is still not solved.

    @note This function is based on the recursive function method,
    and the backtracking lecture, as described in the following webpages:
    https://www.geeksforgeeks.org/introduction-to-recursion-data-structure
    -and-algorithm-tutorials/?ref=lbp
    https://stackoverflow.com/questions/24682039/whats-the-worst-case-valid-
    sudoku-puzzle-for-simple-backtracking-brute-force-al
    https://web.stanford.edu/class/archive/cs/cs106b/cs106b.1188/lectures/
    Lecture11/Lecture11.pdf

    @note This function is also based on the following webpage:

    @exception RuntimeError Raised if the sudoku is not solvable,
    already solved, or there may be a disagreement between the arguments.

    @example This example describes how to use the backtrack_alg function.

    @code
    >>> sudoku = np.array([[0,0,4,0,5,0,0,7,0],
    ...                   [0,0,0,0,0,0,0,0,0],
    ...                   [0,0,0,0,0,8,0,0,0],
    ...                   [0,3,0,0,0,0,0,9,0],
    ...                   [0,0,1,0,0,0,0,0,0],
    ...                   [0,0,0,7,0,0,0,0,0],
    ...                   [0,0,0,4,6,2,0,0,0],
    ...                   [0,8,0,0,0,0,0,0,0],
    ...                   [0,7,0,0,0,0,3,0,0]])
    >>> markup_ = markup(sudoku)
    >>> backtrack_cells = np.where(markup_1.map(len) > 1)
    >>> backtrack_cells = np.array([backtrack_cells[1],
    ...                             backtrack_cells[0]]).T
    >>> backtrack_alg(sudoku, markup_, backtrack_cells, 0)
    True
    >>> print(sudoku)
    np.array([[1,2,4,3,5,6,8,7,9],
              [3,5,8,1,7,9,2,4,6],
              [6,9,7,2,4,8,1,3,5],
              [2,3,5,6,1,4,7,9,8],
              [7,4,1,8,9,3,5,6,2],
              [8,6,9,7,2,5,4,1,3],
              [5,1,3,9,8,7,6,2,4],
              [4,8,2,5,6,1,9,3,7],
              [9,7,6,4,3,2,8,5,1]])
    @endcode
    """

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
    set_row = set(sudoku[backtrack_cells[cell_num][1], :])
    set_col = set(sudoku[:, backtrack_cells[cell_num][0]])
    set_box = set(np.ravel(pp.box(sudoku,
                                  backtrack_cells[cell_num][1],
                                  backtrack_cells[cell_num][0])))
    valid_cell_vals = [
        x for x in backtrack_cell_vals
        if x not in (set_row | set_col | set_box)
    ]
    # fmt: on

    # If there are no valid values for the current cell, return False
    # This will trigger the backtracking, when at a level cell_num + 1.
    # If this happens at cell_num = 0, then the sudoku is not solvable.
    try:
        if valid_cell_vals == []:
            if cell_num == 0:
                raise RuntimeError(
                    "The sudoku is not solvable, already solved, or there "
                    + "may be a disagreement between the arguments, i.e. "
                    + "not being associated, check the arguments are "
                    + "from the same sudoku."
                )
            return False
    except RuntimeError as e:
        print("Traceback: ")
        traceback.print_stack()
        print("Error: ")
        print(e)
        print("Exiting program")
        sys.exit(1)

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
