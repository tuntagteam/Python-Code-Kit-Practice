numbers = [4, 7, 2, 9, 10, 13]

even_count = 0

for number in numbers:
    if number % 2 == 0:
        even_count += 1

print("There are", even_count, "even numbers.")
