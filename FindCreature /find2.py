def combineNumber(a: tuple):
    if a[0] >= 0:
        return a[0] * 10 + a[1]
    else:
        return a[0] * 10 - a[1]


def findCreature(guess: int, deltas: int):
    possibleLocations = []
    positions = []

    if (deltas > 99) or (guess > 99):
        return

    deltasTensDigit = deltas // 10 * 10

    pos1Col = deltasTensDigit // 10
    pos1Row = deltas - deltasTensDigit
    positions.append((pos1Row, pos1Col))

    pos2Col = deltas - deltasTensDigit
    pos2Row = deltasTensDigit // 10
    positions.append((pos2Row, pos2Col))

    guessTensDigit = guess // 10 * 10
    gRow = guessTensDigit // 10
    gCol = guess - guessTensDigit

    for pos in positions:
        possibleLocations.append((gRow + pos[0], gCol + pos[1]))
        possibleLocations.append((gRow - pos[0], gCol - pos[1]))
        possibleLocations.append((gRow - pos[0], gCol + pos[1]))
        possibleLocations.append((gRow + pos[0], gCol - pos[1]))

    greatest = 0
    for r, c in possibleLocations:
        if 0 <= r <= 9 and 0 <= c <= 9:
            a = combineNumber((r, c))
            if a > greatest:
                greatest = a

    lowest = 99
    for r, c in possibleLocations:
        if 0 <= r <= 9 and 0 <= c <= 9:
            a = combineNumber((r, c))
            if a < lowest:
                lowest = a

    print(lowest, greatest)
    return str(lowest) + " " + str(greatest)


if __name__ == "__main__":
    guess = int(input())
    deltas = int(input())
    findCreature(guess, deltas)