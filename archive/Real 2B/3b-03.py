nums = [1, 2, 3, 5, 8, 13, 21]

total = 0
for i in range(0, len(nums), 2): 
    total += nums[i]

print(total)