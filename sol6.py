import utils


def initialise():
    global customsDeclarations
    customsDeclarations = utils.loadInputFile("input_6.txt")


def calculate(setOperation):
    global customsDeclarations

    sumCommon = 0
    declarations = []

    for customsDeclaration in customsDeclarations:
        if customsDeclaration == "":
            # reset and calculate
            # use of python list expansion
            sumCommon += len(setOperation(*declarations))
            declarations = []
        else:
            declarations.append(set(customsDeclaration))

    sumCommon += len(setOperation(*declarations))

    return sumCommon


def part1():
    return calculate(set.union)


def part2():
    return calculate(set.intersection)


initialise()
print("Questions anyone answered yes:", part1())  # 6590
print("Questions everyone answered yes:", part2())  # 3288
