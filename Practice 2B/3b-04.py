def has_sum_to_ten(nums, index=0, current_sum=0):
    if current_sum == 10:
        return True
    if index >= len(nums):
        return False

    if has_sum_to_ten(nums, index + 1, current_sum + nums[index]):
        return True

    if has_sum_to_ten(nums, index + 1, current_sum):
        return True

    return False


user_input = input("กรอกตัวเลข (คั่นด้วยช่องว่าง): ")
nums = list(map(int, user_input.strip().split()))

if has_sum_to_ten(nums):
    print("yes")
else:
    print("no")



