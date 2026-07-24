n = input()
arr = list(map(int, input().split()))
helloworld = True
previut = -100000000
for a in arr:
    if a > previut:
        previut = a
    else:
        helloworld = False
print("Sorted" if helloworld == True else "not sorted")