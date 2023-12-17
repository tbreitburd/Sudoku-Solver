"""!@file solve_sudoku.py
@brief Sudoku solver using backtracking algorithm.

@details Using functions from modules preprocessing.py and solver_tools.py,
it takes in a sudoku in txt format (with specific formatting) as input,
as well as a backtracking type (forward, backward or ordered), and a boolean
indicating whether to use only backtracking or not. The solver then
solves it using a backtracking algorithm, and optionaly a candidate
checking method. It then returns the solved sudoku in the same format
as the input, printing it to the console and writing it to a txt file,
in a directory called "sudoku_solutions".

@author Created by T.Breitburd on 19/11/2023
"""

import sys
import numpy as np
import pandas as pd
from . import preprocessing as preproc
from . import solver_tools as st
import time
import os

# Get the input file path, backtracking type and bactracking_only boolean
# from the command line
input_file = sys.argv[1]
backtracking_type = sys.argv[2]
bactracking_only = sys.argv[3]


def solve_sudoku(input_file, backtracking_type, bactracking_only):
    """!@brief Solve a sudoku using backtracking algorithm.

    @details This function takes in a sudoku in txt format (with specific
    formatting) as input, as well as a backtracking type (forward, backward
    or ordered), and a boolean indicating whether to use only backtracking
    or not. The solver then solves it using a backtracking algorithm, and
    optionaly a candidate checking method. It then returns the solved sudoku
    in the same format as the input, printing it to the console and writing
    it to a txt file, in a directory called "sudoku_solutions".

    @param input_file Path to the sudoku txt file
    @param backtracking_type Type of backtracking to use (forward, backward
    or ordered)
    @param bactracking_only Boolean indicating whether to use only
    backtracking or not

    @return Prints the solved sudoku to the console, and writes it to a txt
    file in a directory called "sudoku_solutions"

    @exception RuntimeError Raised if the sudoku is not valid at loading time,
    after markup, or after backtracking.
    @exception RuntimeError Raised if the backtracking algorithm fails to
    solve the sudoku.

    @example This example describes how to use the solve_sudoku function,
    within a python script.

    @code
    $ cat path/to/sudoku.txt
    104|050|070
    050|100|000
    000|008|005
    ---+---+---
    030|014|090
    001|000|502
    000|700|010
    ---+---+---
    003|462|000
    080|030|000
    070|501|300

    >>> solve_sudoku("path/to/sudoku.txt", "ordered", True)
    124|356|879
    358|179|246
    697|248|135
    ---+---+---
    235|614|798
    741|893|562
    869|725|413
    ---+---+---
    513|462|987
    482|937|651
    976|581|324
    Elapsed time: 0.0856376330 seconds
    @endcode
    """

    input_path = input_file
    # Load the sudoku from its txt file to a 9x9 numpy array
    sudoku = preproc.load_sudoku(input_path)

    # Check if the sudoku is valid
    valid, message = st.check_sudoku(sudoku, False)
    if not valid:
        # fmt: off
        raise RuntimeError("The sudoku is not valid at loading time: "
                           + message)
        # fmt: on

    # Create a markup dataframe of possible values for the sudoku
    # if Bactracking_only: initialise a second markup dataframe,
    # to compare the updated markup with the first one.

    if bactracking_only:
        # We want to put any unique possible value that the markup
        # finds in the sudoku.
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
                if len(markup_1[col][row]) == 1:
                    sudoku[row][col] = markup_1[col][row][0]
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
        solved_sudoku_str = preproc.sudoku_to_output_format(sudoku)
        print(solved_sudoku_str)
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
            # and https://stackoverflow.com/questions/1518346/optimizing-the-
            # backtracking-algorithm-solving-sudoku
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
            solved_sudoku_str = preproc.sudoku_to_output_format(sudoku)
            print(solved_sudoku_str)
        else:
            print("The backtracking algorithm failed to solve the sudoku. " +
                  "Please try a different backtracking type. " +
                  "if the issue persists, the sudoku may be unsolvable."
                  )

    # Check if the sudoku is valid after the backtracking
    valid, message = st.check_sudoku(sudoku, True)
    if not valid:
        # fmt: off
        raise RuntimeError("The sudoku is no longer valid or not yet solved"
                           + " after backtracking: "
                           + message
                           )
        # fmt: on

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

solve_sudoku(input_file, backtracking_type, bactracking_only)

end = time.time()

print(f"Elapsed time: {end - start} seconds")
