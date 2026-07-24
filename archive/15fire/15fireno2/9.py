numbers = [2, 7, 11, 15]
target = 9
seen = set()
for num in numbers:
    if target - num in seen:
        print("Pair:", (target - num, num))
        break
    seen.add(num)
else:
    print("No pair found.")