1. We plan to use a constraint-based approach combined with a bactracking algorithm if the constraint based approach is insufficient.  
2. Just like when solving a sudoku by brain-power, we can scan the empty cells of the sudoku and see if any have enough constraints set on them that they can only have one solution. Taking the example in the instructions, the case (1,7) can be {2,3,7,8} from the constraints of the box. Then we see that the first row already has 7, and that the 7th column has 2 and 3  in the box below. Thus, the only possible value is 8. This is a "
3. Applying this at the start, we might gain some time on a pure backtracking method.  

The simplified algorithm then can be done as follows:  
- Mark up every empty cell with their possible values based on sudoku constraints
- If there are cells with just one markup value, then put that write that value down.
- Update the markups
- Repeat step 3 and 4 until there are no more single markups
- From there, apply the backtracking algorithm, going through only the markup values (i.e. not a completely naïve backtracking algorithm)

In terms of coding, this means:

1. First, taking the input sudoku in its text form and put the values into a 9x9 numpy array. This has the advantage of numpy's single type constraint, creating an error if a non-integer is entered.
2. Creating constraint evaluating functions, to check for impossible values in rows, columns and boxes. Concerning the checking of the box, it might be worth considering them as separate objects, rather than a complex index else-if statement.
3. For the marking up, it seems practicle to create a separate 3D array, possibly a pandas dataframe as it will possibly have a different size for each cell, it will have size [[9]x[9]x[number of markups]]
4. Check for any cell having only one possible value of markups
5. Try to have a markup updating function, rather than re-running the marking up function altogether
6. Once the update returns a markup dataframe with no single-markup options, we can move on to the backtracking algorithm.
7. The backtracking algorithm will go throught the still empty cells, and follow the standard bactracking algorithm step, but going through the values from the markup dataframe. `Because the mark up dataframe will possibly need updating once one value is tested, we will create a separate backtracking markup file, which will be updated (using the same updateign function)`: 
    1. Enumerate the empty cells from left to right and top to bottom
    2. Start with the first empty cell
    3. Enter the first value of the markup possibilities into the current cell. Check that it doesnt break any sudoku constraints. If it does move on to the next value and repeat the test until the value either works or is the last possible value. If none of the values work, stop the run and return a detailed error message
    4. Move on to the next empty cell and repeat step 3. This time if none of the values work, we bactrack to the previous cell.
    5. Repeat steps 3-4 for the current cell you're in and it's previous one.
    6. If the current cell is the last one, then the sudoku is solved and we should output it.
8. Once our code deems the sudoku solved, we can use a function to create an output txt file in the same form as the input.



