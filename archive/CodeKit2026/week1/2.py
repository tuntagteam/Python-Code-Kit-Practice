n = int(input())
missions = []

for _ in range(n):
    start, end = map(int, input().split())
    missions.append((start, end))

def endsort(item):
    return item[1]

missions.sort(key=endsort)
count = 0
last_end = 0

for start, end in missions:
    if start >= last_end:
        count += 1
        last_end = end

print(count)