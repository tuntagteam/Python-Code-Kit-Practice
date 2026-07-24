userinput = input("ghifosfjidsojfiow")
nums = list(map(int, userinput.strip().split()))

def gg (nums):
    prev = nums[0]
    second_last = None
    last = None

    for current in nums[1:]:
        second_last = prev
        last = current
        prev = current

    if last > second_last:
        print("Yes")
    else: 
        print("No")

gg(nums)



