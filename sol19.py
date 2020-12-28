import utils
import re
import math
import copy
import itertools

DEBUG = False


def initialise():
    global messages, rules

    data = utils.loadInputFile("input_19.txt")

    for idx, line in enumerate(data):
        if line == "":
            rules = data[:idx]
            messages = data[idx+1:]
            break


def parseRules(replace=False):
    global rules, ruleDict

    ruleDict = {}

    character = re.compile("^(\\d+): \"(\\w)\"$")
    standard = re.compile("^(\\d+):((?:\\s(\\d)+)+)$")
    orCondition = re.compile("^(\\d+):((?:\\s(?:\\d)+)+)\\s\\|((?:\\s(?:\\d)+)+)$")

    if replace:
        for idx, rule in enumerate(rules):
            if rule.startswith("8:") and replace:
                rules[idx] = "8: 42 | 42 8"

            if rule.startswith("11:") and replace:
                rules[idx] = "11: 42 31 | 42 11 31"

    while len(rules) > 0:

        toRemove = []

        for idx, rule in enumerate(rules):

            m = re.match(character, rule)
            m1 = re.match(standard, rule)
            m2 = re.match(orCondition, rule)

            if m:
                ruleDict[m.group(1)] = str(m.group(2))
                toRemove.append(idx)
            elif m1:
                subRules = m1.group(2).split()
                criteriaMet = True
                for subRule in subRules:
                    if subRule not in ruleDict:
                        criteriaMet = False
                        break

                if criteriaMet:
                    charString = ""
                    for subRule in subRules:
                        charString += ruleDict[subRule]
                    ruleDict[m1.group(1)] = charString
                    toRemove.append(idx)
            elif m2:
                subRulesA = m2.group(2).split()
                subRulesB = m2.group(3).split()

                criteriaMet = True

                # Hacky solution instead of writing a CFG parser
                if m2.group(1) == "8" or m2.group(1) == "11":
                    for subRule in subRulesA:
                        if subRule not in ruleDict:
                            criteriaMet = False
                            break

                    if criteriaMet:

                        charStringA = ""
                        if m2.group(1) == "8":
                            for subRule in subRulesA:
                                charStringA += ruleDict[subRule]
                            generatedRegex = "(" + charStringA + ")+"
                        else:
                            # longest message is 96 characters
                            for i in range(16):
                                # generating ab|aabb|aaabbb etc.
                                for subRule in subRulesA:
                                    for j in range(i+1):
                                        charStringA += ruleDict[subRule]
                                charStringA += "|"

                            # strip last or "|" from regex
                            charStringA = charStringA[:-1]
                            generatedRegex = "(" + charStringA + ")"

                        ruleDict[m2.group(1)] = generatedRegex
                        toRemove.append(idx)

                else:

                    for subRule in subRulesA:
                        if subRule not in ruleDict:
                            criteriaMet = False
                            break
                    for subRule in subRulesB:
                        if subRule not in ruleDict:
                            criteriaMet = False
                            break

                    if criteriaMet:

                        charStringA = ""
                        for subRule in subRulesA:
                            charStringA += ruleDict[subRule]

                        charStringB = ""
                        for subRule in subRulesB:
                            charStringB += ruleDict[subRule]

                        generatedRegex = "(" + charStringA + "|" + charStringB + ")"

                        ruleDict[m2.group(1)] = generatedRegex
                        toRemove.append(idx)
            else:
                raise Exception

        for idx in sorted(toRemove, reverse=True):
            del rules[idx]

        if DEBUG:
            print(len(rules), "rules left to process")


def matchMessages():
    global messages, ruleDict

    matchedCount = 0

    if DEBUG:
        print("\n\n")
        print("Final expression:")
        print(ruleDict['0'])

    exp = re.compile("^" + ruleDict['0'] + "$")

    for messages in messages:
        if re.match(exp, messages):
            matchedCount += 1

    return matchedCount


def part1():
    parseRules()
    return matchMessages()


def part2():
    parseRules(True)
    return matchMessages()


initialise()
print("Part 1:", part1())  # 124
initialise()
print("Part 2:", part2())  # 243
