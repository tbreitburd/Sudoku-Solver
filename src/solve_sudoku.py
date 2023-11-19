"""!@file solve_sudoku.py
@brief This file contains the main sudoku solving code. .

@details Using functions from modules ..., it takes in a sudoku in txt format (with specific formatting), solves it using ..., and returns the solved sudoku in the same format as the input.
@author Created by T.Breitburd on 19/11/2023
"""

import sys
import configparser as cfg

input_file = sys.argv[1]

config = cfg.ConfigParser()
config.read(input_file)

