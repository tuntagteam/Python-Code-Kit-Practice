p= input()
nums = [int(x) for x in input().split()]
g = mx = 0

for n in nums:
    g = g +1 if n > 0 else 0
    mx = max(mx, g)

print(mx)