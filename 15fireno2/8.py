numbers = [1, 2, 2, 3, 4, 4]
seen = set()
result = []
for num in numbers:
    if num not in seen:
        seen.add(num)
        result.append(num)
print("Without duplicates:", result)