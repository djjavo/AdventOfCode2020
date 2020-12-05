import utils


def initialiseGrid():
    global grid, rows, cols

    grid = utils.loadInputFile("input_3.txt")

    rows = len(grid)-1  # 31, so 30
    cols = len(grid[0])-1  # 323, so 322


def computeTreeCollisionsWithSlope(deltaX, deltaY):
    global grid, rows, cols

    # initialise
    currentX = 0
    currentY = 0
    treesEncountered = 0

    while currentY < rows:
        currentX += deltaX
        currentY += deltaY

        # wrap around when exceeded
        if currentX > cols:
            currentX -= 31

        # safety check
        if currentY > rows:
            return treesEncountered

        if grid[currentY][currentX] == "#":
            treesEncountered += 1

    return treesEncountered


def part1():
    return computeTreeCollisionsWithSlope(3, 1)


def part2():
    result = 1
    for x, y in [[1, 1], [3, 1], [5, 1], [7, 1], [1, 2]]:
        result *= computeTreeCollisionsWithSlope(x, y)
    return result


initialiseGrid()
print(part1())
print(part2())
