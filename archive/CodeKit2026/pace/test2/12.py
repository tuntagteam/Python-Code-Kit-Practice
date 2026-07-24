y = list(map(int, input().split()))
x = list(map(int, input().split()))

a=0

for i in range(y[0]):
    for j in range(i+1, y[0]):
        if x[i] + x[j] == y[1]:
            a=1
            break

    if a == 1:
        break

if a == 1:
    print("yes")
else:
    print("no")