import utils
import math
import sys


def initialise():
    global earliestTimeOfArrival, timetable, filteredTimetable

    timetable = utils.loadInputFile("input_13.txt")

    earliestTimeOfArrival = int(timetable[0])

    timetable = timetable[1].split(",")
    filteredTimetable = [int(x) for x in timetable if x != 'x']


def lcm(x, y):
    # https://stackoverflow.com/questions/51716916/built-in-module-to-calculate-the-least-common-multiple
    return abs(a*b) // math.gcd(x, y)


def part1():
    global earliestTimeOfArrival, timetable

    firstBusID = None
    shortestWaitingTime = sys.maxsize

    for x in filteredTimetable:
        if (earliestTimeOfArrival % x > 0):
            waitingTime = x*math.ceil(earliestTimeOfArrival/x) - earliestTimeOfArrival
            if waitingTime < shortestWaitingTime:
                firstBusID = x
                shortestWaitingTime = waitingTime

    return (firstBusID * shortestWaitingTime)


def part2():
    # all of the bus ids are primes
    # find offsets from t=0, factoring in the modulus
    offsets = {x: (-timetable.index(str(x)) % x) for x in filteredTimetable}

    # had to get help at this point :(
    # Chinese remainder theorem?
    timestamp = 0
    increment = 1
    for bus in filteredTimetable:
        # check to see if the bus is departing at current time
        while timestamp % bus != offsets[bus]:
            timestamp += increment
        # increase the increment to find next minimum time for next bus
        increment *= bus

    return timestamp


initialise()
print("Part 1:", part1())  # 2165
print("Part 2:", part2())  # 534035653563227
