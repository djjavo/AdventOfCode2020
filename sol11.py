import utils
import copy


def initialiseGrid():
    global grid, rows, cols

    grid = utils.loadInputFile("input_11.txt")
    grid = [list(x) for x in grid]

    rows = len(grid)  # 31, so 30
    cols = len(grid[0])  # 323, so 322


def inBounds(row, col):
    global rows, cols
    return not (row < 0 or row > rows-1 or col < 0 or col > cols-1)


def findFirstSeat(row, col, rowStep, colStep):
    global grid

    if rowStep == 0 and colStep == 0:
        return 0

    row += rowStep
    col += colStep

    while(inBounds(row, col)):
        if grid[row][col] == "#":
            return 1
        elif grid[row][col] == "L":
            return 0
        row += rowStep
        col += colStep
    return 0


def numberOfOccupiedSeats(row, col):
    global grid, rows, cols
    numberOfOccupiedSeats = 0

    for y in [row-1, row, row+1]:
        for x in [col-1, col, col+1]:
            if inBounds(y, x):
                if not (y == row and x == col):

                    if grid[y][x] == "#":
                        numberOfOccupiedSeats += 1

    return numberOfOccupiedSeats


def numberOfOccupiedSeats2(row, col):
    global grid, rows, cols
    numberOfOccupiedSeats = 0

    for rowStep in [-1, 0, 1]:
        for colStep in [-1, 0, 1]:
            numberOfOccupiedSeats += findFirstSeat(row, col, rowStep, colStep)

    return numberOfOccupiedSeats


def processTick():
    global grid, rows, cols

    # preserve state of original grid
    localGrid = copy.deepcopy(grid)
    changeMade = False

    for col in range(0, cols):
        for row in range(0, rows):
            if grid[row][col] == "L" and numberOfOccupiedSeats(row, col) == 0:
                localGrid[row][col] = "#"
                changeMade = True
            elif grid[row][col] == "#" and numberOfOccupiedSeats(row, col) >= 4:
                localGrid[row][col] = "L"
                changeMade = True

    grid = copy.deepcopy(localGrid)
    return changeMade


def processTick2():
    global grid, rows, cols

    # preserve state of original grid
    localGrid = copy.deepcopy(grid)
    changeMade = False

    for col in range(0, cols):
        for row in range(0, rows):
            if grid[row][col] == "L" and numberOfOccupiedSeats2(row, col) == 0:
                localGrid[row][col] = "#"
                changeMade = True
            elif grid[row][col] == "#" and numberOfOccupiedSeats2(row, col) >= 5:
                localGrid[row][col] = "L"
                changeMade = True

    grid = copy.deepcopy(localGrid)
    return changeMade


def printGrid():
    global grid, rows

    print("-" * rows)
    for row in grid:
        for col in row:
            print(col, end="")
        print()


def part1():
    for i in range(0, 1000000):
        # printGrid()
        changed = processTick()
        if not changed:
            return sum([row.count("#") for row in grid])

    return -1


def part2():
    for i in range(0, 1000000):
        # printGrid()
        changed = processTick2()
        if not changed:
            return sum([row.count("#") for row in grid])

    return -1


initialiseGrid()
print(part1())  # 2344
initialiseGrid()
print(part2())  # 2076
