nums = list(map(int, input().split()))
print(sum(1 for x in nums if x % 2 == 0))
