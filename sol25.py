import utils


def initialise():
    global publicKeys, cardPublicKey, doorPublicKey

    publicKeys = utils.loadInputFile("input_25.txt")

    cardPublicKey = int(publicKeys[0])
    doorPublicKey = int(publicKeys[1])

    print("card public key:", cardPublicKey)
    print("door public key:", doorPublicKey)


def part1():
    # The card transforms the subject number of 7 according to the card's
    # secret loop size. The result is called the card's public key.

    # The door transforms the subject number of 7 according to the door's
    # secret loop size. The result is called the door's public key.

    # The card and door use the wireless RFID signal to transmit the two
    # public keys (your puzzle input) to the other device. Now, the card has
    # the door's public key, and the door has the card's public key. Because
    # you can eavesdrop on the signal, you have both public keys, but neither
    # device's loop size.

    # The card transforms the subject number of the door's public key according
    # to the card's loop size. The result is the encryption key.

    # The door transforms the subject number of the card's public key according
    # to the door's loop size. The result is the same encryption key as the card
    # calculated.

    subject = 7
    value = 1

    for i in range(100000000):
        value = value * subject
        value = value % 20201227

        if value == cardPublicKey:
            cardLoopSize = i
            print("card loop size:", cardLoopSize)
            break

    value = 1

    for i in range(100000000):
        value = value * subject
        value = value % 20201227

        if value == doorPublicKey:
            doorLoopSize = i
            print("door loop size:", doorLoopSize)
            break

    value = 1
    subject = cardPublicKey
    for i in range(doorLoopSize+1):
        value = value * subject
        value = value % 20201227

    encryptionKey = value

    value = 1
    subject = doorPublicKey
    for i in range(cardLoopSize+1):
        value = value * subject
        value = value % 20201227

    assert(encryptionKey == value)
    print("encryption key:", encryptionKey)


def part2():
    print("Merry Christmas!")


initialise()
part1()
part2()
