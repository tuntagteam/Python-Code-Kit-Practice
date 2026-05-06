rows = 13
cols = 50

for r in range(rows):
    line = ""

    for c in range(cols):
        if r < 7 and c < 20:
            if (r + c) % 2 == 0:
                line += "*"
            else:
                line += " "
        else:
            if r % 2 == 0:
                line += "="
            else:
                line += " "

    print(line)