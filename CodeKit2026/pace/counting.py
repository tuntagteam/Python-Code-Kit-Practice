# 8 
# 101 205 101 300 205 205 500 600
# 101 , 205
# 2

from collections import Counter
x=int(input())
y = input().split()
c = Counter(y)
a = sum(1 for v in c.values() if v > 1)
print(a)