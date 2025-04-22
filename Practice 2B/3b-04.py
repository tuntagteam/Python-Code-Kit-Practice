user_input = input("กรอกตัวเลข (คั่นด้วยช่องว่าง): ")
nums = list(map(int, user_input.strip().split()))

n = len(nums)
found = False

for i in range(1, 2 ** n):
    subset_sum = 0
    for j in range(n):
        if (i >> j) & 1:  
            subset_sum += nums[j]
    if subset_sum == 10:
        found = True
        break

if found:
    print("yes")
else:
    print("no")