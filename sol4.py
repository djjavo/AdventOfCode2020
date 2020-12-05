import utils
import re


def initialise():
    # Passport Fields
    # byr (Birth Year)       four digits; at least 1920 and at most 2002.
    # iyr (Issue Year)       four digits; at least 2010 and at most 2020.
    # eyr (Expiration Year)  four digits; at least 2020 and at most 2030.
    # hgt (Height)           a number followed by either cm or in:
    #       If cm, the number must be at least 150 and at most 193.
    #       If in, the number must be at least 59 and at most 76.
    # hcl (Hair Color)       a # followed by exactly six characters 0-9 or a-f.
    # ecl (Eye Color)        exactly one of: amb blu brn gry grn hzl oth.
    # pid (Passport ID)      a nine-digit number, including leading zeroes.
    # cid (Country ID)       ignored, missing or not.
    global batchInput
    batchInput = utils.loadInputFile("input_4.txt")


def validatePassport(passport, check):
    # check all required fields are present
    if not all(fields in passport for fields in ("byr", "iyr", "eyr", "hgt",
                                                 "hcl", "ecl", "pid")):
        return False

    if check == "strict":
        if (len(passport["byr"]) != 4 or int(passport["byr"]) < 1920
                or int(passport["byr"]) > 2002):
            return False
        if (len(passport["iyr"]) != 4 or int(passport["iyr"]) < 2010
                or int(passport["iyr"]) > 2020):
            return False
        if (len(passport["eyr"]) != 4 or int(passport["eyr"]) < 2020
                or int(passport["eyr"]) > 2030):
            return False

        heightIn = re.match("^([0-9]{3})cm$", passport["hgt"])  # 150-193
        heightCm = re.match("^([0-9]{2})in$", passport["hgt"])  # 59-76
        if heightIn is None and heightCm is None:
            return False
        elif heightIn is not None:
            if int(heightIn.group(1)) < 150 or int(heightIn.group(1)) > 193:
                return False
        elif heightCm is not None:
            if int(heightCm.group(1)) < 59 or int(heightCm.group(1)) > 76:
                return False

        if not re.search("^#[a-f0-9]{6}$", passport["hcl"]):
            return False
        if passport["ecl"] not in ["amb", "blu", "brn", "gry",
                                   "grn", "hzl", "oth"]:
            return False
        if not re.search("^[0-9]{9}$", passport["pid"]):
            return False

    return True


def processBatch(check):
    global batchInput

    passport = dict()
    valid = 0

    for line in batchInput:

        # a blank line is the data separator
        # when seeing this, validate and start new passport
        if line == "":
            if validatePassport(passport, check):
                valid += 1
            passport = dict()
        else:
            fields = line.split(" ")
            for field in fields:
                key = field.split(":")[0]
                value = field.split(":")[1]
                passport[key] = value

    # validate final passport in the file
    if validatePassport(passport, check):
        valid += 1
    return valid


def part1():
    return processBatch("lazy")


def part2():
    return processBatch("strict")


initialise()
print("Valid passports [lazy]:", part1())  # 260
print("Valid passports [strict]:", part2())  # 153
