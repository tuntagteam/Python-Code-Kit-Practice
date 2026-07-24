n = int(input())
codes = list(map(int, input().split()))
print(sum(1 for x in codes if x % 2 == 0))
