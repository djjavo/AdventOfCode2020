import utils
import re


def initialise():
    global instructions

    instructions = utils.loadInputFile("input_24.txt")

    print(instructions)

    for idx, instruction in enumerate(instructions):
        instructions[idx] = re.sub(r"(e)|(w)|(se)|(sw)|(ne)|(nw)", r"\g<1>\g<2>\g<3>\g<4>\g<5>\g<6>,", instruction)[:-1]


def processSteps(direction):
    global x, y

    # https://www.redblobgames.com/grids/hexagons/#coordinates
    if direction == "e":
        x += 1
    elif direction == "w":
        x -= 1
    elif direction == "se":
        if y % 2 != 0:
            x += 1
        y -= 1
    elif direction == "sw":
        if y % 2 == 0:
            x -= 1
        y -= 1
    elif direction == "ne":
        if y % 2 != 0:
            x += 1
        y += 1
    elif direction == "nw":
        if y % 2 == 0:
            x -= 1
        y += 1


def getNeighbours(tile):

    # e, se, sw, w, nw, and ne.

    # decode
    x = int(tile.split(":")[0])
    y = int(tile.split(":")[1])

    e = str(x+1) + ":" + str(y)
    w = str(x-1) + ":" + str(y)

    if y % 2 != 0:
        se = str(x+1) + ":" + str(y-1)
    else:
        se = str(x) + ":" + str(y-1)

    if y % 2 == 0:
        sw = str(x-1) + ":" + str(y-1)
    else:
        sw = str(x) + ":" + str(y-1)

    if y % 2 != 0:
        ne = str(x+1) + ":" + str(y+1)
    else:
        ne = str(x) + ":" + str(y+1)

    if y % 2 == 0:
        nw = str(x-1) + ":" + str(y+1)
    else:
        nw = str(x) + ":" + str(y+1)

    neighbours = [e, se, sw, w, nw, ne]

    assert(len(set(neighbours)) == 6)

    return neighbours


def findAdjacent(tile):
    global blackTiles

    adjacentBlackTiles = 0

    neighbours = getNeighbours(tile)

    for neighbour in neighbours:
        if neighbour in blackTiles:
            adjacentBlackTiles += 1

    return adjacentBlackTiles


def part1():
    global instructions, x, y, blackTiles

    blackTiles = {}

    for directions in instructions:

        x = 0
        y = 0

        for direction in directions.split(","):
            processSteps(direction)

        coordinate = str(x) + ":" + str(y)

        if coordinate in blackTiles:
            del blackTiles[coordinate]
        else:
            blackTiles[coordinate] = 1

    print(len(blackTiles))


def part2():
    global blackTiles

    print(blackTiles)

    for day in range(100):

        toRemove = []
        toAdd = []

        for blackTile in blackTiles:
            adjacentBlackTiles = findAdjacent(blackTile)
            if adjacentBlackTiles == 0 or adjacentBlackTiles > 2:
                toRemove.append(blackTile)

        whiteTiles = []

        for blackTile in blackTiles:
            whiteTiles.extend([x for x in getNeighbours(blackTile) if x not in blackTiles])

        whiteTiles = list(set(whiteTiles))

        for whiteTile in whiteTiles:
            adjacentBlackTiles = findAdjacent(whiteTile)
            if adjacentBlackTiles == 2:
                toAdd.append(whiteTile)

        toAdd = list(set(toAdd))

        for tile in toAdd:
            blackTiles[tile] = 1
        for tile in toRemove:
            del blackTiles[tile]

        print("Day ", day+1, ": ", len(blackTiles), sep="")


initialise()
part1()
part2()
