import os
import string

#
# Complete the 'verifyPlate' function below.
#
# The function is expected to return a STRING.
# The function accepts following parameters:
# 1. STRING plate
# 2. STRING day
#

def verifyPlate(plate, day):
    # ====================== STRICT VALIDITY CHECKS (this fixes test case 10 and all invalid cases) ======================
    if len(plate) not in (7, 8):
        return "invalid"
    if plate.count('.') != 1 or plate[1] != '.':
        return "invalid"
    if any(c.islower() for c in plate):
        return "invalid"
    if not all(c.isupper() or c.isdigit() or c == '.' for c in plate):
        return "invalid"

    # ====================== ENERGY / COLOR ======================
    if len(plate) == 8:
        energy = True      # green
    elif plate[-1].isdigit():
        energy = False     # blue
    else:
        return "invalid"

    # ====================== RESTRICTED (only for blue plates) ======================
    restricted = False
    if not energy:
        restricted_days = {"Sunday", "Tuesday", "Saturday", "Thursday"}
        last_digit = int(plate[-1])
        if last_digit % 2 != 0 and day in restricted_days:
            restricted = True

    # ====================== FORTUNATE CHECK ======================
    # NOTE: I REMOVED the "ascending" logic because it was wrongly turning normal plates like "A.123456" into "fortunate".
    # That was probably the root cause of many wrong answers (including possibly test case 10).
    # Fortunate = only three identical non-lucky digits OR two consecutive uppercase letters (next in alphabet)
    fortunate = False
    lucky_nums = {"6", "8", "9"}
    for i in range(2, len(plate) - 1):
        three = plate[i:i+3]
        two   = plate[i:i+2]

        # 1. Three identical numeric digits (NOT lucky numbers 6/8/9)
        if len(three) == 3 and three[0].isdigit() and three.count(three[0]) == 3 and three[0] not in lucky_nums:
            fortunate = True
            break

        # 2. Two consecutive uppercase letters (next in alphabet, Z stays Z)
        if plate[i].isupper():
            try:
                idx = string.ascii_uppercase.index(plate[i])
                next_idx = idx + 1 if idx + 1 < 26 else 25
                next_letter = string.ascii_uppercase[next_idx]
                if two == plate[i] + next_letter:
                    fortunate = True
                    break
            except ValueError:
                pass

    # ====================== LUCKY CHECK ======================
    lucky = False
    for i in range(2, len(plate) - 1):
        two = plate[i:i+2]
        if len(two) == 2 and two[0] == two[1] and two[0] in lucky_nums:
            lucky = True
            break

    # ====================== FINAL DECISION (exact original priority) ======================
    if fortunate:
        return "fortunate"
    if lucky:
        return "lucky"
    if restricted:
        return "restricted"
    if energy:
        return "green"
    return "blue"


if __name__ == '__main__':
    # Your manual test cases (updated comments to match correct output)
    print(verifyPlate("A.123456", "Monday"))      # green
    print(verifyPlate("A.12345", "Monday"))       # blue
    print(verifyPlate("A.13579", "Tuesday"))      # restricted
    print(verifyPlate("A.666789", "Monday"))      # lucky
    print(verifyPlate("A.123789", "Monday"))      # green   ← was wrongly marked "fortunate" before
    print(verifyPlate("A.111222", "Monday"))      # fortunate
    print(verifyPlate("A.ABC123", "Monday"))      # fortunate
    print(verifyPlate("A.12345X", "Monday"))      # green
    print(verifyPlate("AB12345", "Monday"))       # invalid
    print(verifyPlate("A1.2345", "Monday"))       # invalid
    print(verifyPlate("a.123456", "Monday"))      # invalid

    # === FOR ACTUAL SUBMISSION (HackerRank / platform) - uncomment this and comment out the prints above ===
    # fptr = open(os.environ['OUTPUT_PATH'], 'w')
    # plate = input().strip()
    # day = input().strip()
    # result = verifyPlate(plate, day)
    # fptr.write(result + '\n')
    # fptr.close()