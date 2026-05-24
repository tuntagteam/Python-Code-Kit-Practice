n = int(input())
keys = list(map(int, input().split()))
print(sum(1 for x in keys if x % 2 == 1))
