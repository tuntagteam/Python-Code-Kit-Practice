from itertools import combinations

user_input = input("กรอกตัวเลข (คั่นด้วยช่องว่าง): ")
nums = list(map(int, user_input.strip().split()))

found = False  

for r in range(1, len(nums) + 1):
    for subset in combinations(nums, r):
        if sum(subset) == 10:
            found = True
            break
    if found:
        break

if found:
    print("yes")
else:
    print("no")


    