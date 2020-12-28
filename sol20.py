import utils
import re
import copy
from functools import reduce


def initialise():
    global images

    data = utils.loadInputFile("input_20.txt")

    images = {}
    currentImage = []

    for line in data:

        if line.startswith("Tile"):
            imageId = int(line[5:-1])

        elif line == "":
            images[imageId] = currentImage
            currentImage = []

        else:
            currentImage.append(list(line))

    images[imageId] = currentImage
    currentImage = []


def flipX(image):
    image = copy.deepcopy(image)
    tempImage = []
    for line in image:
        tempImage.append(list(reversed(line)))
    return tempImage


def flipY(image):
    image = copy.deepcopy(image)
    return list(reversed(image))


def rotate90(image):
    return [[image[i][j] for i in reversed(range(len(image)))] for j in (range(len(image)))]


def rotate270(image):
    return rotate90(rotate180(image))


def rotate180(image):
    tempImage = []
    tempImage = flipY(flipX(image))
    return tempImage


def matchY(imageA, imageB):
    return [x[-1] for x in imageA] == [x[0] for x in imageB]


def matchX(imageA, imageB):
    return imageA[-1] == imageB[0]


def printImage(image):

    print()
    for y in image:
        for x in y:
            print(x, end="")
        print()
    print()
    print()


def tileWithoutBorders(image):
    # return tile without the borders
    return [[image[j][i] for i in range(1, len(image)-1)] for j in range(1, len(image)-1)]


def joinImages(imageMap, fullImageTileReferences):
    finalImage = []
    for x in fullImageTileReferences:
        for z in range(len(tileWithoutBorders(imageMap[fullImageTileReferences[0][0]]))):
            imageLine = []
            for y in x:
                imageLine = imageLine + (tileWithoutBorders(imageMap[y])[z])
            finalImage.append(imageLine)

    return finalImage


def reconstructImage():
    global images

    allImageCombinations = {}

    # This works on the assumption that there is only 1 valid solution
    # builds a map of all possible tiles that align
    # then starts from the top left tile (pick one to start with)
    # then works right then right, eventually a new row
    # confirming they conform to the matches

    for imageAId, imageA in images.items():

        # key is the image identifier plus the orientation character
        # i.e. O = original, A = rotated 90 degrees
        allImageCombinations[str(imageAId) + "O"] = (imageA)
        allImageCombinations[str(imageAId) + "X"] = flipY(imageA)
        allImageCombinations[str(imageAId) + "Y"] = flipX(imageA)
        allImageCombinations[str(imageAId) + "A"] = rotate90(imageA)
        allImageCombinations[str(imageAId) + "B"] = rotate180(imageA)
        allImageCombinations[str(imageAId) + "C"] = rotate270(imageA)
        allImageCombinations[str(imageAId) + "D"] = flipX(rotate90(imageA))
        allImageCombinations[str(imageAId) + "E"] = flipY(rotate90(imageA))
        allImageCombinations[str(imageAId) + "F"] = flipX(rotate270(imageA))
        allImageCombinations[str(imageAId) + "G"] = flipY(rotate270(imageA))

    # initialise dictionaries to store the matches to the right and below
    # for the current image
    matchesR = {}
    matchesB = {}

    for x in allImageCombinations:
        for y in allImageCombinations:

            # if the image identifiers are different
            # i.e. key without orientation character
            if x[0:-1] != y[0:-1]:

                imageA = allImageCombinations[x]
                imageB = allImageCombinations[y]

                if matchX(imageA, imageB):
                    matchesB[x] = y

                if matchY(imageA, imageB):
                    matchesR[x] = y

                if matchX(imageB, imageA):
                    matchesB[y] = x

                if matchY(imageB, imageA):
                    matchesR[y] = x

    # THIS CODE CHECKS FOR A SINGLE SOLUTION ONLY WORKS WHEN MATCHESR AND B ARE LIST
    # for x in allImageCombinations:
    #     if len(set(matchesR[x])) > 1 or len(set(matchesB[x])) > 1:
    #         print(matchesR[x], matchesB[x],x)
    #         exit()

    cornerCombinations = list()

    # hard-coded dimension of the input tiles
    dimension = 12

    # for all image combinations, brute force attempt
    for x in allImageCombinations:

        valid = True
        fullImageTileReferences = []
        currentRow = [x]
        corner1 = x

        # iterate through the current row of tiles
        for i in range(dimension-1):
            # if the latest tile isn't in the list of right-side matches
            # break and stop processing row, as it's not correct
            if currentRow[-1] not in matchesR:
                valid = False
                break
            else:
                currentRow.append(matchesR[currentRow[-1]])

        #  if we can continue, i.e. have a suitable matching row
        if valid:
            # append the row to the list of rows
            fullImageTileReferences.append(currentRow)
            # the second corner is the end of the first row
            corner2 = currentRow[-1]

            # iterate through the current row of tiles
            for j in range(dimension-1):
                # only continue if the criteria for the row is valid
                if valid:
                    # check that the first tile in the current row is not the list of bottom-side matches
                    if currentRow[0] not in matchesB:
                        valid = False
                    else:
                        # update current row to be the tile matching the bottom-side
                        currentRow = [matchesB[currentRow[0]]]
                        # build out the current row with the list of right-side matches
                        # stop building if an invalid situation is encountered
                        for i in range(dimension-1):
                            if currentRow[-1] not in matchesR:
                                valid = False
                            else:
                                currentRow.append(matchesR[currentRow[-1]])
                # append the row to the list of rows
                fullImageTileReferences.append(currentRow)

        # if we are here and have a valid combination, we have finished matching the tiles
        if valid:
            # get the final 2 corners from the bottom row
            corner3 = currentRow[0]
            corner4 = currentRow[-1]

            # resolve the tile references to reconstruct the original image
            reconstructedImage = joinImages(allImageCombinations, fullImageTileReferences)

            # translate the reconstructed image into a string
            string = "".join(["".join(line) for line in reconstructedImage])

            matches = string
            prev = None
            # use regex to match the signature of the monster (and replace the #'s that form it)
            # 76 because 12*8 = 96 then - 20 (which is the length of the monster fragment)
            while(prev != matches):
                prev = matches
                matches = re.sub(r"(..................)#(..{76})#(....)##(....)##(....)###(.{76}.)#(..)#(..)#(..)#(..)#(..)#(...)", r"\g<1>0\g<2>0\g<3>00\g<4>00\g<5>000\g<6>0\g<7>0\g<8>0\g<9>0\g<10>0\g<11>0\g<12>", matches)

            if matches != string:
                remainingHashes = matches.count("#")

            # append the set of corners to the list of possible combinations
            cornerCombinations.append(set([corner1[0:-1], corner2[0:-1], corner3[0:-1], corner4[0:-1]]))

    for x in cornerCombinations:
        if len(x) == 4:
            # multiple the corners together (part 1 solution)
            cornerMultiplication = reduce(lambda x, y: int(x)*int(y), x)
        else:
            # if there isn't 4 corners, something has gone wrong
            raise Exception

    return cornerMultiplication, remainingHashes


initialise()
ans1, ans2 = reconstructImage()
print("Part 1:", ans1)
print("Part 2:", ans2)
