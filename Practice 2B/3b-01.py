def check_last_vs_second_last(nums):
    prev = nums[0]
    second_last = None
    last = None

    for current in nums[1:]:
        second_last = prev
        last = current
        prev = current

    if last > second_last:
        print("yes")
    else:
        print("no")

user_input = input("Input the number with a space Example => 2 3 5 7 : ")
nums = list(map(int, user_input.strip().split()))

print("Input :", nums, "→", end=" ")
check_last_vs_second_last(nums)


