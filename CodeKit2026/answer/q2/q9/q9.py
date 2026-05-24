n = int(input())
steps = list(map(int, input().split()))
count = 0
for i in range(1, n):
    if steps[i] > steps[i - 1]:
        count += 1
print(count)
