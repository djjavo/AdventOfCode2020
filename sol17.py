import utils
import re
import math
import copy


def initialise():
    global cubes

    cubes = utils.loadInputFile("input_17.txt")

    cubes = [[list(x) for x in cubes]]


def expandAndCentre(dimensions):
    global cubes

    newCubes = list()

    if dimensions == 3:
        d_x, d_y, d_z = len(cubes[0][0]), len(cubes[0]), len(cubes)
        for z in range(0, d_z+2):
            y_list = []
            for y in range(0, d_y+2):
                x_list = []
                for x in range(0, d_x+2):
                    if x > 0 and x < d_x+1 and y > 0 and y < d_y+1 and z > 0 and z < d_z+1:
                        x_list.append(cubes[z-1][y-1][x-1])
                    else:
                        x_list.append(".")
                y_list.append(x_list)
            newCubes.append(y_list)

    elif dimensions == 4:
        d_w, d_x, d_y, d_z = len(cubes[0][0][0]), len(cubes[0][0]), len(cubes[0]), len(cubes)
        for z in range(0, d_z+2):
            y_list = []
            for y in range(0, d_y+2):
                x_list = []
                for x in range(0, d_x+2):
                    w_list = []
                    for w in range(0, d_w+2):
                        if w > 0 and w < d_w+1 and x > 0 and x < d_x+1 and y > 0 and y < d_y+1 and z > 0 and z < d_z+1:
                            w_list.append(cubes[z-1][y-1][x-1][w-1])
                        else:
                            w_list.append(".")
                    x_list.append(w_list)
                y_list.append(x_list)
            newCubes.append(y_list)

    else:
        raise Exception

    cubes = copy.deepcopy(newCubes)


def inBounds(x, y, z):
    if x < 0 or y < 0 or z < 0:
        return False
    if x >= len(cubes[0][0]) or y >= len(cubes[0]) or z >= len(cubes):
        return False
    return True


def inBounds4D(w, x, y, z):
    if w < 0 or x < 0 or y < 0 or z < 0:
        return False
    if w >= len(cubes[0][0][0]) or x >= len(cubes[0][0]) or y >= len(cubes[0]) or z >= len(cubes):
        return False
    return True


def active(x, y, z):
    global cubes

    return cubes[z][y][x] == "#"


def active4D(w, x, y, z):
    global cubes

    return cubes[z][y][x][w] == "#"


def activeNeighbours(x, y, z):
    activeNeighbours = 0

    for n_x in [x-1, x, x+1]:
        for n_y in [y-1, y, y+1]:
            for n_z in [z-1, z, z+1]:
                if not (n_x == x and y == n_y and z == n_z):
                    if inBounds(n_x, n_y, n_z):
                        if active(n_x, n_y, n_z):
                            activeNeighbours += 1

    return activeNeighbours


def activeNeighbours4D(w, x, y, z):
    activeNeighbours = 0

    for n_w in [w-1, w, w+1]:
        for n_x in [x-1, x, x+1]:
            for n_y in [y-1, y, y+1]:
                for n_z in [z-1, z, z+1]:
                    if not (n_w == w and n_x == x and y == n_y and z == n_z):
                        if inBounds4D(n_w, n_x, n_y, n_z):
                            if active4D(n_w, n_x, n_y, n_z):
                                activeNeighbours += 1

    return activeNeighbours


def flipState(state):
    if state == "#":
        return "."
    else:
        return "#"


def countActive(dimensions):
    global cubes

    if dimensions == 3:
        numActive = 0
        for idx_z, z in enumerate(cubes):
            for idx_y, y in enumerate(z):
                for idx_x, _ in enumerate(y):
                    if active(idx_x, idx_y, idx_z):
                        numActive += 1
        return numActive

    elif dimensions == 4:
        numActive = 0
        for idx_z, z in enumerate(cubes):
            for idx_y, y in enumerate(z):
                for idx_x, x in enumerate(y):
                    for idx_w, _ in enumerate(x):
                        if active4D(idx_w, idx_x, idx_y, idx_z):
                            numActive += 1
        return numActive

    else:
        raise Exception


def processTick(dimensions):
    global cubes

    updatedCube = copy.deepcopy(cubes)

    # 3 -> -1 .. 1
    # 5 -> -2 .. 2
    # 7 -> -3 .. 3

    if dimensions == 3:
        for idx_z, z in enumerate(cubes):
            for idx_y, y in enumerate(z):
                for idx_x, x in enumerate(y):

                    # If a cube is inactive but exactly 3 of its neighbours are active, the
                    # cube becomes active. Otherwise, the cube remains inactive.
                    if active(idx_x, idx_y, idx_z) and not (activeNeighbours(idx_x, idx_y, idx_z) == 2 or
                                                            activeNeighbours(idx_x, idx_y, idx_z) == 3):
                        updatedCube[idx_z][idx_y][idx_x] = flipState(cubes[idx_z][idx_y][idx_x])

                    # If a cube is active and exactly 2 or 3 of its neighbours are also active,
                    # the cube remains active. Otherwise, the cube becomes inactive.
                    elif not active(idx_x, idx_y, idx_z) and activeNeighbours(idx_x, idx_y, idx_z) == 3:
                        updatedCube[idx_z][idx_y][idx_x] = flipState(cubes[idx_z][idx_y][idx_x])

    elif dimensions == 4:
        for idx_z, z in enumerate(cubes):
            for idx_y, y in enumerate(z):
                for idx_x, x in enumerate(y):
                    for idx_w, w in enumerate(x):
                        # If a cube is inactive but exactly 3 of its neighbours are active, the
                        # cube becomes active. Otherwise, the cube remains inactive.
                        if active4D(idx_w, idx_x, idx_y, idx_z) and not (activeNeighbours4D(idx_w, idx_x, idx_y, idx_z) == 2 or
                                                    activeNeighbours4D(idx_w, idx_x, idx_y, idx_z) == 3):
                            updatedCube[idx_z][idx_y][idx_x][idx_w] = flipState(cubes[idx_z][idx_y][idx_x][idx_w])

                        # If a cube is active and exactly 2 or 3 of its neighbours are also active,
                        # the cube remains active. Otherwise, the cube becomes inactive.
                        elif not active4D(idx_w, idx_x, idx_y, idx_z) and activeNeighbours4D(idx_w, idx_x, idx_y, idx_z) == 3:
                            updatedCube[idx_z][idx_y][idx_x][idx_w] = flipState(cubes[idx_z][idx_y][idx_x][idx_w])

    else:
        raise Exception

    cubes = copy.deepcopy(updatedCube)


def printCube():

    for idx_z, z in enumerate(cubes):
        print("z=", idx_z, sep="")
        for idx_y, y in enumerate(z):
            for idx_x, x in enumerate(y):
                print(x, end="")
            print()
        print()
        print()


def part1():
    for tick in range(0, 6):
        expandAndCentre(3)
        processTick(3)

    return countActive(3)


def part2():
    for tick in range(0, 6):
        expandAndCentre(4)
        processTick(4)

    return countActive(4)


initialise()
print("Part 1:", part1())  # 265
initialise()
print("Part 2:", part2())  # 1936
