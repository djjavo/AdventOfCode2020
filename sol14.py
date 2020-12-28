import utils
import re
import itertools


def initialise():
    global instructions, exp

    instructions = utils.loadInputFile("input_14.txt")
    exp = re.compile("^mem\\[(\\d+)\\]\\s=\\s(\\d+)$")


def part1():
    global instructions, exp

    memory = {}

    for instruction in instructions:
        if instruction.startswith("mask"):
            mask = instruction[7:]

            xes = [idx for idx, char in enumerate(mask) if char == 'X']
            ones = [idx for idx, char in enumerate(mask) if char == '1']

            maskX = sum(1 << (35-x) for x in xes)
            maskOne = sum(1 << (35-one) for one in ones)

        else:
            m = re.match(exp, instruction)
            location = m.group(1)
            value = int(m.group(2))

            maskedValue = (value & maskX) | maskOne
            memory[location] = maskedValue

    return sum(memory.values())


def part2():
    # this time we are altering the addresses not the values
    global instructions

    memory = {}

    for instruction in instructions:
        if instruction.startswith("mask"):
            toAdd = []
            mask = instruction[7:]

            flippedMask = mask.replace("0", "1").replace("X", "0")
            flippedXes = [idx for idx, char in enumerate(flippedMask) if char == '1']

            xes = [idx for idx, char in enumerate(mask) if char == 'X']
            ones = [idx for idx, char in enumerate(mask) if char == '1']

            maskX = sum(1 << (35-x) for x in flippedXes)
            maskOne = sum(1 << (35-one) for one in ones)

            combinationSets = itertools.chain([itertools.combinations(xes, x) for x in range(len(xes)+1)])

            for combinationSet in combinationSets:
                for combination in combinationSet:
                    x = 0
                    for y in combination:
                        x = x | (1 << 35-y)
                    toAdd.append(x)

        else:
            m = re.match(exp, instruction)
            location = int(m.group(1))
            value = int(m.group(2))

            # this will override all 1's in mask, leave everything else
            # maskedKey = location | maskOne
            maskedLocation = (location | maskOne) & maskX

            for y in toAdd:
                memory[maskedLocation + y] = value

    return sum(memory.values())


initialise()
print(part1())  # 8566770985168
print(part2())  # 4832039794082
