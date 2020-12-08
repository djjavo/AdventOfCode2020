import utils
import re


def initialise():
    global luggageRules, totalBags
    luggageRules = utils.loadInputFile("input_7.txt")
    totalBags = []


def createLookupTable():
    global luggageRules, bagLookup

    exp = re.compile("^(.*)\\s{1}bags contain\\s{1}(.*)\\.$")

    bagLookup = {}

    for luggageRule in luggageRules:
        m = re.match(exp, luggageRule)
        if m:

            thisbagLookup = {}

            if m.group(2) == "no other bags":
                bagLookup[m.group(1)] = thisbagLookup
                continue

            for xyz in m.group(2).split(", "):
                # print(xyz)
                res = re.match("^([0-9]+)\\s(.*)\\s(bag|bags)$", xyz)

                bagCount = res.group(1)
                bagType = res.group(2)

                thisbagLookup[bagType] = int(bagCount)

            bagLookup[m.group(1)] = thisbagLookup


def findBagsContaining(bags):
    global luggageRules, matchedBags

    exp = re.compile("^(.*)\\s{1}bags contain.*("+bags+").*$")

    parentBags = []

    for luggageRule in luggageRules:
        m = re.match(exp, luggageRule)
        if m:
            parentBags.append(m.group(1))
            matchedBags.add(m.group(1))

    if parentBags:  # not empty:
        findBagsContaining('|'.join(parentBags))

    return parentBags


def findBagsWithin(bag, thisBagCount):
    global bagLookup

    if len(bagLookup[bag]) == 0:
        return thisBagCount
    else:
        totalBags = 0
        for thisBag, countOfBags in bagLookup[bag].items():
            totalBags += findBagsWithin(thisBag, countOfBags)
        totalBags *= thisBagCount
        totalBags += thisBagCount
        return totalBags


def part1():
    global matchedBags
    matchedBags = set()

    bags = findBagsContaining("shiny gold")

    return len(matchedBags)


def part2():
    global bagLookup

    totalBags = 0
    for thisBag, countOfBags in bagLookup["shiny gold"].items():
        totalBags += findBagsWithin(thisBag, countOfBags)

    return totalBags


initialise()
createLookupTable()
print("Bags that can hold a shiny gold bag:", part1())  # 197
print("Questions everyone answered yes:", part2())  # 85324
