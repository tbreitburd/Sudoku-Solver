"""@file profiling.py
@brief This file contains the code to conduct profiling on the
sudoku solver, and its different functions.

@author Created by T.Breitburd on 12/2023
"""

import cProfile
import pstats
import io
import os
import numpy as np
import pandas as pd
from ..src import preprocessing as preproc
from ..src import solver_tools as st
from ..src import solve_sudoku as ss
import warnings
import sys

input_file = sys.argv[1]
backtracking_type = sys.argv[2]
bactracking_only = sys.argv[3]

#sudoku = preproc.load_sudoku(input_file)
#markup = st.markup(sudoku)
#backtrack_cells = np.where(markup_1.map(len) > 1)
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
#backtrack_cells = np.where(sudoku == 

pr = cProfile.Profile()
pr.enable()

#sudoku = preproc.load_sudoku(input_file)
#valid, message = st.check_sudoku(sudoku, False)
#markup1 = markup(sudoku)
#box = st.box(sudoku, 2, 3)
#backtrack_alg(sudoku, markup, backtrack_cells, 0)
ss.solve_sudoku(input_file, backtracking_type, bactracking_only)

pr.disable()
s = io.StringIO()
sortby = "cumulative"
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())

with open("/profiling/profile.txt", "w+") as file:
    file.write(s.getvalue())
