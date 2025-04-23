import math

user_input = input("กรอกตัวเลข (คั่นด้วยช่องว่าง): ")
nums = list(map(int, user_input.strip().split()))

even_count = 0
for num in nums:
    if num % 2 == 0:
        even_count += 1

even_float = float(even_count)
print("kkk: {:.4f}".format(even_float))

rounded_up = math.ceil(even_float)
print("kkk:", rounded_up)