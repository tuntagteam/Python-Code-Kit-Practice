n = int(input())
weights = list(map(int, input().split()))
print(max(weights) - min(weights))
