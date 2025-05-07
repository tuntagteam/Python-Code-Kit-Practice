from collections import Counter
numbers = [1, 2, 2, 3, 3, 3, 4]
count = Counter(numbers)
max_freq = max(count.values())
modes = [k for k, v in count.items() if v == max_freq]
print("Mode(s):", modes)