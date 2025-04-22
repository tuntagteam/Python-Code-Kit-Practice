user_input = input("Input : ")
nums = list(map(int, user_input.strip().split()))

total = sum(nums[::2])
print(total)


