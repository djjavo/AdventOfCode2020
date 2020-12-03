import utils

def initialise():
	global data, dataMap

	data = utils.loadInputFile("input_1.txt")
	# convert to int
	data = [int(x) for x in data]

	dataMap = dict()

	for x in data:
		if x not in dataMap:
			dataMap[x] = 1

def part1():
	global data, dataMap

	for x in data:
		if 2020-x in dataMap:
			print(x,2020-x)
			return (2020-x)*x

def part2():
	global data, dataMap

	for x in data:
		for y in data:
			# Assume no duplicates
			if (2020-x)-y in dataMap and x != y:
				print(x,y,2020-x-y)
				return (2020-x-y)*y*x

initialise()

t = utils.Timer("part1")
t.start()
print(part1()) # 864864 (1404 616)
t.stop()

t = utils.Timer("part2")
t.start()
print(part2()) # 281473080 (857 483 680)
t.stop()
