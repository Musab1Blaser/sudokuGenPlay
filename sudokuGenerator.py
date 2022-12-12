import random

# Checks current row, column and box for values being used (ignores "_"). Returns list of values used
def getUsedElems(grid, rowIndex, colIndex):
    usedElems = []
    for i in range(9):
        val = grid[rowIndex][i]
        if val != "_" and val not in usedElems:
            usedElems.append(val)

        val = grid[i][colIndex]
        if val != "_" and val not in usedElems:
            usedElems.append(val)
    
    boxStart = [3 * (rowIndex // 3), 3 * (colIndex // 3)]
    for i in range(3):
        for j in range(3):
            val = grid[boxStart[0] + i][boxStart[1] + j]
            if val != "_" and val not in usedElems:
                usedElems.append(val)

    return usedElems

# Takes list of values used and creates a list of unused/remaining values
def getRemaining(usedElems):
    remaining = [str(i+1) for i in range(9)]
    for i in usedElems:
        if i in remaining:
            remaining.remove(i)
    return remaining

# generate a valid filled sudoku and store it in grid.
def generateSudoku(grid, pos):
    #pos is counted from left to right and then top to down starting from 0 at the top left. 1 is the square to the right of top left. 9 is the square below the top left.
    if pos == 81: #if all cells from top left to bottom right satisfied, return grid
        return True

    rowIndex = pos // 9
    colIndex = pos % 9
    
    usedElems = getUsedElems(grid, rowIndex, colIndex)
    remaining = getRemaining(usedElems)
    if len(remaining) == 0: #if no values can be entered in the current position, so no solutions possible for existing grid. Backtrack to try a new grid
        return False
    sample = random.sample(remaining, len(remaining)) #randomise numbers to be substituted
    
    for val in sample: #try each value for each position until a solution is found
        grid[rowIndex][colIndex] = val
        if generateSudoku(grid, pos + 1) == True: #if current value at current position gives a valid grid, return the grid
            return True

    #if no solutions exist for current sudoku, set current position back to "_" and go one step back (back track)
    grid[rowIndex][colIndex] = "_"
    return False

def findSols(grid, toSubstitute):
    global solutions
    if len(toSubstitute) == 0: #if nothing else left to substitute - grid completed
        solutions += 1
        if solutions > 1: 
            return -1 # too many solutions, sudoku is ambiguous
        else:
            return 0

    pos = toSubstitute[0]
    rowIndex = pos // 9
    colIndex = pos % 9
    
    usedElems = getUsedElems(grid, rowIndex, colIndex)
    remaining = getRemaining(usedElems)
    if len(remaining) == 0: #if no options left to try, backtrack to previous substitution
        return 0

    for val in remaining: #try every possible value for current position and check if this new grid is solvable
        grid[rowIndex][colIndex] = val
        if findSols(grid, toSubstitute[1:]) == -1: #if more than 1 solution found, bubble -1 to original function call
            return -1

    #if no solutions exist for current sudoku, set current position back to "_" and go one step back
    grid[rowIndex][colIndex] = "_"
    return

#removes random clues from the grid as long as 1 solution is possible, or maxDifficulty number of clues have been removed
def makePuzzle(grid, maxDifficulty):
    global solutions
    posList = list(range(81))
    toSubstitute = []

    sample = random.sample(posList, maxDifficulty) #create a random list of clues to remove
    for pos in sample:
        rowIndex = pos // 9
        colIndex = pos % 9

        prevGrid = [row[:] for row in grid]

        grid[rowIndex][colIndex] = "_"
        toSubstitute.append(pos)

        solutions = 0 #note at least 1 solution will exist since we started from a valid grid
        solutionFlag = findSols(grid, toSubstitute) 
    
        if solutionFlag == -1: #if more than 1 solution possible, then return previous grid (that only had 1 solution)
            print(f"Clues Removed: {len(toSubstitute) - 1}")
            return prevGrid
    print(f"Clues Removed: {len(toSubstitute)}")
    return grid

#function for testing, makes sure that the generated complete grid is valid
def checker(grid):
    for row in range(9):
        usedElems = []
        for col in range(9):
            val = grid[row][col]
            if val in usedElems:
                print(f"ERROR at ({row}, {col})")
            else:
                usedElems.append(val)
    for col in range(9):
        usedElems = []
        for row in range(9):
            val = grid[row][col]
            if val in usedElems:
                print(f"ERROR at ({row}, {col})")
            else:
                usedElems.append(val)
    for rowIndex in range(0,9,3):
        for colIndex in range(0,9,3):
            usedElems = []
            for j in range(3):
                for k in range(3):
                    val = grid[rowIndex+j][colIndex+k]
                    if val in usedElems:
                        print(f"ERROR at ({rowIndex}, {colIndex})")
                    else:
                        usedElems.append(val)

# copies the contents of the grid into a file for use by sudokuPlayer
def grid2File(grid, filename):
    fhand = open(filename, "w")
    for row in range(9):
        if row != 0:
            fhand.write("\n")
        if row % 3 == 0 and row != 0:
            fhand.write("\n")

        for col in range(9):
            if col % 3 == 0 and col != 0:
                fhand.write(" ")

            fhand.write(grid[row][col])

#initialisation
solutionGrid = []
for i in range(9):
    solutionGrid.append(["_"]*9)

#generate complete grid and display it
generateSudoku(solutionGrid, 0)
for i in solutionGrid:
    print(i)

puzzleGrid = [row[:] for row in solutionGrid]
#specify maximum number of clues to be removed
maxDifficulty = min(81,int(input("Specify maximum difficulty (amount of clues removed): ")))
puzzleGrid = makePuzzle(puzzleGrid, maxDifficulty)

#show puzzleGrid
for i in puzzleGrid:
    print(i)

grid2File(solutionGrid, "sudokuSolutions.txt")
grid2File(puzzleGrid, "sudokuPuzzles.txt")