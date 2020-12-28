import utils
import re
import math
import copy


def initialise():
    global expressions, numbers

    expressions = utils.loadInputFile("input_18.txt")
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


def process():
    global operandStack, operationStack

    op = operationStack.pop()

    if op == "(":
        return

    x = operandStack.pop()
    y = operandStack.pop()

    if op == "+":
        z = int(x) + int(y)
    elif op == "*":
        z = int(x) * int(y)

    operandStack.append(str(z))


def part1():
    global expressions, numbers, operandStack, operationStack

    totalSum = 0

    for expression in expressions:
        # strip whitespace
        expression = expression.replace(" ", "")

        operandStack = []
        operationStack = []

        for char in expression:

            if char in numbers:
                operandStack.append(char)

            elif (char == "+" or char == "*") and len(operationStack) == 0:
                operationStack.append(char)

            elif (char == "+" or char == "*") and len(operationStack) != 0:
                process()
                operationStack.append(char)

            elif char == "(":
                operationStack.append(char)

            elif char == ")":
                process()

            else:
                process()

        while len(operationStack) > 0:
            process()

        totalSum += int(operandStack[0])

    return totalSum


def part2():
    global expressions, numbers, operandStack, operationStack

    totalSum = 0

    for expression in expressions:
        # strip whitespace
        expression = expression.replace(" ", "")

        operandStack = []
        operationStack = []

        idx = 0

        while idx < len(expression):

            char = expression[idx]

            if char in numbers:
                operandStack.append(char)

            elif (char == "+" or char == "*") and len(operationStack) == 0:
                operationStack.append(char)

            elif char == "+" and len(operationStack) != 0:
                operationStack.append(char)

            elif char == "*":
                # if we have +'s on top of the stack, these should be processed first
                # as they take precedence
                if operationStack[-1] == "+":
                    process()
                    while len(operationStack) > 0 and operationStack[-1] == "+":
                        process()
                    operationStack.append(char)
                elif operationStack[-1] == "(":
                    operationStack.append(char)
                else:
                    operationStack.append(char)

            elif char == "(":
                operationStack.append(char)

            elif char == ")":
                while operationStack[-1] != "(":
                    process()
                operationStack.pop()

            else:
                process()

            idx += 1

        while len(operationStack) > 0:
            process()

        totalSum += int(operandStack[0])

    return totalSum


initialise()
print(part1())  # 209335026987
print(part2())  # 33331817392479
