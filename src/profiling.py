from . import preprocessing as pp
import cProfile
import pstats
import io

input_file = "sudokus/sudoku_near_empty.txt"

pr = cProfile.Profile()
pr.enable()

sudoku = pp.load_sudoku(input_file)

pr.disable()
s = io.StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats("cumulative")
ps.print_stats()

with open("profile.txt", "w+") as file:
    file.write(s.getvalue())
