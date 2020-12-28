import utils


def initialise():
    global instructions

    instructions = utils.loadInputFile("input_12.txt")
    reset()


def reset():
    global heading, north, east, waypointNorth, waypointEast
    heading = 90  # The ship starts by facing east (90)

    north = 0
    east = 0
    waypointNorth = 1
    waypointEast = 10


def rotate(amount):
    global heading

    heading += amount

    if heading >= 360:
        heading -= 360
    elif heading < 0:
        heading += 360


def move(heading, amount):
    global north, east

    if heading == 0:
        north += amount
    elif heading == 90:
        east += amount
    elif heading == 180:
        north -= amount
    elif heading == 270:
        east -= amount


def moveForward(amount):
    global heading
    move(heading, amount)


def distanceFromStart():
    global north, east

    return abs(north) + abs(east)


def moveWaypoint(heading, amount):
    global waypointNorth, waypointEast

    if heading == 0:
        waypointNorth += amount
    elif heading == 90:
        waypointEast += amount
    elif heading == 180:
        waypointNorth -= amount
    elif heading == 270:
        waypointEast -= amount


def rotateWaypoint(direction, amount):
    global waypointNorth, waypointEast

    if direction == "L":
        if amount == 90:
            waypointNorth, waypointEast = waypointEast, -waypointNorth
        elif amount == 270:
            waypointNorth, waypointEast = -waypointEast, waypointNorth

    if direction == "R":
        if amount == 90:
            waypointNorth, waypointEast = -waypointEast, waypointNorth
        elif amount == 270:
            waypointNorth, waypointEast = waypointEast, -waypointNorth

    if amount == 180:
        waypointNorth = -waypointNorth
        waypointEast = -waypointEast


def moveShipToWaypoint(amount):
    global north, east, waypointNorth, waypointEast

    north += amount * waypointNorth
    east += amount * waypointEast
    # viewpoint stays relative, so coords unchanged


def part1():
    global instructions

    for instruction in instructions:
        action, value = instruction[:1], int(instruction[1:])

        if action == "L":
            rotate(-1 * value)
        elif action == "R":
            rotate(1 * value)
        elif action == "F":
            moveForward(value)
        elif action == "N":
            move(0, value)
        elif action == "E":
            move(90, value)
        elif action == "S":
            move(180, value)
        elif action == "W":
            move(270, value)

    return distanceFromStart()


def part2():
    global instructions

    for instruction in instructions:
        action, value = instruction[:1], int(instruction[1:])

        if action == "L":
            rotateWaypoint("L", value)
        elif action == "R":
            rotateWaypoint("R", value)
        elif action == "F":
            moveShipToWaypoint(value)
        elif action == "N":
            moveWaypoint(0, value)
        elif action == "E":
            moveWaypoint(90, value)
        elif action == "S":
            moveWaypoint(180, value)
        elif action == "W":
            moveWaypoint(270, value)

    return distanceFromStart()


initialise()
print("Part 1:", part1())  # 1294
reset()
print("Part 2:", part2())  # 20592
