n, k = map(int, input().split())

count = n // k

answer = k * count * (count + 1) // 2

print(answer)