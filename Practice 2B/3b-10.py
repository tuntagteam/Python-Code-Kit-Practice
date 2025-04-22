user_input = input("กรอกตัวเลข (คั่นด้วยช่องว่าง): ")
nums = list(map(int, user_input.strip().split()))

if len(nums) < 2:
    print("กรุณาใส่อย่างน้อย 2 ตัวเลข")
else:
    max_sum = nums[0] + nums[1]  

    for i in range(1, len(nums) - 1):
        current_sum = nums[i] + nums[i + 1]
        if current_sum > max_sum:
            max_sum = current_sum

    print(max_sum)