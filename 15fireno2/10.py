from collections import Counter
numbers = [1, 2, 2, 3]
count = Counter(numbers)
total = len(numbers)
for k, v in count.items():
    print(f"{k}: {v/total:.2%}")