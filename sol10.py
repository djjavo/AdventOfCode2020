import utils
from collections import Counter


def initialise():
    global adapters, device

    adapters = utils.loadInputFile("input_10.txt")
    adapters = [int(adapters) for adapters in adapters]

    # a adapter can take 1,2,3 jolts lower input
    # device jolts = 3 jolts higher than the highest rated adapter
    # plane charging outlet is 0 jolts
    device = max(adapters) + 3
    adapters.sort()


def contructPossiblePathways(adapters):
    global adapterPathways

    # insert the planes charging outlet at start of list
    adapters.insert(0, 0)

    #  initialise dictionary of pathways
    adapterPathways = {}
    for adapter in adapters:
        adapterPathways[adapter] = []

    # iterate through sorted adapters
    for idx, adapter in enumerate(adapters):
        # iterate though indices from the next until the end of the adapter list
        # for subsequentAdapter in range(idx + 1, len(adapters)):
        for subsequentAdapter in adapters[idx+1:]:
            # if subsequentAdapter exceeds a difference of 3 jolts, proceed to next
            if abs(adapter - subsequentAdapter) > 3:
                break
            # add the current adapter
            adapterPathways[subsequentAdapter].append(adapter)


def part1():
    global adapters, device

    previousAdapter = 0
    joltDifferences = []

    for adapter in adapters:
        joltDifferences.append(abs(previousAdapter - adapter))
        previousAdapter = adapter

    joltDifferences.append(abs(previousAdapter - device))

    distribution = Counter(joltDifferences)

    return distribution[1] * distribution[3]


def part2(adapters):
    global adapterPathways

    adapterCombinations = {}
    # initialise the plane charging outlet with 1 combination
    adapterCombinations[0] = 1

    for adapter in adapters[1:]:
        combinations = 0
        # for each parent adapter, increment by the parents number of combinations
        for parentAdapter in adapterPathways[adapter]:
            combinations += adapterCombinations[parentAdapter]
        # save the number of combinations in dictionary
        adapterCombinations[adapter] = combinations

    # return the number of combinations for the final adapter
    return adapterCombinations[adapters[-1]]


initialise()
contructPossiblePathways(adapters)
print("Part 1:", part1())  # 2046
print("Part 2:", part2(adapters))  # 1157018619904
