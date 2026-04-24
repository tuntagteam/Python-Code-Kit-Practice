n = int(input())
items = list(map(int, input().split()))

count = {}

for item in items:
    if item not in count:
        count[item] = 0
    count[item] += 1

answer = 0

for item in count:
    if count[item] > 1:
        answer += 1

print(answer)