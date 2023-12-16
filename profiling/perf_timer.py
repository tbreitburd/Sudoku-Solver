"""!@file perf_timer.py

@brief This file contains the code to time the performance of the
backtracking algorithm, for different types of backtracking.

@details Using functions from modules preprocessing.py and solver_tools.py,
it takes in a csv file containing a list of sudokus,
and times the performance of the backtracking algorithm
for each sudoku, for three different types of backtracking:
forward, backward and ordered.

The sudokus are solved using the backtracking algorithm,
and the time taken to solve each sudoku is recorded.
The average time taken for each type of backtracking is then printed.

@author Created by T.Breitburd on 14/12/2023
"""

from src import solver_tools as st
import numpy as np
import pandas as pd
import time
import sys

backtracking_only = sys.argv[1]

def solve_for_timing(sudoku, backtracking_type, bactrack_only):
    """!@brief Solve the sudoku.

    @details This function takes in a sudoku,
    and solves it using the backtracking algorithm.

    @param sudoku A 9x9 numpy array containing the sudoku numbers
    @param backtracking_type A string, either "forward", "backward" or
    "ordered", specifying the type of backtracking to use.

    @return None
    """

    # Create a markup dataframe of possible values for the sudoku
    # and initialise a second markup dataframe, to compare the updated markup
    # with the first one.
    if bactrack_only:
        markup_1 = st.markup(sudoku)
        for row in range(9):
                for col in range(9):
                    if len(markup_1[col][row]) == 1:
                        sudoku[row][col] = markup_1[col][row][0]
    else:
        markup_0 = st.markup(sudoku)
        markup_1 = pd.DataFrame(index=range(9), columns=range(9))

        # We want to put any unique possible value that the markup
        # finds in the sudoku.
        # And update the markup following that change,
        # until the markup doesn't change.
        while not np.array_equal(markup_0.values, markup_1.values):
            markup_0 = st.markup(sudoku)
            for row in range(9):
                for col in range(9):
                    if len(markup_0[col][row]) == 1:
                        sudoku[row][col] = markup_0[col][row][0]
            if all(x != 0 for x in np.ravel(sudoku[:][:])):
                break
            markup_1 = st.markup(sudoku)

    # Check if the sudoku is valid after the marking up
    valid, message = st.check_sudoku(sudoku, False)
    if not valid:
        # fmt: off
        raise RuntimeError("The sudoku is no longer valid after markup: "
                           + message)
        # fmt: on

    # If the sudoku is already solved by this point, print it.
    if all(x != 0 for x in np.ravel(sudoku[:][:])):
        return None
    else:
        # If the sudoku is not solved yet, we need to use backtracking.
        # Now get the indexes of the cells that still have more than
        # one possible value, based on the markup file,
        # and store them in a numpy array as pairs.
        backtrack_cells = np.where(markup_1.map(len) > 1)

        # fmt: off
        if backtracking_type == "forward":
            # Simply go from left to right, top to bottom
            backtrack_cells = np.array([backtrack_cells[1],
                                        backtrack_cells[0]]).T
        elif backtracking_type == "backward":
            # Go from right to left, bottom to top
            backtrack_cells = np.array([backtrack_cells[1],
                                        backtrack_cells[0]]).T[::-1]
        elif backtracking_type == "ordered":
            # Sort these cells by the number of possible values they have,
            # in ascending order.
            # This is to possibly make the backtracking algorithm faster.
            # From https://learnpython.com/blog/python-custom-sort-function/
            def sorting_key(cell):
                return len(markup_1[cell[0]][cell[1]])
            backtrack_cells = np.array([backtrack_cells[1],
                                        backtrack_cells[0]]).T
        # fmt: on
            backtrack_cells = sorted(backtrack_cells, key=sorting_key)

        # Now use the backtracking algorithm to solve the sudoku,
        # only going through the possible values listed in the identified cells
        # above.
        # If the algorithm is successful, print the solved sudoku.
        # Otherwise the backtracking algorithm will either raise an error or
        # return False, in which case we raise an error.
        if st.backtrack_alg(sudoku, markup_1, backtrack_cells, 0):
            valid, message = st.check_sudoku(sudoku, True)
            if not valid:
            # fmt: off
                raise RuntimeError("The sudoku is no longer valid after markup: "
                           + message)
            # fmt: on
            return None
        else:
            return None


# Read sudokus from sudokus.csv, and store them in a dataframe
sudokus_df = pd.read_csv("sudokus/sudokus.csv", header=None)
time_forward = []
time_backward = []
time_ordered = []


# Iterate over each sudoku
for backtracking_type in ["forward", "backward", "ordered"]:
    for sudoku_str in sudokus_df[0]:
        # Convert the string representation of the sudoku to a 9x9 numpy array
        sudoku = np.array([int(char) for char in sudoku_str]).reshape((9, 9))

        # Solve the sudoku using the three types of backtracking, and time it
        start_time = time.time()
        solution = solve_for_timing(sudoku, backtracking_type, backtracking_only)
        end_time = time.time()

        duration = end_time - start_time

        if backtracking_type == "forward":
            time_forward.append(duration)
        elif backtracking_type == "backward":
            time_backward.append(duration)
        elif backtracking_type == "ordered":
            time_ordered.append(duration)

# fmt: off
# Print the average time taken for each type of backtracking
print("Average time taken for forward backtracking: " +
      str(np.mean(time_forward)))
print("Average time taken for backward backtracking: " +
      str(np.mean(time_backward)))
print("Average time taken for ordered backtracking: " +
      str(np.mean(time_ordered)))
# fmt: on
