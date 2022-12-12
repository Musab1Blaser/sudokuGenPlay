#please make sure to run sudokuGenerator fully at least once before running the player, else there will be a file not found exception

import colorama
from termcolor import cprint

colorama.init(autoreset = True)

def readGrid(file):
    grid = []
    fhand = open(file)
    for line in fhand:
        #stores each line in a separate list
        #each value of each line is a different element
        if len(line) <= 1: #ignore empty lines
            continue
        grid.append([i for i in line.strip() if i not in " "])
    return grid

# print out the line with properly spaced column numbers so that the grid is easier to read
def displayColNums():
    print("    ", end = "")
    for i in range(9):
        print(i+1, end = " ")
        if (i+1) % 3 == 0:
                print("  ", end = "")
    print()

# print out each line of the sudoku, with the format
# r | _ _ _ | _ _ _ | _ _ _ | r, where r is row number and _ is value
def displayLine(row, vals, colours, boundaryColour):
    #row contains row number
    #vals contains the list of values for a row 1-9 and _
    #colours stores the colour for each value
    print(row + 1, end = " ")
    cprint("|", boundaryColour, end = " ")
    for i in range(len(vals)):
        cprint(vals[i], colours[i], end=" ")
        if (i+1) % 3 == 0:
            cprint("|", boundaryColour, end = " ")
    print(row + 1)

# print out the entire current sudoku grid with appropriate colouring
# colouring is defined as follows: all green for solved grid; or yellow for fixed and cyan for changeable
def displayGrid(currentGrid, fixedVals, fixedColour, addedColour, boundaryColour):
    displayColNums()

    #prints boundaries above and below boxes
    boundaries = "  " + ("-" * 25)
    cprint(boundaries, boundaryColour)

    for row in range(9):
        vals = currentGrid[row]
        colours = []
        #assign colour for each value based on whether game has been won or whether it was fixed or changeable
        for col in range(9):
            if [row, col] in fixedVals:
                colours.append(fixedColour)
            else:
                colours.append(addedColour)
        displayLine(row, vals, colours, boundaryColour)
        if (row + 1) % 3 == 0:
            #prints boundaries above and below boxes
            cprint(boundaries, boundaryColour)

    displayColNums()
    
def takeInput(s):
    #validates input to be between 1 and 9 inclusive
    while True:
        try:
            pos = int(input(f"Enter a valid {s}: "))
            if 1 <= pos <= 9:
                return pos
        except:
            pass

def updateGrid(currentGrid, fixedVals):
    #show grid, ask for position to change, if position is fixed then repeat
    while True:
        displayGrid(currentGrid, fixedVals, "yellow", "cyan", "white")
        print()

        row = takeInput("row number") - 1
        col = takeInput("column number") - 1
        
        if [row, col] not in fixedVals:
            break
        else:
            cprint("This position contains a fixed value. Please pick a different position!", "red")
            print()

    val = takeInput("value to place")
    currentGrid[row][col] = str(val) #update grid
    print()

# check if all values of the current grid match the target grid
def checkGrid(currentGrid, targetGrid, fixedVals):
    for row in range(9):
        for col in range(9):
            if currentGrid[row][col] != targetGrid[row][col]:
                return False
    else:
        #if vals match then print winning grid and message
        displayGrid(currentGrid, fixedVals, "green", "green", "green")
        print()
        cprint("           YOU WON!", "green")
        print()
        return True

# values in grid can be accessed by currentGrid[row][col] where both row and col are 0-indexed
currentGrid = readGrid("sudokuPuzzles.txt")
targetGrid = readGrid("sudokuSolutions.txt")

# create a list of values that the player can not change (those that were set by default)
fixedVals = []
for row in range(9):
    for col in range(9):
        if currentGrid[row][col] != "_":
            fixedVals.append([row, col])

# until the puzzle is solved, let the player keep tring
while not(checkGrid(currentGrid, targetGrid, fixedVals)):
    updateGrid(currentGrid, fixedVals)

