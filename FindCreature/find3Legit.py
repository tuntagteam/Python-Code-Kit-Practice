# ===============================
# Correct reference solution
# ===============================
def correct_findCreature(guess, deltas):
    row = guess // 10
    col = guess % 10

    d1 = deltas // 10
    d2 = deltas % 10

    vals = []

    for vr, hc in ((d1, d2), (d2, d1)):
        for sr in (-1, 1):
            for sc in (-1, 1):
                r = row + sr * vr
                c = col + sc * hc
                if 0 <= r <= 9 and 0 <= c <= 9:
                    vals.append(r * 10 + c)

    if not vals:
        return "NO_VALID"

    return f"{min(vals)} {max(vals)}"


# ===============================
# Student solution (original - unpatched)
# ===============================
def combineNumber(a: tuple):
    if a[0] >= 0:
        return a[0] * 10 + a[1]
    else:
        return a[0] * 10 - a[1]


def student_findCreature(guess: int, deltas: int):
    possibleLocations = []
    positions = []

    if (deltas > 99) or (guess > 99):
        return None

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
    for a in possibleLocations:
        a = combineNumber(a)
        if a < 100:
            if a > greatest:
                greatest = a

    lowest = 99
    for a in possibleLocations:
        a = combineNumber(a)
        if a >= 0:
            if a < lowest:
                lowest = a

    return f"{lowest} {greatest}"


# ===============================
# Brute-force tester
# ===============================
def test_all_cases():
    wrong = 0

    for guess in range(100):
        for deltas in range(100):
            expected = correct_findCreature(guess, deltas)
            student = student_findCreature(guess, deltas)

            if expected != student:
                wrong += 1

                if expected == "NO_VALID":
                    reason = "NO VALID POSITION"
                else:
                    e_min, e_max = map(int, expected.split())
                    s_min, s_max = map(int, student.split())

                    if e_min != s_min and e_max != s_max:
                        reason = "BOTH WRONG"
                    elif e_min != s_min:
                        reason = "MIN WRONG"
                    elif e_max != s_max:
                        reason = "MAX WRONG"
                    else:
                        reason = "UNKNOWN"

                print(
                    f"WRONG | guess={guess:02d}, deltas={deltas:02d} | "
                    f"expected={expected} | got={student} | reason={reason}"
                )

    print(f"\nTotal wrong cases: {wrong}")


# ===============================
# Run tests
# ===============================
if __name__ == "__main__":
    test_all_cases()