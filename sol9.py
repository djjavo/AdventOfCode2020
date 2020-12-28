import utils
from itertools import combinations

# XMAS starts by transmitting a preamble of 25 numbers. After that, each number
# you receive should be the sum of any two of the 25 immediately previous
# numbers. The two numbers will have different values, and there might be more
# than one such pair.


def initialise():
    global numbers, preamble
    numbers = utils.loadInputFile("input_9.txt")
    numbers = [int(number) for number in numbers]
    preamble = 25


def part1():
    global numbers

    for idx, number in enumerate(numbers):
        if idx < 25:
            continue
        else:
            window = numbers[idx-preamble:idx]
            possibilities = [sum(x) for x in combinations(window, 2)]
            if number not in possibilities:
                return number


def part2(invalid):

    startIndex = 0

    for startIndex in range(0, len(numbers)):
        for endIndex in range(len(numbers), startIndex, -1):
            if sum(numbers[startIndex:endIndex]) == invalid:
                return min(numbers[startIndex:endIndex])+max(numbers[startIndex:endIndex])

    return -1


initialise()
invalid = part1()
print("Invalid number:", invalid)  # 2089807806
print("Encryption weakness:", part2(invalid))  # 245848639
