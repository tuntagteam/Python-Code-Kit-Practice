n = int(input())

count = 0
for i in range(n, 0 , -2):
    if count == 3:
        break

    for j in range(i):
        print("*", end=" ")
    print()

    count += 1 