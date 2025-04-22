user_input = input("กรอกตัวเลข (คั่นด้วยช่องว่าง): ")
nums = list(map(int, user_input.strip().split()))

even_count = 0
for num in nums:
    if num % 2 == 0:
        even_count += 1

print(even_count)


