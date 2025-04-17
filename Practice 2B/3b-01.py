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


nums1 = [2, 3, 5, 7]
print("Example 1:", nums1, "→", end=" ")
check_last_vs_second_last(nums1)

nums2 = [10, 5, 50, 250, 25]
print("Example 2:", nums2, "→", end=" ")
check_last_vs_second_last(nums2)
