import utils


def initialise():
    global passwords, criteria, letter, mini, maxi

    data = utils.loadInputFile("input_2.txt")

    passwords = [i.split(':', 1)[1].strip() for i in data]

    criteria = [i.split(':', 1)[0] for i in data]
    letter = [i.split(' ', 1)[1] for i in criteria]
    mini = [int(i.split(' ', 1)[0].split('-')[0]) for i in criteria]
    maxi = [int(i.split(' ', 1)[0].split('-')[1]) for i in criteria]


def part1():
    global passwords, criteria, letter, mini, maxi

    # Initialise counter
    validPasswords = 0
    for idx, x in enumerate(passwords):
        if not (x.count(letter[idx]) < mini[idx] or x.count(letter[idx])
                > maxi[idx]):
            validPasswords += 1
    return validPasswords


def part2():
    global passwords, criteria, letter, mini, maxi

    # Initialise counter
    validPasswords = 0
    for idx, x in enumerate(passwords):
        if (bool(x[mini[idx]-1] == letter[idx]) ^
                bool(x[maxi[idx]-1] == letter[idx])):
            validPasswords += 1
    return validPasswords


initialise()
print("Valid passwords:", part1())  # 474
print("Valid passwords:", part2())  # 745
