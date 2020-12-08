import utils
import re


def initialise():
    global instructions
    instructions = utils.loadInputFile("input_8.txt")


def runBootCode(instructions):
    accumulator = 0
    programCounter = 0
    error = False

    instructionsVisited = []

    while programCounter in range(0, len(instructions)):
        opcode, operand = instructions[programCounter].split(" ")

        if programCounter in instructionsVisited:
            error = True
            break
        else:
            instructionsVisited.append(programCounter)

        if opcode == "acc":
            accumulator += int(operand)
            programCounter += 1
        elif opcode == "jmp":
            programCounter += int(operand)
        elif opcode == "nop":
            programCounter += 1

    return accumulator, error


def substituteInstructionThenRun(substitution):
    global instructions

    localInstructions = instructions[:]

    if len(substitution) > 0:
        if substitution['type'] == "jmp":
            print(localInstructions[substitution['index']])
            localInstructions[substitution['index']] = localInstructions[substitution['index']].replace("jmp", "nop")
            print(localInstructions[substitution['index']])
        elif substitution['type'] == "nop":
            print(localInstructions[substitution['index']])
            localInstructions[substitution['index']] = localInstructions[substitution['index']].replace("nop", "jmp")
            print(localInstructions[substitution['index']])

    return runBootCode(localInstructions)


def part1():
    global instructions

    return runBootCode(instructions)


def part2():

    # Somewhere in the program, either a jmp is supposed to be a nop, or a nop
    # is supposed to be a jmp. (No acc instructions were harmed in the
    # corruption of this boot code.)

    # The program is supposed to terminate by attempting to execute an
    # instruction immediately after the last instruction in the file
    # i.e. when programCounter == len(instructions)

    global instructions

    jmp = [i for i, x in enumerate(instructions) if x.split(" ")[0] == "jmp"]
    nop = [i for i, x in enumerate(instructions) if x.split(" ")[0] == "nop"]

    for x in jmp:
        accumulator, error = substituteInstructionThenRun({"type": "jmp", "index": x})
        if not error:
            return accumulator, error

    for x in nop:
        accumulator, error = substituteInstructionThenRun({"type": "nop", "index": x})
        if not error:
            return accumulator, error


initialise()
print("Bags that can hold a shiny gold bag:", part1())  # 197
print("Questions everyone answered yes:", part2())  # 85324
