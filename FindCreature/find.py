def findCreature(guess, deltas):
    row = guess // 10
    col = guess % 10

    d1 = deltas // 10
    d2 = deltas % 10

    minCell = float('inf')
    maxCell = float('-inf')

    v = [d1, d2]
    h = [d2, d1]

    for i in range(2):
        for vr in (-1, 1):
            for hc in (-1, 1):
                r = row + vr * v[i]
                c = col + hc * h[i]

                if 0 <= r <= 9 and 0 <= c <= 9:
                    cell = r * 10 + c
                    if cell < minCell:
                        minCell = cell
                    if cell > maxCell:
                        maxCell = cell

    print(minCell, maxCell)


def main():
    guess, deltas = map(int, input().split())
    findCreature(guess, deltas)


if __name__ == "__main__":
    main()