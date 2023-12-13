"""!@file solve_sudoku.py
@brief This file contains the main sudoku solving code. .

@details Using functions from modules ...,
it takes in a sudoku in txt format (with specific formatting),
solves it using ...,
and returns the solved sudoku in the same format as the input.
@author Created by T.Breitburd on 19/11/2023
"""

import sys
import numpy as np
import pandas as pd
from . import preprocessing as preproc
from . import solver_tools as st
import time
import os

input_file = sys.argv[1]


def solve_sudoku(input_file):
    input_path = input_file
    # Load the sudoku from its txt file to a 9x9 numpy array
    sudoku = preproc.load_sudoku(input_path)

    # Check if the sudoku is valid
    valid, message = st.check_sudoku(sudoku)
    if not valid:
        # fmt: off
        raise RuntimeError("The sudoku is not valid at loading time: "
                           + message)
        # fmt: on

    # Create a markup dataframe of possible values for the sudoku
    # and initialise a second markup dataframe, to compare the updated markup
    # with the first one.
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
    valid, message = st.check_sudoku(sudoku)
    if not valid:
        # fmt: off
        raise RuntimeError("The sudoku is no longer valid after markup: "
                           + message)
        # fmt: on

    # If the sudoku is already solved by this point, print it.
    if all(x != 0 for x in np.ravel(sudoku[:][:])):
        solved_sudoku_str = preproc.sudoku_to_output_format(sudoku)
        print(solved_sudoku_str)
    else:
        # If the sudoku is not solved yet, we need to use backtracking.
        # Now get the indexes of the cells that still have more than
        # one possible value, based on the markup file,
        # and store them in a numpy array as pairs.
        backtrack_cells = np.where(markup_1.map(len) > 1)
        backtrack_cells = np.array([backtrack_cells[1], backtrack_cells[0]]).T

        # Sort these cells by the number of possible values they have,
        # in ascending order.
        # This is to make the backtracking more efficient.
        # From https://learnpython.com/blog/python-custom-sort-function/
        def sorting_key(cell):
            return len(markup_1[cell[1]][cell[0]])

        backtrack_cells = sorted(backtrack_cells, key=sorting_key)

        # Now use a backtracking algorithm to solve the sudoku,
        # only going through the possible values listed in the identified cells
        # above.
        # If the algorithm is successful, print the solved sudoku.
        if st.backtrack_alg(sudoku, markup_1, backtrack_cells, 0):
            solved_sudoku_str = preproc.sudoku_to_output_format(sudoku)
            print(solved_sudoku_str)

    # Check if the sudoku is valid after the backtracking
    valid, message = st.check_sudoku(sudoku)
    if not valid:
        raise RuntimeError(
            "The sudoku is no longer valid after backtracking: " + message
        )

    # Finally, write the solved sudoku to the output file
    # creating the output directory if it doesn't exist yet
    output_file = input_file.split("/")[-1]
    output_dir = "sudoku_solutions"
    output_path = os.path.join(output_dir, output_file)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_path, "w") as file:
        file.write(solved_sudoku_str)


start = time.time()

solve_sudoku(input_file)

end = time.time()

print(f"Elapsed time: {end - start} seconds")
