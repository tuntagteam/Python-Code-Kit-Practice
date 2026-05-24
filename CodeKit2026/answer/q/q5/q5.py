n, k = map(int, input().split())
scores = list(map(int, input().split()))
print(sum(1 for s in scores if s >= k))
