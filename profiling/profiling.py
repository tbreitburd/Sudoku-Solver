"""!@file profiling.py
@brief This file contains the code to conduct profiling on the
sudoku solver, and its different functions.

@details Using functions from modules preprocessing.py and solver_tools.py,
it takes in the same arguments as when running the solver from the command
line, the input file path, the backtracking type adn whether to only use
backtracking or not. It then profiles the performance of the solver,
using the cProfile module. It then prints the profiling results to the
console, and writes them to a txt file in a directory called "profile".
On can set it up to profile different functions, by commenting out the
functions that are not to be profiled.

@example This file can be run from the command line as follows:
@code
>>> $ python -m profiling.profiling path/to/sudoku.txt 'forward' False
@endcode

@author Created by T.Breitburd on 12/2023
"""

import cProfile
import pstats
import io

# import os
# import numpy as np
# import pandas as pd
# import warnings
import sys

# from src import preprocessing as preproc
# from src import solver_tools as st
from src import solve_sudoku as ss

# Setting the arguments to be used in the solver, as it is profiled
input_file = sys.argv[1]
backtracking_type = sys.argv[2]
bactracking_only = sys.argv[3]


# ----------------- For profiling individual functions -----------------
# ---------- Uncomment as needed to profile the backtrack_alg----------

# sudoku = preproc.load_sudoku(input_file)
# markup = st.markup(sudoku)
# backtrack_cells = np.where(markup_1.map(len) > 1)
#
#        # fmt: off
# Simply go from left to right, top to bottom
#        if backtracking_type == "forward":
#                                       backtrack_cells[0]]).T
#            backtrack_cells = np.array([backtrack_cells[1],
#        elif backtracking_type == "backward":
#            # Go from right to left, bottom to top
#            backtrack_cells = np.array([backtrack_cells[1],
#                                        backtrack_cells[0]]).T[::-1]
#        elif backtracking_type == "ordered":
#            def sorting_key(cell):
#                return len(markup_1[cell[0]][cell[1]])
#            backtrack_cells = np.array([backtrack_cells[1],
#                                        backtrack_cells[0]]).T
# fmt: on
#            backtrack_cells = sorted(backtrack_cells, key=sorting_key)


# --------------------------- Profiling -------------------------
# ---------- Uncomment as needed to profile the solver ----------
pr = cProfile.Profile()
pr.enable()

# sudoku = preproc.load_sudoku(input_file)
# valid, message = st.check_sudoku(sudoku, False)
# markup1 = markup(sudoku)
# box = st.box(sudoku, 2, 3)
# backtrack_alg(sudoku, markup, backtrack_cells, 0)
ss.solve_sudoku(input_file, backtracking_type, bactracking_only)

pr.disable()
s = io.StringIO()
sortby = "cumulative"

# Print the profiling results to the console
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())

# Write the profiling results to a txt file as well
with open("profiling/profile.txt", "w+") as file:
    file.write(s.getvalue())
