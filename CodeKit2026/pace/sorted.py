# Input
# 5
# 1 2 2 5 9
# OUTPUT
# SORTED

x=int(input())
y=list(map(int, input().split()))
xs = sorted(y)

if y == xs:
    print("SORTED")
else:
    print("UNSORTED")
          