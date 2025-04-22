user_input = input("กรอกตัวเลข (คั่นด้วยช่องว่าง): ")
nums = list(map(int, user_input.strip().split()))

count = 0

for i in range(len(nums) - 1):
    if nums[i] + nums[i + 1] == 10:
        count += 1

print(count)