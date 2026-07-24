n = int(input())
points = list(map(int, input().split()))
count = 0
for i in range(1, n):
    if points[i] > points[i - 1]:
        count += 1
print(count)
