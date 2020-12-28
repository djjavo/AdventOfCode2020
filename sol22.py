import utils
import copy


def initialise():
    global playerOneDeck, playerTwoDeck

    deck = utils.loadInputFile("input_22.txt")

    for idx, card in enumerate(deck):
        if card == "":
            break

    playerOneDeck = deck[1:idx]
    playerTwoDeck = deck[idx+2:]

    playerOneDeck = [int(x) for x in playerOneDeck]
    playerTwoDeck = [int(x) for x in playerTwoDeck]

    assert(len(playerOneDeck) == len(playerTwoDeck))


def subGame(playerOneDeck, playerTwoDeck):
    deckHistory = []

    playerOneDeck = copy.deepcopy(playerOneDeck)
    playerTwoDeck = copy.deepcopy(playerTwoDeck)

    while len(playerOneDeck) > 0 and len(playerTwoDeck) > 0:

        currentDeckStatus = playerOneDeck + ["|"] + playerTwoDeck

        if currentDeckStatus in deckHistory:
            # defaults to player one winning
            break
        else:
            deckHistory.append(currentDeckStatus)

        playerOneCard = playerOneDeck.pop(0)
        playerTwoCard = playerTwoDeck.pop(0)

        if len(playerOneDeck) >= playerOneCard and len(playerTwoDeck) >= playerTwoCard:
            if subGame(playerOneDeck[:playerOneCard], playerTwoDeck[:playerTwoCard]):
                playerOneDeck.append(playerOneCard)
                playerOneDeck.append(playerTwoCard)
            else:
                playerTwoDeck.append(playerTwoCard)
                playerTwoDeck.append(playerOneCard)

        elif playerOneCard > playerTwoCard:
            playerOneDeck.append(playerOneCard)
            playerOneDeck.append(playerTwoCard)
        elif playerTwoCard > playerOneCard:
            playerTwoDeck.append(playerTwoCard)
            playerTwoDeck.append(playerOneCard)
        else:
            raise Exception

    # return True if player one wins
    return len(playerOneDeck) > 0


def processRound(playerOneDeck, playerTwoDeck):
    playerOneCard = playerOneDeck.pop(0)
    playerTwoCard = playerTwoDeck.pop(0)

    if playerOneCard > playerTwoCard:
        playerOneDeck.append(playerOneCard)
        playerOneDeck.append(playerTwoCard)
    elif playerTwoCard > playerOneCard:
        playerTwoDeck.append(playerTwoCard)
        playerTwoDeck.append(playerOneCard)
    else:
        raise Exception


def processRecursiveRound(playerOneDeck, playerTwoDeck):

    playerOneCard = playerOneDeck.pop(0)
    playerTwoCard = playerTwoDeck.pop(0)

    if playerOneCard == 4 and playerTwoCard == 3:
        print("popping: ", playerOneCard, playerTwoCard)

    if len(playerOneDeck) >= playerOneCard and len(playerTwoDeck) >= playerTwoCard:

        if subGame(playerOneDeck[:playerOneCard], playerTwoDeck[:playerTwoCard]):
            playerOneDeck.append(playerOneCard)
            playerOneDeck.append(playerTwoCard)
        else:
            playerTwoDeck.append(playerTwoCard)
            playerTwoDeck.append(playerOneCard)

    elif playerOneCard > playerTwoCard:
        playerOneDeck.append(playerOneCard)
        playerOneDeck.append(playerTwoCard)
    elif playerTwoCard > playerOneCard:
        playerTwoDeck.append(playerTwoCard)
        playerTwoDeck.append(playerOneCard)
    else:
        raise Exception


def calculateScore(playerOneDeck, playerTwoDeck):
    score = 0

    if len(playerOneDeck) > 0:
        for idx, card in enumerate(playerOneDeck):
            score += (card * (len(playerOneDeck) - idx))
    else:
        for idx, card in enumerate(playerTwoDeck):
            score += (card * (len(playerTwoDeck) - idx))

    return score


def part1():
    global playerOneDeck, playerTwoDeck

    while len(playerOneDeck) > 0 and len(playerTwoDeck) > 0:
        processRound(playerOneDeck, playerTwoDeck)

    return calculateScore(playerOneDeck, playerTwoDeck)


def part2():
    global playerOneDeck, playerTwoDeck

    while len(playerOneDeck) > 0 and len(playerTwoDeck) > 0:
        processRecursiveRound(playerOneDeck, playerTwoDeck)

    return calculateScore(playerOneDeck, playerTwoDeck)


initialise()
print("Part 1:", part1())  # 32366
initialise()
print("Part 2:", part2())  # 30891
