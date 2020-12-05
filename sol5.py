import utils
import math

def initialise():
	global boardingPasses
	boardingPasses = utils.loadInputFile("input_5.txt")

	# 7 chars: 128 rows on the plane (numbered 0 through 127)
	# 3 chars: 8 columns on the plane (numbered 0 through 7)

def calculateRow(input):

	rowMin = 0
	rowMax = 127

	if len(input) != 7:
		raise Exception

	for letter in input:
		if letter == "F":
			rowMax = rowMax-math.ceil((rowMax-rowMin)/2)
		if letter == "B":
			rowMin = rowMin+math.ceil((rowMax-rowMin)/2)

	return rowMin

def calculateCol(input):

	colMin = 0
	colMax = 7

	if len(input) != 3:
		raise Exception

	for letter in input:
		if letter == "L":
			colMax = colMax-math.ceil((colMax-colMin)/2)
		if letter == "R":
			colMin = colMin+math.ceil((colMax-colMin)/2)

	return colMin

# Replacement for calculateCol/calculateRow
def toBinary(input):
	# https://stackoverflow.com/questions/3411771/best-way-to-replace-multiple-characters-in-a-string
	return int(input.replace('F', '0').replace('L', '0').replace('B', '1').replace('R', '1'), 2)

def part1():
	global boardingPasses, ids

	ids = []

	for boardingPass in boardingPasses:
		ids.append(toBinary(boardingPass[:7]) * 8 + toBinary(boardingPass[7:]))

	return(max(ids))

def part2():
	global boardingPasses, ids

	nonExistantIds = [x for x in range(min(ids), max(ids)) if x not in ids]

	for x in nonExistantIds:
		if x+1 in ids and x-1 in ids:
			return x

initialise()
print("Highest seat ID:", part1()) # 930
print("My seat ID:", part2()) # 515
