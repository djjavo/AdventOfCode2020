import utils
import re


def initialise():
    global ticketInput, rules, otherTickets, validNumbers, ruleDict, ticket

    ticketInput = utils.loadInputFile("input_16.txt")

    rules = []
    otherTickets = []

    for line in ticketInput:
        if line == "":
            break
        rules.append(line)

    for idx, line in enumerate(ticketInput):
        if line == "your ticket:":
            ticket = ticketInput[idx+1]
            break

    ticket = [int(x) for x in ticket.split(",")]

    for i in range(idx+4, len(ticketInput)):
        otherTickets.append(ticketInput[i].split(","))

    validNumbers = []

    exp = re.compile(r"^(.*): (\d+)-(\d+) or (\d+)-(\d+).*$")
    ruleDict = {}

    for rule in rules:
        m = re.match(exp, rule)

        validNumbers.extend(range(int(m.group(2)), int(m.group(3))+1))
        validNumbers.extend(range(int(m.group(4)), int(m.group(5))+1))

        ruleDict[m.group(1)] = []

        ruleDict[m.group(1)].extend(range(int(m.group(2)), int(m.group(3))+1))
        ruleDict[m.group(1)].extend(range(int(m.group(4)), int(m.group(5))+1))


def extractColumn(list, idx):
    return [int(row[idx]) for row in list]


def part1():
    global otherTickets, validNumbers, validTickets

    errorNumbers = []
    validTickets = []

    for otherTicket in otherTickets:
        valid = True
        tempValidNumbers = validNumbers[:]
        for number in otherTicket:
            number = int(number)
            if number not in tempValidNumbers:
                errorNumbers.append(number)
                valid = False
            else:
                tempValidNumbers.remove(number)

        if valid:
            validTickets.append(otherTicket)

    return sum(errorNumbers)


def part2():
    global rules, validTickets, ruleDict, ticket

    positions = []

    cols = len(validTickets[0])
    col = []

    possibilities = {}

    for i in range(0, cols):
        possibilities[i] = []

    for i in range(0, cols):
        for rule in ruleDict:
            valid = True
            for j in extractColumn(validTickets, i):
                if j not in ruleDict[rule]:
                    valid = False
                    break
            if valid:
                possibilities[i].append(rule)

    complete = False

    while not complete:
        complete = True
        for possibility in possibilities:
            if len(possibilities[possibility]) == 1:
                item = possibilities[possibility][0]
                possibilities[possibility] = []

                if item.startswith('departure'):
                    positions.append(possibility)

                # remove and break
                for possibilityInner in possibilities:
                    try:
                        possibilities[possibilityInner].remove(item)
                    except ValueError:
                        pass

            if len(possibilities[possibility]) != 0:
                complete = False

    result = 1

    for position in positions:
        result *= int(ticket[position])

    return result


initialise()
print("Part 1:", part1())  # 22977
print("Part 2:", part2())  # 998358379943
