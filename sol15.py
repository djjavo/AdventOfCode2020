import utils


def initialise():
    global numbers, spoken

    numbers = utils.loadInputFile("input_15.txt")
    numbers = numbers[0].split(",")
    numbers = [int(x) for x in numbers]

    spoken = {}

    for idx, number in enumerate(numbers):
        spoken[number] = [idx+1]

    # the last number in the loop is spoken here

    if 0 not in spoken.keys():
        spoken[0] = []
    spoken[0].append(len(numbers)+1)


def processTurn(turn):
    global lastSpoken, spoken

    if lastSpoken in spoken.keys() and len(spoken[lastSpoken]) > 1:
        number = spoken[lastSpoken][-1] - spoken[lastSpoken][-2]
        if number not in spoken.keys():
            spoken[number] = []
        spoken[number].append(turn)
    else:
        number = 0
        spoken[0].append(turn)

    lastSpoken = number


def part1():
    global numbers, spoken, lastSpoken

    lastSpoken = 0

    for turn in range(len(numbers)+2, 2021):
        processTurn(turn)

    return lastSpoken


def part2():
    global numbers, spoken, lastSpoken

    lastSpoken = 0

    for turn in range(len(numbers)+2, 30000001):
        processTurn(turn)

    return lastSpoken


initialise()
print("Part 1:", part1())  # 639
initialise()
print("Part 2:", part2())  # 266
