"""!@file test_preproc.py

@brief Module containing tests for the preprocessing module.

@details This module contains tests for the preprocessing module. The
preprocessing module contains functions used to preprocess a sudoku before
solving it. The preprocessing module contains the following functions:
load_sudoku, box, sudoku_to_output_format.

The load_sudoku function is used to load a sudoku from a text file. The text
file must contain 9 lines of 9 characters each. Each character must be a digit
between 0 and 9. The digit 0 represents an empty cell in the sudoku.

The box function is used to extract a 3x3 box from a sudoku. The box is
specified by its row and column number.

The sudoku_to_output_format function is used to convert a sudoku to a string
with the following format:
000|007|000
000|009|504
000|050|169
---+---+---
080|000|305
075|000|290
406|000|080
---+---+---
762|080|000
103|900|000
000|600|000

@author Created by T.Breitburd on 26/11/2023
"""
from src import preprocessing
import numpy as np
import unittest


def test_load_sudoku():
    """@brief Test the load_sudoku function on a sudoku.

    @details The load_sudoku function should return a 9x9 numpy array
    representing the sudoku.
    """

    np.array_equal(
        preprocessing.load_sudoku("sudokus/sudoku1.txt"),
        [
            [0, 0, 0, 0, 0, 7, 0, 0, 0],
            [0, 0, 0, 0, 0, 9, 5, 0, 4],
            [0, 0, 0, 0, 5, 0, 1, 6, 9],
            [0, 8, 0, 0, 0, 0, 3, 0, 5],
            [0, 7, 5, 0, 0, 0, 2, 9, 0],
            [4, 0, 6, 0, 0, 0, 0, 8, 0],
            [7, 6, 2, 0, 8, 0, 0, 0, 0],
            [1, 0, 3, 9, 0, 0, 0, 0, 0],
            [0, 0, 0, 6, 0, 0, 0, 0, 0],
        ],
    )


class TestLoadFunction(unittest.TestCase):
    def test_load_sudoku2(self):
        """@brief Test the load_sudoku function on a sudoku with an invalid
        format.

        @details The load_sudoku function should raise a SystemExit with exit
        code 1.
        """
        # Test that a certain input triggers SystemExit with exit code 1
        with self.assertRaises(SystemExit) as context:
            preprocessing.load_sudoku("sudokus/bad_format_sudoku.txt")

        # Check the exit code
        self.assertEqual(context.exception.code, 1)


sudoku = np.array(
    [
        [0, 0, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 0, 9, 5, 0, 4],
        [0, 0, 0, 0, 5, 0, 1, 6, 9],
        [0, 8, 0, 0, 0, 0, 3, 0, 5],
        [0, 7, 5, 0, 0, 0, 2, 9, 0],
        [4, 0, 6, 0, 0, 0, 0, 8, 0],
        [7, 6, 2, 0, 8, 0, 0, 0, 0],
        [1, 0, 3, 9, 0, 0, 0, 0, 0],
        [0, 0, 0, 6, 0, 0, 0, 0, 0],
    ]
)


def test_box():
    """@brief Test the box function on a sudoku.

    @details The box function should return a 3x3 numpy array representing the
    box.
    """
    # fmt: off
    assert np.array_equal(
        preprocessing.box(sudoku, 1, 5), np.array([[0, 0, 7],
                                                   [0, 0, 9],
                                                   [0, 5, 0]])
    )
    # fmt: on


class TestBox(unittest.TestCase):
    """@brief Test the box function on a sudoku with an invalid box number.

    @details The box function should raise a SystemExit with exit code 1.
    """

    def test_box2(self):
        # Test that a certain input triggers SystemExit with exit code 1
        with self.assertRaises(SystemExit) as context:
            preprocessing.box(sudoku, 1, 10)

        # Check the exit code
        self.assertEqual(context.exception.code, 1)


def test_sudoku_to_output_format():
    """@brief Test the sudoku_to_output_format function on a sudoku.

    @details The sudoku_to_output_format function should return a string
    representing the sudoku.
    """
    assert preprocessing.sudoku_to_output_format(sudoku) == (
        "000|007|000\n"
        "000|009|504\n"
        "000|050|169\n"
        "---+---+---\n"
        "080|000|305\n"
        "075|000|290\n"
        "406|000|080\n"
        "---+---+---\n"
        "762|080|000\n"
        "103|900|000\n"
        "000|600|000"
    )
