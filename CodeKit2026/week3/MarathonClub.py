n, p = map(int, input().split())
times = list(map(int, input().split()))

target = times[p - 1]

rank = 1

for t in times:
    if t < target:
        rank += 1

print(rank)