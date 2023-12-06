"""!@file solve_sudoku.py
@brief This file contains the main sudoku solving code. .

@details Using functions from modules ...,
it takes in a sudoku in txt format (with specific formatting),
solves it using ...,
and returns the solved sudoku in the same format as the input.
@author Created by T.Breitburd on 19/11/2023
"""

import sys
import configparser as cfg
import numpy as np
import pandas as pd
from . import preprocessing as preproc
from . import solver_tools as st

input_file = sys.argv[1]

config = cfg.ConfigParser()
config.read(input_file)


# Load the sudoku from its txt file to a 9x9 numpy array
sudoku = preproc.load_sudoku(config["Input"]["sudoku_near_empty"])

# Create a markup dataframe of possible values for the sudoku
# and initialise a second markup dataframe, to compare the updated markup
# with the first one.
markup_0 = st.markup(sudoku)
markup_1 = pd.DataFrame(index=range(9), columns=range(9))


# We want to put any unique possible value that the markup finds in the sudoku.
# And update the markup following that change, until the markup doesn't change.
while not np.array_equal(markup_0.values, markup_1.values):
    markup_0 = st.markup(sudoku)
    for row in range(9):
        for col in range(9):
            if len(markup_0[col][row]) == 1:
                sudoku[row][col] = markup_0[col][row][0]
    if all(x != 0 for x in np.ravel(sudoku[:][:])):
        break
    markup_1 = st.markup(sudoku)


# Now get the indexes of the cells that have more than one possible value,
# based on the markup file, and store them in a numpy array as pairs.
backtrack_cells = np.where(markup_1.map(len) > 1)
backtrack_cells = np.array([backtrack_cells[1], backtrack_cells[0]]).T


# Now use a backtracking algorithm to solve the sudoku,
# only going through the possible values listed in the identified cells above.
# If the algorithm is successful, print the solved sudoku.
if st.backtrack_alg(sudoku, markup_1, backtrack_cells, 0):
    solved_sudoku_str = preproc.sudoku_to_output_format(sudoku)
    print(solved_sudoku_str)
else:
    print("Something went wrong")


# Finally, write the solved sudoku to the output file
output_file = config["Output"]["sudoku_near_empty"]

with open(output_file, "w") as file:
    file.write(solved_sudoku_str)
