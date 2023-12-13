import cProfile
import pstats
import io
import os
import numpy as np
import pandas as pd
import warnings

input_file = "sudokus/sudoku1.txt"


def load_sudoku(path):
    """!@brief Load the sudoku txt file into a useable array

    @details This function takes in a path to a sudoku txt file,
    reads the file into a series of strings for each row,
    checks that the file has the correct format,
    then picks out the numbers from the strings, dropping the separators,
    and returns a 9x9 numpy array of the sudoku.

    @param path Path to the sudoku txt file

    @return A 9x9 numpy array containing the sudoku numbers
    """
    # We use os to have relative paths be portable
    proj_dir = os.getcwd()
    sudoku_path = os.path.join(proj_dir, path)

    # Read the sudoku file, and drop the separator lines
    try:
        f = open(sudoku_path, "r")
    except FileNotFoundError:
        raise FileNotFoundError(
            "The sudoku file was not found at the path: " + sudoku_path
        )

    sudoku_rows = f.readlines()

    # Check that the sudoku file has the correct format:
    # There should be 11 rows
    if len(sudoku_rows) != 11:
        raise ValueError(
            "The sudoku in text form has an incorrect number "
            + "of rows, should be 11 but is "
            + str(len(sudoku_rows))
        )
    # 12 columns for the first 9 rows (9 + 2 separators + new line character)
    len_rows = [len(char) for char in sudoku_rows]
    if not all(x == 12 for x in len_rows[:10]):
        raise ValueError(
            "The sudoku in text form has an incorrect number "
            + "of columns, should be 12 but is "
            + str(len_rows[:10])
        )
    # horizontal separators should be "---+---+---\n"
    if sudoku_rows[3] != "---+---+---\n" and sudoku_rows[7] != "---+---+---\n":
        raise ValueError(
            "The sudoku file has incorrect "
            + "horizontal separators, must be ---+---+---"
        )

    # Drop the horizontal separator lines
    sudoku_rows = sudoku_rows[0:3] + sudoku_rows[4:7] + sudoku_rows[8:11]

    # Check that the sudoku rows have the correct format,
    # with vertical separators at specific positions
    InRowSep = [char[3] for char in sudoku_rows]
    InRowSep2 = [char[7] for char in sudoku_rows]
    if not all(x == "|" for x in InRowSep + InRowSep2):
        raise ValueError(
            "The sudoku file has incorrect vertical separators" + ", must be |"
        )

    # Initialize the sudoku array
    sudoku = np.zeros((9, 9), dtype=int)

    # Remove the "new line" characters and the vertical separators,
    # and add those rows to the sudoku array
    for row_num, row in enumerate(sudoku_rows, 1):
        row = [x for x in row if x != "\n" and x != "|"]
        sudoku[row_num - 1] = row
    return sudoku


def box(sudoku, row, col):
    """!@brief This function takes in a sudoku and a cell's row and column,
    and returns a 3x3 array of the sudoku box that cell is in.

    @details The function takes in a sudoku and a cell's row and column,
    and returns a 3x3 array of the sudoku box that cell is in.

    @param sudoku The sudoku to extract the box from
    @param row The row of the cell, 0 indexed
    @param col The column of the cell, 0 indexed

    @return A 3x3 array of the corresponding box.
    """
    # Check that the cell coordinates are valid
    if row < 0 or row > 8 or col < 0 or col > 8:
        raise ValueError(
            "The cell coordinates are not valid, "
            + "must be between 0 and 8 inclusive but:"
            + "Row: "
            + str(row)
            + ", Col: "
            + str(col)
        )

    # Initialize box array
    box = np.zeros((3, 3))
    # Identify the box's box-coordinates (tuples of 1, 2 or 3)
    box_row = int((row + 3) // 3)
    box_col = int((col + 3) // 3)

    # Get the box values
    row_start = int(3 * (box_row - 1))
    row_end = int(row_start + 3)

    col_start = int(3 * (box_col - 1))
    col_end = int(col_start + 3)

    # fmt: off
    # This line caused black/flake8 conflicts
    box = [sudoku[i][col_start:col_end] for i in range(row_start, row_end)]
    # fmt: on

    return box


def check_sudoku(sudoku):
    """!@brief Check if the sudoku is valid.

    @details This function takes in a sudoku,
    and checks if it is valid, i.e. a maximum of one of each number
    in each row, column and box.

    @param sudoku A 9x9 numpy array containing the sudoku numbers

    @return A boolean, True if the sudoku is valid, False if it is not.
    And a string, containing a message explaining why the sudoku is not valid.
    """

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
                if np.count_nonzero((np.ravel(box(sudoku, i, k)) == j)) > 1:
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
    sudoku_vals = set(np.ravel(sudoku[:][:]))
    if all(x != 0 for x in sudoku_vals):
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
                set_row = set(sudoku[row, :])
                set_col = set(sudoku[:, col])
                set_box = set(np.ravel(box(sudoku, row, col)))
                # fmt: off
                cell_markup = [
                    i for i in range(1, 10)
                    if i not in (set_row | set_col | set_box)
                ]
                # fmt: on

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
                            box(
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


sudoku = load_sudoku(input_file)

pr = cProfile.Profile()
pr.enable()

markup1 = markup(sudoku)

pr.disable()
s = io.StringIO()
sortby = "cumulative"
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())

with open("profile.txt", "w+") as file:
    file.write(s.getvalue())

print(markup1)
