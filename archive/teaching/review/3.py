numbers = [2, 7, 8, 5, 10, 3, 6]
count_even = 0
for n in numbers:
    if n % 2 == 0:
        count_even += 1
print("มีจำนวนเลขคู่ทั้งหมด:", count_even)