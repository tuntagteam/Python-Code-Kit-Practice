s = input().strip()

start = s.index("S")

fruit_positions = []

for i, ch in enumerate(s):
    if ch == "#":
        fruit_positions.append(i)

left = min(fruit_positions)
right = max(fruit_positions)

distance_all = right - left

answer = distance_all + min(abs(start - left), abs(start - right))

print(answer)