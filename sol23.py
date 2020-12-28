import utils
from llist import dllist, dllistnode


def initialise():
    global cups, currentCupIdx, totalCups, move

    cups = utils.loadInputFile("input_23.txt")

    cups = [int(cup) for cup in cups[0]]

    currentCupIdx = 0
    totalCups = len(cups)

    move = 1


def printCups():
    global cups, currentCup, currentCupIdx

    print("cups:", end=" ")

    for cup in cups:
        if cup is currentCup:
            print("(", cup, ")", sep="", end=" ")
        else:
            print(cup, end=" ")

    print()


def safeWrap(n):
    global totalCups

    if n >= totalCups:
        return n - totalCups
    if n < 0:
        return n + totalCups
    else:
        return n


def processMove():
    global cups, currentCup, currentCupIdx, move

    currentCup = cups[currentCupIdx]

    # picks up (removes) cups n+1,n+2,n+3
    pickedUp = [cups[safeWrap(currentCupIdx+1)], cups[safeWrap(currentCupIdx+2)], cups[safeWrap(currentCupIdx+3)]]

    # print("-- move", move, "--")
    # printCups()
    # print("picked up:", pickedUp)

    [cups.remove(cup) for cup in pickedUp]

    # destination cup is current cup label -1
    destinationCup = currentCup - 1
    # if goes below 1, wrap around to highest
    if destinationCup < 0:
        # print("now setting to ", totalCups)
        destinationCup = totalCups

    while True:
        # if this has been picked up, keep subtracting 1
        if destinationCup in cups:
            break
        # print(destinationCup, "not present, minusing...")
        destinationCup -= 1
        # if goes below 1, wrap around to highest
        if destinationCup < 0:
            # print("now setting to ", totalCups)
            destinationCup = totalCups

    # print("destination", destinationCup)
    # print()

    # place cups immediately clockwise of destination cup in same order
    destinationIndex = cups.index(destinationCup)

    cups = cups[0:destinationIndex+1] + pickedUp + cups[destinationIndex+1:]

    # new current cup = current cup + 1 (wraps)
    currentCupIdx = cups.index(currentCup)
    currentCupIdx = safeWrap(currentCupIdx+1)

    move += 1


def getNextNode(idx):
    global linkedList
    if linkedList.nodeat(idx+1) is None:
        return linkedList.first()
    return linkedList.nodeat(idx+1)


def getNext(node):
    global linkedList
    if node.next is None:
        return linkedList.nodeat(0)
    else:
        return node.next


def findAvailableDestination(destination, currentCup):
    while True:
        destination -= 1
        if destination < 1:
            destination = max(cupMap.keys())
        if destination in cupMap and destination != currentCup.value:
            return destination


def part1():
    global cups

    for i in range(100):
        processMove()

    startIdx = cups.index(1)
    labels = cups[startIdx+1:] + cups[:startIdx]

    return "".join(str(cup) for cup in labels)


def part2():
    # had to get a fair bit of help on this one
    global cups, linkedList, cupsToPick, cupMap

    # add the additional numbers preserving order
    cups = cups + [cup for cup in range(max(cups)+1, 1000001)]

    # create as linked list
    linkedList = dllist(cups)

    cupMap = {}

    # create a hashmap, value -> node in linkedList
    for idx in range(linkedList.size):
        cupMap[linkedList.nodeat(idx).value] = linkedList.nodeat(idx)

    currentCup = linkedList.nodeat(0)

    rounds = 10000000
    for i in range(rounds):

        nextCup = currentCup
        for j in range(4):
            nextCup = getNext(nextCup)

        cupsToPick = []

        thisCup = currentCup
        for j in range(3):
            thisCup = getNext(thisCup)
            cupsToPick.append((thisCup, thisCup.value))

        for j in range(3):
            del cupMap[cupsToPick[j][1]]
            linkedList.remove(cupsToPick[j][0])

        destination = currentCup.value - 1
        if destination in cupsToPick or destination not in cupMap:
            destination = findAvailableDestination(destination, currentCup)

        destinationNode = cupMap[destination]
        nextDestinationNode = destinationNode.next

        if nextDestinationNode is None:
            destinationNode = None
            nextDestinationNode = linkedList.nodeat(0)

        linkedList.insert(cupsToPick[0][1], nextDestinationNode)
        linkedList.insert(cupsToPick[1][1], nextDestinationNode)
        linkedList.insert(cupsToPick[2][1], nextDestinationNode)

        if destinationNode is not None:
            cupMap[cupsToPick[0][1]] = destinationNode.next
            cupMap[cupsToPick[1][1]] = destinationNode.next.next
            cupMap[cupsToPick[2][1]] = destinationNode.next.next.next
        else:
            cupMap[cupsToPick[0][1]] = linkedList.nodeat(0)
            cupMap[cupsToPick[1][1]] = linkedList.nodeat(0).next
            cupMap[cupsToPick[2][1]] = linkedList.nodeat(0).next.next

        currentCup = nextCup

    # find position of cup 1
    cupOne = cupMap[1]

    firstAnswerCup = cupOne.next
    if firstAnswerCup is None:
        firstAnswerCup = linkedList.nodeat(0)
    secondAnswerCup = firstAnswerCup.next
    if secondAnswerCup is None:
        secondAnswerCup = linkedList.nodeat(0)

    return firstAnswerCup.value * secondAnswerCup.value


initialise()
print("Part 1:", part1())  # 76385429
initialise()
print("Part 2:", part2())  # 12621748849
